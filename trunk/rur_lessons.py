#!/usr/bin/env python
# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    rur_lessons.py
    Version 1.0
    Authors: Frederic Muller   Copyright  2006
    fred@beijinglug.org
"""
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# 
# 
# This program checks which language is being used in RUR-PLE and
# launches the lessons in the default web browser in that 
# language. If no language is found, it defaults to English.
# 
# TODO: take a command line parameter to overwrite the default settings


import os
import webbrowser

# grabs rurple.lang location in user's home directory as per rur_py/translation.py
_user_dir = os.path.join(os.path.expanduser("~"), ".rurple")
_user_file = os.path.join(_user_dir, "rurple.lang")

# returns the content of .rurple/rurple.lang
def language():
    try:
        iso_code = open(_user_file, 'r').read()
    except:
        iso_code = 'en'
    return iso_code

url = os.getcwd() + "/lessons/" + language() + "/lessons_toc.htm"

# Open URL in a new tab, if a browser window is already open. 
webbrowser.open_new_tab(url)
