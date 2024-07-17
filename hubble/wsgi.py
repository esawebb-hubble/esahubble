# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2009-2014 ESO

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
import os

environment = os.environ.get('ENVIRONMENT', 'dev')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spacetelescope.settings.{}".format(environment))

application = get_wsgi_application()
