from __future__ import absolute_import
# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
import os

from spacetelescope.hubblesite.avm import jsonmapper, remove_duplicates, load_json
from spacetelescope.hubblesite.utils import *
from django.test import TestCase, tag
import pytz


@tag('avm')
class TestAVM(TestCase):
    def setUp(self):
        self.test_jm = jsonmapper({
            'Creator': 'John Doe',
            'Contact Name': 'John Doe;Anne Doe',
            'Fake Field': 'This doesn\'t exists'
        })

    def test_strings2stringlist(self):
        test_string = 'a,b,c;d,e,f'
        test_list = self.test_jm.strings2stringlist(test_string)

        self.assertEqual(len(test_list), 6)
        self.assertEqual(test_list[0], 'a')

    def test_listdistances(self):
        test_string = 'z=c;e'
        test_list = self.test_jm.listdistances(test_string)

        self.assertEqual(test_list[0], 'e')
        self.assertEqual(test_list[1], 'c')

    def test_replace_html(self):
        test_string = 'test&gt;tost'
        test_list = self.test_jm.replace_html(test_string)

        self.assertEqual(test_list, 'test>tost')

    def test_subjectcategories(self):
        test_string = 'Xtest&gt;tost;test&gt;tost;asd&gt;fgh'
        test_list = self.test_jm.subjectcategories(test_string)

        self.assertEqual(len(test_list), 2)
        self.assertEqual(test_list[0], u'test>tost')

    def test_cet_datetime(self):
        summer_time = datetime.strptime('2020-07-30 10:00', '%Y-%m-%d %H:%M')
        not_summer_time = datetime.strptime('2020-02-22 10:00', '%Y-%m-%d %H:%M')

        utc = pytz.utc.localize(summer_time)
        seoul = pytz.timezone('Asia/Seoul').localize(not_summer_time)
        bogota = pytz.timezone('America/Bogota').localize(not_summer_time)

        self.assertEquals(self.test_jm.cet_datetime(utc).isoformat(), '2020-07-30T12:00:00+02:00')
        self.assertEquals(self.test_jm.cet_datetime(seoul).isoformat(), '2020-02-22T02:00:00+01:00')
        self.assertEquals(self.test_jm.cet_datetime(bogota).isoformat(), '2020-02-22T16:00:00+01:00')

    def test_datestring2datetime(self):
        test_date = '2011-03-23'

        self.assertEqual(self.test_jm.datestring2datetime(test_date).isoformat(), '2011-03-23T05:00:00+01:00')

    def test_datetimestring2datetime(self):
        test_datetime = '2011-03-23 20:15:11'
        dt2d = self.test_jm.datetimestring2datetime(test_datetime)

        self.assertEqual(dt2d.isoformat(), '2011-03-24T01:15:11+01:00')

    def test_starttimes2datetimelist(self):
        starttimes = '2005-03-23;2007-06-14;2002-06-15;2002-06-14;2002-06-13;2002-06-12;2020-01-01-01'
        st2dl = self.test_jm.starttimes2datetimelist(starttimes)

        self.assertEqual(st2dl[0].isoformat(), '2005-03-23T06:00:00+01:00')

    def test_string2coordinateframeCV(self):
        frame_cv = self.test_jm.string2coordinateframeCV('icrs')
        not_existent_frame_cv = self.test_jm.string2coordinateframeCV('2tp')

        self.assertEqual(frame_cv, 'ICRS')
        self.assertEqual(not_existent_frame_cv, None)

    def test_string2filetypeCV(self):
        frame_cv = self.test_jm.string2filetypeCV('image/tiff')
        not_existent_frame_cv = self.test_jm.string2filetypeCV('toff')

        self.assertEqual(frame_cv, 'TIFF')
        self.assertEqual(not_existent_frame_cv, None)

    def test_string2spatialqualityCV(self):
        frame_cv = self.test_jm.string2spatialqualityCV('Full')
        frame_cv2 = self.test_jm.string2spatialqualityCV('toff')

        self.assertEqual(frame_cv, 'Full')
        self.assertEqual(frame_cv2, {'Full': 'Full', 'Position': 'Position'})

    def test_string2coordprojectionsCV(self):
        frame_cv = self.test_jm.string2coordprojectionsCV('TAN')
        frame_cv2 = self.test_jm.string2coordprojectionsCV('toff')
        cv = {
            'TAN': 'TAN',
            'SIN': 'SIN',
            'ARC': 'ARC',
            'AIT': 'AIT',
            'CAR': 'CAR',
            'CEA': 'CEA',
        }

        self.assertEqual(frame_cv, 'TAN')
        self.assertEqual(frame_cv2, cv)

    # There are issues with this couple of tests

    def test_avmdict(self):
        avm_data = self.test_jm.avmdict()
        contact_name = avm_data.get('Contact.Name') if avm_data is not None and 'Contact.Name' in avm_data else []

        self.assertIsNotNone(avm_data)
        self.assertEqual(len(contact_name), 2)


@tag('avm', 'avm_utils')
class UtilsTest(TestCase):
    def test_get_url_content(self):
        url = 'https://hubblesite.org/newscenter/archive/releases/2005/37/image/'
        text, redirect = get_url_content(url)

        self.assertEqual(redirect, 'https://hubblesite.org/contents/news-releases/2005/news-2005-37.html')

    def test_remove_void(self):
        text = 'Here is a jump and a tab and multiple space'
        dirty_text = 'Here is a jump \n and a tab \r and multiple space'
        filtered_text = remove_void(dirty_text)

        self.assertEqual(filtered_text, text)

    def test_remove_duplicates(self):
        json_data = load_json(os.path.join(os.path.dirname(__file__), 'test_clients.json'))
        clients = json_data.get('clients') if json_data is not None and 'clients' in json_data else []
        clients_filtered = remove_duplicates(clients)

        self.assertIsNotNone(json_data)
        self.assertEqual(len(clients), 3)
        self.assertEqual(len(clients_filtered), 2)

