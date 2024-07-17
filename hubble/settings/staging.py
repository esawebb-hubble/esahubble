import copy

from .common import *

# Make this unique, and don't share it with anybody.
SECRET_KEY = "sssmvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

DATABASES = copy.deepcopy(DATABASES)
DATABASES['default']['HOST'] = ""
DATABASES['default']['PASSWORD'] = ""


EMAIL_HOST = 'smtphost.hq.eso.org'
EMAIL_PORT = '25'
EMAIL_SUBJECT_PREFIX = '[HUBBLE-INTEGRATION]'


CELERY_BROKER_URL = ''


# Shop:
ORDER_PREFIX = "hbi"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': 'nova',
        'LOCATION': [
            '',
        ],
        'TIMEOUT': 86400
    },
}
