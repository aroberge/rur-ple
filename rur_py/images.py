# -*- coding: utf-8
# RUR-PLE: Roberge's Used Robot - a Python Learning Environment
#    images.py - Contains all images for RUR-PLE
#    Version 0.8.7
#    Author: Andre Roberge    Copyright  2005
#    andre.roberge@gmail.com

import misc
import wx

try:
    GREY_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREY_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREY_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREY_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading robot_?.png in RobotFactory.py"

try:
    YELLOW_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/yellow_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    YELLOW_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/yellow_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    YELLOW_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/yellow_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    YELLOW_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/yellow_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading yellow_robot_?.png in RobotFactory.py"

try:
    GREEN_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/green_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREEN_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/green_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREEN_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/green_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREEN_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/green_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading green_robot_?.png in RobotFactory.py"

try:
    BLUE_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/blue_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    BLUE_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/blue_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    BLUE_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/blue_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    BLUE_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/blue_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading blue_robot_?.png in RobotFactory.py"

try:
    LIGHT_BLUE_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/light_blue_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    LIGHT_BLUE_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/light_blue_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    LIGHT_BLUE_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/light_blue_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    LIGHT_BLUE_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/light_blue_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading light_blue_robot_?.png in RobotFactory.py"

try:
    PURPLE_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/purple_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PURPLE_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/purple_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PURPLE_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/purple_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PURPLE_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/purple_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading purple_robot_?.png in RobotFactory.py"

try:
    SPLASH_SCREEN = wx.Image(misc.IMAGE_DIR+'/splash_screen.png',
                  wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print "%s\nProblem loading splash_screen.png in start.py"%info


try:
    ICON = wx.Image(misc.IMAGE_DIR+'/rur16x16.png',
                  wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print "Problem loading rur16x16.png in start.py"

try:
    HIT_WALL_IMAGE = wx.Image(misc.IMAGE_DIR+'/ouch.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading ouch.png in dialogs.py"

try:
    MINI_SPLASH = wx.Image(misc.IMAGE_DIR+'/splash_screen_small.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading splash_screen_small.png in dialogs.py"


try:
    EDIT_WORLD = wx.Image(misc.IMAGE_DIR+'/edit_world.png',
                                wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print "Problem loading edit_world.png in WorldDisplay.py"

try:
    #== browser
    OPEN_HTML = wx.Image(misc.IMAGE_DIR+'/folder_html.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    HOME = wx.Image(misc.IMAGE_DIR+'/folder_home.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    BACK = wx.Image(misc.IMAGE_DIR+'/back.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    FORWARD = wx.Image(misc.IMAGE_DIR+'/forward.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    LANGUAGES = wx.Image(misc.IMAGE_DIR+'/languages.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    #== Robot world
    RUN_PROGRAM = wx.Image(misc.IMAGE_DIR+'/run1.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    SPEED = wx.Image(misc.IMAGE_DIR+'/speed.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    STEP = wx.Image(misc.IMAGE_DIR+'/step.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    STOP = wx.Image(misc.IMAGE_DIR+'/stop.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PAUSE = wx.Image(misc.IMAGE_DIR+'/pause.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    SHOW_WORLD_FILE = wx.Image(misc.IMAGE_DIR+'/show_world_file.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    HIGHLIGHT = wx.Image(misc.IMAGE_DIR+'/highlight.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    OPEN_PROGRAM = wx.Image(misc.IMAGE_DIR+'/open_program.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    SAVE_PROGRAM = wx.Image(misc.IMAGE_DIR+'/save_program.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    OPEN_WORLD = wx.Image(misc.IMAGE_DIR+'/open_world.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    SAVE_WORLD = wx.Image(misc.IMAGE_DIR+'/save_world.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    WALL = wx.Image(misc.IMAGE_DIR+'/wall.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    RESET_WORLD = wx.Image(misc.IMAGE_DIR+'/reset_world.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    ADD_REMOVE_ROBOT = wx.Image(misc.IMAGE_DIR+'/add_robot.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    BEEPERS_ROBOT = wx.Image(misc.IMAGE_DIR+'/beepers.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    RESIZE = wx.Image(misc.IMAGE_DIR+'/resize.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    NEW_ROBOT_IMAGES = wx.Image(misc.IMAGE_DIR+'/new_images.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    #== Python editor
    OPEN_PYTHON = wx.Image(misc.IMAGE_DIR+'/open_py.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    SAVE_PYTHON = wx.Image(misc.IMAGE_DIR+'/save_py.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    CLEAR_TEXT = wx.Image(misc.IMAGE_DIR+'/clear_text.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    RUN_WITH = wx.Image(misc.IMAGE_DIR+'/run_with.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    HELP = wx.Image(misc.IMAGE_DIR+'/help.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GOTO = wx.Image(misc.IMAGE_DIR+'/goto.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    LAYOUT = wx.Image(misc.IMAGE_DIR+'/layout.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    SHOW_HIDE = wx.Image(misc.IMAGE_DIR+'/show_hide.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading button images in RobotFactory.py"
