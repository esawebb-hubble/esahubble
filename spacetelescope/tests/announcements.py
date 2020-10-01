import re

from django.test import TestCase, tag, Client
from djangoplicity.announcements.models import Announcement, WebUpdate
from djangoplicity.science.models import ScienceAnnouncement

from spacetelescope.tests import utils


@tag('announcements')
class TestAnnouncements(TestCase):
    fixtures = ['test/media', 'test/announcements']

    def setUp(self):
        self.client = Client()
        self.announcement = Announcement.objects.filter(published=True).first()
        self.science_announcement = ScienceAnnouncement.objects.filter(published=True).first()
        self.web_updates_number = WebUpdate.objects.filter(published=True).count()
        self.announcements_number = Announcement.objects.filter(published=True).count()
        self.science_announcements_number = ScienceAnnouncement.objects.filter(published=True).count()

    def test_announcements(self):
        response = self.client.get('/announcements/')
        regexp = utils.get_pagination_regex(self.announcements_number, 'announcements')

        self.assertContains(response, 'Announcements')
        self.assertTrue(bool(re.search(regexp, response.content)))

    def test_announcements_detail(self):
        response = self.client.get('/announcements/{}/'.format(self.announcement.pk))
        self.assertContains(response, self.announcement.title)

    def test_announcements_webupdates(self):
        response = self.client.get('/announcements/webupdates/')
        regexp = utils.get_pagination_regex(self.web_updates_number, 'web updates')

        self.assertContains(response, 'Web Updates')
        self.assertTrue(bool(re.search(regexp, response.content)))

    def test_forscientists(self):
        response = self.client.get('/forscientists/announcements/')
        regexp = utils.get_pagination_regex(self.science_announcements_number, 'announcements')

        self.assertContains(response, 'Announcements')
        self.assertTrue(bool(re.search(regexp, response.content)))

    def test_forscientists_detail(self):
        response = self.client.get('/forscientists/announcements/{}/'.format(self.science_announcement.pk))
        self.assertContains(response, self.science_announcement.title)
