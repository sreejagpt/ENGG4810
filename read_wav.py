import sys 
from pylab import * 
import wave


def show_wave_n_spec(filename):
    spf = wave.open(filename,'r')
    sound = spf.readframes(spf.getnframes())
    sound = fromstring(sound, 'Int32')
    spf.close()

    #now rewriting to new file
    spf = wave.open('beep1_resampled.wav', 'w')
    spf.setparams((1, 2, 44100, 0,'NONE', 'not compressed'))
    spf.writeframesraw(sound)
    
    #echo(100.0, sound)
    return sound 
    spf.close()

  

def pitchshift(sound, shift):
    spf = wave.open('beep1_pitchshift.wav', 'w')
    spf.setparams((1, 2, 44100 * shift, 0, 'NONE', 'not compressed'))
    spf.writeframesraw(sound)
    plot(sound)
    show()
    spf.close()

def plotter(sound):
    plot(sound)
    show()
    
#bitcrusher
def bitcrusher(sound):
    spf = wave.open('beep1_bitcrushed.wav', 'w')
    spf.setparams((1, 1, 44100, 0, 'NONE', 'not compressed'))
    spf.writeframesraw(sound)
    plot(sound)
    show()
    spf.close()
    
    
#applying echo to a file
def echo(delay, sound):

    outputsound = sound
    att = [0.008, 0.006, 0.005, 0.003, 0.0001]
    plot(sound) #need to remove
    show() #need to remove 
    p = int(delay)
    for n in range(0, size(sound)):
        outputsound[n] = sound[n]
        if (n - p)>=0: #VERY BUGGY
                outputsound[n] = (outputsound[n] + att[int(delay) - p + 1]*sound[n - p])
              
    plot(outputsound)
    
    show()
    spf = wave.open('beep1_echo.wav', 'w')
    spf.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
    spf.writeframes(outputsound)
    spf.close()

if __name__ == '__main__':
    show_wave_n_spec('beep1.wav')
