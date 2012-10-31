# -*- coding: utf8 -*-

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

class ChinookTextRenderer(dfl_outputs.TextRenderer):
    def date(self, val): return val.strftime('%Y-%m-%d')

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
                   ('screen', '*')      : ChinookTextRenderer,
                  }
#if QuickReportSettings().HAVE_EXCEL:
#    RENDERERS_TABLE[('excel', '*')] = ...



# ==============================================================================
# Disabilitate certi output per certi report, usando la forma
# DISALLOW_OUTPUT = {'nick_del_report' : (tupla degli output da disabilitare)}
# usate '*' al posto del nick per disabilitare un output per tutti i report.

DISALLOW_OUTPUT = {
                   '*'         : ('text (csv)',),   # per tutti!!
                   'employees' : ('excel',),
                  }



