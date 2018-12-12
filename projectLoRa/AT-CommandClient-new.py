import serial
import io
import time
import random
import Client as client
import Message
from _thread import start_new_thread

ser = serial.Serial ("/dev/ttyUSB1")#Open named port)
#ser = serial.Serial ("/dev/ttyUSB0")#Open named port)
ser.timeout = 0.3
ser.baudrate = 115200

read = ""
message = []

if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
client = client.Client("NEW",ser,"",[])



def readSerialLine():
    global read
    global message
    while 1:
        read = sio.readline()
        if read != "":
            print(read)
            tempMessage = read.split(',')
            if len(tempMessage) > 4:
                message = tempMessage
                messageObj = Message.Message(message[3],message[4],message[5],message[6],message[7],message[8],message[9])
                checkMessageType(messageObj)
                #checkForAction(messageObj)


def checkMessageType(message):
    if message.type == "ALIV":
        print("TRUE ALIV MESSAGE")
        if(client.state == "KOOR"):
            client.state = "NEW"
            print(client.state)
            pass
        if(client.state == "NEW"):
            client.state = "CL"
            print(client.state)
            pass
        if(client.state == "CL"):
            client.state = "CL"
            print(client.state)
            pass
    if message.type == "CDIS":
        client.sendAlive()
        pass
    if message.type == "ADDR":
        
        pass
    if message.type == "ALIV":
        pass
    #Client state change to CL and dicoverA Address
    pass

def runningDevice():
    if(client.state == "KOOR"):
        client.sendAlive
    
    pass



start_new_thread(readSerialLine,())
start_new_thread(runningDevice,())

#keyboard input
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