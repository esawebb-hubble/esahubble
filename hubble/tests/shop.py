from django.test import TestCase, tag, Client
from product.models import Category, Product
from satchmo_store.shop.models import Config

from hubble.tests import utils


@tag('shop')
class TestShop(TestCase):
    fixtures = ['test/common', 'test/shop']

    def setUp(self):
        self.client = Client()

        self.shop = Config.objects.first()

        # Shows a category hierarchy in product_detail view
        self.category = Category.objects.get(pk=10000)
        self.category_with_meta = Category.objects.get(pk=10002)
        self.product = Product.objects.first()

    def test_index(self):
        response = self.client.get('/shop/')
        self.assertContains(response, self.shop.store_name)

    def test_freeorder(self):
        response = self.client.get('/shop/freeorder/')
        self.assertContains(response, 'Full Name')
        self.assertContains(response, 'Email Address')
        self.assertContains(response, 'Country of delivery')
        self.assertContains(response, 'Justification')

    def test_freeorder_done(self):
        # Submit form in order to proceed to freeorder confirmation
        response = self.client.post(
            '/shop/freeorder/',
            data={
                'name': 'jhon doe',
                'email': 'doe@test.com',
                'newsletter': 'on',
                'country': 10000,
                'justification': 'Whatever',
                'g-recaptcha-response': None
            }
        )
        self.assertContains(response, 'Free order application submitted')

    def test_category_detail(self):
        response = self.client.get('/shop/category/{}/'.format(self.category.slug))
        self.assertContains(response, self.category.name)

    def test_category_detail_meta(self):
        response = self.client.get('/shop/category/{}/'.format(self.category_with_meta.slug))
        self.assertContains(response, self.category.name)

    def test_product_process(self):
        # Visit cart page without products in cart
        response = self.client.get('/shop/cart/')
        self.assertContains(response, 'Shopping Cart')

        # Add some products to cart, in order to render the cart_box template in the product detail
        response = self.client.post('/shop/add/', {
            'quantity': 3,
            'productname': self.product.slug
        })
        self.assertEqual(response.status_code, 302)

        # Visit product detail
        response = self.client.get('/shop/product/{}/'.format(self.product.slug))
        self.assertContains(response, self.product.name)

        # Visit cart page
        response = self.client.get('/shop/cart/')
        self.assertContains(response, self.product.name)

        # Visit checkout page
        response = self.client.get('/shop/checkout/')
        self.assertContains(response, 'Step 1 of 3')

        # Bad submit form in order to raise form errors
        response = self.client.post(
            '/shop/checkout/',
            {
                'paymentmethod': 'CONCARDIS',
                'ship_country': 10000,
                'discount': '000'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Submit form in order to proceed to payment
        response = self.client.post(
            '/shop/checkout/',
            {
                'paymentmethod': 'CONCARDIS',
                'email': 'test@mail.com',
                'city': 'Neverland',
                'first_name': 'Sheldon',
                'last_name': 'Cooper',
                'phone': '69300012',
                'addressee': 'Amy Farrah Fowler',
                'street1': 'In the middle of Nowhere',
                'street2': 'Maybe you should look behing you',
                'state': 'Bermuda',
                'postal_code': '23836',
                'country': 10000,
                'copy_address': 'on',
                'discount': '666',
            },
            follow=True
        )
        utils.check_redirection_to(self, response, '/shop/checkout/payment/')

        # Submit form in order to proceed to confirmation
        response = self.client.post(
            '/shop/checkout/payment/',
            {
                'shipping': 'PUP1'
            },
            follow=True
        )
        utils.check_redirection_to(self, response, '/shop/checkout/payment/confirm/')

        # We can't check concardis, but we can assume the order was placed successfully
        response = self.client.get('/shop/checkout/success/')
        self.assertContains(response, 'Order successfully completed')

    def check_redirection_to(self, response, to):
        redirects_number = len(response.redirect_chain)
        last_url, status_code = response.redirect_chain[-1] if redirects_number > 0 else (None, None)

        self.assertGreater(redirects_number, 0)
        self.assertEqual(status_code, 302)
        self.assertEqual(last_url, to)
