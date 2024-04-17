from __future__ import print_function
#
# eso.org
# Copyright 2010 ESO
#
# -*- coding: utf-8 -*-
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#

from djangoplicity.utils import optionparser
#get mapping
from djangoplicity.releases.models import Release

import re

releases = Release.objects.all()

update_db = False

def doit(text, id):

    pattern = r'''/news/science_paper'''
    repl    = r'''/static/archives/releases/science_papers'''
    
    (new_text, n_repls) = re.subn(pattern, repl, text)
    
    if n_repls > 0:
        print(n_repls, 'replacement(s) in', id, '<p>') 
        print('old >>>>>>>>> <p>')
        print(text)
        print('new >>>>>>>>> <p>')
        print(new_text)
        print('--------------------------- <p> ')
    return new_text


#*************************************************************************************************************
if __name__ == '__main__':
    args = optionparser.get_options( [('c','update_db','commit changes to the database?',False) ])    
    update_db   = args['update_db']
    print(update_db)
    if update_db == 'True': 
        update_db = True
    else:
        update_db = False
        
    print("In Releases.links:")
    if update_db: print("updating the database entries...")
    if not update_db: print("use option -c True, for committing the changes to the database.")
    for obj in releases:
        try:
            links = obj.links.encode('utf-8')
        except:
            links = strip_tags(obj.links).encode('utf-8')
            print("PROBLEM with " + links) 
        obj_id = obj.id.encode('utf-8')
        new_text = doit(links, obj_id)
        if update_db:
            try:
                obj.links = new_text
                obj.save()
            except:
                print('Problem updating database for ' + id)
