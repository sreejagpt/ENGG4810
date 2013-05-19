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
    
    sound = fromstring(sound, 'Int16')
    spf.close()

    #now rewriting to new file
    filename_resampled = filename.split('.wav')[0]+'_resampled.wav'
    spf = wave.open(filename_resampled, 'wb')
    spf.setnchannels(1)
    spf.setsampwidth(sampwidth)
    spf.setframerate(framerate)
    spf.setnframes(nframes)
    
    #we need to resolve 16 bit frames to 12 bit
    sound=convert_to_12_bit_unsigned(sound)
    spf.writeframes(sound.tostring()) 
   
    spf.close()
      
    spf = wave.open(filename_resampled,'rb')
    frames = spf.getnframes()
    sound1 = spf.readframes(frames)
    sound1 = fromstring(sound1, 'Int16')
    spf.close()
    
    #echo('laser.wav', 30* (len(sound1)/50), 0.9997, sound) #this is my effects tester zone
    #pitchshift(sound1, 1.8)
    return sound
    
def convert_to_12_bit_unsigned(sound):
    
    sound = sound >> 4
    sound = sound - min(sound)
    
    return sound
    
def decimator(filename, sound, dec, crush):
    newname = filename.split('.wav')[0]+'_decimator.wav'
    spf = wave.open(newname, 'wb')
    outputsound = sound
    
    for i in range(0, (len(sound) - dec), dec):
        for j in range(i, i+dec):
            outputsound[j] = sound[i]

    spf.setnchannels(1)
    spf.setsampwidth(2)
    spf.setframerate(44100)
    spf.setnframes(len(outputsound))
    
    spf.writeframes(outputsound.tostring())
    
    spf.close()
    return bitcrusher(filename, outputsound, crush)
  

def pitchshift(filename, sound, shift): #shift is a floating pt number
    newname = filename.split('.wav')[0]+'_pitchshift.wav'
    spf = wave.open(newname, 'wb')
    spf.setnchannels(1)
    spf.setsampwidth(2)
    spf.setframerate(round(44100 * shift))
    spf.setnframes(round(len(sound)/shift))
    #sound = convert_to_12_bit_unsigned(sound)
    spf.writeframes(sound.tostring())
    spf.close()

    return sound
    
def plotter(sound):
    plot(sound)
    show()
    
#bitcrusher
def bitcrusher(filename, sound, crush):
    crush = crush % 12 # :D
    newname = filename.split('.wav')[0]+'_bitcrushed.wav'
    spf = wave.open(newname, 'wb')
    #max_sound = max(sound)
    
    
    #sound = sound & (131070/(2**crush))

    #max_sound2 = max(sound)
    
    #sound = sound* round(max_sound/max_sound2)

    sound = sound >> (12 - crush)
    
    spf.setnchannels(1)
    spf.setsampwidth(2)
    spf.setframerate(44100)
    spf.setnframes(len(sound))
    
    spf.writeframes(sound.tostring())
    
    spf.close()
    return sound
    
#applying echo to a file
def echo(filename, delay, att, sound):

    outputsound = sound

    largest = max(outputsound)
    smallest = min(outputsound)
    
    for p in range(delay+1, len(outputsound)):
        outputsound[p] = sound[p] + ((att* outputsound[p - delay]))
        #if outputsound[p] > largest or outputsound[p] < smallest:
         #   outputsound[p] = 0
            
    newname = filename.split('.wav')[0]+'_echo.wav'
   
    #now write echo to new file
    spf = wave.open(newname, 'wb')
    #set nchannels, sampwidth, framerate, nframes, comptype, compname
    spf.setnchannels(1)
    spf.setsampwidth(2)
    spf.setframerate(44100)
    
    spf.setnframes(len(outputsound))
    #outputsound = convert_to_12_bit_unsigned(outputsound)
    spf.writeframes(outputsound.tostring())
    spf.close() #close echo file

    #ws.PlaySound('beep1_echo.wav', ws.SND_FILENAME)
    #time.sleep(1)
 
    return outputsound


#applying echo to a file
def delay(filename, delay, att, sound):

    outputsound = sound

    largest = max(outputsound)
    smallest = min(outputsound)
   
    for p in range(delay+1, len(outputsound)):
        outputsound[p] = sound[p] + ((att * sound[p - delay]))
        #if outputsound[p] > largest or outputsound[p] < smallest:
         #   outputsound[p] = 0
            
    
    #now write echo to new file
    newname = filename.split('.wav')[0]+'_delay.wav'
    spf = wave.open(newname, 'wb')
    #set nchannels, sampwidth, framerate, nframes, comptype, compname
    spf.setnchannels(1)
    spf.setsampwidth(2)
    spf.setframerate(44100)
    spf.setnframes(len(outputsound))
    #outputsound = convert_to_12_bit_unsigned(outputsound)
    spf.writeframes(outputsound.tostring())
    spf.close() #close delay file

    return outputsound


if __name__ == '__main__':
    show_wave_n_spec('laser.wav')
    show_wave_n_spec('beach.wav')
    show_wave_n_spec('littlesecrets.wav')
    show_wave_n_spec('techno.wav')
    show_wave_n_spec('thump.wav')
    show_wave_n_spec('manybeeps.wav')
    show_wave_n_spec('sleepyhead.wav')
