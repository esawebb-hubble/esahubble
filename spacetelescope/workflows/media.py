# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
from django.conf import settings
from django.core.mail import send_mail


def video_rename( pk=None, new_pk=None ):
    """
    Workflow step to notify a list of users, about an online video that has been
    renamed. Used to keep the master file archive up-to-date with the online archive.
    """

    msg_subject = 'Video renamed: %s -> %s' % (pk, new_pk)
    msg_body = """http://www.spacetelescope.org/videos/%s/""" % new_pk
    msg_from = settings.DEFAULT_FROM_EMAIL
    msg_to = settings.VIDEO_RENAME_NOTIFY
    print("Sending emails to: {}".format(msg_to))
    # TODO: ESA/Hubble uses Mailgun to send emails. Please check how to add the msg_to emails to the recipients
    # send_mail( msg_subject, msg_body, msg_from, msg_to, fail_silently=False )
