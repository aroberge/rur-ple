# -*- coding: utf-8
''' RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    wxutils.py
    Version 1.0
    Author: Peter Maas    Copyright  2010
    andre.roberge@gmail.com

    Utilities for wxPython
'''
import sys
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

def getscreen():
    '''
    
    '''
        # rurple default screen dimensions at startup
    # SCREEN[0] is rurple window size width at startup
    # SCREEN[1] is rurple window size height at startup
    # SCREEN[2] is the programming pane width in "code and learn" tab
    # SCREEN[3] is the debugging window height at the lower right in "code and learn"
    # SCREEN[4] is Reeborg's world brick length
    # SCREEN[5] is Reeborg's world brick thickness
    # SCREEN[6] is the beeper position offset
    # SCREEN[7] is Reeborg's horizontal offset
    # SCREEN[8] is Reeborg's vertical offset
    # SCREEN[9] is the bouton large spacer
    # SCREEN = [797,545,350,40,27,5,8,8,3] # 800x600 monitors
    # SCREEN = [900,545,450,40,27,5,8,8,3] # 1024x600 netbooks
    # SCREEN = [980,700,450,110,34,6,13,12,9] # for 1024x768 and above
    # SCREEN = [900,660,290,57,34,6,13,12,9] # in version 1.0.1
    try:
       commandline = sys.argv[1]
    except IndexError:
       screen_size = wx.Display().GetGeometry()
       if screen_size[2] < 800:
           commandline = "-xs"
       if screen_size[2] < 905:
           commandline = "-s"
       elif screen_size[3] < 695:
           commandline = "sw"
       else:
           commandline = ''

    if commandline == "-xs": # for 640x480
        screen = [637,445,260,5,20,4,5,4,-1,1]
    elif commandline == "-s" and os.name == "posix": # for 800x600 on Linux
	screen = [797,545,350,40,27,5,8,8,3,23]
    elif commandline == "-s": # for 800x600 on Windows
	screen = [797,545,345,24,27,5,8,8,3,23]
    elif commandline == "-sw" and os.name == "posix": # for 1024x600 on Linux
	screen = [900,545,450,40,27,5,8,8,3,25]
    elif commandline == "-sw": # for 1024x600 on Windows
	screen = [900,545,445,24,27,5,8,8,3,25]
    elif commandline == "-n": # for 1024x768 and above
        screen = [980,700,445,95,34,6,13,12,9,25] # default size
    else:
        screen = [980,700,445,95,34,6,13,12,9,25] # default size

    return screen
