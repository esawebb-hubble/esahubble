# -*- coding: utf-8 -*-
#
# esahubble.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

"""
DEPRECATED - Please use South data migrations instead.

Certain templates embeds pages defined via the djangoplicity.poages app. They
use a page key to select which page to embed. To ensure that these keys are
created a special management command "appsregister" will execute the code
in this module to ensure that the keys exists.

Currently, the "appsregister" command must be run manually by the developer
after a new deployment. Also, "appsregister" is no longer the preferred method
for creating data in the database. Instead South data migrations should be used
instead, which provides much better management and features.
"""


# ========================
# Register global page key
# ========================
from djangoplicity.pages.models import register_page_key
from django.utils.translation import ugettext as _

import warnings

warnings.warn( "Use of appsregister have been deprecated. Please use South data migrations instead.", DeprecationWarning )

PAGE_KEYS = {
              "login": 'huble.login',
              "logout": 'huble.logout',
              "hubblecast_sidebar": "huble.hubblecast_sidebar",
              "access_denied": "huble.access_denied",
              "shop_right_column": "djangoplicity.shop_right_column",
              "free_order_form": "djangoplicity.free_order_form",
              "frontpage_rightcol": "huble.frontpage_rightcol",
              "image_archive_top": "huble.image_archive_top",
            }

register_page_key( 'huble', PAGE_KEYS["login"], _('Login page'), _('Displayed above the login form.') )
register_page_key( 'huble', PAGE_KEYS["logout"], _('Logout page'), _('Displayed on the logout page.') )
register_page_key( 'huble', PAGE_KEYS["hubblecast_sidebar"], _('Hubblecast Sidebar'), _('Right-column displayed on the hubblecast feature page') )
register_page_key( 'huble', PAGE_KEYS["access_denied"], _('Access Denied'), _('Displayed when users are denied access to embargoed/staging resources.') )
register_page_key( 'huble', PAGE_KEYS["frontpage_rightcol"], _('Frontpage right column'), _('Displayed above archive picture of the day.') )
register_page_key( 'huble', PAGE_KEYS["image_archive_top"], _('Image archive top'), _('Displayed just below the title in image archive list views.') )
register_page_key( 'djangoplicity', PAGE_KEYS["shop_right_column"], _('Shop Right Column'), _('Displayed on shop frontpage in right column.') )
register_page_key( 'djangoplicity', PAGE_KEYS["free_order_form"], _('Free Order Form'), _('Displayed message on the Free Order form.') )
