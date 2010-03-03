# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    cpu.py - "Central Processing Unit" for the robot
    Version 0.9.8.5
    Author: Andre Roberge    Copyright  2005, 2006
    andre.roberge@gmail.com
"""
import sys

import wx
import time # for delay in robot movement
import dialogs
import event_manager
from translation import _
from world_creation import Visible_world

import parser
import test_import

class Singleton(object):
    """From the 2nd edition of the Python cookbook."""
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
        return cls._inst

class rur_program(Singleton):
    def myInit(self, parent, wld, WldDis, ProgEdit, r_dict):
        self.parent = parent
        self.world = wld
        self.WorldDisplay = WldDis
        self.ProgramEditor = ProgEdit
        self.robot_dict = r_dict
        self.isRunning = False
        self.isStepped = False
        self.isPaused = False
        self.stopped_by_user = False

    def restart(self, r_dict):
        code = self.ProgramEditor.GetText()
        no_error, mesg = parser.ParseProgram(code)
        if no_error:
            self.code = parser.FixLineEnding(code)
            self.lines_of_code = self.code.split('\n')
            code, flag = test_import.process_file(code)
        else:
            self.code = ""
            dialogs.messageDialog(mesg, _("Error found in your program."))
        self.robot_dict = r_dict
        self.isPaused = False
        self.stopped_by_user = False
        self.execute_program()

    def StopProgram(self):
        self.isPaused = False
        self.isStepped = False
        self.isRunning = False
        self.stopped_by_user = True

    def set_line_number(self, n, name='robot'): # obtained from my_trace
        try:
            robot = self.robot_dict[name]
        except KeyError:
            for key in self.robot_dict:
                name = key
                break
            if name == 'robot':  # no robot created yet
                self.ProgramEditor.highlight(n-1)
                return
            robot = self.robot_dict[name]
        self.ProgramEditor.highlight(n-1)
        self.ProgramEditor.Refresh()
        self.wait_update_refresh(robot, name)

    #--- Robot actions

    def turn_off(self, name='robot'):
        robot = self.robot_dict[name]
        robot.turn_off()  # will raise an exception to indicate normal end :-)

    def move(self, name='robot'):
        robot = self.robot_dict[name]
        x0, y0 = robot.getPos()
        robot.move()  # may raise an exception
        x1, y1 = robot.getPos()
        orientation = robot._getOrientation()
        colour = robot.trace_colour
        style = robot.trace_style
        robot.line_trace.append( (x0, y0, x1, y1, orientation, style, colour) )
        self.update_refresh(robot, name)

    def turn_left(self, name='robot'):
        robot = self.robot_dict[name]
        x, y = robot.getPos()
        orientation = robot._getOrientation()
        colour = robot.trace_colour
        style = robot.trace_style
        robot.line_trace.append( (x, y, x, y, orientation, style, colour) )
        robot.turn_left()  # must occur after line_trace.append
        self.update_refresh(robot, name)

    def turn_right(self, name='robot'):
        robot = self.robot_dict[name]
        x, y = robot.getPos()
        orientation = robot._getOrientation()
        colour = robot.trace_colour
        style = robot.trace_style
        robot.line_trace.append( (x, y, x, y, orientation, style, colour) )
        robot.turn_right()  # must occur after line_trace.append
        self.update_refresh(robot, name)

    def put_beeper(self, name='robot'):
        robot = self.robot_dict[name]
        robot.put_beeper() # may raise an exception
        self.update_refresh(robot, name)

    def pick_beeper(self, name='robot'):
        robot = self.robot_dict[name]
        robot.pick_beeper() # may raise an exception
        self.update_refresh(robot, name)

    def set_trace_style(self, style=1, colour='sea green', name='robot'):
        robot = self.robot_dict[name]
        robot.set_trace_style(style, colour)

    def set_delay(self, delay, name='robot'):
        robot = self.robot_dict[name]
        robot.delay = delay

    def roll_dice(self, n, name='robot'):
        robot = self.robot_dict[name]
        return robot.roll_dice(n)

    #--- tests
    def front_is_clear(self, name='robot'):
        robot = self.robot_dict[name]
        return robot.front_is_clear()

    def left_is_clear(self, name='robot'):
        robot = self.robot_dict[name]
        return robot.left_is_clear()

    def right_is_clear(self, name='robot'):
        robot = self.robot_dict[name]
        return robot.right_is_clear()

    def facing_north(self, name='robot'):
        robot = self.robot_dict[name]
        return robot.facing_north()

    def facing_west(self, name='robot'):
        robot = self.robot_dict[name]
        return robot.facing_west()

    def facing_east(self, name='robot'):
        robot = self.robot_dict[name]
        return robot.facing_east()

    def facing_south(self, name='robot'):
        robot = self.robot_dict[name]
        return robot.facing_south()

    def carries_beepers(self, name='robot'):
        robot = self.robot_dict[name]
        return robot.any_beepers_in_beeper_bag()

    def next_to_a_beeper(self, name='robot'):
        robot = self.robot_dict[name]
        return robot.next_to_a_beeper()

    #--- display controls

    def wait_update_refresh(self, robot, name):
        wx.Yield()
        if self.stopped_by_user:
            self.stopped_by_user = False
            mesg = _("Hey!  You stopped me!")
            raise dialogs.UserStopException(mesg)
            return
        if self.isStepped:
            self.isStepped = False
            self.isPaused = True
            arg = self.parent.status_bar.running_field, _("Program paused")
            event_manager.SendCustomEvent(self.parent, arg)
        while self.isPaused:
            wx.Yield()
            time.sleep(0.01)
            wx.Yield()
        self.update_refresh(robot, name)
        
    def update_refresh(self, robot, name):
        if 'robot' in self.robot_dict:
            arg = self.parent.status_bar.beeper_field, self.robot_dict['robot']._beeper_bag
            event_manager.SendCustomEvent(self.parent, arg)
        time.sleep(robot.delay)
        wx.Yield()
        self.world.DoDrawing()
        self.WorldDisplay.drawImage()
        if name:
            self.WorldDisplay.scrollWorld(name)
        self.WorldDisplay.Refresh()
        wx.Yield()

    def repeat(self, f, n):
        for i in range(n):
            f()

    def clear_trace(self):
        '''Removes the trails left by the robots.'''
        for name in self.robot_dict:
            self.robot_dict[name].line_trace = []

    def setBackgroundColour(self, colour):
        self.world.background_colour = wx.Brush(colour)
        self.world.background_images_created = False
        self.WorldDisplay.SetBackgroundColour(colour)

    def inputString(self, text=''):
        dlg = wx.TextEntryDialog(self.parent, text, _("Requesting a string"), '')
        if dlg.ShowModal() == wx.ID_OK:
            user_response = dlg.GetValue()
        dlg.Destroy()
        return user_response
    
    def inputInt(self, text=''):
        dlg = wx.TextEntryDialog(self.parent, text, _("Requesting an integer"), '')
        if dlg.ShowModal() == wx.ID_OK:
            user_response = dlg.GetValue()
        dlg.Destroy()
        return int(user_response)

    def my_trace(self, frame, event, arg):
        if event == "line":
            lineno = frame.f_lineno
            if str(frame.f_code).find("<string>") != -1:
                self.set_line_number(lineno)
        return self.my_trace

    def execute_program(self):
        self.clear_trace()
        if self.code=="":
            dialogs.messageDialog(_("All done!"),
                    _("No instruction to execute."))
            return
        self.parent.outputWindow.redirect()
        if 'robot' in self.parent.world.robot_dict:
            time_delay = [5, 1, 0.6, 0.3, 0.1, 0.06, 0.03, 0.01, 0.]
            selected = self.parent.slider_speed.GetValue()
            self.parent.world.robot_dict['robot'].delay = time_delay[selected]
        self.isRunning = True
        MyGlobals = {'move': self.move,
                     'turn_left': self.turn_left,
                     'pick_beeper': self.pick_beeper,
                     'put_beeper': self.put_beeper,
                     'set_trace_style': self.set_trace_style,
                     'set_delay': self.set_delay,
                     'RefurbishedRobot': RefurbishedRobot,
                     'UsedRobot' : UsedRobot,
                     'turn_off': self.turn_off,
                     'repeat': self.repeat,
                     'set_line_number': self.set_line_number,
                     'front_is_clear': self.front_is_clear,
                     'left_is_clear': self.left_is_clear,
                     'right_is_clear': self.right_is_clear,
                     'on_beeper': self.next_to_a_beeper,  # new, as suggested
                     'next_to_a_beeper': self.next_to_a_beeper, # compatibility with old code
                     'carries_beepers': self.carries_beepers,
                     'facing_north': self.facing_north,
                     'HitWallException': dialogs.HitWallException,
                     'setBackgroundColour': self.setBackgroundColour,
                     'input_int': self.inputInt,
                     'input_string': self.inputString}
        arg = self.parent.status_bar.running_field, _("Program is running")
        event_manager.SendCustomEvent(self.parent, arg)
        try:
            try:
                sys.settrace(self.my_trace)
                exec self.code in MyGlobals
                sys.settrace(None)
                self.world.DoDrawing()
                self.WorldDisplay.drawImage()
                self.WorldDisplay.Refresh()
                raise dialogs.NoTurnOffException(_("You forgot to turn me off!"))
            except dialogs.NoTurnOffException, mesg:
                dialogs.NoTurnOffError(mesg)
            except dialogs.NormalEnd, mesg:
                dialogs.NormalEndDialog(mesg)
            except dialogs.HitWallException, mesg:
                dialogs.DialogHitWallError(mesg)
            except dialogs.PickBeeperException, mesg:
                dialogs.DialogPickBeeperError(mesg)
            except dialogs.PutBeeperException, mesg:
                dialogs.DialogPutBeeperError(mesg)
            except dialogs.UserStopException, mesg:
                dialogs.UserStopError(mesg)
            except Exception, info:
                # There should be only two remaining possibilities...
                if "invalid syntax" in info:
                    info = _("Error found near line %s.")%info[1][1]
                    dialogs.messageDialog(info, _("Execution error"))
                else:
                    dialogs.messageDialog(
                    _("%s\nUnrecognized instruction.")%info, 
                               _("Execution error"))
        finally:
            self.isRunning = False
            self.isStepped = False
            self.isPaused = False
            end = self.parent.status_bar.running_field, _("Program not running")
            event_manager.SendCustomEvent(self.parent, end)
            self.parent.outputWindow.redirect('reset')
            sys.settrace(None)
            self.ProgramEditor.remove_highlight()
            self.ProgramEditor.Refresh()

class UsedRobot(object):
    def __init__(self, avenues=1, streets=1, orient_key='E',
                 beepers=0, name=None, colour='grey', parent = None):

        if parent == None:
            parent = Visible_world()
            
        true_robot = parent.addOneRobot(avenues=avenues,
                                        streets = streets,
                                        orient_key=orient_key,
                                        beepers=beepers,
                                        name = name,
                                        colour = colour)
        self.robot = parent.robot_dict[true_robot.name]
        self.name = true_robot.name
        self.program = rur_program()
        self.parent = parent
        self.parent.object_dict[self.name] = True
        self.program.wait_update_refresh(self.robot, self.name)
    def __del__(self):
        self.parent.object_dict[self.name] = False
    def move(self):
        self.program.move(self.name)
    def turn_off(self):
        self.program.turn_off(self.name)
    def turn_left(self):
        self.program.turn_left(self.name)
    def put_beeper(self):
        self.program.put_beeper(self.name)
    def pick_beeper(self):
        self.program.pick_beeper(self.name)
    def set_trace_style(self, style=1, colour='sea green'):
        self.program.set_trace_style(style, colour, self.name)
    def set_delay(self, delay=0.3):
        self.program.set_delay(delay, self.name)
    def front_is_clear(self):
        return self.program.front_is_clear(self.name)
    def facing_north(self):
        return self.program.facing_north(self.name)
    def carries_beepers(self):
        return self.program.carries_beepers(self.name)
    def on_beeper(self):  # new name
        return self.program.next_to_a_beeper(self.name)
    def next_to_a_beeper(self):  # old name kept for compatibility...
        return self.program.next_to_a_beeper(self.name)


class RefurbishedRobot(UsedRobot):
    def __init__(self, avenues=1, streets=1, orient_key='E',
                 beepers=0, name=None, colour='grey', parent=None):
        #UsedRobot.__init__(self, avenues=avenues, orient_key = orient_key,
        #        beepers=beepers, name=name, colour=colour, parent=parent)
        if parent == None:
            parent = Visible_world()
 
        true_robot = parent.addOneRobot(avenues=avenues,
                                        streets = streets,
                                        orient_key=orient_key,
                                        beepers=beepers,
                                        name = name,
                                        colour = colour,
                                        better = True)
        self.robot = parent.robot_dict[true_robot.name]
        self.name = true_robot.name
        self.program = rur_program()
        self.parent = parent
        self.parent.object_dict[self.name] = True
        self.program.wait_update_refresh(self.robot, self.name)

    def turn_right(self):
        self.program.turn_right(self.name)
    def facing_east(self):
        return self.program.facing_east(self.name)
    def facing_west(self):
        return self.program.facing_west(self.name)
    def facing_south(self):
        return self.program.facing_south(self.name)
    def roll_dice(self, n=6):
        return self.program.roll_dice(n, self.name)
