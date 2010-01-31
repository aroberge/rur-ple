# -*- coding: utf-8
''' RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    wxutils.py
    Version 1.0
    Author: Peter Maas    Copyright  2010
    andre.roberge@gmail.com

    Utilities for wxPython
'''
import wx

def wxversiontuple():
     '''returns wx.version() as a tuple of ints for numeric
     comparison of versions.
     '''
     try:
         if hasattr(wx, 'version'):
             return tuple(map(int, wx.version().split()[0].split('.')))
         elif hasattr(wx, '__version__'):
             return tuple(map(int, wx.__version__.split('.')))
     except Exception:
         return (0, 0, 0, 0)
