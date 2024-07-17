#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    environment = os.environ.get('ENVIRONMENT', 'dev')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hubble.settings.{}".format(environment))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
