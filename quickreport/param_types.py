# -*- coding: utf8 -*-

"""Quickreport

I widget che corrispondono ai vari tipi di parametri possibili. 
Quando in <progetto>.params.py si specifica un tipo per un parametro, cio' che 
viene visualizzato nella gui e' il widget corrispondente qui definito.

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""

import wx
import datetime

from gui_utils import post_evt_param_changed, EVT_PARAM_CHANGED

__all__ = ['text', 'integer', 'boolean', 
           'symple_list', 'id_list', 'droplist', 'id_droplist', 
           'date', 'period', 
           'month', 'bimester', 'trimester', 'quadrimester', 'semester']


# 'text' type input parameter =================================================
class TextWidget(wx.TextCtrl):
    def __init__(self, *a, **k):
        wx.TextCtrl.__init__(self, *a, **k)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)
    
    def on_kill_focus(self, evt):
        if self.IsModified(): 
            self.DiscardEdits()
            post_evt_param_changed(evt)
        
    def SetBounds(self, val): pass
        
def text(parent): return TextWidget(parent)
    
    
# 'integer' type input parameter ===============================================
class IntegerWidget(wx.SpinCtrl):
    def __init__(self, *a, **k):
        wx.SpinCtrl.__init__(self, *a, **k)
        self.Bind(wx.EVT_SPIN, post_evt_param_changed)
        
    def SetBounds(self, bounds): return wx.SpinCtrl.SetRange(self, *bounds)

def integer(parent): return IntegerWidget(parent)


# 'boolean' type input parameter ===============================================
class BooleanWidget(wx.CheckBox):
    def __init__(self, *a, **k):
        wx.CheckBox.__init__(self, *a, **k)
        self.Bind(wx.EVT_CHECKBOX, post_evt_param_changed)
        
    def SetBounds(self, val): pass
    
def boolean(parent): return BooleanWidget(parent)


# 'symple_list' type input parameter ===========================================
class SimpleListWidget(wx.ListBox):
    def __init__(self, *a, **k):
        wx.ListBox.__init__(self, *a, **k)
        self.Bind(wx.EVT_LISTBOX, post_evt_param_changed)
        
    SetBounds = wx.ListBox.SetItems
    GetValue = wx.ListBox.GetStringSelection
    SetValue = wx.ListBox.SetStringSelection
    
def symple_list(parent): return SimpleListWidget(parent)


# 'id_list' type input parameter ===============================================
class TwoFieldsListWidget(wx.ListBox):
    def __init__(self, *a, **k):
        wx.ListBox.__init__(self, *a, **k)
        self.ids = []
        self.Bind(wx.EVT_LISTBOX, post_evt_param_changed)
        
    def SetBounds(self, bounds):
        self.ids = [i[0] for i in bounds]
        self.SetItems([i[1] for i in bounds])
    
    def SetValue(self, val):
        if val is None: 
            self.SetSelection(-1)
            return
        self.SetSelection(self.ids.index(val))
        
    def GetValue(self):
        return self.ids[self.GetSelection()]

def id_list(parent): return TwoFieldsListWidget(parent)


# 'droplist' type input parameter ==============================================
class DropDownListWidget(wx.ComboBox):
    def __init__(self, *a, **k):
        k['style'] = wx.CB_DROPDOWN|wx.CB_READONLY
        wx.ComboBox.__init__(self, *a, **k)
        self.Bind(wx.EVT_COMBOBOX, post_evt_param_changed)
    
    SetBounds = wx.ComboBox.SetItems
    
def droplist(parent): return DropDownListWidget(parent)


# 'id_droplist' type input parameter ===========================================
class TwoFieldsDropDownWidget(wx.ComboBox):
    def __init__(self, *a, **k):
        k['style'] = wx.CB_DROPDOWN|wx.CB_READONLY
        wx.ComboBox.__init__(self, *a, **k)
        self.ids = []
        self.Bind(wx.EVT_COMBOBOX, post_evt_param_changed)
        
    def SetBounds(self, bounds):
        self.ids = []
        self.Clear()
        for i in bounds:
            self.ids.append(i[0])
            self.Append(i[1])
    
    def SetValue(self, val):
        if val is None: 
            wx.ComboBox.SetSelection(self, -1)
            return
        wx.ComboBox.SetSelection(self, self.ids.index(val))
        
    def GetValue(self):
        return self.ids[self.GetSelection()]

def id_droplist(parent): return TwoFieldsDropDownWidget(parent)


# 'date' type input parameter ==================================================
class DateWidget(wx.DatePickerCtrl):
    def __init__(self, *a, **k):
        wx.DatePickerCtrl.__init__(self, *a, **k)
        self._min = None
        self._max = None
        self.Bind(wx.EVT_DATE_CHANGED, self.on_changed)

    def on_changed(self, evt):
        if (self._min is not None) and (self.GetValue() < self._min): 
            self.SetValue(self._min)
        elif (self._max is not None) and (self.GetValue() > self._max): 
            self.SetValue(self._max)
#        post_evt_param_changed(evt)
    
    def SetBounds(self, bounds):
        if bounds is None: return 
        self._min, self._max = bounds
        self.on_changed(None)
        
    def GetValue(self):
        y, m, d = map(int, 
                      wx.DatePickerCtrl.GetValue(self).FormatISODate().split('-'))
        return datetime.date(y, m, d)
    
    def SetValue(self, v):
        tt = v.timetuple()
        dmy = (tt[2], tt[1]-1, tt[0])
        wx.DatePickerCtrl.SetValue(self, wx.DateTimeFromDMY(*dmy))
        
def date(parent): return DateWidget(parent, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)


# 'period' type input parameter ================================================
class PeriodWidget(wx.Panel):
    def __init__(self, *a, **k):
        wx.Panel.__init__(self, *a, **k)
        self.period_from = DateWidget(self, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        self.period_to = DateWidget(self, style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        s = wx.FlexGridSizer(2, 2, 5, 5)
        s.AddGrowableCol(1)
        s.Add(wx.StaticText(self, -1, 'from'), 0, wx.ALIGN_CENTER_VERTICAL)
        s.Add(self.period_from, 1, wx.EXPAND|wx.ALL, 5)
        s.Add(wx.StaticText(self, -1, 'to'), 0, wx.ALIGN_CENTER_VERTICAL)
        s.Add(self.period_to, 1, wx.EXPAND|wx.ALL, 5)
        self.Bind(EVT_PARAM_CHANGED, self.on_date_changed)
        self.SetSizer(s)
    
    def on_date_changed(self, evt): 
        if evt: evt.Skip()
        from_, to = self.GetValue()
        if from_ > to:
            self.SetValue((to, to))
    
    def SetBounds(self, bounds):
        if bounds is None: return
        self.period_from.SetBounds(bounds)
        self.period_to.SetBounds(bounds)
                                   
    def SetValue(self, val):
        self.period_from.SetValue(val[0])
        self.period_to.SetValue(val[1])

    def GetValue(self):
        return self.period_from.GetValue(), self.period_to.GetValue()
        
def period(parent): return PeriodWidget(parent)


# 'fixed period family' type input parameters ==================================
from math import ceil
class FixedPeriodWidget(wx.Panel):
    months = 'January February March April May June July August September October November December'.split()
    spans = ',, bimester, trimester, quadrimester,, semester'.split(',')
    def __init__(self, *a, **k):
        self.period = k.pop('period')
        wx.Panel.__init__(self, *a, **k)
        if self.period == 1:
            ch = self.months
        else:
            ch = [str(i)+self.spans[self.period] for i in range(1, (12/self.period)+1)]
        self.division = wx.ComboBox(self, -1, choices=ch, 
                                    style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.year = wx.SpinCtrl(self, min=1800, max=2200, size=((80, -1)))
        s = wx.BoxSizer()
        s.Add(self.division, 1, wx.EXPAND|wx.RIGHT, 5)
        s.Add(self.year, 0, wx.FIXED_MINSIZE|wx.LEFT, 5)
        self.SetSizer(s)
        self.Bind(wx.EVT_COMBOBOX, self.on_changed, self.division)
        self.Bind(wx.EVT_SPINCTRL, self.on_changed, self.year)
    
    def on_changed(self, evt):
        evt.SetEventObject(self)
        post_evt_param_changed(evt)
        
    def GetValue(self):
        start = datetime.date(
                            self.year.GetValue(), 
                            ((self.period * self.division.GetSelection()) + 1),
                            1)
        end = ((start + 
               datetime.timedelta(days=(30*self.period)+15)).replace(day=1) - 
               datetime.timedelta(days=1))
        return start, end
    
    def SetValue(self, val):
        self.year.SetValue(val.year)
        self.division.SetSelection(int(ceil(float(val.month)/self.period))-1)
    
    def SetBounds(self, bounds): 
        if bounds is None: return
        try: min = bounds[0].year
        except AttributeError: min=None
        try: max = bounds[1].year
        except AttributeError: max=None
        self.year.SetRange(min, max)


def _fixed_period(period, parent): return FixedPeriodWidget(parent, period=period)

def month(parent): return _fixed_period(1, parent)
def bimester(parent): return _fixed_period(2, parent)
def trimester(parent): return _fixed_period(3, parent)
def quadrimester(parent): return _fixed_period(4, parent)
def semester(parent): return _fixed_period(6, parent)


