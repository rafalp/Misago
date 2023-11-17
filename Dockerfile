# This Dockerfile is intended solely for local development of Misago
# If you are seeking a suitable Docker setup for running Misago in a 
# production, please us misago-docker instead
FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1

# Install dependencies in one single command/layer
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

# Install pip-tools
RUN python -m pip install pip-tools

# Add requirements and install them. We do this unnecessasy rebuilding.
ADD requirements.txt /
ADD requirements-plugins.txt /

RUN pip install --upgrade pip && \
    pip install -r requirements.txt &&

WORKDIR /srv/misago

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
