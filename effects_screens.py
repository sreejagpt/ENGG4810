import wx
from wx.lib.pubsub import Publisher

class EchoScreen(wx.Frame):
    """ This class defines a little popup window that helps the user  assign
    parameters for the echo function"""
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title = "Echo Parameters", style=wx.SYSTEM_MENU)
        self.id = -1
        self.alpha = -999
        self.delay = -999
        self.vertsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        self.holdlatch_options = ['hold', 'latch']
        self.currentmode =  self.holdlatch_options[0]

        #Instruction label:
        msg = "Enter Parameters for the Echo Function"
        self.vertsizer.Add(wx.StaticText(self.panel, label=msg), 0, wx.ALIGN_CENTER|wx.ALL, border = 50)




        #Alpha Label
        self.vertsizer.Add(wx.StaticText(self.panel, label="Enter Alpha:"), 
            0, wx.ALIGN_CENTER, border = 10)

        #Alpha text Area
        self.alpha_textctrl = wx.TextCtrl(self.panel, -1)
        self.vertsizer.Add(self.alpha_textctrl, 0, wx.ALIGN_CENTER, border = 50)

        #Delay label
        self.selection = wx.StaticText(self.panel, label="Enter Delay (as a percentage):")
        self.vertsizer.Add(self.selection, 0, wx.ALIGN_CENTER, border = 50)

        #Delay text Area
        self.delay_textctrl = wx.TextCtrl(self.panel, -1)
        self.vertsizer.Add(self.delay_textctrl, 0, wx.ALIGN_CENTER, border = 50)

        #Ok button
        self.okbutton = wx.Button(self.panel, label='OK', size=(80,25))
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOK)
        self.vertsizer.Add(self.okbutton, 0, wx.ALIGN_CENTER | wx.ALL, border = 50)

        self.panel.SetSizerAndFit(self.vertsizer)
        self.SetSize((200, 300))
        self.Center()


    def OnOK(self, e):
        #Read text boxes and send over (alpha, delay)
        self.alpha = self.alpha_textctrl.GetValue()
        self.delay = self.delay_textctrl.GetValue()
        msg = (self.alpha, self.delay)
        Publisher().sendMessage(("receive.echoVals"), msg)
        self.Close()
