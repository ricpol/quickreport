# -*- coding: utf8 -*-

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


