#!/usr/bin/env bash
# Sometimes postgres is not ready before django attempts to connect.
# This script waits until we can do a basic select before continuing.
export PGPASSWORD=$POSTGRES_PASSWORD
RETRIES=10

until psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 5
done
