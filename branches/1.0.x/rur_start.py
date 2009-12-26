#!/usr/bin/env python
# -*- coding: latin-1 -*-
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    rur_start.py - "Main" file for RUR-PLE.
    Version 1.0
    Author: André Roberge    Copyright  2006
    andre.roberge@gmail.com
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

# todo: consider adding support for translation of commands e.g.
# todo: ...  francais()  initialises commands equivalent like avance(), etc.
# todo: create easy install for windows (exe file)
# todo: create easy install for linux  (setup.py...)
# todo: consider adding new page in notebook for turtle graphics.

import os
import sys
import wx
import wx.lib.buttons
import rur_py.misc as misc  # a few global variables

if __name__ == "__main__": # ensures that all wxPython stuff is loaded properly
    App = wx.PySimpleApp(0) # (1) redirects print output to window; 
                            # (0) to terminal
    cur_path = os.path.dirname(sys.argv[0])
    if cur_path != '':
        os.chdir(cur_path)
    misc.HOME = os.getcwd() # sets up path for later use
    #
    os.chdir("rur_images")
    misc.IMAGE_DIR = os.getcwd()
    os.chdir(misc.HOME)
    #
    os.chdir("lessons")
    from rur_py.translation import language_code
    os.chdir(language_code)
    misc.HTML_DIR = os.getcwd()
    os.chdir(misc.HOME)
    #
    os.chdir("rur_programs")
    misc.PRGM_DIR = os.getcwd()
    os.chdir(misc.HOME)
    #
    os.chdir("world_files")
    misc.WORLD_DIR = os.getcwd()
    os.chdir(misc.HOME)
    #
    os.chdir("python_files")
    misc.PYTHON_DIR  = os.getcwd()
    os.chdir(misc.HOME)

#--- see end of file for completion of the start of the application

import wx.py as py           # For the interpreter
import rur_py.images as images # load all images
import rur_py.dialogs as rD    # contains various dialogs and exception classes
from rur_py.translation import _

from rur_py.sash import MySashWindow
from rur_py.lightning import EditorSashWindow
import rur_py.parser as parser
from rur_py.bouton import pythonChoiceWindow
code = ""    # global variable defined for convenience; contains user program

from rur_py.cpu import rur_program
import rur_py.browser as browser
import rur_py.event_manager as event_manager
from rur_py.status_bar import rurStatusBar

class RURnotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, -1)
        self.parent = parent
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self, -1, self.OnPageChanged)

    def OnPageChanged(self, event):
        arg = self.parent.status_bar.notebook_new_page, event.GetSelection()
        event_manager.SendCustomEvent(self.parent, arg)
        event.Skip()

class RURApp(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 
                          _("RUR: a Python Learning Environment"),
                          size = (800, 660),
                          style=wx.DEFAULT_FRAME_STYLE)
        self.raw_code = ""
        self.filename = ""
        self.world_filename = ""
        self.isPaused = False
        self.isRunning = False
        self.isStepped = False
        self.status_bar = rurStatusBar(self)
        self.SetStatusBar(self.status_bar)

        # icon on top left of window
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(images.ICON)
        self.SetIcon(icon)
        #
        self.Show(True)
        self.window = RURnotebook(self)
        #
        win = browser.TestHtmlPanel(self.window, self)
        self.window.AddPage(win, _("  RUR: Read and Learn  "))
        #
        self.sash = MySashWindow(self.window, self)
        
        self.outputWindow = self.sash.output_window
        
        self.window.AddPage(self.sash, _("Robot: Code and Learn"))
        # See MySashWindow for the following 'shortcut' notation
        self.world = self.WorldDisplay.world
        # create a backup copy that will be used to "reset" the world
        self.backup_dict = {}
        self.backup_dict['avenues'] = self.world.av
        self.backup_dict['streets'] = self.world.st
        self.backup_dict['beepers'] = {}
        self.backup_dict['walls'] = []
        # add a robot to start
        self.world.addOneRobot(name='robot')
        self.backup_dict['robot'] = self.world.robot_dict[
                                                    'robot']._getInfoTuple()
        # create user_program object as a two-step process: create Singleton
        self.user_program = rur_program()
        # binds attributes explicitly
        self.user_program.myInit(self, self.world, self.WorldDisplay,
                               self.ProgramEditor, self.world.robot_dict)
        # We will then be able to "link" to the one rur_program() without
        # having to worry about changing attributes
        # recreate the image so that the robot shows up.
        self.world.DoDrawing()
        self.WorldDisplay.drawImage()
        self.WorldDisplay.Refresh()
        #
        win = py.shell.Shell(self.window, -1,
                            introText = "")
        self.window.AddPage(win, _("Python: Code and Learn"))

        self.sash2 = EditorSashWindow(self.window, grand_parent=self,
                                      controller=pythonChoiceWindow,
                 top_control=True, top_control_height=40)    
                # 40 = bouton "." btn_size[1] + 8
        self.window.AddPage(self.sash2, _("Python: simple editor"))

        self.SetSize((900, 660))
        self.window.SetFocus()
        self.SendSizeEvent()  # added to attempt to solve problem on MacOS
        wx.EVT_CLOSE(self, self.OnClose)

    def OnClose(self, event):
        if self.ProgramEditor.GetModify():
            rD.rurMessageDialog(
             _("Robot program has changed.\nYou may save it before quitting."), 
             _("Program has been changed"))
            self.SaveProgramFile(event)
            # in case the user does not save the program, make it appear
            # as though it has been saved so that the next attempt to 
            # quit will work.
            self.ProgramEditor.SetSavePoint() 
        else:
            self.Destroy()

#---- World file methods
    def OpenWorldFile(self, dummy):
        if self.isRunning:
            return
        wildcard = _("World files (*.wld)|*.wld| All files (*.*)|*.*") 
        dlg = wx.FileDialog(self, _("Choose a file"), misc.WORLD_DIR, "",
                           wildcard, wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.world_filename = dlg.GetPath()
            self.ReadWorldFile()
            self.UpdateWorld()
            self.user_program.clear_trace()
            misc.WORLD_DIR = os.path.dirname(self.world_filename)
            arg = self.status_bar.world_field, \
                  os.path.basename(self.world_filename)
            event_manager.SendCustomEvent(self, arg)
        dlg.Destroy()

    def ReadWorldFile(self):
        if self.isRunning:
            return
        txt = open(self.world_filename, 'r').read()
        txt = parser.FixLineEnding(txt)
        flag = parser.ParseWorld(txt)
        if flag:
            self.backup_dict = {} # used to 'reset' the world
            exec txt in self.backup_dict # extracts avenues, streets, robot,
                                     # walls and beepers

    def ResetWorld(self, dummy):
        if self.isRunning:
            return
        self.UpdateWorld()

    def UpdateWorld(self):
        try:
            av = self.backup_dict['avenues']
        except:
            rD.rurMessageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("avenues"), 
                   _("Invalid world file format"))
            return
        try:
            st = self.backup_dict['streets']
        except:
            rD.rurMessageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("streets"), 
                   _("Invalid world file format"))
            return
        self.world.resetDimensions(av, st)
        try:
            if 'robot' in self.backup_dict:
                x, y, key, beep = self.backup_dict['robot']
                arg = self.status_bar.beeper_field, beep
                event_manager.SendCustomEvent(self, arg)
        except:
            rD.rurMessageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("robot"), 
                   _("Invalid world file format"))
            return
        # We might be reloading the world, to which robots may have been added
        # Remove all robots that have been added, if any; 
        # recall that "named" robots are added through a user-defined program, 
        # not in a world file.
        self.world.robot_dict = {}
        # Recreate the robot that was in the original file
        if 'robot' in self.backup_dict:
            self.world.addOneRobot(x, y, key, beep, name='robot')

        # world characteristics
        # note: we make shallow copies of rurApp.backup_dict as we 
        # may need it if we call ResetWorld().
        try:
            for corner in self.world.beepers_dict:
                del self.world.beepers_dict[corner] # empty, but keep reference
            for corner in self.backup_dict['beepers']:
                self.world.beepers_dict[corner] = self.backup_dict[
                                                            'beepers'][corner]
        except:
            rD.rurMessageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("beepers"), 
                   _("Invalid world file format"))
            return
        # We need to keep one reference only to walls_list
        try:
            for col, row in self.world.walls_list:
                self.world.walls_list.remove((col, row)) # empty, but keep ref.
            for col, row in self.backup_dict['walls']:
                self.world.walls_list.append((col, row))
        except:
            rD.rurMessageDialog(
                   _("Problem with %s\nPlease recreate world file.")%
                   _("walls"), 
                   _("Invalid world file format"))
            return

        # prepare to recreate the background images
        self.world.background_images_created = False
        self.world.AdjustWorldSize()
        self.world.InitTileSizes()
        self.WorldDisplay.InitialiseVariables()
        self.world.DoDrawing()
        # create a new bitmap image
        self.WorldDisplay.buffer = wx.EmptyBitmap(self.world.maxWidth,
                                               self.world.maxHeight)
        self.WorldDisplay.drawImage()

    def SaveWorldFile(self, dummy):
        if self.isRunning:
            return
        wildcard = _("World files (*.wld)|*.wld| All files (*.*)|*.*")
        fname = os.path.basename(self.filename)
        dlg = wx.FileDialog(self, _("Save new world as"), misc.WORLD_DIR,
                               fname, wildcard, wx.SAVE| wx.CHANGE_DIR )
        if dlg.ShowModal() == wx.ID_OK:
            self.world_filename = dlg.GetPath()
            f = open(self.world_filename, 'w')
            txt = self.WorldDisplay.UpdateEditor()
            f.write(txt)
            f.close()
            arg = self.status_bar.world_field, \
                  os.path.basename(self.world_filename)
            event_manager.SendCustomEvent(self, arg)
            misc.WORLD_DIR = os.path.dirname(self.world_filename)
            # save a backup copy to 'reset world'
            self.backup_dict = {} 
            exec txt in self.backup_dict
        dlg.Destroy()

#----- Program files methods

    def OpenProgramFile(self, dummy):
        if self.isRunning:
            return
        wildcard = _("Program files (*.rur)|*.rur| All files (*.*)|*.*")
        dlg = wx.FileDialog(self, _("Choose a file"), misc.PRGM_DIR, "",
                           wildcard, wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            global code
            self.filename = dlg.GetPath()
            arg = self.status_bar.program_field, \
                  os.path.basename(self.filename)
            event_manager.SendCustomEvent(self, arg)
            code = open(self.filename, 'r').read()
            code = parser.FixLineEnding(code)
            self.ProgramEditor.SetText(code)
            no_error, mesg = parser.ParseProgram(code)
            misc.PRGM_DIR = os.path.dirname(self.filename)
            if no_error:
                self.raw_code = code
                self.ProgramEditor.SetSavePoint()
            else:
                code = ""
                rD.rurMessageDialog(mesg, ("Program will not be used."))
        dlg.Destroy()
    
    def SaveProgramFile(self, dummy):
        if self.isRunning:
            return
        global code
        code = self.ProgramEditor.GetText()
        no_error, mesg = parser.ParseProgram(code)
        if no_error:
            wildcard = _("Program files (*.rur)|*.rur| All files (*.*)|*.*")
            fname = os.path.basename(self.filename)
            dlg = wx.FileDialog(self, _("Save new program as"), misc.PRGM_DIR,
                               fname, wildcard, wx.SAVE| wx.CHANGE_DIR )
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetPath()
                f = open(self.filename, 'w')
                f.write(code)
                f.close()
                arg = self.status_bar.program_field, \
                      os.path.basename(self.filename)
                event_manager.SendCustomEvent(self, arg)
                code = parser.FixLineEnding(code)
                misc.PRGM_DIR = os.path.dirname(self.filename)
            dlg.Destroy()
            self.ProgramEditor.SetSavePoint()
        else:
            code = ""
            rD.rurMessageDialog(mesg, _("Program will not be saved."))

#--- Program controls

    def RunProgram(self, dummy):
        if self.user_program.isRunning:
            if self.user_program.isPaused or self.user_program.isStepped:
                self.user_program.isStepped = False
                self.Pause(None)
            return
        self.user_program.isRunning = True
        self.user_program.restart(self.world.robot_dict)

    def Pause(self, dummy):
        if not (self.user_program.isRunning or self.user_program.isStepped):
            return
        if self.user_program.isPaused:
            self.user_program.isPaused = False
            arg = self.status_bar.running_field, _("Program is running")
            event_manager.SendCustomEvent(self, arg)
        else:
            self.user_program.isPaused = True
            arg = self.status_bar.running_field, _("Program paused")
            event_manager.SendCustomEvent(self, arg)

    def Step(self, dummy):
        self.user_program.isStepped = True
        if not self.user_program.isRunning:
            self.RunProgram(None)
        else:
            self.Pause(None)

    def StopProgram(self, dummy):
        self.user_program.StopProgram()
        arg = self.status_bar.running_field, _("Program not running")
        event_manager.SendCustomEvent(self, arg)
        self.user_program.stopped_by_user = True

#--- World controls

    def EditWalls(self, event):
        if self.user_program.isRunning:
            return
        self.user_program.clear_trace()
        if self.world.editWalls:
            self.world.editWalls = False
            self.world.DoDrawing()
        else:
            self.world.editWalls = True
            self.world.DoDrawing()
        self.WorldDisplay.drawImage()
        self.WorldDisplay.Refresh()

    def BeepersToRobot(self, dummy):
        if self.user_program.isRunning:
            return
        self.user_program.clear_trace()
        try:
            dummy = self.backup_dict['robot']
        except KeyError:
            msg = _("No robot in world to give beepers to.")
            rD.rurMessageDialog(msg, 'error')
            return
        rD.RobotBeeperDialog(self, -1, _("Beepers!"))

    def BeepersUpdateStatusBar(self):
        arg = self.status_bar.beeper_field, \
              self.world.robot_dict['robot']._beeper_bag
        event_manager.SendCustomEvent(self, arg)
        # update the world window text at the same time
        self.rightWindow.DestroyChildren() # removes the old wx.StaticText
        wx.StaticText(self.rightWindow, -1,
                        self.WorldDisplay.UpdateEditor(), (10, 10))
                        
    def ResizeWorld(self, dummy):
        if self.user_program.isRunning:
            return
        self.user_program.clear_trace()
        rD.ResizeWorldDialog(self, -1, _("World size!"))

    def ToggleHighlight(self, dummy):
        if self.user_program.isRunning:
            return
        global code
        if misc.line_number_flag:
            misc.line_number_flag = False
            code = self.raw_code
        else:
            misc.line_number_flag = True
            code = parser.add_line_number_info(code)

    def ToggleWorldWindow(self, dummy):
        if self.user_program.isRunning:
            return
        if self.rightWindow.isVisible:
            self.rightWindow.SetDefaultSize(wx.Size(0, 600))
            self.rightWindow.isVisible = False
        else:
            self.rightWindow.SetDefaultSize(wx.Size(200, 600))
            self.rightWindow.isVisible = True

        wx.LayoutAlgorithm().LayoutWindow(self.sash, self.WorldDisplay)
        self.rightWindow.DestroyChildren() # removes the old wx.StaticText
        wx.StaticText(self.rightWindow, -1,
                        self.WorldDisplay.UpdateEditor(), (10, 10))

    def AddRemoveRobot(self, dummy):
        if self.user_program.isRunning:
            return
        if self.world.robot_dict:
            # remove all robots from non-empty dict
            self.world.robot_dict = {}
            arg = self.status_bar.beeper_field, self.status_bar.no_robot
        else:
            self.world.robot_dict = {}
            self.world.addOneRobot(name='robot')
            self.backup_dict['robot'] = self.world.robot_dict[
                                                       'robot']._getInfoTuple()
            arg = self.status_bar.beeper_field, \
                  self.world.robot_dict['robot']._beeper_bag
        event_manager.SendCustomEvent(self, arg)
        self.world.DoDrawing()
        self.WorldDisplay.drawImage()
        self.WorldDisplay.Refresh()
        
    def load_images(self, event):
        wildcard = "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, "Choose an image: robot facing South", 
                           os.getcwd(), "", wildcard, wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fileSouth = dlg.GetPath()
        dlg.Destroy()        
        dlg = wx.FileDialog(self, "Choose an image: robot facing North", 
                           os.getcwd(), "", wildcard, wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fileNorth = dlg.GetPath()
        dlg.Destroy()  
        dlg = wx.FileDialog(self, "Choose an image: robot facing East", 
                           os.getcwd(), "", wildcard, wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fileEast = dlg.GetPath()
        dlg.Destroy()  
        dlg = wx.FileDialog(self, "Choose an image: robot facing West", 
                           os.getcwd(), "", wildcard, wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fileWest = dlg.GetPath()
        dlg.Destroy()  
        image_south = images.GREY_ROBOT_S
        image_north = images.GREY_ROBOT_N
        image_east = images.GREY_ROBOT_E
        image_west = images.GREY_ROBOT_W
        try:
            image_south = wx.Image(self.fileSouth).ConvertToBitmap()
            image_north = wx.Image(self.fileNorth).ConvertToBitmap()
            image_east = wx.Image(self.fileEast).ConvertToBitmap()
            image_west = wx.Image(self.fileWest).ConvertToBitmap()
        except Exception, info:
            print "Conversion or loading problems: can not use new images."
            print "info = %", info
        images.GREY_ROBOT_S = image_south
        images.GREY_ROBOT_N = image_north
        images.GREY_ROBOT_E = image_east
        images.GREY_ROBOT_W = image_west
        self.AddRemoveRobot(event) # remove robot with old image
        self.AddRemoveRobot(event) # and add new one

class MySplashScreen(wx.SplashScreen):
    def __init__(self):
        wx.SplashScreen.__init__(self, images.SPLASH_SCREEN,
                wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT, 100, None, -1,
                style = wx.SIMPLE_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        wx.EVT_CLOSE(self, self.OnClose)

    def OnClose(self, evt):
        dummy = RURApp()
        evt.Skip()

if __name__ == "__main__":
    Splash = MySplashScreen()
    Splash.Show()
    App.MainLoop()

