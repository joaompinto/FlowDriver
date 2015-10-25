# -*- coding: utf-8 -*-

"""
The top window contains the toolbar and the design canvas
"""

import wx
from flowcanvas import MyCanvas
from itemeditframe import RichTextFrame


def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result


class TopWindow(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(800, 600))

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.mainSizer = mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.CreateToolBar()
        self.canvas = MyCanvas(self)
        mainSizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(mainSizer)
        self.Layout()
        self.statusbar = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)
        self.menubar = wx.MenuBar(0)
        self.SetMenuBar(self.menubar)

        self.Centre(wx.BOTH)

    def CreateToolBar(self, *args, **kwargs):
        self.toolbar = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.toolbar.SetToolBitmapSize((32, 32))
        self.toolbar.AddLabelTool(1, '', scale_bitmap(wx.Bitmap('images/plus.png'), 32, 32))
        self.Bind(wx.EVT_TOOL, self.OnAddFlowItemClick, id=1)
        self.toolbar.Realize()
        self.mainSizer.Add(self.toolbar, 0, wx.EXPAND, 5)

    def OnAddFlowItemClick(self, event):
        RichTextFrame(self.canvas).Show()
