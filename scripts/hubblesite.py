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
import re
import urllib.request, urllib.error, urllib.parse 

from datetime import datetime, tzinfo
import pytz
from pytz import timezone

import socket
timeout = 60
socket.setdefaulttimeout(timeout)

def get_redirect(link):
    #returns link from urllib2.urlopen() or if this is not possilbe None is returned
    redirect = ''
    try:
        remote   = urllib.request.urlopen(link) 
        redirect = remote.geturl()
    except:
        redirect = None            
    return redirect

def remove_void(text):
    '''
    removes double whites and linebreaks
    '''
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = ' '.join(text.split())
    return text

def get_release_date(link):
    '''
    returns the release date in UTC found on the http://hubblesite.org/newsc...../image/ site
    
    <h2 class="date">  <strong>  August 13, 1990</strong> 12:00 AM (EDT) </h2>
    
    1990-June-22 12:00 AM EDT
    1990-June-22 04:00 AM UTC
    '''
    
    pat = re.compile(r'<h2 class="date">.*?<strong>([\S]+)[\s]+([\S]+),[\s]*?([\S]+)[\s]*?</strong>[\s]+([\S]+):([\S]+)[\s]+([\S]+)[\s]+\(?([A-Z]+)\)?[\s]+</h2>') 
    
    release_date = None
    link = release_images(link) # link now ends with .../image/ and points to the release images
    
    # read the website
    try:
        site = urllib.request.urlopen(link)
        text = site.read()
        # remove all line breaks and double whitespace
        text = remove_void(text)
              
        #pat = re.compile(r'<h2 class="date">.*?<strong>([\S]+)[\s]+([\S]+),[\s]*?([\S]+)[\s]*?</strong>[\s]+([\S]+):([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+</h2>') 
        date = None
        try:
            date = pat.findall(text)[0]
            #print date
            B = str(date[0])  # %B     Locale's full month name.  'December'#
            d = str(date[1])  # %d     Day of the month as a decimal number [01,31].
            Y = str(date[2])  # %Y     Year with century as a decimal number.
            I = str(date[3])  # %I     Hour (12-hour clock) as a decimal number [01,12].
            M = str(date[4])  # %M     Minute as a decimal number [00,59].
            p = str(date[5])  # %p     Locale's equivalent of either AM or PM.
            Z = str(date[6])  # (%Z)   Time zone name (unfortunately only UTC is working).
            datestring = Y + '-' + B + '-' + d + ' ' + I + ':' + M  + ' ' + p
            
            fmt = '%Y-%B-%d %I:%M %p'
            naive = datetime.strptime(datestring,fmt)
            
            # take care of timezones
            utc = timezone('UTC')
            eastern = timezone('US/Eastern')
            
            tz = utc    
            # for daylight saving 
            is_dts = False
            
            if Z == 'EDT' or Z == 'EST':
                #print 'US/Eastern'
                tz = eastern
                if Z == 'EDT': is_dts = True
            else:
                print('unsupported timezone:', Z)
                print('assuming UTC')
          
            aware = tz.localize(naive, is_dts)
            release_date = tz.normalize(aware)
            release_date = release_date.astimezone(utc)  
        except:
            print("no datetime information found")
            pass
    except:
        print(link, ' could not be read')
        pass
    
    return release_date # in UTC

def release_images(link):
    '''
    returns link to the release images section for a press release link
    '''
    link = get_redirect(link)
    # some special cases that might occure
    if link == '''http://hubblesite.org/newscenter/archive/''': link = None
    
    if link:
        if link.find('image') == -1:
            if link[-1] == '/':
                link = link + 'image/'
            else:
                link = link + '/image/'
        else:
            end = link.find('image')
            link = link[:end] + 'image/'
    return link

def list_links(url_images):   # [^>]
    '''
    list all links and titles for image releases
    example: http://hubblesite.org/newscenter/archive/releases/2005/37/image/:
    ['A Giant Hubble Mosaic of the Crab Nebula', '/newscenter/archive/releases/2005/37/image/a/']
    ['Crab Nebula: a Dead Star Creates Celestial Havoc', '/newscenter/archive/releases/2005/37/image/b/']
    '''
    newlinks = None
    try:
        site = urllib.request.urlopen(url_images)
        text = site.read()
        
        # remove all linebreaks and double whitespace
        text = remove_void(text)
         
        pat = re.compile(r'(<a href="(/newscenter/archive/[^"]+)">)[\s]?<span class="link">(.*?)</span>.*?</a>')  
        links = None
        try:
            links = pat.findall(text)
        except:
            pass
        newlinks = []
        for l in links:
            description = l[2]
            link        = l[1]
            if link.find('http://hubblesite.org') == -1: 
                link = 'http://hubblesite.org' + link
            newl = [description,link]
            newlinks.append(newl)
    except:
        newlinks = None
    return newlinks
      


if __name__ == '__main__':
    #routines to test the helper functions
    

    tests = [r'http://hubblesite.org/newscenter/archive/releases/1990/06/', 
             r'http://hubblesite.org/newscenter/archive/releases/1990/06/image/a/']

    for t in tests:
        print(t)
        print(get_release_date(t).strftime('%Y-%B-%d %I:%M %p %Z'))   
          
    exit()
    
    print("list_links:")
    release = r'''http://hubblesite.org/newscenter/archive/releases/2005/37'''
   # release = r'''http://hubblesite.org/newscenter/archive/releases/2008/16/image/ce/'''
    images = release_images(release)
    

    links = list_links(images)

    print(images)
    c = 0
    if links: 
        for link in links: 
            c = c + 1
            print(c, '   ', link)
