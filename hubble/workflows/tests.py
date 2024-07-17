from __future__ import absolute_import
# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
import unittest
from django.core import mail
from .media import video_rename
from django.test import TestCase

class EmailTest(TestCase):
    def test_video_rename(self):
        # Send message.
        video_rename(1,2)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Video renamed: 1 -> 2')

