#!/usr/bin/env python
import wx


class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)


app = wx.App(False)
frame = MyFrame(None, 'windows title here')
app.MainLoop()