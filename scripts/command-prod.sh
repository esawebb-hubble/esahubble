#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
newrelic-admin run-program gunicorn --workers 4 --log-level info --timeout 300 --bind 0.0.0.0:8000 spacetelescope.wsgi:application
