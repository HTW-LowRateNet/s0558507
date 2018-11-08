import serial
import io
import time
from _thread import start_new_thread






ser = serial.Serial (port = "/dev/ttyS0")#Open named port)
ser.timeout = 0.1
ser.baudrate = 115200     



if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
print("Initializing the device ..")
def initalConfig():
    rstAT = "AT+RST"
    setAddrAT= "AT+ADDR=2020"
    getAddrAT= "AT+ADDR?"
    cfgAT = "AT+CFG=433000000,20,6,12,1,1,0,0,0,0,3000,8,4"
    rxAT = "AT+RX"
    saveAT = "AT+SAVE"
    #WriteConfig
    #sio.write(rstAT + '\r\n')
    sio.write(cfgAT + '\r\n')
    sio.flush()
    sleep(2)
    sio.write(setAddrAT + '\r\n')
    sio.flush()
    sleep(2)
    sio.write(getAddrAT + '\r\n')
    sio.flush()
    sleep(2)
    sio.write(saveAT + '\r\n')
    sio.flush()
    sleep(2)
    sio.write(rxAT + '\r\n')
    sio.flush()
    sleep(2)
    print("ich wurde ausgeführt")


def readSerialLine():
    while 1:
        read = sio.readline()       
        if read != "":
            print(read)

start_new_thread(readSerialLine,())
initalConfig()
while 1:
    #i=1
    #if i == 1:
        #initalConfig()
        #i=i+1
    input_val = input("> ")
    if input_val == 'exit':
        ser.close()
        exit()
    else:
        sio.write(input_val + '\r\n')
        sio.flush()
        #print(">>"+sio.readline())
ser.close()


