from django.test import TestCase, tag, Client

from spacetelescope.tests import utils


@tag('pages')
class TestPageTemplate(TestCase):
    fixtures = ['test/common', 'test/pages']

    def setUp(self):
        self.anonymous_client = Client()
        self.admin_client = utils.get_staff_client()

    def test_onecolumn(self):
        response_online = self.anonymous_client.get('/test-online/')
        response_offline = self.anonymous_client.get('/test-not-online/')

        self.assertEqual(response_online.status_code, 200)
        self.assertEqual(response_offline.status_code, 404)

    def test_onecolumn_as_admin(self):
        response = self.admin_client.get('/test-not-online/')
        self.assertEqual(response.status_code, 200)

    def test_onecolumn_coming_soon(self):
        response = self.admin_client.get('/test-online-coming-soon/')
        self.assertEqual(response.status_code, 200)
