# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    event_manager.py
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com
"""

import wx

# Custom event
# The functions and class are needed to create everything needed for our custom
# wxPython event with the extra ability to include extra data.
# See class MyWorldGUI.UpdateWorld for how to use it with extra data.
# Every object that wants to update the statusbar should call SendCustomEvent()
StatusBarEvent = wx.NewEventType()

def myEVT_StatusBarChanged(window, function):
    """See class StatusBarChangedEvent and class StatusBar"""
    window.Connect( -1, -1, StatusBarEvent, function )

def SendCustomEvent(parent, *args):
    """Use this to emit a event which is received by the statusbar class.
    parent must be a valid wxPython window.
    args is a optional tuple which is passed to the receiving object."""
    event = StatusBarChangedEvent(parent.GetId(), args)
    parent.GetEventHandler().AddPendingEvent(event)

class StatusBarChangedEvent(wx.PyCommandEvent):
    """Custom event used to notify the statusbar.
    This event can be used everywere but here we let the statusbar handle it."""
    eventType = StatusBarEvent
    def __init__(self, id, data):
        self.data = data
        wx.PyCommandEvent.__init__(self, self.eventType, id)
    def Clone(self):
        self.__class__(self.GetId())

