# !/usr/bin/env python
import wx
app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "自动生成PDF书签【sweeney_he】")  # A Frame is a top-level window.
frame.Show(True)  # Show the frame.
app.MainLoop()