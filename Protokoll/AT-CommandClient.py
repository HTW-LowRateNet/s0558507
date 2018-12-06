import serial
import io
import time
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



messageCodes = [
    ('ALIV', 1 ),
    ('KDIS', 2),
    ('ADDR', 3),
    ('POLL', 4),
]
messageCodes.sort() # Sorts the list in-place



print("Initializing the device ..")

'''
MessageCodes aus der Praesi --- dient als Anhalt

KDIS = Koordinator Discovery
ADDR = Koordinator Sendet einem Client eine feste Adresse
MSSG = einfache Nachricht
POLL = Selbstanfrage zur Sicherstellung der eindeutigen Adresse
DISC = Entdeckung von allen Nachbarn
ALIV = Anfrage, ob ein Knoten noch in der Naehe ist (Eigentlich durch DISC abgedeckt)
'''

'''
#RoutingTabelle {<String>,<String,Int>}
routingTable = {"0000":{"":1}}
'''

'''
#NeighboorDiscovery
def neighboorDiscovery():
    pass
'''

'''
def incrementHex(valhex):
    return str(valhex+1)
    #return hex(valhex+1)
'''

def makeKoordinator():
    pass

def checkMessage(message):
    global messageCodes
    return 1
    '''
    try:
        return next(x for x in messageCodes if message[3] in x)
    except StopIteration:
        raise ValueError("No matching record found")
    '''
    
def checkKoordinator(line):
    #koordinator hat 0000
    if message[1] == "0000":
        return 1
    else:
        return -1

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
    commands = ([cfgAT, setAddrAT, getAddrAT, saveAT, getDestAT, rxAT])
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
            check = checkKoordinator(message)
            check2 = checkMessage(message)
            #print("MessageCODE = "+check2)
            print(check)
            print(message)
            print(read)

#ReadLineThread
start_new_thread(readSerialLine,())

#InitialConfig to configure the LoRa Modul
initalConfig()


#Main Loop ueberarbeiten da ich ja jetzt SendCommand besitze
while 1:
    input_val = input("> ")
    if input_val == 'exit':
        ser.close()
        exit()
    else:
        sio.write(input_val + '\r\n')
        sio.flush()
ser.close()


