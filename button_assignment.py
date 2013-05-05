import wx
from wx.lib.pubsub import Publisher

class ButtonAssignment(wx.Frame):
    """ This class defines a little popup window that helps the user  assign
    specific sounds to buttons """
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title = "Choose Button", style=wx.SYSTEM_MENU)
        self.vertsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)

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
        self.selection.SetLabel("Your selection: Button "+str(self.id))
        return

    def OnOK(self, e):
        #Complete export and hide this frame
        #Do export
        #Publisher().sendMessage(("show.mainframe"), 'Closing now')
        self.Close()

