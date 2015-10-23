import wx
from editframe import RichTextFrame
from flowevents import *


class FlowItem:
    def __init__(self, pos, size, title, content):
        self.pos = pos
        self.size = size
        self.title = title
        self.content = content


# ---------------------------------------------------------------------------

class MyCanvas(wx.ScrolledWindow):
    def __init__(self, parent, id=-1, size=wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

        self.selected_item = None
        self.clicked_item = None
        self.lines = []
        self.flow_items = []
        self.maxWidth = 1000
        self.maxHeight = 1000
        self.x = self.y = 0
        self.curLine = []
        self.click_offset = None

        self.SetBackgroundColour("WHITE")
        # self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))

        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        self.SetScrollRate(20, 20)


        # Initialize the buffer bitmap.  No real DC is needed at this point.
        self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DoDrawing(dc)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftButtonEvent)
        self.Bind(wx.EVT_MOTION, self.OnLeftButtonEvent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(EVT_UPD_FLOW_ITEM, self.OnUpdateFlowItem)
        self.Bind(EVT_ADD_FLOW_ITEM, self.OnAddFlowItem)

    def getWidth(self):
        return self.maxWidth

    def getHeight(self):
        return self.maxHeight

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    def DoDrawing(self, dc):
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.BeginDrawing()
        self.DrawFlowItems(dc)
        dc.EndDrawing()

    def DrawFlowItems(self, dc):
        dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 2))
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        dc.SetTextForeground(wx.BLUE)
        for item in self.flow_items:
            dc.DrawRectangle(item.pos.x, item.pos.y, item.size.x, item.size.y)
            dc.DrawText(item.title, item.pos.x + 2, item.pos.y)

    def SetXY(self, event):
        self.x, self.y = self.ConvertEventCoords(event)

    def ConvertEventCoords(self, event):
        newpos = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        return newpos

    def OnDoubleClick(self, event):
        event_pos = wx.Point(event.GetX(), event.GetY())
        clicked_item = self.item_at_pos(event_pos)
        if clicked_item:
            RichTextFrame(self, clicked_item.title, clicked_item.content).Show()


    def OnLeftButtonEvent(self, event):

        event_pos = wx.Point(event.GetX(), event.GetY())

        if self.IsAutoScrolling():
            self.StopAutoScrolling()

        if event.LeftDown():
            self.SetFocus()
            self.clicked_item = clicked_item = self.item_at_pos(event_pos)
            if clicked_item:
                self.click_offset = wx.Point(event_pos.x - clicked_item.pos.x, event_pos.y - clicked_item.pos.y)
                self.CaptureMouse()

        elif event.Dragging() and self.clicked_item:

            clicked_item = self.clicked_item
            clicked_item.pos.x = event_pos.x - self.click_offset.x
            clicked_item.pos.y = event_pos.y - self.click_offset.y

            dc = wx.BufferedDC(None, self.buffer)
            self.DoDrawing(dc)

            # refresh it
            #self.RefreshRect(rect)
            self.Refresh()

        elif event.LeftUp() and self.clicked_item:
            self.clicked_item = None
            self.ReleaseMouse()

    def get_next_item_position(self):
        """
        Free position to place the next item
        :return:
        """
        radius = 60
        potential_pos = ((radius, 0), (0, radius), (-radius, 0), (0, -radius))
        lookup_locations = [wx.Point(100, 100)]
        selected_item = self.selected_item
        if selected_item:
            for x, y in potential_pos:
                lookup_locations.append(wx.Point(selected_item.pos.x + x, selected_item.pos.y + y))


        for pos in lookup_locations:
            if self.item_at_pos(pos) is None:
                return pos

    def item_at_pos(self, check_pos):
        for item in self.flow_items:
            x_delta = check_pos.x - item.pos.x
            y_delta = check_pos.y - item.pos.y
            if 0 <= x_delta < item.size.x and 0 <= y_delta < item.size.y:
                return item

    def add_flow_item(self, title, content):
        pos = self.get_next_item_position()
        size = wx.Size(50, 100)
        item = FlowItem(pos, size, title, content)
        self.flow_items.append(item)
        self.selected_item = item
        dc = wx.BufferedDC(None, self.buffer)
        self.DoDrawing(dc)
        self.x, self.y = pos
        self.Refresh()

    def OnAddFlowItem(self, event):
        self.add_flow_item(event.title, event.content)


    def OnUpdateFlowItem(self, event):
        self.selected_item.title = event.title
        self.selected_item.contents = event.content
        dc = wx.BufferedDC(None, self.buffer)
        self.DoDrawing(dc)
        self.Refresh()
