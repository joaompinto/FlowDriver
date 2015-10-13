import wx
import wx.richtext as rt
from flowevents import *


# ----------------------------------------------------------------------

class RichTextFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos=wx.DefaultPosition,
                            size = wx.Size( 500,300), style=wx.DEFAULT_FRAME_STYLE)

        self.parent = parent
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, style=wx.TE_PROCESS_TAB)
        self.m_textCtrl2.Bind(wx.EVT_CHAR, self.on_title_key_char)
        bSizer2.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        self.Centre(wx.BOTH)


        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER);

        self.rtc.Freeze()
        self.rtc.BeginSuppressUndo()

        self.rtc.BeginFontSize(12)
        self.rtc.EndFontSize()

        self.rtc.EndSuppressUndo()
        self.rtc.Thaw()

        self.rtc.SetSizeHints(400, 200)
        bSizer2.Add(self.rtc, 0, wx.ALL, 5)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetSizer(bSizer2)
        self.Layout()

    def on_title_key_char(self, event):

        if event.GetKeyCode() in [wx.WXK_TAB, wx.WXK_RETURN]:
            self.rtc.SetFocus()
        else:
            event.Skip()

    def getTitle(self):
        return

    def OnClose(self, event):
        evt = AddFlowItemEvent(title=self.m_textCtrl2.GetLineText(0), content=None)
        wx.PostEvent(self.parent, evt)
        print "Postint event to ", self.parent
        self.Destroy()




