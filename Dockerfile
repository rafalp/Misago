# This dockerfile is only meant for local development of Misago
# If you are looking for a proper docker setup for running Misago in production,
# please use misago-docker instead
FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1

# Install dependencies in one single command/layer
RUN apt-get update && apt-get install -y \
    vim \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    locales \
    postgresql-client \
    gettext

# Add requirements and install them.
ADD requirements.txt /
ADD requirements-dev.txt /
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

WORKDIR /app/

EXPOSE 8000

CMD uvicorn misago.asgi:app --host 0.0.0.0 --reload
