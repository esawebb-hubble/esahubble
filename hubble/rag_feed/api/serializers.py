from rest_framework import serializers
from bs4 import BeautifulSoup
from djangoplicity.pages.models import Page
from djangoplicity.releases.models import Release
from djangoplicity.announcements.models import Announcement
from djangoplicity.newsletters.models import Newsletter
from djangoplicity.science.models import ScienceAnnouncement
from djangoplicity.media.models import Image, PictureOfTheWeek, ImageComparison, Video
from djangoplicity.products2.models import (
    Book, Brochure, Model3d, Application, Calendar, ConferencePoster, Exhibition,
    FITSImage, Logo, Media, Merchandise, PostCard, Presentation,
    PressKit, PrintedPoster, OnlineArt, Sticker, VideoConferenceBackground
)

class RagFeedBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer to standardize the RAG feed output.
    """
    url = serializers.SerializerMethodField()
    text_content = serializers.SerializerMethodField()

    class Meta:
        fields = ('title', 'url', 'date_created', 'last_modified', 'text_content')
        abstract = True

    def get_url(self, obj):
        """
        Gets the absolute URL of the object.
        """
        if hasattr(obj, 'get_absolute_url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.get_absolute_url())
        return None

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content to return only plain text.
        """
        # It will look for a 'content' field by default.
        # This can be overridden in child serializers if the content field has a different name.
        html_content = getattr(obj, 'content', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class PageRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Page model.
    """
    date_created = serializers.DateTimeField(source='created')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Page
        fields = RagFeedBaseSerializer.Meta.fields

class ReleaseRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Release model (Press Releases).
    """
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Release
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the 'description' field.
        """
        html_content = getattr(obj, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class AnnouncementRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Announcement model.
    """
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Announcement
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the 'description' field.
        """
        html_content = getattr(obj, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''


class NewsletterRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Newsletter model.
    """
    # Newsletters use 'subject' instead of 'title'
    title = serializers.CharField(source='subject')
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Newsletter
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content.
        Prioritizes the 'html' field, falls back to 'text' if empty.
        """
        content = getattr(obj, 'html', '')
        if not content:
            content = getattr(obj, 'text', '')

        if content:
            soup = BeautifulSoup(content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class ScienceAnnouncementRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the ScienceAnnouncement model.
    """
    # Use release_date as the creation date
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = ScienceAnnouncement
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the 'description' field.
        """
        html_content = getattr(obj, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class ImageRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Image model in the media application.
    """
    # Images use release_date as their main publication/creation date
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Image
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the 'description' field.
        """
        html_content = getattr(obj, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''


class POTWRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the PictureOfTheWeek (POTW / POTM) model.
    POTW acts as a wrapper, so we extract text and title from its related visual.
    """
    date_created = serializers.DateTimeField(source='release_date')

    # We must explicitly define title because POTW relies on its visual for it
    title = serializers.SerializerMethodField()

    class Meta(RagFeedBaseSerializer.Meta):
        model = PictureOfTheWeek
        fields = RagFeedBaseSerializer.Meta.fields

    def get_title(self, obj):
        """
        Retrieves the title from the associated visual (Image, Video, or Comparison).
        """
        visual = obj.visual()
        if visual and hasattr(visual, 'title'):
            return visual.title
        return obj.id  # Fallback to ID if no title is found

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the description of the associated visual.
        """
        visual = obj.visual()
        if not visual:
            return ''

        html_content = getattr(visual, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class ImageComparisonRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the ImageComparison model.
    """
    # Image comparisons use release_date as their main publication/creation date
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = ImageComparison
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the 'description' field.
        """
        html_content = getattr(obj, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class VideoRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Video model.
    """
    # Videos use release_date as their main publication/creation date
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Video
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the 'description' field.
        """
        html_content = getattr(obj, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class ProductRagFeedSerializer(RagFeedBaseSerializer):
    """
    Generic serializer for Product models inheriting from StandardArchiveInfo.
    """
    # Products use release_date as their main publication date
    date_created = serializers.DateTimeField(source='release_date')

    # We don't define a Meta class with a specific model here,
    # as this serializer will be reused across multiple product models.
    title = serializers.CharField()

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the 'description' field.
        """
        html_content = getattr(obj, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class BookRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(RagFeedBaseSerializer.Meta): model = Book

class BrochureRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(RagFeedBaseSerializer.Meta): model = Brochure

class Model3dRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = Model3d

class ApplicationRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = Application

class CalendarRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = Calendar

class ConferencePosterRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = ConferencePoster

class ExhibitionRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = Exhibition

class FITSImageRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = FITSImage

class LogoRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = Logo

class MediaProductRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = Media

class MerchandiseRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = Merchandise

class PostCardRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = PostCard

class PresentationRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = Presentation

class PressKitRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = PressKit

class PrintedPosterRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = PrintedPoster

class OnlineArtRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = OnlineArt

class StickerRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = Sticker

class VideoConferenceBackgroundRagFeedSerializer(ProductRagFeedSerializer):
    class Meta(ProductRagFeedSerializer.Meta): model = VideoConferenceBackground
