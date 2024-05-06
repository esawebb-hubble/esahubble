from __future__ import print_function
#
# -*- coding: utf-8 -*-#
# eso.org
# Copyright 2011 ESO
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#
# Mantis 12175: Fix release dates for images and videos
#
#
# Find wrong release_dates:
# 1) Check id with release_date - e.g. opo0214a with release date in 2010 must be wrong
#    should be opoYYNNx NN is a cont. number?
# 2) Release dates with 2011-03-03 18:00-18:44 are wrong
#
# Don't bother about images connected to announcements, releases and potws.
#
# For images with long_caption_link or press_release_link follow the link and extract the date. 
#
#
#*************************************************************************************************************


from future import standard_library
standard_library.install_aliases()
from djangoplicity.utils import optionparser
from djangoplicity.media.models import Image
from djangoplicity.media.models import Video

import re
import urllib.request, urllib.error, urllib.parse

import logging, sys
import socket

from datetime import datetime
import pytz

import hubblesite

def change_datetime(obj):
    '''
    follows the long_caption_link or the press_release_link to get the correct date
    '''
    # get link to image or press release
    link = None
    success = False
    if obj.long_caption_link.find('http') > -1:
        link = obj.long_caption_link
    elif obj.press_release_link.find('http') > -1:
        link = obj.press_release_link
    
    # follow link and get new date
    if link:
        release_date = hubblesite.get_release_date(link)
        if release_date:
            try:
                release_date = release_date.astimezone( pytz.timezone( 'Europe/Berlin' ) )
                release_date = datetime.replace(release_date, tzinfo=None)
                obj.release_date = release_date
                obj.save()
                success = True
            except AttributeError as e:
                print(obj.id, 'AttributeError:', e)
            except ValueError as e:
                print(obj.id, 'ValueError:', e)
            except Exception as e:
                print(obj.id, 'Save failed:', e)
    return success


def process_objects(objs):
    '''
    find the objects that need a correction of the release_date
    '''
    pat = re.compile('[a-zA-Z]+(\d{2})\S+')
    
    count = 0
    finddate1 = datetime.strptime('2011-03-03 18:00:00','%Y-%m-%d %H:%M:%S')
    finddate2 = datetime.strptime('2011-03-03 19:00:00','%Y-%m-%d %H:%M:%S')
    for obj in objs:

        YY = None
        dt = obj.release_date
        if (dt):
            # process all objects with 2011-03-03 18:00:00 - 19:00:00
            if dt >= finddate1 and dt <= finddate2:
                if change_datetime(obj): count = count + 1
                print(obj.id, 'old: ', dt, '\t new: ', obj.release_date ,'\t\t reason: 20110303')
            # process all objects where opoYY YY does not match the year of the release_date 
            else:
                #only care about opo... and heic...
                if obj.id.find('opo') == -1 and obj.id.find('heic') == -1: continue
                YY = pat.findall(obj.id)
                if len(YY) > 0:
                    YY = YY[0]
                    if YY != dt.strftime('%y'):
                        if change_datetime(obj): count = count + 1
                        print(obj.id, 'old: ', dt, '\t new: ', obj.release_date ,'\t\t reason: ', YY,' != ', dt.strftime('%y'))
        else:
            pass
    return count


if __name__ == '__main__':
    logger = logging.getLogger('app.' + __name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stderr))
    logger.propagate = False
    logger.info("Fix release dates for images and videos")
    
    
    
    # timeout in seconds
    timeout = 60
    socket.setdefaulttimeout(timeout)


    test =  '''<h2 class="release-number"><strong>News Release Number:</strong> STScI-2006-25</h2>'''
    pattern = re.compile('''h2 class="release-number".*?:.*?>\s*(.*?)<.*?h2''')    
    
    print('videos') 
    print(process_objects(Video.objects.all()), ' videos have a new release_date')
    print('images')
    print(process_objects(Image.objects.all()), ' images have a new release_date')


