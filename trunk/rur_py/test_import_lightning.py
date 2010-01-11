#!/usr/bin/env python
# -*- coding: utf-8
'''test_import_lightning is a demo application showing how one can
embed Lightning Compiler (lightning.py), but having buttons laid out 
horizontally at the top of the window instead of vertically on the left side
as is done with lighthing.py
Adapt as you wish but please acknowledge the original source 
if you do.      André Roberge, andre.roberge@gmail.com'''

import wx   
import wx.py as py    # For the interpreter
from lightning import EditorSashWindow, set_styles

class topControlPanel(wx.Panel):
    def __init__(self, parent, editor):
        wx.Panel.__init__(self, parent, -1)
        helpId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.help, 
                  wx.Button(self, helpId, "Help", (3, 10)))
        openId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.openFile, 
                  wx.Button(self, openId, "Open", (3, 40)))
        saveId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.saveFile, 
                  wx.Button(self, saveId, "Save", (100, 10)))
        runId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.run, 
                  wx.Button(self, runId, "Run", (100, 40)))
        runWithId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.run_with, 
                  wx.Button(self, runWithId, "Run with", (200, 10)))
        goToId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.goToLine, 
                  wx.Button(self, goToId, "Go to", (200, 40)))
        showId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.show, 
                  wx.Button(self, showId, "Hide/show", (300, 10)))
        clearId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.clear, 
                  wx.Button(self, clearId, "Erase", (300, 40)))
        switchId = wx.NewId()
        self.Bind(wx.EVT_BUTTON, editor.switch_layout, 
                  wx.Button(self, switchId, "Layout", (400, 10)))
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

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self,parent, -1, title, size=(800, 600),
                    style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.app = wx.Notebook(self, -1)
        editor = EditorSashWindow(self.app, controller=topControlPanel,
                 top_control=True, top_control_height=80)    
        self.app.AddPage(editor, "Editor")
        sh = py.shell.Shell(self.app, -1)
        set_styles(sh)
        self.app.AddPage(sh, "Interpreter")
        self.Show(True)
        editor.PythonEditor.SetFocus()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame=MainWindow(None, 'Embedded Lightning Compiler')
    app.MainLoop()
