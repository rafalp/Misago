# This dockerfile is only meant for local development of Misago
# If you are looking for a proper docker setup for running Misago in production,
# please use misago-docker instead
FROM python:3.8 as build-python

# Add requirements and install them
ADD requirements.txt /app/
ADD requirements-dev.txt /app/
ADD requirements-plugins.txt /app/
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    pip install -r /app/requirements-dev.txt && \
    pip install -r /app/requirements-plugins.txt

# Build final (slim) image
FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV IN_MISAGO_DOCKER 1

# Copy from previous image
COPY --from=build-python /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/

# Install dependencies in one single command/layer
RUN apt-get update && apt-get install -y \
    postgresql-client

# Run APP
ADD . /app/

WORKDIR /app/

EXPOSE 8000

CMD uvicorn misago.asgi:app --host 0.0.0.0 --reload
