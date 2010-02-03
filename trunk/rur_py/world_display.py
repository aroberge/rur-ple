# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    world_display.py - Displays "world" with "robot" and allow
                      keyboard-based interactions
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005
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

import wx
from world_creation import Visible_world
from robot_factory import Used_robot, New_improved_robot
import dialogs
import wxutils

 # version dependent function keycode to make rur-ple work with
 # wxpython 2.6 to latest
if wxutils.wxversiontuple() < (2, 7, 1, 1):
    def keycode(event):
        return event.KeyCode()
else:
    def keycode(event):
        return event.KeyCode

class WorldGUI(wx.ScrolledWindow):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size,
                                  style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour("WHITE")
        self.world = Visible_world()
        self.editor = False  #
        self.InitialiseVariables()
        self.MakePopupMenu()
        self.bindEvents()
        self.SetFocus()

    def InitialiseVariables(self):
        # Create the world image
        self.world.updateImage = False
        self.world.DoDrawing()
        # Initialize the buffer bitmap.  No real DC is needed at this point.
        self.buffer = wx.EmptyBitmap(self.world.maxWidth, self.world.maxHeight)
        self.drawImage()

        # Set the size of the total window, of which only a small part
        # will be displayed; apparently SetVirtualSize needs
        # a single (tuple) argument, which explains the double (( )).
        self.SetVirtualSize((self.world.maxWidth, self.world.maxHeight))

        # Set the scrolling rate; use same value in both horizontal and
        # vertical directions.
        scrollRate = self.world.tile_narrow + self.world.tile_wide
        self.SetScrollRate(scrollRate, scrollRate)
        # yPos below set so that we are at the bottom of the scrolledWindow
        self.SetScrollbars(1, 1, self.world.maxWidth,
                           self.world.maxHeight, yPos=self.world.maxHeight)
        # allow for testing "new and improved" robot
        self.newRobot = False

    def bindEvents(self):
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_LEFT_DOWN(self, self.OnLeftDown) # for "drawing"
        wx.EVT_CHAR(self, self.MyKeys) # to test Robot actions
        wx.EVT_IDLE(self, self.OnIdle)
        wx.EVT_RIGHT_UP(self, self.OnRightUp)

    def OnIdle(self, event=None):
        """
        Do any needed updating on Idle time ...
        """
        if self.world.updateImage:
            self.drawImage()
        self.world.updateImage = False

    def OnPaint(self, event=None):
        try:
            dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        except:
            dc = wx.BufferedPaintDC(self, self.buffer) # before wxPython 2.5.4.1

    def isActive(self, event):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        self.x, self.y = event.GetPositionTuple()
        self.x += xView*xDelta
        self.y += yView*yDelta
        # Test to see if in "active" zone i.e. inside world borders
        if (self.x > self.world.xOffset and
           self.y > self.world.yTopOffset and
           self.y < self.world.maxHeight - self.world.yOffset and
           self.x < self.world.maxWidth - self.world.right_scroller_space):
            return True
        else:
            return False

    def OnLeftDown(self, event):
        """Called when the left mouse button is pressed and build
           or remove walls."""
        self.SetFocus()
        if self.isActive(event):
            col, row = self.world.CalculatePosition(self.x, self.y)
            self.world.ChangeWall(col, row)
            if self.world.updateImage:
                self.drawImage()
                self.Refresh()
        else:
            pass   # added for clarity; we are on the outside

    def MakePopupMenu(self):
        """Make a menu for beepers that can be popped up later;
        this menu will offer the possibility of
        putting a given number of beepers
        at the current location (street/avenue intersection)."""
        menu = wx.Menu()
        self._beeperChoice = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, \
                          11, 12, 13, 14, 15, 20, 40, 60, 80, 99]
        maxNumberOfBeepers = len(self._beeperChoice)
        # This version is revised from 0.9.1 to avoid "hard-wired"
        # IDs in appending the menu and let wxPython decide on suitable
        # values.  The previous version caused problems on MacOS.
        # Note that OnMenuSetBeepers() had to be modified as well.
        self.popID = []
        for index, beepers in enumerate(self._beeperChoice):
            self.popID.append(wx.NewId())
            menu.Append(self.popID[index], str(beepers))
            self.Bind(wx.EVT_MENU, self.OnMenuSetBeepers, 
                      id=self.popID[index])
        self.menu = menu
        
    def OnMenuSetBeepers(self, event):
        self._num = self._beeperChoice[self.popID.index(event.GetId())]

    def OnRightUp(self, event):
        """called when the right mouse button is released,
        will call the popup menu, offering the possibility of
        putting a given number of beepers
        at the current location (street/avenue intersection)."""
        if self.isActive(event):
            col, row = self.world.CalculatePosition(self.x, self.y)
            if row%2:
                if col%2:
                    pt = event.GetPosition()
                    self.PopupMenu(self.menu, pt)
                    av = (col+1)/2
                    st = (row+1)/2
                    self.world.setBeepers((av, st), self._num)
                    if self.world.updateImage:
                        self.drawImage()
                        self.Refresh()
        else:
            pass   # added for clarity; we are on the outside

    def MyKeys(self, event):
        message = """
            F5: Help (i.e. this message)

Editing world:
            lower case e: toggle in/out of edit walls mode
            Left mouse button: add or remove walls (if in edit walls mode)
            Right mouse button: put beepers at intersection

Robot actions:
            Up arrow:     move robot forward
            Left arrow:   turn robot left
            lower case p: pick_beeper
            upper case P: put_beeper

            Errors will occur if you attempt to move through a wall,
            put a beeper when you carry none,
            or try to pick up a beeper where there is none.

For testing only (future features):
            F7: creates New_improved_robot
            Right arrow:   turn robot right (only New_improved_robot)
            F8: creates Used_robot (default)"""
        code = keycode(event)
        if code == wx.WXK_UP:           # up arrow
            if 'robot' in self.world.robot_dict:
                try:
                    self.world.MoveRobot('robot') # may raise an exception
                    self.scrollWorld('robot')
                except dialogs.HitWallException, mesg:
                    dialogs.DialogHitWallError(mesg)
        elif code == wx.WXK_LEFT:       # left arrow
            self.world.TurnRobotLeft('robot')
        elif code == 112:            # p - lower case
            if 'robot' in self.world.robot_dict:
                try:
                    self.world.robot_dict['robot'].pick_beeper()
                    if self.editor:
                        self.editor.DestroyChildren()
                        wx.StaticText(self.editor, -1, self.UpdateEditor(), (10, 10))
                except dialogs.PickBeeperException, mesg:
                    dialogs.DialogPickBeeperError(mesg)
        elif code == 80:             # P - upper case
            if 'robot' in self.world.robot_dict:
                try:
                    self.world.robot_dict['robot'].put_beeper()
                    if self.editor:
                        self.editor.DestroyChildren()
                        wx.StaticText(self.editor, -1, self.UpdateEditor(), (10, 10))
                except dialogs.PutBeeperException, mesg:
                    dialogs.DialogPutBeeperError(mesg)
        elif code == 101:            # e - lower case
            if self.world.editWalls:
                self.world.editWalls = False
                self.world.DoDrawing()
            else:
                self.world.editWalls = True
                self.world.DoDrawing()
        elif code == wx.WXK_F5:
            dialogs.messageDialog(message, "Help :-)")
        elif code == wx.WXK_F7:
            self.world.robot_dict['robot'] = New_improved_robot(parent = self.world)
            self.world.DoDrawing()
            self.newRobot = True
        elif code == wx.WXK_F8:
            self.world.robot_dict['robot'] = Used_robot(parent = self.world)
            self.world.DoDrawing()
            self.newRobot = False
        elif code == wx.WXK_RIGHT:       # right arrow
            if self.newRobot:         # only New_improved_robot can turn right.
                self.world.TurnRobotRight('robot')
            else:
                pass
        else:
            pass
        if self.world.updateImage:
            self.drawImage()
            self.Refresh()
    #- end of MyKeys()-----------------------------------------

    def scrollWorld(self, name):
        '''Determines if window needs scrolling and does necessary.'''
        # determine robot image bounding box
        x0, y0 = self.world.robot_image_origin
        x1, y1 = self.world.robot_dict[name]._image_size
        x1 += x0
        y1 += y0

        # marginal space around robot
        margin = self.world.tile_narrow + self.world.tile_wide
        margin *= 2

        # position of top left visible window in "scrollrate" units
        xView, yView = self.GetViewStart()
        xViewOld, yViewOld = xView, yView

        # corresponding amount of pixel per "scroll"
        xDelta, yDelta = self.GetScrollPixelsPerUnit()

        # size of wisible window
        width, height = self.GetSizeTuple()

        #-- Determine if window needs to be scrolled so that object
        # remains visible.  Assume that the object fits entirely
        # in the visible view.
        if x0 - margin < xView*xDelta:
            xView = max(0, -1 + (x0-margin)/xDelta)
        elif x1 + margin > xView*xDelta + width:
            xView = (x1 + margin - width)/xDelta
        if y0 - margin < yView*yDelta:
            yView = max(0, -1 + (y0-margin)/yDelta)
        elif y1 + margin > yView*yDelta + height:
            yView = (y1 + margin - height)/yDelta
        # if needed, scroll window by required amount to keep image in view
        if xView != xViewOld or yView != yViewOld:
            self.Scroll(xView, yView)

    def drawImage(self):
        dc = wx.BufferedDC(None, self.buffer)
        dc.BeginDrawing()
        # Simply copy the world image onto the buffer
        dc.DrawBitmap(self.world.world_image, 0, 0, True)
        # update the editor
        if self.editor:
            self.editor.DestroyChildren() # removes the old wx.StaticText
            wx.StaticText(self.editor, -1, self.UpdateEditor(), (10, 10))
        dc.EndDrawing()


    def UpdateEditor(self):
        av_string = "avenues = " + str(self.world.num_cols//2)
        st_string = "streets = " + str(self.world.num_rows//2)
        robot_string = ''
        for name in self.world.robot_dict:
            x, y = self.world.robot_dict[name].getPos()
            beepers = self.world.robot_dict[name]._beeper_bag
            orientation = self.world.robot_dict[name]._getOrientationKey()
            robot_string += name + " = " + \
                  self.world.robot_dict[name]._getInfoString() + "\n"
        if len(self.world.walls_list) > 0:
            wall_string = "walls = [\n"
            for item in self.world.walls_list:
                wall_string = wall_string + ("    " + str(item)
                                         + ', \n')
            wall_string = wall_string[0:-3]+'\n]'
        else:
            wall_string = "walls = []"
        if len(self.world.beepers_dict) > 0:
            beeper_list = "beepers = {\n"
            for key in self.world.beepers_dict:
                beeper_list = beeper_list + ("    " + str(key) + ': '
                       + str(self.world.beepers_dict[key])+ ', \n')
            beeper_list = beeper_list[0:-3]+'\n}'
        else:
            beeper_list = "beepers = {}"

        worldmap = av_string + '\n' + st_string + '\n' + robot_string \
                  + wall_string + '\n' +  beeper_list
        return worldmap
