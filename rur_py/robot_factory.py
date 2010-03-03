# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    robot_factory.py - see description below
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005, 2006
    andre.roberge@gmail.com

robot_factory includes four classes:

    Robot_brain1(), which incorporates the basic logic of the robot, including
    a limited ability to sense the outside world.

    Robot_brain2(), which incorporates an "advanced" version, capable of more
    remote sensing ability, akin to Pattis's original Karel as well as
    turning right directly.

    Used_robot() subclasses Robot_brain1 and adds a body (i.e. physical
    representation: images for visual display, time delay for execution
    of movements, etc.)

    New_improved_robot() subclasses both Used_robot (for physical display) and
    Robot_brain2 for the improved logic.
    """

import dialogs
import images
from images import getImage
import random
from translation import _
import conf
from sound import play
import os

#---------------------------------------------------------------------------

class Robot_brain1(object):

    _directions = [ (0, 1), (-1, 0), (0, -1), (1, 0) ]
    _orient_dict = { 'E': 3, 'S': 2, 'W': 1, 'N': 0}

    def __init__(self, parent=None, avenues=1, streets=1,
                 orient_key = 'E', beepers=0):
        # East; value by default - tied to lessons
        self.parent = parent
        #--- Basic variables
        self._beeper_bag = beepers
        self._x = avenues
        self._y = streets
        self._facing = self._orient_dict[orient_key.upper()]

    #--- "public" getter
    def getPos(self):
        """ returns current robot position; intended to be
            accessed by user-defined program."""
        return self._x, self._y

    #--- "private" getters and setters
    def _setPos(self, x, y):
        """ sets robot position (teleport); intended to be
            accessed only through GUI, not by user-defined program."""
        self._x = x
        self._y = y

    def _getOrientation(self):
        """ returns orientation (0, 1, 2, 3); needed for drawing trace.
            Not intended to be accessed by user-defined program."""
        return self._facing

    def _getOrientationKey(self):
        """ returns orientation key ('N', 'E', 'S', W').
            Not intended to be accessed by user-defined program."""
        for key in self._orient_dict.keys():
            if self._orient_dict[key] == self._facing:
                return key

    def _getInfoTuple(self):
        """ returns (avenue, street, orientation, beepers).
            Not intended to be accessed by user-defined program."""
        return self._x, self._y, self._getOrientationKey(), self._beeper_bag

    def _getInfoString(self):
        """ returns (avenue, street, orientation, beepers).
            Not intended to be accessed by user-defined program."""
        return str(self._getInfoTuple())

    #--- built-in tests

    def front_is_clear(self):
        ''' True if no wall or border in front of robot'''
        col = 2*self._x - 1
        row = 2*self._y - 1
        xx, yy = self._directions[self._facing]
        return self.parent.isClear(col+xx, row+yy)

    def facing_north(self):
        ''' True if Robot facing north'''
        if self._facing == 0:
            return True
        else:
            return False

    def any_beepers_in_beeper_bag(self):
        '''True if some beepers are left in Robot's bag'''
        if self._beeper_bag == 0:
            return False
        else:
            return True

    def next_to_a_beeper(self):
        '''True if beepers are present at current robot position.'''
        if (self._x, self._y) in self.parent.beepers_dict:
            return True
        else:
            return False

    def left_is_clear(self):
        '''Returns True if no walls or borders are to the immediate left
           of the robot.'''
        col = 2*self._x - 1
        row = 2*self._y - 1
        facing = self._facing + 1
        facing %= 4
        xx, yy = self._directions[facing]
        if (col+xx, row+yy) in self.parent.walls_list:
            return False
        if (col+xx, row+yy) in self.parent.borders:
            return False
        else:
            return True

    def right_is_clear(self):
        '''Returns True if no walls or borders are to the immediate
           right of the robot.'''
        col = 2*self._x - 1
        row = 2*self._y - 1
        facing = self._facing + 3
        facing %= 4
        xx, yy = self._directions[facing]
        if (col+xx, row+yy) in self.parent.walls_list:
            return False
        if (col+xx, row+yy) in self.parent.borders:
            return False
        else:
            return True

    #--- Actions

    def move(self):
        '''Robot moves one street/avenue in direction where it is facing'''
        if self.front_is_clear():
            xx, yy = self._directions[self._facing]
            self._x += xx
            self._y += yy
            if self.next_to_a_beeper():
                self.at_beeper(self._x, self._y)
        else:
            mesg = _("""That move really hurt!
Please, make sure that there is no wall in front of me!""")
            raise dialogs.HitWallException(mesg)

    def turn_off(self):
        mesg = _("I obey your command:\n turning myself off.")
        raise dialogs.NormalEnd(mesg)

    def turn_left(self):
        '''Robot turns left by 90 degrees.'''
        self._facing += 1
        self._facing %= 4

    def put_beeper(self):
        '''Robot put one beeper down at current location.'''
        if self.any_beepers_in_beeper_bag():
            self._beeper_bag -= 1
            self.parent.addOneBeeper(self._x, self._y)
        else:
            mesg = _("put_beeper() failed.\n I am not carrying any beepers.")
            raise dialogs.PutBeeperException(mesg)

    def pick_beeper(self):
        '''Robot picks one beeper up at current location.'''
        if self.next_to_a_beeper():
            self.parent.removeOneBeeper(self._x, self._y)
            self._beeper_bag += 1
        else:
            mesg = _("""pick_beeper failed.
I must be next to a beeper before I can pick it up.""")
            raise dialogs.PickBeeperException(mesg)

    def at_beeper(self, x, y):
        '''Notifies interested parties about robot
        being at a beeper.
        '''
        onbeepersound = os.path.join(conf.getSettings().SOUNDS_DIR, 'beep.wav')
        if os.path.isfile(onbeepersound):
            play(onbeepersound)

class Robot_brain2(Robot_brain1):
    def __init__(self, parent=None, avenues=1, streets=1, orient_key = 'E',
                 beepers=0):
        Robot_brain1.__init__(self, parent, avenues, streets,
                              orient_key, beepers)

    #--- Additional built-in tests

    def facing_east(self):
        if self._facing == 3:
            return True
        else:
            return False

    def facing_south(self):
        if self._facing == 2:
            return True
        else:
            return False

    def facing_west(self):
        if self._facing == 1:
            return True
        else:
            return False

    #--- Additional action
    def turn_right(self):
        self._facing += 3
        self._facing %= 4

    def roll_dice(self, n=6):
        return random.randint(1, n)



class Used_robot(Robot_brain1):
    """ Adds physical attributes """

    def __init__(self, avenues=1, streets=1, orient_key = 'E',
                 beepers=0, name = 'robot', colour = 'grey', parent=None):
        Robot_brain1.__init__(self, parent, avenues, streets,
                              orient_key, beepers)

        settings = conf.getSettings()
        
        self._delay = 0.3
        self.name = name
        self.colour = colour.lower()

        # The following are used to follow the robot trail
        self.line_trace = []
        self.set_trace_style(1, "sea green")  # default

    #--- Robot images
        # create a list of four objects
        if self.colour == 'yellow':
            self._image = [getImage(images.YELLOW_ROBOT_N), getImage(images.YELLOW_ROBOT_W),
                       getImage(images.YELLOW_ROBOT_S), getImage(images.YELLOW_ROBOT_E)]
        elif self.colour == 'blue':
            self._image = [getImage(images.BLUE_ROBOT_N), getImage(images.BLUE_ROBOT_W),
                       getImage(images.BLUE_ROBOT_S), getImage(images.BLUE_ROBOT_E)]
        elif self.colour == 'light blue':
            self._image = [getImage(images.LIGHT_BLUE_ROBOT_N), getImage(images.LIGHT_BLUE_ROBOT_W),
                       getImage(images.LIGHT_BLUE_ROBOT_S), getImage(images.LIGHT_BLUE_ROBOT_E)]
        elif self.colour == 'purple':
            self._image = [getImage(images.PURPLE_ROBOT_N), getImage(images.PURPLE_ROBOT_W),
                       getImage(images.PURPLE_ROBOT_S), getImage(images.PURPLE_ROBOT_E)]
        elif self.colour == 'green':
            self._image = [getImage(images.GREEN_ROBOT_N), getImage(images.GREEN_ROBOT_W),
                       getImage(images.GREEN_ROBOT_S), getImage(images.GREEN_ROBOT_E)]
        else:
            self._image = [getImage(images.GREY_ROBOT_N), getImage(images.GREY_ROBOT_W),
                       getImage(images.GREY_ROBOT_S), getImage(images.GREY_ROBOT_E)]

        self.imageOffset = (settings.SCREEN[7], settings.SCREEN[8])

        # image size (x, y) [all images equal]; for use in automatic scrolling
        self._image_size = self._image[0].GetWidth(), \
                           self._image[0].GetHeight()
        ## Note: for some reason, GetSize() did not work  using
        ## wxPython 2.4, which is why I used GetWidth() and GetHeight()

        # selecting the right image based on initial orientation
        self.robot_image = self._image[self._facing]

    #--- Action over-riden to handle images
    def turn_left(self):
        '''Robot turns left by 90 degrees, and image is updated.'''
        Robot_brain1.turn_left(self)
        self.robot_image = self._image[self._facing]

    def set_trace_style(self, style, colour = "sea green"):
        if style == 1:
           self.trace_offset = [(3, 3), (3, -3), (-3, -3), (-3, 3)]
           self.trace_width = 1
        elif style == 2:
           self.trace_offset = [(5, 5), (5, -5), (-5, -5), (-5, 5)]
           self.trace_width = 1
        elif style == 3:
           self.trace_offset = [(3, 3), (3, -3), (-3, -3), (-3, 3)]
           self.trace_width = 3
        elif style == 4:
           self.trace_offset = [(5, 5), (5, -5), (-5, -5), (-5, 5)]
           self.trace_width = 3
        elif style == 5:
            self.trace_offset = [(0, 0), (0, 0), (0, 0), (0, 0)]
            self.trace_width = 3
        else:
            self.trace_offset = [(0, 0), (0, 0), (0, 0), (0, 0)]
            self.trace_width = 0

        self.trace_style = style
        self.trace_colour = colour

    def get_trace_style(self, style):
        if style == 1:
           trace_offset = [(3, 3), (3, -3), (-3, -3), (-3, 3)]
           trace_width = 1
        elif style == 2:
           trace_offset = [(5, 5), (5, -5), (-5, -5), (-5, 5)]
           trace_width = 1
        elif style == 3:
           trace_offset = [(3, 3), (3, -3), (-3, -3), (-3, 3)]
           trace_width = 3
        elif style == 4:
           trace_offset = [(5, 5), (5, -5), (-5, -5), (-5, 5)]
           trace_width = 3
        elif style == 5:
            trace_offset = [(0, 0), (0, 0), (0, 0), (0, 0)]
            trace_width = 3
        else:
            trace_offset = [(0, 0), (0, 0), (0, 0), (0, 0)]
            trace_width = 0
        return trace_width, trace_offset

    def set_delay(self, delay):
        '''Sets the delay value between robot actions.'''
        if delay >= 0 and delay <= 10:
            self._delay = delay
        else:
            mesg = _("""Setting delay failed.
Accepted values are between 0 and 10.""")
            dialogs.messageDialog(mesg, _("Error"))

    def get_delay(self):
        return self._delay

    delay = property(get_delay, set_delay, None, "Time between robot actions")

class New_improved_robot(Robot_brain2):
    """ Adds physical attributes and better logic."""
    def __init__(self, avenues=1, streets=1, orient_key = 'E',
                 beepers=0, name = 'robot', colour = 'grey', parent=None):
        Robot_brain2.__init__(self, parent, avenues, streets,
                              orient_key, beepers)
        self._delay = 0.3
        self.name = name
        self.colour = colour.lower()

        # The following are used to follow the robot trail
        self.line_trace = []
        self.set_trace_style(1, "sea green")  # default
    #--- Robot images
        # create a list of four objects
        if self.colour == 'yellow':
            self._image = [getImage(images.YELLOW_ROBOT_N), getImage(images.YELLOW_ROBOT_W),
                       getImage(images.YELLOW_ROBOT_S), getImage(images.YELLOW_ROBOT_E)]
        elif self.colour == 'blue':
            self._image = [getImage(images.BLUE_ROBOT_N), getImage(images.BLUE_ROBOT_W),
                       getImage(images.BLUE_ROBOT_S), getImage(images.BLUE_ROBOT_E)]
        elif self.colour == 'light blue':
            self._image = [getImage(images.LIGHT_BLUE_ROBOT_N), getImage(images.LIGHT_BLUE_ROBOT_W),
                       getImage(images.LIGHT_BLUE_ROBOT_S), getImage(images.LIGHT_BLUE_ROBOT_E)]
        elif self.colour == 'purple':
            self._image = [getImage(images.PURPLE_ROBOT_N), getImage(images.PURPLE_ROBOT_W),
                       getImage(images.PURPLE_ROBOT_S), getImage(images.PURPLE_ROBOT_E)]
        elif self.colour == 'green':
            self._image = [getImage(images.GREEN_ROBOT_N), getImage(images.GREEN_ROBOT_W),
                       getImage(images.GREEN_ROBOT_S), getImage(images.GREEN_ROBOT_E)]
        else:
            self._image = [getImage(images.GREY_ROBOT_N), getImage(images.GREY_ROBOT_W),
                       getImage(images.GREY_ROBOT_S), getImage(images.GREY_ROBOT_E)]

        self.imageOffset = (settings.SCREEN[7], settings.SCREEN[8])

        # image size (x, y) [all images equal]; for use in automatic scrolling
        self._image_size = self._image[0].GetWidth(), \
                           self._image[0].GetHeight()
        ## Note: for some reason, GetSize() did not work  using
        ## wxPython 2.4, which is why I used GetWidth() and GetHeight()

        # selecting the right image based on initial orientation
        self.robot_image = self._image[self._facing]

    #--- Action over-riden to handle images
    def turn_left(self):
        '''Robot turns left by 90 degrees, and image is updated.'''
        Robot_brain1.turn_left(self)
        self.robot_image = self._image[self._facing]

    def set_trace_style(self, style, colour = "sea green"):
        if style == 1:
           self.trace_offset = [(3, 3), (3, -3), (-3, -3), (-3, 3)]
           self.trace_width = 1
        elif style == 2:
           self.trace_offset = [(5, 5), (5, -5), (-5, -5), (-5, 5)]
           self.trace_width = 1
        elif style == 3:
           self.trace_offset = [(3, 3), (3, -3), (-3, -3), (-3, 3)]
           self.trace_width = 3
        elif style == 4:
           self.trace_offset = [(5, 5), (5, -5), (-5, -5), (-5, 5)]
           self.trace_width = 3
        elif style == 5:
            self.trace_offset = [(0, 0), (0, 0), (0, 0), (0, 0)]
            self.trace_width = 3
        else:
            self.trace_offset = [(0, 0), (0, 0), (0, 0), (0, 0)]
            self.trace_width = 0

        self.trace_style = style
        self.trace_colour = colour

    def get_trace_style(self, style):
        if style == 1:
           trace_offset = [(3, 3), (3, -3), (-3, -3), (-3, 3)]
           trace_width = 1
        elif style == 2:
           trace_offset = [(5, 5), (5, -5), (-5, -5), (-5, 5)]
           trace_width = 1
        elif style == 3:
           trace_offset = [(3, 3), (3, -3), (-3, -3), (-3, 3)]
           trace_width = 3
        elif style == 4:
           trace_offset = [(5, 5), (5, -5), (-5, -5), (-5, 5)]
           trace_width = 3
        elif style == 5:
            trace_offset = [(0, 0), (0, 0), (0, 0), (0, 0)]
            trace_width = 3
        else:
            trace_offset = [(0, 0), (0, 0), (0, 0), (0, 0)]
            trace_width = 0
        return trace_width, trace_offset

    def set_delay(self, delay):
        '''Sets the delay value between robot actions.'''
        if delay >= 0 and delay <= 10:
            self._delay = delay
        else:
            mesg = _("""Setting delay failed.
Accepted values are between 0 and 10.""")
            dialogs.messageDialog(mesg, _("Error"))

    def get_delay(self):
        return self._delay

    delay = property(get_delay, set_delay, None, "Time between robot actions")


    # TODO: design "better looking" images for this robot.
    #--- Action over-riden to handle images
    def turn_right(self):
        '''Robot turns right by 90 degrees, and image is updated.'''
        Robot_brain2.turn_right(self)
        self.robot_image = self._image[self._facing]
