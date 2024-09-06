#!/usr/bin/env bash

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
done 

alembic upgrade head

gunicorn main:app --bind 0.0.0.0:8000 --workers 3 -k uvicorn.workers.UvicornWorker