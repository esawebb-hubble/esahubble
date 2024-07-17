# -*- coding: utf-8 -*-
#
# esahubble.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

"""
Creation of LDAP/ADS users.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend


def user_create_handler( sender=None, instance=None, created=None, raw=False, **kwargs ):
    """
    When creating a user via the admin. Populate the user from ldap if possible and set
    an unusuable password.
    """
    if created and not raw:
        try:
            backend = LDAPBackend()
            u = backend.populate_user( instance.username )
            u.set_unusable_password()
            u.save()
        except Exception:
            pass

post_save.connect( user_create_handler, User )
