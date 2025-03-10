# -*- coding: utf-8 -*-
#
# esahubble.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

# Feed settings for website project

class ImageFeedSettings():
    title = 'ESAHubble Images'
    link = 'https://esahubble.org/images/'
    external_feed_url = 'https://feeds.feedburner.com/esahubble/images/'


class PictureOfTheWeekFeedSettings():
    title = 'ESAHubble Picture Of The Week'
    link = 'https://esahubble.org/images/potw/'
    external_feed_url = 'https://feeds.feedburner.com/esahubble/images/potw/'


class Top100FeedSettings():
    title = 'ESAHubble Top 100 Images'
    link = 'https://esahubble.org/images/archive/top100'
    external_feed_url = 'https://feeds.feedburner.com/esahubble/images/top100/'


class AnnouncementFeedSettings():
    title = 'ESAHubble Announcements'
    link = 'https://esahubble.org/announcements/'
    external_feed_url = "https://feeds.feedburner.com/esahubble/announcements/"


class VideoFeedSettings():
    title = 'ESAHubble Videos'
    link = 'https://esahubble.org/videos/'
    external_feed_url = 'https://feeds.feedburner.com/esahubble/videos/'


class ReleaseFeedSettings():
    title = 'ESAHubble News'
    link = 'https://esahubble.org/news/'
    description = "The latest news about astronomy and the NASA/ESA/CSA Hubble Space Telescope"
    external_feed_url = 'https://feeds.feedburner.com/esahubble/news/'


class HubblecastFeedSettings():
    title = 'ESAHubblecast %s'
    link = 'https://esahubble.org/videos/hubblecast/'
    description = ('The latest news about astronomy, space and the NASA/ESA Hubble Space Telescope presented in High '
                   'Definition is only for devices that play High Definition video (not iPhone or iPod). To watch the '
                   'Hubblecast on your iPod and/or iPhone, please download the Standard Definition version also '
                   'available on iTunes.')
    header_template = 'feeds/hubblecast_header.html'
    external_feed_url = 'https://feeds.feedburner.com/esahubble/cast/'


class FeedRedirectSettings():
    redirects = {
        '/images/feed/': ImageFeedSettings.external_feed_url,
        '/images/potw/feed/': PictureOfTheWeekFeedSettings.external_feed_url,
        '/videos/feed/': VideoFeedSettings.external_feed_url,
        '/videos/feed/category/hubblecast/hd/': HubblecastFeedSettings.external_feed_url,
        '/videos/feed/category/hubblecast/sd/': 'https://feeds.feedburner.com/esahubble/cast_sd/',
        '/videos/feed/category/hubblecast/fullhd/': 'https://feeds.feedburner.com/esahubble/cast_fullhd/',
        '/videos/feed/category/hubblecast/': HubblecastFeedSettings.external_feed_url,
        '/news/feed/': ReleaseFeedSettings.external_feed_url,
        '/announcements/feed/': AnnouncementFeedSettings.external_feed_url,
        '/images/feed/top100/': Top100FeedSettings.external_feed_url,
    }

    whitelist = ['FeedBurner', ]  # ,'Mozilla']
    whitelist_ips = ['134.171.', '127.0.0.1']  # must use ?bypass=1 in request


CATEGORY_SPECIFIC_SETTINGS = {
    'hubblecast': 'HubblecastFeedSettings',
}

FORMATS = {
    '': ( 'HD', '' ),
    'hd': ( 'HD', '' ),
    'sd': ( 'SD', '' ),
    'fullhd': ( 'Full HD', '' ),
}
