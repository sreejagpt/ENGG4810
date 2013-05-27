
def send_config_to_mpc():
    w = open('config.cfg','rb')
    import serial
    ser = serial.Serial()
    ser.port=12
    ser.baudrate=115200
    
    ser.open()

    #ser.flush()
    ser.write("cf.cfgH\n")
    ack=ser.readline()
    
    #print "I am expecting the filename here as ACK:: ", ack
    
    import os
    statinfo = os.stat('config.cfg')

    ser.write(str(statinfo.st_size)+'\n')
    
    ack=ser.readline()
    #print "First ack: ", ack
    
    #print "I am expecting the filesize here as ACK:: ", ack
    buff=''
    for line in w:
        buff = buff+line
    #print "Now sending file ", buff
    ser.write(buff)
    ack=ser.readline()
    #print "I just received this ack:: ", ack
    
    ser.close()
    w.close()

def send_wav_to_mpc():
    
    import serial
    ser = serial.Serial()
    ser.port=12
    ser.baudrate=115200
    ser.open()
    #ser.flush()
    ser.write("04.wavH\n")
    ack=ser.readline()
    
    #print "I am expecting the filename here as ACK:: ", ack
    
    import os
    statinfo = os.stat('laser_resampled.wav')

    ser.write(str(statinfo.st_size)+'\n')
    
    ack=ser.readline()
    ack=ser.readline()
    #print "First ack: ", ack
    w = open('laser_resampled.wav','rb')
    buff=''
    i=0
    try:
        byte = w.read(1)
        #byte=chr(ord(byte))
        while i < statinfo.st_size:
            # Send byte
            buff=buff+byte
            if len(buff) == 1024 or i == (statinfo.st_size - 1):
                
                ack=ser.write(buff)
                buff=''
                print ack, ' bytes sent. ', (100*(statinfo.st_size - i)/statinfo.st_size), " % remaining"
            i=i+1
            byte = w.read(1)
    finally:
        w.close()

    ser.close()