# -*- coding: utf-8 -*-

"""
The item edit frame provides content editing for flow items
"""

import wx
import wx.richtext as rt
from flowevents import *


class RichTextFrame(wx.Frame):
    def __init__(self, parent, title=None, content=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE)
        self.is_new_item = True
        if title is not None:
            self.is_new_item = False

        self.parent = parent
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        verticalSizer = wx.BoxSizer(wx.VERTICAL)

        self.titleCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     style=wx.TE_PROCESS_TAB)
        if title is not None:
            self.titleCtrl.ChangeValue(title)
        self.titleCtrl.Bind(wx.EVT_CHAR, self.on_title_key_char)
        verticalSizer.Add(self.titleCtrl, 0, wx.ALL, 5)

        self.Centre(wx.BOTH)

        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)

        self.rtc.Freeze()
        self.rtc.BeginSuppressUndo()

        self.rtc.BeginFontSize(12)
        self.rtc.EndFontSize()

        self.rtc.EndSuppressUndo()
        self.rtc.Thaw()

        self.rtc.SetSizeHints(400, 200)
        verticalSizer.Add(self.rtc, 0, wx.ALL, 5)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetSizer(verticalSizer)
        self.Layout()

    def on_title_key_char(self, event):

        if event.GetKeyCode() in [wx.WXK_TAB, wx.WXK_RETURN]:
            self.rtc.SetFocus()
        else:
            event.Skip()

    def getTitle(self):
        return

    def OnClose(self, event):
        if self.is_new_item:
            evt = AddFlowItemEvent(title=self.titleCtrl.GetLineText(0), content=None)
        else:
            evt = UpdateFlowItemEvent(title=self.titleCtrl.GetLineText(0), content=None)
        wx.PostEvent(self.parent, evt)
        self.Destroy()
