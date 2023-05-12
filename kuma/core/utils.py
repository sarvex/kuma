import functools
import logging
import os
import random
import re
import tempfile
import time
from itertools import islice

import commonware.log
import lockfile
from celery import chain, chord
from polib import pofile

from django.conf import settings
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import _get_queryset
from django.utils.encoding import force_unicode
from django.utils.http import urlencode

from taggit.utils import split_strip

from .cache import memcache
from .jobs import IPBanJob


# this is not intended to be an all-knowing IP address regex
IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


log = commonware.log.getLogger('kuma.core.utils')


def get_ip(request):
    """
    Retrieves the remote IP address from the request data.  If the user is
    behind a proxy, they may have a comma-separated list of IP addresses, so
    we need to account for that.  In such a case, only the first IP in the
    list will be retrieved.  Also, some hosts that use a proxy will put the
    REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
    IP from the proper place.

    **NOTE** This function was taken from django-tracking (MIT LICENSE)
             http://code.google.com/p/django-tracking/
    """

    # if neither header contain a value, just use local loopback
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # make sure we have one and only one IP
        try:
            ip_address = IP_RE.match(ip_address)
            ip_address = ip_address.group(0) if ip_address else '10.0.0.1'
        except IndexError:
            pass

    return ip_address


def paginate(request, queryset, per_page=20):
    """Get a Paginator, abstracting some common paging actions."""
    paginator = Paginator(queryset, per_page)

    # Get the page from the request, make sure it's an int.
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    # Get a page of results, or the first page if there's a problem.
    try:
        paginated = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paginated = paginator.page(1)

    base = request.build_absolute_uri(request.path)

    items = [(k, v) for k in request.GET if k != 'page'
             for v in request.GET.getlist(k) if v]

    qsa = urlencode(items)

    paginated.url = f'{base}?{qsa}'
    return paginated


def smart_int(string, fallback=0):
    """Convert a string to int, with fallback for invalid strings or types."""
    try:
        return int(float(string))
    except (ValueError, TypeError):
        return fallback


def strings_are_translated(strings, locale):
    # http://stackoverflow.com/a/24339946/571420
    pofile_path = os.path.join(settings.ROOT, 'locale', locale, 'LC_MESSAGES',
                               'messages.po')
    try:
        po = pofile(pofile_path)
    except IOError:  # in case the file doesn't exist or couldn't be parsed
        return False
    all_strings_translated = True
    for string in strings:
        if not any(e for e in po if e.msgid == string and
                   (e.translated() and 'fuzzy' not in e.flags)
                   and not e.obsolete):
            all_strings_translated = False
    return all_strings_translated


def file_lock(prefix):
    """
    Decorator that only allows one instance of the same command to run
    at a time.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            name = '_'.join((prefix, f.__name__) + args)
            file = os.path.join(tempfile.gettempdir(), name)
            lock = lockfile.FileLock(file)
            try:
                # Try to acquire the lock without blocking.
                lock.acquire(0)
            except lockfile.LockError:
                log.warning(f'Aborting {name}; lock acquisition failed.')
                return 0
            else:
                # We have the lock, call the function.
                try:
                    return f(self, *args, **kwargs)
                finally:
                    lock.release()

        return wrapper

    return decorator


def generate_filename_and_delete_previous(ffile, name, before_delete=None):
    """Generate a new filename for a file upload field; delete the previously
    uploaded file."""

    new_filename = ffile.field.generate_filename(ffile.instance, name)

    try:
        # HACK: Speculatively re-fetching the original object makes me feel
        # wasteful and dirty. But, I can't think of another way to get
        # to the original field's value. Should be cached, though.
        # see also - http://code.djangoproject.com/ticket/11663#comment:10
        orig_instance = ffile.instance.__class__.objects.get(
            id=ffile.instance.id
        )
        orig_field_file = getattr(orig_instance, ffile.field.name)
        orig_filename = orig_field_file.name

        if orig_filename and new_filename != orig_filename:
            if before_delete:
                before_delete(orig_field_file)
            orig_field_file.delete()
    except ffile.instance.__class__.DoesNotExist:
        pass

    return new_filename


class MemcacheLockException(Exception):
    pass


class MemcacheLock(object):
    def __init__(self, key, attempts=1, expires=60 * 60 * 3):
        self.key = f'lock_{key}'
        self.attempts = attempts
        self.expires = expires
        self.cache = memcache

    def locked(self):
        return bool(self.cache.get(self.key))

    def acquire(self):
        for i in xrange(0, self.attempts):
            if stored := self.cache.add(self.key, 1, self.expires):
                return True
            if i != self.attempts - 1:
                sleep_time = (((i + 1) * random.random()) + 2 ** i) / 2.5
                logging.debug('Sleeping for %s while trying to acquire key %s',
                              sleep_time, self.key)
                time.sleep(sleep_time)
        raise MemcacheLockException(f'Could not acquire lock for {self.key}')

    def release(self):
        self.cache.delete(self.key)


def get_object_or_none(klass, *args, **kwargs):
    """
    A tool like Django's get_object_or_404 but returns None in case
    of a DoesNotExist exception.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def parse_tags(tagstring, sorted=True):
    """
    Parses tag input, with multiple word input being activated and
    delineated by commas and double quotes. Quotes take precedence, so
    they may contain commas.

    Returns a sorted list of unique tag names, unless sorted=False.

    Ported from Jonathan Buchanan's `django-tagging
    <http://django-tagging.googlecode.com/>`_
    """
    if not tagstring:
        return []

    tagstring = force_unicode(tagstring)

    # Special case - if there are no commas or double quotes in the
    # input, we don't *do* a recall... I mean, we know we only need to
    # split on spaces.
    if u',' not in tagstring and u'"' not in tagstring:
        words = list(split_strip(tagstring, u' '))
        if sorted:
            words.sort()
        return words

    words = []
    buffer = []
    # Defer splitting of non-quoted sections until we know if there are
    # any unquoted commas.
    to_be_split = []
    saw_loose_comma = False
    open_quote = False
    i = iter(tagstring)
    try:
        while True:
            c = i.next()
            if c == u'"':
                if buffer:
                    to_be_split.append(u''.join(buffer))
                    buffer = []
                # Find the matching quote
                open_quote = True
                c = i.next()
                while c != u'"':
                    buffer.append(c)
                    c = i.next()
                if buffer:
                    if word := u''.join(buffer).strip():
                        words.append(word)
                    buffer = []
                open_quote = False
            else:
                if not saw_loose_comma and c == u',':
                    saw_loose_comma = True
                buffer.append(c)
    except StopIteration:
        # If we were parsing an open quote which was never closed treat
        # the buffer as unquoted.
        if buffer:
            if open_quote and u',' in buffer:
                saw_loose_comma = True
            to_be_split.append(u''.join(buffer))
    if to_be_split:
        delimiter = u',' if saw_loose_comma else u' '
        for chunk in to_be_split:
            words.extend(split_strip(chunk, delimiter))
    words = list(words)
    if sorted:
        words.sort()
    return words


def chunked(iterable, n):
    """Return chunks of n length of iterable.

    If ``len(iterable) % n != 0``, then the last chunk will have
    length less than n.

    Example:

    >>> chunked([1, 2, 3, 4, 5], 2)
    [(1, 2), (3, 4), (5,)]

    :arg iterable: the iterable
    :arg n: the chunk length

    :returns: generator of chunks from the iterable
    """
    iterable = iter(iterable)
    while 1:
        if t := tuple(islice(iterable, n)):
            yield t
        else:
            return


def chord_flow(pre_task, tasks, post_task):

    if not settings.CELERY_ALWAYS_EAGER:
        return chain(pre_task, chord(header=tasks, body=post_task))
    # Eager mode and chords don't get along. So we serialize
    # the tasks as a workaround.
    tasks.insert(0, pre_task)
    tasks.append(post_task)
    return chain(*tasks)


def limit_banned_ip_to_0(group, request):
    ip = get_ip(request)
    return IPBanJob().get(ip)
