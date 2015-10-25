# -*- coding: utf-8 -*-

"""
The flow canvas provides a scrollable canvas where flow items are drawn.
It also handles the design editing actions.

Implementation supported by:
http://wiki.wxpython.org/DoubleBufferedDrawing
"""

import wx
from itemeditframe import RichTextFrame
from flowevents import *


class FlowItem:
    def __init__(self, pos, size, title, content):
        self.pos = pos
        self.size = size
        self.title = title
        self.content = content
        self.linked_items = []

    @property
    def center(self):
        return wx.Point(self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2)


class MyCanvas(wx.ScrolledWindow):
    def __init__(self, parent, id=-1, size=wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

        self.selected_item = None
        self.clicked_item = None
        self.lines = []
        self.flow_items = []
        self.maxWidth = 1024
        self.maxHeight = 1024
        self.x = self.y = 0
        self.curLine = []
        self.click_offset = None

        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        self.SetScrollRate(20, 20)

        # Initialize the buffer bitmap.  No real DC is needed at this point.
        self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
        self.UpdateDrawing()

        self.capturing_mouse = False

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
        # the bitmap is copied to the screen when the object goes out of scope
        del dc

    def Draw(self, dc):
        dc.SetBackground(wx.Brush("LIGHT GREY"))
        dc.Clear()
        dc.BeginDrawing()
        self.DrawFlowItems(dc)
        dc.EndDrawing()

    def UpdateDrawing(self):
        dc = wx.BufferedDC(None, self.buffer)
        self.Draw(dc)
        self.Refresh(eraseBackground=False)
        self.Update()

    def determine_link_points(self, source_item, target_item):
        """
        :param source_item: Item linking from
        :param targe_item: Item linking from
        :return: (start pos, end Pos)
        """
        delta_x = target_item.center.x - source_item.center.x
        delta_y = target_item.center.y - source_item.center.y
        source_offset = wx.Point(0, 0)
        target_offset = wx.Point(0, 0)
        if abs(delta_x) >= abs(delta_y):
            source_offset.x = source_item.size.x if delta_x > 0 else 0
            source_offset.y = source_item.size.y / 2
            target_offset.x = 0 if delta_x > 0 else source_item.size.x
            target_offset.y = source_item.size.y / 2
        elif abs(delta_y) >= abs(delta_x):
            source_offset.x = source_item.size.x / 2
            source_offset.y = source_item.size.y if delta_y > 0 else 0
            target_offset.x = source_item.size.x / 2
            target_offset.y = 0 if delta_y > 0 else source_item.size.y

        return source_item.pos + source_offset, target_item.pos + target_offset

    def DrawItem(self, item, dc):
        if item == self.selected_item:
            dc.SetPen(wx.Pen("BLACK", 2))
        else:
            dc.SetPen(wx.Pen("WHITE", 0))
        dc.SetBrush(wx.Brush("WHITE"))
        dc.DrawRectangle(item.pos.x, item.pos.y, item.size.x, item.size.y)
        dc.SetPen(wx.Pen("WHITE", 0))

        # Draw the label
        dc.SetBrush(wx.Brush(wx.Colour(49, 58, 117)))
        dc.DrawRectangle(item.pos.x, item.pos.y, item.size.x, 20)

        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD)
        dc.SetFont(font)
        dc.SetTextForeground(wx.WHITE)
        dc.DrawText(item.title, item.pos.x + 4, item.pos.y+2)

        dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 2))
        for linked_item in item.linked_items:
            source_pos, target_pos = self.determine_link_points(item, linked_item)
            dc.DrawLine(source_pos.x, source_pos.y, target_pos.x, target_pos.y)

    def DrawFlowItems(self, dc):
        for item in self.flow_items:
            self.DrawItem(item, dc)

    def SetXY(self, event):
        self.x, self.y = self.ConvertEventCoords(event)

    def ConvertEventCoords(self, event):
        x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        return wx.Point(x, y)

    def OnDoubleClick(self, event):
        if self.selected_item:
            RichTextFrame(self, self.selected_item.title, self.selected_item.content).Show()

    def OnLeftButtonEvent(self, event):

        event_pos = wx.Point(event.GetX(), event.GetY())

        if self.IsAutoScrolling():
            self.StopAutoScrolling()

        if event.LeftDown():
            self.SetFocus()
            self.clicked_item = clicked_item = self.item_at_pos(self.ConvertEventCoords(event))
            if clicked_item:
                self.selected_item = clicked_item
                self.capturing_mouse = True
                self.CaptureMouse()

                self.selected_item = clicked_item
                self.UpdateDrawing()  # Need to update the selected item color
                self.click_offset = wx.Point(event_pos.x - clicked_item.pos.x, event_pos.y - clicked_item.pos.y)

        elif event.Dragging() and self.clicked_item:

            new_pos = event_pos - self.click_offset

            # Limit movement to the canvas boundaries
            new_pos.x = max(new_pos.x, 0)
            new_pos.y = max(new_pos.y, 0)
            new_pos.x = min(new_pos.x, self.maxWidth - self.clicked_item.size.x - 1)
            new_pos.y = min(new_pos.y, self.maxHeight - self.clicked_item.size.y - 1)
            self.clicked_item.pos = new_pos

            self.UpdateDrawing()

        elif event.LeftUp():
            if self.capturing_mouse:
                self.ReleaseMouse()
                self.capturing_mouse = False
            self.clicked_item = None

    def get_next_item_position(self):
        """
        Free position to place the next item
        :return:
        """

        lookup_locations = [wx.Point(300, 150)]
        selected_item = self.selected_item
        if selected_item:
            radius = wx.Point(selected_item.size.x, selected_item.size.y) + wx.Point(30, 30)
            potential_pos = ((radius.x, 0), (0, radius.y), (-radius.x, 0), (0, -radius.y))
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
        size = wx.Size(100, 110)
        item = FlowItem(pos, size, title, content)
        self.flow_items.append(item)
        if self.selected_item:  # Link from selected item
            self.selected_item.linked_items.append(item)
        self.selected_item = item
        self.UpdateDrawing()
        self.x, self.y = pos

    def OnAddFlowItem(self, event):
        self.add_flow_item(event.title, event.content)

    def OnUpdateFlowItem(self, event):
        self.selected_item.title = event.title
        self.selected_item.contents = event.content
        self.UpdateDrawing()
