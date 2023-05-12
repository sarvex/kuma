from nose.tools import ok_

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

from kuma.core.tests import KumaTestCase

from ..models import UserProfile


random_str = User.objects.make_random_password


class UserTestCase(KumaTestCase):
    """Base TestCase for the users app test cases."""
    fixtures = ['test_users.json']


def profile(user, **kwargs):
    """Return a saved profile for a given user."""
    return UserProfile.objects.get(user=user)


def user(save=False, **kwargs):
    if 'username' not in kwargs:
        kwargs['username'] = random_str(length=15)
    password = kwargs.pop('password', 'password')
    user = User(**kwargs)
    user.set_password(password)
    if save:
        user.save()
    return user


def email(save=False, **kwargs):
    if 'user' not in kwargs:
        kwargs['user'] = user(save=True)
    if 'email' not in kwargs:
        kwargs['email'] = f'{random_str()}@{random_str()}.com'
    email = EmailAddress(**kwargs)
    if save:
        email.save()
    return email


def verify_strings_in_response(test_strings, response):
    for test_string in test_strings:
        ok_(
            test_string in response.content,
            msg=f"Expected '{test_string}' in content.",
        )


def verify_strings_not_in_response(test_strings, response):
    for test_string in test_strings:
        ok_(
            test_string not in response.content,
            msg=f"Found unexpected '{test_string}' in content.",
        )
