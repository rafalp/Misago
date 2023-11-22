# This Dockerfile is intended solely for local development of Misago
# If you are seeking a suitable Docker setup for running Misago in a 
# production, please use misago-docker instead
FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1
ENV MISAGO_PLUGINS "/app/plugins"

# Install env dependencies in one single command/layer
RUN apt-get update && apt-get install -y \
    vim \
    libffi-dev \
    libssl-dev \
    sqlite3 \
    libjpeg-dev \
    libopenjp2-7-dev \
    locales \
    cron \
    postgresql-client-15 \
    gettext

# Add files and dirs for build step
ADD dev /app/dev
ADD requirements.txt /app/requirements.txt
ADD plugins /app/plugins

WORKDIR /app/

# Install Misago requirements
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    pip install pip-tools

# Bootstrap plugins
RUN ./dev bootstrap_plugins

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000 --noreload
