"""
HEIC vs OPO ids
----------------

Generate Hubblesite OPO ids for all images with a long caption link. Output in CSV format.   
"""
from __future__ import print_function
from spacetelescope.hubblesite.utils import stsci_image_id
from djangoplicity.media.models import Image

for im in Image.objects.all():
    if im.long_caption_link and im.long_caption_link.find( "hubblesite" ) != -1:
        opoid = stsci_image_id( im.long_caption_link )  
        print("%s,%s,%s,%s" % ( im.id, opoid, "https://www.esahubble.org/images/%s/" % im.id, im.long_caption_link ))
