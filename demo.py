#!/usr/bin/env python
# -*- coding: utf8 -*-
u"""\
BENVENUTI IN QUICKREPORT!
=========================

Quickreport è un framework per la generazione automatica dei report. 
Può essere usato all'interno di tutte le applicazioni wxPython \
che hanno bisogno di una sezione di reportistica (gestionali etc.). 

Questa è una piccola demo basata sul database Chinook \
(chinookdatabase.codeplex.com). 
Il menu "report" raccoglie alcuni esempi di report generati automaticamente \
con Quickreport. 
Quickreport permette di gestire contemporaneamente più menu in parti differenti \
della vostra interfaccia. Per esempio, facendo right-click su questa finestra, \
si aprirà un menu contestuale con alcuni altri report. 

Esplorate la demo, leggete la documentazione, ed eseguite lo script \
_start_project.py per iniziare a usare Quickreport nei vostri progetti!

==========================
Quickreport 
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""

import sqlite3
import wx 

# importare Quickreport: per prima cosa impostare il nome del progetto!
from quickreport.settings import QuickReportSettings
QuickReportSettings().current_project = 'chinook_demo'
# poi si puo' importare il resto...
from quickreport.gui import make_menu_report



class MyApp(wx.App):
    def OnInit(self):
        self.db = sqlite3.connect('chinook.sqlite', 
                                  detect_types=sqlite3.PARSE_DECLTYPES)
        # inizializzare Quickreport: 
        QuickReportSettings().db = self.db 
        QuickReportSettings().encoding = 'utf-8'
        return True
    
    
class Main(wx.Frame): 
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        
        # qui fingiamo di aver fatto login...
        QuickReportSettings().current_user = 1   
        
        menubar = wx.MenuBar()
        menu = make_menu_report(self)   # <- tutto cio' che serve!
        menubar.Append(menu, '&report')
        self.SetMenuBar(menubar)
        
        p = wx.Panel(self)
        p.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        t = wx.TextCtrl(p, -1, __doc__, style=wx.TE_MULTILINE|wx.TE_READONLY)
        t.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        s = wx.BoxSizer()
        s.Add(t, 1, wx.EXPAND|wx.ALL, 10)
        p.SetSizer(s)
        self.SetSize((500, 400))
        self.SetTitle('QUICKREPORT demo')

    def OnContextMenu(self, evt):
        menu = make_menu_report(self, 'context_menu')  # <- tutto cio' che serve!
        self.PopupMenu(menu)
        

app = MyApp(False)
Main(None).Show()
app.MainLoop()

