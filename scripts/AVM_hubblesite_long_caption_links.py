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
# Mantis 12079 retrieves long_caption_links for images related to a NASA Press Release 
#*************************************************************************************************************

from future import standard_library
standard_library.install_aliases()
from builtins import str
from djangoplicity.media.models import Image
from djangoplicity.releases.models import Release

import re
import urllib.request, urllib.error, urllib.parse

import logging, sys
import socket
import pprint

import hubblesite as hb

def get_root(link):
    '''
    example: from https://esahubble.org/newsarchive/..... get https://esahubble.org
    '''
    off = len('https://')
    end = off + link[off:].find('/')
    return link[:end]
    
    
def get_ranking(link):
    ''' get's a long_caption_link like ..../2011/23/ and returns 2011*1000 + 23 as a sort of ranking to determine which link was first'''
    s = link.split('/')
    return int(s[-2])*1000 + int(s[-1])

def simplify_text(text):
    '''
    remove "
    remove ,
    remove :
    remove '
    remove linebreaks and double spaces
    make lower
    '''
    text = text.replace('"','')
    text = text.replace(",","")
    text = text.replace(":","")
    text = text.replace("'","")
        
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = ' '.join(text.split())
    
    text = hb.remove_void(text)
    text = text.lower()
    return text

def similar_titles(titles):
    '''
    returns True if the two words in the list titles are similar
    '''
    result = False
    titles[0] = simplify_text(titles[0])
    titles[1] = simplify_text(titles[1])    
      
    if titles[0] == titles[1]: result = True 
    return result
    
def analyse_links(pr_id):
    '''
    in spacetelescope.org press releases are sometimes links to the corresponding NASA Press Release
    return the link that points to hubblesite.org and contains NASA in its description
    '''
    links = None
    long_caption_link = None 
    pat = re.compile(r'<a href="(http://[^"]+)">([^<]+)</a>')
    try:
        related = Release.objects.filter(id__startswith = pr_id)[0]
        links = pat.findall(related.links)
        for link in links: 
            if link[1].find(r'''NASA''') > -1: 
                if link[0].find(r'''hubblesite''') > -1:
                    if not long_caption_link:
                        long_caption_link = link
                        # if there are more than one link to hubblesite with Nasa, take the latest
                    else:
                        if get_ranking(long_caption_link) < get_ranking(link):
                            long_caption_link = link

    except IndexError:
        pass

    return long_caption_link

def check_reachability(url):
    result = True
    
    try:
        urllib.request.urlopen(url) #,data = '', timeout=5
    except urllib.error.URLError as e:
        result = str(e.code) 
    return result


def get_long_caption_link(url, iterator, check_reachability_flag = True):
    '''
    NOT VALID
    This was the first try to get long_caption_links
    by simply using the last letter of .id 
    heic0515c --> hubblesite.org/...../image/c/
    Unfortunately this points very often to a different image
    '''
    long_c = None
    try:
        remote   = urllib.request.urlopen(url)
    except urllib.error.URLError:
        remote  = 'timeout?'
    for line in remote:
        if line.find('<a href=') > -1 and line.find('''/image/''') > -1:
            look_for = '''<a href='''
            start = line.find(look_for) + len(look_for)
            end = line[start:].find('''>''')
            long_c = line[start:end]
            if long_c[0] == '''"''': long_c = long_c[1:]
            if long_c[-1] == '''"''': long_c = long_c[:-1]
            if long_c[0] == '/': long_c = 'https://hubblesite.org' + long_c

            # now replace the last letter in the link with the iterator (heic0515c) /a/ --> /c/
            end = long_c.rfind('/')
            start = long_c[:end].rfind('/')
            long_c = long_c[:start] + '/' + iterator + '/'
            if check_reachability_flag:
                check = check_reachability(long_c)
                if not check: long_c = None
            break
    return long_c

    
    
def analyse(images):
    '''
    counts the number of links per long_caption_link destination
    example:
    hubblesite: 800
    heritage: 55
    '''
    my_dict = {}  #dict containing little dicts ldict
    ldict = {}
    my_list = []
    link_dict = {} # collects the possible roots for long_caption_links
    for image in images:
        if image.long_caption_link.find('http') == -1: continue

        my_list.append(image.id)

        prefix = image.id[:3]
        link   = get_root(image.long_caption_link)
        if link in link_dict:
            link_dict[link] = link_dict[link] + 1
        else: link_dict[link] = 1
        if prefix in my_dict:
            ldict = my_dict[prefix]
            if link in ldict:
                n = ldict[link]
                n = n + 1
                ldict[link] = n
            if link not in ldict:
                ldict[link] = 1
        my_dict[prefix] = ldict
        if prefix not in my_dict:
            ldict = {link: 1}
            my_dict[prefix] = ldict
    my_list.sort()
    print(my_list)
    for d in list(dict):
        print(d, my_dict[d])
    print(link_dict)

def get_related_pr(id):
    temp = ''   
    pattern = re.compile(r'''([a-z]*)(\d*)''')
    temp = pattern.findall(id)
    related = temp[0][0] + temp[0][1]
    iterator = temp[1][0]
    return related, iterator


if __name__ == '__main__':
    # timeout in seconds
    timeout = 60
    socket.setdefaulttimeout(timeout)

    images = Image.objects.all()#filter(image__long_caption_link != '')
    n_images = str(len(images))
    print(n_images, ' image objects')
        
    hcount = 0
    savecount = 0
    psavecount = 0
    pcount = 0

    for image in images:
        link = None
        link_images = None
        nasa_images = None
        result = None
        long_c = None
        press_release_link = None
        link_type = 'not found'
        
        # DEBUG
        #if image.id == 'heic0904i':  #in heic0904i the titles are almost the same appart of the date format
        
        # get only images without a long_caption_link
        if image.long_caption_link.find('http') == -1:
            if image.press_release_link.find('http') == -1:
                # get id of related press release 
                related, iterator = get_related_pr(image.id)
                # find the link to hubblesite.org NASA Press Release
                result =  analyse_links(related)
                if result:
                    press_release_link = result[0]
            else:
                press_release_link = image.press_release_link 
                    # get link to image releases of NASA Press release
            if (press_release_link): 
                link_images = hb.release_images(press_release_link)
                # if no link to release images exist, use original link to NASA Press Release
                if not link_images:
                    long_c = press_release_link
                    link_type = '''using link to NASA's Press Release, no link to NASA's release images'''
                # get links to individual image releases
                if (link_images):
                    nasa_images = hb.list_links(link_images)

                    # if there was no match, use link to Press release release images as long_caption
                    if not nasa_images:
                        long_c = link_images
                        link_type = '''generate link list failed, using link to NASA's release images'''
                    else:
                        # maybe there is just one link?
                        if len(nasa_images) == 1:
                            long_c = nasa_images[0][1]
                            link_type = '''single image in NASA's release images'''
                        else:
                            for ni in nasa_images:
                                if similar_titles([image.title,ni[0]]): 
                                    long_c = ni[1]
                                    link_type = '''titles match with a NASA's release image'''

                            # if there was no match, use link to Press release release images as long_caption
                            if not long_c:
                                long_c = link_images
                                link_type = '''no match, using link to NASA's release images'''
            if long_c and long_c == link_images:
                # often heic###a equals hubblesite.org/.../image/a/, unfortunately not so often with b and even less with c,d,e....
                if iterator == 'a':
                    long_c = link_images + iterator + '/'
                    link_type = '''try link + /a/'''
            
            print(image.id,';\t', long_c,';\t', link_type)
     
            if(press_release_link  and image.press_release_link.find('http') == -1):
                pcount = pcount + 1
                image.press_release_link = press_release_link
                try:
                    image.save()
                    psavecount = psavecount + 1
                except Exception:
                    print(image.id, ': failed to store press_release_link ', press_release_link)
                    
            
            if long_c:
                hcount = hcount + 1
                image.long_caption_link = long_c
                try:
                    image.save()
                    savecount = savecount + 1
                except Exception:
                    print(image.id, ': failed to store long_caption_link ', long_c)
                    
    print(str(hcount), 'long_caption_links found')
    print(str(pcount), 'press_release_link found')
    print('saved ', str(savecount), ' long_caption_links and ', str(psavecount), ' press_release_links.')
 
