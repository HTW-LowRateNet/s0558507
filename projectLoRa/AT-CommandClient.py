import serial
import io
import time

import mods.message_check_method as checker
from _thread import start_new_thread

#serial connection
#ser = serial.Serial (port = "/dev/ttyS0")#Open named port)
ser = serial.Serial (port = "/dev/ttyUSB0")#Open named port)
ser.timeout = 0.3
ser.baudrate = 115200

#Koordinator Semaphore
#IAMCAPTAIN = false

if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
read = ""
state =""
message = []
knownaddr = []
ownaddr = ""


print("Initializing the device ..")


'''
###
Outsourced
###

messageCodes = [
    ('ALIV', 1 ),
    ('KDIS', 2),
    ('ADDR', projectLoRa),
    ('POLL', 4),
]
messageCodes.sort() # Sorts the list in-place



def makeKoordinator():
    pass

def checkMessage(message):
    global messageCodes
    try:
        return next(x for x in messageCodes if message[projectLoRa] in x)
    except StopIteration:
        raise ValueError("No matching record found")

def checkKoordinator(line):
    #koordinator hat 0000
    if message[1] == "0000":
        return 1
    else:
        return -1

'''

#CommandSend Method
def sendCommand(command):
    sio.write(command + '\r\n')
    sio.flush()
    sio.readline()

#InitialConfig methode
def initalConfig():
    rstAT = "AT+RST"
    setAddrAT= "AT+ADDR=FFFF"
    getAddrAT= "AT+ADDR?"
    getDestAT= "AT+DEST?"
    cfgAT = "AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4"
    rxAT = "AT+RX"
    saveAT = "AT+SAVE"
    commands = ([rstAT, cfgAT, setAddrAT, getAddrAT, saveAT, getDestAT, rxAT])
    for i in commands:
        print(i)
        sendCommand(i)

#ReadLine Funktion
def readSerialLine():
    
    global read
    global state
    global message
    global knownaddr
    global ownaddr


    while 1:
        read = sio.readline()       
        if read != "":
            message = read.split(',')
            check = checker.checkKoordinator(message)
            check2 = checker.checkMessage(message)
            print("MessageCODE = "+check2)
            print(check)
            print(message)
            print(read)

#ReadLineThread
start_new_thread(readSerialLine,())

#InitialConfig to configure the LoRa Modul
initalConfig()


#Main Loop
while 1:
    input_val = input("> ")
    if input_val == 'exit':
        ser.close()
        exit()
    else:
        sio.write(input_val + '\r\n')
        sio.flush()
ser.close()


