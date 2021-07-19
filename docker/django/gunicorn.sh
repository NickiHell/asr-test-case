#!/usr/bin/env sh

set -o errexit
set -o nounset

export DJANGO_ENV
export DJANGO_SETTINGS_MODULE=server.settings

cd /code

python manage.py migrate --noinput
python manage.py collectstatic --noinput

/usr/local/bin/gunicorn server.asgi:application -k uvicorn.workers.UvicornWorker \
  --workers=4 \
  --max-requests=2000 \
  --max-requests-jitter=400 \
  --bind='0.0.0.0:8000'\
  --chdir='/' \
  --log-file=- \
  --worker-tmp-dir='/dev/shm'
