import wx


# There are two different approaches to drawing, buffered or direct.
# This sample shows both approaches so you can easily compare and
# contrast the two by changing this value.
BUFFERED = 1

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
        self.moving_item = None
        self.lines = []
        self.flow_items = []
        self.maxWidth = 1000
        self.maxHeight = 1000
        self.x = self.y = 0
        self.curLine = []
        self.drawing = False

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

    def OnLeftButtonEvent(self, event):
        if self.IsAutoScrolling():
            self.StopAutoScrolling()

        if event.LeftDown():
            self.SetFocus()
            current_pos = wx.Point(event.GetX(), event.GetY())
            self.moving_item = self.item_at_pos(current_pos)
            if self.moving_item:
                self.move_offset = wx.Point(event.GetX() - self.moving_item.pos.x, event.GetY() - self.moving_item.pos.x)
                self.start_move_pos = current_pos
                self.CaptureMouse()
            #self.moving = True

        elif event.Dragging() and self.moving_item:
            old_rect = wx.Rect()
            selected_item = self.selected_item
            x1, y1 = self.CalcScrolledPosition(selected_item.pos.x, selected_item.pos.y)
            x2, y2 = self.CalcScrolledPosition(selected_item.pos.x+selected_item.size.x, selected_item.pos.y+selected_item.size.y)
            old_rect.SetTopLeft((x1, y1))
            old_rect.SetBottomRight((x2, y2))
            old_rect.Inflate(2, 2)
            self.selected_item.pos.x = event.GetX() - self.move_offset.x
            self.selected_item.pos.y = event.GetY() - self.move_offset.y
            dc = wx.BufferedDC(None, self.buffer)
            self.DoDrawing(dc)
            # figure out what part of the window to refresh, based
            # on what parts of the buffer we just updated
            x1, y1, x2, y2 = dc.GetBoundingBox()
            x1, y1 = self.CalcScrolledPosition(x1, y1)
            x2, y2 = self.CalcScrolledPosition(x2, y2)
            # make a rectangle
            rect = wx.Rect()
            rect.SetTopLeft((x1, y1))
            rect.SetBottomRight((x2, y2))
            rect.Inflate(2, 2)

            print x1, y1, x2, y2
            # refresh it

            self.RefreshRect(old_rect)
            self.RefreshRect(rect)

        elif event.LeftUp() and self.moving_item:
            self.moving_item = None
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
