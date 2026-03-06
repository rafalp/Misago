# This Dockerfile is intended solely for local development of Misago
# If you are seeking a suitable Docker setup for running Misago in a 
# production, please use misago-docker instead
FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1
ENV MISAGO_PLUGINS "/app/plugins"

# Install env dependencies in one single command/layer
RUN apt-get update && apt-get install --no-install-recommends -y \
    vim \
    libffi-dev \
    libssl-dev \
    sqlite3 \
    libjpeg-dev \
    libopenjp2-7-dev \
    locales \
    cron \
    postgresql-client-15 \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Add files and dirs for build step
COPY dev /app/dev
COPY requirements.txt /app/requirements.txt
COPY plugins /app/plugins

WORKDIR /app/

# Install Misago requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir pip-tools

# Bootstrap plugins
RUN ./dev bootstrap_plugins

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
