# -*- coding: utf8 -*-
"""Quickreport

Utilita' per la gui di Quickreport.

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""

import wx
import wx.lib.newevent

def ask_path(parent_window):
    dlg = wx.FileDialog(parent_window, message='Save report', style=wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
        return dlg.GetPath()
    else:
        return None
    


ParamChangedEvt, EVT_PARAM_CHANGED = wx.lib.newevent.NewCommandEvent()
def post_evt_param_changed(event):
    widget = event.GetEventObject()
    e = ParamChangedEvt(widget.GetId(), param_name=widget.GetName())
    wx.PostEvent(widget, e)
#    event.Skip()  # TODO e' il caso? in realta' non mi serve mai...
