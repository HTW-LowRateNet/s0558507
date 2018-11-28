import serial
import io
import time
from _thread import start_new_thread

ser = serial.Serial (port = "/dev/ttyS0")#Open named port)
ser.timeout = 0.3
ser.baudrate = 115200     

if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
print("Initializing the device ..")

def sendCommand(command):
    sio.write(command + '\r\n')
    sio.flush()
    sio.readline()

def initalConfig():
    rstAT = "AT+RST"
    setAddrAT= "AT+ADDR=2020"
    getAddrAT= "AT+ADDR?"
    getDestAT= "AT+DEST?"
    cfgAT = "AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4"
    rxAT = "AT+RX"
    saveAT = "AT+SAVE"
    commands = ([cfgAT, setAddrAT, getAddrAT, saveAT, getDestAT, rxAT])
    for i in commands:
        print(i)
        sendCommand(i)

def readSerialLine():
    while 1:
        read = sio.readline()       
        if read != "":
            print(read)

start_new_thread(readSerialLine,())

initalConfig()
while 1:
    input_val = input("> ")
    if input_val == 'exit':
        ser.close()
        exit()
    else:
        sio.write(input_val + '\r\n')
        sio.flush()
ser.close()


