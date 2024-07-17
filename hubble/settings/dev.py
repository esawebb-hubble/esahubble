import sys
import copy

from .common import *

SECRET_KEY = "g6ymvx$i1sv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SECURE_PROXY_SSL_HEADER = None

ALLOWED_HOSTS = ['*']


def show_toolbar(request):
    '''
    The default callback checks if the IP is internal, but docker's IP
    addresses are not in INTERNAL_IPS, so we force the display in dev mode
    '''
    return True


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    'SKIP_TEMPLATE_PREFIXES': (
        'django/forms/widgets/',
        'admin/widgets/',
        'menus/',
        'pipeline/',
    ),
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
#   'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
#   'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

##################
# DATABASE SETUP #
##################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hubble',
        'USER': 'hubble',
        'PASSWORD': 'hubble',
        'HOST': 'hubble-db',
        'PORT': 5432,
    }
}

##########
# CACHE  #
##########
CACHES = {
    'notdefault': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': 'hubble',
        'LOCATION': [
            'cache:11211',
        ],
        'TIMEOUT': 86400
    },
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

##########
# CELERY #
##########
CELERY_BROKER_URL = 'amqp://hubble:hubble@broker:5672/'

# Avoid infinite wait times and retries
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}


SERVE_STATIC_MEDIA = True


#########
# EMAIL #
#########
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

##################
# CATPCHA #
##################
# This keys are provided by google for testing purposes
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
