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


class DelayScreen(wx.Frame):
    """ This class defines a little popup window that helps the user  assign
    parameters for the echo function"""
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title = "Delay Parameters", style=wx.SYSTEM_MENU)
        self.id = -1
        self.alpha = -999
        self.delay = -999
        self.vertsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        

        #Instruction label:
        msg = "Enter Parameters for the Delay Function"
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
        Publisher().sendMessage(("receive.delayVals"), msg)
        self.Close()


class BitcrushScreen(wx.Frame):
    """ This class defines a little popup window that helps the user  assign
    parameters for the Decimator/Bitcrush function"""
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title = "Bitcrush Parameters", style=wx.SYSTEM_MENU)
        self.id = -1
        self.dec = -999
        self.bitcrusher = -999
        
        self.vertsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        

        #Instruction label:
        msg = "Decimator/Bitcrusher"
        self.vertsizer.Add(wx.StaticText(self.panel, label=msg), 0, wx.ALIGN_CENTER|wx.ALL, border = 50)




        #Decimator Label
        self.vertsizer.Add(wx.StaticText(self.panel, label="Enter Decimator Value:"), 
            0, wx.ALIGN_CENTER, border = 10)

        #Decimator text Area
        self.dec_textctrl = wx.TextCtrl(self.panel, -1)
        self.vertsizer.Add(self.dec_textctrl, 0, wx.ALIGN_CENTER, border = 50)

        #Bitcrusher label
        self.selection = wx.StaticText(self.panel, label="Enter Bitcrush Value (1 - 12 bits):")
        self.vertsizer.Add(self.selection, 0, wx.ALIGN_CENTER, border = 50)

        #Bitcrusher text Area
        self.bitcrusher_textctrl = wx.TextCtrl(self.panel, -1)
        self.vertsizer.Add(self.bitcrusher_textctrl, 0, wx.ALIGN_CENTER, border = 50)

        #Ok button
        self.okbutton = wx.Button(self.panel, label='OK', size=(80,25))
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOK)
        self.vertsizer.Add(self.okbutton, 0, wx.ALIGN_CENTER | wx.ALL, border = 50)

        self.panel.SetSizerAndFit(self.vertsizer)
        self.SetSize((200, 300))
        self.Center()


    def OnOK(self, e):
        #Read text boxes and send over (dec,bit)
        self.dec = self.dec_textctrl.GetValue()
        self.bitcrusher = self.bitcrusher_textctrl.GetValue()
        msg = (self.dec, self.bitcrusher)
        Publisher().sendMessage(("receive.decBitVals"), msg)
        self.Close()

class PitchShiftScreen(wx.Frame):
    """ This class defines a little popup window that helps the user  assign
    parameters for the pitch shift function"""
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title = "Pitch Shift Parameters", style=wx.SYSTEM_MENU)
        self.id = -1
        self.pitch = -999
        self.vertsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        

        #Instruction label:
        msg = "Enter Parameters for Pitch Shift"
        self.vertsizer.Add(wx.StaticText(self.panel, label=msg), 0, wx.ALIGN_CENTER|wx.ALL, border = 50)




        #Pitch Shift Label
        self.vertsizer.Add(wx.StaticText(self.panel, label="Enter Pitch Shift Factor:"), 
            0, wx.ALIGN_CENTER, border = 10)

        #Alpha text Area
        self.ps_textctrl = wx.TextCtrl(self.panel, -1)
        self.vertsizer.Add(self.ps_textctrl, 0, wx.ALIGN_CENTER, border = 50)


        #Ok button
        self.okbutton = wx.Button(self.panel, label='OK', size=(80,25))
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOK)
        self.vertsizer.Add(self.okbutton, 0, wx.ALIGN_CENTER | wx.ALL, border = 50)

        self.panel.SetSizerAndFit(self.vertsizer)
        self.SetSize((200, 300))
        self.Center()


    def OnOK(self, e):
        #Read text boxes and send over (alpha, delay)
        self.ps = self.ps_textctrl.GetValue()
        msg = self.ps
        Publisher().sendMessage(("receive.psVals"), msg)
        self.Close()

class SliceScreen(wx.Frame):
    """ This class defines a little popup window that helps the user  assign
    parameters for the pitch shift function"""
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title = "Slice Parameters", style=wx.SYSTEM_MENU)
        self.id = -1
        self.start=0
        self.stop=100
        self.vertsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        

        #Instruction label:
        msg = "Enter Parameters for Slicing"
        self.vertsizer.Add(wx.StaticText(self.panel, label=msg), 0, wx.ALIGN_CENTER|wx.ALL, border = 50)

        #Start Label
        self.vertsizer.Add(wx.StaticText(self.panel, label="Enter Start Point (Percentage of length):"), 
            0, wx.ALIGN_CENTER, border = 10)

        #Alpha text Area
        self.start_textctrl = wx.TextCtrl(self.panel, -1)
        self.vertsizer.Add(self.start_textctrl, 0, wx.ALIGN_CENTER, border = 50)

        #Stop Label
        self.vertsizer.Add(wx.StaticText(self.panel, label="Enter Stop Point (Percentage of length):"), 
            0, wx.ALIGN_CENTER, border = 10)

        #Stop text Area
        self.stop_textctrl = wx.TextCtrl(self.panel, -1)
        self.vertsizer.Add(self.stop_textctrl, 0, wx.ALIGN_CENTER, border = 50)


        #Ok button
        self.okbutton = wx.Button(self.panel, label='OK', size=(80,25))
        self.okbutton.Bind(wx.EVT_BUTTON, self.OnOK)
        self.vertsizer.Add(self.okbutton, 0, wx.ALIGN_CENTER | wx.ALL, border = 50)

        self.panel.SetSizerAndFit(self.vertsizer)
        self.SetSize((250, 350))
        self.Center()


    def OnOK(self, e):
        #Read text boxes and send over (alpha, delay)
        self.start = self.start_textctrl.GetValue()
        self.stop = self.stop_textctrl.GetValue()
        if self.start > self.stop:
            return
        msg = (self.start, self.stop)
        
        Publisher().sendMessage(("receive.sliceVals"), msg)
        self.Close()


    
