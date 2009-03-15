""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    bouton.py - Defines "menu choices" through buttons
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com
"""

import wx
import images
from rur_py.translation import _

class rurChoiceWindow(wx.ScrolledWindow):
    def __init__(self, parent, great_grand_parent):
        wx.ScrolledWindow.__init__(self, parent, -1)

        self.ggp = great_grand_parent    # rurApp instance!
        btn_size = (32, 32)
        self.ggp.BUTTON_HEIGHT = btn_size[0] + 8
        spacer_small = (4, 4)
        spacer_large = (25, 25)

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
                          "Load new images for robot"]

        button_list1 = [
            [wx.NewId(), True, self.ggp.OpenProgramFile, images.OPEN_PROGRAM,
                btn_size, tip_list[0]],
            [wx.NewId(), True, self.ggp.SaveProgramFile, images.SAVE_PROGRAM,
                btn_size, tip_list[1]],
            [None,      False, None, None, spacer_large, None],
            [wx.NewId(), True, self.ggp.OpenWorldFile, images.OPEN_WORLD,
                btn_size, tip_list[2]],
            [wx.NewId(), True, self.ggp.SaveWorldFile, images.SAVE_WORLD,
                btn_size, tip_list[3]],
            [wx.NewId(), True, self.ggp.ResetWorld, images.RESET_WORLD,
                btn_size, tip_list[4]],
            [None,      False, None, None, spacer_large, None],
            [wx.NewId(), True, self.ggp.RunProgram, images.RUN_PROGRAM,
                btn_size, tip_list[5]],
            [wx.NewId(), True, self.ggp.Step, images.STEP, btn_size, 
                tip_list[6]],
            [wx.NewId(), True, self.ggp.Pause, images.PAUSE, btn_size, 
                tip_list[7]],
            [wx.NewId(), True, self.ggp.StopProgram, images.STOP, btn_size, 
                tip_list[8]],
            [None,      False, None, None, spacer_large, None],
            [wx.NewId(), True, None, images.SPEED, btn_size, tip_list[9]]
            ]

        button_list2 = [
            [None,      False, None, None, spacer_large, None],
            [wx.NewId(), True, self.ggp.EditWalls, images.WALL, btn_size, 
                tip_list[10]],
            [wx.NewId(), True, self.ggp.ResizeWorld, images.RESIZE, btn_size, 
                tip_list[11]],
            [wx.NewId(), True, self.ggp.BeepersToRobot, images.BEEPERS_ROBOT,
                btn_size, tip_list[12]],
            [None,      False, None, None, spacer_large, None],
            [wx.NewId(), True, self.ggp.AddRemoveRobot, images.ADD_REMOVE_ROBOT,
                btn_size, tip_list[13]],
            [None,      False, None, None, spacer_large, None],
            [wx.NewId(), True, self.ggp.ToggleWorldWindow, images.SHOW_WORLD_FILE,
                btn_size, tip_list[14]],
            [None,      False, None, None, spacer_large, None],
            [wx.NewId(), True, self.ggp.load_images, images.NEW_ROBOT_IMAGES,
                btn_size, tip_list[15]],
            ]
        box = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_list = []
        for id, button, action, img, size, tip in button_list1:
            if button:
                name = wx.lib.buttons.GenBitmapButton(self, id, img, size=size)
                name.SetToolTipString(tip)
                wx.EVT_BUTTON(self, id, action)
                box.Add(name, 0, wx.SHAPED)
                self.btn_list.append(name)  # create lists for later reference
            else:
                box.Add(size, 0, wx.EXPAND)

        min_speed = 0
        max_speed = 8
        default_speed = 3
        self.ggp.slider_speed = wx.Slider(
            # id, value, min, max, (x, y), (length, height)
            self, -1, default_speed, min_speed, max_speed,
            (-1, -1), (-1, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS #| wx.SL_LABELS
            )
        self.ggp.slider_speed.SetTickFreq(1, 1)
        self.ggp.slider_speed.SetToolTipString(tip_list[9])
        box.Add(self.ggp.slider_speed, 0, wx.SHAPED)
        self.ggp.slider_speed.SetFocus()  # to make it same colour as background

        for id, button, action, img, size, tip in button_list2:
            if button:
                name = wx.lib.buttons.GenBitmapButton(self, id, img, size=size)
                name.SetToolTipString(tip)
                wx.EVT_BUTTON(self, id, action)
                box.Add(name, 0, wx.SHAPED)
                self.btn_list.append(name)  # create lists for later reference
            else:
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
                          "Load new images for robot"]
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

        # temporary list until images are created
        labels = ["Help", "Run with", "Go to", "Hide/show", "Layout"]
        
        button_list = [
            [None, False, None, None, spacer_small, None],
            [openId, True, editor.openFile,
                images.OPEN_PYTHON, btn_size, tip_list[0]],
            [None, False, None, None, spacer_small, None],
            [saveId, True, editor.saveFile,
                images.SAVE_PYTHON, btn_size, tip_list[1]],
            [None, False, None, None, spacer_large, None],
            [runId, True, editor.run,
                images.RUN_PROGRAM, btn_size, tip_list[2]],
            [None, False, None, None, spacer_small, None],
            [runWithId, True, editor.run_with,
                images.RUN_WITH, btn_size, tip_list[3]],
            [None, False, None, None, spacer_large, None],
            [helpId, True, editor.help,
                images.HELP, btn_size, tip_list[4]],
            [None, False, None, None, spacer_large, None],
            [goToId, True, editor.goToLine,
                images.GOTO, btn_size, tip_list[5]],
            [None, False, None, None, spacer_large, None],
            [showId, True, editor.show,
                images.SHOW_HIDE, btn_size, tip_list[6]],
            [None, False, None, None, spacer_large, None],
            [switchId, True, editor.switch_layout,
                images.LAYOUT, btn_size, tip_list[7]],
            [None, False, None, None, spacer_large, None],
            [clearId, True, editor.clear,
                images.CLEAR_TEXT, btn_size, tip_list[8]]
            ]
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_list = []
        for id, button, action, img, size, tip in button_list:
            if button:
                btn = wx.BitmapButton(self, id, img, size=size)
                #btn = wx.lib.buttons.GenBitmapButton(self, id, img, size=size)
                #btn = wx.Button(self, id, tip[:7], size=size)
                btn.SetToolTipString(tip)
                self.Bind(wx.EVT_BUTTON, action, btn)
                box.Add(btn, 0, wx.SHAPED)
                self.btn_list.append(btn)  # create a list for later reference
            else:
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
