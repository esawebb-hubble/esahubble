from __future__ import print_function
#
# -*- coding: utf-8 -*-
#
# eso.org
# Copyright 2011 ESO
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#
# Mantis 12079 helper to find information on hubblesite.org 
#*************************************************************************************************************

from future import standard_library
standard_library.install_aliases()
from builtins import str
from datetime import datetime, tzinfo
import pytz
import re
import socket
import urllib.request, urllib.error, urllib.parse
from djangoplicity.utils.templatetags.djangoplicity_datetime import timezone


def image_info( url ):
    info = {}
    
    (text,redirect) = get_url_content( url )
    
    info['release_date'] = get_cet_release_date( text )
    info['link'] = url
    info['redirected_link'] = redirect
    
    return info

def get_url_content( url ):
    """
    Get content from URL
    """
    try:
        timeout = 60
        socket.setdefaulttimeout(timeout)
        conn = urllib.request.urlopen( url )
        text = conn.read()
        redirect = conn.geturl() 
        conn.close()
    except urllib.error.URLError:
        text = None
        redirect = None
        
    return (text,redirect)

def remove_void(text):
    '''
    removes double whites and linebreaks
    '''
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = ' '.join(text.split())
    return text


long_caption_link_pattern = re.compile( '.*?([0-9]*?)/([0-9]*?)/image/([a-z]{1,2})/?$' )
def stsci_image_id( long_caption_link ):
    """
    creates 2003-28-a out of the long caption link ...eases/2003/28/image/a/
    returns None if failed
    """
    
    try:
        results = long_caption_link_pattern.findall( long_caption_link )[0]
        if results[2] == '':
            return None
        return "STScI-PRC-%s-%s-%s" % ( results[0], results[1], results[2] )
    except IndexError:
        # Handle IndexError: list index out of range
        return None
    except (TypeError, AttributeError):
        # Handle TypeError or AttributeError: invalid arguments or attributes
        return None
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return None

def get_cet_release_date( *args ):
    release_date = get_release_date( *args )
    if release_date: 
        return timezone( release_date, arg='Europe/Berlin' )
    return None

def get_release_date( text ):
    """
    returns the release date in UTC found on the http://hubblesite.org/newsc...../image/ site
    
    <h2 class="date">  <strong>  August 13, 1990</strong> 12:00 AM (EDT) </h2>
    
    1990-June-22 12:00 AM EDT
    1990-June-22 04:00 AM UTC
    """
    release_date = None
    text = remove_void( text )
    pat = re.compile(r'<h2 class="date">.*?<strong>([\S]+)[\s]+([\S]+),[\s]*?([\S]+)[\s]*?</strong>[\s]+([\S]+):([\S]+)[\s]+([\S]+)[\s]+\(?([A-Z]+)\)?[\s]+</h2>') 
    
    # link = release_images(link) # link now ends with .../image/ and points to the release images
    # pat = re.compile(r'<h2 class="date">.*?<strong>([\S]+)[\s]+([\S]+),[\s]*?([\S]+)[\s]*?</strong>[\s]+([\S]+):([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+</h2>') 
    date = None
    try:
        date = pat.findall( text )[0]
        
        B = str( date[0] )  # %B     Locale's full month name.  'December'#
        d = str( date[1] )  # %d     Day of the month as a decimal number [01,31].
        Y = str( date[2] )  # %Y     Year with century as a decimal number.
        I = str( date[3] )  # %I     Hour (12-hour clock) as a decimal number [01,12].
        M = str( date[4] )  # %M     Minute as a decimal number [00,59].
        p = str( date[5] )  # %p     Locale's equivalent of either AM or PM.
        
        datestring = Y + '-' + B + '-' + d + ' ' + I + ':' + M + ' ' + p
        fmt = '%Y-%B-%d %I:%M %p'
        release_date = datetime.strptime( datestring, fmt )

        # take care of timezones
        tz_eastern = pytz.timezone( 'US/Eastern' )
        release_date = tz_eastern.localize( release_date )
    except IndexError:
        # Handle IndexError: list index out of range
        release_date = None
    except (TypeError, ValueError, AttributeError):
        # Handle TypeError, ValueError, AttributeError: invalid arguments or attributes
        release_date = None
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        release_date = None

    return release_date

id_pattern = re.compile('(ann|heic|opo|potw)([0-9]{2})([0-9]{2})([a-zA-Z]{1,2})?')
ext_id_pattern = re.compile('(ann|heic|opo|potw)([0-9]{2})([0-9]{2})([a-zA-Z]{1,2}[0-9]{0,2})?')
def split_id( id, extended=False ):
    """
    Split id into components
    """
    if extended:
        m = ext_id_pattern.match( id )
    else:
        m = id_pattern.match( id )
    if m:
        prefix = m.group(1)
        year = int(m.group(2))
        year = 1900 + year if year > 15 else 2000 + year
        rel = int(m.group(3))
        no = m.group(3)
        
        return ( prefix, year, rel, no )
    return None

def id_vs_releasedate( object ):
    """
    ID/release date sanity check: check if release date year matches id year. 
    """
    if object.release_date:
        res = split_id( object.id )
        if res:
            ( prefix, year, rel, no ) = res
            return year == object.release_date.year
    return None


def long_caption_link_to_thumb( link ):
    results = long_caption_link_pattern.findall( link )[0]
    return "https://imgsrc.hubblesite.org/hu/db/images/hs-%s-%s-%s-thumb.jpg" % ( results[0], results[1], results[2] )
    

def opo_image_list_links( url_images ):
    '''
    list all links and titles for image releases
    example: https://hubblesite.org/newscenter/archive/releases/2005/37/image/:
    ['A Giant Hubble Mosaic of the Crab Nebula', '/newscenter/archive/releases/2005/37/image/a/']
    ['Crab Nebula: a Dead Star Creates Celestial Havoc', '/newscenter/archive/releases/2005/37/image/b/']
    '''
    newlinks = None
    (text, redirect) = get_url_content( url_images )
    text = remove_void(text)
        
    pat = re.compile(r'(<a href="(/newscenter/archive/[^"]+)">)[\s]?<span class="link">(.*?)</span>.*?</a>')  
    links = None
    try:
        links = pat.findall( text )
    except Exception as e:
        print(f"An error occurred: {e}")

    newlinks = []
    for l in links:
        description = l[2]
        link        = l[1]
        if link.find('https://hubblesite.org') == -1:
            link = 'https://hubblesite.org' + link
        newl = [description,link]
        newlinks.append(newl)
    return newlinks

#def release_images_link( linkt ):
#   """
#   returns link to the release images section for a press release link
#   """
#   if link == '''http://hubblesite.org/newscenter/archive/''': link = None
#   
#   if link:
#       if link.find('image') == -1:
#           if link[-1] == '/':
#               link = link + 'image/'
#           else:
#               link = link + '/image/'
#       else:
#           end = link.find('image')
#           link = link[:end] + 'image/'
#   return link
#
#def list_links(url_images):   # [^>]
#   '''
#   list all links and titles for image releases
#   example: http://hubblesite.org/newscenter/archive/releases/2005/37/image/:
#   ['A Giant Hubble Mosaic of the Crab Nebula', '/newscenter/archive/releases/2005/37/image/a/']
#   ['Crab Nebula: a Dead Star Creates Celestial Havoc', '/newscenter/archive/releases/2005/37/image/b/']
#   '''
#   newlinks = None
#   try:
#       site = urllib2.urlopen(url_images)
#       text = site.read()
#       
#       # remove all linebreaks and double whitespace
#       text = remove_void(text)
#        
#       pat = re.compile(r'(<a href="(/newscenter/archive/[^"]+)">)[\s]?<span class="link">(.*?)</span>.*?</a>')  
#       links = None
#       try:
#           links = pat.findall(text)
#       except:
#           pass
#       newlinks = []
#       for l in links:
#           description = l[2]
#           link        = l[1]
#           if link.find('http://hubblesite.org') == -1: 
#               link = 'http://hubblesite.org' + link
#           newl = [description,link]
#           newlinks.append(newl)
#   except:
#       newlinks = None
#   return newlinks
#     


if __name__ == '__main__':
    tests = [r'https://hubblesite.org/newscenter/archive/releases/1990/06/',
             r'https://hubblesite.org/newscenter/archive/releases/1990/06/image/a/',
             'https://hubblesite.org/newscenter/archive/releases/2011/08/']

    for t in tests:
        print(image_url_info(t))
        #print get_release_date(t).strftime('%Y-%B-%d %I:%M %p %Z')
