import shlex
import urllib2
from StringIO import StringIO

from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest

from nose.tools import eq_
from nose import SkipTest

from kuma.core.tests import KumaTestCase

from ..context_processors import next_url


def parse_robots(base_url):
    """ Given a base url, retrieves the robot.txt file and
        returns a list of rules. A rule is a tuple.
        Example:
        [("User-Agent", "*"), ("Crawl-delay", "5"),
         ...
         ("Disallow", "/template")]

        Tokenizes input to whitespace won't break
        these acceptance tests.
    """
    rules = []
    robots = shlex.shlex(urllib2.urlopen(f"{base_url}/robots.txt"))
    robots.whitespace_split = True
    while token := robots.get_token():
        rule = None
        if token[-1] == ':':
            rule = token[:-1], robots.get_token()
        if rule:
            rules.append(rule)
    return rules


def _make_request(path):
    req = WSGIRequest({
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': path,
        'wsgi.input': StringIO()})
    req.user = AnonymousUser()
    return req


class TestDevMoRobots(KumaTestCase):
    """ These are really acceptance tests, but we seem to lump
        together unit, integration, regression, and
        acceptance tests """
    def test_production(self):
        # Skip this test, because it runs against external sites and breaks.
        raise SkipTest()

    def test_stage_bug607996(self):
        # Skip this test, because it runs against external sites and breaks.
        raise SkipTest()


class TestDevMoNextUrl(KumaTestCase):
    """ Tests that the next_url value is properly set,
    including query string """
    def test_basic(self):
        path = '/one/two'
        eq_(next_url(_make_request(path))['next_url'], path)

    def test_querystring(self):
        path = '/one/two?something'
        eq_(next_url(_make_request(path))['next_url'], path)
