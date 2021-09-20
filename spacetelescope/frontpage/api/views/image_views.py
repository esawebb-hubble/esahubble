from django.db.models import Q
from rest_framework import generics, renderers

from djangoplicity.media.models import Image
from djangoplicity.media.options import ImageOptions

from spacetelescope.frontpage.api.serializers import ESASkySerializer


EXCLUDED_IMAGES = [
    'heic0810ae',
    'heic0910h',
    'opo0028a',
    'opo9607a',
    'opo1432b',
    'potw1717a',
    'potw1709a',
    'potw2021a',
    'heic1710d',
    'potw1024a',
    'potw1515a',
    'potw1201a',
    'potw1215a',
    'potw2127a',
    'potw1910a',
    'potw1149a'
]


class ESASkyListView(generics.ListAPIView):
    serializer_class = ESASkySerializer
    renderer_classes = (renderers.JSONRenderer, )

    def get_queryset(self):
        """
        We filter the Image model objects that meet the following conditions:

        - Content Metadata --> Type = Observation
        - Coordinate Metadata --> Quality = Full
        - Published = True

        We exclude the images that have problems with the zoomable feature as
        they will not be rendered correctly on the ESASKY site.
        """

        qs = ImageOptions.Queries.zoomable.queryset(
            Image, ImageOptions, self.request
        )[0].filter(Q(type='Observation') & Q(spatial_quality='Full')).order_by('-priority')

        return qs.exclude(id__in=EXCLUDED_IMAGES)
