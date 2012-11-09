# -*- coding: utf8 -*-
"""Quickreport

Una piccola piattaforma per testare i widget.

==========================================
:version: vedi quickreport.__version.py__
:copyright: Riccardo Polignieri 2012
:license: ISC
"""
import sys, os, os.path
import wx
import wx.stc as stc
sys.path.append(os.path.dirname(os.getcwd()))

from quickreport.settings import QuickReportSettings
QuickReportSettings().current_project = 'chinook_demo'
import quickreport.param_types as typ 
import quickreport.gui as gui 
from quickreport.gui_utils import post_evt_param_changed, EVT_PARAM_CHANGED

def mock_param_changed(self, evt):
    evt.SetEventObject(self)
    post_evt_param_changed(evt)
setattr(gui.ParametersPanel, 'on_param_changed', mock_param_changed)


# ==============================================================================
# adapted from wxPyhon demo
styles = (
    (stc.STC_STYLE_DEFAULT, "face:Courier New,size:10"),
    (stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold"),
    (stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold"),
    # Python styles
    (stc.STC_P_DEFAULT, "fore:#000000,face:Courier New,size:10"), # Default 
    (stc.STC_P_NUMBER, "fore:#007F7F,size:10"), # Number
    (stc.STC_P_STRING, "fore:#7F0000,face:Courier New,size:10"), # String
    (stc.STC_P_CHARACTER, "fore:#7F0000,face:Courier New,size:10"), # Single quoted string
    (stc.STC_P_WORD, "fore:#00007F,bold,size:10"), # Keyword
    (stc.STC_P_OPERATOR, "bold,size:10"), # Operators
    (stc.STC_P_IDENTIFIER, "fore:#000000,face:Courier New,size:10"), # Identifiers
    (stc.STC_P_STRINGEOL, "fore:#000000,face:Courier New,back:#E0C0E0,eol,size:10"), # End of line where string is not closed
)
keywords = "True False None"
class PythonSTC(stc.StyledTextCtrl):
    def __init__(self, *a, **k):
        stc.StyledTextCtrl.__init__(self, *a, **k)
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, keywords)
        self.SetMargins(0, 0)
        self.SetViewWhiteSpace(False)
        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)

        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:Courier New,size:10")
        self.StyleClearAll()  # Reset all to be like the default
        for style_type, style in styles:
            self.StyleSetSpec(style_type, style)
        self.SetCaretForeground("BLUE")

    def OnUpdateUI(self, evt): # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)
        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1
        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos
        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)
        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

# ==============================================================================


class TestBoard(wx.Frame):
    def __init__(self, *a, **k):
        wx.Frame.__init__(self, *a, **k)
        
        self.created_widgets = []
        
        p = wx.Panel(self)
        p.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.types = wx.ComboBox(p, choices=typ.__all__, style=wx.CB_READONLY)
        self.options = PythonSTC(p)
        create = wx.Button(p, -1, 'create widget')
        create.Bind(wx.EVT_BUTTON, self.on_create)
        self.created = wx.ListBox(p)
        getvalue = wx.Button(p, -1, 'get', size=(30, -1))
        getvalue.Bind(wx.EVT_BUTTON, self.on_getvalue)
        self.newbounds = wx.TextCtrl(p)
        self.newdefault = wx.TextCtrl(p)
        set_bounds = wx.Button(p, -1, 'set', size=(30, -1))
        set_bounds.Bind(wx.EVT_BUTTON, self.on_set_bounds)
        set_default = wx.Button(p, -1, 'set', size=(30, -1))
        set_default.Bind(wx.EVT_BUTTON, self.on_set_default)
        
        for ctl in (self.options, self.newbounds, self.newdefault):
            ctl.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL))
        
        s = wx.BoxSizer(wx.VERTICAL)
        s1 = wx.FlexGridSizer(2, 2, 5, 5)
        s1.AddGrowableCol(1)
        s1.AddGrowableRow(1)
        for l, ctl in (('type', self.types), ('options', self.options)):
            s1.Add(wx.StaticText(p, -1, l), 0, wx.ALIGN_CENTER_VERTICAL)
            s1.Add(ctl, 1, wx.EXPAND)
        s.Add(s1, 2, wx.EXPAND|wx.ALL, 5)
        s.Add(create, 0, wx.EXPAND|wx.ALL, 5)
        s1 = wx.BoxSizer()
        s1.Add(self.created, 1, wx.EXPAND|wx.ALL, 5)
        s1.Add(getvalue, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        s.Add(s1, 1, wx.EXPAND, 0)
        s1 = wx.FlexGridSizer(2, 3, 5, 5)
        s1.AddGrowableCol(1)
        for l, ctl, b in (('re-bnds', self.newbounds, set_bounds), 
                          ('re-def.', self.newdefault, set_default)):
            s1.Add(wx.StaticText(p, -1, l), 0, wx.ALIGN_CENTER_VERTICAL)
            s1.Add(ctl, 1, wx.EXPAND)
            s1.Add(b, 0, wx.EXPAND)
        s.Add(s1, 0, wx.EXPAND|wx.ALL, 5)
        p.SetSizer(s)
        
        self.SetTitle('Input Parameter Test')
        self.SetSize((400, 450))
    
    def notify_destroy(self, child_name):
        self.created_widgets.remove(child_name)
        self.created.SetItems(self.created_widgets)
        
    def on_create(self, evt):
        widget = self.types.GetStringSelection()
        if not widget: return
        id = wx.NewId()
        title = '[%i] %s' % (id, widget)

        widget = getattr(typ, widget)
        options = self.options.GetText().strip()
        args = {}
        if options: args = eval(options)
        gui.PARAMETERS = {'test':(('test_param', 'test_param', widget, args),)}
        ParamWindow(self, id, title, size=(-1, 150), name=title).Show()
        self.created_widgets.append(title)
        self.created.SetItems(self.created_widgets)
        
    def on_set_bounds(self, evt):
        widget = self.created.GetStringSelection()
        if not widget: return
        bounds = self.newbounds.GetValue().strip()
        if not bounds: return
        wx.FindWindowByName(widget).SetBounds(eval(bounds))
    
    def on_set_default(self, evt):
        widget = self.created.GetStringSelection()
        if not widget: return
        default = self.newdefault.GetValue().strip()
        if not default: return
        wx.FindWindowByName(widget).SetDefault(eval(default))

    def on_getvalue(self, evt):
        widget = self.created.GetStringSelection()
        if not widget: return
        print 'value:', wx.FindWindowByName(widget).GetValue()
        

class ParamWindow(wx.Frame):
    def __init__(self, *a, **k):
        wx.Frame.__init__(self, *a, **k)
        p = wx.Panel(self)
        self.param = gui.ParametersPanel(p, report='test')
        self.track_changes = wx.CheckBox(p, -1, 'track parameter changes')
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self.param, 1, wx.EXPAND)
        s.Add(self.track_changes, 0, wx.EXPAND|wx.ALL, 5)
        p.SetSizer(s)
        self.Bind(EVT_PARAM_CHANGED, self.on_param_changed)
        self.Bind(wx.EVT_CLOSE, self.on_close)
    
    def on_param_changed(self, evt):
        if self.track_changes.GetValue(): 
            print 'change detected in', self.GetTitle()
            
    def on_close(self, evt):
        self.GetParent().notify_destroy(self.GetTitle())
        evt.Skip()
    
    def GetValue(self): 
        return self.param.get_data()
    
    def SetBounds(self, bounds):
        self.param.param_options['test_param']['bounds'] = bounds
        self.param.set_default_and_bounds('test_param')
    
    def SetDefault(self, bounds):
        self.param.param_options['test_param']['default'] = bounds
        self.param.set_default_and_bounds('test_param')


app = wx.App()
TestBoard(None).Show()
app.MainLoop()

