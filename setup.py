# -*- coding: utf-8 -*-
#
# esahubble.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from setuptools import setup, find_packages

setup(
    name = 'hubble',
    packages = find_packages('src'),
    package_dir = { '': 'src' },
    include_package_data = True,
    install_requires = [
        'setuptools',
        'netaddr',
    ],
    zip_safe = False,
)
