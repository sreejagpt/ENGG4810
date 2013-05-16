import sys 
from pylab import *
import numpy as np
import wave
import winsound as ws
import time

def show_wave_n_spec(filename):
    spf = wave.open(filename,'rb')
    frames = spf.getnframes()
    sound = spf.readframes(-1)
    nchannels = spf.getnchannels()
    sampwidth = spf.getsampwidth()
    framerate = 44100
    nframes = spf.getnframes()
    print nframes, len(sound)
    sound = fromstring(sound, 'Int16')
    spf.close()

    #ws.PlaySound('beep1.wav', ws.SND_FILENAME)
    #time.sleep(1)

    #now rewriting to new file
    spf = wave.open('beep1_resampled.wav', 'wb')
    spf.setnchannels(1)
    spf.setsampwidth(sampwidth)
    spf.setframerate(framerate)
    spf.setnframes(nframes)
    min_sound = min(sound)
    #we need to resolve 16 bit frames to 12 bit
    for i in range(0, size(sound)):
        sound[i] = ((sound[i]/16) + min_sound)%4096
    spf.writeframes(sound.tostring())
    print min(sound), max(sound)
    spf.close()
    
    #ws.PlaySound('beep1_resampled.wav', ws.SND_FILENAME)
    #time.sleep(1)


    spf = wave.open('beep1_resampled.wav','rb')
    frames = spf.getnframes()
    sound1 = spf.readframes(frames)
    sound1 = fromstring(sound1, 'Int16')
    spf.close()
    
    #delay( 30* (len(sound1)/50), 0.9997, sound)
    
    return sound1
    

  

def pitchshift(sound, shift):
    spf = wave.open('beep1_pitchshift.wav', 'w')
    spf.setparams((1, 2, 44100 * shift, frames, 'NONE', 'not compressed'))
    spf.writeframes(sound.tostring())
    plot(sound)
    show()
    spf.close()

def plotter(sound):
    plot(sound)
    show()
    
#bitcrusher
def bitcrusher(sound):
    spf = wave.open('beep1_bitcrushed.wav', 'wb')
    spf.setparams((1, 1, 44100, 0, 'NONE', 'not compressed'))
    spf.writeframes(sound.tostring())
    plot((sound))
    show()
    spf.close()
    
    
#applying echo to a file
def echo(delay, att, sound):

    outputsound = sound

    largest = max(outputsound)
    smallest = min(outputsound)
    print smallest
    for p in range(delay+1, len(outputsound)):
        outputsound[p] = sound[p] + ((att* outputsound[p - delay]))
        if outputsound[p] > largest or outputsound[p] < smallest:
            outputsound[p] = 0
            
    
    #now write echo to new file
    spf = wave.open('beep1_echo.wav', 'wb')
    #set nchannels, sampwidth, framerate, nframes, comptype, compname
    spf.setnchannels(1)
    spf.setsampwidth(2)
    spf.setframerate(44100)
    spf.setnframes(len(outputsound))
    spf.writeframes(outputsound.tostring())
    spf.close() #close echo file

    ws.PlaySound('beep1_echo.wav', ws.SND_FILENAME)
    time.sleep(1)
    return outputsound


#applying echo to a file
def delay(delay, att, sound):

    outputsound = sound

    largest = max(outputsound)
    smallest = min(outputsound)
    print smallest
    for p in range(delay+1, len(outputsound)):
        outputsound[p] = sound[p] + ((att * sound[p - delay]))
        if outputsound[p] > largest or outputsound[p] < smallest:
            outputsound[p] = 0
            
    
    #now write echo to new file
    spf = wave.open('beep1_delay.wav', 'wb')
    #set nchannels, sampwidth, framerate, nframes, comptype, compname
    spf.setnchannels(1)
    spf.setsampwidth(2)
    spf.setframerate(44100)
    spf.setnframes(len(outputsound))
    spf.writeframes(outputsound.tostring())
    spf.close() #close delay file

    ws.PlaySound('beep1_delay.wav', ws.SND_FILENAME)
    time.sleep(1)
    return outputsound


if __name__ == '__main__':
    show_wave_n_spec('beep1.wav')
