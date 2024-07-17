from django.test import TestCase, Client, tag

from hubble.tests import utils

@tag('general')
class TestGeneralPurpose(TestCase):
    def setUp(self):
        self.client = Client()

    def test_feed(self):
        response = self.client.get('/rss/feed.xml', follow=True)
        utils.check_redirection_to(self, response, 'https://feeds.feedburner.com/hubble_news/')

    def test_d2d_view(self):
        response = self.client.get('/d2d/')

        json_response = utils.load_json(response)

        self.assertIn('Creator', json_response)
        self.assertIn('URL', json_response)

        self.assertEqual('ESA/Hubble', json_response.get('Creator'))
        self.assertEqual('https://www.esahubble.org', json_response.get('URL'))
