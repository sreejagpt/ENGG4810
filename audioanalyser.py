
import pymedia.audio.sound as sound, time
snd1= sound.Output( 44100, 2, sound.AFMT_S16_LE )
f= open( 'many_beeps.wav', 'rb' )
s= ' '
while len( s )> 0:
        s= f.read( 4000000 )
while 1:
        snd1.play( s )

                        

#analyzer= sound.SpectrAnalyzer( CHANNELS, SAMPLES, NUM_FREQS )
