import os

from django.core.files.storage import FileSystemStorage

from djangoplicity.archives.resources import ResourceFile
from djangoplicity.media.consts import MEDIA_CONTENT_SERVERS


def get_zoomable_source(instance, fileclass=ResourceFile):
    """
    Getting tiles folder path from the CDN
    """

    resource_format = 'zoomable'
    localbase = os.path.join(instance.Archive.Meta.root, "{}{}{}".format(resource_format, os.sep, instance.id))
    storage = FileSystemStorage()
    resource = None
    tiles = []

    if storage.exists(localbase):
        resource = fileclass(localbase, storage)

    if resource and hasattr(instance, 'content_server') and instance.content_server and instance.content_server_ready:
        try:
            content_server = MEDIA_CONTENT_SERVERS[instance.content_server]
        except KeyError:
            content_server = None

        if content_server:
            archive_class_name = "{}.{}".format(instance.__module__, instance.__class__.__name__)
            try:
                archive_formats = content_server.formats[archive_class_name]
            except KeyError:
                # No content server defined for this format
                archive_formats = []

            if resource_format in archive_formats:
                tiles_location = os.path.join(
                    storage.location, "{}{}".format(instance.Archive.Meta.root, resource_format)
                )
                url = os.path.join(content_server.get_url(resource, resource_format), instance.Archive.Meta.root)
                storage = FileSystemStorage(base_url=url, location=tiles_location)
                tiles_folders = os.listdir(os.path.join(tiles_location, instance.id))
                for folder in tiles_folders:
                    tiles_path = os.path.join(tiles_location, instance.id, folder)
                    if os.path.isdir(tiles_path):
                        base_path = os.path.join(resource_format, instance.id, folder)
                        tile_resource_base = fileclass(base_path, storage)
                        tiles.append("{}".format(tile_resource_base.absolute_url))

    return tiles

def get_first_subject(instance):
    """

    """

    subjects = instance.subject_name.all()
    if subjects.exists():
        first_subject = subjects.first()
        return first_subject.name
    else:
        return ""
