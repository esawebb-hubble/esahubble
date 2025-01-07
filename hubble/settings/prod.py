from .common import *
from .partials.util import get_secret
import copy
import dj_database_url
from djangoplicity.contentserver import CDN77ContentServer

DEBUG = False
SECRET_KEY = get_secret('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    '.esahubble.org',
    '.spacetelescope.org'
]

# Required to import a big number of images using the admin import form
DATA_UPLOAD_MAX_NUMBER_FIELDS = 200000

# CACHE
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': SHORT_NAME,
        'LOCATION': [
            'cache:11211',
        ],
        'TIMEOUT': 86400
    }
}

# DATABASE
if get_secret('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config()
    }

# EMAIL: SMTP CONFIG
EMAIL_SUBJECT_PREFIX = '[ESA/HUBBLE]'
EMAIL_HOST = 'smtp.eu.mailgun.org'
EMAIL_HOST_USER = get_secret('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_PASSWORD')
EMAIL_PORT = '587'
EMAIL_USE_TLS = True

ARCHIVE_AUTO_RESOURCE_DELETION = True

# Shop:
LIVESETTINGS_OPTIONS = copy.deepcopy(LIVESETTINGS_OPTIONS)
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['PSPID'] = u''
LIVESETTINGS_OPTIONS[1]['SETTINGS']['PAYMENT_CONCARDIS']['LIVE'] = u'True'
LIVE = 'True'
ORDER_PREFIX = "hb"

# CELERY
CELERY_BROKER_URL = 'amqp://{}:{}@broker:5672/'.format(get_secret('RABBITMQ_USER'), get_secret('RABBITMQ_PASS'))

SOCIAL_FACEBOOK_TOKEN = ""
SOCIAL_TWITTER_TUPLE = (
    "",
    "",
    "",
    "",
)

MEDIA_CONTENT_SERVERS = {
    'CDN77': CDN77ContentServer(
        name='CDN77',
        formats={
            'djangoplicity.media.models.images.Image': (
                'large',
                'publicationjpg',
                'screen',
                'wallpaper1',
                'wallpaper2',
                'wallpaper3',
                'wallpaper4',
                'wallpaper5',
                'thumb150y',
                'thumb300y',
                'thumb350x',
                'thumb700x',
                'newsfeature',
                'news',
                'banner1920',
                'screen640',
                'zoomable',
            ),
            'djangoplicity.media.models.videos.Video': (
                'videoframe',
                'small_flash',
                'medium_podcast',
                'medium_mpeg1',
                'medium_flash',
                'large_qt',
                'broadcast_sd',
                'hd_and_apple',
                'hd_broadcast_720p50',
                'hd_1080p25_screen',
                'hd_1080p25_broadcast',
                'ultra_hd',
                'ultra_hd_h265',
                'ultra_hd_broadcast',
                'dome_8kmaster',
                'dome_4kmaster',
                'dome_2kmaster',
                'dome_mov',
                'dome_preview',
                'cylindrical_4kmaster',
                'cylindrical_8kmaster',
                'cylindrical_16kmaster',
                'news',
            ),
        },
        url='https://cdn.esahubble.org/',
        url_bigfiles='https://cdn2.esahubble.org/',
        remote_dir='',
        host='push-19.cdn77.com',
        username=get_secret('CDN_STORAGE_USERNAME'),
        password=get_secret('CDN_STORAGE_PASSWORD'),
        api_login=get_secret('CDN_API_LOGIN'),
        api_password=get_secret('CDN_API_PASSWORD'),
        cdn_id='1663784698',
        cdn_id_bigfiles='1072368761',
        aws_access_key_id=get_secret('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=get_secret('AWS_SECRET_ACCESS_KEY'),
        aws_storage_bucket_name=get_secret('AWS_STORAGE_BUCKET_NAME'),
        aws_s3_region_name=get_secret('AWS_S3_REGION_NAME'),
        aws_s3_endpoint_url=get_secret('AWS_S3_ENDPOINT_URL'),
        aws_s3_custom_domain=get_secret('AWS_S3_CUSTOM_DOMAIN')
    ),
}

MEDIA_CONTENT_SERVERS_CHOICES = (
    ('', 'Default'),
    ('CDN77', 'CDN77'),
)

DEFAULT_MEDIA_CONTENT_SERVER = 'CDN77'

# YOUTUBE
YOUTUBE_CLIENT_SECRET = os.path.join(ROOT, 'config', 'youtube', 'client-secret.json')
YOUTUBE_TOKEN = os.path.join(ROOT, 'config', 'youtube', 'youtube-oauth2-token.json')
YOUTUBE_DEFAULT_TAGS = ['Hubble', 'Hubble Space Telescope', 'Telescope', 'Space', 'Observatory', 'ESA']
