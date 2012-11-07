# -*- coding: utf8 -*-
"""Quickreport

Una piccola piattaforma per testare i widget.

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""
import sys, os, os.path
import wx

sys.path.append(os.path.dirname(os.getcwd()))

from quickreport.settings import QuickReportSettings
QuickReportSettings().current_project = 'chinook_demo'
import quickreport.param_types as typ 
import quickreport.gui as gui 
from quickreport.gui_utils import post_evt_param_changed, EVT_PARAM_CHANGED

def mock_param_changed(self, evt):
    evt.SetEventObject(self)
    post_evt_param_changed(evt)
setattr(gui.ParametersPanel, 'on_param_changed', mock_param_changed)
    
class TestBoard(wx.Frame):
    def __init__(self, *a, **k):
        wx.Frame.__init__(self, *a, **k)
        
        self.created_widgets = []
        
        p = wx.Panel(self)
        p.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.created = wx.ListBox(p)
        getvalue = wx.Button(p, -1, 'get', size=(30, -1))
        getvalue.Bind(wx.EVT_BUTTON, self.on_getvalue)
        self.types = wx.ComboBox(p, choices=typ.__all__, style=wx.CB_READONLY)
        self.bounds = wx.TextCtrl(p)
        self.default = wx.TextCtrl(p)
        self.nullable = wx.CheckBox(p)
        self.options = wx.TextCtrl(p, style=wx.TE_MULTILINE)
        create = wx.Button(p, -1, 'create widget')
        create.Bind(wx.EVT_BUTTON, self.on_create)
        self.newbounds = wx.TextCtrl(p)
        self.newdefault = wx.TextCtrl(p)
        set_bounds = wx.Button(p, -1, 'set', size=(30, -1))
        set_bounds.Bind(wx.EVT_BUTTON, self.on_set_bounds)
        set_default = wx.Button(p, -1, 'set', size=(30, -1))
        set_default.Bind(wx.EVT_BUTTON, self.on_set_default)
        
        for ctl in (self.bounds, self.default, self.options, 
                    self.newbounds, self.newdefault):
            ctl.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL))
        
        s = wx.BoxSizer(wx.VERTICAL)
        s1 = wx.BoxSizer()
        s1.Add(self.created, 1, wx.EXPAND|wx.ALL, 5)
        s1.Add(getvalue, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        s.Add(s1, 1, wx.EXPAND, 0)
        s1 = wx.FlexGridSizer(5, 2, 5, 5)
        s1.AddGrowableCol(1)
        s1.AddGrowableRow(4)
        for l, ctl in (('types', self.types), 
                       ('bounds', self.bounds), ('default', self.default), 
                       ('null', self.nullable), ('options', self.options)):
            s1.Add(wx.StaticText(p, -1, l), 0, wx.ALIGN_CENTER_VERTICAL)
            s1.Add(ctl, 1, wx.EXPAND)
        s.Add(s1, 2, wx.EXPAND|wx.ALL, 5)
        s.Add(create, 0, wx.EXPAND|wx.ALL, 5)
        s1 = wx.FlexGridSizer(2, 3, 5, 5)
        s1.AddGrowableCol(1)
        for l, ctl, b in (('re-bnds', self.newbounds, set_bounds), 
                          ('re-def.', self.newdefault, set_default)):
            s1.Add(wx.StaticText(p, -1, l), 0, wx.ALIGN_CENTER_VERTICAL)
            s1.Add(ctl, 1, wx.EXPAND)
            s1.Add(b, 0, wx.EXPAND)
        s.Add(s1, 0, wx.EXPAND|wx.ALL, 5)
        p.SetSizer(s)
        
        self.SetTitle('Input Parameter Test')
        self.SetSize((400, 450))
    
    def notify_destroy(self, child_name):
        self.created_widgets.remove(child_name)
        self.created.SetItems(self.created_widgets)
        
    def on_create(self, evt):
        widget = self.types.GetStringSelection()
        if not widget: return
        id = wx.NewId()
        title = '[%i] %s' % (id, widget)
        
        widget = getattr(typ, widget)
        bounds = self.bounds.GetValue().strip()
        default = self.default.GetValue().strip()
        nullable = self.nullable.GetValue()
        options = self.options.GetValue().strip()
        args = {}
        if bounds: args['bounds'] = eval(bounds)
        if default: args['default'] = eval(default)
        if nullable: args['null'] = 'nullable'
        if options: args['type_options'] = eval(options)
        gui.PARAMETERS = {'test':(('test_param', 'test_param', widget, args),)}
        ParamWindow(self, id, title, size=(-1, 150), name=title).Show()
        self.created_widgets.append(title)
        self.created.SetItems(self.created_widgets)
        
    def on_set_bounds(self, evt):
        widget = self.created.GetStringSelection()
        if not widget: return
        bounds = self.newbounds.GetValue().strip()
        if not bounds: return
        wx.FindWindowByName(widget).SetBounds(eval(bounds))
    
    def on_set_default(self, evt):
        widget = self.created.GetStringSelection()
        if not widget: return
        default = self.newdefault.GetValue().strip()
        if not default: return
        wx.FindWindowByName(widget).SetDefault(eval(default))

    def on_getvalue(self, evt):
        widget = self.created.GetStringSelection()
        if not widget: return
        print 'value:', wx.FindWindowByName(widget).GetValue()
        

class ParamWindow(wx.Frame):
    def __init__(self, *a, **k):
        wx.Frame.__init__(self, *a, **k)
        p = wx.Panel(self)
        self.param = gui.ParametersPanel(p, report='test')
        self.track_changes = wx.CheckBox(p, -1, 'track parameter changes')
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self.param, 1, wx.EXPAND)
        s.Add(self.track_changes, 0, wx.EXPAND|wx.ALL, 5)
        p.SetSizer(s)
        self.Bind(EVT_PARAM_CHANGED, self.on_param_changed)
        self.Bind(wx.EVT_CLOSE, self.on_close)
    
    def on_param_changed(self, evt):
        if self.track_changes.GetValue(): 
            print 'change detected in', self.GetTitle()
            
    def on_close(self, evt):
        self.GetParent().notify_destroy(self.GetTitle())
        evt.Skip()
    
    def GetValue(self): 
        return self.param.get_data()
    
    def SetBounds(self, bounds):
        self.param.param_options['test_param']['bounds'] = bounds
        self.param.set_default_and_bounds('test_param')
    
    def SetDefault(self, bounds):
        self.param.param_options['test_param']['default'] = bounds
        self.param.set_default_and_bounds('test_param')


app = wx.App()
TestBoard(None).Show()
app.MainLoop()

