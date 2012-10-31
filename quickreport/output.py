# -*- coding: utf8 -*-

"""Quickreport

Questo modulo gestisce la generazione degli output, raccogliendo i dati da 
output_file, output_screen, <project>.output_types, e i valori dei parametri 
dalla gui.

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""

from importlib import import_module
from settings import QuickReportSettings
current_project = QuickReportSettings().current_project
_m = import_module('quickreport.'+current_project+'.output_types')
DISALLOW_OUTPUT = _m.DISALLOW_OUTPUT

from output_screen import SCREEN_AVAILABLE_OUTPUTS, SCREEN_DISPATCH_TABLE
from output_file import FILE_AVAILABLE_OUTPUTS, FILE_DISPATCH_TABLE


DISPATCH_TABLE = FILE_DISPATCH_TABLE
DISPATCH_TABLE.update(SCREEN_DISPATCH_TABLE)


def get_available_outputs(report):
    return ([i for i in FILE_AVAILABLE_OUTPUTS 
                if ((i not in DISALLOW_OUTPUT.get(report, []))
                   and (i not in DISALLOW_OUTPUT.get('*', [])))] +
            [i for i in SCREEN_AVAILABLE_OUTPUTS 
                if ((i not in DISALLOW_OUTPUT.get(report, []))
                    and (i not in DISALLOW_OUTPUT.get('*', [])))])
    

def generate_output(parent_window, report, out_name, 
                    headers, col_types, first_row, data):
    cls, args = DISPATCH_TABLE[out_name]
    cls(parent_window, out_name, report, 
        headers, col_types, first_row, data, **args).run()

