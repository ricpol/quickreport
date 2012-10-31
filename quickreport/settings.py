# -*- coding: utf8 -*-

"""Quickreport

Un singleton per raccogliere i parametri da condividere con l'applicazione wx 
"al di sopra" di Quickreport. 

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""
from locale import getpreferredencoding

class QuickReportSettings(object):
    def __new__(cls, *a, **k):
        if not hasattr(cls, '_inst'):
            cls._inst = super(QuickReportSettings, cls).__new__(cls, *a, **k)
        return cls._inst

    HAVE_EXCEL = True
    db = None
    current_project = None
    encoding = getpreferredencoding()
    
