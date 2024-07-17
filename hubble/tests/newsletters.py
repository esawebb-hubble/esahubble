from django.test import TestCase, tag
from djangoplicity.newsletters.models import NewsletterType, Newsletter

from hubble.tests import utils

@tag('newsletters')
class TestNewsletters(TestCase):
    fixtures = [
        'test/common',
        'test/media',
        'test/announcements',
        'test/releases',
        'test/highlights',
        'test/newsletters'
    ]

    def setUp(self):
        self.client = utils.get_staff_client()

        self.newsletter_types = NewsletterType.objects.all()
        self.newsletter = Newsletter.objects.filter(published=True, send__isnull=False).first()

    def test_newsletter_generation(self):
        for newsletter_type in self.newsletter_types:
            response = self.client.post(
                '/admin/newsletters/newsletter/new/',
                {
                    'type': newsletter_type.pk,
                    'start_date_0': '01/01/2000',
                    'start_date_1': '00:00:00',
                    'end_date_0': '31/12/2220',
                    'end_date_1': '23:59:59',
                    '_generate': 'Generate'
                },
                follow=True
            )
            utils.check_redirection_to(self, response, r'/admin/newsletters/newsletter/[0-9]+/change/')

    def test_newsletter_list(self):
        url = '/newsletters/{}/'.format(self.newsletter.type.slug)

        response = self.client.get('{}{}'.format(url, '?search=this+does+not+exists'))
        self.assertContains(response, 'No entries were found')

        response = self.client.get(url)
        self.assertContains(response, self.newsletter.type.name)

    def test_newsletter_detail(self):
        response = self.client.get('/newsletters/{}/html/{}/'.format(self.newsletter.type.slug, self.newsletter.pk))
        self.assertContains(response, self.newsletter.subject)
