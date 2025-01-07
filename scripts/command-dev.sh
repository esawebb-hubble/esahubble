#!/bin/sh

# Copy test media that will provide extra coverage for templates
/bin/cp -rf test-utils/media/* docs/static

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial dev
python manage.py runserver 0.0.0.0:8000
