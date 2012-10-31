# -*- coding: utf8 -*-

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

def employee_list():
    "abilita solo se l'utente e' il gran capo o i suoi diretti sottoposti."
    cur = QuickReportSettings().db.cursor()
    cur.execute('SELECT ReportsTo FROM Employee WHERE EmployeeId=?;', 
                (QuickReportSettings().current_user,))
    a = cur.fetchall()[0][0]
    return a in (None, 1)


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

DISPATCH_TABLE = {'employees' : employee_list,
                 }

