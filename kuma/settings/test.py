from kuma.settings.common import *  # noqa

DEBUG = False
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
ES_LIVE_INDEX = False
ES_URLS = ['localhost:9200']

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)

INSTALLED_APPS += (
    'kuma.core.tests.taggit_extras',
    'kuma.actioncounters.tests',
)
BANISH_ENABLED = False
