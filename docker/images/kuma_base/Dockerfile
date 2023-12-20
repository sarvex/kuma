FROM python:3.12.1-slim@sha256:123229cfb27c384ee1fcc15aec660ad280a09121b7893377e80ae1b2e72cf942

# Set the environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # gunicorn concurrency
    WEB_CONCURRENCY=4

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    dirmngr \
    # Needed for pytz to be able to install
    libsasl2-modules \
    gettext \
    build-essential \
    # Needed for Python to build cffi
    libffi-dev

# add non-privileged user
RUN useradd --uid 1000 --shell /bin/bash --create-home kuma \
    && mkdir -p app \
    && chown kuma:kuma /app \
    && chmod 775 /app

# install Python libraries
WORKDIR /app
COPY --chown=kuma:kuma ./pyproject.toml ./poetry.lock /app/
RUN pip install poetry~=1.1.12 \
    && POETRY_VIRTUALENVS_CREATE=false poetry install --no-root \
    && rm -rf ~/.cache/pip ~/.cache/pypoetry/cache

# setup default run parameters
USER kuma
WORKDIR /app
EXPOSE 8000
