# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

import django.views
import django.views.defaults

from django.conf import settings
from django.conf.urls import include, url
from django.views.decorators.cache import cache_page
from django.views.generic.base import RedirectView

import djangoplicity.views
from djangoplicity.announcements.models import Announcement, WebUpdate
from djangoplicity.announcements.options import AnnouncementOptions, WebUpdateOptions
from djangoplicity.media.models import Image, Video, PictureOfTheWeek, ImageComparison
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions, ImageComparisonOptions
from djangoplicity.menus.views import sitemap
from djangoplicity.newsletters.models import Newsletter
from djangoplicity.newsletters.options import NewsletterOptions
from djangoplicity.pages.views import view_page
from djangoplicity.products2.models import Book, Brochure, Calendar, Logo, Exhibition, FITSImage, Sticker, PostCard, \
    PrintedPoster, ConferencePoster, Merchandise, Presentation, Model3d, \
    OnlineArtAuthor, Application, Media, OnlineArt, PressKit, VideoConferenceBackground

from djangoplicity.products2.options import BrochureOptions, CalendarOptions, LogoOptions, ExhibitionOptions, \
    FITSImageOptions, StickerOptions, PostCardOptions, PrintedPosterOptions, ConferencePosterOptions, \
    MerchandiseOptions, PresentationOptions, Model3dOptions, OnlineArtAuthorOptions, \
    ApplicationOptions, MediaOptions, OnlineArtOptions, PressKitOptions, BookOptions, VideoConferenceBackgroundOptions
from djangoplicity.releases.models import Release
from djangoplicity.releases.options import ReleaseOptions
from djangoplicity.science.models import ScienceAnnouncement
from djangoplicity.science.options import ScienceAnnouncementOptions

from spacetelescope.admin import admin_site, adminlogs_site, adminshop_site
from spacetelescope.frontpage.api.views.image_views import ESASkyListView
from spacetelescope.frontpage.views import FrontpageView, d2d


urlpatterns = []

if not settings.DEBUG:
    urlpatterns += [
        url( r'^%s(?P<path>.*)' % settings.MEDIA_URL[1:], djangoplicity.archives.contrib.security.views.serve_static_file),
    ]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += [

    # Djangoplicity Adminstration
    url( r'^admin/cache/', include( ('djangoplicity.cache.urls', "cache"), namespace="admincache_site" )),
    url( r'^admin/history/', include( ('djangoplicity.adminhistory.urls', "history"), namespace="adminhistory_site" )),
    url( r'^admin/system/', adminlogs_site.urls, { 'extra_context': { 'ADMINLOGS_SITE': True }  } ),
    url( r'^admin/', admin_site.urls, { 'extra_context': { 'ADMIN_SITE': True }  } ),
    url( r'^admin/import/', include('djangoplicity.archives.importer.urls') ),
    url( r'^admin/', include('djangoplicity.metadata.wtmlimport.urls'), { 'extra_context': { 'ADMIN_SITE': True }  } ),
    url( r'^public/djangoplicity/admin/reportsdetails/', include( 'djangoplicity.reports.urls' ) ),
    url(r'^tinymce/', include('tinymce.urls')),

    # Djangoplicity pages API
    url( r'^public/djangoplicity/admin/pages/', include('djangoplicity.pages.urls') ),

    # Server alive check (used for load balancers - called every 5 secs )
    url( r'^alive-check.dat$', djangoplicity.views.alive_check ),

    # Media Archive
    url( r'^images/potw/', include('djangoplicity.media.urls_potw'), { 'model': PictureOfTheWeek, 'options': PictureOfTheWeekOptions } ),
    url( r'^images/comparisons/', include('djangoplicity.media.urls_imagecomparisons'), { 'model': ImageComparison, 'options': ImageComparisonOptions } ),
    url( r'^images/', include('djangoplicity.media.urls_images'), { 'model': Image, 'options': ImageOptions } ),
    url( r'^news/', include('djangoplicity.releases.urls'), { 'model': Release, 'options': ReleaseOptions } ),
    url( r'^videos/', include('djangoplicity.media.urls_videos'), { 'model': Video, 'options': VideoOptions } ),

    # Other archives
    url( r'^announcements/webupdates/', include('djangoplicity.announcements.urls_webupdates'), { 'model': WebUpdate, 'options': WebUpdateOptions } ),
    url( r'^announcements/', include('djangoplicity.announcements.urls'), { 'model': Announcement, 'options': AnnouncementOptions } ),

    ### ENTIRE BLOCK REFERENCING djangoplicity.products
    url( r'^about/further_information/books/', include('djangoplicity.products2.urls.books'), { 'model': Book, 'options': BookOptions } ),

    # Products
    url( r'^about/further_information/brochures/', include('djangoplicity.products2.urls.brochures'), {'model': Brochure, 'options': BrochureOptions} ),
    url( r'^products/models3d/', include('djangoplicity.products2.urls.models3d'), { 'model': Model3d, 'options': Model3dOptions, 'translate': True } ),
    url( r'^products/calendars/', include('djangoplicity.products2.urls.calendars'), { 'model': Calendar, 'options': CalendarOptions, 'translate': True  } ),
    url( r'^products/applications/', include('djangoplicity.products2.urls.applications'), { 'model': Application, 'options': ApplicationOptions } ),
    url( r'^products/conf_posters/', include('djangoplicity.products2.urls.conf_posters'), { 'model': ConferencePoster, 'options': ConferencePosterOptions, 'translate': True  } ),
    url( r'^products/exhibitions/', include('djangoplicity.products2.urls.exhibitions'), { 'model': Exhibition, 'options': ExhibitionOptions, 'translate': True  } ),
    url( r'^products/logos/', include('djangoplicity.products2.urls.logos'), { 'model': Logo, 'options': LogoOptions, 'translate': True  } ),
    url( r'^products/merchandise/', include('djangoplicity.products2.urls.merchandise'), { 'model': Merchandise, 'options': MerchandiseOptions, 'translate': True  } ),
    url( r'^products/postcards/', include('djangoplicity.products2.urls.postcards'), { 'model': PostCard, 'options': PostCardOptions, 'translate': True  } ),
    url( r'^products/presentations/', include('djangoplicity.products2.urls.presentations'), { 'model': Presentation, 'options': PresentationOptions, 'translate': True  } ),
    url( r'^products/print_posters/', include('djangoplicity.products2.urls.print_posters'), { 'model': PrintedPoster, 'options': PrintedPosterOptions, 'translate': True  } ),
    url(r'^press/kits/', include('djangoplicity.products2.urls.presskits'), {'model': PressKit, 'options': PressKitOptions}),

    url( r'^products/media/', include('djangoplicity.products2.urls.media'), { 'model': Media, 'options': MediaOptions } ),
    url( r'^products/stickers/', include('djangoplicity.products2.urls.stickers'), { 'model': Sticker, 'options': StickerOptions, 'translate': True  } ),
    url( r'^products/video-conference-backgrounds/', include('djangoplicity.products2.urls.videobackgrounds'), { 'model': VideoConferenceBackground, 'options': VideoConferenceBackgroundOptions, } ),
    url( r'^products/art/', include('djangoplicity.products2.urls.art'), { 'model': OnlineArt, 'options': OnlineArtOptions } ),
    # Virtual tours
    url( r'^products/artists/', include('djangoplicity.products2.urls.artists'), { 'model': OnlineArtAuthor, 'options': OnlineArtAuthorOptions, 'translate': True  } ),

    url( r'^forscientists/announcements/', include('djangoplicity.science.urls'), { 'model': ScienceAnnouncement, 'options': ScienceAnnouncementOptions } ),

    url( r'^projects/fits_liberator/fitsimages/', include('djangoplicity.products2.urls.fitsimages'), { 'model': FITSImage, 'options': FITSImageOptions } ),


    url( r'^rss/feed.xml$', RedirectView.as_view(url='https://feeds.feedburner.com/hubble_news/') ),
    url( r'^rss/vodcast.xml$', RedirectView.as_view(url='https://feeds.feedburner.com/hubblecast_sd/') ),
    url( r'^rss/vodcasthd.xml$', RedirectView.as_view(url='https://feeds.feedburner.com/hubblecast/') ),
    url( r'^rss/vodcastfullhd.xml$', RedirectView.as_view(url='https://feeds.feedburner.com/hubblecast_fullhd/') ),
    url( r'^rss/hubblecasthd_amp.xml$', RedirectView.as_view(url='https://feeds.feedburner.com/hubblecast/') ),

    # User authentication
    url( r'^login/$', django.contrib.auth.views.LoginView.as_view(template_name='login.html') ),
    url( r'^logout/$', django.contrib.auth.views.LogoutView.as_view(template_name='logout.html') ),
    url( r'^password_reset/$', django.contrib.auth.views.PasswordResetView.as_view(email_template_name='registration/password_reset_email.txt'), name='password_reset' ),
    url( r'^password_reset/done/$', django.contrib.auth.views.PasswordResetDoneView.as_view(), name='password_reset_done' ),
    url( r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', django.contrib.auth.views.PasswordResetConfirmView.as_view(), name='django.contrib.auth.views.password_reset_confirm' ),
    url( r'^reset/done/$', django.contrib.auth.views.PasswordResetCompleteView.as_view(), name='password_reset_complete' ),

    # Shop
    url( r'^newsletters/', include( ('djangoplicity.mailinglists.urls', 'djangoplicity_mailinglists'), namespace='djangoplicity_mailinglists' ) ),
    url( r'^newsletters/', include( 'djangoplicity.newsletters.urls'), { 'model': Newsletter, 'options': NewsletterOptions, } ),
    url( r'^facebook/', include('djangoplicity.iframe.urls')  ),

    # Main view
    url( r'^$', cache_page(60 * 5)(FrontpageView.as_view()) ),

    #ESASky API for JSONFeed
    url(r'^zoomables/$', ESASkyListView.as_view()),

    # Sitemap
    url(r'^sitemap/$', sitemap),

    url( r'^d2d/$', d2d ),

    # Static pages
    url(r'^(?P<url>.*/)$', view_page)
]

# Static files/media serving during development
if settings.SERVE_STATIC_MEDIA:
    urlpatterns += [
        url( r'^' + settings.DJANGOPLICITY_MEDIA_URL[1:] + r'(?P<path>.*)$', django.views.static.serve, {'document_root': settings.DJANGOPLICITY_MEDIA_ROOT, 'show_indexes': True } ),
        url( r'^' + settings.MEDIA_URL[1:] + r'(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True } ),
    ]
