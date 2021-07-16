import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .base import *
from .logs import LOGGING


DEBUG = env('DEBUG', default='0') == '1'
IS_TEST_PS = env('IS_TEST_PS', default='0') == '1'

DEFAULT_DATABASE_BACKEND = 'django_db_geventpool.backends.postgresql_psycopg2'
engine = env('DATABASE_BACKEND', default=DEFAULT_DATABASE_BACKEND)
DATABASES['default'] = env.db('DATABASE_URL', engine=engine)
DATABASES['default']['CONN_MAX_AGE'] = 0
if engine == DEFAULT_DATABASE_BACKEND:
    DATABASES['default']['OPTIONS'] = {
        'MAX_CONNS': env.int('DATABASE_MAX_CONNS', default=5),
    }


sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
    traces_sample_rate=env.bool('ENABLE_APM', default=False),
    send_default_pii=True,
    environment=env('SENTRY_ENVIRONMENT', default='development'),
    release=env('RELEASE').lower(),
)

LOGGING['formatters']['simple'] = {
            'format': 'WEB %(message)s'
        }
LOGGING['handlers']['external'] = {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': env('MONITORING_LOG_PATH', default='/tmp/monitoring.log'),
        }
LOGGING['loggers']['external-file-monitoring'] = {
            'level': 'INFO',
            'handlers': ['console', 'external'],
            'propagate': False,
        }

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

PRIVATE_STORAGE_SERVER = 'nginx'
PRIVATE_STORAGE_INTERNAL_URL = '/private-x-accel-redirect/'
