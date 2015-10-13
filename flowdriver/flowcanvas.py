import wx


# There are two different approaches to drawing, buffered or direct.
# This sample shows both approaches so you can easily compare and
# contrast the two by changing this value.
BUFFERED = 1


# ---------------------------------------------------------------------------

class MyCanvas(wx.ScrolledWindow):
    def __init__(self, parent, id=-1, size=wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

        self.selected_item = None
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
        dc.BeginDrawing()
        self.DrawFlowItems(dc)
        dc.EndDrawing()

    def DrawFlowItems(self, dc):
        dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 4))
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        dc.SetTextForeground(wx.BLACK)
        for pos, size, title, content in self.flow_items:
            dc.DrawRectangle(pos.x, pos.y, size.x, size.y)
            dc.DrawText(title, pos.x + 2, pos.y)

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

            self.curLine = []
            self.CaptureMouse()
            self.drawing = True

        elif event.Dragging() and self.drawing:
            dc = wx.BufferedDC(None, self.buffer)

            dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 2))
            coords = (self.x, self.y) + self.ConvertEventCoords(event)
            self.curLine.append(coords)
            dc.DrawLine(*coords)
            self.SetXY(event)

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
            # refresh it
            self.RefreshRect(rect)

        elif event.LeftUp() and self.drawing:
            self.lines.append(self.curLine)
            self.curLine = []
            self.ReleaseMouse()
            self.drawing = False

    def get_next_item_position(self):
        """
        Free position to place the next item
        :return:
        """
        radius = 100
        potential_pos = ((0, radius), (radius, 0), (-radius, 0), (-radius, 0))
        lookup_locations = [wx.Point(100, 100)]
        if self.selected_item:
            last_pos = self.selected_item[0]
            for x, y in potential_pos:
                lookup_locations.append(wx.Point(last_pos.x + x, last_pos.y + y))

        for pos in lookup_locations:
            print "LOOK", pos
            if self.item_at_pos(pos) is None:
                return pos

    def item_at_pos(self, check_pos):
        for item in self.flow_items:
            pos, size, label, content = item
            x_delta = check_pos.x - pos.x
            y_delta = check_pos.y - pos.y
            if 0 <= x_delta < size.x and 0 <= y_delta < size.y:
                return item

    def add_flow_item(self, title, content):
        pos = self.get_next_item_position()
        print "POS", pos
        size = wx.Size(50, 100)
        self.flow_items.append((pos, size, title, content))
        dc = wx.BufferedDC(None, self.buffer)
        self.DoDrawing(dc)
        self.x, self.y = pos
        self.Refresh()
