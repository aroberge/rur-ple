# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    editor.py - editor for program files.
    March 2006: major change to use the "lightning compiler" basis.
    Author: Andre Roberge    Copyright  2005, 2006
    andre.roberge@gmail.com
"""
import wx
import wx.stc as stc
from lightning import PythonEditor

if wx.Platform == '__WXMSW__':
    faces = { 'mono' : 'Courier New',
              'helv' : 'Arial',
              'size' : 11,
              'size2': 8,
             }
else:
    faces = { 'mono' : 'Courier',
              'helv' : 'Helvetica',
              'size' : 11,
              'size2': 9,
             }

class rur_editor(PythonEditor):
    def __init__(self, parent, ID):
        PythonEditor.__init__(self, parent, ID)
        self.parent = parent

        # changes from defaults: for pedagogical reasons, I chose to highlight python keywords (bold, blue),
        # all strings (including comments) in green and everything else in black.
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#6699CC,bold,face:%(mono)s,size:%(size)d" % faces)# Keywords
        all_strings_style = "fore:#660066,face:%(mono)s,size:%(size)d"
        comments_style = "fore:#009900,face:%(mono)s,size:%(size)d"
        self.SetViewWhiteSpace(1)  # show white spaces ...
        self.SetIndentationGuides(False) # therefore, do not show indent guides
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, comments_style % faces) # Comments
        self.StyleSetSpec(stc.STC_P_STRING, all_strings_style % faces)      # String
        self.StyleSetSpec(stc.STC_P_CHARACTER, all_strings_style % faces)   # Single quoted string
        self.StyleSetSpec(stc.STC_P_TRIPLE, all_strings_style % faces)      # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, all_strings_style % faces)# Triple double quotes
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, comments_style % faces)# Comment-blocks

#--- highlighting user_code line --------------------------------

        self.MarkerDefine(7, stc.STC_MARK_BACKGROUND, 'white', 'wheat')
        self.marked_line = -1

    def highlight(self, line):
        if self.marked_line != -1:
            self.MarkerDelete(self.marked_line, 7)
        self.MarkerAdd(line, 7)
        self.marked_line = line

    def remove_highlight(self):
        self.MarkerDelete(self.marked_line, 7)
        self.marked_line = -1
