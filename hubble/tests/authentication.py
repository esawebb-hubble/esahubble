from django.test import TestCase, tag, Client
from django.urls import reverse

from hubble.tests import utils

@tag('auth')
class TestAuthentication(TestCase):
    fixtures = ['test/common']

    def setUp(self):
        self.anonymous_client = Client()
        self.admin_client = utils.get_staff_client()
        self.credentials = {'username': 'test_standard', 'password': 'admin'}

    def test_already_logged_in(self):
        login_url = reverse('admin:login')
        index_url = reverse('admin:index')

        response = self.admin_client.get(login_url, follow=True)
        utils.check_redirection_to(self, response, index_url)

    def test_login_error(self):
        response = self.anonymous_client.post(
            '/login/',
            {'username': self.credentials['username'], 'password': 'badpassword'}
        )
        self.assertContains(response, 'Your username and password didn\'t match. Please try again.')

    def test_login_success(self):
        response = self.anonymous_client.post('/login/', self.credentials, follow=True)
        utils.check_redirection_to(self, response, '/')

    def test_logout(self):
        response = self.admin_client.get('/logout/')
        self.assertContains(response, 'You have been successfully logged out.')

    def test_password_reset(self):
        response_get = self.anonymous_client.get('/password_reset/')
        self.assertContains(
            response_get,
            'Forgotten your password?'
        )

        response_post = self.client.post('/password_reset/', data={"email": 'test@email.com'}, follow=True)
        utils.check_redirection_to(self, response_post, '/password_reset/done/')
