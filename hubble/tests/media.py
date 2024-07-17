from django.test import TestCase, Client, tag
from djangoplicity.media.models import Video, Image, PictureOfTheWeek, ImageComparison

from spacetelescope.tests import utils


@tag('media', 'images')
class TestImage(TestCase):
    fixtures = ['test/media']

    def setUp(self):
        self.client = Client()
        self.images_number = Image.objects.filter(published=True).count()
        self.potw_number = PictureOfTheWeek.objects.filter(published=True).count()
        self.image_comparisons_number = ImageComparison.objects.filter(published=True).count()

    def test_images(self):
        response = self.client.get('/images/')
        pagination_found = utils.eval_pagination_regex(response, self.images_number, 'images')

        self.assertContains(response, 'Images')
        self.assertTrue(pagination_found)

    def test_images_potw(self):
        response = self.client.get('/images/potw/')
        pagination_found = utils.eval_pagination_regex(response, self.potw_number, 'press releases')

        self.assertContains(response, 'Picture of the Week')
        self.assertTrue(pagination_found)

    def test_image_comparisons(self):
        response = self.client.get('/images/comparisons/')
        pagination_found = utils.eval_pagination_regex(response, self.image_comparisons_number, 'entries')

        self.assertContains(response, 'Image Comparisons')
        self.assertTrue(pagination_found)

    def test_images_top100(self):
        response = self.client.get('/images/archive/top100/')
        self.assertContains(response, 'Top 100 Images')


@tag('media', 'videos')
class TestVideo(TestCase):
    fixtures = ['test/media']

    def setUp(self):
        self.client = Client()
        self.video = Video.objects.get(pk='10000')
        self.videos_number = Video.objects.filter(published=True).count()

    def test_videos_list(self):
        response = self.client.get('/videos/')
        pagination_found = utils.eval_pagination_regex(response, self.videos_number, 'entries')

        self.assertContains(response, 'Videos')
        self.assertTrue(pagination_found)

    def test_videos_detail(self):
        response = self.client.get('/videos/{}/'.format(self.video.id))
        self.assertContains(response, self.video.title)

    def test_video_hubblecast(self):
        response = self.client.get('/videos/archive/category/hubblecast/')
        pagination_found = utils.eval_pagination_regex(response, self.videos_number, 'entries')

        self.assertContains(response, 'All Hubblecasts')
        self.assertTrue(pagination_found)
