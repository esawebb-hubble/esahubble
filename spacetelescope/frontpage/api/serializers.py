from rest_framework import serializers

from djangoplicity.archives.utils import get_instance_d2d_resource
from djangoplicity.media.models import Image
from djangoplicity.utils.templatetags.djangoplicity_text_utils import remove_html_tags
from djangoplicity.utils.datetimes import timezone

from spacetelescope.frontpage.api.utils import get_tiles_for_instance


class ESASkySerializer(serializers.ModelSerializer):
    """
    Custom Image serializer for the ESASky JSONFeed
    """

    credit = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    release_date = serializers.SerializerMethodField()
    tiles = serializers.SerializerMethodField()
    large = serializers.SerializerMethodField()
    coordinate_metadata = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = (
            'id', 'title', 'description', 'priority', 'release_date', 'last_modified',
            'coordinate_metadata', 'credit', 'tiles', 'large'
        )

    def get_tiles(self, obj):
        return get_tiles_for_instance(obj)

    def get_large(self, obj):
        large_dict = get_instance_d2d_resource(obj, 'large', 'Large', 'Image')
        return large_dict.get('URL', None)

    def get_credit(self, obj):
        return remove_html_tags(obj.credit)

    def get_description(self, obj):
        return remove_html_tags(obj.description)

    def get_release_date(self, obj):
        return timezone(obj.release_date, 'UTC')

    def get_coordinate_metadata(self, obj):

        def get_float(value):
            try:
                return float(value)
            except:  # pylint: disable=bare-except
                return None

        def s_to_f(array):
            '''
            Convert an array of strings to an array of float
            Invalid values are returned as None
            '''
            return [get_float(x) for x in array]

        return {
            "CoordinateFrame": obj.spatial_coordinate_frame,
            "Equinox": obj.spatial_equinox,
            "ReferenceValue": s_to_f(obj.get_spatial_reference_value()),
            "ReferenceDimension": s_to_f(obj.get_spatial_reference_dimension()),
            "ReferencePixel": s_to_f(obj.get_spatial_reference_pixel()),
            "Scale": s_to_f(obj.get_spatial_scale()),
            "Rotation": get_float(obj.spatial_rotation),
            "CoordinateSystemProjection": obj.spatial_coordsystem_projection,
            "Quality": obj.spatial_quality
        }
