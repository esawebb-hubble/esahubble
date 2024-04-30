# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

# Feed settings for website project


class PictureOfTheWeekFeedSettings():
    external_feed_url = 'https://feeds.feedburner.com/hubble_potw/'


class AnnouncementFeedSettings():
    title = 'Hubble Announcements'
    link = 'https://www.spacetelescope.org/announcements/'
    external_feed_url = "https://feeds.feedburner.com/hubble_announcements/"


class VideoPodcastFeedSettings():
    title = 'Spacetelescope.org Video Feed'
    link = 'https://www.spacetelescope.org/videos/'
    description = 'The Latest Videos from Spacetelescope.org'
    enclosure_resources = {
            '': ['resource_hd_and_apple', 'resource_hd720p_screen', ],
            'hd': ['resource_hd_and_apple', 'resource_hd720p_screen', ],
            'sd': ['resource_medium_podcast', 'resource_vodcast', ],
            'fullhd': ['resource_hd_1080p25_screen', 'resource_hd1080p_screen', ],
    }


class ReleaseFeedSettings():
    title = 'Hubble News'
    link = 'https://www.spacetelescope.org/news/'
    description = "The latest news about astronomy and the NASA/ESA Hubble Space Telescope"
    external_feed_url = 'https://feeds.feedburner.com/hubble_news/'


class HubblecastFeedSettings():
    title = 'Hubblecast %s'
    link = 'https://www.spacetelescope.org/videos/hubblecast/'
    description = 'The latest news about astronomy, space and the NASA/ESA Hubble Space Telescope presented in High Definition is only for devices that play High Definition video (not iPhone or iPod). To watch the Hubblecast on your iPod and/or iPhone, please download the Standard Definition version also available on iTunes.'
    header_template = 'feeds/hubblecast_header.html'
    external_feed_url = 'https://feeds.feedburner.com/hubblecast/'


class FeedRedirectSettings():
    redirects = {
                '/images/potw/feed/': PictureOfTheWeekFeedSettings.external_feed_url,
                '/videos/feed/category/hubblecast/hd/': HubblecastFeedSettings.external_feed_url,
                '/videos/feed/category/hubblecast/sd/': 'https://feeds.feedburner.com/hubblecast_sd/',
                '/videos/feed/category/hubblecast/fullhd/': 'https://feeds.feedburner.com/hubblecast_fullhd/',
                '/videos/feed/category/hubblecast/': HubblecastFeedSettings.external_feed_url,
                '/news/feed/': ReleaseFeedSettings.external_feed_url,
                '/announcements/feed/': 'https://feeds.feedburner.com/hubble_announcements/',
    }

    whitelist = ['FeedBurner', ]  # ,'Mozilla']
    whitelist_ips = ['134.171.', '127.0.0.1']  # must use ?bypass=1 in request


class Top100FeedSettings():
    title = 'Hubble Top 100 Images'


class ScienceAnnouncementFeedSettings():
    title = 'ESA/Hubble Science Announcements'
    link = 'http://www.spacetelescope.org/science/announcements/'
    description = 'ESA/Hubble Science Announcements Feed'


CATEGORY_SPECIFIC_SETTINGS = {
    'hubblecast': 'HubblecastFeedSettings',
}

FORMATS = {
    '': ( 'HD', '' ),
    'hd': ( 'HD', '' ),
    'sd': ( 'SD', '' ),
    'fullhd': ( 'Full HD', '' ),
}
