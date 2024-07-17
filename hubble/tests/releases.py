from django.test import TestCase, tag, Client
from djangoplicity.releases.models import Release

from hubble.tests import utils


@tag('releases')
class TestReleases(TestCase):
    fixtures = ['test/common', 'test/media', 'test/releases']

    def setUp(self):
        self.anonymous_client = Client()
        self.admin_client = utils.get_staff_client()

        self.release = Release.objects.get(pk=10000)
        self.release_staging = Release.objects.get(pk=10001)
        self.release_unpublished = Release.objects.get(pk=10002)
        self.release_embargoed = Release.objects.get(pk=10003)

    def test_news(self):
        response = self.anonymous_client.get('/news/')
        self.assertContains(response, 'Press Releases')

    def test_release_detail(self):
        response = self.anonymous_client.get('/news/{}/'.format(self.release.pk))
        self.assertContains(response, self.release.title)

    def test_release_embargoed(self):
        response = self.admin_client.get('/news/{}/'.format(self.release_embargoed.pk))
        self.assertContains(response, self.release_embargoed.title)

    def test_release_staging(self):
        response = self.admin_client.get('/news/{}/'.format(self.release_staging.pk))
        self.assertContains(response, self.release_staging.title)

    def test_release_unpublished(self):
        response = self.admin_client.get('/news/{}/'.format(self.release_unpublished.pk))
        self.assertContains(response, self.release_unpublished.title)

    def test_release_kids(self):
        response = self.anonymous_client.get('/news/{}/kids/'.format(self.release.pk))
        self.assertContains(response, self.release.kids_title)
