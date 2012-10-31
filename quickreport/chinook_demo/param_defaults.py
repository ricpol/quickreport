# -*- coding: utf8 -*-

"""Quickreport - param_defaults.py

Funzioni per bounds default "dinamici" da assegnare ai parametri. 
Le funzioni definite in questo modulo restituiscono valori di default, bounds o 
entrambi per i parametri dei report, e possono essere usate in aggiunta a 
quelle "standard" messe a disposizione in quickreport.param_defaults.py. 

Queste funzioni sono richiamate dai 'func_default', 'func_bounds', e/o 
'default_bounds' assegnati al parametro (vedi params.py per i dettagli). 

Ciascuna funzione puo' ricevere dei named arguments (**kwargs), che corrispondono 
ai vari 'args_default', 'args_bounds', 'args_default_bounds', 'dep_default', 
'dep_bounds', 'dependencies' assegnati al parametro (vedi params.py per i 
dettagli). 

Queste funzioni probabilmente avranno bisogno di interrogare il database: l
a connessione al database e' disponibile come QuickReportSettings().db
"""

import datetime
from ..settings import QuickReportSettings

def search_artist(artist=''):
    if not artist: return None, []
    cur = QuickReportSettings().db.cursor()
    cur.execute("""SELECT ArtistId, Name FROM Artist 
                   WHERE Name LIKE ? ORDER BY Name;""", ('%'+artist+'%',))
    bounds = cur.fetchall()
    try: default = bounds[0][0]
    except IndexError: default = None
    return default, bounds

def artist_list():
    cur = QuickReportSettings().db.cursor()
    cur.execute('SELECT DISTINCT ArtistId, Name FROM Artist ORDER BY Name;')
    bounds = cur.fetchall()
    default = bounds[0][0]
    return default, bounds

def album_list(artist=None):
#    if artist is None: 
#        return None, []
    cur = QuickReportSettings().db.cursor()
    cur.execute("""SELECT DISTINCT AlbumId, Title FROM Album 
                   WHERE ArtistId=? ORDER BY Title;""", (artist,))
    bounds = cur.fetchall()
    try: default = bounds[0][0]
    except IndexError: default = None
    return default, bounds

def employee_title():
    cur = QuickReportSettings().db.cursor()
    cur.execute('SELECT DISTINCT Title FROM Employee ORDER BY Title;')
    bounds = [i[0] for i in cur.fetchall()]
    default = bounds[0] 
    return default, bounds
    
def country_invoces():
    cur = QuickReportSettings().db.cursor()
    cur.execute('SELECT DISTINCT BillingCountry FROM Invoice ORDER BY BillingCountry;')
    bounds = [i[0] for i in cur.fetchall()]
    default = bounds[0] 
    return default, bounds

def city_invoices(country=None):
    if country is None: 
        return None, []
    cur = QuickReportSettings().db.cursor()
    cur.execute("""SELECT DISTINCT BillingCity FROM Invoice 
                   WHERE BillingCountry=? ORDER BY BillingCity;""", (country,))
    bounds = [i[0] for i in cur.fetchall()]
    default = bounds[0] 
    return default, bounds
    
    
    