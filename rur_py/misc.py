# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    misc.py - contains various parameters
    Version 1.0
    Author: Andre Roberge    Copyright  2006
    andre.roberge@gmail.com
"""

stopped_by_user = False

#--- directories information
HOME = ''     # will be set as current working directory
MYFILES_HOME = '' # user's sample code directory
IMAGE_DIR = ''    # images for program - excluding lessons
HTML_DIR = ''     # lessons and other html files
PRGM_DIR = ''     # user-defined programs
WORLD_DIR = ''    # user-defined worlds
PYTHON_DIR = ''

# TODO: Should be moved to a better place, perhaps wxcompat.
def wxversiontuple():
     '''returns wx.version() as a tuple of ints for numeric
     comparison of versions.
     '''
     import wx
     return tuple(map(int, wx.version().split()[0].split('.')))
