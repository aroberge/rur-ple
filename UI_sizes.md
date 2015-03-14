This page points to rurple default window sizes and the "Code and learn" tab dimension links in the code.

# Introduction #
The purpose is to make it easy for developers and people not liking the default split or wanting to modify it to fit different screen sizes by default. All sizes are in pixel.

# Command line options #
There are now 3 different sizes supported by default:
  * default size (no option at startup) starts rurple in a 980x700 window
  * small monitors: -800x600 or -s option
  * netbook screens: -1024x600 or -sw option

All the above sizes should appear without scrollbars in "code and learn" tab.

# Variables #
All values have been moved to the variable initialization section in rur\_start.py and the variable is called misc.SCREEN. Should you want to add one mode for yourself, you just need add an elif branch before the default option in rur\_start.py.

`misc.SCREEN=[800,660,290,57,34,6,13,12,9]`
where
  * 800 is rurple window size width at startup
  * 660 is rurple window size height at startup
  * 290 is the programming pane width in "code and learn" tab
  * 57 is the debugging window height at the lower right in "code and learn"
  * 34 is Reeborg's world brick length
  * 6 is Reeborg's world brick thickness
  * 13 is the beeper position offset
  * 12 is Reeborg's horizontal offset
  * 9 is Reeborg's vertical offset

# Code location #
## Rur-ple size at startup ##
Defined in rur\_start.py
  * line 110: `size = (misc.SCREEN[0], misc.SCREEN[1])`
  * line 171: `self.SetSize((misc.SCREEN[0], misc.SCREEN[1]))` <- this line overrides the former one

## World drawing size in pixel ##
Defined in world\_creation.py
  * line 222: `tile_info = (misc.SCREEN[4], misc.SCREEN[5])`
  * beepers centering is defined just below and adjusted based on above parameters

## Code and Learn windows split ##
Defined in sash.py
  * line 56: `win.SetDefaultSize(wx.Size(misc.SCREEN[2], 600))`
  * line 74: `self.bottomWindow.SetDefaultSize(wx.Size(800, misc.SCREEN[3]))`

## Beepers offset ##
Defined in world\_creation.py
  * line 223: `beeper_info = (20, misc.SCREEN[6], 6, 3)`

## Robots offset ##
Defined in robot\_factory.py
  * line 257: `self.imageOffset = (misc.SCREEN[7], misc.SCREEN[8])`
  * line 266: `self.imageOffset = (misc.SCREEN[7], misc.SCREEN[8])`

## version 1.0.1 sizes ##
Current released version launches with:
  * screen size of 900 x 660
  * program code left pane of 300 (code and learn)
  * debug lower right pane of 100 (code and learn)