import serial
import io
import time
from _thread import start_new_thread

ser = serial.Serial (
    port = "/dev/ttyS0")#Open named port)
ser.timeout = 0.1
ser.baudrate = 115200                     #Set baud rate to 9600


if(not ser.isOpen()):
    ser.open()

print("Initializing the device ..")
sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))

def readSerialLine():
    while 1:
        read = sio.readline()       
        if read != "":
            print(read)

def initalConfig():
    cfgAT = "AT+CFG=433000000,20,6,12,1,1,0,0,0,0,3000,8,4"
    sio.write(cfgAT + '\r\n')
    rxAT = "AT+RX"
    sio.write(rxAT + '\r\n')

#initalConfig()
start_new_thread(readSerialLine,())

while 1:          
    input_val = input("> ")
    if input_val == 'exit':
        ser.close()
        exit()
    else:
        sio.write(input_val + '\r\n')
        sio.flush()
        #print(">>"+sio.readline())
  
ser.close()
