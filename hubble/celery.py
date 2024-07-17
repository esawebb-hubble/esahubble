# -*- coding: utf-8 -*-
#
# esahubble.org
# Copyright 2014 ESO & ESA/Hubble
#
# Authors:
#   Mathias Andre <mandre@eso.org>

from __future__ import absolute_import
from __future__ import print_function
import sys

from celery import Celery

from django.conf import settings
import os

environment = os.environ.get('ENVIRONMENT', 'dev')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hubble.settings.{}".format(environment))

app = Celery('hubble')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# A strange bug with Celery makes the first few tasks fail if CONN_MAX_AGE
# is set:
# OperationalError: could not receive data from server: Bad file descriptor
# As a workaround we disable the settings if running in celery
if 'celery' in sys.argv[0]:
    print('Djangoplicity: Disabling CONN_MAX_AGE')
    settings.DATABASES['default']['CONN_MAX_AGE'] = 0


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
