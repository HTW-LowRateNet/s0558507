import serial
import io
import time
import random
import Client as client
import Message
from _thread import start_new_thread

#ser = serial.Serial ("/dev/ttyUSB1")#Open named port)
ser = serial.Serial ("/dev/ttyUSB0")#Open named port)
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
        checkForAction()
        if read != "":
            print(read)
            tempMessage = read.split(',')
            if len(tempMessage) > 4:
                #time.sleep(1)
                message = tempMessage
                messageObj = Message.Message(message[3],message[4],message[5],message[6],message[7],message[8],message[9])
                checkMessageType(messageObj)
                
                              
                
def checkForAction():
    if(client.configured == True):
        if(client.state == "NEW" and client.coordinatorAliv == False):
            if(client.cdis <= 3):
                client.sendCoordinatorDisc()
                time.sleep(5)
                client.cdis = client.cdis + 1
                return
            if(client.cdis > 2):
                client.setupCoordinator()
                return

        if(client.state == "COOR"):
            client.sendAlive()
            return
        if(client.state == "CL"):
            client.sendNeighboorDisc()
            return
     #   return


def checkMessageType(message):
    ####################
    ####    HANDLE MESSAGE TYPE ALIV
    ###################
    if message.type == "ALIV":
        print("i have recieve a TRUE ALIV MESSAGE!!")
        client.coordinatorAliv = True
        client.cdis = 0
        # two coordinatorers eventually split action from check message to action use semaphores
        if(client.state == "COOR"):
            client.state = "NEW"
            client.setAddr()
            print("MyState is actually = "+client.state)
            return
        ### TOO MUCH
        if(client.state == "NEW"):
            ### SEND ADDR !!!!!
            client.sendAddrRequest()
            ### SEND CDIS !!!!!
            #client.sendCoordinatorDisc()
            print("MyState is actually = "+client.state)
            return
        
        if(client.state == "CL"):
            ## FORWARD ALIV MESSAAGE
            client.state = "CL"
            print("MyState is actually = "+client.state)
            client.sendForwardMessage(message)
            return
            
    ####################
    ####    HANDLE MESSAGE TYPE ADDR
    ###################
    if message.type == "ADDR":
        print("ADDR REQUEST OR RESPONSE MESSAGE")
        if(client.state == "COOR"):
            print("MyState is actually = "+client.state)
            client.sendAddrResponse(message.srcAddr)
            return
        if(client.state == "NEW" and message.destAddr == client.addr):
            print("MyState is actually = "+client.state)
            print("I will set me a new Address from --> "+client.addr+" --> to --> "+message.msg)
            client.setAddrModul(message.msg)
            client.sendAddrAckknowledge()
            client.state = "CL"
            print("MyState is actually = "+client.state)
            print("MY NEW ADDR = "+client.addr)
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
            print("MyState is actually = "+client.state)
            client.sendForwardMessage(message)
            return
                
    ####################
    ####    HANDLE MESSAGE TYPE ADDR
    ###################
    if message.type == "AACK":
        print("ADDR REQUEST ACKNOWLEDGE")
        if(client.state == "COOR"):
            print("MyState is actually = "+client.state)
            #save the new adress and send it to the client
            client.coordinatorAddrCounter = client.coordinatorAddrStore + 1
            client.coordinatorAddrStore.append(message.srcAddr)
            #client.sendAddrResponse(message.srcAddr)
            return
        
        #IGNORE FOR STATE NEW !!!!!! KISS
        #if(client.state == "NEW"):
            #print("MyState is actually = "+client.state)
            #######  ignore   #########
            # IAM in STATE NEW not AUTORIZED TO FORWARD MESSAGES!!!!
        if(client.state == "CL"):
            client.sendForwardMessage(message)
            return
    
    
    ####################
    ####    HANDLE MESSAGE TYPE CDIS
    ###################
    if message.type == "CDIS":
        print("CDIS REQUEST MESSAGE")
        if(client.state == "COOR"):
            print("MyState is actually = "+client.state)
            client.sendAlive()
            return

        ## NEW STATE NOT ALLOWED TO FORWARD MESSAGES
        #if(client.state == "NEW"):
            #print("MyState is actually = "+client.state)
            #######  ignore   #########
            ####### FORWARDING!!!!
            ## NEW STATE NOT ALLOWED TO FORWARD MESSAGES
         #   return
        if(client.state == "CL"):
            client.sendForwardMessage(message)
            return

start_new_thread(readSerialLine,())


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
