# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    world_creation.py - See description below
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com

    world_creation.py includes two classes:

    World(), which incorporates the logic of the world in which the robot moves.

    Visible_world() which is derived from World() and contains all the
    visual representation (colours and sizes of walls, beepers, etc.).
    """
import wx
import conf
from translation import _
import robot_factory
import conf

#---------------------------------------------------------------------------


class Singleton(object):
    """From the 2nd edition of the Python cookbook."""
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
        return cls._inst

class World(Singleton):
    """ This class defines the world's logic.  The world representation on
        the computer screen is as follows:
                  11111111112
        012345678901234567890
        #####################0
        #                   #1
        # # # # # # # # # # #2
        #                   #3
        # #@#@# # # # # # # #4
        # @   @             #5
        # # # # # # # # # # #6
        #                   #7
        # # # # # # # # # # #8
        #                   #9
        # # # # # # # # # # #10
        #                   #11
        #####################12

        where "#" represents a built-in "tile"  (outside wall or
        "anchor point" from which a wall is attached) and "@" represents
        a user-added tile/wall.

        A robot is allowed to move horizontally or vertically along "streets"
        or "avenues".  In the above drawing, street 1 would be on row 11,
        street 2 would be on [screen ]row 9, etc.
        (the row numbers are on the right of the drawing).
        The column/row above follows the usual computer graphical
        convention, with the origin at the TOP left corner.
        Avenues/streets follow the usual mathematical convention with the
        origin at the BOTTOM left corner.
        Thus, avenue 1 would be on column 1, avenue 2 would be on column 3, etc.

        In general, we will have avenue n on column 2n-1.
        Similarly, we will have street n on [screen] row (max_row) - (2n-1).

        User-defined walls can only occur on (even row, odd column) or
        (odd row, even column).  For example, in the above diagram, we have
        user-defined walls, indicated by @, on
        (5, 2), (5, 6), (4, 3) and (4, 5).

        Outside walls are on column 0 and some even-numbered column, as well
        as on row 0 and some even-numbered row.  We thus have an odd number
        of both rows and columns.
        """


    walls_list = []
    borders = []
    beepers_dict = {}
    def __init__(self, avenues=10, streets=10, walls = [], beepers = {},
                  robot = {}):
        self.av = avenues
        self.st = streets
        self.robot_dict = robot
        self.robot_number = 0
        self.num_cols = 2*avenues + 1
        self.num_rows = 2*streets + 1
        World.walls_list = walls
        for (col, row) in World.walls_list:
            if not (col+row)%2:   # old "debug" statement; kept in case
                print "Wall in impossible position"
                print "col =", col, "row =", row
                print "Please contact manufacturer (or check your input file)."
        World.beepers_dict = beepers
        self.setBorders()

    def setBorders(self):
        """ setBorder(self): The world is surrounded by a continuous wall.
            This function sets the corresponding "wall list" or "border"
            based on the world's dimensions."""
        for col in range(1, self.num_cols-1, 2):
            if (col, 0) not in World.borders:
                World.borders.append( (col, 0) )
            if (col, self.num_rows) not in World.borders:
                World.borders.append( (col, self.num_rows-1) )
        for row in range(1, self.num_rows-1, 2):
            if (0, row) not in World.borders:
                World.borders.append( (0, row) )
            if (self.num_cols, row) not in World.borders:
                World.borders.append( (self.num_cols-1, row) )

    def resetDimensions(self, avenues=10, streets=10):
        """ resetDimensions(self, avenues=10, streets=10):
            This is to allow changing world dimensions without
            having to restart the program.  It also removes
            all user-defined walls and beepers."""
        self.av = avenues
        self.st = streets
        self.num_cols = 2*avenues + 1
        self.num_rows = 2*streets + 1
        World.borders = []
        World.walls_list = []
        World.beepers_dict = {}
        self.setBorders()

    def ToggleWalls(self, col, row):
        """ ToggleWalls(self, col, row):
            This function is intended for adding or removing a
            wall from a GUI world editor."""
        if (col+row)%2 :  # safety check
            if (col, row) in World.walls_list: #toggle value
                World.walls_list.remove((col, row))
            else:
                World.walls_list.append((col, row))
        else:     # "old debug" statement; kept in case
            print "Wall in impossible position."
            print "col =", col, "row =", row
            print "Please contact manufacturer with bug report."

    def setBeepers(self, (av, st), nb):
        """ setBeepers(self, (av, st), nb):
            This function is intended to set the number of beepers from a
            GUI world editor."""
        if (av, st) in World.beepers_dict:
            if nb == 0:
                del World.beepers_dict[(av, st)]
            else:
                World.beepers_dict[(av, st)] = nb
        elif nb > 0:
            World.beepers_dict[(av, st)] = nb
        else:     # old "debug" statement; kept in case
            pass
            #print "Attempting to set the number of beepers to a negative "
            #print "value using setBeepers() in World().  This should never "
            #print "happen.  Please contact manufacturer with bug report."

    def isClear(self, col, row):
        """ isClear(self, col, row):
            This function informs the user (robot) whether or not a given
            combination of (col, row) is Clear i.e. if there is no wall
            or border there."""
        if (col, row) in World.walls_list:
            return False
        if (col, row) in World.borders:
            return False
        else:
            return True

    def addOneBeeper(self, av, st):
        """ addOneBeeper(self, av, st):
            This function is intended for adding a single
            beeper in the world from a robot put_beeper() command."""
        if (av, st) in World.beepers_dict:
            World.beepers_dict[(av, st)] += 1
        else:
            World.beepers_dict[(av, st)] = 1

    def removeOneBeeper(self, av, st):
        """ removeOneBeeper(self, av, st):
            This function is intended for removing a single
            beeper in the world from a robot pick_beeper() command.
            The robot command should first check to make sure there is
            a beeper to be removed by using getBeepers."""
        if (av, st) in World.beepers_dict:
            World.beepers_dict[(av, st)] -= 1
            if World.beepers_dict[(av, st)] == 0:
                del World.beepers_dict[(av, st)]
        else:     # old "debug" statement; kept in case
            pass
            #print "Attempting to remove a beeper using method "
            #print "removeOneBeepers() in World where there is no beeper."
            #print "This should not occur."
            #print "Please contact manufacturer with a bug report!"

    def addOneRobot(self, avenues=1, streets=1, orient_key = 'E',
                 beepers=0, name = None, colour = 'grey', better = False):
        """ addOneRobot(self, av, st, orient, beep, name, colour):
            This function is intended for adding a single robot."""
        if name is None:
            self.robot_number += 1
            name = "Robot" + str(self.robot_number)
        while name in self.robot_dict:
            name += str(self.robot_number)
        if not better:
            self.robot_dict[name] = robot_factory.Used_robot(
                   avenues, streets, orient_key, beepers, name, colour, self)
        else:
            self.robot_dict[name] = robot_factory.New_improved_robot(
                   avenues, streets, orient_key, beepers, name, colour, self)
        return self.robot_dict[name]

class Visible_world(World):
    """ Visible_world extends World() by adding method to draw a representation
        of that world.  It comes with default values that should be sufficient
        for all practical purpose but nonetheless allows for a large degree
        of customization. """

    settings = conf.getSettings()

    #--- Initialisation
    def __init__(self, avenues=10, streets=10, walls = [],
                 beepers = {}, robot = {},
                editWalls = False,
                screen_offsets = (50, 50, 20, 40),
                tile_info = None,
                beeper_info = None,
                wall_colours = ("black", "brown"),
                edit_wall_colours = ("brown", "black"),
                grid_colour = "light grey",
                wall_grid_colour = "brown",
                beeper_outside_colour = "cadet blue",
                beeper_inside_colour = "white",
                beeper_number_colour = "black"
                ):

        World.__init__(self, avenues, streets, walls, beepers, robot)

        settings = conf.getSettings()
        
        if tile_info == None:
            tile_info = (settings.SCREEN[4], settings.SCREEN[5])

        if beeper_info == None:
            beeper_info = (20, settings.SCREEN[6], 6, 3)

        # world positioning on "screen"
        self.xOffset = screen_offsets[0] # left
        self.yOffset = screen_offsets[1] # bottom
        self.yTopOffset = screen_offsets[2] # top
        self.right_scroller_space = screen_offsets[3] # right; leaving enough
        #room so that the right boundary is never hidden under the scrollbar.

        # rectangular walls or "tiles"
        self.tile_wide = tile_info[0]
        self.tile_narrow = tile_info[1]

        # the following 4 values are approximate values, used to center
        # beepers and beeper numbers, obtained through trial and error, based
        # on self.tile_wide=34, self.tile_narrow = 6
        self.beeper_radius = beeper_info[0]
        self.beeper_offset = beeper_info[1]
        self.beep_single_digit = beeper_info[2]
        self.beep_double_digit = beeper_info[3]

        # Walls are rectangles of a given colour, filled with a second.
        self.wall_outside_colour = wall_colours[0]

        self.wall_inside_colour = wall_colours[1]
        # allows for the possibility of using different colour when editing
        self.edit_wall_outside_colour = edit_wall_colours[0]
        self.edit_wall_inside_colour = edit_wall_colours[1]
        self.editWalls = editWalls

        self.grid_colour = grid_colour
        self.wall_grid_colour = wall_grid_colour

        self.beeper_outside_colour = beeper_outside_colour
        self.beeper_inside_colour = beeper_inside_colour
        self.beeper_number_colour = beeper_number_colour

        self.background_colour = wx.Brush('white')

        # we will create two basic world images and
        # then set this flag to True; if world dimension changes, we will
        # reset it to False
        self.background_images_created = False
        self.AdjustWorldSize()
        self.InitTileSizes()

        self.object_dict = {} # keeps track or robots

    def AdjustWorldSize(self):
        """ Computes the width and height of the display based on chosen
            parameters."""
        self.maxWidth = (self.num_cols - 1) * (
                        self.tile_wide + self.tile_narrow
                )/2 + self.tile_narrow + self.xOffset \
                         + self.right_scroller_space
        self.maxHeight = (self.num_rows - 1) * (
                        self.tile_wide + self.tile_narrow
                    )/2 + self.tile_narrow + self.yOffset + self.yTopOffset

    def InitTileSizes(self):
        """ Creates a two dimensional array of tiles containing the
            size information."""
        self.tiles_data = [[0 for row in range(self.num_rows)] \
                       for col in range(self.num_cols)]
        ns = self.tile_narrow # temporary variable easier to read in equations
        ws = self.tile_wide   # temporary variable easier to read in equations
        for col in range(0, self.num_cols):
            for row in range(0, self.num_rows):
                x = (col//2)*(ns+ws) + (col%2)*ns + self.xOffset
                y = (row//2)*(ns+ws) + (row%2)*ns + self.yTopOffset
                if col%2:
                    x_side = ws + 2*ns
                    x -= ns
                else:
                    x_side = ns
                if row%2:
                    y_side = ws + 2*ns
                    y -= ns
                else:
                    y_side = ns
                self.tiles_data[col][row] = (x, y, x_side, y_side)

    #--- World changes from Graphical World Editor

    def CalculatePosition(self, x, y):
        """ Computes the corresponding (column, row) value from an (x, y)
            world coordinate."""
        tilePair = self.tile_narrow + self.tile_wide
        x -= self.xOffset
        y -= self.yTopOffset
        numberOfWideAndNarrow = x//tilePair
        if (x - numberOfWideAndNarrow*tilePair < self.tile_narrow):
            col = 2*numberOfWideAndNarrow
        else:
            col = 2*numberOfWideAndNarrow + 1
        numberOfWideAndNarrow = y//tilePair
        if (y - numberOfWideAndNarrow*tilePair < self.tile_narrow):
            row = 2*numberOfWideAndNarrow
        else:
            row = 2*numberOfWideAndNarrow + 1
        row = self.flipRow(row)
        return col, row

    # remember that row 0 on screen is on top; in RUR world, it is on bottom
    def flipRow(self, row):
        """ On the screen, row 0 is at the top.  To facilitate
            the calculation of row <---> street, we flip the rows
            in RUR world so that row 0 is at the bottom."""
        return self.num_rows - row - 1

    def ChangeWall(self, col, row):
        """ After "clicking" a point on the screen, we check if it corresponds
            to a wall area and, if so, adds a wall if there is none, or
            remove it if there is one."""
        if not self.editWalls: return
        if col == 0 or row == 0 or \
           col == self.num_cols -1 or \
           row == self.num_rows - 1 :
            return    # we are on the border

        # wall exists when (col, row) is either (odd, even) or (even, odd)
        if (row+col)%2:
            self.ToggleWalls(col, row)
            self.DoDrawing()

    def MoveRobot(self, name):
        """ Change the robot position on the screen."""
        self.robot_dict[name].move()
        self.DoDrawing()

    def TurnRobotLeft(self, name):
        """ Change the robot orientation on the screen."""
        self.robot_dict[name].turn_left()
        self.DoDrawing()

    def TurnRobotRight(self, name):
        """ Change the robot orientation on the screen;
            only New_improved_robot can turn right."""
        self.robot_dict[name].turn_right()
        self.DoDrawing()

    def setBeepers(self, (av, st), nb):
        """ Sets the number of beepers at a given intersection from
            the Graphical world builder; robot induced changes
            are dealt with in class World."""
        World.setBeepers(self, (av, st), nb)
        self.DoDrawing()

    #--- Drawing routines : "background"

    def DrawBorders(self, dc):
        if self.editWalls:
            dc.SetPen(wx.Pen(self.edit_wall_outside_colour,1))
            dc.SetBrush(wx.Brush(self.edit_wall_inside_colour))
        else:
            dc.SetPen(wx.Pen(self.wall_outside_colour,1))
            dc.SetBrush(wx.Brush(self.wall_inside_colour))
        rects = []
        ### 4 corners
        rects.append( self.tiles_data[0][0] )
        rects.append( self.tiles_data[self.num_cols-1][0] )
        rects.append( self.tiles_data[0][self.num_rows-1] )
        rects.append( self.tiles_data[self.num_cols-1]
                      [self.num_rows-1] )
        for (col, row) in World.borders:
            rects.append(self.tiles_data[col][row]) #no need to flip; symmetry!
        if self.editWalls:
            for col in range(2, self.num_cols-1, 2):
                for row in range(2, self.num_rows-1, 2):
                        rects.append( self.tiles_data[col][row] )
        dc.DrawRectangleList(rects)

    def DrawGrid(self, dc):
        dc.SetPen(wx.Pen(self.grid_colour, 1, wx.DOT))
        tilePair = self.tile_narrow + self.tile_wide
        for row in range(1, self.num_rows - 1, 2):
            y = row*tilePair/2 + self.tile_narrow/2 + self.yTopOffset
            dc.DrawLine(self.xOffset, y,
                        self.maxWidth - self.right_scroller_space, y)
        for col in range(1, self.num_cols - 1, 2):
            x = col*tilePair/2 + self.tile_narrow/2 + self.xOffset
            dc.DrawLine(x, self.tile_narrow + self.yTopOffset, x,
                        self.maxHeight - self.yOffset)
        if self.editWalls:
            dc.SetPen(wx.Pen(self.wall_grid_colour, 1, wx.DOT))
            for row in range(2, self.num_rows - 1, 2):
                y = row*tilePair/2 + self.tile_narrow/2 + self.yTopOffset
                dc.DrawLine(self.xOffset, y,
                            self.maxWidth - self.right_scroller_space, y)
            for col in range(2, self.num_cols - 1, 2):
                x = col*tilePair/2 + self.tile_narrow/2 + self.xOffset
                dc.DrawLine(x, self.tile_narrow + self.yTopOffset, x,
                            self.maxHeight - self.yOffset)

    def DrawLabels(self, dc):
        tilePair = self.tile_narrow + self.tile_wide
        x_shift = self.xOffset//2
        y_shift = -self.yOffset
        if self.editWalls:
            # wx.SWISS is the sans-serif font
            dc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))
            pixelShift = dc.GetTextExtent("8")   # try to centre the labels
            dc.SetTextForeground(self.wall_grid_colour)
            for row in range(self.num_rows):
                y = row*tilePair/2 - pixelShift[1]//4 + self.yTopOffset
                dc.DrawText(str(self.flipRow(row)), x_shift, y)
            for col in range(self.num_cols - 1):
                x = (col*tilePair/2 + self.tile_narrow/2
                        + self.xOffset - pixelShift[0]//2)
                dc.DrawText(str(col), x, self.maxHeight + y_shift)
            x_shift = self.xOffset//4
            y_shift = -self.yOffset//2
        else:
            dc.SetTextForeground(wx.BLACK)
            dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
            dc.DrawText(_("Avenue"), 5*x_shift,
                        self.maxHeight + y_shift//2)
            dc.DrawRotatedText(_("Street"), x_shift//3,
                               self.maxHeight + 3*y_shift , 90)
        dc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        pixelShift = dc.GetTextExtent("8")   # try to centre the labels
        dc.SetTextForeground(wx.BLACK)
        for row in range(1, self.num_rows, 2):
            y = row*tilePair/2 - pixelShift[1]//4 + self.yTopOffset
            dc.DrawText(str(self.flipRow(row)//2 + 1), x_shift, y)
        for col in range(1, self.num_cols, 2):
            x = (col*tilePair/2 + self.tile_narrow/2
                   + self.xOffset - pixelShift[0]//2)
            dc.DrawText(str(col//2+1), x, self.maxHeight + y_shift)


    def DrawBackground(self, dc):
        """ Creates two background images, one for normal robot motion,
            the other for editing walls.  This is done to speed up the
            drawing process following a change in the world through a
            robot action.  These two background images need to be
            recreated if the world dimensions change."""
        if not self.background_images_created:
            saved_flag = self.editWalls
            self.editWalls = False
            self.image_noEditWalls = wx.EmptyBitmap(self.maxWidth,
                                                   self.maxHeight)
            offDC = wx.MemoryDC()
            offDC.SelectObject(self.image_noEditWalls)

            offDC.SetBackground(self.background_colour)

            offDC.Clear()
            self.DrawGrid(offDC)
            self.DrawLabels(offDC)
            self.DrawBorders(offDC)
            ## first image completed
            self.editWalls = True
            self.image_EditWalls = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
            # Selecting a new image in offDC; this releases the first one
            # for further use.
            offDC.SetBackground(self.background_colour)
            offDC.SelectObject(self.image_EditWalls)
            offDC.Clear()
            self.DrawGrid(offDC)
            self.DrawLabels(offDC)
            self.DrawBorders(offDC)
            # We are finished with offDC.  We must release its link with
            # the second image
            del offDC
            ## second image completed
            self.editWalls = saved_flag
            self.background_images_created = True
        if self.editWalls:
            dc.DrawBitmap(self.image_EditWalls, 0, 0, True)
        else:
            dc.DrawBitmap(self.image_noEditWalls, 0, 0, True)

    #--- Drawing routines : "foreground"

    def DrawTrace(self, dc, name):
        """ Draws a line that shows the path taken by the robot."""
        tilePair = self.tile_narrow + self.tile_wide
        yOffset = self.tile_narrow/2 + self.yTopOffset
        xOffset = self.tile_narrow/2 + self.xOffset
        for line in self.robot_dict[name].line_trace:
            x_0, y_0, x_1, y_1, orientation, style, colour = line
            width, trace_offset = self.robot_dict[name].get_trace_style(style)
            dc.SetPen(wx.Pen(colour, width))
            X0, Y0 = trace_offset[orientation]
            if (x_0 == x_1) and (y_0 == y_1):    #turning left
                X1, Y1 = trace_offset[(orientation+1)%4]
            else:
                X1, Y1 = X0, Y0
            col_0 = 2*x_0 - 1
            col_1 = 2*x_1 - 1
            row_0 = self.flipRow(2*y_0 - 1)
            row_1 = self.flipRow(2*y_1 - 1)
            y0 = row_0*tilePair/2 + yOffset + Y0
            y1 = row_1*tilePair/2 + yOffset + Y1
            x0 = col_0*tilePair/2 + xOffset + X0
            x1 = col_1*tilePair/2 + xOffset + X1
            dc.DrawLine(x0, y0, x1, y1)

    def DrawRobot(self, dc, name):
        avenue, street = self.robot_dict[name].getPos()
        row = self.flipRow(2*street -1)
        col = 2*avenue -1
        # irrelevant = tile size
        x, y, irrelevant, irrelevant2 = self.tiles_data[col][row]
        xx, yy = self.robot_dict[name].imageOffset
        x += xx
        y += yy
        self.robot_image_origin = (x, y) # for use in automatic scrolling
        dc.DrawBitmap(self.robot_dict[name].robot_image, x, y, True)

    def DrawWalls(self, dc):
        if self.editWalls:
            dc.SetPen(wx.Pen(self.edit_wall_outside_colour,1))
            dc.SetBrush(wx.Brush(self.edit_wall_inside_colour))
        else:
            dc.SetPen(wx.Pen(self.wall_outside_colour,1))
            dc.SetBrush(wx.Brush(self.wall_inside_colour))
        rects = []
        for (column, row) in World.walls_list :
                rects.append( self.tiles_data[column][self.flipRow(row)])
        dc.DrawRectangleList(rects)

    def DrawBeepers(self, dc):
        dc.SetPen(wx.Pen(self.beeper_outside_colour,3))
        dc.SetBrush(wx.Brush(self.beeper_inside_colour))
        circles = []
        points = []
        nb = []
        for (avenue, street) in World.beepers_dict :
            row = self.flipRow(2*street -1)
            col = 2*avenue -1
            # irrelevant = tile size
            x, y, irrelevant, irrelevant2 = self.tiles_data[col][row]
            x += self.beeper_offset
            y += self.beeper_offset
            circles.append( (x, y, self.beeper_radius, self.beeper_radius) )
            if World.beepers_dict[(avenue, street)] < 10:
                points.append((x+self.beep_single_digit, y+2))
            else:
                points.append((x+self.beep_double_digit, y+2))
            nb.append(str(World.beepers_dict[(avenue, street)]))
        dc.DrawEllipseList(circles)
        dc.SetTextForeground(self.beeper_number_colour)
        dc.DrawTextList(nb, points, None, None)

    #--- Drawing routine: "background AND foreground"

    def DoDrawing(self):
        self.world_image = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
        dc = wx.MemoryDC()
        dc.SelectObject(self.world_image)
        dc.Clear()
        dc.BeginDrawing()
        self.DrawBackground(dc)
        self.DrawWalls(dc)
        list_to_delete = []
        for name in self.robot_dict:  # draw all traces
            self.DrawTrace(dc, name)
        self.DrawBeepers(dc)
        for item in self.object_dict:  # see if robot still exists in cpu.py
            if not self.object_dict[item]:
                list_to_delete.append(item)
        for name in self.robot_dict:
            if name not in list_to_delete: # don't draw out-of-scope robots
                self.DrawRobot(dc, name)
        dc.EndDrawing()
        self.updateImage = True
