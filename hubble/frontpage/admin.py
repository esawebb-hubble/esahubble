# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010-2015 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>

from django.contrib import admin

from spacetelescope.frontpage.models import Highlight


class HighlightAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'image', 'link', 'order', 'published']
    list_editable = ['title', 'image', 'link', 'order', 'published']
    list_filter = ['published']
    search_fields = ['name', 'title', 'description', 'image', 'link']
    ordering = [ 'order']
    fieldsets = (
        (None, {'fields': ('name', 'order', 'published') }),
        ('Content', {'fields': ('title', 'image', 'link', 'description',), }),
    )


def register_with_admin(admin_site):
    admin_site.register( Highlight, HighlightAdmin )
