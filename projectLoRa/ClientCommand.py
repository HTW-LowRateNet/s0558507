import serial
import io
import time
import random
import Client as client
import Message
from _thread import start_new_thread

#ser = serial.Serial ("/dev/ttyUSB1")#Open named port)
ser = serial.Serial ("/dev/ttyUSB0")#Open named port)
ser.timeout = 0.1
ser.baudrate = 115200

#unbedingt implementieren .... das sorgt dafür den BufferVernünftig zu Managen
#ser.inWaitung()

read = ""
message = []

if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))

client = client.Client("NEW",ser,"",[])

start_new_thread(client.config,())

def readSerialLine():
    
    global read
    global message
    while 1:
        #if ser.isWaiting() > 4:
        #Dann erst ReadLine
        #
        if ser.inWaiting():
            read = sio.readline()
            #if read != "":
            print(read)
            tempMessage = read.split(',')
            if len(tempMessage) > 4:
                message = tempMessage
                client.messageObj = Message.Message(message[3],message[4],message[5],message[6],message[7],message[8],message[9])
                checkMessageType(client.messageObj)
                client.messageStore.append(client.messageObj.getMessage())
            #if len(tempMessage) > 10:
                #break
                
        #print("STATE = "+client.state)
        #koennte besser sein hier ebenfalls mit entsprechender Zeit einschrnkung zu arbeiten damit gebe ich allgemein den Takt fuer alle Aktionen auf dem Geraet an welches sich entsprechend besser handlen laesst
        if client.configured:
            checkForAction()
                    
                              
                
def checkForAction():
    if not client.coordinatorAliv and client.state == "NEW" and client.configured:
        #if client.cdis <= 3 and client.configured:
        #print("ich will --> cdis == "+str(client.cdis))
        if client.cdis == 1:
            print("cdis = "+str(client.cdis))
            client.state = "COOR"
            client.setAddrModul("0000")
            return
        else:
            timeN = time.time()
            actualDelta = timeN - client.deltaTime
            #print("DELTATIME --> " +str(actualDelta))
            
            if actualDelta > 10:
                client.deltaTime = time.time()
                client.adrDiscovery()
    if(client.state == "COOR"):
        timeN = time.time()
        actualDelta = timeN - client.deltaTime
        #print("DELTATIME --> " +str(actualDelta))
        if actualDelta > 10:
            client.deltaTime = time.time()
            client.sendAlive()
            print(client.messageStore)
    if(client.state == "CL"):
        timeN = time.time()
        actualDelta = timeN - client.deltaTime
        if actualDelta > 20:
            client.deltaTime = time.time()
            client.sendNeighboorDisc()
            print(client.messageStore)
     #   return


def checkMessageType(message):
    ####################
    ####    HANDLE MESSAGE TYPE ALIV
    ###################
    #### TODO: FORWARDING ALIV ABFANGEN !!!!!
    if message.type == "ALIV":
        print("i have recieve a TRUE ALIV MESSAGE!!")
        client.coordinatorAliv = True
        client.cdis = 0
        # two coordinatorers eventually split action from check message to action use semaphores
        if(client.state == "COOR"):
            client.resetCoordinator()
            #client.state = "NEW"
            #client.setAddr()
            print("MyState is actually = "+client.state)
            return
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
            print("MyState is actually = "+client.state+"is set to --> ")
            client.state = "CL"
            print("MyState is actually = "+client.state)
            print("I will set me a new Address from --> "+client.addr+" --> to --> "+message.msg)
            client.setAddrModul(str(message.msg))
            time.sleep(0.1)
            client.sendAddrAckknowledge()
            print("MY NEW ADDR = "+client.addr)
            #######  ignore   #########
            ####### FORWARDING!!!!
            #### SET NACHRICHTEN UND WEITERLEITEN
            #!!!!!!!!!
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
            client.coordinatorAddrCounter = client.coordinatorAddrCounter + 1
            aackAddr = str(message.srcAddr)
            client.coordinatorAddrStore.append(aackAddr)
            print("ADDRESSSTORE --> "+str(client.coordinatorAddrStore))
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
    #####
    ##  HandleNetworkReset
    ######
    if message.type == "NRST":
        client.config()
        
    if message.type == "DISC":
        for i in client.nb:
            if i != str(message.srcAddr): 
                client.nb.append(str(message.srcAddr))
                nb.sort()
                break
        print(str(client.nb))
    
    if message.type == "MSSG":
        if client.state == "CL" or client.state == "COOR":
            client.sendForwardMessage(message)
        
  
        
   
    

#while client.state == "NEW":
#    client.adrDiscovery(3)

start_new_thread(readSerialLine,())


#keyboard input
while 1:
    #readSerialLine()
    input_val = input("> ")
    if input_val == 'exit':
        ser.close()
        exit()
    else:
        sio.write(input_val + '\r\n')
        sio.flush()
        #print(">>"+sio.readline())
 
ser.close()