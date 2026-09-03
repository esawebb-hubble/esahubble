from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Q

from djangoplicity.pages.models import Page
from djangoplicity.releases.models import Release
from djangoplicity.announcements.models import Announcement
from djangoplicity.newsletters.models import Newsletter
from djangoplicity.science.models import ScienceAnnouncement
from djangoplicity.media.models import Image, PictureOfTheWeek, ImageComparison, Video
from .serializers import *

class RagFeedPagination(PageNumberPagination):
    """
    Custom pagination for the RAG feed endpoints.
    """
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PageListAPIView(ListAPIView):
    """
    View to expose the content of public Pages.
    """
    serializer_class = PageRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only pages that are published
        and within their publication window (no embargo).
        """
        now = timezone.now()
        return Page.objects.filter(
            Q(published=True) &
            (Q(start_publishing__isnull=True) | Q(start_publishing__lte=now)) &
            (Q(end_publishing__isnull=True) | Q(end_publishing__gte=now))
        ).order_by('-last_modified')

class ReleaseListAPIView(ListAPIView):
    """
    View to expose the content of public Press Releases.
    """
    serializer_class = ReleaseRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters to return only published releases that have
        passed their release date (embargo).
        """
        now = timezone.now()
        return Release.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')

class AnnouncementListAPIView(ListAPIView):
    """
    View to expose the content of public Announcements.
    """
    serializer_class = AnnouncementRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only published announcements
        that have passed their release date (embargo).
        """
        now = timezone.now()
        return Announcement.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')

class NewsletterListAPIView(ListAPIView):
    """
    View to expose the content of public Newsletters.
    """
    serializer_class = NewsletterRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only published newsletters
        that have passed their release date.
        """
        now = timezone.now()
        return Newsletter.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')

class ScienceAnnouncementListAPIView(ListAPIView):
    """
    View to expose the content of public Science Announcements.
    """
    serializer_class = ScienceAnnouncementRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only published science announcements
        that have passed their release date (embargo).
        """
        now = timezone.now()
        return ScienceAnnouncement.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')

class ImageListAPIView(ListAPIView):
    """
    View to expose the content of public Images.
    """
    serializer_class = ImageRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only published images
        that have passed their release date (embargo).
        """
        now = timezone.now()
        return Image.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')


class POTWListAPIView(ListAPIView):
    """
    View to expose the content of public Pictures of the Week / Month.
    """
    serializer_class = POTWRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only published POTWs
        that have passed their release date (embargo).
        """
        now = timezone.now()

        # We also use select_related to optimize the database query,
        # since we know the serializer will need to access the related visual.
        return PictureOfTheWeek.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).select_related('image', 'video', 'comparison').order_by('-release_date')

class ImageComparisonListAPIView(ListAPIView):
    """
    View to expose the content of public Image Comparisons.
    """
    serializer_class = ImageComparisonRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only published image comparisons
        that have passed their release date (embargo).
        """
        now = timezone.now()
        return ImageComparison.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')

class VideoListAPIView(ListAPIView):
    """
    View to expose the content of public Videos.
    """
    serializer_class = VideoRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only published videos
        that have passed their release date (embargo).
        """
        now = timezone.now()
        return Video.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')

class BaseProductListAPIView(ListAPIView):
    """
    Abstract base view for all Product models to avoid repeating queryset logic.
    """
    serializer_class = ProductRagFeedSerializer
    pagination_class = RagFeedPagination

    # This must be defined in child classes
    model_class = None

    def get_queryset(self):
        """
        Filters the queryset for published items that have passed their embargo.
        """
        if not self.model_class:
            return []

        now = timezone.now()
        return self.model_class.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')


# --- Specific Product Endpoints ---

class BookListAPIView(BaseProductListAPIView):
    model_class = Book
    serializer_class = BookRagFeedSerializer

class BrochureListAPIView(BaseProductListAPIView):
    model_class = Brochure
    serializer_class = BrochureRagFeedSerializer

class Model3dListAPIView(BaseProductListAPIView):
    model_class = Model3d
    serializer_class = Model3dRagFeedSerializer

class ApplicationListAPIView(BaseProductListAPIView):
    model_class = Application
    serializer_class = ApplicationRagFeedSerializer

class CalendarListAPIView(BaseProductListAPIView):
    model_class = Calendar
    serializer_class = CalendarRagFeedSerializer

class ConferencePosterListAPIView(BaseProductListAPIView):
    model_class = ConferencePoster
    serializer_class = ConferencePosterRagFeedSerializer

class ExhibitionListAPIView(BaseProductListAPIView):
    model_class = Exhibition
    serializer_class = ExhibitionRagFeedSerializer

class FITSImageListAPIView(BaseProductListAPIView):
    model_class = FITSImage
    serializer_class = FITSImageRagFeedSerializer

class LogoListAPIView(BaseProductListAPIView):
    model_class = Logo
    serializer_class = LogoRagFeedSerializer

class MediaProductListAPIView(BaseProductListAPIView):
    model_class = Media
    serializer_class = MediaProductRagFeedSerializer

class MerchandiseListAPIView(BaseProductListAPIView):
    model_class = Merchandise
    serializer_class = MerchandiseRagFeedSerializer

class PostCardListAPIView(BaseProductListAPIView):
    model_class = PostCard
    serializer_class = PostCardRagFeedSerializer

class PresentationListAPIView(BaseProductListAPIView):
    model_class = Presentation
    serializer_class = PresentationRagFeedSerializer

class PressKitListAPIView(BaseProductListAPIView):
    model_class = PressKit
    serializer_class = PressKitRagFeedSerializer

class PrintedPosterListAPIView(BaseProductListAPIView):
    model_class = PrintedPoster
    serializer_class = PrintedPosterRagFeedSerializer

class OnlineArtListAPIView(BaseProductListAPIView):
    model_class = OnlineArt
    serializer_class = OnlineArtRagFeedSerializer

class StickerListAPIView(BaseProductListAPIView):
    model_class = Sticker
    serializer_class = StickerRagFeedSerializer

class VideoConferenceBackgroundListAPIView(BaseProductListAPIView):
    model_class = VideoConferenceBackground
    serializer_class = VideoConferenceBackgroundRagFeedSerializer

