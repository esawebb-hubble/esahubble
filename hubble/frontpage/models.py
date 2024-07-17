# -*- coding: utf-8 -*-
#
# esahubble.org
# Copyright 2010-2015 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>

from django.db import models


class Highlight(models.Model):
    """
    Ads for frontpage
    """
    name = models.SlugField()
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField()
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Translation:
        fields = ['title', 'description', 'image', 'link']
        excludes = []

    class Meta:
        ordering = ['order']
