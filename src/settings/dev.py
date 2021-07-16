import logging

import dotenv

from .base import *
from .logs import LOGGING

dotenv.read_dotenv(override=True)

DEBUG = IS_TEST_PS = True

DATABASES['default'] = env.db('DATABASE_URL', default='pgsql://postgres:@localhost:5432/ps')

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False

CELERY_TASK_ALWAYS_EAGER = env.bool('CELERY_TASK_ALWAYS_EAGER', default=False)

if env.bool('SHOW_QUERYCOUNT', False):
    MIDDLEWARE.append('querycount.middleware.QueryCountMiddleware')
    QUERYCOUNT = {
        'THRESHOLDS': {
            'MEDIUM': 20,
            'HIGH': 30,
            'MIN_TIME_TO_LOG': 0,
            'MIN_QUERY_COUNT_TO_LOG': 0
        },
        'IGNORE_REQUEST_PATTERNS': [r'^/adm-panel/'],
        'IGNORE_SQL_PATTERNS': [],
        'DISPLAY_DUPLICATES': True,
        'RESPONSE_HEADER': None
    }

CHAT_ALARM_BILLING = 'https://rocketchat.b2bpolis.ru/hooks/MHc6t9XWr38kA2cJK/K7gPBqQbCT3RKnP4yhyor3Sk2vTpbafKYsH3559XzTrmAXud'
CHAT_ALARM_PROLONGATION = 'https://rocketchat.b2bpolis.ru/hooks/MHc6t9XWr38kA2cJK/K7gPBqQbCT3RKnP4yhyor3Sk2vTpbafKYsH3559XzTrmAXud'
CHAT_ALARM_COMMON = 'https://rocketchat.b2bpolis.ru/hooks/MHc6t9XWr38kA2cJK/K7gPBqQbCT3RKnP4yhyor3Sk2vTpbafKYsH3559XzTrmAXud'
CHAT_INFO_SCRIPTS = 'https://rocketchat.b2bpolis.ru/hooks/MHc6t9XWr38kA2cJK/K7gPBqQbCT3RKnP4yhyor3Sk2vTpbafKYsH3559XzTrmAXud'

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'redis_lock.django_cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

if env.bool('SHOW_NPLUSONE', False):
    INSTALLED_APPS += ('nplusone.ext.django',)
    MIDDLEWARE.insert(0, 'nplusone.ext.django.NPlusOneMiddleware')

    NPLUSONE_LOGGER = logging.getLogger('nplusone')
    NPLUSONE_LOG_LEVEL = logging.DEBUG

    LOGGING['loggers']['nplusone'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    }


if env.bool('ENABLE_SILK', False):
    INSTALLED_APPS += ('silk',)
    MIDDLEWARE.insert(4, 'silk.middleware.SilkyMiddleware')

DEBUG_SMS_TOKEN = env('DEBUG_SMS_TOKEN', default=None)

METRICS_INFLUXDB['database'] = 'test'
METRICS_INFLUXDB_ANALYTICS['database'] = 'test'
