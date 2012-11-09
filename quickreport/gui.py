# -*- coding: utf8 -*-
"""Quickreport

La gui di Quickreport: i menu e la finestra dei parametri.

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""

from importlib import import_module
import wx
import wx.lib.scrolledpanel as scrolled

from settings import QuickReportSettings
current_project = QuickReportSettings().current_project

_m = import_module('quickreport.'+current_project+'.params')
PARAMETERS = _m.PARAMETERS
REPORT_MENUS = _m.REPORT_MENUS
REP_NAMES = _m.REP_NAMES
REPORT_MENU_LABELS = _m.REPORT_MENU_LABELS

_m = import_module('quickreport.'+current_project+'.enable_menus')
enable_menu  = _m.enable_menu

_m = import_module('quickreport.'+current_project+'.query')
get_query = _m.get_query

from gui_utils import EVT_PARAM_CHANGED
from output import generate_output, get_available_outputs


def make_menu(menu_name, items, parent, callback):
    menu = wx.Menu()
    for item in items:
        if isinstance(item, tuple):
            menu.AppendMenu(-1, item[0], make_menu(menu_name, item[1], parent, callback))
        else:
            if not item:
                menu.AppendSeparator()
                continue
            menuItem = menu.Append(-1, REPORT_MENU_LABELS[menu_name][item])
            menuItem.Enable(enable_menu(item))
            parent.Bind(wx.EVT_MENU, 
                        lambda evt, parent=parent, item=item: callback(parent, item),
                        menuItem)
    return menu



def report_dispatcher(parent, label):
    ParametersDialog(parent, report=label).ShowModal()
    

def make_menu_report(parent, menu_name='main_menu'):
        return make_menu(menu_name, REPORT_MENUS[menu_name], parent, report_dispatcher)






class ParametersPanel(scrolled.ScrolledPanel):
    def __init__(self, *a, **k):
        k['style'] = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER
        report_name = k.pop('report') 
        scrolled.ScrolledPanel.__init__(self, *a, **k)
        
        self.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.param_options = {}
        self.param_widgets = {} 
        self.null_widgets = {} 
        
        s = wx.BoxSizer(wx.VERTICAL)
        parameters = PARAMETERS.get(report_name, [])
        for param, label, input_type, options in parameters:
            type_options = options.get('type_options', {})
            self.param_widgets[param] = input_type(self, **type_options)
            self.param_widgets[param].SetName(param)
            self.param_widgets[param].Bind(EVT_PARAM_CHANGED, self.on_param_changed)
            self.param_options[param] = options
            
            # resolving static bounds first, if present
            b = options.get('bounds', None)
            if b and (not callable(b)):
                self.param_widgets[param].SetBounds(b)
            
            # setting validator, if present:
            try:
                self.param_widgets[param].SetValidator(options['validator']())
            except KeyError:
                pass

            # 'null' option parsing:
            null_label = options.get('null', '')
            if null_label:
                null_checked = options.get('null_default', False)
                self.null_widgets[param] = wx.CheckBox(self, -1, null_label, name=param)
                self.Bind(wx.EVT_CHECKBOX, self.on_check, self.null_widgets[param])
                self.null_widgets[param].SetValue(null_checked)
                self.param_widgets[param].Enable(not null_checked)

            # packing widgets in sizers...
            s.Add(wx.StaticText(self, -1, label), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
            s1 = wx.BoxSizer()
            s1.Add(self.param_widgets[param], 1, wx.EXPAND|wx.ALL, 5)
            if null_label:
                s1.Add(self.null_widgets[param], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
            s.Add(s1, 0, wx.EXPAND)
            s.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(s)
        self.SetupScrolling()

        # bounds/default initial setting (we must follow the parameter list order): 
        for param, label, input_type, options in parameters:
            self.set_default_and_bounds(param)

    def set_default_and_bounds(self, param_name):
        options = self.param_options[param_name]
        set_bounds, set_default = False, False
        args = {}
        deps = options.get('dependencies', [])
        for dep in deps:
            if self.param_options[dep].get('dependency_if_null', False):
                args[dep] = self.param_widgets[dep].GetValue()
            else:
                args[dep] = self.get_param_data(dep)
            
        if options.get('default_bounds'):
            args.update(options.get('args_default_bounds', {}))
            default, bounds = options['default_bounds'](**args)
            set_bounds, set_default = True, True
        else:
            if options.get('func_bounds'):
                args.update(options.get('args_bounds', {}))
                bounds = options['func_bounds'](**args)
                set_bounds = True
            if options.get('func_default'):
                args.update(options.get('args_default', {}))
                default = options['func_default'](**args)
                set_default = True
            else:
                try:
                    default = options['default']
                    set_default = True
                except KeyError:
                    pass
                
        if any((set_bounds, set_default)):
            widget = self.param_widgets[param_name]
            widget.SetEvtHandlerEnabled(False)
            if set_bounds:
                widget.SetBounds(bounds)
            if set_default:
                self.set_param_data(param_name, default)
            widget.Refresh()
            widget.SetEvtHandlerEnabled(True)
    
    def on_param_changed(self, evt):
        # wx.SafeYield(None, True)
        for param in self.param_options[evt.param_name].get('recalc', []):
            self.set_default_and_bounds(param)
        
    def on_check(self, evt):
        param_name = evt.GetEventObject().GetName()
        self.param_widgets[param_name].Enable(not evt.IsChecked())
        if self.param_options[param_name].get('recalc_on_null', False):
            for param in self.param_options[param_name].get('recalc', []):
                self.set_default_and_bounds(param)
    
    def set_param_data(self, param_name, data):
        widget = self.param_widgets[param_name]
        if param_name in self.null_widgets and data == self.param_options[param_name].get('null_value', None):
            self.null_widgets[param_name].SetValue(True)
            widget.Enable(False)
        else:
            widget.SetValue(data)
                 
    def get_param_data(self, param_name):
        if (param_name in self.null_widgets) and self.null_widgets[param_name].IsChecked():
            return self.param_options[param_name].get('null_value', None)
        else:
            return self.param_widgets[param_name].GetValue()

    def get_data(self):
        data = {}
        for param in self.param_widgets:
            data[param] = self.get_param_data(param)
        return data


class ParametersDialog(wx.Dialog): 
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        self.report = kwds.pop('report') 
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        l = wx.StaticText(self, -1, REP_NAMES[self.report])
        l.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.pan = ParametersPanel(self, report=self.report)
        ok = wx.Button(self, -1, 'R E P O R T')
        ok.Bind(wx.EVT_BUTTON, self.on_ok)
        self.available_outputs = get_available_outputs(self.report)
        self.output_doc = wx.ComboBox(self, -1, 
                                      choices=self.available_outputs, 
                                      style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.output_doc.SetValue(self.available_outputs[0])
        
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(l, 0, wx.ALL, 5)
        s.Add(self.pan, 1, wx.ALL|wx.EXPAND, 5)
        s1 = wx.BoxSizer()
        s1.Add(ok, 3, wx.ALL|wx.EXPAND, 5)
        s1.Add(self.output_doc, 2, wx.ALL|wx.EXPAND, 5)
        s.Add(s1, 0, wx.EXPAND)
        self.SetSizer(s)
        self.SetTitle('Report')
        self.Layout()

    def on_ok(self, evt):
        if not self.pan.Validate():
            return
        params = self.pan.get_data()
        data = get_query(self.report, params)
        
        headers = data.next()
        col_types = data.next()
        try:
            first_row = data.next()
        except StopIteration:
            wx.MessageBox('Sorry, no data.', 'Report', wx.OK|wx.ICON_INFORMATION)
            return
        
        out_name = self.available_outputs[self.output_doc.GetSelection()]
        generate_output(self, self.report, out_name, 
                        headers, col_types, first_row, data)


