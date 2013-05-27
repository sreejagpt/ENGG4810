
def send_config_to_mpc():
    try:
        w = open('C:\\Python27\\ENGG4810\\config.cfg','rb')
    except Exception:
        print "Oh no!"
    import serial
    ser = serial.Serial()
    ser.port=11
    ser.baudrate=115200
    
    ser.open()

    #ser.flush()
    ser.write("cf.cfgH\n")
    ack=ser.readline()
    
    #print "I am expecting the filename here as ACK:: ", ack
    
    import os
    statinfo = os.stat('C:\\Python27\\ENGG4810\\config.cfg')

    ser.write(str(statinfo.st_size)+'\n')
    
    ack=ser.readline()
    print "First ack: ", ack
    
    print "I am expecting the filesize here as ACK:: ", ack
    buff=''
    for line in w:
        buff = buff+line
    print "Now sending file ", buff
    ser.write(buff)
    ack=ser.readline()
    print "I just received this ack:: ", ack
    
    ser.close()
    w.close()

def send_wav_to_mpc(filename, button, holdlatch):
    
    import serial
    ser = serial.Serial()
    ser.port=11
    ser.baudrate=115200
    ser.open()
    #ser.flush()
    if int(button) < 10:
        button = '0'+str(button)
    ser.write(str(button)+".wav"+str(holdlatch)+"\n")
    ack=ser.readline()
    
    print "I am expecting the filename here as ACK:: ", ack
    
    import os
    statinfo = os.stat(str(filename))

    ser.write(str(statinfo.st_size)+'\n')
    
    ack=ser.readline()
    ack=ser.readline()
    print "First ack: ", ack
    w = open(filename,'rb')
    buff=''
    i=0
    try:
        byte = w.read(1)
        
        while i < statinfo.st_size:
            # Send byte
            buff=buff+byte
            if len(buff) == 1024 or i == (statinfo.st_size - 1):
                ack=ser.write(buff)
                #print ack
                buff=''
                print (100*(statinfo.st_size - i)/statinfo.st_size), "% remaining"
                
            i=i+1
            byte = w.read(1)
    finally:
        w.close()

    ser.close()
    return

if __name__ == '__main__':
    send_config_to_mpc()
    #send_config_to_mpc()

    send_wav_to_mpc('C:\\Python27\\ENGG4810\\sleepyhead_resampled.wav', 11, 'H')
    #show_wave_n_spec('sound3.wav')
