# -*- coding: utf-8 -*-

"""
Flow management custome events
"""

from wx.lib.newevent import NewEvent

AddFlowItemEvent, EVT_ADD_FLOW_ITEM = NewEvent()
UpdateFlowItemEvent, EVT_UPD_FLOW_ITEM = NewEvent()
