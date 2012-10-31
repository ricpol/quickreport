# -*- coding: utf8 -*-

"""Quickreport - query.py
Questo modulto contiene le query necessarie per produrre i report. 

Ogni funzione definita qui dovrebbe produrre:
- "fields", una tupla di stringhe per le intestazioni di colonne
- "field_types", una tupla di stringhe per i tipi per i campi (tra quelli compresi 
  in quickreport.output_types.__all__, o definiti nel progetto in 
  output_types)
- uno statement sql 
- una tupla di parametri per la stringa sql
Fatto questo, basta passare questi elementi alla funzione di convenienza 
_sql_exec, concludendo la funzione in questo modo: 
        return _sql_exec(fields, field_types, sql, params)

Infine, occorre inserire la funzione definita nella tabella DISPATCH_TABLE
"""


# ==============================================================================
# definire qui sotto le funzioni necessarie a produrre gli output dei report

def album_artist(params):
    fields = ('Artist', 'Album', 'Track')
    field_types = 'text text text'.split()
    sql = """SELECT Artist.Name, Title, Track.Name
             FROM Track JOIN Album ON Track.AlbumId=Album.AlbumId 
             JOIN Artist ON Album.ArtistId=Artist.ArtistId 
             WHERE Artist.ArtistId=? ORDER BY Artist.Name, Title, Track.Name;""" 
    return _sql_exec(fields, field_types, sql, (params['sel_artist'],))


def invoices_period(params):
    fields = ('Customer', 'City', 'Country', 'Date', 'Total')
    field_types = ('text', 'text', 'text', 'date', 'float_')
    sql = """SELECT LastName || ", " || FirstName AS CustomerName, 
             BillingCity, BillingCountry, InvoiceDate, Invoice.Total 
             FROM Invoice JOIN Customer ON Invoice.CustomerId=Customer.CustomerId 
             WHERE InvoiceDate>? AND InvoiceDate<? ORDER BY InvoiceDate;"""
    return _sql_exec(fields, field_types, sql, params['period'])


def tracks(params):
    fields = ('Artist', 'Album', 'Track', 'Composer', 'Price')
    field_types = 'text text text text float_'.split()
    p = ()
    where, distinct, join = '', '', ''
    if params['artist']:
        p = (params['artist'],)
        where = 'WHERE Artist.ArtistId=?'
    if params['album']:
        p = (params['album'],)
        where = 'WHERE Album.AlbumId=?'
    if params['sold']:
        distinct = 'DISTINCT'
        join = 'JOIN InvoiceLine ON Track.TrackId=InvoiceLine.TrackId'
    sql = """SELECT %s Artist.Name, Title, Track.Name, Composer, Track.UnitPrice 
             FROM Track JOIN Album ON Track.AlbumId=Album.AlbumId 
             JOIN Artist ON Album.ArtistId=Artist.ArtistId %s %s 
             ORDER BY Artist.Name, Title, Track.Name;""" % (distinct, join, where)
    return _sql_exec(fields, field_types, sql, p)


def genres(params):
    fields = ('Genre', 'Tracks')
    field_types = ('text', 'int_')
    sql = """SELECT Genre.Name, count(TrackId)
             FROM Genre JOIN Track ON Genre.GenreId=Track.GenreId 
             GROUP BY Genre.Name ORDER BY Genre.Name;"""
    return _sql_exec(fields, field_types, sql)


def invoices_by_country(params):
    fields = ('Customer', 'City', 'Country', 'Date', 'Total')
    field_types = ('text', 'text', 'text', 'date', 'float_')
    p = ()
    where = ''
    if params['country']:
        where = 'WHERE Country=?'
        p = (params['country'],)
    if params['city']:
        where = 'WHERE City=?'
        p = (params['city'],)
    sql = """SELECT LastName || ", " || FirstName AS CustomerName, 
             BillingCity, BillingCountry, InvoiceDate, Invoice.Total 
             FROM Invoice JOIN Customer ON Invoice.CustomerId=Customer.CustomerId 
             %s ORDER BY CustomerName;""" % where
    return _sql_exec(fields, field_types, sql, p)


def employees(params):
    fields = ('Last Name', 'First Name', 'Position', 'Hire Date', 'reports')
    field_types = ('text', 'text', 'text', 'date', 'int_')
    sql = 'SELECT LastName, FirstName, Title, HireDate, ReportsTo FROM Employee'
    p = ()
    if params['pos']: 
        sql += ' WHERE Title=?'
        p = (params['pos'],)
    sql += ' ORDER BY LastName;'
    return _sql_exec(fields, field_types, sql, p)



# ==============================================================================
# non modificare questa parte

from ..settings import QuickReportSettings
def _sql_exec(fields, field_types, sql, params=()):
    yield fields
    yield field_types
    cur = QuickReportSettings().db.cursor()
    cur.execute(sql, params)
    while True:
        row = cur.fetchone()
        if not row:
            raise StopIteration
        yield row 

def get_query(report, params):
    return DISPATCH_TABLE[report](params)
    
    
# ==============================================================================
# inserire qui la funzione definita sopra, nella forma
# {nick_del_report : funzione}

DISPATCH_TABLE = {'album_artist' : album_artist,
                  'invoices_period' : invoices_period,
                  'invoices_trimester' : invoices_period,
                  'tracks' : tracks,
                  'genres' : genres,
                  'invoices_by_contry' : invoices_by_country,
                  'employees' : employees,
                  }

