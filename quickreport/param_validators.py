# -*- coding: utf8 -*-

"""Quickreport

Validatori di uso comune per i widget dei parametri.

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""

import wx


class NotEmpty(wx.PyValidator):
    def Clone(self): return NotEmpty()
    def TransferToWindow(self): return True
    def TransefFromWindow(self): return True
    
    def Validate(self, val):
        ctl = self.GetWindow()
        txt = ctl.GetValue().strip()
        if not txt:
            ctl.SetBackgroundColour("yellow")
            ctl.Refresh()
            return False
        else:
            ctl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            ctl.Refresh()
            return True


class ValidPeriod(wx.PyValidator):
    def Clone(self): return ValidPeriod()
    def TransferToWindow(self): return True
    def TransefFromWindow(self): return True
    
    def Validate(self, val):
        ctl = self.GetWindow()
        val = ctl.GetValue()
        if val[0] > val[1]:
            ctl.SetBackgroundColour("yellow")
            ctl.Refresh()
            return False
        else:
            tl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))
            ctl.Refresh()
            return True
     

