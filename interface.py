''' Interface for TP2 code '''
import matplotlib 
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure 
import wx 
from wx.lib.pubsub import Publisher 
import wx.lib.plot as plt 
import interface_config_page as pg2 
import read_wav as wav 
import sys

import wave


class PageOne(wx.Panel):
    #Effects screen
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.dirname='C:\Python27\ENGG4810'
        self.frame = parent
        self.inputsounds = [None] * 5 #'pure' sounds imported by user
        self.outputsounds = [None] * 5 #'filtered' sounds that user creates
        self.panels = []
        self.figures = []
        self.canvs = []
        self.openButtons = []
        self.eButtons = [] #echo
        self.uButtons = [] #undo
        self.dButtons = [] #delay
        self.pButtons = [] #pitch
        self.bButtons = [] #bitcrusher
        self.exButtons = [] #export via serial
        self.exButtons_SD = [] #export via SD
        self.buttonPanels = []
        self.sliders = []

        #Publisher().subscribe(self.showFrame, ("show.mainframe"))

        #master VSizer:
        self.masterVSizer = wx.BoxSizer(wx.VERTICAL)

        for i in range(0, 5):
            #create panel
            panel = wx.Panel(self)
            self.panels.append(panel)
            #create canvas 
            fig = Figure(None, facecolor="grey")
            self.figures.append(fig)
            canv = FigureCanvas(self.panels[i], -1, self.figures[i])
            self.canvs.append(canv)

            #buttons: open, undo, play, echo, delay, pitch shift, bitcrusher,
            # and export
            
            #create a button panel
            panel = wx.Panel(self.panels[i])
            self.buttonPanels.append(panel)
            
            #create Open button 
            openbtn = wx.Button(self.buttonPanels[i], id = 10 + i,
                                        label='Open', size=(80,25))
            openbtn.Bind(wx.EVT_BUTTON, self.OnOpen)
            self.openButtons.append(openbtn)

            #create echo button
            ebtn = wx.Button(self.buttonPanels[i], id = 20 + i,
                                        label='Echo', size=(80,25))
            ebtn.Bind(wx.EVT_BUTTON, self.OnEcho)
            self.eButtons.append(ebtn)

            #create delay button
            dbtn = wx.Button(self.buttonPanels[i], id = 30 + i,
                                        label='Delay', size=(80,25))
            dbtn.Bind(wx.EVT_BUTTON, self.OnDelay)
            self.dButtons.append(dbtn)

            #create pitch shift button
            pbtn = wx.Button(self.buttonPanels[i], id = 40 + i,
                                        label='Pitch Shift', size=(80,25))
            pbtn.Bind(wx.EVT_BUTTON, self.OnDelay)
            self.pButtons.append(pbtn)

            #create bitcrusher button
            bbtn = wx.Button(self.buttonPanels[i], id = 50 + i,
                                        label='Bitcrusher', size=(80,25))
            bbtn.Bind(wx.EVT_BUTTON, self.OnDelay)
            self.bButtons.append(bbtn)

            #create export button
            exbtn = wx.Button(self.buttonPanels[i], id = 60 + i, 
                                        label='Export (USB)', size=(80,25))
            exbtn.Bind(wx.EVT_BUTTON, self.OnExportUSB)
            self.exButtons.append(exbtn)

            #create export via SD button
            ex2btn = wx.Button(self.buttonPanels[i], id = 70 + i,
                                        label='Export (SD)', size=(80,25))
            ex2btn.Bind(wx.EVT_BUTTON, self.OnExportSD)
            self.exButtons_SD.append(ex2btn)

            #create undo button
            ubtn = wx.Button(self.buttonPanels[i], id = 80 + i,
                                        label='Undo', size=(80,25))
            ubtn.Bind(wx.EVT_BUTTON, self.OnUndo)
            self.uButtons.append(ubtn)

            #create button Sizer
            self.buttonSizer = wx.GridSizer(4, 2, 1, 1)
            self.buttonSizer.AddMany([(self.openButtons[i], 0, wx.EXPAND),
                                 (self.eButtons[i], 0, wx.EXPAND),
                                 (self.dButtons[i], 0, wx.EXPAND),
                                 (self.pButtons[i], 0, wx.EXPAND),
                                 (self.bButtons[i], 0, wx.EXPAND),
                                 (self.exButtons[i], 0, wx.EXPAND),
                                 (self.uButtons[i], 0, wx.EXPAND),
                                 (self.exButtons_SD[i], 0, wx.EXPAND)])
            self.buttonPanels[i].SetSizerAndFit(self.buttonSizer)

            #create vertical slider
            sld = wx.Slider(self.panels[i], value=280, minValue=100,
                            maxValue=500, size=(-1, 100), id = 90 + i,
                            style=wx.SL_VERTICAL | wx.SL_AUTOTICKS)
            sld.SetTickFreq(80, 1)
            self.sliders.append(sld)
            #create sizer
            innerVSizer = wx.BoxSizer(wx.HORIZONTAL)
            innerVSizer.Add(self.canvs[i], 1, border=4,
                                 flag=wx.EXPAND | wx.ALL)
            innerVSizer.Add(self.buttonPanels[i], 0, border=4)
            innerVSizer.Add(self.sliders[i], 0, border=4)
            self.panels[i].SetSizerAndFit(innerVSizer)
            self.masterVSizer.Add(self.panels[i], 1, wx.EXPAND | wx.ALL, 4)

        self.SetSizerAndFit(self.masterVSizer)

   
    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()

            sound = wav.show_wave_n_spec(self.dirname+"\\"+self.filename)
            id = (e.GetId())%10
            #now we have the sound file!!
            #add it to our 'pure' sound collection
            self.inputsounds[id] = sound            
            self.outputsounds[id] = sound #WARNING TODO this must be removed after implementing effects
            self.axes = self.figures[id].add_subplot(111)
            #clear axes first
            self.axes.cla()
            
            for i in range(0, len(sound)):
                sound[i] = sound[i]/1000;
            self.axes.plot(sound, "-b")
            self.axes.set_axis_off()
            self.axes.set_ybound(lower = min(sound), upper = max(sound))
            self.axes.set_xbound(lower = 0, upper = len(sound))
            
            self.canvs[id] = FigureCanvas(self.panels[id], -1, self.figures[id])
            
            
        dlg.Destroy()

    def showFrame(self):
        frame = self.GetParent()
        frame.Show()

    def OnEcho(self, e):
        return
    
    def OnDelay(self, e):
        return

    def OnExportUSB(self, e):
        #self.frame.Hide()
        self.new_frame = ButtonAssignment()
        self.new_frame.Show()

    def OnExportSD(self, e):
        #self.frame.Hide()
        self.new_frame = ButtonAssignment()
        self.new_frame.Show()

    def OnUndo(self, e):
        return


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Team Project 2 | Team 13")

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        page1 = PageOne(nb)
        page2 = pg2.PageTwo(nb)
        #page3 = PageOne(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Effects")
        nb.AddPage(page2, "Configuration")
        #nb.AddPage(page3, "Help") #Maybe USB MIDI goes in this tab TODO
        
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
        self.Maximize()
        self.Center()



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




if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
