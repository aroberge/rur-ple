# -*- coding: utf-8
# RUR-PLE: Roberge's Used Robot - a Python Learning Environment
#    images.py - Contains all images for RUR-PLE
#    Version 0.8.7
#    Author: Andre Roberge    Copyright  2005
#    andre.roberge@gmail.com

import os
import wx
import conf

# robots
GREY_ROBOT_S = 'robot_s.png'
GREY_ROBOT_N = 'robot_n.png'
GREY_ROBOT_E = 'robot_e.png'
GREY_ROBOT_W = 'robot_w.png'

YELLOW_ROBOT_S = 'yellow_robot_s.png'
YELLOW_ROBOT_N = 'yellow_robot_n.png'
YELLOW_ROBOT_E = 'yellow_robot_e.png'
YELLOW_ROBOT_W = 'yellow_robot_w.png'

GREEN_ROBOT_S = 'green_robot_s.png'
GREEN_ROBOT_N = 'green_robot_n.png'
GREEN_ROBOT_E = 'green_robot_e.png'
GREEN_ROBOT_W = 'green_robot_w.png'

BLUE_ROBOT_S = 'blue_robot_s.png'
BLUE_ROBOT_N = 'blue_robot_n.png'
BLUE_ROBOT_E = 'blue_robot_e.png'
BLUE_ROBOT_W = 'blue_robot_w.png'

LIGHT_BLUE_ROBOT_S = 'light_blue_robot_s.png'
LIGHT_BLUE_ROBOT_N = 'light_blue_robot_n.png'
LIGHT_BLUE_ROBOT_E = 'light_blue_robot_e.png'
LIGHT_BLUE_ROBOT_W = 'light_blue_robot_w.png'

PURPLE_ROBOT_S = 'purple_robot_s.png'
PURPLE_ROBOT_N = 'purple_robot_n.png'
PURPLE_ROBOT_E = 'purple_robot_e.png'
PURPLE_ROBOT_W = 'purple_robot_w.png'

#== browser
OPEN_HTML = 'folder_html.png'
HOME = 'folder_home.png'
BACK = 'back.png'
FORWARD = 'forward.png'
LANGUAGES = 'languages.png'

#== Robot world
RUN_PROGRAM = 'run1.png'
SPEED = 'speed.png'
STEP = 'step.png'
STOP = 'stop.png'
PAUSE = 'pause.png'
WALL = 'wall.png'
HIGHLIGHT = 'highlight.png'
SHOW_WORLD_FILE = 'show_world_file.png'
OPEN_PROGRAM = 'open_program.png'
SAVE_PROGRAM = 'save_program.png'
OPEN_WORLD = 'open_world.png'
SAVE_WORLD = 'save_world.png'
EDIT_WORLD = 'edit_world.png'
RESET_WORLD = 'reset_world.png'
ADD_REMOVE_ROBOT = 'add_robot.png'
BEEPERS_ROBOT = 'beepers.png'
RESIZE = 'resize.png'
NEW_ROBOT_IMAGES = 'new_images.png'

#== Python editor
OPEN_PYTHON = 'open_py.png'
SAVE_PYTHON = 'save_py.png'
CLEAR_TEXT = 'clear_text.png'
RUN_WITH = 'run_with.png'
HELP = 'help.png'
GOTO = 'goto.png'
LAYOUT = 'layout.png'
SHOW_HIDE = 'show_hide.png'

# others
SPLASH_SCREEN = 'splash_screen.png'
ICON = 'rur16x16.png'
HIT_WALL_IMAGE = 'ouch.png'
MINI_SPLASH = 'splash_screen_small.png'

settings = conf.getSettings()

_imageBitmap = {}

def getImage(imagePath):
    '''
    '''
    global _imageBitmap, settings
    
    if not imagePath in _imageBitmap:
        _imageBitmap[imagePath] = wx.Image(
            os.path.join(settings.IMAGE_DIR, imagePath),
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    return _imageBitmap[imagePath]

def setImage(imagePath, image):
    '''
    '''
    _imageBitmap[imagePath] = image
