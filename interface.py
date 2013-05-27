''' Interface for TP2 code '''
import matplotlib 
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure 
import wx 
from wx.lib.pubsub import Publisher
import interface_config_page as pg2 
import read_wav as wav 
import sys
import serial_comms as sc

import wave
import button_assignment as ba
import effects_screens as effs
import winsound as ws

class PageOne(wx.Panel):
    #Effects screen
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.dirname='C:\Python27\ENGG4810'
        self.EffectId = -1
        self.currentid = -1
        self.holdlatchmode = 'hold'
        self.frame = parent
        self.inputsounds = [None] * 5 #'pure' sounds imported by user
        self.outputsounds = [None] * 5 #'filtered' sounds that user creates
        self.buttonassignments = [(None, None)] * 16 #which button is assigned to what?
        self.inputfilenames = [None] * 5
        self.panels = []
        self.figures = [None] * 5
        self.canvs = []
        self.openButtons = []
        self.eButtons = [] #echo
        self.uButtons = [] #play
        self.dButtons = [] #delay
        self.pButtons = [] #pitch
        self.bButtons = [] #bitcrusher
        self.sliceButtons=[]
        self.exButtons = [] #export via serial
        self.exButtons_SD = [] #export via SD
        self.buttonPanels = []
        

        Publisher().subscribe(self.showFrame, ("show.mainframe"))
        Publisher().subscribe(self.echoTime, ("receive.echoVals"))
        Publisher().subscribe(self.decBitTime, ("receive.decBitVals"))
        Publisher().subscribe(self.delayTime, ("receive.delayVals"))
        Publisher().subscribe(self.psTime, ("receive.psVals"))
        Publisher().subscribe(self.sliceTime, ("receive.sliceVals"))
        
        #master VSizer:
        self.masterVSizer = wx.BoxSizer(wx.VERTICAL)

        for i in range(0, 5):
            #create panel
            panel = wx.Panel(self)
            self.panels.append(panel)
            #create canvas 
            fig = Figure(None, facecolor="grey")
            self.figures[i] = fig
            canv = FigureCanvas(self.panels[i], -1, self.figures[i])
            self.canvs.append(canv)

            #buttons: open, play, echo, delay, pitch shift, bitcrusher,
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
            pbtn.Bind(wx.EVT_BUTTON, self.OnPitchShift)
            self.pButtons.append(pbtn)

            #create bitcrusher button
            bbtn = wx.Button(self.buttonPanels[i], id = 50 + i,
                                        label='Dcmtr/Bitcrshr', size=(80,25))
            bbtn.Bind(wx.EVT_BUTTON, self.OnBitcrush)
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

            #create play button
            ubtn = wx.Button(self.buttonPanels[i], id = 80 + i,
                                        label='Play', size=(80,25))
            ubtn.Bind(wx.EVT_BUTTON, self.OnPlay)
            self.uButtons.append(ubtn)

            #create Slice button
            slbtn = wx.Button(self.buttonPanels[i], id = 90 + i,
                                        label='Slice', size=(80,25))
            slbtn.Bind(wx.EVT_BUTTON, self.OnSlice)
            self.sliceButtons.append(slbtn)

            #create button Sizer
            self.buttonSizer = wx.GridSizer(5, 2, 1, 1)
            self.buttonSizer.AddMany([(self.openButtons[i], 0, wx.EXPAND),
                                 (self.eButtons[i], 0, wx.EXPAND),
                                 (self.dButtons[i], 0, wx.EXPAND),
                                 (self.pButtons[i], 0, wx.EXPAND),
                                 (self.bButtons[i], 0, wx.EXPAND),
                                 (self.exButtons[i], 0, wx.EXPAND),
                                 (self.sliceButtons[i], 0, wx.EXPAND),
                                 (self.exButtons_SD[i], 0, wx.EXPAND),
                                 (self.uButtons[i], 0, wx.EXPAND)])
            self.buttonPanels[i].SetSizerAndFit(self.buttonSizer)

            
            #create sizer
            innerVSizer = wx.BoxSizer(wx.HORIZONTAL)
            innerVSizer.Add(self.canvs[i], 1, border=4,
                                 flag=wx.EXPAND | wx.ALL)
            innerVSizer.Add(self.buttonPanels[i], 0, border=4)
            
            self.panels[i].SetSizerAndFit(innerVSizer)
            self.masterVSizer.Add(self.panels[i], 1, wx.EXPAND | wx.ALL, 4)

        self.SetSizerAndFit(self.masterVSizer)

    

   
    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            if self.filename.split(".")[1] == "mp3":
                self.convert_mp3_to_wav(self.filename)
                self.filename=self.filename.split(".mp3")[0]+".wav"
            sound = wav.show_wave_n_spec(self.dirname+"\\"+self.filename)
            ide = (e.GetId())%10
            #now we have the sound file!!
            #add it to our 'pure' sound collection
            self.inputsounds[ide] = sound
            self.inputfilenames[ide] = self.filename.split(".wav")[0]+"_resampled.wav"        
            self.outputsounds[ide] = sound #WARNING TODO this must be removed after implementing effects
            self.axes = self.figures[ide].add_subplot(111)
            
            #clear axes first
            self.axes.clear()
            
            self.axes.plot(sound, "-b")
            self.axes.set_axis_off()
            self.axes.set_ybound(lower = min(sound), upper = max(sound))
            self.axes.set_xbound(lower = 0, upper = len(sound))
            
            self.canvs[ide] = FigureCanvas(self.panels[ide], -1, self.figures[ide])
            
            
        dlg.Destroy()

    def convert_mp3_to_wav( self, name ):
            import pymedia.audio.acodec as acodec
            import pymedia.muxer as muxer
            import time, wave, string, os
            name=str(name)
            name1= str.split( name, '.' )
            name2= string.join( name1[ : len( name1 )- 1 ] )
            # Open demuxer first

            dm= muxer.Demuxer( name1[ -1 ].lower() )
            dec= None
            f= open( name, 'rb' )
            snd= None
            s= " "
            while len( s ):
                s= f.read( 20000 )
                if len( s ):
                    frames= dm.parse( s )
                    for fr in frames:
                        if dec== None:
                            # Open decoder

                            dec= acodec.Decoder( dm.streams[ 0 ] )
                        r= dec.decode( fr[ 1 ] )
                        if r and r.data:
                            if snd== None:
                                snd= wave.open( name2+ '.wav', 'wb' )
                                snd.setparams( (r.channels, 2, r.sample_rate, 0, 'NONE','') )
                            
                            snd.writeframes( r.data )

    def showFrame(self, msg):
        self.buttonpressed = msg.data[0]
        self.holdlatchmode = msg.data[1]
        #Assigning sound to keypad key
        if self.buttonpressed != -1:
            sound = self.inputsounds[self.currentid]
            filename = self.inputfilenames[self.currentid]
            self.buttonassignments[self.buttonpressed] = (self.holdlatchmode, filename)
            Publisher().sendMessage(("update.assignments"), self.buttonassignments)
        frame = self.GetParent()
        frame.Show()

    def decBitTime(self, msg):
        #extract values from message
        self.dec = msg.data[0]
        self.bitcrusher = msg.data[1]
        #call Echo!
        
        sound = self.inputsounds[self.EffectId]

        if sound == None:
            return
        
        sound = wav.decimator(self.inputfilenames[self.EffectId], sound, int(self.dec), int(self.bitcrusher))
        self.axes = self.figures[self.EffectId].add_subplot(111)
        
        #clear axes first
        self.axes.clear()
        self.inputsounds[self.EffectId] = sound
        self.inputfilenames[self.EffectId] = self.inputfilenames[self.EffectId].split('.wav')[0]+'_bitcrushed.wav'
        self.axes.plot(sound, "-b")
        self.axes.set_axis_off()
        self.axes.set_ybound(lower = min(sound), upper = max(sound))
        self.axes.set_xbound(lower = 0, upper = len(sound))
            
        self.canvs[self.EffectId] = FigureCanvas(self.panels[self.EffectId], -1, self.figures[self.EffectId])
        
    def delayTime(self, msg):
        self.alpha = msg.data[0]
        self.delay = msg.data[1]
        
        #call Echo! 
        sound = self.inputsounds[self.EffectId]

        if sound == None:
            return
        self.delay = round(((int(self.delay)) * len(sound))/100)
        
        sound = wav.delay(self.inputfilenames[self.EffectId], int(self.delay),
                         float(self.alpha), sound)
        self.axes = self.figures[self.EffectId].add_subplot(111)
        #clear axes first
        self.axes.clear()
        self.inputsounds[self.EffectId] = sound
        self.inputfilenames[self.EffectId] = self.inputfilenames[self.EffectId].split('.wav')[0]+'_delay.wav'
        self.axes.plot(sound, "-b")
        self.axes.set_axis_off()
        self.axes.set_ybound(lower = min(sound), upper = max(sound))
        self.axes.set_xbound(lower = 0, upper = len(sound))
            
        self.canvs[self.EffectId] = FigureCanvas(self.panels[self.EffectId], -1, self.figures[self.EffectId])

    def echoTime(self, msg):
        self.alpha = msg.data[0]
        self.delay = msg.data[1]
        #call Echo!
        
        sound = self.inputsounds[self.EffectId]

        if sound == None:
            return
        self.delay = round(((int(self.delay)) * len(sound))/100)
        
        sound = wav.echo(self.inputfilenames[self.EffectId], int(self.delay),
                         float(self.alpha), sound)
        self.axes = self.figures[self.EffectId].add_subplot(111)

        #clear axes first
        self.axes.clear()
        self.inputsounds[self.EffectId] = sound
        self.inputfilenames[self.EffectId] = self.inputfilenames[self.EffectId].split('.wav')[0]+'_echo.wav'
        self.axes.plot(sound, "-b")
        self.axes.set_axis_off()
        self.axes.set_ybound(lower = min(sound), upper = max(sound))
        self.axes.set_xbound(lower = 0, upper = len(sound))
            
        self.canvs[self.EffectId] = FigureCanvas(self.panels[self.EffectId], -1, self.figures[self.EffectId])

    def psTime(self, msg):
        self.ps = float(msg.data)
        #call Echo!
        
        sound = self.inputsounds[self.EffectId]

        if sound == None:
            return
        
        
        sound = wav.pitchshift(self.inputfilenames[self.EffectId], sound, self.ps)
        self.axes = self.figures[self.EffectId].add_subplot(111)
        #clear axes first
        self.axes.clear()
        self.inputsounds[self.EffectId] = sound
        self.inputfilenames[self.EffectId] = self.inputfilenames[self.EffectId].split('.wav')[0]+'_pitchshift.wav'
        self.axes.plot(sound, "-b")
        self.axes.set_axis_off()
        self.axes.set_ybound(lower = min(sound), upper = max(sound))
        self.axes.set_xbound(lower = 0, upper = len(sound))
            
        self.canvs[self.EffectId] = FigureCanvas(self.panels[self.EffectId], -1, self.figures[self.EffectId])

    def sliceTime(self, msg):
        self.start=int(msg.data[0])
        self.stop=int(msg.data[1])
        print "Slicing "+self.inputfilenames[self.EffectId]
        sound=self.inputsounds[self.EffectId]

        self.start=int((self.start*len(sound))/100)
        self.stop=int((self.stop*len(sound))/100)
        
        sound=sound[self.start:self.stop+1]
        #plot new wav file
        self.axes = self.figures[self.EffectId].add_subplot(111)
        #clear axes first
        self.axes.clear()
          
        self.axes.plot(sound, "-b")
        self.axes.set_axis_off()
        self.axes.set_ybound(lower = min(sound), upper = max(sound))
        self.axes.set_xbound(lower = 0, upper = len(sound))
        self.canvs[self.EffectId] = FigureCanvas(self.panels[self.EffectId], -1, self.figures[self.EffectId])
        #write it to wave file

        spf1=wave.open(self.inputfilenames[self.EffectId], 'rb')
        channels = spf1.getnchannels()
        width = spf1.getsampwidth()
        framerate = spf1.getframerate()
        nframe=spf1.getnframes()
        spf1.close()

        spf = wave.open(self.inputfilenames[self.EffectId], 'wb')
        spf.setnchannels(channels)
        spf.setsampwidth(width)
        spf.setframerate(framerate)
        spf.setnframes(len(sound))
        spf.writeframes(sound.tostring())


        spf.close()

        #store it to self.sounds.
        self.inputsounds[self.EffectId] = sound
        #self.inputfilenames[self.EffectId] = self.inputfilenames[self.EffectId].split('.wav')[0]+'_sliced.wav'
        
        return

    def OnEcho(self, e):
        #open little window which inputs attenuation and delay
        self.new_frame = effs.EchoScreen()
        self.new_frame.Show()
        #get sound from self.inputsounds
        self.EffectId = e.GetId() % 20
        return

    def OnBitcrush(self, e):
        self.new_frame = effs.BitcrushScreen()
        self.new_frame.Show()
        self.EffectId = e.GetId() % 50

    def OnSlice(self, e):
        self.new_frame = effs.SliceScreen()
        self.new_frame.Show()
        self.EffectId = e.GetId() % 90
    
    def OnDelay(self, e):
        #open little window which inputs attenuation and delay
        self.new_frame = effs.DelayScreen()
        self.new_frame.Show()
        #get sound from self.inputsounds
        self.EffectId = e.GetId() % 30
        return

    def OnPitchShift(self, e):
        #open little window which inputs shift value
        self.new_frame = effs.PitchShiftScreen()
        self.new_frame.Show()
        #get sound from self.inputsounds
        self.EffectId = e.GetId() % 40
        return

    def OnExportUSB(self, e):
        #get button id
        self.currentid = (e.GetId())%60
        self.new_frame = ba.ButtonAssignment()
        self.new_frame.Show()

    def OnExportSD(self, e):
        #get button id
        self.currentid = (e.GetId())%70
        self.new_frame = ba.ButtonAssignment()
        self.new_frame.Show()

    def OnPlay(self, e):
        ide = (e.GetId()) % 80
        #now play the file
        print "Play ", self.inputfilenames[ide]
        ws.PlaySound(self.inputfilenames[ide], ws.SND_FILENAME)
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
        #self.Center()



if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
