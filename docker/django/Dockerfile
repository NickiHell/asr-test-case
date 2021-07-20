# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM python:3.9-slim-buster AS development_build


ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  # build:
  BUILD_ONLY_PACKAGES='wget' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # dockerize:
  DOCKERIZE_VERSION=v0.6.1 \
  # tini:
  TINI_VERSION=v0.19.0 \
  # poetry:
  POETRY_VERSION=1.1.7 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"


RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    # Defining build-time-only dependencies:
    $BUILD_ONLY_PACKAGES \
  # Installing `dockerize` utility:
  # https://github.com/jwilder/dockerize
  && wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && rm "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" && dockerize --version \
  # https://github.com/python-poetry/poetry
  && curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
  && poetry --version \
  && apt-get remove -y $BUILD_ONLY_PACKAGES \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./poetry.lock ./pyproject.toml /code/
COPY ./pytest.ini /code/
COPY ./manage.py /code/
COPY ./server /code/server
COPY ./tests /code/tests
COPY ./docker/django/entrypoint.sh docker-entrypoint.sh
COPY ./docker/django/gunicorn.sh gunicorn.sh

# Project initialization:
RUN echo "$DJANGO_ENV" \
  && poetry install \
    $(if [ "$DJANGO_ENV" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction --no-ansi \
  # Upgrading pip, it is insecure, remove after `pip@21.1`
  && poetry run pip install -U pip \
  # Cleaning poetry installation's cache for production:
  && if [ "$DJANGO_ENV" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi


ENTRYPOINT ["bash", "docker-entrypoint.sh"]
