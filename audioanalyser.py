import pymedia
import time
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pylab as P

f = open('manybeeps_resampled.wav', 'rb')
s=f.read()

spa = pymedia.audio.sound.SpectrAnalyzer(1, 575, 1024)
bands= spa.asBands(5, s)


for band in bands:
        x=[]
        y=[]
        
        for item in band:
                if len(x) == 0:
                        x.append(item[0])
                        y.append(item[1])
                else:
                        x.append(item[0]+x[len(x) - 1])
                        y.append(item[1]+y[len(y) - 1])
                        #x.append(item[0])
                        #y.append(item[1])
        break
x=np.array(x)
y=np.array(y)
print x, '\n',  y
n, bins, patches = P.hist(x,y, histtype='bar')
P.show()
"""
for band in bands:
        x=[]
        y=[]
        
        for item in band:
                x.append(item[0])
                y.append(item[1])

        x=np.array(x)
        y=np.array(y)
        fig = plt.figure()
        #ax = fig.add_subplot(111)

        plt.hist(x,100)


        plt.show()

        print '\n\n\n'
        time.sleep(2)
        break
"""

