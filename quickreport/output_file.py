# -*- coding: utf8 -*-

"""Quickreport

Questo modulo comprende i generatori di output su file 
(testo, csv, html ed eventualmente excel).                                                        .

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
from gui_utils import ask_path

HTML_STYLE = """<style type="text/css">
table {width: 100%; margin-bottom: 10px; font-size: 1em; border-collapse: collapse;}
table caption {margin-top: 10px; padding: 0 0 0.5em 3px; 
               font: 150% georgia, sans-serif; text-align: left;}
table th, table td {text-align: left; vertical-align: top; 
                    padding: 4px 7px !important; padding: 6px 10px;}
thead th {text-align: left; vertical-align: top; background-color: #F1FFE3;
          border-bottom: 1px solid #B8E78B;}
tbody tr.dark {background-color: #F5F5F5;}
tbody td {border-bottom: 1px solid #DDD;}
tbody tr:hover {background-color: #FBFEDF;}
</style>"""


class BaseOutput(object):
    def __init__(self, parent_window, out_name, report, 
                 headers, col_types, first_row, data, **args):
        try:
            self.render_machine = PROJECT_RENDERERS_TABLE[(out_name, report)]()
        except KeyError:
            try: 
                self.render_machine = PROJECT_RENDERERS_TABLE[(out_name, '*')]()
            except KeyError:
                self.render_machine = RENDERERS_TABLE[out_name]()
        
        self.report = report
        self.path = ask_path(parent_window)
        self.headers = headers
        self.col_types = col_types
        self.first_row = first_row
        self.data = data
        
    def run(self): 
        if not self.path: return
        self.open_file()
        self.write_title()
        self.write_headers()
        self.renderers = [getattr(self.render_machine, t) for t in self.col_types]
        self.write_row(self.first_row)
        for row in self.data:
            self.write_row(row)
        self.close_file()
    
    def write_title(self): 
        self.renderers = [getattr(self.render_machine, 'text')]
        self.write_row([REP_NAMES[self.report]])
        
    def write_headers(self): 
        self.renderers = [getattr(self.render_machine, 'text')]*len(self.col_types)
        self.write_row(self.headers)
    
    def write_row(self, row): raise NonImplementedError
    def open_file(self):      raise NonImplementedError
    def close_file(self):     raise NonImplementedError


class TextOutput(BaseOutput):
    def __init__(self, *a, **k):
        BaseOutput.__init__(self, *a, **k)
        self.sep = k['sep']
        self.file_ext = k['file_ext']
        
    def open_file(self):
        self.file = open(self.path+self.file_ext, 'a')
        
    def close_file(self): 
        self.file.close()
        
    def write_row(self, row):
        for n, el in enumerate(row):
            if el is not None:
                self.file.write(self.renderers[n](el)+self.sep)
            else:
                self.file.write(self.sep)
        self.file.write('\n')


class HTMLOutput(BaseOutput):
    def __init__(self, *a, **k):
        BaseOutput.__init__(self, *a, **k)
        self.row_even = False
        
    def open_file(self):
        self.file = open(self.path+'.htm', 'a')
    
    def close_file(self): 
        self.file.write('</tbody>\n</table>\n</body>\n</html>\n')
        self.file.close()
        
    def write_title(self): 
        enc = QuickReportSettings().encoding
        txt = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=%s">
%s
<title>%s</title>
</head>
""" % (QuickReportSettings().encoding, HTML_STYLE, REP_NAMES[self.report])
        self.file.write(txt)
        
    def write_headers(self): 
        txt = """<body>\n<table>
<caption>%s</caption>
<thead>
<tr><th>%s</th></tr>
</thead>
<tbody>
""" % (REP_NAMES[self.report], '</th><th>'.join(self.headers))
        self.file.write(txt)
    
    def write_row(self, row):
        if self.row_even:
            txt = '<tr class="dark">'
        else:
            txt = '<tr>'
        self.row_even = not self.row_even
        for n, el in enumerate(row):
            if el is not None:
                txt += '<td>' + self.renderers[n](el) + '</td>'
            else:
                txt += '<td></td>'
        txt += '</tr>\n'
        self.file.write(txt)


try:
    from xlwt import Workbook
except ImportError:
    QuickReportSettings().HAVE_EXCEL = False

if QuickReportSettings().HAVE_EXCEL:
    class ExcelOutput(BaseOutput):
        def open_file(self):
            self.book = Workbook()
            self.sheet = self.book.add_sheet(self.report)
            self.current_row = 0
        
        def close_file(self):
            self.book.save(self.path+'.xls')
            
        def write_row(self, row):
            for col, val in enumerate(row):
                if val is not None: 
                    self.sheet.write(self.current_row, col, *self.renderers[col](val))
                else:
                    self.sheet.write(self.current_row, col, None)
            self.current_row += 1



FILE_AVAILABLE_OUTPUTS = ['text (tabs)', 'text (csv)', 'html']
if QuickReportSettings().HAVE_EXCEL: 
    FILE_AVAILABLE_OUTPUTS.append('excel')

FILE_DISPATCH_TABLE = {
        'text (tabs)'  : (TextOutput, {'sep':'\t', 'file_ext':'.txt'}),
        'text (csv)'   : (TextOutput, {'sep':';', 'file_ext':'.csv'}),
        'html'         : (HTMLOutput, {}),
                      }
if QuickReportSettings().HAVE_EXCEL: 
    FILE_DISPATCH_TABLE['excel'] = (ExcelOutput, {})


        
    
