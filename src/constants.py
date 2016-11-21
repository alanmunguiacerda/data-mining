#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

NO_MRKUP_DATA_SYMBOL = "?"
MISSING_DATA_SYMBOL = "<b><i>?</i></b>"
ADD_MARKUP_STRING = '<span foreground="green">Add</span>'
DEL_MARKUP_STRING = '<span foreground="red">Del</span>'
MOD_MARKUP_STRING = '<span foreground="blue">Mod</span>'
SPAN_MARKUP_REGEXP = '(</?span([a-z]|=|\"|\s)*>)'
CHI_VALUES_DIR = os.path.abspath('abs_values/chi_square.json')
