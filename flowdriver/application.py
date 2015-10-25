# -*- coding: utf-8 -*-

"""
Main application object holder
"""

import wx
from topwindow import TopWindow


class Application:

    def __init__(self):
        self.app = wx.App(redirect=False)
        self.top = TopWindow("FlowDriver")

    def start(self):
        self.top.Show()
        self.app.MainLoop()
