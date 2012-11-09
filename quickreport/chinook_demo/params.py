# -*- coding: utf8 -*-

"""Quickreport - params.py.

Elenco dei report e dei parametri. 
In questo modulo sono definiti i nomi dei report, gli alberi dei menu, 
e i parametri di ciascun report. 

REP_NAMES contiene i nomi dei report: un nick, e il nome lungo che compare nei 
menu e come titolo del report nei vari output.

REPORT_MENUS elenca i nomi degli alberi dei menu. 

PARAMETERS elenca i parametri di ciascun report. 
Per ciascun parametro, occorrono quattro elementi:
- un nick univoco che identifica il parametro;
- una label descrittiva per la gui;
- un tipo, da scegliere tra i tipi "normali" messi a disposizione in 
  quickreport.param_types (qui importati con il nome typ.*) oppure un tipo 
  personalizzato, definito del param_types del progetto (qui importati come 
  p_typ.*);
- un dizionario di ulteriori elementi facoltativi. Se non c'e' bisogno di 
  elementi facoltativi, lasciare un dizionario vuoto. 
  
Gli elementi facoltativi che si possono aggiungere sono: 
- 'validator' -> un validatore (tra quelli messi a disposizione in
  quickreport.param_validators e importati come val.*, oppure definito nel 
  param_validators del progetto, e importato come p_val.*)
- 'null' -> se il paramentro puo' avere valore Null, una label per la gui 
- 'null_default' -> se True, il parametro e' Null per default (def.: False, 
  se non si inserisce questo elemento facoltativo)
- 'null_value' -> l'eventuale valore da dare allo stato di Null 
  (default: None, se non si inserisce questo elemento facoltativo)
- 'default' -> un valore di default per il parametro
- 'bounds' -> dei bounds per il parametro
- 'func_default' -> una funzione che restituisce un default (importata da 
  quickreport.param_defaults come dfl.*, oppure definita nel param_defaults 
  del progetto e importata come p_dfl.*)
- 'func_bounds' -> una funzione che restituisce dei bounds (importata come sopra)
- 'default_bounds' -> una funzione che restituisce default e bounds (importata
  come sopra)
- 'args_default' -> un dizionario di named arguments da passare a func_default
- 'args_bounds' -> un dizionario di named arguments da passare a func_bounds
- 'args_default_bounds' -> un diz. di named arguments da passare a default_bounds
- 'dep_default' -> una lista di altri parametri, il cui valore e' passato 
  a 'func_default' al momento di valutarla
- 'dep_bounds' -> una lista di altri parametri, il cui valore e' passato 
  a 'func_bounds' al momento di valutarla
- 'dependencies' -> una lista di altri parametri, il cui valore e' passato 
  a 'default_bounds' al momento di valutarla
- 'dependency_if_null' -> se True, e se il paramentro compare come "dependency" 
  di altri parametri, al momento della valutazione trasmette il valore effettivo 
  del parametro, senza contare lo stato eventuale di Null. 
  Defalut: False (se non si inserisce questo elemento facoltativo)
- 'recalc' -> una lista di altri parametri che devono essere ricalcolati 
  quando il valore di questo cambia
- 'recalc_on_null' -> se True (e se il parametro e' "nullable"), il ricalcolo 
  dei parametri nella lista "recalc" avviene anche quando cambia lo stato di 
  Null. Default: False (se non si inserisce questo elemento facoltativo)
"""

import quickreport.param_types as typ      # common param types
import param_types as p_typ                # project-defined param types

import quickreport.param_defaults as dfl   # common defaults
import param_defaults as p_dfl             # project-defined default

import quickreport.param_validators as val # common validators
import param_validators as p_val           # project-defined validators

from datetime import datetime as dt


# ==============================================================================
# Inserire qui i nomi dei report {nick : nome_per_finestra_param}

REP_NAMES = {
    'album_artist'       : 'Album by artist', 
    'tracks'             : 'Albums and tracks',
    'genres'             : 'List of genres',
    'employees'          : 'Employees list',
    'invoices_period'    : 'Invoices by period', 
    'invoices_trimester' : 'Invoices by trimester',
    'invoices_by_contry' : 'Invoices by country',
             }


# ==============================================================================
# definire qui gli alberi dei menu (occorre almeno definire 'main_menu')

REPORT_MENUS = {
    'main_menu' : 
            (
                ('Some reports', 
                    ('album_artist', 
                     'tracks')
                ),
                ('Another report', 
                    ('genres',)
                ),  
                'employees',
                '',   # <- this is a separator!
                ('Even more reports', 
                    (
                        ('two more', 
                            ('invoices_period', 
                             'invoices_trimester')
                        ),
                        ('one more',
                            ('invoices_by_contry',)
                        )
                    )
                ),
            ),

    'context_menu' : 
            (
                'album_artist', 
                'tracks',
                'genres',
            ),

}

# definire qui, per ciascun menu e per ciascun report elencato nel menu, 
# le label dei report (con le eventuali scorciatoie). 
# Occorre almeno definire 'main_menu'
REPORT_MENU_LABELS = {
    'main_menu' : {'album_artist'       : 'Album by &artist\tCtrl+1',  
                   'tracks'             : 'Albums and &tracks\tCtrl+2', 
                   'genres'             : 'List of &genres\tCtrl+3', 
                   'employees'          : 'Employees &list\tCtrl+4', 
                   'invoices_period'    : 'Invoices by &period\tCtrl+5',  
                   'invoices_trimester' : 'Invoices by &trimester\tCtrl+6', 
                   'invoices_by_contry' : 'Invoices by &country\tCtrl+7'},
                   
    'context_menu': {'album_artist' : 'Album by artist', 
                     'tracks'       : 'Albums and tracks',
                     'genres'       : 'List of genres'}
}

# ==============================================================================
# elencare qui i parametri necessari per i report, nella forma:
# {report_nick : (tupla di parametri)
# Per i valori da specificare per ciascun parametro, 
# cfr. la docstring del modulo

PARAMETERS = {
'album_artist': (
    ('artist', 'Search artist', typ.text, 
        {'recalc': ['sel_artist']}),
    ('sel_artist', 'Select artist', typ.droplist, 
        {'type_options': {'use_id':True}, 
         'default_bounds': p_dfl.search_artist, 'dependencies': ['artist']}),
    ),
'tracks': (
    ('artist', 'Artist', typ.droplist, 
        {'type_options': {'use_id':True}, 
         'null': 'All', 'null_default': True, 'default_bounds': p_dfl.artist_list,
         'recalc': ['album'], 'recalc_on_null': True, 'dependency_if_null': True}),
    ('album', 'Title of Album', typ.droplist, 
        {'type_options': {'use_id':True}, 
         'null': 'All', 'null_default': True, 'default_bounds': p_dfl.album_list,
         'dependencies': ['artist']}),
    ('sold', 'Show only tracks that have been sold (at least once)', typ.boolean, 
        {'default': False}),
    ),
'employees': (
    ('pos', 'Position', typ.symple_list, 
        {'default_bounds': p_dfl.employee_title, 
         'null': 'All', 'null_default': True}),
    ),
'invoices_period': (
    ('period', 'Period', typ.period, 
       {'func_bounds': dfl.years_span, 'func_default': dfl.years_span, 
       'args_bounds': {'min_offset':-2, 'max_offset':+1},
       'args_default': {'min_offset':-2, 'max_offset':+1}, 
       'validator': val.ValidPeriod}),
    ),
'invoices_trimester': (
    ('period', 'Period', typ.trimester, 
        {'bounds': (dt(2007, 1, 1), dt(2012, 1, 1)), 'default': dt(2011, 1, 1)}),
    ),
'invoices_by_contry': (
    ('country', 'Contry', typ.droplist, 
        {'null': 'All', 'default_bounds': p_dfl.country_invoces, 
         'recalc': ['city'], 'recalc_on_null': True, 'dependency_if_null': True}),
    ('city', 'City', typ.droplist,
        {'null': 'All', 'default_bounds': p_dfl.city_invoices, 
         'dependencies': ['country']})
    ),
}



