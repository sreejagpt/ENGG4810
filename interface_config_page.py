"""Config page"""

import wx
import wx.lib.plot as plot
import time

from wx.lib.pubsub import Publisher

class PageTwo(wx.Panel):
    
    #Device Screen
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #leftmost panel and middle panel are identical
        self.buttonassignments = [(None, None)]*16

        Publisher().subscribe(self.UpdateButtonAssignments, ("update.assignments"))
        
        #masterVSizer is the true master
        self.masterVSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        #master HSizer:
        self.masterHSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #Add Effects Editor to horizontal layout
        self.effectseditor = EffectsEditor(self.panel)
        self.masterHSizer.Add(self.effectseditor, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL, 30)

        #add information square to horiz layout
        self.info_panel = wx.Panel(self.panel)
        self.txt = wx.StaticText(self.info_panel, label =
                            "Hover over a button to view information.\n Click on a button to play sound")
        self.masterHSizer.Add(self.info_panel, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL, 20)


        #grid layout for buttons
        self.buttonSizer = wx.GridSizer(4, 4, 1, 1)
        self.btnPanel = wx.Panel(self.panel)
        for i in range(0, 16):
            #create 16 buttons and display them
            btn = wx.Button(self.btnPanel, label=str(i+1), id = i, size=(120,80))
            btn.Bind(wx.EVT_BUTTON, self.OnButtonPress)
            btn.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
            #btn.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)
            self.buttonSizer.Add(btn, 0, wx.EXPAND)

        #add grid sizer to horiz layout
        self.btnPanel.SetSizerAndFit(self.buttonSizer)
        self.masterHSizer.Add(self.btnPanel, 0, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL)


        self.panel.SetSizerAndFit(self.masterHSizer)


    def OnButtonPress(self, e):
        button = e.GetEventObject()
        self.panel.Refresh()

    def UpdateButtonAssignments(self, msg):
        self.buttonassignments = msg.data

    def onMouseOver(self, event):
        # mouseover changes text on button
        button = event.GetEventObject()
        self.txt.SetLabel('Hover over button to view filename\nassigned to it')
        buttonid = event.GetId()
        if self.buttonassignments[buttonid][1] != None:
            self.txt.SetLabel("Button "+str(buttonid + 1)+" stores file "+self.buttonassignments[buttonid][1]\
                +"\nMode: "+self.buttonassignments[buttonid][0])
        time.sleep(0.05)
        event.Skip()
        

    def onMouseLeave(self, event):
        # mouse not over button, back to original text
    
        self.txt.SetLabel("Hover over a button to view information.\n Click on a button to play sound")
        event.Skip()


class EffectsEditor(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #This class makes a panel that holds all the values
        #of effects that may be imported/exported
        
        self.loop_options = ['1', '1/2', '1/4', '1/8', '1/16', '1/32']
        #config file values
        self.vals = {'slot1': None, 'slot2': None, 'loop': None, 'tempo': None}
        self.decode = {'lpf': '2nd Order Lowpass', 'hpf': '2nd Order High Pass', 'bpf': '2nd Order Bandpass',
        'nf': '2nd Order Notch Filter', 'delay': 'Delay', 'echo': 'Echo', 'dcb': 'Decimator/Bitcrusher',
        'bko': 'Bitwise KO', '1': '1', '2': '1/2', '4': '1/4', '6':'1/6', '8':'1/8', '16':'1/16', '32':'1/32'}
        self.encode = {'2nd Order Lowpass':'lpf', '2nd Order High Pass':'hpf', '2nd Order Bandpass':'bpf',
        '2nd Order Notch Filter':'nf', 'Delay':'delay', 'Echo' : 'echo', 'Decimator/Bitcrusher':'dcb',
        'Bitwise KO':'bko', '1': '1','1/2': '2', '1/4':'4', '1/6':'6', '1/8':'8', '1/16':'16', '1/32':'32'}
        self.effect_options = ['2nd Order Lowpass', '2nd Order High Pass', '2nd Order Bandpass',
            '2nd Order Notch Filter', 'Delay', 'Echo', 'Decimator/Bitcrusher', 'Bitwise KO']

        self.horizsizer = wx.BoxSizer(wx.VERTICAL)
        #Effects Editor Label
        self.horizsizer.Add(wx.StaticText(self, label =
                            "EFFECTS EDITOR"), 0, wx.EXPAND| wx.ALL, border = 10)
        #Slot 1 Label
        self.horizsizer.Add(wx.StaticText(self, label =
                            "Slot 1 Effect"), 0, wx.EXPAND| wx.ALL, border = 10)

        #Drop Down Box
        self.slot1_combobox = wx.ComboBox(self, choices=self.effect_options,
            style=wx.CB_DROPDOWN)
        self.slot1_combobox.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.horizsizer.Add(self.slot1_combobox, 0, wx.EXPAND| wx.ALL, border = 10)

        #Slot 2 Label
        self.horizsizer.Add(wx.StaticText(self, label =
                            "Slot 2 Effect"), 0, wx.EXPAND| wx.ALL, border = 10)

        #Drop Down Box
        self.slot2_combobox = wx.ComboBox(self, choices=self.effect_options,
            style=wx.CB_DROPDOWN)
        self.slot2_combobox.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.horizsizer.Add(self.slot2_combobox, 0, wx.EXPAND| wx.ALL, border = 10)

        #Loop Label
        self.horizsizer.Add(wx.StaticText(self, label =
                            "Loop Interval"), 0, wx.EXPAND| wx.ALL, border = 10)

        #Loop Drop Down Box
        self.loop_combobox = wx.ComboBox(self, choices=self.loop_options, 
            style=wx.CB_DROPDOWN)
        self.loop_combobox.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.horizsizer.Add(self.loop_combobox, 0, wx.EXPAND| wx.ALL, border = 10)

        #Tempo Label
        self.horizsizer.Add(wx.StaticText(self, label =
                            "Tempo (in bpm)"), 0, wx.EXPAND| wx.ALL, border = 10)

        #Tempo Text Area
        self.tempo_textctrl = wx.TextCtrl(self, -1)
        self.horizsizer.Add(self.tempo_textctrl, 0, wx.EXPAND| wx.ALL, border = 10)


        #Import Button (via SD)
        self.importbutton = wx.Button(self, label='Import Configuration (via SD)', size=(80,25))
        self.importbutton.Bind(wx.EVT_BUTTON, self.OnImportSD)
        self.horizsizer.Add(self.importbutton, 0, wx.EXPAND | wx.ALL, border = 10)

        #Import Button (via USB)
        self.importbutton = wx.Button(self, label='Import Configuration (via USB)', size=(80,25))
        self.importbutton.Bind(wx.EVT_BUTTON, self.OnImportUSB)
        self.horizsizer.Add(self.importbutton, 0, wx.EXPAND | wx.ALL, border = 10)

        #Export Button
        self.exportbutton = wx.Button(self, label='Export Configuration (via SD)', size=(80,25))
        self.exportbutton.Bind(wx.EVT_BUTTON, self.OnExportSD)
        self.horizsizer.Add(self.exportbutton, 0, wx.EXPAND|wx.ALL, border = 10)

        #Export Button
        self.exportbutton = wx.Button(self, label='Export Configuration (via USB)', size=(80,25))
        self.exportbutton.Bind(wx.EVT_BUTTON, self.OnExportUSB)
        self.horizsizer.Add(self.exportbutton, 0, wx.EXPAND|wx.ALL, border = 10)

        #Set Sizer to self
        self.SetSizerAndFit(self.horizsizer)

    def OnImportSD(self, e):
        #Read file from location
        self.dirname='C:\Python27\ENGG4810' #TODO change this to SD card drive
        dlg = wx.FileDialog(self, "Choose a Config File", self.dirname, "", "*.cfg", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.file=open(self.dirname+"\\"+self.filename, 'r')
            #Go through file line by line and parse it
            for line in self.file:
                strip = line.split(' ', 1)

                try:
                    self.vals[strip[0].strip()] = strip[1].strip()
                except KeyError:
                    pass
            #we now have our config file parsed in
            
            #Reset working values by setting the fields to them
            self.slot1_combobox.SetLabel(self.decode[self.vals['slot1']])
            self.slot2_combobox.SetLabel(self.decode[self.vals['slot2']])
            self.loop_combobox.SetLabel(self.decode[self.vals['loop']])
            self.tempo_textctrl.SetLabel(self.vals['tempo'])

    def OnImportUSB(self, e):
        return #TODO
    
    def OnExportSD(self, e):
        self.BuildFile(e)
        #saves to SD card
        try:
            sdfile = open('I:\cf.cfg', 'w')
        
            cfgfile = open('config.cfg', 'r')
        except IOError:
            return
        for line in cfgfile:
            sdfile.write(line)
        cfgfile.close()
        sdfile.close()

        self.ShowMessage("Sent Config File to SD Card")
        

        return

    def BuildFile(self, e):
        slot1 = self.slot1_combobox.GetValue()
        slot2 = self.slot2_combobox.GetValue()
        loop = self.loop_combobox.GetValue()
        tempo = self.tempo_textctrl.GetValue()

        #convert to short forms to be used in config file
        slot1_enc = self.encode[str(slot1.strip())]
        slot2_enc = self.encode[str(slot2.strip())]
        loop_enc = self.encode[str(loop.strip())]
        

        f = open('config.cfg', 'w')
        f.write(slot1_enc+'\r\n')
        f.write(slot2_enc+'\r\n')
        f.write(loop_enc+'\r\n')
        f.write(tempo+'\r\n')
        f.close()
        return


    def send_dummy_to_mpc(self):

        import serial
        ser = serial.Serial()
        ser.port=11
        ser.baudrate=115200
        
        ser.open()

        #ser.flush()
        ser.write("dummyH\n")

        ack=ser.readline()

        ser.write("dummyH\n")
        
        ack=ser.readline()
        #print ack
        
        ser.close()

    def send_config_to_mpc(self):
            try:
                w = open('C:\\Python27\\ENGG4810\\config.cfg','rb')
            except Exception:
                self.ShowMessage("Oh no!")
            import serial
            ser = serial.Serial()
            ser.port=11
            ser.baudrate=115200
            
            ser.open()

            ser.write("cf.cfgH\n")
            ack=ser.readline()
            time.sleep(0.05)
            #print ack
            import os
            statinfo = os.stat('C:\\Python27\\ENGG4810\\config.cfg')

            ack='blah '

            ser.write(str(statinfo.st_size)+'\n')
            i=0
            while ack.strip() != str(statinfo.st_size):
                ack=ser.readline()
                print "Size Ack: ", ack
                i=i+1
                if i==5:
                    self.ShowMessage('Serial Communications Timeout')
                    return

            buff=''
            for line in w:
                buff = buff+line
            ser.write(buff)
            ack=ser.readline()
            #print ack
            ser.close()
            w.close()


    def ShowMessage(self, message):
        wx.MessageBox(message, 'Message', 
            wx.OK | wx.ICON_INFORMATION)

    def OnExportUSB(self, e):
        self.BuildFile(e)
        time.sleep(1)
        self.send_dummy_to_mpc()
        time.sleep(0.05)
        self.send_config_to_mpc()
        time.sleep(0.05)
        self.send_config_to_mpc()
        self.ShowMessage('Config File Exported to MPC')
        return



    def OnSelect(self, e):
        i = e.GetString()
        e.GetEventObject().SetLabel(i)
        

