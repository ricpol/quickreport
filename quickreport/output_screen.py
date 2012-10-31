# -*- coding: utf8 -*-

"""Quickreport

Questo modulo contiene la gui per l'output su schermo.

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""

from importlib import import_module
from settings import QuickReportSettings
current_project = QuickReportSettings().current_project
_m = import_module('quickreport.'+current_project+'.params')
REP_NAMES = _m.REP_NAMES
_m = import_module('quickreport.'+current_project+'.output_types')
PROJECT_RENDERERS_TABLE = _m.RENDERERS_TABLE

from output_types import RENDERERS_TABLE

import wx


class OutputFrame(wx.Frame):   
    def __init__(self, parent_window, out_name, report, 
                 headers, col_types, first_row, data, **args):  
        wx.Frame.__init__(self, parent_window.GetParent()) 
        p = wx.Panel(self)
        p.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.title_label = wx.StaticText(p, -1, REP_NAMES[report])
        self.title_label.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.list = wx.ListCtrl(p, -1, style=wx.LC_REPORT)
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self.title_label, 0, wx.ALL, 5)
        s.Add(self.list, 1, wx.ALL|wx.EXPAND, 5)
        p.SetSizer(s)
        self.SetTitle('Report')
        self.headers = headers
        self.first_row = first_row
        self.data = data
        try:
            render_machine = PROJECT_RENDERERS_TABLE[(out_name, report)]()
        except KeyError:
            try: 
                render_machine = PROJECT_RENDERERS_TABLE[(out_name, '*')]()
            except KeyError:
                render_machine = RENDERERS_TABLE[out_name]()
        self.renderers = [getattr(render_machine, t) for t in col_types]
        
    def run(self):
        for n, h in enumerate(self.headers): 
            self.list.InsertColumn(n, h) 
        self.append_row(self.first_row)
        for row in self.data:
            self.append_row(row)
        self.Show()
    
    def append_row(self, row):
        transl_row = []
        for n, el in enumerate(row):
            if el is not None:
                transl_row.append(self.renderers[n](el))
            else:
                transl_row.append('')
        self.list.Append(transl_row)
        

SCREEN_AVAILABLE_OUTPUTS = ['screen']

SCREEN_DISPATCH_TABLE = {
        'screen'       : (OutputFrame, {}),
                        }


