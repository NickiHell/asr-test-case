from .base import *

DEBUG = IS_TEST_PS = True

DATABASES['default'] = env.db('DATABASE_URL', default='pgsql://postgres:@localhost:5432/test')
