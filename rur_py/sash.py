# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    sash.py - Sash windows classes.
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com
"""

import wx
from world_display import WorldGUI
from bouton import rurChoiceWindow
from editor import rur_editor
from lightning import LogWindow
import conf
                            
class MySashWindow(wx.Panel):
    def __init__(self, parent, grand_parent):

        settings = conf.getSettings()
        
        wx.Panel.__init__(self, parent, -1)
        self.grand_parent = grand_parent
        self.ID_WINDOW_TOP = wx.NewId()
        self.ID_WINDOW_RIGHT = wx.NewId()
        self.ID_WINDOW_LEFT = wx.NewId()
        self.ID_WINDOW_BOTTOM = wx.NewId()
        wx.EVT_SASH_DRAGGED_RANGE(self, self.ID_WINDOW_TOP,
                               self.ID_WINDOW_BOTTOM, self.OnSashDrag)
        wx.EVT_SIZE(self, self.OnSize)

        # The following will occupy the space not used by the Layout Algorithm
        self.grand_parent.WorldDisplay = WorldGUI(self, -1)
        # Create the other windows
        # At the top, a window-like a toolbar containing buttons

        win = wx.SashLayoutWindow(self, self.ID_WINDOW_TOP, wx.DefaultPosition,
                                 wx.Size(800, 40), wx.NO_BORDER|wx.SW_3D)
        win.SetOrientation(wx.LAYOUT_HORIZONTAL)
        win.SetAlignment(wx.LAYOUT_TOP) #top
        win.SetSashVisible(wx.SASH_BOTTOM, True)
        self.topWindow = win

        # A window to the right of the client window
        win =  wx.SashLayoutWindow(self, self.ID_WINDOW_RIGHT,
                                  wx.DefaultPosition, wx.Size(350, 600),
                                  wx.NO_BORDER|wx.SW_3D)
        win.SetDefaultSize(wx.Size(0, 600))
        win.SetOrientation(wx.LAYOUT_VERTICAL)
        win.SetAlignment(wx.LAYOUT_RIGHT)
        win.SetSashVisible(wx.SASH_LEFT, True)
        self.grand_parent.rightWindow = win
        self.grand_parent.rightWindow.isVisible = False

        # Another window to the left of the client window
        win = wx.SashLayoutWindow(self, self.ID_WINDOW_LEFT,
                                 wx.DefaultPosition, wx.Size(300, 600),
                                 wx.NO_BORDER|wx.SW_3D)
        win.SetDefaultSize(wx.Size(settings.SCREEN[2], 600))
        win.SetOrientation(wx.LAYOUT_VERTICAL)
        win.SetAlignment(wx.LAYOUT_LEFT)
        win.SetSashVisible(wx.SASH_RIGHT, True)
        self.leftWindow = win
        #### new
        # Output window at the bottom
        win =  wx.SashLayoutWindow( self, self.ID_WINDOW_BOTTOM, 
                wx.DefaultPosition, wx.Size(800, settings.SCREEN[3]),
                wx.NO_BORDER|wx.SW_3D
                )
        #winids.append(win.GetId())
        #win.SetDefaultSize((WIDTH, self.output_default_height))
        win.SetOrientation(wx.LAYOUT_HORIZONTAL)
        win.SetAlignment(wx.LAYOUT_BOTTOM)
        win.SetSashVisible(wx.SASH_TOP, True)
        self.bottomWindow = win
        self.output_window = LogWindow(self.bottomWindow)
        self.bottomWindow.SetDefaultSize(wx.Size(800, settings.SCREEN[3]))
        ####################
        self.grand_parent.ch = rurChoiceWindow(self.topWindow, self.grand_parent)
        self.topWindow.SetDefaultSize(wx.Size(800, self.grand_parent.BUTTON_HEIGHT))

        self.grand_parent.WorldEditor = wx.Panel(self.grand_parent.rightWindow, -1)
        self.grand_parent.ProgramEditor = rur_editor(self.leftWindow, -1)
        # to update from within WorldDisplay, create the following link
        self.grand_parent.WorldDisplay.editor = self.grand_parent.rightWindow

    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
            return
        eID = event.GetId()
        if eID == self.ID_WINDOW_TOP:
            self.topWindow.SetDefaultSize(wx.Size(800, event.GetDragRect().height))
        elif eID == self.ID_WINDOW_RIGHT:
            self.grand_parent.rightWindow.SetDefaultSize(wx.Size(event.GetDragRect().width, 600))
        elif eID == self.ID_WINDOW_LEFT:
            self.leftWindow.SetDefaultSize(wx.Size(event.GetDragRect().width, 600))
        elif eID == self.ID_WINDOW_BOTTOM:
            self.bottomWindow.SetDefaultSize(wx.Size(800, event.GetDragRect().height))
        wx.LayoutAlgorithm().LayoutWindow(self, self.grand_parent.WorldDisplay)
        self.grand_parent.WorldDisplay.Refresh()

    def OnSize(self, event):
        wx.LayoutAlgorithm().LayoutWindow(self, self.grand_parent.WorldDisplay)

