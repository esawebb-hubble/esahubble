# -*- coding: utf-8 -*-
#
# esahubble.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from djangoplicity.contrib.admin.sites import AdminSite
from djangoplicity.contrib.admin.discover import autoregister

# Import all admin interfaces we need
import django.contrib.auth.admin
import django.contrib.redirects.admin
import django.contrib.sites.admin
import djangoplicity.announcements.admin
import djangoplicity.customsearch.admin
import djangoplicity.mailinglists.admin
import djangoplicity.media.admin
import djangoplicity.menus.admin
import djangoplicity.metadata.admin
import djangoplicity.newsletters.admin
import djangoplicity.pages.admin
import djangoplicity.releases.admin
import djangoplicity.reports.admin
import djangoplicity.science.admin
import hubble.frontpage.admin
# Products imports
from djangoplicity.contrib.admin import DjangoplicityModelAdmin
from djangoplicity.products2.admin import register_if_installed, ExhibitionGroupAdmin, OnlineArtAuthorAdmin, \
    ConferenceAdmin
from djangoplicity.products2.base.models import ArchiveCategory
from djangoplicity.products2.models import Model3d, Calendar, Application, Book, Brochure, Logo, Exhibition, \
    Sticker, PostCard, PrintedPoster, ConferencePoster, Merchandise, Media, Presentation, OnlineArt, \
    ExhibitionGroup, OnlineArtAuthor, PressKit, FITSImage, VideoConferenceBackground
from djangoplicity.products2.options import Model3dOptions, CalendarOptions, ApplicationOptions, LogoOptions, \
    ExhibitionOptions, StickerOptions, PostCardOptions, PrintedPosterOptions, ConferencePosterOptions, \
    MerchandiseOptions, MediaOptions, PresentationOptions, OnlineArtOptions, PressKitOptions, BrochureOptions, \
    FITSImageOptions, BookOptions, VideoConferenceBackgroundOptions


# Register each applications admin interfaces with
# an admin site.
admin_site = AdminSite( name="admin_site" )
adminlogs_site = AdminSite( name="adminlogs_site" )
adminshop_site = AdminSite( name="adminshop_site" )

autoregister( admin_site, djangoplicity.announcements.admin )
autoregister( admin_site, django.contrib.auth.admin )
autoregister( admin_site, django.contrib.sites.admin )
autoregister( admin_site, djangoplicity.menus.admin )
autoregister( admin_site, djangoplicity.pages.admin )
autoregister( admin_site, djangoplicity.media.admin )
autoregister( admin_site, djangoplicity.releases.admin )
autoregister( admin_site, djangoplicity.metadata.admin )
#autoregister( admin_site, djangoplicity.events.admin )
autoregister( admin_site, djangoplicity.mailinglists.admin )
autoregister( admin_site, djangoplicity.newsletters.admin )
autoregister( admin_site, djangoplicity.customsearch.admin )
#autoregister( admin_site, djangoplicity.eventcalendar.admin )
autoregister( admin_site, djangoplicity.science.admin )
autoregister( admin_site, hubble.frontpage.admin )
autoregister( admin_site, djangoplicity.contacts.admin )
autoregister( adminlogs_site, djangoplicity.actions.admin )
autoregister( adminlogs_site, djangoplicity.admincomments.admin )


#
# Applications that does not support above method.
#
djangoplicity.reports.admin.advanced_register_with_admin(admin_site)

adminlogs_site.register(django.contrib.redirects.models.Redirect,
                        django.contrib.redirects.admin.RedirectAdmin)

adminlogs_site.register(django.contrib.sites.models.Site,
                        django.contrib.sites.admin.SiteAdmin)

admin_site.register(django.contrib.auth.models.User,
                    django.contrib.auth.admin.UserAdmin)

admin_site.register(django.contrib.auth.models.Group,
                    django.contrib.auth.admin.GroupAdmin)




# autoregister( adminshop_site, djangoplicity.archives.contrib.satchmo.freeorder.admin )

# Products 2 admin register

def register_products_with_admin( admin_site ):
    register_if_installed( admin_site, Model3d, Model3dOptions )
    register_if_installed( admin_site, Calendar, CalendarOptions, name='Calendar' )
    register_if_installed( admin_site, Application, ApplicationOptions )
    register_if_installed(admin_site, Book, BookOptions,
                          extra={'search_fields': ['isbn'], 'fieldsets': [('Extra', {'fields': ('isbn', 'doi'), }), ]})
    register_if_installed(admin_site, Brochure, BrochureOptions, exclude=['embargo_date', 'created', 'last_modified'])
    register_if_installed( admin_site, Logo, LogoOptions )
    register_if_installed( admin_site, Exhibition, ExhibitionOptions, extra={ 'list_display': ['group', 'group_order'], 'list_editable': ['group', 'group_order'], } )
    register_if_installed( admin_site, FITSImage, FITSImageOptions )
    register_if_installed( admin_site, Sticker, StickerOptions )
    register_if_installed( admin_site, PostCard, PostCardOptions )
    register_if_installed( admin_site, PrintedPoster, PrintedPosterOptions )
    register_if_installed( admin_site, ConferencePoster, ConferencePosterOptions )
    register_if_installed( admin_site, Merchandise, MerchandiseOptions )
    register_if_installed( admin_site, Media, MediaOptions )
    register_if_installed( admin_site, Presentation, PresentationOptions )
    register_if_installed( admin_site, PressKit, PressKitOptions )
    register_if_installed( admin_site, OnlineArt, OnlineArtOptions, name='Artist' )
    register_if_installed( admin_site, VideoConferenceBackground, VideoConferenceBackgroundOptions)

    class ArchiveCategoryAdmin(DjangoplicityModelAdmin):
       list_display = ('fullname',)

       change_list_template = 'admin/products/change_list_archivecategory.html'

    admin_site.register(ArchiveCategory, ArchiveCategoryAdmin)

# Register with default admin site
admin_site.register( ExhibitionGroup, ExhibitionGroupAdmin )  # Special
admin_site.register( OnlineArtAuthor, OnlineArtAuthorAdmin )  # Special
register_products_with_admin( admin_site )
