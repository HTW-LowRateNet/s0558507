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

client.config()



def readSerialLine():
    global read
    global message
    while 1:
        read = sio.readline()
        if read != "":
            print(read)
            tempMessage = read.split(',')
            if len(tempMessage) > 4:
                time.sleep(1)
                message = tempMessage
                messageObj = Message.Message(message[3],message[4],message[5],message[6],message[7],message[8],message[9])
                checkMessageType(messageObj)
                #checkForAction(messageObj)
                
                client.cdis = client.cdis + 1
                #if client.cdis < 4 and client.coordinatorAliv == False:
                
                client.sendCoordinatorDisc()

def checkMessageType(message):
    ####################
    ####    HANDLE MESSAGE TYPE ALIV
    ###################
    if message.type == "ALIV":
        print("TRUE ALIV MESSAGE")
        # two coordinatorers
        if(client.state == "COOR"):
            client.state = "NEW"
            client.coordinatorAliv = True
            client.cdis = 0
            print(client.state)
            return
        
        if(client.state == "NEW"):
            client.coordinatorAliv = True
            client.state = "CL"
            client.cdis = 0
            print(client.state)
            return
        if(client.state == "CL"):
            client.coordinatorAliv = True
            client.state = "CL"
            client.cdis = 0
            print(client.state)
            return
            
    ####################
    ####    HANDLE MESSAGE TYPE ADDR
    ###################
    if message.type == "ADDR":
        print("ADDR REQUEST OR RESPONSE MESSAGE")
        if(client.state == "COOR"):
            print("Clientstate:"+client.state)
            #save the new adress and send it to the client
            client.sendAddrResponse(message.srcAddr)
            return
        if(client.state == "NEW"):
            print("Clientstate:"+client.state)
            #######  ignore   #########
            ####### FORWARDING!!!!
            #### SET NACHRICHTEN UND WEITERLEITEN
            
            #send ACK and set state to CL and set Addr
            #ACK lauft nicht ueber ADDR!!!
            #if(message.msgID==1):
                #client.setAddrModul(message.msg)
            #else
                
                #pass
            return
        if(client.state == "CL"):
            #ignore
            print("Clientstate:"+client.state)
            return
        
    ####################
    ####    HANDLE MESSAGE TYPE ADDR
    ###################
    if message.type == "AACK":
        print("ADDR REQUEST OR RESPONSE MESSAGE")
        if(client.state == "COOR"):
            print("Clientstate:"+client.state)
            #save the new adress and send it to the client
            client.sendAddrResponse(message.srcAddr)
            return
        if(client.state == "NEW"):
            print("Clientstate:"+client.state)
            #######  ignore   #########
            ####### FORWARDING!!!!
            #### SET NACHRICHTEN UND WEITERLEITEN
            
            #send ACK and set state to CL and set Addr
            #ACK lauft nicht ueber ADDR!!!
            #if(message.msgID==1):
                #client.setAddrModul(message.msg)
            #else
                
                #pass
            return
    
    
    ####################
    ####    HANDLE MESSAGE TYPE CDIS
    ###################
    if message.type == "CDIS":
        print("CDIS REQUEST MESSAGE")
        if(client.state == "COOR"):
            print("Clientstate:"+client.state)
            client.sendAlive()
            #save the new adress and send it to the client
            return
        if(client.state == "NEW"):
            print("Clientstate:"+client.state)
            #ignore
            return
        if(client.state == "CL"):
            #ignore
            return
  
start_new_thread(readSerialLine,())

#start_new_thread(runningDevice,())

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