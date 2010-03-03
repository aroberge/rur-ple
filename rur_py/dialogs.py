# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    dialogs.py - dialogs, messages and exceptions used to communicate
                 with user.
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com
"""

import os
import wx
from translation import _
import images
from images import getImage

class MyDialogs(wx.Dialog):
    '''Custom dialogs that include "interesting" image and text.'''
    def __init__(self, parent, ID, title, mesg, btn_txt, img,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_DIALOG_STYLE, modal=True):

        x, y = img.GetWidth(), img.GetHeight()
        # leave room for text
        size = wx.Size(x, y+100)

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI dialog using the Create
        # method.
        pre = wx.PreDialog()
        pre.Create(parent, ID, title, pos, size, style)
        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wx.Python extension is concerned.
        self.this = pre.this

        # Add the message from the exception
        wx.StaticText(self,-1, mesg, wx.Point(0,0))
        # custom image
        wx.StaticBitmap(self, -1, img, wx.Point(0, 40))
        btnId = wx.NewId()
        button = wx.Button(self, btnId, btn_txt)
        x, y = size
        button.SetPosition(wx.Point(x/2-30, y-60))
        wx.EVT_BUTTON(self, btnId, self.OnCloseMe)
        wx.EVT_CLOSE(self, self.OnCloseWindow)

        self.CenterOnScreen()
        if modal:
            self.ShowModal()
        else:
            self.Show()

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()


#--- Error dialogs

class DialogHitWallError(MyDialogs):
    """ Custom dialog """
    def __init__(self, excpt):
        MyDialogs.__init__(self, None, -1, _("Error"), excpt.mesg,
                              _("Turn off"), getImage(images.HIT_WALL_IMAGE))

class DialogPutBeeperError(MyDialogs):
    """ Will need to have its own image """
    def __init__(self, excpt):
        MyDialogs.__init__(self, None, -1, _("Error"), excpt.mesg,
                              _("Turn off"), getImage(images.HIT_WALL_IMAGE))

class DialogPickBeeperError(MyDialogs):

    """ Will need to have its own image """
    def __init__(self, excpt):
        MyDialogs.__init__(self, None, -1, _("Error"), excpt.mesg,
                              _("Turn off"), getImage(images.HIT_WALL_IMAGE))

class UserStopError(MyDialogs):
    """ Will need to have its own image """
    def __init__(self, excpt):
        MyDialogs.__init__(self, None, -1, _("Error"), excpt.mesg,
                              _("Turn off"), getImage(images.HIT_WALL_IMAGE))

class NoTurnOffError(MyDialogs):
    """ Will need to have its own image """
    def __init__(self, excpt):
        MyDialogs.__init__(self, None, -1, _("Error"), excpt.mesg,
                              _("Turn off"), getImage(images.HIT_WALL_IMAGE))

class NormalEndDialog(MyDialogs):
    def __init__(self, excpt):
        MyDialogs.__init__(self, None, -1, _("Success!"), excpt.mesg,
                              "Ok", getImage(images.MINI_SPLASH), modal=False)
        self.timer = wx.Timer(self)
        self.timer.Start(2000)
        self.Bind(wx.EVT_TIMER, self.OnCloseMe)

#--- Exceptions

class LogicException(Exception):
    '''General class to deal with problematic instructions given to robot.'''
    def __init__(self,mesg):
        self.mesg = mesg
    def __str__(self):
        return repr(self.mesg)

class HitWallException(LogicException):
    pass

class PutBeeperException(LogicException):
    pass

class PickBeeperException(LogicException):
    pass

class UserStopException(LogicException):
    pass

class NoTurnOffException(LogicException):
    pass

class NormalEnd(LogicException):
    """ This is a normal condition raised when the program ends properly."""
    pass


#--- General Message

def messageDialog(text, title, flags = wx.OK | wx.ICON_INFORMATION):
    '''
    '''
    messageDialog = wx.MessageDialog(None, text, title, flags)
    rc = messageDialog.ShowModal()
    messageDialog.Destroy()
    return rc

def openDialog(title, wildcard, filename, initdir):
    '''
    '''
    fname = os.path.basename(filename)
    dlg = wx.FileDialog(None, title, initdir,
                           fname, wildcard, wx.OPEN | wx.CHANGE_DIR)
    returncode = dlg.ShowModal()
    if returncode == wx.ID_OK:
        savedFileName = dlg.GetPath()
    else:
        savedFileName = ""
    dlg.Destroy()
    return savedFileName

def saveDialog(title, wildcard, filename, initdir):
    '''
    '''
    fname = os.path.basename(filename)
    dlg = wx.FileDialog(None, title, initdir,
                           fname, wildcard, wx.SAVE | wx.CHANGE_DIR)
    returncode = dlg.ShowModal()
    if returncode == wx.ID_OK:
        savedFileName = dlg.GetPath()
    else:
        savedFileName = ""
    dlg.Destroy()
    return savedFileName

def checkedSaveDialog(content, title, wildcard, filename, initdir,
        overwrite = False):
    '''
    '''
    saveFinished = False
    while not saveFinished:
        savedFileName = saveDialog(title, wildcard, filename, initdir)
        if savedFileName != "":
            if overwrite or overwriteCheck(savedFileName):
                try:
                    f = open(savedFileName, 'w')
                    f.write(content)
                    f.close()
                except IOError, e:
                    messageDialog(unicode(e[1]), (u'IO Error'),
                        wx.OK | wx.STAY_ON_TOP)
                    # write aborted
                    saveFinished = False
                else:
                    # overwrite done
                    saveFinished = True
            else:
                # overwrite aborted
                saveFinished = False
        else:
            # save file aborted
            saveFinished = True

    return savedFileName

def overwriteCheck(filename):
    '''Issues a message dialog if filename is an existing file. Returns
    False if the dialog is closed by pressing Cancel. Returns True if OK is
    pressed or filename does not yet exist.
    '''
    if os.path.isfile(filename):
        if messageDialog(_(u'File %s exists. Do you want to'
            ' overwrite it?') % filename,_(u'Overwrite File?'), wx.OK
            | wx.CANCEL | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP) == wx.ID_OK:
            return True
        else:
            return False
    return True
        
#--- New attempt using sliders


class RobotBeeperDialog(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, None, -1, title=title)

        self.SetBackgroundColour("wheat")

        self.parent = parent
        self.world = parent.world
        self.WorldDisplay = parent.WorldDisplay
        self.robot = parent.world.robot_dict

        btnId = wx.NewId()
        button = wx.Button(self, btnId, "ok")
        wx.EVT_BUTTON(self, btnId, self.OnCloseMe)
        wx.EVT_CLOSE(self, self.OnCloseWindow)

        self.max1 = 20
        self.max2 = 980
        if self.robot['robot']._beeper_bag > self.max1:
            self.beepers1 = self.max1
            self.beepers2 = self.robot['robot']._beeper_bag - self.max1
        else:
            self.beepers1 = self.robot['robot']._beeper_bag
            self.beepers2 = 0

        self.slider1 = wx.Slider(self,
            # id, value, min, max, (x, y), (length, height)
            -1, self.beepers1, 0, self.max1, (0, 0), (250, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.slider1.SetTickFreq(1, 1)
        self.slider2 = wx.Slider(self,
            # id, value, min, max, (x, y), (length, height)
             -1, self.beepers2, 0, self.max2, (0, 0), (250, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.slider2.SetTickFreq(35, 1)

        mesg = _("""Select the desired value, or sum of values as
the number of beepers to put in the robot's beeper bag.""")
        label = wx.StaticText(self, -1, mesg, (0, 0))
        gbs = wx.GridBagSizer(10, 10)
        gbs.Add(label, (0, 2), (1, 4))
        gbs.Add(self.slider1, (1, 2), (1, 4))
        gbs.Add(self.slider2, (2, 2), (1, 4))
        gbs.Add(button, (3, 3))

        self.SetSizerAndFit(gbs)
        self.Show()

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnCloseMe(self, event):
        num = self.slider1.GetValue()
        num += self.slider2.GetValue()
        self.robot['robot']._beeper_bag = num
        # retrieve backup value
        x, y, key, beep = self.parent.backup_dict['robot']
        # reset to new value
        self.parent.backup_dict['robot'] = x, y, key, num
        self.parent.BeepersUpdateStatusBar()
        self.Show(False)
        self.Destroy()

class ResizeWorldDialog(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, None, -1, title=title)

        self.SetBackgroundColour("wheat")
        self.parent = parent
        self.world = parent.world
        self.WorldDisplay = parent.WorldDisplay
        self.robot = parent.world.robot_dict

        mesg = _("""Select the desired world dimensions (streets and avenues).
The existing walls and beepers will be removed.""")
        label = wx.StaticText(self, -1, mesg, (0,0))
        min_avenues = 5
        min_streets = 5
        max_avenues = 30
        max_streets = 30
        self.streets = parent.world.st
        self.avenues = parent.world.av

        world_image = wx.StaticBitmap(self, -1, getImage(images.EDIT_WORLD), (60, 90))
        length, height = world_image.GetSize()

        self.slider_street = wx.Slider(
            # id, value, min, max, (x, y), (length, height)
            self, -1, self.streets, min_streets, max_streets,
            (0, 0), (-1, height),
             wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_AUTOTICKS
            )
        self.slider_street.SetTickFreq(1, 1)
        self.slider_avenue = wx.Slider(
            # id, value, min, max, (x, y), (length, height)
            self, -1, self.avenues, min_avenues, max_avenues,
            (0, 0), (length, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.slider_avenue.SetTickFreq(1, 1)
        #

        btnId = wx.NewId()
        button = wx.Button(self, btnId, "ok")
        wx.EVT_BUTTON(self, btnId, self.OnCloseMe)
        wx.EVT_CLOSE(self, self.OnCloseWindow)

        gbs = wx.GridBagSizer(10, 10)
        gbs.Add(label, (0, 2), (1, 4))
        gbs.Add(self.slider_avenue, (1, 2), (1, 4))
        gbs.Add(world_image, (2, 2), (1, 4))
        gbs.Add(self.slider_street, (2, 1))
        gbs.Add(button, (3, 3))

        self.SetSizerAndFit(gbs)
        self.Show()

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnCloseMe(self, event):
        st = self.slider_street.GetValue()
        av = self.slider_avenue.GetValue()

        self.world.resetDimensions(av, st)
        if 'robot' in self.robot:
            self.robot['robot']._setPos(1, 1) # brings robot back to the origin
            self.robot['robot']._facing = 3   # facing east
            self.robot['robot'].robot_image = \
                     self.robot['robot']._image[self.robot['robot']._facing]
        # prepare to recreate the background images
        self.world.background_images_created = False
        self.world.AdjustWorldSize()
        self.world.InitTileSizes()
        self.WorldDisplay.InitialiseVariables()
        self.world.DoDrawing()
        # create a new bitmap image
        self.parent.buffer = wx.EmptyBitmap(self.world.maxWidth,
                                           self.world.maxHeight)
        self.WorldDisplay.drawImage()

        self.Show(False)
        self.Destroy()
