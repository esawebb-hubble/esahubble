#
# -*- coding: utf-8 -*-
#
# eso.org
# Copyright 2011 ESO
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#   script to test and apply functions in hubblesite/avm.py
#   
#*************************************************************************************************************
from __future__ import print_function
from builtins import chr
from spacetelescope.hubblesite import avm
import os, sys

def prepare4unicode():
    import sys, codecs, locale
    # this allows stdout > into a file
    sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
    # little unicode test
    star = chr(9734)
    print(star)

if __name__ == '__main__':
    # for testing
    prepare4unicode()
    
    script_path = os.path.dirname(sys.argv[0])
    json_file = os.path.join(script_path, 'stpr_search.json')
    
    jsonmapper = avm.jsonmapper()
    data = avm.load_json(json_file)
    print(len(data), "entries in original data")
    data = avm.remove_duplicates(data)
    print(len(data), "after remove_duplicates")
    for dataset in data:
        print("______________________________________________________________________________")
        jsonmapper.jsondict = dataset
        avmdict = jsonmapper.avmdict()
        for key in list(avmdict.keys()):
            jsonkey = jsonmapper.mapping[key]['fieldname']
            if jsonkey in list(dataset.keys()): jsondata = dataset[jsonkey]
            print("%-30s: %-90s JSON: %s" % (key, avmdict[key], jsondata))
