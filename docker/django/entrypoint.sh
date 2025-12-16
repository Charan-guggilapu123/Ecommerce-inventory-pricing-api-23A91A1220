#!/bin/sh
set -e

echo "Waiting for postgres..."
sleep 5

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
