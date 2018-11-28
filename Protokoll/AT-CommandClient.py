import serial
import io
import time
from _thread import start_new_thread

#serial connection
ser = serial.Serial (port = "/dev/ttyS0")#Open named port)
ser.timeout = 0.3
ser.baudrate = 115200

#RoutingTabelle {<String>,<String,Int>}
routingTable = {"0000":{"":1}}

if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
print("Initializing the device ..")

'''
KDIS = Koordinator Discovery
ADDR = Koordinator Sendet einem Client eine feste Adresse
MSSG = einfache Nachricht
POLL = Selbstanfrage zur Sicherstellung der eindeutigen Adresse
DISC = Entdeckung von allen Nachbarn
ALIV = Anfrage, ob ein Knoten noch in der Nähe ist (Eigentlich durch DISC abgedeckt)
'''


#NeighboorDiscovery
def neighboorDiscovery():
    pass


def incrementHex(valhex):
    return str(valhex+1)
    #return hex(valhex+1)

def checkKoordinator():
    #koordinator hat 0000
    
    pass


#CommandSend Method
def sendCommand(command):
    sio.write(command + '\r\n')
    sio.flush()
    sio.readline()

#InitialConfig methode
def initalConfig():
    rstAT = "AT+RST"
    setAddrAT= "AT+ADDR=00FF"
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
    while 1:
        read = sio.readline()       
        if read != "":
            print(read)

#ReadLineThread
start_new_thread(readSerialLine,())

#InitialConfig to configure the LoRa Modul
initalConfig()


#Main Loop überarbeiten da ich ja jetzt SendCommand besitze
while 1:
    input_val = input("> ")
    if input_val == 'exit':
        ser.close()
        exit()
    else:
        sio.write(input_val + '\r\n')
        sio.flush()
ser.close()


