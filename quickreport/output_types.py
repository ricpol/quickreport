# -*- coding: utf8 -*-

"""Quickreport

Questo modulo comprende le varie "rendering machine" per i tipi degli output. 

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""


import datetime
from settings import QuickReportSettings


class DefaultRenderer(object):
    def __init__(self):
        self.ENC = QuickReportSettings().encoding
    # TODO: implementare un fallback totale con __getattr__ ?


class TextRenderer(DefaultRenderer):
    def text(self, val): return val.encode(self.ENC)
    def int_(self, val): return str(val)
    def float_(self, val): return str(val)
    def timestamp(self, val): return val.strftime('%d.%m.%Y %H:%M')
    def date(self, val): return val.strftime('%d.%m.%Y')
    def time(self, val): return val.strftime('%H:%M')
    def check(self, val): return 'X' if val is True else ''
    def bool_(self, va): return 'T' if val is True else 'F'
    def bool_01(self, val): return 'T' if val==1 else 'F'


class ScreenRenderer(TextRenderer): 
    def text(self, val): return val


class CsvRenderer(TextRenderer):
    def text(self, val): 
        val = val.replace(';', ',')
        return val.encode(ENC)


class HtmlRenderer(TextRenderer): pass


try:
    from xlwt import XFStyle
except ImportError:
    QuickReportSettings().HAVE_EXCEL = False

if QuickReportSettings().HAVE_EXCEL:
    class ExcelRenderer(DefaultRenderer):
        def __init__(self):
            self.STYLES = {}
            for s in ('timestamp', 'date', 'time', 'bool_01'):
                self.STYLES[s] = XFStyle()
            self.STYLES['timestamp'].num_format_str = 'DD-MM-YYYY h:mm' 
            self.STYLES['date'].num_format_str = 'DD-MM-YYYY' 
            self.STYLES['time'].num_format_str = 'h:mm'
            self.STYLES['bool_01'].num_format_str = '"T";;"F"' 
        
        def text(self, val): return (val,)
        def int_(self, val): return (val,)
        def float_(self, val): return (val,)
        def timestamp(self, val): return (val, self.STYLES['timestamp'])
        def date(self, val): return (val, self.STYLES['date'])
        def time(self, val): return (val, self.STYLES['time'])
        def check(self, val): return (('X' if val is True else ''),)
        def bool_(self, va): return (int(val), self.STYLES['bool_01'])
        def bool_01(self, val): return (val, self.STYLES['bool_01'])



RENDERERS_TABLE = {'text (tabs)' : TextRenderer,
                   'text (csv)'  : CsvRenderer,
                   'html'        : HtmlRenderer,
                   'screen'      : ScreenRenderer,
                  }
if QuickReportSettings().HAVE_EXCEL:
    RENDERERS_TABLE['excel'] = ExcelRenderer
