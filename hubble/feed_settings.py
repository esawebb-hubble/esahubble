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
    description = """The ESAHubble Images feed showcases breathtaking images and scientific observations captured by the NASA/ESA/CSA James Webb Space Telescope. 
    Explore stunning infrared views of nebulae, star-forming regions, and isolated planetary-mass objects, 
    accompanied by detailed descriptions and insights into the latest astronomical discoveries."""
    external_feed_url = 'https://feeds.feedburner.com/esahubble/images/'


class PictureOfTheWeekFeedSettings():
    title = 'ESAHubble Picture Of The Week'
    link = 'https://esahubble.org/images/potw/'
    description = """The ESAHubble Picture of the Month feed features a carefully selected image from the NASA/ESA/CSA James Webb Space Telescope each month. 
    These images highlight stunning cosmic phenomena, from distant galaxies to intricate nebulae, 
    accompanied by expert insights into the science behind them."""
    external_feed_url = 'https://feeds.feedburner.com/esahubble/images/potw/'


class Top100FeedSettings():
    title = 'ESAHubble Top 100 Images'
    link = 'https://esahubble.org/images/archive/top100'
    description = """The ESAHubble Top 100 Images feed showcases the most popular and iconic images captured by the NASA/ESA/CSA James Webb Space Telescope.
    Explore stunning visuals of distant galaxies, star-forming regions, and cosmic phenomena, accompanied by detailed descriptions and insights into the latest astronomical discoveries."""
    external_feed_url = 'https://feeds.feedburner.com/esahubble/images/top100/'


class AnnouncementFeedSettings():
    title = 'ESAHubble Announcements'
    link = 'https://esahubble.org/announcements/'
    description = """The ESAHubble Announcements feed provides the latest news and updates about the NASA/ESA/CSA James Webb Space Telescope. 
    Stay informed about mission developments, scientific discoveries, and important project updates."""
    external_feed_url = "https://feeds.feedburner.com/esahubble/announcements/"


class VideoFeedSettings():
    title = 'ESAHubble Videos'
    link = 'https://esahubble.org/videos/'
    description = """The ESAHubble Videos feed features the latest video content related to the NASA/ESA/CSA James Webb Space Telescope. 
    Explore stunning visuals, mission updates, and expert insights through engaging video materials."""
    external_feed_url = 'https://feeds.feedburner.com/esahubble/videos/'


class ReleaseFeedSettings():
    title = 'ESAHubble News'
    link = 'https://esahubble.org/news/'
    description = """The ESAHubble News feed delivers the latest updates and discoveries from the NASA/ESA/CSA James Webb Space Telescope. 
    Stay informed about groundbreaking scientific findings, mission progress, and important announcements."""
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
