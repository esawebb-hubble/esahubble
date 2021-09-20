from django.db.models import Q
from rest_framework import generics, renderers

from djangoplicity.media.models import Image
from djangoplicity.media.options import ImageOptions

from spacetelescope.frontpage.api.serializers import ESASkySerializer


EXCLUDED_IMAGES = [
    'potw1717a',
    'potw1709a',
    'potw2021a',
    'opo1432b',
    'heic1710d',
    'potw1024a',
    'potw1515a',
    'potw1201a',
    'potw1215a',
    'potw2127a',
    'potw1910a',
    'potw1149a',
    'potw1145a',
    'heic0810ae',
    'heic1118a',
    'heic0910h'
]


class ESASkyListView(generics.ListAPIView):
    serializer_class = ESASkySerializer
    renderer_classes = (renderers.JSONRenderer, )

    def get_queryset(self):
        qs = ImageOptions.Queries.zoomable.queryset(
            Image, ImageOptions, self.request
        )[0].filter(Q(type='Observation') & Q(spatial_quality='Full')).order_by('-priority')

        # TODO: Remove undesired images
        return qs
