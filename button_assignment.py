import wx
from wx.lib.pubsub import Publisher

class ButtonAssignment(wx.Frame):
    """ This class defines a little popup window that helps the user  assign
    specific sounds to buttons """
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title = "Choose Button", style=wx.SYSTEM_MENU)
        self.id = -1
        self.vertsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        self.holdlatch_options = ['hold', 'latch']
        self.currentmode =  self.holdlatch_options[0]

        #Instruction label:
        msg = "Click a button to assign file to:"
        self.vertsizer.Add(wx.StaticText(self.panel, label=msg), 0, wx.ALIGN_CENTER, border = 50)

        #Create 16 buttons:
        self.buttonSizer = wx.GridSizer(4, 4, 1, 1)
        self.btnPanel = wx.Panel(self.panel)
        for i in range(0, 16):
            #create 16 buttons and display them
            btn = wx.Button(self.btnPanel, label=str(i+1), id = i, size=(120,80))
            btn.Bind(wx.EVT_BUTTON, self.OnButtonPress)
            self.buttonSizer.Add(btn, 0, wx.EXPAND)

        self.btnPanel.SetSizerAndFit(self.buttonSizer)
        self.vertsizer.Add(self.btnPanel, 0, wx.EXPAND|wx.ALL, border = 50)


        #Hold/Latch Label
        self.vertsizer.Add(wx.StaticText(self.panel, label="Set Hold/Latch Mode"), 
            0, wx.ALIGN_CENTER, border = 10)

        #Hold/Latch Drop Down Box
        self.holdlatch_combobox = wx.ComboBox(self.panel, choices=self.holdlatch_options, 
            style=wx.CB_READONLY)
        self.holdlatch_combobox.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        #self.holdlatch_combobox.SetLabel(self.holdlatch_options[0])
        self.vertsizer.Add(self.holdlatch_combobox, 0, wx.ALIGN_CENTER, border = 50)


        #Your selection label
        self.selection = wx.StaticText(self.panel, label="Your selection: <None>")
        self.vertsizer.Add(self.selection, 0, wx.ALIGN_CENTER, border = 50)

        self.okbutton = wx.Button(self.panel, label='OK', size=(80,25))
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOK)
        self.vertsizer.Add(self.okbutton, 0, wx.ALIGN_CENTER, border = 50)

        self.panel.SetSizerAndFit(self.vertsizer)
        self.SetSize((600, 550))
        self.Center()

    def OnButtonPress(self, e):
        #update self.selection label and store value to self.buttonchoice
        self.id = e.GetId()
        self.selection.SetLabel("Your selection: Button "+str((self.id) + 1))

    def OnSelect(self, e):
        i = e.GetString()
        self.currentmode = i
        e.GetEventObject().SetLabel(i)

    def OnOK(self, e):
        #Complete export and hide this frame
        #Do export here TODO
        #msg stores button clicked
        #msg is -1 if no button clicked
        msg = (self.id, self.currentmode)
        Publisher().sendMessage(("show.mainframe"), msg)
        self.Close()

