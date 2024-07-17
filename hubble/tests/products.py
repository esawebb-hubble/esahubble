from django.test import TestCase, tag
from django.urls import reverse
from djangoplicity.products.models import Book

from hubble.tests import utils

@tag('products')
class TestProducts(TestCase):
    fixtures = ['test/common', 'test/shop', 'test/products']

    def setUp(self):
        self.client = utils.get_standard_client()
        self.published_book = Book.objects.filter(published=True).first()
        self.not_published_book = Book.objects.filter(published=False).first()

    def test_arts(self):
        response = self.client.get('/products/art/')
        self.assertEqual(response.status_code, 200)

    def test_kidsdrawing(self):
        response = self.client.get('/kidsandteachers/drawings/')
        self.assertEqual(response.status_code, 200)

    def test_postcards(self):
        response = self.client.get('/products/postcards/')
        self.assertContains(response, 'Postcards')

    def test_merchandise(self):
        response = self.client.get('/products/merchandise/')
        self.assertContains(response, 'Merchandise')

    def test_book_published(self):
        url = reverse('books_detail', args=[str(self.published_book.id)])
        response = self.client.get(url)

        self.assertContains(response, self.published_book.title, status_code=200)

    def test_book_not_published(self):
        """
        This test provides coverage for:
        hubble/templates/403.html
        """
        url = reverse('books_detail', args=[str(self.not_published_book.id)])
        response = self.client.get(url)

        self.assertContains(response, 'Access Denied', status_code=403)
