# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from __future__ import absolute_import
import os
import re

# pylint: disable=no-name-in-module
from celery.schedules import crontab

# We can't use ugettext from django.utils.translation as it will itself
# load the settings resulting in a ImproperlyConfigured error
ugettext = lambda s: s


import djangoplicity.crosslinks
from djangoplicity.contentserver import CDN77ContentServer

#############################
# ENVIRONMENT CONFIGURATION #
#############################
SHORT_NAME = 'hubble'
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARCHIVE_IMPORT_ROOT = '%s/import' % ROOT
PRJBASE = "%s/spacetelescope" % ROOT
PRJNAME = 'spacetelescope.org'
DJANGOPLICITY_ROOT = "%s/.local/lib/python3.8/site-packages/djangoplicity" % ROOT
LOG_DIR = "%s/logs" % ROOT
TMP_DIR = "%s/tmp" % ROOT
SHARED_DIR = "%s/shared" % ROOT
GA_ID = "UA-2368492-6"
FACEBOOK_APP_ID = "144508505618279"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
VIDEOS_THUMBNAIL_POSITION = 'middle'  # Used to generated thumbnails of videos when it's provideo

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


###################
# ERROR REPORTING #
###################
class internal_ips( list ):
    """
    INTERNAL_IPS container that allows more specific check if an IP is an internal IP.

    Each entry must be a complete ( a.b.c.d ) or partial ( a.b.c. ) IP address. If
    an entry is prefixed with tilde ( ~ ) it means the IP address is excluded. This allows
    you e.g include the entire range 134.171. but exclude certain subnets and specific IP
    addresses.
    """
    def __contains__( self, key ):
        is_internal = False
        for ip in self:
            if ip[0] == '~':
                if key.startswith( ip[1:] ):
                    return False
            else:
                if key.startswith( ip ):
                    is_internal = True
        return is_internal


INTERNAL_IPS = internal_ips( [
    '127.0.0.1',
    '134.171.',
    '~134.171.86.',
    '~134.171.172.',
    '~134.171.185.',
    '~134.171.80.85',
] )

GARCHING_INTERNAL_IPS = (
    '134.171.0.0/18',
    '134.171.64.0/20',
    '127.0.0.1',
)

SITE_ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')
DEBUG = SITE_ENVIRONMENT == 'dev'
DEBUG_TOOLBAR = DEBUG
DEBUG_TOOLBAR_CONFIG = {}
DEBUG_TOOLBAR_PANELS = []

HUBBLE_DEFAULT_EMAIL = 'web@esahubble.org'

ADMINS = (
    ('Web team ESAHubble', HUBBLE_DEFAULT_EMAIL),
)
MANAGERS = ADMINS

SERVE_STATIC_MEDIA = False


##################
# DATABASE SETUP #
##################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spacetelescope',
        'USER': 'spacetelescope',
        'PASSWORD': '',
        'HOST': 'localhost',
        'CONN_MAX_AGE': 600,
    }
}

########################
# INTERNATIONALIZAION  #
########################
# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes

LANGUAGES = (
    ( 'en', ugettext( 'English' ) ),
)

LANGUAGE_CODE = 'en'

FORMAT_MODULE_PATH = 'spacetelescope.formats'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
USE_L10N = True

#LOCALE_PATHS = ( DJANGOPLICITY_ROOT + "/locale", PRJBASE + "/locale", )

# Default date and time formats (con be overridden by locale)
DATE_FORMAT = ugettext('j F Y')
DATE_LONG_FORMAT = ugettext('j F Y')
DATETIME_FORMAT = ugettext('M j, Y, H:i T')
DATETIME_LONG_FORMAT = ugettext('M j, Y y, H:i T')
MONTH_DAY_FORMAT = ugettext('F j')
TIME_FORMAT = ugettext('H:i T')
YEAR_MONTH_FORMAT = ugettext('F Y')
WIDGET_FORMAT = ugettext("j/m/Y")

# MEDIA
MEDIA_ROOT = os.path.join(ROOT, 'media')
MEDIA_URL = '/media/'

# STATIC FILES (CSS, JavaScript, Images)
# See: https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(ROOT, 'static')
STATIC_URL = '/assets/'


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# ADMIN_MEDIA_PREFIX is necessary due to satchmo current version. TODO: remove when Satchmo is upgraded
ADMIN_MEDIA_PREFIX = "/static/app/admin/"
DJANGOPLICITY_MEDIA_URL = "/static/app/djangoplicity/"
DJANGOPLICITY_MEDIA_ROOT = "%s/static" % DJANGOPLICITY_ROOT

MIDENTIFY_PATH = '/usr/bin/midentify'


##########
# CACHE  #
##########
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': SHORT_NAME,
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 86400
    }
}
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = SHORT_NAME
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# keyedcached settings:
CACHE_TIMEOUT = CACHE_MIDDLEWARE_SECONDS if CACHES['default']['BACKEND'] != 'django.core.cache.backends.dummy.DummyCache' else 0  # prevents stupid error from keyecache
KEY_PREFIX = SHORT_NAME

USE_ETAGS = True

#############
# TEMPLATES #
#############
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PRJBASE + '/templates',
            DJANGOPLICITY_ROOT + '/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'djangoplicity.utils.context_processors.project_environment',
                'djangoplicity.utils.context_processors.google_analytics_id',
                'djangoplicity.utils.context_processors.djangoplicity_environment',
                'djangoplicity.archives.context_processors.internal_request',
                # 'satchmo_store.shop.context_processors.settings',
            ],
        },
    },
]

ROOT_URLCONF = 'spacetelescope.urls'

###############################
# MIDDLEWARE AND APPLICATIONS #
###############################
MIDDLEWARE = [
    # Compresses content for browsers that understand gzip compression (all modern browsers).
    'django.middleware.gzip.GZipMiddleware',  # Response

    # Handles conditional GET operations. If the response has a ETag or Last-Modified header,
    # and the request has If-None-Match or If-Modified-Since, the response is replaced by an
    # HttpNotModified.
    'django.middleware.http.ConditionalGetMiddleware',

    # The CsrfMiddleware class provides easy-to-use protection against Cross Site Request Forgeries.
    'django.middleware.csrf.CsrfViewMiddleware',

    # Enables session support
    'django.contrib.sessions.middleware.SessionMiddleware',  # Request/Response (db)

    # Adds the user attribute, representing the currently-logged-in user, to every incoming
    # HttpRequest object.
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Request
]

if DEBUG_TOOLBAR:
    # Add debug toolbar to request
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

if DEBUG:
    # Add debug toolbar to request
    MIDDLEWARE += [
        'djangoplicity.utils.middleware.ProfileMiddleware',
    ]


MIDDLEWARE += [
    # enables Messaging middleware
    'django.contrib.messages.middleware.MessageMiddleware',
]

if USE_I18N:
    MIDDLEWARE += [
        # Sets local for request based on URL prefix.
        'djangoplicity.translation.middleware.LocaleMiddleware',  # Request/Response
    ]

MIDDLEWARE += [
    # - Forbids access to user agents in the DISALLOWED_USER_AGENTS setting
    # - Performs URL rewriting based on the APPEND_SLASH and PREPEND_WWW settings.
    # - Handles ETags based on the USE_ETAGS setting.
    'django.middleware.common.CommonMiddleware',  # Request/Response

    # Sets a boolean session variable INTERNAL_REQUEST if request.META['REMOTE_ADDR'] is in INTERNAL_IPS
    'djangoplicity.archives.middleware.InternalRequestMiddleware',  # Request

    # Module for URL redirection.
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',  # Response

    # Module for URL redirection based on regular expressions
    'djangoplicity.utils.middleware.RegexRedirectMiddleware',  # Response

    # 'djangoplicity.archives.contrib.satchmo.middleware.SatchmoSSLRedirectOverride',
]

DJANGO_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.postgres',
    # 'satchmo_store.shop',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    #'django.contrib.comments',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
]

DJANGOPLICITY_APPS = [
    'djangoplicity',
    'djangoplicity.menus',
    'djangoplicity.reports',
    #'djangoplicity.massmailer',
    #'djangoplicity.news',
    'djangoplicity.pages',
    'djangoplicity.media',
    #'djangoplicity.contrib.redirects',
    'djangoplicity.archives',
    # 'djangoplicity.archives.contrib.satchmo',
    # 'djangoplicity.archives.contrib.satchmo.freeorder',
    'djangoplicity.archives.contrib.security',
    'djangoplicity.announcements',
    'djangoplicity.science',
    'djangoplicity.releases',
    'djangoplicity.products2',
    'djangoplicity.metadata',
    'djangoplicity.cache',
    'djangoplicity.adminhistory',
    'djangoplicity.utils',
    'djangoplicity.celery',
    #'djangoplicity.events',
    'djangoplicity.mailinglists',
    'djangoplicity.newsletters',
    'djangoplicity.iframe',
    'djangoplicity.contacts',
    'djangoplicity.customsearch',
    'djangoplicity.admincomments',
    'djangoplicity.simplearchives',
    #'djangoplicity.eventcalendar',
    'djangoplicity.actions',
    'djangoplicity.cutter',
    #'djangoplicity.mailer',
    #'djangoplicity.scrum',
    #'djangoplicity.kiosk.engine',
    #'djangoplicity.kiosk.slides',
]

THIRD_PARTY_APPS = [
    'mptt',
    # 'django_extensions',
    'django_mailman',
    # 'registration',
    'sorl.thumbnail',
    # 'keyedcache',
    ### Satchmo
    # 'livesettings',
    # 'satchmo_utils',
    # 'satchmo_store.contact',
    # 'product',
    # 'product.modules.configurable',
    # 'shipping',
    # 'payment',
    # 'djangoplicity.concardis',
    # 'l10n',
    # 'tax',
    # 'tax.modules.no',
    # 'app_plugins',
    # 'shipping.modules.tieredweight',
    # 'captcha',
    'gunicorn',
    'django_ace',
    'rest_framework',
    'pipeline',
    'tinymce',
    # CONTACTS
    'crispy_forms',
]

SPACETELESCOPE_APPS = [
    'spacetelescope',
    'spacetelescope.frontpage',
]

INSTALLED_APPS = DJANGO_APPS + DJANGOPLICITY_APPS + SPACETELESCOPE_APPS + THIRD_PARTY_APPS

if USE_I18N:
    INSTALLED_APPS += [
        'djangoplicity.translation',
        'rosetta',
    ]


if DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

############
# SESSIONS #
############
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 86400
SESSION_COOKIE_DOMAIN = None


################
# FILE UPLOADS #
################
FILE_UPLOAD_TEMP_DIR = TMP_DIR
FILE_UPLOAD_PERMISSIONS = 0o666

# EMAIL CONFIG
SERVER_EMAIL = 'nobody@esahubble.org'
DEFAULT_FROM_EMAIL = 'nobody@esahubble.org'
DEFAULT_MAIL_USER = [HUBBLE_DEFAULT_EMAIL]
DEFAULT_MAIL_TAGGING = ['zidmani@gmail.com']
EMAIL_SUBJECT_PREFIX = '[SPACETELESCOPE-LOCAL]'

##################
# AUTHENTICATION #
##################

AUTHENTICATION_BACKENDS = (
    # 'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
#AUTH_PROFILE_MODULE = ''
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

#############
# LDAP AUTH #
#############
'''
Disabled when migrated to esahubble.org
import ldap
from django_auth_ldap.config import LDAPSearch, ActiveDirectoryGroupType

AUTH_LDAP_SERVER_URI = ""

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_REFERRALS: 0,
    ldap.OPT_PROTOCOL_VERSION: 3,
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER
}

AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch( "DC=ads,DC=eso,DC=org",
    ldap.SCOPE_SUBTREE, "(&(objectCategory=user)(objectClass=person)(sAMAccountName=%(user)s)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))" )

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "dc=ads,dc=eso,dc=org",
    ldap.SCOPE_SUBTREE, "(objectClass=group)"
)

# Defaults:
# - ePOD staff will get active/staff account - but no permissions.
# - All ESO staff will get an inactive account on login - this account has to manually be activated.
AUTH_LDAP_ALWAYS_UPDATE_USER = False  # Prevent user from being updated every time a user logs in.

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "CN=SA-PAD-EPR,OU=Garching,OU=Shared Acess Groups,OU=Groups,DC=ads,DC=eso,DC=org",
    "is_staff": "CN=SA-PAD-EPR,OU=Garching,OU=Shared Acess Groups,OU=Groups,DC=ads,DC=eso,DC=org",
}

############
# AUTH_TKT #
############
AUTH_TKT_UNAUTH_URL = '/access_denied/'
AUTH_TKT_COOKIE_NAME = 'auth_tkt'
AUTH_TKT_HTACCESS = '.esoacc'
# AUTH_TKT_REDIRECT_FIELD_NAME = 'next'
# AUTH_TKT_IGNOREIP = 'off'
# AUTH_TKT_TIMEOUT_URL = ''
# AUTH_TKT_FILEPERMS =
'''

#########
# PAGES #
#########
PAGE_TEMPLATE_CHOICES = (
    ('pages/page_onecolumn.html', 'Default one column layout'),
    ('pages/page_twocolumn.html', 'Default two column layout'),
    ('pages/page_search.html', 'Google custom search layout')
)

#############
# PAGIANTOR #
#############
DEFAULT_PAGINATE_BY = 10
PAGINATOR_ADJ = 5
BREADCRUMB_SEPARATOR = '&raquo;'

#################
# DJANGO ASSETS #
#################
ASSETS_DEBUG = DEBUG
ASSETS_UPDATER = "timestamp"

###########
# ARCHIVE #
###########

# For static media protection to be enabled, and archive must be present here
# For file import to work, the archive must be present here.
ARCHIVES = (
    ('djangoplicity.media.models.Image', 'djangoplicity.media.options.ImageOptions'),
    ('djangoplicity.media.models.Video', 'djangoplicity.media.options.VideoOptions'),
    ('djangoplicity.media.models.VideoSubtitle', 'djangoplicity.media.options.VideoSubtitleOptions'),
    ('djangoplicity.media.models.ImageComparison', 'djangoplicity.media.options.ImageComparisonOptions'),
    ('djangoplicity.releases.models.Release', 'djangoplicity.releases.options.ReleaseOptions'),
    #('djangoplicity.announcements.models.Announcement','djangoplicity.announcements.options.AnnouncementOptions'),
    ('djangoplicity.products2.models.Model3d', 'djangoplicity.products2.options.Model3dOptions'),
    ('djangoplicity.products2.models.Calendar', 'djangoplicity.products2.options.CalendarOptions'),
    ('djangoplicity.products2.models.Application', 'djangoplicity.products2.options.ApplicationOptions'),
    ('djangoplicity.products2.models.Brochure', 'djangoplicity.products2.options.BrochureOptions'),
    ('djangoplicity.products2.models.Logo', 'djangoplicity.products2.options.LogoOptions'),
    ('djangoplicity.products2.models.Exhibition', 'djangoplicity.products2.options.ExhibitionOptions'),
    ('djangoplicity.products2.models.FITSImage', 'djangoplicity.products2.options.FITSImageOptions'),
    ('djangoplicity.products2.models.Sticker', 'djangoplicity.products2.options.StickerOptions'),
    ('djangoplicity.products2.models.PostCard', 'djangoplicity.products2.options.PostCardOptions'),
    ('djangoplicity.products2.models.PressKit', 'djangoplicity.products2.options.PressKitOptions'),
    ('djangoplicity.products2.models.PrintedPoster', 'djangoplicity.products2.options.PrintedPosterOptions'),
    ('djangoplicity.products2.models.ConferencePoster', 'djangoplicity.products2.options.ConferencePosterOptions'),
    ('djangoplicity.products2.models.Merchandise', 'djangoplicity.products2.options.MerchandiseOptions'),
    ('djangoplicity.products2.models.Media', 'djangoplicity.products2.options.MediaOptions'),
    ('djangoplicity.products2.models.Presentation', 'djangoplicity.products2.options.PresentationOptions'),
    ('djangoplicity.products2.models.OnlineArt', 'djangoplicity.products2.options.OnlineArtOptions'),
    ('djangoplicity.products2.models.OnlineArtAuthor', 'djangoplicity.products2.options.OnlineArtAuthorOptions'),
    ('djangoplicity.products2.models.ConferenceItem', 'djangoplicity.products2.options.ConferenceItemOptions'),
    ('djangoplicity.products2.models.VideoConferenceBackground', 'djangoplicity.products2.options.VideoConferenceBackgroundOptions'),
    ('djangoplicity.newsletters.models.Newsletter', 'djangoplicity.newsletters.options.NewsletterOptions'),
)

ARCHIVE_EMBARGO_LOGIN = ('hst', 'shtenvix')
ARCHIVE_EMAIL_SENDER = "ESA/Hubble Information Centre <info@esahubble.org>"

ARCHIVE_URL_QUERY_PREFIX = 'archive'
ARCHIVE_URL_DETAIL_PREFIX = ''
ARCHIVE_URL_FEED_PREFIX = 'feed'
ARCHIVE_URL_SEARCH_PREFIX = 'search'
ARCHIVE_PAGINATOR_PREFIX = 'page'
ARCHIVE_ROOT = 'archives/'

ENABLE_ADVANCED_SEARCH = True
ADV_SEARCH_START_YEAR = 1998

ARCHIVE_AUTO_RESOURCE_DELETION = False
RELEASE_ARCHIVE_ROOT = 'archives/releases/'
IMAGES_ARCHIVE_ROOT = 'archives/images/'
IMAGECOMPARISON_ARCHIVE_ROOT = 'archives/imagecomparisons/'
VIDEOS_ARCHIVE_ROOT = 'archives/videos/'
ANNOUNCEMENTS_ARCHIVE_ROOT = 'archives/announcements/'
NEWSLETTERS_ARCHIVE_ROOT = 'archives/newsletters/'
SCIENCEANNOUNCEMENTS_ARCHIVE_ROOT = 'archives/science/'

SHOP_NEWSLETTER_FROM = 'ESO & ESA/Hubble'

VIDEOS_FEATURED_SUBJECT = 'hubblecast'

VIDEOS_SUBTITLES_FORMATS = ('hd_and_apple', 'medium_podcast')
# List of extra formats which should be removed when importing new videos.
VIDEOS_FORMATS_REMOVE = [
    #'hd_broadcast_720p25',
]

RELEASE_LINK_PREFIX = "heic"

DEFAULT_CREATOR = u"ESA/Hubble"
DEFAULT_CREATOR_URL = "https://esahubble.org"
DEFAULT_CONTACT_ADDRESS = u"ESA Office, Space Telescope Science Institute, 3700 San Martin Dr"
DEFAULT_CONTACT_CITY = u"Baltimore"
DEFAULT_CONTACT_STATE_PROVINCE = "MD"
DEFAULT_CONTACT_POSTAL_CODE = u"21218"
DEFAULT_CONTACT_COUNTRY = u"United States"
DEFAULT_RIGHTS = "Creative Commons Attribution 4.0 International License"
DEFAULT_PUBLISHER = u"ESA/Hubble"
DEFAULT_PUBLISHER_ID = u"esahubble"

DEFAULT_CREDIT = u"NASA &amp; ESA"

MP4BOX_PATH = '/usr/bin/MP4Box'
MP4FRAGMENT_PATH = '/opt/bin/mp4fragment'

ARCHIVE_WORKFLOWS = {
    'media.video.rename': ('spacetelescope.workflows.media', 'video_rename'),
}

VIDEO_RENAME_NOTIFY = [HUBBLE_DEFAULT_EMAIL, 'hubbleesa@gmail.com']

ARCHIVE_CROSSLINKS = djangoplicity.crosslinks.crosslinks_for_domain('spacetelescope.org')


# CONTACTS APP
# Hashids salt, used to encrype/decrypt Contacts' UIDs
# TODO: Use secret if required
HASHIDS_SALT = 'UbKopIrheasdGiwrked'
HASHIDS_ALPHABET = 'abcdefghijkmnopqrstuvwxyz123456789'
HASHIDS_ALPHABET_UPPER = 'ABCDEFGHJKMNPQRSTUVWXYZ123456789'


##########
# SOCIAL #
##########
SOCIAL_FACEBOOK_TOKEN = ""
SOCIAL_TWITTER_TUPLE = (
    "",
    "",
    "",
    "",
)


SOCIAL_FACEBOOK_WALL = 'http://www.facebook.com/hubbleESA?sk=wall'

#########
# FEEDS #
#########
FEED_SETTINGS_MODULE = 'spacetelescope.feed_settings'

############
# REPORTS  #
############
REPORTS_DEFAULT_FORMATTER = 'html'
REPORT_REGISTER_FORMATTERS = True

##########
# CELERY #
##########

CELERY_IMPORTS = [
    "djangoplicity.archives.contrib.security.tasks",
    "djangoplicity.celery.tasks",
]

# Message routing
CELERY_TASK_DEFAULT_QUEUE = "celery"
CELERY_TASK_DEFAULT_EXCHANGE = "celery"
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_TASK_DEFAULT_ROUTING_KEY = "celery"
CELERY_TASK_QUEUES = {
    "celery": {
        "exchange": "celery",
        "exchange_type": "direct",
        "binding_key": "celery",
    },
}

CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False

# Broker settings.
CELERY_BROKER_USE_SSL = False
CELERY_BROKER_URL = ''

# Task result backend
CELERY_RESULT_BACKEND = "amqp"

# AMQP backend settings
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_EXPIRES = 3600

# Task execution
CELERY_TASK_IGNORE_RESULT = True
CELERY_WORKER_DISABLE_RATE_LIMITS = True

# Events
CELERY_WORKER_SEND_TASK_EVENTS = True

# Logging
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

CELERY_TASK_ALWAYS_EAGER = False

# File to save revoked tasks across workers restart
CELERY_WORKER_STATE_DB = os.path.join(TMP_DIR, 'celery_states')
CELERY_BEAT_SCHEDULE_FILENAME = os.path.join(TMP_DIR, 'celerybeat_schedule')

# Define Celery periodic tasks
CELERY_BEAT_SCHEDULE = {
    'update_static_files_protection_cache': {
        'task': 'djangoplicity.archives.contrib.security.tasks.update_static_files_protection_cache',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'mailchimp-abuse-report': {
        'task': 'newsletters.abuse_reports',
        'schedule': crontab(minute=0, hour=8, day_of_week='fri'),
    },
    'mailchimp-fetch-info': {
        'task': 'mailinglists.mailchimplist_fetch_info',
        'schedule': crontab(minute=0, hour=8),
    },
    'mailchimp-install-hooks': {
        'task': 'mailinglists.webhooks',
        'schedule': crontab(minute=50, hour=4),
    },
    'mailchimp-clean-tokens': {
        'task': 'mailinglists.clean_tokens',
        'schedule': crontab(minute=5, hour=5),
    },
    'check-content-server-resources': {
        'task': 'djangoplicity.contentserver.tasks.check_content_server_resources',
        'schedule': crontab(minute=0, hour=4),
    },
    # Mon 29 Apr 10:53:57 CEST 2019 - Mathias
    # Disabled as CDN77 complained it created too many hits (and forced
    # pre-fetch of the full archive)
    #  'check-content-server-resources-all': {
    #      'task': 'djangoplicity.contentserver.tasks.check_content_server_resources',
    #      'schedule': crontab(minute=0, hour=10, day_of_week='sun'),
    #      'kwargs': {'last': 15000},  # Large enough to check all resources
    #  },
    'cdn77-purge-prefetch': {
        'task': 'djangoplicity.contentserver.cdn77_tasks.purge_prefetch',
        'schedule': crontab(minute='*/10'),  # Every 10 minutes
    },
    'shop-subscribers': {
        'task': 'djangoplicity.archives.contrib.satchmo.tasks.shop_subscribers',
        'schedule': crontab(minute=0, hour=9, day_of_week='sun'),
    },
    'clearsessions': {
        'task': 'djangoplicity.celery.tasks.clearsessions',
        'schedule': crontab(minute=0, hour=3),
    },
}

##############
# JavaScript #
##############
JQUERY_JS = "jquery/jquery-1.11.1.min.js"
JQUERY_UI_JS = "jquery-ui-1.12.1/jquery-ui.min.js"
JQUERY_UI_CSS = "jquery-ui-1.12.1/jquery-ui.min.css"
DJANGOPLICITY_ADMIN_CSS = "djangoplicity/css/admin.css"
DJANGOPLICITY_ADMIN_JS = "djangoplicity/js/admin.js"
SUBJECT_CATEGORY_CSS = "djangoplicity/css/widgets.css"

REGEX_REDIRECTS = (
#   ( re.compile( '/hubbleshop/webshop/webshop\.php\?show=sales&section=(books|cdroms)' ), '/shop/category/\g<1>/' ),
    ( re.compile( r'/about/history/sm4blog/(.+)' ), r'/static/sm4blog/\g<1>' ),
    ( re.compile( r'/news/(doc|pdf|text)/(.+)' ), r'/static/archives/releases/\g<1>/\g<2>' ),
    ( re.compile( r'/news/(science_paper)/(.+)' ), r'/static/archives/releases/science_papers/\g<1>' ),
    ( re.compile( r'/images/html/([a-z0-9-_]+)\.html' ), r'/images/\g<1>/' ),
    ( re.compile( r'/videos/(vodcast|hd1080p_screen|hd1080p_broadcast|hd720p_screen|hd720p_broadcast|h264|broadcast)/(.+)' ), r'/static/archives/videos/\g<1>/\g<2>' ),
    ( re.compile( r'/images/html/zoomable/([a-z0-9-_]+).html' ), r'/images/\g<1>/zoomable/' ),
    ( re.compile( r'/videos/html/mov/(320px|180px)/([a-z0-9-_]+).html' ), r'/videos/\g<2>/' ),
    ( re.compile( r'/bin/videos.pl\?(searchtype=news&)?string=([a-z0-9-_]+)' ), r'/videos/?search=\g<2>' ),
    ( re.compile( r'/bin/images.pl\?(searchtype=news&)?string=([a-z0-9-_]+)' ), r'/images/?search=\g<2>' ),
    ( re.compile( r'/about/further_information/(brochures|books|newsletters)/(pdf|pdfsm)/(.+)' ), r'/static/archives/\g<1>/\g<2>/\g<3>' ),
    ( re.compile( r'/bin/calendar.pl' ), r'/extras/calendars/' ),
    ( re.compile( r'/bin/calendar.pl\?string=(\d+)' ), r'/extras/calendars/archive/year/\g<1>/' ),
    ( re.compile( r'/bin/images.pl\?embargo=0&viewtype=standard&searchtype=freesearch&lang=en&string=(.+)' ), r'/images/?search=\g<1>' ),
    ( re.compile( r'/bin/images.pl\?searchtype=freesearch&string=(.+)' ), r'/images/?search=\g<1>' ),
    ( re.compile( r'/bin/images.pl\?searchtype=top100' ), r'/images/archive/top100/' ),
    ( re.compile( r'/bin/images.pl\?searchtype=wallpaper' ), r'/images/archive/wallpapers/' ),
    ( re.compile( r'/bin/news.pl\?string=([a-z0-9-_]+)' ), r'/news/\g<1>/' ),
    ( re.compile( r'/goodies/printlayouts/html/([a-z0-9-_]+).html' ), r'/news/\g<1>/' ),
    ( re.compile( r'/images/archive/freesearch/([^/]+)/viewall/\d+' ), r'/images/?search=\g<1>' ),
    ( re.compile( r'/images/archive/topic/([^/]+)/(|standard)/(\d+)?' ), r'/images/archive/category/\g<1>/' ),
    ( re.compile( r'/images/archive/wallpaper/(.+)' ), r'/images/archive/wallpapers/' ),
    ( re.compile( r'/kidsandteachers/education/lowres_pdf/([a-z0-9-_]+)\.pdf' ), r'/static/archives/education/pdfsm/\g<1>.pdf' ),
    ( re.compile( r'/projects/python-xmp-toolkit/(.*)' ), r'/static/projects/python-xmp-toolkit/\g<1>' ),
    ( re.compile( r'/videos/archive/topic/([^/]+)/(|standard|viewall)/(\d+)?' ), r'/videos/archive/category/\g<1>/' ),
    ( re.compile( r'/videos/html/mpeg/320px/([a-z0-9-_]+).html' ), r'/videos/\g<1>/' ),
    ( re.compile( r'/videos/scripts/(.+)' ), r'/static/archives/videos/script/\g<1>' ),
)

SITE_DOMAIN = "www.spacetelescope.org"

# ======================================================================
# SITE SPECIFIC SECTIONS
# ======================================================================

###########
# SATCHMO #
###########
SHOP_CONF = {
    'DEFAULT_NAVISION_JOB': '050',
    'DEFAULT_NAVISION_JSP': 8900,
    'DEFAULT_NAVISION_ACCOUNT': '50.030',
    'ORDER_FILE_PREFX': "hb",
    'ARCHIVE_DEFAULTS': {
        'djangoplicity.products.models.PostCard': { 'ACCOUNT': '50.050', },
        'djangoplicity.products.models.Merchandise': { 'ACCOUNT': '50.050', },
        'djangoplicity.products.models.Media': { 'ACCOUNT': '50.050', },
        'djangoplicity.products.models.Calendar': { 'ACCOUNT': '50.050', },
        'djangoplicity.products.models.ConferenceItem': { 'ACCOUNT': '50.230', },
        'djangoplicity.products.models.Sticker': { 'ACCOUNT': '50.050', },
    }
}


DIRNAME = os.path.abspath( os.path.dirname( __file__ ) )
LOCAL_DEV = True

# MIDDLEWARE += [
#     "threaded_multihost.middleware.ThreadLocalMiddleware",
# ]

# AUTHENTICATION_BACKENDS += ( 'satchmo_store.accounts.email-auth.EmailBackend', )

SATCHMO_SETTINGS = {
    'SHOP_BASE': '/shop',
    'MULTISHOP': False,
    'SSL': True,
#   'SHOP_URLS': patterns('',
#       ( r'^checkout/', 'spacetelescope.views.shop_closed' ),
#   )
}

SITE_NAME = "Hubbleshop"
SITE_DOMAIN = "www.spacetelescope.org"
LOGDIR = LOG_DIR
LOGFILE = 'satchmo.log'
CHECKOUT_SSL = True

L10N_SETTINGS = {
    'currency_formats': {
        'EURO': {'symbol': u'€', 'positive': u"€ %(val)0.2f", 'negative': u"€ (%(val)0.2f)", 'decimal': ','},
    },
    'default_currency': 'EURO',
    'show_admin_translations': False,
    'allow_translation_choice': False,
}

LIVESETTINGS_OPTIONS = {
    1: {
        'DB': False,
        'SETTINGS': {
            u'LANGUAGE': {
                u'CURRENCY': u'\u20ac',
                u'SHOW_TRANSLATIONS': u'False'
            },
            u'PAYMENT': {
                u'COUNTRY_MATCH': u'False',
                u'MINIMUM_ORDER': u'2.99',
                #u'ORDER_EMAIL_EXTRA': u'distribution@spacetelescope.org',
                u'ORDER_EMAIL_OWNER': u'True',
                u'MODULES': u'["PAYMENT_CONCARDIS"]'
            },
            u'PAYMENT_DUMMY': {
                u'CREDITCHOICES': u'["Visa", "Mastercard", "Discover", "American Express"]'
            },
            u'PRODUCT': {
                u'IMAGE_DIR': u'satchmoimages',
                u'MEASUREMENT_SYSTEM': u'["metric"]',
                # Note the string below is too long to store in the database since PRODUCT_TYPES is not a LongSetting
                # Therefore it must be configured here!
                u'TRACK_INVENTORY': u'False',
                u'NUM_PAGINATED': u'10',
                u'NUM_DISPLAY': u'20',
            },
            u'SHIPPING': {
                #u'PER_DAYS': u'1 - 3 business days',
                #u'PER_SERVICE': u'Deutsche Post/DHL',
                u'SELECT_CHEAPEST': u'False',
                u'HIDING': u'NO',
                u'MODULES': u'["shipping.modules.tieredweight","djangoplicity.archives.contrib.satchmo.esoshipping.officedelivery","djangoplicity.archives.contrib.satchmo.esoshipping.pickup"]',
            },
            u'TAX': {
                u'PRODUCTS_TAXABLE_BY_DEFAULT': u'False',
                u'TAX_SHIPPING': u'False',
            },
            u'SHOP': {
                u'REQUIRED_BILLING_DATA': u'["email", "first_name", "last_name", "phone", "street1", "city", "postal_code", "country"]',
                u'ENFORCE_STATE': u'False',
                u'SHOW_SITE': u'False',
                u'LOGO_URI': u'https://www.spacetelescope.org/static/archives/logos/screen/eso_colour.jpg',
            },
            u'PAYMENT_CONCARDIS': {
                u'PSPID': u'',
                u'SHA_IN_PASSPHRASE': u'',
                u'SHA_OUT_PASSPHRASE': u'',
                u'LIVE': u'False',
                u'EXTRA_LOGGING': u'True',
            },
        }
    }
}

ORDER_PREFIX = 'hbl'
LIVE = False
SHOP_PICKUP_LOCATIONS = ({
    'id': 'PUP1',
    'name': 'ESO HQ',
    'desc': ugettext( "Self-pickup/ESO HQ in Munich, Germany" ),
    'method': ugettext("Pickup (9-17 CET/CEST) at ESO HQ Reception,"),
    'delivery': ugettext("Karl-Schwarzschild-Str. 2, 85748 Garching, GERMANY"),
},)

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

#
# Pipeline configuration (CSS/JS packing)
#
# Only config this for the docker web service, not flower, celery, etc, to avoid:
# ValueError: Missing staticfiles manifest entry for
# And because the web service is the only that collect statics before
if os.environ.get('SERVICE_TYPE') == 'web':
    STATICFILES_STORAGE = 'djangoplicity.utils.storage.PipelineManifestStorage'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'pipeline.finders.PipelineFinder',
    )

# We split the CSS into main and extras to load the more important first
# and the rest in the end. This also solves a problem with IE9 which stops
# loading CSS rules if there are "too many"
PIPELINE = {
    'STYLESHEETS': {
        'main': {
            'source_filenames': (
                'font-awesome/css/font-awesome.min.css',
                'sprites/sprites.css',
                'css/hubble.css',
            ),
            'output_filename': 'css/main.css',
        },
        'extras': {
            'source_filenames': (
                'jquery-ui-1.12.1/jquery-ui.min.css',
                'slick-1.5.0/slick/slick.css',
                'justified/css/jquery.justified.css',
                'magnific-popup/magnific-popup.css',
            ),
            'output_filename': 'css/extras.css',
        },
    },
    'JAVASCRIPT': {
        'main': {
            'source_filenames': (
                'jquery/jquery-1.11.1.min.js',
                'jquery-ui-1.12.1/jquery-ui.min.js',
                'bootstrap/bootstrap-3.1.1-dist/js/bootstrap.min.js',
                'js/jquery.menu-aim.js',
                'slick-1.5.0/slick/slick.min.js',
                'djangoplicity/jwplayer/jwplayer.js',
                'djangoplicity/js/jquery.beforeafter-1.4.js',
                'js/masonry.pkgd.min.js',
                'justified/js/jquery.justified.min.js',
                'magnific-popup/jquery.magnific-popup.min.js',
                'djangoplicity/js/widgets.js',
                'djangoplicity/js/pages.js',
                'djangoplicity/js/djp-jwplayer.js',
                'js/picturefill.min.js',
                'js/enquire/enquire.min.js',
                'js/sorttable.js',
                'js/hubble.js',
            ),
            'output_filename': 'js/main.js',
        },
        'ie8compat': {
            'source_filenames': (
                'js/ie8compat/matchMedia/matchMedia.js',
                'js/ie8compat/matchMedia/matchMedia.addListener.js',
            ),
            'output_filename': 'js/ie8compat.js',
        },
        'openseadragon': {
            'source_filenames': (
                'djangoplicity/openseadragon/openseadragon.min.js',
            ),
            'output_filename': 'js/openseadragon.js',
        },
    },
    'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    'DISABLE_WRAPPER': True,
}

# Required since Django 1.6:
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
        textcolor save link image media preview codesample table
        code lists fullscreen  insertdatetime  nonbreaking contextmenu
        directionality searchreplace wordcount visualblocks visualchars
        code fullscreen autolink lists  charmap print  hr anchor pagebreak
    ''',
    'toolbar1': '''
        fullscreen code | cut copy | searchreplace | alignleft aligncenter alignright alignjustify | formatselect forecolor backcolor | superscript subscript |
     ''',
    'toolbar2': '''
        bold italic underline strikethrough | bullist numlist table hr | indent outdent | undo redo | link unlink anchor image media charmap | nonbreaking |
    ''',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'statusbar': True,
    'entity_encoding': 'raw',
    'convert_urls': False,
}

NEWSLETTER_SUBSCRIBERS_URL = 'https://us2.admin.mailchimp.com/lists/members/import/setup?id=518393&type=CutPaste'
