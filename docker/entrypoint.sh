#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 2
    done
    sleep 2
    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
alembic upgrade head

exec "$@"