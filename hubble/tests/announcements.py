from django.test import TestCase, tag, Client
from djangoplicity.announcements.models import Announcement, WebUpdate
from djangoplicity.science.models import ScienceAnnouncement

from hubble.tests import utils


@tag('announcements')
class TestAnnouncements(TestCase):
    fixtures = ['test/media', 'test/announcements']

    def setUp(self):
        self.client = Client()
        self.announcement = Announcement.objects.get(pk='10000')
        self.announcement_with_video = Announcement.objects.get(pk='10001')
        self.announcements_number = Announcement.objects.filter(published=True).count()

    def test_announcements(self):
        response = self.client.get('/announcements/')
        pagination_found = utils.eval_pagination_regex(response, self.announcements_number, 'announcements')

        self.assertContains(response, 'Announcements')
        self.assertTrue(pagination_found)

    def test_announcements_detail(self):
        response = self.client.get('/announcements/{}/'.format(self.announcement.pk))
        self.assertContains(response, self.announcement.title)

        response = self.client.get('/announcements/{}/'.format(self.announcement_with_video.pk))
        self.assertContains(response, self.announcement_with_video.title)


@tag('announcements', 'scienceannouncements')
class TestScienceAnnouncements(TestCase):
    fixtures = ['test/media', 'test/announcements']

    def setUp(self):
        self.client = Client()
        self.science_announcement = ScienceAnnouncement.objects.get(pk='10000')
        self.science_announcements_number = ScienceAnnouncement.objects.filter(published=True).count()

    def test_forscientists(self):
        response = self.client.get('/forscientists/announcements/')
        pagination_found = utils.eval_pagination_regex(response, self.science_announcements_number, 'announcements')

        self.assertContains(response, 'Announcements')
        self.assertTrue(pagination_found)

    def test_forscientists_detail(self):
        response = self.client.get('/forscientists/announcements/{}/'.format(self.science_announcement.pk))
        self.assertContains(response, self.science_announcement.title)


@tag('announcements', 'webupdates')
class TestWebUpdates(TestCase):
    fixtures = ['test/media', 'test/announcements']

    def setUp(self):
        self.client = Client()
        self.web_updates_number = WebUpdate.objects.filter(published=True).count()

    def test_announcements_webupdates(self):
        response = self.client.get('/announcements/webupdates/')
        pagination_found = utils.eval_pagination_regex(response, self.web_updates_number, 'web updates')

        self.assertContains(response, 'Web Updates')
        self.assertTrue(pagination_found)
