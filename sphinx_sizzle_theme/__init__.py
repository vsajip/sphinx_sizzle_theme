# -*- coding: utf-8 -*-
#
# Copyright 2019 by Vinay Sajip. All Rights Reserved.
#

from os import path


__version__ = '0.0.3'


def setup(app):
    app.add_html_theme('sizzle', path.abspath(path.dirname(__file__)))
