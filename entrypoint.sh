#!/bin/sh
set -e

# Apply any pending migrations against the mounted SQLite volume on every boot.
python manage.py migrate --noinput

# Collect static files into STATIC_ROOT so WhiteNoise can serve them.
python manage.py collectstatic --noinput

exec "$@"
