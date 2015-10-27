# -*- coding: utf-8 -*-

"""
The item edit frame provides content editing for flow items
"""

from StringIO import StringIO
import wx
import wx.richtext as rt
from flowevents import *


class RichTextFrame(wx.Frame):
    def __init__(self, parent, title=None, content=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE)
        self.is_new_item = True
        self.content = content
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
        self.rtc.Bind(wx.EVT_CHAR, self.on_rtc_key_char)
        wx.CallAfter(self.load_rtc_buffer)

        self.rtc.SetSizeHints(400, 200)


        verticalSizer.Add(self.rtc, 0, wx.ALL, 5)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetSizer(verticalSizer)
        self.AddRTCHandlers()

        self.Layout()
        self.set_default_style()
        if not title:
            wx.CallAfter(self.titleCtrl.SetFocus)
        else:
            wx.CallAfter(self.rtc.SetFocus)

    def set_default_style(self):
        tmpStyle = rt.RichTextAttr()
        #tmpStyle.SetFontFaceName('Courier New')
        tmpStyle.SetFontSize(12)
        self.rtc.SetBasicStyle(tmpStyle)
        self.rtc.SetDefaultStyle(tmpStyle)

    def AddRTCHandlers(self):
        rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

    def load_rtc_buffer(self):
        content = self.content
        if content:
            print "my content is", content
            stream = StringIO()
            handler = rt.RichTextXMLHandler()
            handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
            buffer = self.rtc.GetBuffer()
            buffer.AddHandler(handler)
            stream.write(content)
            stream.seek(0)
            handler.LoadStream(buffer, stream)
            self.rtc.Refresh()

    def on_title_key_char(self, event):
        if event.GetKeyCode() in [wx.WXK_TAB, wx.WXK_RETURN]:
            self.rtc.SetFocus()
        else:
            event.Skip()

    def on_rtc_key_char(self, event):
        keycode = event.GetKeyCode()
        if keycode == 2:  # CTRL+B
            self.rtc.ApplyBoldToSelection()
        if keycode == 9:  # CTRL+I
            self.rtc.ApplyItalicToSelection()
        if keycode == 21:  # CTRL+U
            self.rtc.ApplyUnderlineToSelection()
        event.Skip()

    def getTitle(self):
        return

    def OnClose(self, event):
        handler = rt.RichTextXMLHandler()
        handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)

        stream = StringIO()
        handler.SaveStream(self.rtc.GetBuffer(), stream)
        content = stream.getvalue()
        print "closing with", content
        if self.is_new_item:
            evt = AddFlowItemEvent(title=self.titleCtrl.GetLineText(0), content=content)
        else:
            evt = UpdateFlowItemEvent(title=self.titleCtrl.GetLineText(0), content=content)
        wx.PostEvent(self.parent, evt)
        self.Destroy()
