# -*- coding: utf-8 -*-

"""
The top window contains the toolbar and the design canvas
"""

import wx
from gettext import gettext as _
from flowcanvas import MyCanvas
from itemeditframe import RichTextFrame
from fileio import save_file, open_file


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
        self.openFilename = None

    def CreateToolBar(self, *args, **kwargs):
        self.toolbar = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.toolbar.SetToolBitmapSize((32, 32))
        self.toolbar.AddLabelTool(1, '', scale_bitmap(wx.Bitmap('images/plus.png'), 32, 32))
        self.toolbar.AddSeparator()

        ids = [wx.ID_SAVE, wx.ID_OPEN]
               #wx.ID_UNDO, wx.ID_REDO, wx.ID_DELETE]

        arts = [wx.ART_FILE_SAVE, wx.ART_FILE_OPEN,
                wx.ART_UNDO, wx.ART_REDO, wx.ART_DELETE]
        tips = [_("Save"), _("Open a File"),  _("Undo the Last Action"), _("Redo the Last Undone Action"),
                _("Delete the currently selected item")]

        for x, (_id, art_id, tip) in enumerate(zip(ids, arts, tips)):
            art = wx.ArtProvider.GetBitmap(art_id, wx.ART_TOOLBAR)
            self.toolbar.AddSimpleTool(_id, art, tip)

        self.Bind(wx.EVT_TOOL, self.OnAddFlowItemClick, id=1)
        self.Bind(wx.EVT_TOOL, self.OnFileSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_TOOL, self.OnFileOpen, id=wx.ID_OPEN)
        self.toolbar.Realize()
        self.mainSizer.Add(self.toolbar, 0, wx.EXPAND, 5)

    def OnAddFlowItemClick(self, event):
        self.canvas.add_flow_item()
        RichTextFrame(self.canvas).Show()

    def OnFileSave(self, event):
        if self.openFilename is None:
            saveFileDialog = wx.FileDialog(self, "Save ofl file", "", "",
                                           "FLD files (*.fld)|*.fld", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

            if saveFileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed idea...
            self.openFilename = saveFileDialog.GetPath()
            saveFileDialog.Destroy()
            if '.' not in self.openFilename:
                self.openFilename += ".fld"
        save_file(self.openFilename , self.canvas.flow_items)


    def OnFileOpen(self, event):
        openFileDialog = wx.FileDialog(self, "Open FLD file", "", "",
                               "FLD files (*.fld)|*.fld", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)


        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        self.openFilename = openFileDialog.GetPath()
        openFileDialog.Destroy()

        loaded_items = open_file(openFileDialog.GetPath())

        if loaded_items is None:
            dlg = wx.MessageDialog(self, 'Not a valid file', 'Opening file', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # Conver position strings to wxPoints
        for item in loaded_items:
            x, y = [int(z) for z in item.pos.strip("()").split(',')]
            item.pos = wx.Point(x, y)
            x, y = [int(z) for z in item.size.strip("()").split(',')]
            item.size = wx.Point(x, y)

        self.canvas.flow_items = loaded_items
        self.canvas.UpdateDrawing()
        self.canvas.Refresh()

