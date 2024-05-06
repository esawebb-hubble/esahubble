from __future__ import print_function
#
# -*- coding: utf-8 -*-
#
# eso.org
# Copyright 2011 ESO
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#
# Mantis ESO 3065, now for spacetelescope
#
# Tag all images with subject category and remove temporary taxonomy items.
# 2011 Apr 18
#*************************************************************************************************************

from builtins import chr
from builtins import str
from builtins import range
import pprint

from djangoplicity.media.models import Image
from djangoplicity.media.models import Video
from djangoplicity.metadata.models import TaxonomyHierarchy
from djangoplicity.metadata.models import SubjectName

import sys, codecs, locale

def analyse_taxonomy(generate_code = False ):
    '''
    see which X.tags are used
    and generate sceleton for the code
    '''
    # 1 build dictionary
    x_tags = {}


    for xth in TaxonomyHierarchy.objects.filter(top_level = 'X'):
        x_tags[xth.avm_code()] = [xth.name,0]
        
    for img in Image.objects.all():#.filter(pk = 'eso9212d'):
        x_tag  = False
        for sc in  img.subject_category.all():
            if sc.top_level == 'X': x_tag = True
        if x_tag:
            [name, number] = x_tags[sc.avm_code()]
            x_tags[sc.avm_code()] = [name, number + 1]
      
    keys = list(x_tags.keys())
    keys.sort()
    if generate_code:
        for key in keys:
            print("    elif tag == '%s':       # '%s' %d" % (key, x_tags[key][0], x_tags[key][1]))
            print("        pass")
        print('-----------------------')
    pprint.pprint(x_tags)

def scan_tags(image, name):
    found = None
    for sc in  image.subject_category.exclude(top_level = 'X'):
        if sc.name.upper().find(name.upper()) > -1: found = sc   
    return found

def get_toplevel(image):
    toplevel = None
    for sc in  image.subject_category.exclude(top_level = 'X'):
        toplevel = sc.top_level   
        # assuming that all existing toplevels are the same, if not, the last tag determines top_level   
    return toplevel


def print_tags(image):
    found = False
    scs = image.subject_category.exclude(top_level = 'X')
    if len(scs) > 0: print(image.id, end=' ')
    for sc in  scs:
        print(sc.name, end=' ')
    print()
    return found

def scan_subjectnames(image, name):
    found = False
    for sn in  image.subject_name.all():
        if sn.name.find(name) > -1: found = True   
    return found

def add_subjectname(image, subject_name):
    """
    if there is not already a subject_name containing name
    a new subject_name name is added
    
    returns True, if a new subject_name was added
    """
    added = False
    if not scan_subjectnames(image,subject_name): 
        print("%-45s; %-9s; %s; subject_name ;%s; added;\t title: %s" % (image.id, sc.avm_code(), sc.name, subject_name, image.title))                                             
        new_name = SubjectName.objects.get(name = subject_name)
        image.subject_name.add(new_name)
        added = True
    else: print("%-45s; %-9s; %s; subject_name ;%s; already exists;\t title: %s" % (image.id, sc.avm_code(), sc.name, subject_name, image.title))                                                     
    return added

def add_avmtag(image, name, code):
    """
    if there is not already a AVM-tag containing name
    a new tag with code is added
    and the old x-tag will be removed 
    
    returns True, if a new tag was added
    """
    added = False
    existing_tag = scan_tags(image, name)
    if not existing_tag:
        codes = code.split('.')
        level = [None,None,None,None,None,None]
        level[0] = codes[0]
        for i in range(1,len(codes),1):
            level[i] = int(codes[i])       
        new_tag = TaxonomyHierarchy.objects.get( top_level = level[0], 
                                                 level1 = level[1], 
                                                 level2 = level[2], 
                                                 level3 = level[3], 
                                                 level4 = level[4], 
                                                 level5 = level[5])
        print("%-45s; %-9s; %s; replace with;%s; %s;\t title: %s" % (image.id, sc.avm_code(), sc.name, new_tag.avm_code(), new_tag.name, image.title))                                             
        image.subject_category.add(new_tag)
        added = True 
    else: print("%-45s; %-9s; %s; already existing tag;%s; %s;\t title: %s" % (image.id, sc.avm_code(), sc.name, existing_tag.avm_code(), existing_tag.name, image.title))                                             
    return added

def treat_x(sc, image, remove = True): 
    tag = sc.avm_code()
    changed = False
    if tag == 'X.101.10':   # 'Extrasolar Planets Videos' 1  
        # replace with B.3.7.1. Planetary System       
        changed = add_avmtag(image,  'Planetary System','B.3.7.1')    
        image.subject_category.remove(sc)
        
    elif tag == 'X.101.11':        # 'JWST Images/Videos' 24
        # add subject_name JWST
        changed = add_subjectname(image,'JWST')
        # set image.type = 'Artwork'
        print("%-45s; %-9s; %s; set image.type = 'Artwork'" % (image.id, sc.avm_code(), sc.name))
        image.type = 'Artwork'
        image.subject_category.remove(sc)
        changed = True

    elif tag == 'X.101.12':        # 'Spacecraft Images/Videos' 20
        # replace with 8.2 Spacecraft 
        changed = add_avmtag(image,  'Spacecraft','E.8.2')    
        image.subject_category.remove(sc)

    elif tag == 'X.101.13':        # 'Miscellaneous  Images/Videos' 165
        # remove tag
        print("%-45s; %-9s; %s; only removing tag" % (image.id, sc.avm_code(), sc.name))
        image.subject_category.remove(sc)
        changed = True     
        
    elif tag == 'X.101.21':        # 'Illustration Images' 237
        # set type to artwork and remove tag
        print("%-45s; %-9s; %s; set image.type = 'Artwork'" % (image.id, sc.avm_code(), sc.name))
        image.type = 'Artwork'
        image.subject_category.remove(sc)
        changed = True
        
    elif tag == 'X.101.22':        # 'Mission' 132
        # replace with 8.2 Spacecraft
        changed = add_avmtag(image,  'Spacecraft','E.8.2')
        image.subject_category.remove(sc)
        
    elif tag == 'X.101.3':        # 'Solar System Images/Videos' 577
        # A
        changed = add_avmtag(image,  'Solar System','A')
        image.subject_category.remove(sc)       

    elif tag == 'X.101.4':        # 'Stars Images/Videos' 206
        # make B.3, change to C afterwards if necessary
        changed = add_avmtag(image,  'Star','B.4')
        image.subject_category.remove(sc)
        
    elif tag == 'X.101.5':        # 'Star Clusters Images/Videos' 100
        # B.3.6.4. 
        changed = add_avmtag(image,  'Cluster','B.3.6.4')
        image.subject_category.remove(sc)
    
    elif tag == 'X.101.6':        # 'Nebulae Images/Videos' 330
        # B.4, change to C afterwards if necessary
        changed = add_avmtag(image,  'Nebula','B.4')           
        image.subject_category.remove(sc)
        
    elif tag == 'X.101.7':        # 'Galaxies Images/Videos' 474
        ds = ['opo9228b',''] # Cosmology
        cs = [] # local universe
        bs = [] # Milky Way
        if image.id in bs:
            image_type = 'B'
        elif image.id in cs:
            image_type = 'C'
        elif image.id in ds:
            image_type = 'D'
        
        # maybe there is a tag for Milky Way => B
        elif scan_tags(image, 'ilky'):
            image_type = 'B'
        # or maybe a tag for Cosmology => D
        elif scan_tags(image, 'Cosmology'): 
            image_type = 'D'
        else: 
            image_type = 'C'
    
        changed = add_avmtag(image, 'Galax', image_type + '.5')
        image.subject_category.remove(sc)
        
    elif tag == 'X.101.8':        # 'Quasars/AGN/Black Hole Images/Videos' 85
        # 1. determine top_level
        if 0.1 < image.distance < 11:
            image_type = 'D'
        # maybe there is a tag for Cosmology => D
        elif scan_tags(image, 'Cosmology'): 
            image_type = 'D'
        # check if there is a tag for Milky Way => B
        elif scan_tags(image, 'ilky'):
            image_type = 'B'
        else: image_type = ''

        # determine sub_levels AGN / BH / Quasar?           
        title = str(image.title).upper()
        if title.find('MILKY WAY') > -1 and image_type == '':
            changed = add_avmtag(image, 'Black Hole', 'B' + '.5.4.6')
        if title.find('BLACK HOLE') > -1:
            if image_type == '': image_type = 'C'
            changed = add_avmtag(image, 'Black Hole', image_type + '.5.4.6')
        if title.find('QUASAR') > -1:
            if image_type == '': image_type = 'D'
            changed = add_avmtag(image, 'Quasar', image_type + '.5.3.2.1')
        if title.find('ACTIVE') > -1:
            if image_type == '': image_type = 'C'
            changed = add_avmtag(image, 'AGN', image_type + '.5.3.2')
            
        if changed: image.subject_category.remove(sc)
        else: print("%-45s; %-9s; %s; BH or AGN? ; ; ;\t title: %s" % (image.id, sc.avm_code(), sc.name,  image.title))                                             
        
            
    elif tag == 'X.101.9':        # 'Cosmology Images/Videos' 241
        # D
        changed = add_avmtag(image,  'Cosmology','D')
        image.subject_category.remove(sc)
        
        
    ret_val = None
    if changed: ret_val = image     
    return ret_val


if __name__ == '__main__':

    # this allows stdout > into a file
    sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
    
    #little unicode test
    star = chr(9734)
    print(star)
    
    changed_images = set()

    count = 0
    #  First process the easier tags, then in 2. round the newly created tags can be used to check the top_level       
    print('Images 1. round')
    for img in Image.objects.all():
        n_tags = len(img.subject_category.all())
        for sc in  img.subject_category.all():
            if sc.top_level == 'X': 
                if sc.avm_code() == 'X.101.8' or sc.avm_code() == 'X.101.7': continue  
                count = count + 1
                changed_images.add(treat_x(sc, img))

    print("apply the changes")
    for img in changed_images:
        if img:
            try: 
                img.save()
            except Exception:
                print("save failed with %s in %s" % (sc.name, img.id))

    print('Images 2. round')
    for img in Image.objects.all():
        n_tags = len(img.subject_category.all())
        for sc in  img.subject_category.all():
            if sc.top_level == 'X': 
                if sc.avm_code() == 'X.101.8' or sc.avm_code() == 'X.101.7': 
                    count = count + 1
                    changed_images.add(treat_x(sc, img))

    print("apply the changes")
    for img in changed_images:
        if img:
            try: 
                img.save()
            except Exception:
                print("save failed with %s in %s" % (sc.name, img.id))
            
    print('treated', count, 'tags')
    
    
    
    
    
    
# 'X.101.1': [u'Hubble Images Videos', 0],
# 'X.101.10': [u'Extrasolar Planets Videos', 1],
# O.K. 'X.101.11': [u'JWST Images/Videos', 24],
# O.K. 'X.101.12': [u'Spacecraft Images/Videos', 20],
# ? remove tag ? 'X.101.13': [u'Hubble DVD Videos', 165],
# O.K. 'X.101.21': [u'Illustration Images', 228],
# 'X.101.22': [u'Mission', 124],
# O.K. 'X.101.3': [u'Solar System Images/Videos', 518],
# O.K. 'X.101.4': [u'Stars Images/Videos', 166],
# O.K. 'X.101.5': [u'Star Clusters Images/Videos', 84],
# O.K. 'X.101.6': [u'Nebulae Images/Videos', 249],
# O.K. 'X.101.7': [u'Galaxies Images/Videos', 379],
# if there is no Milky Way tag (B) use C for BH and AGN and D for Quasar 'X.101.8': [u'Quasars/AGN/Black Hole Images/Videos', 72],
# O.K.'X.101.9': [u'Cosmology Images/Videos', 205]


