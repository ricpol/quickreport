# -*- coding: utf8 -*-

"""Quickreport

Funzioni per default/bounds dei parametri. 
Questo modulo contiene alcune funzioni "standard" che possono essere utili 
in tutti i progetti. 

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""

import datetime
from settings import QuickReportSettings

def date_today(offset=0):
    'Restituisce la data di oggi +/- offset (giorni).'
    return datetime.date.today()+datetime.timedelta(days=offset)

def years_span(min_offset=-10, max_offset=10):
    """Restituisce l'anno attuale + min_offset e l'anno attule + max_offset.
       @returns: (datetime.date, datetime.date)
    """
    y = datetime.date.today().year
    return (datetime.date(y+min_offset, 1, 1), datetime.date(y+max_offset, 1, 1))

def today_years_span(min_offset=-10, max_offset=10):
    """Restituisce la data di oggi, e l'anno attuale + min_offset / max_offset 
       (cfr. years_span). 
       @ returns: (datetime.date, (datetime.date, datetime.date))
    """
    return datetime.date.today(), (years_span(min_offset, max_offset))


