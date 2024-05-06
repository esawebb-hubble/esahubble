#
# -*- coding: utf-8 -*-
#
# eso.org
# Copyright 2011 ESO
# Authors:
#  Lars Holm Nielsen <lnielsen@eso.org>
#  Dirk Neumayer <dirk.neumayer@gmail.com>
#
#  access avm metadata as dict, source is a json file from
#  http://archdev.stsci.edu/stpr/search.php 
#
#  to get the json file:
#  for all fields goto Output Columns and push button add all, 
#  choose the maximum value in Maximum Records and
#  in Output Format choose 'File: JSON Format'
#  then press search
# 
#***********************************************************************************************************************


from builtins import str
from builtins import object
from datetime import datetime
import pytz
from djangoplicity.utils.templatetags.djangoplicity_datetime import timezone

import re
import logging

logger = logging.getLogger(__name__)

import json

def load_json(json_file):
    '''
    loads the content of the given JSON file and returns it.
    '''
    json_data = None
    try:
        fp = open(json_file,'r')
        json_data = json.load(fp)
        fp.close()
    except IOError as xxx_todo_changeme:
        (errno, strerror) = xxx_todo_changeme.args
        logger.error("I/O error(%s): %s" % (errno, strerror))
        logger.error("Problem opening file %s, returning None" % json_file )   
    return json_data

def remove_duplicates(data):
    '''
    remove duplicates, prefere jpeg entries
    in the jsondata are often more than one entries for each ID, one with tiff, one with jpeg
    take all the jpeg versions and add all other image IDs that do not have a jpeg version
    '''
    image_list = []
    list_ids = []
    other = []
    for dataset in data:
        if dataset['Image Format'] == u'image/jpeg': 
            image_list.append(dataset)
            list_ids.append(dataset['Identifier'])
        else: other.append(dataset)
    for o in other:
        if o['Identifier'] not in list_ids:
            image_list.append(o)
            list_ids.append(o['Identifier'])          
    return image_list

class jsonmapper(object):
    '''
    this class provides the function avmdict() that converts the json dict in jsonmapper.jsondict into an AVM dict
    the main logic is in the mapping dictionary. It contains for each AVM field the corresponding JSON fieldname 
    and function if string processing is necessary
    '''
    # TODO: replace "-" with None in lists of strings?
    # TODO: sometimes AVMFormat should be string, but in json it is a csv list of strings like in Credit, 
    #       return a list of strings instead?
    # in future, use this in a Deserializer function  
    def __init__(self, dataset = {}):
        self.jsondict = dataset
        self.mapping = {
    # 3.1 Creator Metadata
     'Creator':                       { 'fieldname': 'Creator'},
     'CreatorURL':                    { 'fieldname': 'CreatorURL'},
     'Contact.Name':                  { 'fieldname': 'Contact Name',   'func': self.semicolonstrings2stringlist},
     'Contact.Email':                 { 'fieldname': 'Contact Email',  'func': self.semicolonstrings2stringlist},
     'Contact.Telephone':             { 'fieldname': 'Contact Phone',  'func': self.semicolonstrings2stringlist},
     'Contact.Address':               { 'fieldname': 'Contact Address'},
     'Contact.City':                  { 'fieldname': 'Contact City'},
     'Contact.StateProvince':         { 'fieldname': 'Contact State'},
     'Contact.PostalCode':            { 'fieldname': 'Contact code'},   # TODO: ['Contact code','Contact Code'] in case they fix the typo
     'Contact.Country':               { 'fieldname': 'Contact Country'},
     'Rights':                        { 'fieldname': 'Usage Terms'},
    # 3.2 Content Metadata         
     'Title':                         { 'fieldname': 'Title'},
     'Headline':                      { 'fieldname': 'Headline'},
     'Description':                   { 'fieldname': 'Description'},
     'Subject.Category':              { 'fieldname': 'Subject Category', 'func': self.subjectcategories},                           
     'Subject.Name':                  { 'fieldname': 'Subject', 'func': self.semicolonstrings2stringlist},              
     'Distance':                      { 'fieldname': 'Distance', 'func': self.listdistances},
     'Distance.Notes':                { 'fieldname': 'Distance Notes'},
     'ReferenceURL':                  { 'fieldname': 'Press Release Images' },
     'Credit':                        { 'fieldname': 'Credit'},
     'Date':                          { 'fieldname': 'Date Created', 'func': self.datetimestring2datetime},
     'ID':                            { 'fieldname': 'Identifier'},
     'Type':                          { 'fieldname': 'Image Type'},
     'Image.ProductQuality':          { 'fieldname': 'Image Product Quality'},
    # 3.3 Observation Metadata         
     'Facility':                      { 'fieldname': 'Facility',  'func': self.semicolonstrings2stringlist},
     'Instrument':                    { 'fieldname': 'Instrument','func': self.semicolonstrings2stringlist},
     'Spectral.ColorAssignment':      { 'fieldname': 'Color Assignments','func': self.semicolonstrings2stringlist},
     'Spectral.Band':                 { 'fieldname': 'Spectral Band','func': self.semicolonstrings2stringlist},
     'Spectral.Bandpass':             { 'fieldname': 'BandPass ID',  'func': self.semicolonstrings2stringlist},
     'Spectral.CentralWavelength':    { 'fieldname': 'BandPass RefValue','func': self.semicolonstrings2stringlist},
     'Spectral.Notes':                { 'fieldname': 'Spectral Notes', 'func': self.replace_html},
     'Temporal.StartTime':            { 'fieldname': 'Exposure Start Times', 'func': self.starttimes2datetimelist}, 
     'Temporal.IntegrationTime':      { 'fieldname': 'Exposure Times','func': self.semicolonstrings2stringlist},
     'DatasetID':                     { 'fieldname': 'Dataset IDs',  'func': self.strings2stringlist},
    # 3.4 Coordinate Metadata
     'Spatial.CoordinateFrame':       { 'fieldname': 'Ref Frame', 'func':  self.string_2_coordinate_framecv},
     'Spatial.Equinox':               { 'fieldname': 'Equinox'},
      # TODO: Decide which json-fields to use
     'Spatial.ReferenceValue':        { 'fieldname': 'Spatial Reference Value',  'func': self.semicolonstrings2stringlist}, 
     # or 'Spatial.ReferenceValue':{ 'fieldname': ['Dec (J2000)','RA (J2000)']},   # Spatial Reference Values seems to match better with the AVM guide
     'Spatial.ReferenceDimension':    { 'fieldname': 'Spatial Reference Dimension',  'func': self.strings2stringlist},
     'Spatial.ReferencePixel':        { 'fieldname': 'Spatial Reference Pixel',  'func': self.strings2stringlist},
     'Spatial.Scale':                 { 'fieldname': 'Image Scale', 'func': self.strings2stringlist},    
     'Spatial.Rotation':              { 'fieldname': 'Spatial Rotation'},
     'Spatial.CoordsystemProjection': { 'fieldname': 'Coord Proj', 'func': self.string_2_coord_projections_cv},
     'Spatial.Quality':               { 'fieldname': 'Spatial Quality', 'func': self.string_2_spatial_quality_cv},
     'Spatial.Notes':                 { 'fieldname': 'Spatial Notes', 'func':   self.replace_html},
     'Spatial.FITSHeader':            { 'fieldname': 'SpatialFITSHeader'},
     'Spatial.CDMatrix':              { 'fieldname': 'CD matrix',  'func': self.strings2stringlist},                 # AVM 1.1 (depreciated) 
    # 3.5 Publixher Metadata
     'Publisher':                     { 'fieldname': 'Publisher'},
     'PublisherID':                   { 'fieldname': 'Publisher ID'},
     'ResourceID':                    { 'fieldname': 'Resource ID'},   
     'ResourceURL':                   { 'fieldname': 'URL'},    
     'RelatedResources':              { 'fieldname': 'Related Resouuces',  'func': self.semicolonstrings2stringlist}, # ['Related Resources','Related Resouuces'] in case they fix the typo
     'MetadataDate':                  { 'fieldname': 'Metadata Date', 'func': self.datetimestring2datetime},
     'MetadataVersion':               { 'fieldname': 'Meta Version'},
    # 3.6 File Metadata
     'File.Type':                     { 'fieldname': 'Image Format',   'func': self.string_2_file_type_cv},
     'File.Dimension':                { 'fieldname': 'Image Length', 'func': lambda fieldname: [ self.jsondict['Image Length'], self.jsondict['Image Width'] ]},         
     'File.Size':                     { 'fieldname': 'File Size', 'func': self.strings2stringlist},        
     'File.BitDepth':                 { 'fieldname': 'Bit Depth'}, 
    # X in AVM 1.1 not defined      
     'X.IngestDate':                  { 'fieldname': 'Ingest Date', 'func': self.datetimestring2datetime},
     'X.ProposalID':                  { 'fieldname': 'Proposal ID', 'func': self.strings2stringlist},
     'X.ImageCount':                  { 'fieldname': 'Image Count'},      
     'X.Source':                      { 'fieldname': 'Source'}, 
     'X.Dec':                         { 'fieldname': 'Dec (J2000)'},
     'X.RA':                          { 'fieldname': 'RA (J2000)'},
}
        
    def listdistances(self, strings):
        lightyear = None
        redshift  = None
        texts = self.strings2stringlist(strings)
        for text in texts:
            # is it a redshift?
            if text.find('z=') > -1: redshift = text.split('=')[1]
            else: lightyear = text
        return [lightyear, redshift]

    def strings2stringlist(self, strings):
        ''' converts comma (;,) separated values to a list of strings
        '''
        string_list = None
        strings = strings.replace(',',';') 
        string_list = self.semicolonstrings2stringlist(strings)
        return string_list
    
    def semicolonstrings2stringlist(self, strings):
        ''' converts semicolon (;) separated values to a list of strings
        '''
        string_list = None
        if strings and strings.find(';'): string_list = [s.strip() for s in strings.split(';')]
        return string_list
    
    def replace_html(self, text):
        '''
        text from stpr sometimes contains &gt; instead of >
        add here other replacements if necessary
        '''
        return text.replace(u'&gt;', u'>')
    
    def subjectcategories(self, strings):
        ''' skip X., return list with category objects
        '''
        strings = self.replace_html(strings)
        category_list = self.strings2stringlist(strings)
        for value in category_list:
            if value[0] == 'X': category_list.remove(value)
        return category_list
    
    def starttimes2datetimelist( self, starttimes ):
        dates = []
        star_times_list = self.strings2stringlist( starttimes )
        for value in star_times_list:
            try:
                date = self.datestring2datetime( value )
            except ValueError:    # "-", '-', -, other format?
                date = None
                if len(value) > 4:    # other format?
                    logger.error("ValueError in starttimes2datetimelist trying to convert %s into a datetime object" % value)
            dates.append( date )        
        return dates
    
    def cet_datetime( self, date ):
        '''
        return date in timezone Europe/Berlin
        '''
        return timezone( date, arg='Europe/Berlin' )
    
    def datestring2datetime(self, datestring):
        """
        returns the date in UTC
        datestring has format like 2011-03-23
        """
        fmt = '%Y-%m-%d'
        date = datetime.strptime( datestring, fmt )
        # assuming ES/Eastern for hubblesite dates
        tz_eastern = pytz.timezone( 'US/Eastern' )
        date = tz_eastern.localize( date )
        #return datetime in timezone Europe/Berlin
        date = self.cet_datetime(date)
        return date
    
    def datetimestring2datetime(self, datestring):
        """
        returns the date in UTC
        datestring has format like 2011-03-23 20:15:11
        """
        fmt = '%Y-%m-%d %H:%M:%S'
        date = datetime.strptime( datestring, fmt )
        # assuming ES/Eastern for hubblesite dates
        tz_eastern = pytz.timezone( 'US/Eastern' )
        date = tz_eastern.localize( date )
        #return datetime in timezone Europe/Berlin
        date = self.cet_datetime(date)
        return date
    
    def string_2_coordinate_frame_cv(self, frame):
        
        CV = {'ICRS': 'ICRS', # – celestial epoch-independent system 
              'FK5': 'FK5',   # – celestial, default J2000 epoch 
              'FK4': 'FK4',   # – celestial, default B1950 epoch 
              'ECL': 'ECL',   # – ecliptic coordinates 
              'GAL': 'GAL',   # – galactic coordinates 
              'SGAL': 'SGAL', # – supergalactic coordinates 
              }
        frame = frame.upper()
        try:
            framecv = CV[frame]
        except KeyError:
            framecv = None
            logger.error("ValueError in string_2_coordinate_framecv trying to convert %s" % frame)
        return framecv

    
    def string_2_file_type_cv(self, filetype):
        CV = {'image/tiff': 'TIFF',
              'image/jpeg': 'JPEG',
              'image/png':  'PNG',
              'image/gif':  'GIF',
              'image/psd':  'PSD',
              'image/pdf':  'PDF'}
        filetype = filetype.lower()
        try:
            type = CV[filetype]
        except KeyError:
            type = None
            logger.error("ValueError in string_2_file_type_cv trying to convert %s" % filetype)
        return type
    
    def string_2_spatial_quality_cv(self, text):
        CV = {'Full': 'Full',           # – Verified full WCS information (though may exclude CD matrix). 
              'Position': 'Position'    # – Spatial.ReferenceValue describes a coordinate contained somewhere within the image. Other included WCS info is to be taken as approximate or incomplete.  
              }
        try:
            CV = CV[text]
        except KeyError:
            logger.error("ValueError in string_2_spatial_quality_cv trying to convert %s" % text)
        return CV
    
    def string_2_coord_projections_cv(self, text):
        CV = {'TAN': 'TAN', # – tangent 
              'SIN': 'SIN', # – sinusoidal 
              'ARC': 'ARC', # – arc sky
              'AIT': 'AIT', # – AITOFF full-sky
              'CAR': 'CAR', # – Plate –Careé (rectilinear coordinates)
              'CEA': 'CEA', # – cylindrical equal-area 
              }
        try:
            CV = CV[text]
        except KeyError:
            logger.error("ValueError in string_2_coord_projections_cv trying to convert %s" % text)
        return CV   
    
    def avmdict(self):
        ''' 
        returns an avmdict using the values of the jsondict
        '''   
        avmdata = {}
        for key in list(self.mapping.keys()):
            json_fieldname = self.mapping[key]['fieldname']
            value = None
            try:
                value = self.jsondict[json_fieldname]       
            except KeyError:
                value = None
                logger.debug(" for avm field %s, invalid fieldname %s" % (key, json_fieldname))
            else:
                if 'func' in self.mapping[key]:
                    func = self.mapping[key]['func']
                    if callable(func):
                        value = func( value )
                    else:
                        logger.error("function %s to process JSON field %s not callable" % (str(func), str(key)))
                elif json_fieldname in self.jsondict: 
                    value = self.jsondict[json_fieldname]
                avmdata.update( { key: value })                        
        return avmdata
    
                             
    
    

