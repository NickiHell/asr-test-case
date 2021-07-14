FROM python:3.9-slim-buster as compile-image

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.5

RUN apt-get update && apt-upgrade

RUN pip install --upgrade pip
RUN pip install poetry


COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi


FROM python:3.9-slim-buster as runtime-image
RUN apt-get -q update && apt-get install -y --no-install-recommends vim && apt-get clean && rm -rf /var/lib/apt

ENV TZ=Asia/Vladivostok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY docker/build/etc/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

COPY --from=compile-image /usr/local /usr/local

COPY src /app
WORKDIR /app
