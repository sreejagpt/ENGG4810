# Read from Mic Input and find the freq's
import pyaudio
import numpy as np
import bge
import wave

chunk = 2048

# use a Blackman window
window = np.blackman(chunk)
# open stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 1920

p = pyaudio.PyAudio()
myStream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = chunk)

def AnalyseStream(cont):
    data = myStream.read(chunk)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(chunk), data))*window
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/chunk
        print("The freq is %f Hz." % (thefreq))
    else:
        thefreq = which*RATE/chunk
        print("The freq is %f Hz." % (thefreq))

# stream.close()
# p.terminate()
