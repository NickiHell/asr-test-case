import fakeredis
import redis

from server.settings.components import BASE_DIR
from server.settings.environments.development import *

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


def patch_redis():
    redis.Redis = fakeredis.FakeRedis()
    redis.StrictRedis = fakeredis.FakeStrictRedis()


patch_redis()

SECRET_KEY = config('DJANGO_SECRET_KEY')

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False

CELERY_TASK_ALWAYS_EAGER = True

AUTH_USER_MODEL = 'users.User'
