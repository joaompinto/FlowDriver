# -*- coding: utf-8 -*-

"""
Flow management custome events
"""

from wx.lib.newevent import NewEvent

AddFlowItemEvent, EVT_ADD_FLOW_ITEM = NewEvent()
UpdateFlowItemEvent, EVT_UPD_FLOW_ITEM = NewEvent()
SelectFlowItemEvent, EVT_SELECT_FLOW_ITEM = NewEvent()
SelectedFlowItemEvent, EVT_SELECTED_FLOW_ITEM = NewEvent()
SwitchFlowItemEvent, EVT_SWITCH_FLOW_ITEM = NewEvent()
