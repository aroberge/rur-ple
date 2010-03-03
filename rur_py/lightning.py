#!/usr/bin/env python
# -*- coding: utf-8
ABOUT='''Lightning Compiler is a simple Python editor that can execute Python 
programs 'instantly', outputting the result in a side window, for testing 
purposes.  Adapt as you wish but please acknowledge the original source 
if you do.           (c) André Roberge, andre.roberge@gmail.com'''

import keyword
import os
import sys
import re
from tempfile import gettempdir
TMP_DIR = gettempdir()

import wx   
import wx.stc as stc
import wx.py as py    # For the interpreter
from translation import _
import dialogs

BOTTOM, RIGHT = 1, 2
#--- The following can be configured easily by the user
WIDTH, HEIGHT = 800, 600   # Window size
CONTROL_WIDTH = 100
OUT_WIDTH, OUT_HEIGHT = 300, 230 # Default starting values for
                             #  output window, depending on layout
OUTPUT = BOTTOM   # default is output window at the bottom of the editor
HIDDEN = True     # hidden when program is launched
CLEAR_BEFORE_RUN = False  # if True, output window is cleared before each run

if wx.Platform == '__WXMSW__':
    faces = { 'mono' : 'Courier New',
              'helv' : 'Arial',
              'size' : 11,
              'size2': 8,
             }
else:
    faces = { 'mono' : 'Courier',
              'helv' : 'Helvetica',
              'size' : 11,
              'size2': 9,
             }

# Since the Python shell inherits from the stc.StyledTextCtrl outside of this
# program, and both LogWindow and PythonEditor inherits inside, we extract
# in a single function the customization part so that it can be accessed by
# all three without having to duplicate the code. Since it is not a normal
# class method, we will use "instance" instead of "self" for notation.
def set_styles(instance):       
    # Global default styles for all languages
    instance.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)
    # folding and white spaces
    instance.SetProperty("fold", "1")
    instance.SetProperty("tab.timmy.whinge.level", "1")
    instance.SetMargins(2, 2)
    # Set up the numbers in the margin for margin #1
    instance.SetMarginType(1, stc.STC_MARGIN_NUMBER)
    # Reasonable (?) value for 4 digits using a small mono font (33 pixels)
    instance.SetMarginWidth(1, 33)
    # Default
    instance.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(mono)s,size:%(size)d" % faces)
    instance.SetViewWhiteSpace(1)
    # Comments
    instance.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#009900,face:%(mono)s,size:%(size)d" % faces)
    # Number
    instance.StyleSetSpec(stc.STC_P_NUMBER, "fore:#FF0000,bold,size:%(size)d" % faces)
    # String
    instance.StyleSetSpec(stc.STC_P_STRING, "fore:#660066,face:%(mono)s,size:%(size)d" % faces)
    # Single quoted string
    instance.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#660066,face:%(mono)s,size:%(size)d" % faces)
    # Keyword
    instance.StyleSetSpec(stc.STC_P_WORD, "fore:#336699,bold,face:%(mono)s,size:%(size)d" % faces)
    # Triple quotes
    instance.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#660066,size:%(size)d" % faces)
    # Triple double quotes
    instance.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#660066,size:%(size)d" % faces)
    # Class name definition
    instance.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#000099,bold,underline,face:%(mono)s,size:%(size)d" % faces)
    # Function or method name definition
    instance.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#3333ff,bold,face:%(mono)s,size:%(size)d" % faces)
    # Operators
    instance.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
    # Identifiers
    instance.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(mono)s,size:%(size)d" % faces)
    # Comment-blocks
    instance.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
    # End of line where string is not closed
    instance.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)
    # Python styles ----------------------------------------
    instance.SetLexer(stc.STC_LEX_PYTHON)
    keywords=keyword.kwlist
    keywords.extend(['None', 'as', 'True', 'False'])
    instance.SetKeyWords(0, " ".join(keywords))
#---  End of configuration options by user -----

HISTORY='''January 2006 - version 1.0
February 2006 - version 1.1 minor changes mostly to add key shortcuts
Suggestions by Franz Steinhaeusler (with code samples!)
version 1.1.1 changed LogWindow.write() so that window scrolls automatically
version 1.2  Changed layout and added hiding output window option
version 1.3  Changed to wxNotebook, and added an interpreter.
version 1.4  Possibility to run selected text.  Added "Go to line" option.
version 1.5  Added drag and drop option
version 1.6  Added styling options to interpreter
             Added layout option for output window
             Made options easier to customize by user
version 1.7  Added 'run with' option, to simulate command line arguments.
version 1.7.1 Changed arguments from list to string.
version 1.7.2 Fixed "bug" when goToLine is cancelled.
version 1.8  Refactored so that it could more easily be embedded in other
            applications, including having the option of laying out
            buttons horizontally at the top, as is the case in RUR-PLE.
            (RUR-PLE also uses buttons with images instead of text.)
version 1.9  Added an option to run code snippets with doctest, either
             in basic mode, or in verbose mode.
version 1.9.1 test files (for doctest) now in temporary directory; refactored.
version 2.0  Added multiple editor pages option, and ability to run 
             doctest suite in external file.
version 2.1  Added self-indentation and folding key control, courtesy of
            Milan Melena.
            
Thanks to suggestions (with code snippets!) by 
Franz Steinhaeusler and Tim Golden
Other suggestions by Rune Strand and various anonymous users.
'''

SHORTCUTS = '''NOTE: not all of the following are available using the version
of the editor embedded within rur-ple.

alt-F4: exit                           ctrl-a: select all
ctrl-o: open file                      ctrl-c: copy
ctrl-s: save file                      ctrl-v: paste
ctrl-r: run script                     ctrl-x: cut
ctrl-e: erase output window content    F1: help!
ctrl-l: changes layout                 ctrl-h: hide/show output window
ctrl-g: go to line                     ctrl-n: new (additional) editor
ctrl-space and ctrl-shift-space: fold/expand (all) code

F6: run script with arguments; arguments are assumed to be separated by
spaces, and are available in the string _Args, which may be a unicode string
depending on the version of wxPython that is used.  
If the script needs to be run a second time with the same arguments, 
it can be run with ctrl-r.

F2/F3: invokes doctest on the code displayed in the editor, 
either in basic or verbose mode.
F4/F5: invokes doctest "suite" (with unittest) on the code displayed in 
the editor, either in basic or verbose mode; a single external test file
can be used.

WARNING: if your script contains encoding information like 
# -*- encoding: latin-1 -*-
this may lead to a SystemError: compile_node: unexpected node type.
If so, try removing the encoding line.

NOTE: tabs automatically  converted to 4 spaces in editor window!

NOTE: You can "drag and drop" a file into the editor window.
'''

editor_tabs = []  # list keeping track of additional editors

def set_colour(instance, color):
    style = "%s,face:%s(mono)s,size:%s(size2)d"%(color, '%', '%')
    instance.StyleSetSpec(stc.STC_STYLE_LINENUMBER, style%faces)

def fixLineEnding(txt):
    txt1 = re.sub('\r\n', '\n', txt)
    txt = re.sub('\r', '\n', txt1)
    return txt

#----------------------------------------------------------------------
class PythonSTC(stc.StyledTextCtrl):
    def __init__(self, parent, ID):
        stc.StyledTextCtrl.__init__(self, parent, ID,
                                  style = wx.NO_FULL_REPAINT_ON_RESIZE)
        # Setup a margin to hold fold markers
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        # and now set up the fold markers; squares for top level
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "black")
        # circles for mid-levels to better distinguish from top-level
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_CIRCLEPLUSCONNECTED, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "black")
        # straight perpendicular lines to connect
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "black")
        # Indentation and tab stuff
        self.SetIndent(4)               # Proscribed indent size for wx
        self.SetIndentationGuides(True) # To help beginners, show indent guides
        self.StyleSetSpec(stc.STC_STYLE_INDENTGUIDE, "fore:#333333")
        self.SetBackSpaceUnIndents(True)# Backspace unindents rather than delete 1 space
        self.SetTabIndents(True)        # Tab key indents
        self.SetTabWidth(4)             # Prescribed tab size for wx
        self.SetUseTabs(False)          # Use spaces rather than tabs, or TabTimmy will complain!
        self.SetViewWhiteSpace(False)
        # events
        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI) #wxPython 2.5
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
# The following has been copied vertabim from the wxPython demo
    def OnUpdateUI(self, evt):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)
        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1
        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos
        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)
        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
# The following has been copied vertabim from the wxPython demo
    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)
# The following has been copied vertabim from the wxPython demo
    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True
        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break;
        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)
                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)
            lineNum += 1
# The following has been copied vertabim from the wxPython demo
    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line += 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)
            if level == -1:
                level = self.GetFoldLevel(line)
            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.Expand(line, doExpand, force, visLevels-1)
                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line += 1;
        return line
    
    def OnKeyPressed(self, event):
        key = event.GetKeyCode()
        # Folding ...
        if key == ord(" "):
            if event.ControlDown():
                if event.ShiftDown():
                    self.FoldAll()
                    return
                else:
                    line = self.LineFromPosition(self.GetCurrentPos())
                    if not self.GetFoldLevel(line) & stc.STC_FOLDLEVELHEADERFLAG:
                        line = self.GetFoldParent(line)
                        self.GotoLine(line)
                    self.ToggleFold(line)
                    return
        # Indentation
        if key == wx.WXK_RETURN:
            ind = "\n"
            line = self.GetCurLine()[0]
            m = re.match(" +", line)
            if m:
                ind += m.group(0)
            if chr(self.GetCharAt(self.GetCurrentPos()-1)) == ":":
                ind += "    "
            self.AddText(ind)
            return
        event.Skip(True)    
    
    
#----------------------------------------------------------------------

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.parent = parent

    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            f = open(file)
            for line in f.readlines():
                self.parent.PythonEditor.AddText(line)

class PythonEditor(PythonSTC):
    def __init__(self, parent, ID=-1):
        PythonSTC.__init__(self, parent, ID)
        self.parent = parent
        set_styles(self)
        set_colour(self, "back:#99AACC")

class LogWindow(PythonEditor):
    def __init__(self, parent):
        PythonEditor.__init__(self, parent)
        self.SetKeyWords(0, " ")
        set_colour(self, "back:#99AA99")

    def redirect(self, option=''):
        if option == "reset":
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            print "redirecting output to default"
        else:
            if sys.stdout == sys.__stdout__:
                print "redirecting output to LogWindow instance."
            sys.stdout = self
            sys.stderr = self

    def write(self, text):
        '''required method for sys.stdout and sys.stderr handling'''
        self.AddText(text)
        self.EnsureCaretVisible()
        
    def clear_text(self, event):
        self.ClearAll()

class ControlPanel(wx.Panel):
    def __init__(self, parent, editor):
        wx.Panel.__init__(self, parent, -1)
        helpId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.help, 
                  wx.Button(self, helpId, _("Help (F1)"), (3, 5)))
        newTabId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.newTab, 
                  wx.Button(self, newTabId, _("New Editor (c-n)"), (3, 30)))
        openId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.openFile, 
                  wx.Button(self, openId, _("Open (c-o)"), (3, 70)))
        saveId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.saveFile, 
                  wx.Button(self, saveId, _("Save (c-s)"), (3, 95)))
        runId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.run, 
                  wx.Button(self, runId, _("Run (c-r)"), (3, 135)))
        runWithId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.run_with, 
                  wx.Button(self, runWithId, _("Run with (F6)"), (3, 160)))
        doctestId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.doctest_basic, 
                  wx.Button(self, doctestId, _("docTest (F2)"), (3, 200)))
        verboseId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.doctest_verbose, 
                  wx.Button(self, verboseId, _("Verbose (F3)"), (3, 225)))
        testSuiteId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.doctest_suite, 
                  wx.Button(self, testSuiteId, _("test suite (F4)"), (3, 250)))
        verboseSuiteId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.doctest_verbose_suite, 
                  wx.Button(self, verboseSuiteId, _("v. suite (F5)"), (3, 275)))

        goToId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.goToLine, 
                  wx.Button(self, goToId, _("Go to (c-g)"), (3, 315)))
        showId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.show, 
                  wx.Button(self, showId, _("Hide/show (c-h)"), (3, 355)))
        clearId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.clear, 
                  wx.Button(self, clearId, _("Erase (c-e)"), (3, 380)))
        switchId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.switch_layout, 
                  wx.Button(self, switchId, _("Layout (c-l)"), (3, 405)))


        aTable = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('O'), openId),
                                    (wx.ACCEL_CTRL, ord('S'), saveId),
                                    (wx.ACCEL_CTRL, ord('R'), runId),
                                    (wx.ACCEL_NORMAL, wx.WXK_F6, runWithId),
                                    (wx.ACCEL_CTRL, ord('E'), clearId),
                                    (wx.ACCEL_NORMAL, wx.WXK_F1, helpId),
                                    (wx.ACCEL_CTRL, ord('H'), showId),
                                    (wx.ACCEL_CTRL, ord('G'), goToId),
                                    (wx.ACCEL_CTRL, ord('L'), switchId),
                                    (wx.ACCEL_CTRL, ord('N'), newTabId),
                                    (wx.ACCEL_NORMAL, wx.WXK_F2, doctestId),
                                    (wx.ACCEL_NORMAL, wx.WXK_F3, verboseId),
                                    (wx.ACCEL_NORMAL, wx.WXK_F4, testSuiteId),
                                    (wx.ACCEL_NORMAL, wx.WXK_F5, verboseSuiteId)])
        editor.SetAcceleratorTable(aTable)      

class EditorSashWindow(wx.Panel):
    def __init__(self, parent, grand_parent=None, controller=ControlPanel, 
                  top_control=False, top_control_height=-1):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        winids = []
        self.arguments = ''
        self.output_default_height = OUT_HEIGHT
        self.output_default_width = OUT_WIDTH
        if top_control:   # for embedding in RUR-PLE
            self.controls = wx.SashLayoutWindow(self, -1)
            winids.append(self.controls.GetId())
            self.controls.SetDefaultSize((WIDTH, top_control_height))
            self.controls.SetOrientation(wx.LAYOUT_HORIZONTAL)
            self.controls.SetAlignment(wx.LAYOUT_TOP)
            win = controller(self.controls, self)
        else:    # Left window has fixed size and contains control buttons
            self.controls = wx.SashLayoutWindow(self, -1)
            winids.append(self.controls.GetId())
            self.controls.SetDefaultSize((100, HEIGHT))
            self.controls.SetOrientation(wx.LAYOUT_VERTICAL)
            self.controls.SetAlignment(wx.LAYOUT_LEFT)
            win = controller(self.controls, self)
        if grand_parent is not None:
            grand_parent.py_ch = win
        
        self.remainingSpace = wx.SashLayoutWindow(self, -1, 
                                 style=wx.NO_BORDER|wx.SW_3D)
        self.PythonEditor = PythonEditor(self.remainingSpace)
        # Output window at the bottom
        win =  wx.SashLayoutWindow(
                self, -1, wx.DefaultPosition, wx.DefaultSize, 
                wx.NO_BORDER|wx.SW_3D
                )
        winids.append(win.GetId())
        win.SetDefaultSize((WIDTH, self.output_default_height))
        win.SetOrientation(wx.LAYOUT_HORIZONTAL)
        win.SetAlignment(wx.LAYOUT_BOTTOM)
        win.SetSashVisible(wx.SASH_TOP, True)
        win.SetExtraBorderSize(8)
        self.bottomWindow = win
        # Output window at the right
        win =  wx.SashLayoutWindow(
                self, -1, wx.DefaultPosition, wx.DefaultSize, 
                wx.NO_BORDER|wx.SW_3D
                )
        winids.append(win.GetId())
        win.SetDefaultSize((self.output_default_width, HEIGHT))
        win.SetOrientation(wx.LAYOUT_VERTICAL)
        win.SetAlignment(wx.LAYOUT_RIGHT)
        win.SetSashVisible(wx.SASH_LEFT, True)
        win.SetExtraBorderSize(8)
        self.rightWindow = win

        self.output_window_bottom = LogWindow(self.bottomWindow)
        self.output_window_right = LogWindow(self.rightWindow)
        if OUTPUT == RIGHT:
            self.output_window = self.output_window_right
            self.hide_bottom_window = True
            self.hide_right_window = HIDDEN
        else:
            self.output_window = self.output_window_bottom
            self.hide_bottom_window = HIDDEN
            self.hide_right_window = True
        self.show_bottom()
        self.show_right()
        
        self.Bind(wx.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag, id=min(winids), 
                  id2=max(winids))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        # drag and drop
        dt = MyFileDropTarget(self)
        self.PythonEditor.SetDropTarget(dt)        
        
    def OnSashDrag(self, event):
        eobj = event.GetEventObject()
        if eobj is self.bottomWindow:
            self.output_default_height = event.GetDragRect().height
            self.bottomWindow.SetDefaultSize((WIDTH, event.GetDragRect().height))
        elif eobj is self.rightWindow:
            self.output_default_width = event.GetDragRect().width
            self.rightWindow.SetDefaultSize((event.GetDragRect().width, HEIGHT))
        self._refresh()
        
    def _refresh(self):
        wx.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()

    def OnSize(self, event):
        wx.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)

    def openFile(self, event):
        self.filename = dialogs.openDialog(_("Choose a file"),
           _("Python files (*.py)|*.py| All files (*.*)|*.*"),
            "",  os.getcwd())

        if self.filename != "":
            user_code = open(self.filename, 'r').read()
            self.PythonEditor.SetText(user_code)




    def saveFile(self, event):
        user_code = self.PythonEditor.GetText()
        user_code = fixLineEnding(user_code)
        self.filename = dialogs.checkedSaveDialog(user_code,
            _("Save Python file as"),
            _("Python files (*.py)|*.py| All files (*.*)|*.*"),
            self.filename, os.getcwd())

        
    ##--- Running routines
    
    def prepare_execution(self):
        # ensures output window is visible
        if OUTPUT == RIGHT:
            if not self.hide_right_window:
                self.show_right()
        else:
            if not self.hide_bottom_window:
                self.show_bottom()
        if CLEAR_BEFORE_RUN:
            self.clear("fake event")
        self.output_window.redirect()
        self.select = self.PythonEditor.GetSelectedText()
        if self.select:
            print "#Begin: == Executing selected (not entire) text =="
            user_code = self.select
        else:
            user_code = self.PythonEditor.GetText()
        return fixLineEnding(user_code)
    
    def post_execution(self):
        if self.select:
            print "#End: == Executing selected (not entire) text =="
        self.output_window.redirect('reset')

    def run(self, event):
        '''Runs the user code; input() and raw_input() are implemented
           with dialogs.'''
        user_code = self.prepare_execution()
        myGlobals = {}
        myGlobals['_Args'] = self.arguments
        myGlobals['raw_input'] = self.myRawInput
        myGlobals['input'] = self.myInput
        exec user_code in myGlobals
        self.post_execution()
        
    def run_with(self, event):
        '''Runs the user code with arguments passed to script'''
        dlg = wx.TextEntryDialog(self, _("Enter arguments list"), 
        _("Running script with arguments"), self.arguments)
        if dlg.ShowModal() == wx.ID_OK:
            self.arguments = dlg.GetValue()
        dlg.Destroy()        
        self.run("fake event")             

    def doctest_basic(self, event, verbose=False):
        '''Runs the user code using the doctest module'''
        user_code = self.prepare_execution()
        user_code += "\nimport doctest\ndoctest.testmod()"
        self.doctest_execute(user_code, verbose)
        self.post_execution() 

    def doctest_execute(self, user_code, verbose):
        '''Creates temporary python module to be tested and tests it.'''
        tmp_filename = os.path.join(TMP_DIR, '_doctest_file.py')
        f = open(tmp_filename, 'w')
        f.write(user_code)
        f.close()
        if verbose:
            f_in, f_out = os.popen4("python %s -v"%tmp_filename)
        else:
            f_in, f_out = os.popen4("python %s"%tmp_filename)
        for line in f_out.readlines():
            print line,
        
    def doctest_verbose(self, event):
        '''Runs the user code using the doctest module in verbose mode'''
        self.doctest_basic(event, verbose=True)

    def select_test_file(self):
        ''' Dialog to select test file to use with doctest suite (unittest).'''
        wildcard = _("All files (*.*)|*.*")
        dlg = wx.FileDialog(self, _("Select file to be used in test suite"), 
                           os.getcwd(), "", wildcard, wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.testfile_name = dlg.GetPath()
        else:
            self.testfile_name = None
        dlg.Destroy()

    def doctest_suite(self, event, verbose=False):
        '''Runs the user code using the doctest and unittest module
           with tests in external file.'''
        self.select_test_file()
        if self.testfile_name is None:
            return
        
        user_code = self.prepare_execution()
        if verbose:
            unittest_verb = 'verbosity=2'
        else:
            unittest_verb = ''
        added_text = '''
import doctest
doctest.testmod()
import unittest
suite = doctest.DocFileSuite(r\'%s')
unittest.TextTestRunner(%s).run(suite)
'''%(self.testfile_name, unittest_verb)
        user_code += added_text
        self.doctest_execute(user_code, verbose)
        self.post_execution() 

    def doctest_verbose_suite(self, event):
        '''Runs the user code using the doctest and unittest module in 
           verbose mode with tests in external file.'''
        self.doctest_suite(event, verbose=True)

    def clear(self, event):
        '''Clears the output window'''
        self.output_window.ClearAll()
    
    def help(self, event):
        if OUTPUT == RIGHT:
            self.hide_right_window = False
        else:
            self.hide_bottom_window = False
            self.output_default_height = 400 # impose larger height to display
        self.show("fake event")  # will be forced to display
        self.output_window.AddText("%s\n%s\n\n%s"%(SHORTCUTS, ABOUT, HISTORY))

    def newTab(self, event):
        '''Adds a new editor page.'''
        editor_tabs.append(EditorSashWindow(self.parent))
        nb = len(editor_tabs)+1
        self.parent.AddPage(editor_tabs[-1], "Editor %d"%nb)
        

    def show(self, event):
        '''Shows or hides the output window'''
        if OUTPUT == RIGHT:
            self.show_right()
        else:
            self.show_bottom()

    def show_right(self):
        '''Shows or hides the right output window'''
        if self.hide_right_window:
            self.rightWindow.SetDefaultSize((0, 600))
            self.hide_right_window = False
        else:
            self.rightWindow.SetDefaultSize((self.output_default_width, 600))
            self.hide_right_window = True
        self._refresh()
            
    def show_bottom(self):
        '''Shows or hides the bottom output window'''
        if self.hide_bottom_window:
            self.bottomWindow.SetDefaultSize((800, 0))
            self.hide_bottom_window = False
        else:
            self.bottomWindow.SetDefaultSize((800, self.output_default_height))
            self.hide_bottom_window = True
        self._refresh()

    def switch_layout(self, event):
        global OUTPUT
        if OUTPUT == RIGHT:
            OUTPUT = BOTTOM
            self.output_window = self.output_window_bottom
            if self.hide_right_window:
                self.show_right()
                self.show_bottom()
        else:
            OUTPUT = RIGHT
            self.output_window = self.output_window_right
            if self.hide_bottom_window:
                self.show_right()
                self.show_bottom()
        self._refresh()

    def goToLine(self, event):
        dlg = wx.TextEntryDialog(self, _("Enter line number"), _("Go to line"), '')
        line = ''
        if dlg.ShowModal() == wx.ID_OK:
            line = int(dlg.GetValue()) - 1
        dlg.Destroy()
        if line != '':
            self.PythonEditor.GotoLine(line)
        self.PythonEditor.SetFocus()

    def myRawInput(self, text):
        dlg = wx.TextEntryDialog(self, text, _("raw_input() request"), '')
        if dlg.ShowModal() == wx.ID_OK:
            user_response = dlg.GetValue()
        dlg.Destroy()
        print "# raw_input(\'%s\'): %s" % (text, user_response)
        return user_response
    
    def myInput(self, text):
        dlg = wx.TextEntryDialog(self, text, _("input() request"), '')
        if dlg.ShowModal() == wx.ID_OK:
            user_response = dlg.GetValue()
        dlg.Destroy()
        print "# input(\'%s\'): %s" % (text, user_response)
        return eval(user_response)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self,parent, -1, title, size=(WIDTH, HEIGHT),
                    style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.app = wx.Notebook(self, -1)
        editor = EditorSashWindow(self.app)
        self.app.AddPage(editor, -("Editor"))
        sh = py.shell.Shell(self.app, -1)
        set_styles(sh)
        self.app.AddPage(sh, _("Interpreter"))
        self.Show(True)
        editor.PythonEditor.SetFocus()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame=MainWindow(None, _("Lightning Compiler"))
    app.MainLoop()
