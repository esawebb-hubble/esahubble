from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^pages/$', PageListAPIView.as_view(), name='rag-feed-pages'),
    url(r'^releases/$', ReleaseListAPIView.as_view(), name='rag-feed-releases'),
    url(r'^announcements/$', AnnouncementListAPIView.as_view(), name='rag-feed-announcements'),
    url(r'^newsletters/$', NewsletterListAPIView.as_view(), name='rag-feed-newsletters'),
    url(r'^science-announcements/$', ScienceAnnouncementListAPIView.as_view(), name='rag-feed-science-announcements'),
    url(r'^media/images/$', ImageListAPIView.as_view(), name='rag-feed-media-images'),
    url(r'^media/potm/$', POTWListAPIView.as_view(), name='rag-feed-media-potws'),
    url(r'^media/comparisons/$', ImageComparisonListAPIView.as_view(), name='rag-feed-media-comparisons'),
    url(r'^media/videos/$', VideoListAPIView.as_view(), name='rag-feed-media-videos'),
    # Products
    url(r'^products/books/$', BookListAPIView.as_view(), name='rag-feed-books'),
    url(r'^products/brochures/$', BrochureListAPIView.as_view(), name='rag-feed-brochures'),
    url(r'^products/models3d/$', Model3dListAPIView.as_view(), name='rag-feed-models'),
    url(r'^products/applications/$', ApplicationListAPIView.as_view(), name='rag-feed-applications'),
    url(r'^products/calendars/$', CalendarListAPIView.as_view(), name='rag-feed-calendars'),
    url(r'^products/conference-posters/$', ConferencePosterListAPIView.as_view(), name='rag-feed-conference-posters'),
    url(r'^products/exhibitions/$', ExhibitionListAPIView.as_view(), name='rag-feed-exhibitions'),
    url(r'^products/fits-images/$', FITSImageListAPIView.as_view(), name='rag-feed-fits-images'),
    url(r'^products/logos/$', LogoListAPIView.as_view(), name='rag-feed-logos'),
    url(r'^products/media/$', MediaProductListAPIView.as_view(), name='rag-feed-media-products'),
    url(r'^products/merchandise/$', MerchandiseListAPIView.as_view(), name='rag-feed-merchandise'),
    url(r'^products/postcards/$', PostCardListAPIView.as_view(), name='rag-feed-postcards'),
    url(r'^products/presentations/$', PresentationListAPIView.as_view(), name='rag-feed-presentations'),
    url(r'^products/press-kits/$', PressKitListAPIView.as_view(), name='rag-feed-press-kits'),
    url(r'^products/printed-posters/$', PrintedPosterListAPIView.as_view(), name='rag-feed-printed-posters'),
    url(r'^products/space-art/$', OnlineArtListAPIView.as_view(), name='rag-feed-space-art'),
    url(r'^products/stickers/$', StickerListAPIView.as_view(), name='rag-feed-stickers'),
    url(r'^products/video-conference-backgrounds/$', VideoConferenceBackgroundListAPIView.as_view(), name='rag-feed-video-conference-backgrounds'),
]
