# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    browser.py - Simple html browser
        Adapted from wxPython demo code
    Version 1.0
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com
"""
import os.path
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

import os
import conf
import wx
import wx.html as  html
import wx.lib.wxpTag
import translation
from  translation import _
import images
from images import getImage
import dialogs

#----------------------------------------------------------------------

def relPathOfPage(page):
    '''Returns the part of the URL after the language path. Used to
    switch between corresponding lessons of different languages.
    '''
    # Make sure that lessonbase has a http like path separator
    lessonbase = conf.getSettings().LESSONS_DIR.replace(os.path.sep, '/')
    if (page.startswith(lessonbase)):
        lbcount = len(lessonbase.split('/'))
        pageparts = page.split('/')
        return '/'.join(pageparts[lbcount +1:])
    else:
        return ''

class TestHtmlPanel(wx.Panel):
    def __init__(self, parent, grand_parent):

        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.lessons_dir = conf.getLessonsNlDir()
        
        self.parent = parent
        self.grand_parent = grand_parent

        self.html = html.HtmlWindow(self, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)

        btn_size = (32, 32)
        spacer_large = (125, 36)
        spacer_small = (4, 4)
        tip_list = [_("Open local html file"), _("Go back in browser history"),
                     _("Home"), _("Go forward in browser history"),
                     _("Select a language")]
        button_list = [
            [None,      False, None, None, spacer_small, None],
            [wx.NewId(), True, self.OnLoadFile, getImage(images.OPEN_HTML),
                btn_size, tip_list[0]],
            [None,      False, None, None, spacer_large, None],
            [wx.NewId(), True, self.OnBack, getImage(images.BACK),
                btn_size, tip_list[1]],
            [None,      False, None, None, spacer_small, None],
            [wx.NewId(), True, self.OnHome, getImage(images.HOME),
                btn_size, tip_list[2]],
            [None,      False, None, None, spacer_small, None],
            [wx.NewId(), True, self.OnForward, getImage(images.FORWARD),
                btn_size, tip_list[3]],
            [None,      False, None, None, spacer_large, None],
            [wx.NewId(), True, None, getImage(images.LANGUAGES),
                (58,34), tip_list[4]],
            [None,      False, None, None, spacer_small, None]
            ]

        self.box = wx.BoxSizer(wx.VERTICAL)
        subbox = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_list = []
        for id, button, action, img, size, tip in button_list:
            if button:
                name = wx.lib.buttons.GenBitmapButton(self, id, img, size=size)
                name.SetToolTipString(tip)
                wx.EVT_BUTTON(self, id, action)
                subbox.Add(name, 0, wx.SHAPED)
                self.btn_list.append(name)  # create a list for later reference
            else:
                subbox.Add(size, 0, wx.EXPAND)

        languageList = []
        for language in conf.getAvailableLanguages():
            languageList.append(translation.languages[language][2])
        languageList.sort()
        self.ch = wx.Choice(self, -1, choices = languageList)

        # set index of current language
        try:
            langnum = languageList.index(translation.languages[
                conf.getLanguage()][2])
        except ValueError:
            langnum = languageList.index(translation.languages['en'][2])

        self.ch.SetSelection(langnum)

        self.Bind(wx.EVT_CHOICE, self.ChooseLanguage, self.ch)
        subbox.Add(self.ch, 0, wx.SHAPED)

        self.box.Add(subbox, 0, wx.GROW)
        self.box.Add(self.html, 1, wx.GROW)
        self.SetSizer(self.box)
        self.SetAutoLayout(True)

        name = os.path.join(self.lessons_dir, 'rur.htm')
        self.html.LoadPage(name)

    def ChooseLanguage(self, event):
        translation.select(event.GetString()) 
        # notebook tabs
        self.grand_parent.window.SetPageText(0, _("  RUR: Read and Learn  "))
        self.grand_parent.window.SetPageText(1, _("Robot: Code and Learn"))
        self.grand_parent.window.SetPageText(2, _("Python: Code and Learn"))
        self.grand_parent.window.SetPageText(3, _("Python: simple editor"))
        self.grand_parent.SetTitle(_("RUR: a Python Learning Environment"))
        # tool tips; recreate the list in the new language and use it
        tip_list = [_("Open local html file"), _("Go back in browser history"),
                     _("Home"), _("Go forward in browser history"),
                     _("Select a language")]
        for i in range(len(tip_list)):
            self.btn_list[i].SetToolTipString(tip_list[i])
        self.parent.Refresh()
        # choice window in Robot page
        self.grand_parent.ch.SelectLanguage()
        # choice window in Python editor
        self.grand_parent.py_ch.SelectLanguage()

        self.lessons_dir = conf.getLessonsNlDir()
        # page loaded in browser
        current_page = self.html.GetOpenedPage()
        relPath = relPathOfPage(current_page)
        if len(relPath) > 0:
            new_page = os.path.join(self.lessons_dir, relPath)
            if os.path.isfile(new_page):
                self.html.LoadPage(new_page)
            else:
                lessonbase = conf.getSettings().LESSONS_DIR
                new_page = os.path.join(lessonbase, 'en', relPath)
                if os.path.isfile(new_page):
                    self.html.LoadPage(new_page)
                else:
                    dialogs.messageDialog(
                        _('Cannot find a translation for %s') % current_page,
                        _('Translation Problem'))
        # status bar
        self.grand_parent.status_bar.ChangeLanguage()
        # world display
        self.grand_parent.world.background_images_created = False
        self.grand_parent.world.DoDrawing()

    def OnHome(self, event):
        name = os.path.join(self.lessons_dir, 'rur.htm')
        self.html.LoadPage(name)

    def OnLoadFile(self, event):
        openedFileName = dialogs.openDialog(_("Choose a file"),
            _("html files (*.htm*)|*.htm*| All files (*.*)|*.*"),
            "", self.lessons_dir)

        if openedFileName != "":
            path = openedFileName
            self.html.LoadPage(path)

    def OnBack(self, event):
        if not self.html.HistoryBack():
            #wx.MessageBox("No more items in history!")
            pass

    def OnForward(self, event):
        if not self.html.HistoryForward():
            #wx.MessageBox("No more items in history!")
            pass
