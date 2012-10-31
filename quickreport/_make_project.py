#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Quickreport

Utilita' per creare nuovi progetti.

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""

import os, os.path
import sys

ALLOWED = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

MODULES = {
'__init__.py': ' ',
# ******************************************************************************
# ******************************************************************************
'enable_menus.py': '''# -*- coding: utf8 -*-

"""Quickreport - enable_menus.py

Questo modulo contiene funzioni che decidono se abilitare una specifica 
voce di menu. 
Tutte le funzioni qui definite devono ritornare True o False. 
Dopo averle definite, e' necessario registrare le funzioni nella DISPATCH_TABLE, 
associandole al nome del report che si desidera (dis)abilitare. 

La connessione al database e' disponibile come QuickReportSettings().db
"""

from ..settings import QuickReportSettings

# ==============================================================================
# definire qui le funzioni necessarie



# ==============================================================================
# non cambiare questa parte

def enable_menu(menu): 
    try:
        return DISPATCH_TABLE[menu]()
    except KeyError:
        return True


# ==============================================================================
# registrare le funzioni definite sopra, nella forma
# DISPATCH_TABLE = {'nick_del_report' : funzione, }

DISPATCH_TABLE = {

                 }

''',
# ******************************************************************************
# ******************************************************************************
'output_types.py' : '''# -*- coding: utf8 -*-

"""Quickreport - output_types.py

In questo modulo e' possibile fare due cose:
1) definire tipi per gli output personalizzati, in sostituzione/aggiunta 
a quelli definiti in quickreport.output_types
2) disabilitare alcuni output per specifici report (o per tutti i report)

Per la prima cosa, potete sostituire completamente le classi definite in 
quickreport.output_types, e creare una vostra gerarchia specifica per il progetto. 
Ma piu' probabilmente vorrete invece sottoclassare, e fare delle modifiche piu' 
marginali. In questo caso, la gerarchia predefinita e' disponibile in questo 
modulo come dfl_outputs.*
Ecco un esempio: volete che, in questo progetto, il tipo "date" sia renderizzato 
in tutti gli output come "giorno: ...". 
Dovete sostituire il rendering di "date" in tutti gli output messi a disposizione, 
sottoclassando in questo modo: 
class MyTextRenderer(dfl_outputs.TextRenderer): 
    def date(self, val): return val.strftime('giorno: %d.%m.%Y')
# etc. etc.

Fatto questo, dovete inserire le vostre sotto-classi 
nella tabella RENDERERS_TABLE: 

RENDERERS_TABLE = {'text (tabs)' : MyTextRenderer, <etc. etc.>}

La RENDERERS_TABLE definita in questo modo prende la precedenza su quella 
definita in quickreport.output_types. Cosi' tutto cio' che non e' definito in 
questa RENDERERS_TABLE ricade nei quickreport.output_types predefiniti. 


Per la seconda cosa, usate DISALLOW_OUTPUT per disabilitare certi output per 
certi report: per esempio, 
DISALLOW_OUTPUT = {'employees' : ('excel', 'screen'),
                   '*' : ('text (csv)')}
disabilita gli output "excel" e "screen" solo per il report "employees", 
e disabilita l'output "text (csv)" per _tutti_ i report di questo progetto. 
"""

import quickreport.output_types as dfl_outputs   # per i sottoclassamenti
from ..settings import QuickReportSettings
try:
    from xlwt import XFStyle
except ImportError:
    QuickReportSettings().HAVE_EXCEL = False


# ==============================================================================
# dichiarate qui le varie (sotto)classi dei renderer per i vari output



# ==============================================================================
# dichiarate qui le eventuali (sotto)classi che dipendono da HAVE_EXEL
if QuickReportSettings().HAVE_EXCEL:
    # class ...
    pass



# ==============================================================================
# Qui accoppiate le classi che avete definito sopra con i vari tipi di output. 
# Gli output possibili sono: 
# 'text (tabs)' , 'text (csv)' , 'html', 'excel' , 'screen'
# Usate la chiave ('output', '*') per accoppiare la classe al rendering 
# di _tutti_ i report per quell' 'output'.
# Usate la chiave ('output', 'nick_report') per accoppiare la classe 
# al rendering di _un_solo_report_ per quell' 'output'.

RENDERERS_TABLE = {
#                   ('text (tabs)', '*') : ...,
#                   ('text (csv)', '*')  : ...,
#                   ('html', '*')        : ...,
#                   ('screen', '*')      : ...,
                  }
#if QuickReportSettings().HAVE_EXCEL:
#    RENDERERS_TABLE[('excel', '*')] = ...



# ==============================================================================
# Disabilitate certi output per certi report, usando la forma
# DISALLOW_OUTPUT = {'nick_del_report' : (tupla degli output da disabilitare)}
# usate '*' al posto del nick per disabilitare un output per tutti i report.

DISALLOW_OUTPUT = {
                   
                  }

''',
# ******************************************************************************
# ******************************************************************************
'param_defaults.py' : '''# -*- coding: utf8 -*-

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


''',
# ******************************************************************************
# ******************************************************************************
'param_types.py': '''# -*- coding: utf8 -*-

"""Quickreport - param_types.py

Questo modulo raccoglie i tipi di parametro definiti nel progetto, da usare 
in aggiunta a quelli messi a disposizione in quickreport.param_types. 
Per un'idea di come definire i tipi, vedi anche quickreport.param_types. 

Per ogni tipo occorre definire una classe wx che definisce il widget da usare 
nella gui, e una funzione factory. 

La classe deve supportare queste API:
1) GetValue, che restituisce il valore del widget
  (usato al momento di raccogliere il valore del parametro per elaborare l'output)
2) SetValue, che assegna un valore al widget
  (usato per impostare il default del widget)
3) SetBounds, che assegna i bounds al widget (p. es. liste di possibili scelte, 
  minimi e massimi, etc.)
  (usato per impostare i bounds del widget)
4) Inoltre devono notificare il cambiamento di valore chiamando la funzione 
  post_evt_param_changed (gia' predisposta e importata)
I punti 2-4 non sono obbligatori, se non si intendono usare default, bounds, o 
recalc per il parametro (vedi params.py per i dettagli). In questo caso, 
bastera' fornire un'interfaccia vuota (con "pass"). 

La funzione factory deve avere il nome esatto del tipo di parametro, 
prende un solo argomento (il parent del widget), e restituisce 
una istanza del widget definito dalla classe. 

Schema di esempio che definisce il tipo "myparam":

class MyParamWidget(wx.<SomeCtrl>): 
    def __init__(self, *a, **k):
        wx.<SomeCtrl>.__init__(self, *a, **k)
        self.Bind(wx.<SOME_APPROPRIATE_EVENT>, post_evt_param_changed)
        # oppure anche:
        # self.Bind(wx.<SOME_APPROPRIATE_EVENT>, self.a_callback)
        
    def a_callback(self, evt):
        # processo l'evento internamente, e concludo:
        post_evt_param_changed(evt)
        
    def GetValue: 
        # ...
    def SetValue: pass
    def SetBounds: pass
    
def myparam(parent): return MyParamWidget(parent)
"""


import wx
from ..gui_utils import post_evt_param_changed


''',
# ******************************************************************************
# ******************************************************************************
'param_validators.py': '''# -*- coding: utf8 -*-

""" Quickreport - param_validators.py

Validatori wx definiti nel progetto. 
Le classi di validatori definite qui potranno essere importate in params.py 
come p_val.* (vedi params.py per i dettagli) e usate per validare i parametri.
"""

import wx


''',
# ******************************************************************************
# ******************************************************************************
'params.py' : '''# -*- coding: utf8 -*-

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
# Inserire qui i nomi dei report {nome_lungo : nick}

REP_NAMES = {

             }
REP_NAMES.update({v:k for k, v in REP_NAMES.iteritems()})



# ==============================================================================
# definire qui gli alberi dei menu (occorre almeno definire 'main_menu')

REPORT_MENUS = {
    'main_menu' : 
            (
                
            ),


}


# ==============================================================================
# elencare qui i parametri necessari per i report, nella forma:
# {report_nick : (tupla di parametri)
# Per i valori da specificare per ciascun parametro, 
# cfr. la docstring del modulo

PARAMETERS = {

}



''',
# ******************************************************************************
# ******************************************************************************      
'query.py' : '''# -*- coding: utf8 -*-

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

DISPATCH_TABLE = {
                  
                  }


''',
# ******************************************************************************
# ******************************************************************************  

}



d = os.path.dirname(__file__)

print 'Quickreport project start utility.\n==================================\n'
while True:
    p = raw_input('Insert project name or "q" to abort: ')
    if p == 'q': 
        sys.exit(0)
    if p in os.listdir(d): 
        print 'This name already exists\n'
    elif p.startswith(tuple('123456780')) or any(map(lambda x: x not in ALLOWED, p)):
        print 'Invalid name\n'
    else:
        os.mkdir(os.path.join(d, p))
        for m in MODULES:
            with open(os.path.join(d, p, m), 'a') as f:
                f.write(MODULES[m])
        raw_input('Done. Press <enter> to quit.\n')
        break

