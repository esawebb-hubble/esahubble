from __future__ import print_function
#
# eso.org
# Copyright 2011 ESO
#
# -*- coding: utf-8 -*-
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#
# Mantis 12079
# 1. Task: Generate list:
# hubblesite id, spacetelescope id, spacetele url, hubblesite url
# 2. Generate HTML page:
# each line: spacetelescope image thumb and hubblesite thumbnail 


#*************************************************************************************************************

from future import standard_library
standard_library.install_aliases()
from builtins import str
from djangoplicity.utils import optionparser
from djangoplicity.media.models import Image

import re
import urllib.request, urllib.error, urllib.parse

import logging, sys
import socket

import datetime

def store_JSON(path_json, dict):
    '''
    stores the data in dict in JSON format
    the JSON data will be presented by the website using dynamic.js
    '''
    f = open(path_json,'w')
    
    ids = list(dict.keys())
    ids.sort()
    f.write('{\n')
    f.write('"items": [\n')
    nel = len(ids)
    count = 0
    for spacetelescope_id in ids:
        count = count + 1
        logger.info(spacetelescope_id)
        element = dict[spacetelescope_id]
        spacetelescope_thumb = element[0]
        spacetelescope_url = element[1]
        hubblesite_id = element[2]
        hubblesite_thumb = element[3]
        hubblesite_huge  = element[4]
        long_caption_link = element[5]
        f.write('{' + '\n')
        f.write('"spacetelescope_id": "'    + spacetelescope_id    + '",' + '\n')
        f.write('"spacetelescope_thumb": "' + spacetelescope_thumb + '",'  + '\n')
        f.write('"spacetelescope_url": "'   + spacetelescope_url   + '",'  + '\n')
        f.write('"hubblesite_id": "'        + hubblesite_id        + '",  \n')
        f.write('"hubblesite_thumb": "'     + hubblesite_thumb     + '",' + '\n')
        f.write('"hubblesite_huge": "'      + hubblesite_huge      + '",' + '\n') 
        f.write('"long_caption_link": "'    + long_caption_link    + '"' + '\n')        
        f.write('}\n')
        if count < nel: f.write(',\n')
    f.write(']\n')
    f.write('}\n')
    f.close()
    print("produced", path_json)
    return
    
def new_id(long_caption_link):
    '''
    creates 2003-28-a out of the long caption link ...eases/2003/28/image/a/
    returns '-' if failed
    '''
    id = ''
    pattern = re.compile('.*?([0-9]*?)/([0-9]*?)/image/([a-z]?)')
    try:
        results = pattern.findall(long_caption_link)[0]
        id  = results[0]+'-'+results[1]
        if results[2] != '': id = id +'-'+results[2]
    except:
        id = '-'
    return id


if __name__ == '__main__':
    logger = logging.getLogger('app.' + __name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stderr))
    logger.propagate = False
    logger.info("get hubblesite ids")
        
    # timeout in seconds
    timeout = 60
    socket.setdefaulttimeout(timeout)

    # opo0328a  => link to thumbnail
    # http://www.spacetelescope.org/static/archives/images/screen/opo0328a.jpg
    # opo0328a  => long_caption  
    # http://hubblesite.org/newscenter/archive/releases/2003/28/image/a/
    # the hubble site id is in a line like this:
    # <h2 class="release-number"><strong>News Release Number:</strong> STScI-2003-28</h2>
    # STScI-2003-28
    
    # link to largest version: 
    # http://imgsrc.hubblesite.org/hu/db/images/hs-2003-28-a-full_jpg.jpg
    
    # link to thumbnail hubblesite:
    # http://imgsrc.hubblesite.org/hu/db/images/hs-2003-28-a-small_web.jpg
    
    # link to spacetelescope thumbnail:
    # http://www.spacetelescope.org/static/archives/images/screen/opo0328a.jpg
    
    
    hubble_pre = r'''http://imgsrc.hubblesite.org/hu/db/images/hs-'''
    hubble_thumb_post = r'''-small_web.jpg'''
    hubble_original_post = r'''-full_jpg.jpg'''
    spacetelescope_site_pre = r'''http://www.spacetelescope.org/images/'''
    spacetelescope_thumb_pre = r'''http://www.spacetelescope.org/static/archives/images/screen/'''
    spacetelescope_thumb_post = r'''.jpg'''
    
    test =  '''<h2 class="release-number"><strong>News Release Number:</strong> STScI-2006-25</h2>'''
    pattern = re.compile('''h2 class="release-number".*?:.*?>\s*(.*?)<.*?h2''')
        
    dict = {} # {spacetelescope_id:[spacetelescope_thumb, hubblesite_id, hubblesite_thumb, hubblesite_huge, long_caption_link]}for the results

    images = Image.objects.all()
    print("spacetelescope id\t hubblesite id\t spacetelescope url\t hubblesite url")
    n_images = str(len(images))
    count = 0
    now = datetime.datetime.now()
    jsonfile = '/Users/lnielsen/Desktop/Hubble/' + now.strftime("%Y-%m-%d") + 'a.js'
    print('store results in ', jsonfile)
    for image in images:
        if image.long_caption_link.find('http://hubblesite.org') == -1: continue
        #if image.id[:3] == 'opo': continue  # all opo images until 01-03-2011 are opo.js and have been manually compared 
        count = count + 1
        #if count > 30: break
        try:
            remote   = urllib.request.urlopen(image.long_caption_link)
        except:
            remote  = 'timeout?'
        #hubblesite = remote.readlines()
        for line in remote:
            if line.find('release-number') > -1:
                break
        try:
            hubble_id = pattern.findall(line)[0].strip()            
        except:
            hubble_id = '?'
        middle = new_id(image.long_caption_link)
        spacetelescope_thumb = spacetelescope_thumb_pre + image.id + spacetelescope_thumb_post
        spacetelescope_url   = spacetelescope_site_pre + image.id + '/'
        if middle != '-':
            hubblesite_thumb = hubble_pre + middle + hubble_thumb_post
            hubblesite_huge = hubble_pre + middle + hubble_original_post
            
            #Check if hubblesite thumb can be found
            thumberror = ''
            try:
                urllib.request.urlopen(hubblesite_thumb) #,data = '', timeout=5
            except urllib.error.URLError as e:
                hubblesite_thumb = 'ERROR' + str(e.code) + ' ' + hubblesite_thumb               
                thumberror = 'Thumb not found (' + str(e.code) + ') at ' + hubblesite_thumb
            
        else:
            hubblesite_thumb = '-'
            hubblesite_huge  = '-'
        

        dict[image.id] = [spacetelescope_thumb, spacetelescope_url, hubble_id, hubblesite_thumb, hubblesite_huge, image.long_caption_link]
        
        print("%s\t%s\t%s\t%s" % (image.id, hubble_id, spacetelescope_url, image.long_caption_link))
        logger.info(str(count)+' / '+n_images + ' ' + image.id + ' ' + hubble_id + ' ' + middle  + ' ' + image.long_caption_link + ' ' + thumberror)
    store_JSON(jsonfile,dict)
           
        
