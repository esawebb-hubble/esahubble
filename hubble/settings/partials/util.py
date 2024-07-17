import os
from django.core.exceptions import ImproperlyConfigured


def get_secret(key, required=True):
    if required and key not in os.environ:
        raise ImproperlyConfigured('The environment variable {} is not configured'.format(key))
    return os.environ.get(key)
