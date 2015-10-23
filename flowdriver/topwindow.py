# -*- coding: utf-8 -*-


import wx
from flowcanvas import MyCanvas
from editframe import RichTextFrame
from flowevents import *

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
        self.m_statusBar1 = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)
        self.m_menubar1 = wx.MenuBar(0)
        self.SetMenuBar(self.m_menubar1)

        self.Centre(wx.BOTH)



    def CreateToolBar(self, *args, **kwargs):
        self.m_toolBar1 = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.m_toolBar1.SetToolBitmapSize((32, 32))
        self.m_toolBar1.AddLabelTool(1, '', scale_bitmap(wx.Bitmap('images/plus.png'), 32, 32))
        self.Bind(wx.EVT_TOOL, self.OnAddFlowItemClick, id=1)
        self.m_toolBar1.Realize()
        self.mainSizer.Add(self.m_toolBar1, 0, wx.EXPAND, 5)

    def OnAddFlowItemClick(self, event):
        RichTextFrame(self.canvas).Show()
