# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    bouton.py - Defines "menu choices" through buttons
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com
"""

import wx
import images
from images import getImage
from translation import _
import conf  # a few global variables

SPACER = 0
BITMAP = 1
BUTTON = 2
    
class rurChoiceWindow(wx.ScrolledWindow):
    def __init__(self, parent, great_grand_parent):
        settings = conf.getSettings()

        wx.ScrolledWindow.__init__(self, parent, -1)

        self.ggp = great_grand_parent    # rurApp instance!
        btn_size = (32, 32)
        self.ggp.BUTTON_HEIGHT = btn_size[0] + 8
        spacer_large = (settings.SCREEN[9], settings.SCREEN[9])

        tip_list = [_("Opens existing robot program"), 
                          _("Saves robot program"), 
                          _("Opens existing world file"),
                          _("Saves world file"), 
                          _("Resets world - from open file"), 
                          _("Runs robot program"),
                          _("Steps through robot program instructions"), 
                          _("Pause program"), 
                          _("Stops program"), 
                          _("Adjust robot speed"),
                          _("Edit walls"),
                          _("Resize world"),
                          _("Give beepers to robot"), 
                          _("Remove/add robot from/to world"),
                          _("Toggle world file view"),
                          _("Load new images for robot")]

        widget_list1 = [
            [wx.NewId(), BUTTON, self.ggp.OpenProgramFile,
                getImage(images.OPEN_PROGRAM), btn_size, tip_list[0]],
            [wx.NewId(), BUTTON, self.ggp.SaveProgramFile,
                getImage(images.SAVE_PROGRAM), btn_size, tip_list[1]],
            [None,      SPACER, None, None, spacer_large, None],
            [wx.NewId(), BUTTON, self.ggp.OpenWorldFile,
                getImage(images.OPEN_WORLD), btn_size, tip_list[2]],
            [wx.NewId(), BUTTON, self.ggp.SaveWorldFile,
                getImage(images.SAVE_WORLD), btn_size, tip_list[3]],
            [wx.NewId(), BUTTON, self.ggp.ResetWorld,
                getImage(images.RESET_WORLD), btn_size, tip_list[4]],
            [None,      SPACER, None, None, spacer_large, None],
            [wx.NewId(), BUTTON, self.ggp.RunProgram,
                getImage(images.RUN_PROGRAM), btn_size, tip_list[5]],
            [wx.NewId(), BUTTON, self.ggp.Step,
                getImage(images.STEP), btn_size, tip_list[6]],
            [wx.NewId(), BUTTON, self.ggp.Pause,
                getImage(images.PAUSE), btn_size, tip_list[7]],
            [wx.NewId(), BUTTON, self.ggp.StopProgram,
                getImage(images.STOP), btn_size, tip_list[8]],
            [None,      SPACER, None, None, spacer_large, None],
            [wx.NewId(),  BITMAP, None,
                getImage(images.SPEED), btn_size, tip_list[9]]
            ]

        widget_list2 =[
            [None,      SPACER, None, None, spacer_large, None],
            [wx.NewId(), BUTTON, self.ggp.EditWalls,
                getImage(images.WALL), btn_size, tip_list[10]],
            [wx.NewId(), BUTTON, self.ggp.ResizeWorld,
                getImage(images.RESIZE), btn_size, tip_list[11]],
            [wx.NewId(), BUTTON, self.ggp.BeepersToRobot,
                getImage(images.BEEPERS_ROBOT), btn_size, tip_list[12]],
            [None,      SPACER, None, None, spacer_large, None],
            [wx.NewId(), BUTTON, self.ggp.AddRemoveRobot,
                getImage(images.ADD_REMOVE_ROBOT), btn_size, tip_list[13]],
            [None,      SPACER, None, None, spacer_large, None],
            [wx.NewId(), BUTTON, self.ggp.ToggleWorldWindow,
                getImage(images.SHOW_WORLD_FILE), btn_size, tip_list[14]],
            [None,      SPACER, None, None, spacer_large, None],
            [wx.NewId(), BUTTON, self.ggp.load_images,
                getImage(images.NEW_ROBOT_IMAGES), btn_size, tip_list[15]],
            ]
        box = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_list = []
        for id, widget, action, img, size, tip in widget_list1:
            if widget == BUTTON:
                name = wx.lib.buttons.GenBitmapButton(self, id, img, size=size)
                name.SetToolTipString(tip)
                wx.EVT_BUTTON(self, id, action)
                box.Add(name, 0, wx.SHAPED)
                self.btn_list.append(name)  # create lists for later reference
            elif widget == BITMAP:
                name = wx.StaticBitmap(self, -1, img, size=size)
                box.Add(name, 0, wx.SHAPED)
                self.btn_list.append(name)  # create lists for later reference
            elif widget == SPACER:
                box.Add(size, 0, wx.EXPAND)

        min_speed = 0
        max_speed = 8
        default_speed = 3
        self.ggp.slider_speed = wx.Slider(
            # id, value, min, max, (x, y), (length, height)
            self, -1, default_speed, min_speed, max_speed,
            (-1, -1), (100, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS #| wx.SL_LABELS
            )
        self.ggp.slider_speed.SetTickFreq(1, 1)
        self.ggp.slider_speed.SetToolTipString(tip_list[9])
        box.Add(self.ggp.slider_speed, 0, wx.SHAPED)
        self.ggp.slider_speed.SetFocus()  # to make it same colour as background

        for id, widget, action, img, size, tip in widget_list2:
            if widget == BUTTON:
                name = wx.lib.buttons.GenBitmapButton(self, id, img, size=size)
                name.SetToolTipString(tip)
                wx.EVT_BUTTON(self, id, action)
                box.Add(name, 0, wx.SHAPED)
                self.btn_list.append(name)  # create lists for later reference
            elif widget == BITMAP:
                name = wx.StaticBitmap(self, -1, img, size=size)
                box.Add(name, 0, wx.SHAPED)
                self.btn_list.append(name)  # create lists for later reference
            elif widget == SPACER:
                box.Add(size, 0, wx.EXPAND)
        self.SetSizer(box)
        self.SetScrollRate(10, 0)

    def SelectLanguage(self):
        # recreate the list, using the new language
        tip_list = [_("Opens existing robot program"), 
                          _("Saves robot program"), 
                          _("Opens existing world file"),
                          _("Saves world file"), 
                          _("Resets world - from open file"), 
                          _("Runs robot program"),
                          _("Steps through robot program instructions"), 
                          _("Pause program"), 
                          _("Stops program"), 
                          _("Adjust robot speed"),
                          _("Edit walls"),
                          _("Resize world"),
                          _("Give beepers to robot"), 
                          _("Remove/add robot from/to world"),
                          _("Toggle world file view"),
                          _("Load new images for robot")]
        for i in range(len(tip_list)):
            self.btn_list[i].SetToolTipString(tip_list[i])
        self.ggp.slider_speed.SetToolTipString(tip_list[9])

class pythonChoiceWindow(wx.Panel):
    def __init__(self, parent, editor):
        wx.Panel.__init__(self, parent, -1)

        btn_size = (32, 32)
        spacer_small = (4, 4)
        spacer_large = (25, 25)

        tip_list = [_("Open Python file"), 
                         _("Save Python file"),
                         _("Run Python program"),
                        _("Run program with argument list"),
                        _("Help"),
                        _("Go to line number"),
                        _("Hide or show output window"),
                        _("Change layout"),
                         _("Clear text")]

        helpId = wx.NewId()
        openId = wx.NewId()
        saveId = wx.NewId()
        runId = wx.NewId()
        runWithId = wx.NewId()
        goToId = wx.NewId()
        showId = wx.NewId()
        clearId = wx.NewId()
        switchId = wx.NewId()

        widget_list = [
            [None, SPACER, None, None, spacer_small, None],
            [openId, BUTTON, editor.openFile,
                getImage(images.OPEN_PYTHON), btn_size, tip_list[0]],
            [None, SPACER, None, None, spacer_small, None],
            [saveId, BUTTON, editor.saveFile,
                getImage(images.SAVE_PYTHON), btn_size, tip_list[1]],
            [None, SPACER, None, None, spacer_large, None],
            [runId, BUTTON, editor.run,
                getImage(images.RUN_PROGRAM), btn_size, tip_list[2]],
            [None, SPACER, None, None, spacer_small, None],
            [runWithId, BUTTON, editor.run_with,
                getImage(images.RUN_WITH), btn_size, tip_list[3]],
            [None, SPACER, None, None, spacer_large, None],
            [helpId, BUTTON, editor.help,
                getImage(images.HELP), btn_size, tip_list[4]],
            [None, SPACER, None, None, spacer_large, None],
            [goToId, BUTTON, editor.goToLine,
                getImage(images.GOTO), btn_size, tip_list[5]],
            [None, SPACER, None, None, spacer_large, None],
            [showId, BUTTON, editor.show,
                getImage(images.SHOW_HIDE), btn_size, tip_list[6]],
            [None, SPACER, None, None, spacer_large, None],
            [switchId, BUTTON, editor.switch_layout,
                getImage(images.LAYOUT), btn_size, tip_list[7]],
            [None, SPACER, None, None, spacer_large, None],
            [clearId, BUTTON, editor.clear,
                getImage(images.CLEAR_TEXT), btn_size, tip_list[8]]
            ]
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_list = []
        for id, widget, action, img, size, tip in widget_list:
            if widget == BUTTON:
                btn = wx.BitmapButton(self, id, img, size=size)
                #btn = wx.lib.buttons.GenBitmapButton(self, id, img, size=size)
                #btn = wx.Button(self, id, tip[:7], size=size)
                btn.SetToolTipString(tip)
                self.Bind(wx.EVT_BUTTON, action, btn)
                box.Add(btn, 0, wx.SHAPED)
                self.btn_list.append(btn)  # create a list for later reference
            elif widget == BITMAP:
                name = wx.StaticBitmap(self, -1, img, size=size)
                box.Add(name, 0, wx.SHAPED)
                self.btn_list.append(name)  # create lists for later reference
            elif widget == SPACER:
                box.Add(size, 0, wx.EXPAND)
        self.SetSizer(box)

        aTable = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('O'), openId),
                                    (wx.ACCEL_CTRL, ord('S'), saveId),
                                    (wx.ACCEL_CTRL, ord('R'), runId),
                                    (wx.ACCEL_NORMAL, wx.WXK_F5, runWithId),
                                    (wx.ACCEL_CTRL, ord('E'), clearId),
                                    (wx.ACCEL_NORMAL, wx.WXK_F1, helpId),
                                    (wx.ACCEL_CTRL, ord('H'), showId),
                                    (wx.ACCEL_CTRL, ord('G'), goToId),
                                    (wx.ACCEL_CTRL, ord('L'), switchId)])
        editor.SetAcceleratorTable(aTable)      
  

    def SelectLanguage(self):
        # recreate the list, using the new language
        tip_list = [_("Open Python file"), 
                         _("Save Python file"),
                         _("Run Python program"),
                        _("Run program with argument list"),
                        _("Help"),
                        _("Go to line number"),
                        _("Hide or show output window"),
                        _("Change layout"),
                         _("Clear text")]
        for i in range(len(tip_list)):
            self.btn_list[i].SetToolTipString(tip_list[i])

