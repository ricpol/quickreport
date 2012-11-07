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
import wx.lib.masked as  masked
import datetime

from gui_utils import post_evt_param_changed, EVT_PARAM_CHANGED

__all__ = ['text', 'integer', 'boolean', 
           'symple_list', 'droplist', 
           'currency',
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
        self.multichoice = k.pop('multichoice')
        if self.multichoice:
            k['style'] = wx.LB_EXTENDED
        wx.ListBox.__init__(self, *a, **k)
        self.Bind(wx.EVT_LISTBOX, post_evt_param_changed)
        
    SetBounds = wx.ListBox.SetItems
    
    def SetValue(self, val):
        if self.multichoice:
            for v in val:
                self.SetStringSelection(v)
        else:
            self.SetStringSelection(val)
            
    def GetValue(self):
        if self.multichoice:
            return [self.GetString(i) for i in self.GetSelections()]
        else:
            return self.GetStringSelection()

class TwoFieldsListWidget(wx.ListBox):
    def __init__(self, *a, **k):
        self.multichoice = k.pop('multichoice')
        if self.multichoice:
            k['style'] = wx.LB_EXTENDED
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
        if self.multichoice:
            for v in val:
                self.SetSelection(self.ids.index(v))
        else:
            self.SetSelection(self.ids.index(val))
        
    def GetValue(self):
        if self.multichoice:
            return [self.ids[i] for i in self.GetSelections()]
        else:
            return self.ids[self.GetSelection()]

class MultiChoiceListWidget(wx.CheckListBox):
    def __init__(self, *a, **k):
        self.use_id = k.pop('use_id')
        wx.CheckListBox.__init__(self, *a, **k)
        if self.use_id:
            self.ids = []
        self.Bind(wx.EVT_CHECKLISTBOX, self._on_check)
    
    def _on_check(self, evt):
        self.SetSelection(evt.GetSelection())
        post_evt_param_changed(evt)
        
    def SetBounds(self, bounds):
        if self.use_id:
            self.ids = [i[0] for i in bounds]
            self.SetItems([i[1] for i in bounds]) 
        else:
            self.SetItems(bounds)
        
    def SetValue(self, val):
        if val is None: 
            self.SetSelection(-1)
            return
        if self.use_id:
            for v in val:
                self.SetSelection(self.ids.index(v))
        else:
            self.SetStringSelection(val)
        
    def GetValue(self):
        if self.use_id:
            return [self.ids[i] for i in self.GetSelections()]
        else:
            return self.GetStringSelection()
        
def symple_list(parent, use_id=False, multichoice=False): 
    if multichoice and wx.PlatformInfo[1] in ('wxMSW', 'wxGTK'):
        return MultiChoiceListWidget(parent, use_id=use_id)
    if use_id:
        return TwoFieldsListWidget(parent, multichoice=multichoice)
    else:
        return SimpleListWidget(parent, multichoice=multichoice)
        

# 'droplist' type input parameter ==============================================
class DropDownListWidget(wx.ComboBox):
    def __init__(self, *a, **k):
        k['style'] = wx.CB_DROPDOWN|wx.CB_READONLY
        wx.ComboBox.__init__(self, *a, **k)
        self.Bind(wx.EVT_COMBOBOX, post_evt_param_changed)
    
    SetBounds = wx.ComboBox.SetItems
    
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

def droplist(parent, use_id=False): 
    if use_id: return TwoFieldsDropDownWidget(parent)
    else: return DropDownListWidget(parent)


# 'currency' type input parameter ==============================================
EURO_CONVENTIONS = {  # note: actually, conventions for euro adopted in _Italy_!
    'mon_decimal_point': ',', 'int_frac_digits': 2, 'p_sep_by_space': 1, 
    'frac_digits': 2, 'thousands_sep': '.', 'n_sign_posn': 3, 'decimal_point': ',', 
    'int_curr_symbol': 'EUR', 'n_cs_precedes': 1, 'p_sign_posn': 3, 
    'mon_thousands_sep': '.', 'negative_sign': '-', 'currency_symbol': '\x80', 
    'n_sep_by_space': 1, 'mon_grouping': [3, 0], 'p_cs_precedes': 1, 
    'positive_sign': '', 'grouping': [3, 0]}
DOLLAR_CONVENTIONS = { # conventions for usd adopted in USA
    'mon_decimal_point': '.', 'int_frac_digits': 2, 'p_sep_by_space': 0, 
    'frac_digits': 2, 'thousands_sep': ',', 'n_sign_posn': 0, 'decimal_point': '.', 
    'int_curr_symbol': 'USD', 'n_cs_precedes': 1, 'p_sign_posn': 3, 
    'mon_thousands_sep': ',', 'negative_sign': '-', 'currency_symbol': '$', 
    'n_sep_by_space': 0, 'mon_grouping': [3, 0], 'p_cs_precedes': 1, 
    'positive_sign': '', 'grouping': [3, 0]}
POUND_CONVENTIONS = {  # conventions for pounds adopted in GB
    'mon_decimal_point': '.', 'int_frac_digits': 2, 'p_sep_by_space': 0, 
    'frac_digits': 2, 'thousands_sep': ',', 'n_sign_posn': 3, 'decimal_point': '.', 
    'int_curr_symbol': 'GBP', 'n_cs_precedes': 1, 'p_sign_posn': 3, 
    'mon_thousands_sep': ',', 'negative_sign': '-', 'currency_symbol': '\xa3', 
    'n_sep_by_space': 0, 'mon_grouping': [3, 0], 'p_cs_precedes': 1, 
    'positive_sign': '', 'grouping': [3, 0]}

class CurrencyWidget(wx.Panel):
    def __init__(self, *a, **k):
        use_decimal = k.pop('use_decimal')
        conv = k.pop('conventions')
        if conv == 'euro'    : conv = EURO_CONVENTIONS
        elif conv == 'dollar': conv = DOLLAR_CONVENTIONS
        elif conv == 'pound' : conv = POUND_CONVENTIONS
        wx.Panel.__init__(self, *a, **k)
        
        self.currency = masked.NumCtrl(self, limited=True,
            fractionWidth         = (conv['frac_digits'] if use_decimal else 0),
            groupDigits           = (conv['mon_grouping'][0]>0),
            groupChar             = conv['thousands_sep'],
            decimalChar           = conv['decimal_point'],
            useParensForNegatives = (conv['n_sign_posn']==0))
        self.currency.Bind(masked.EVT_NUM, post_evt_param_changed)
                           
        s = wx.BoxSizer()
        s.Add(wx.StaticText(self, -1, conv['currency_symbol']), 0, 
              wx.ALIGN_CENTER_VERTICAL, 0)
        s.Add(self.currency, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(s)
        
    def SetBounds(self, bounds):
        # TODO disconnect event 
        self.currency.SetMin(bound[0])
        self.currency.SetMax(bounds[1])
        
    def SetValue(self, val):
        # TODO disconnect event
        self.currency.SetValue(val)
        
    def GetValue(self): 
        return self.currency.GetValue()
        
def currency(parent, conventions='euro', use_decimal=True):
    return CurrencyWidget(parent, conventions=conventions, use_decimal=use_decimal)


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


