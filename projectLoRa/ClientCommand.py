import serial
import io
import time
import random
import Client as client
import Message
from _thread import start_new_thread

#ser = serial.Serial ("/dev/ttyUSB1")#Open named port)
ser = serial.Serial ("/dev/ttyUSB0")#Open named port)
ser.timeout = 0.5
ser.write_timeout = 0.5
ser.baudrate = 115200


#unbedingt implementieren .... das sorgt dafür den BufferVernünftig zu Managen
#ser.inWaitung()

read = ""
message = []

if(not ser.isOpen()):
    ser.open()

sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))#BufferedRWPair(ser,ser))

client = client.Client("NEW",sio,"",[])

start_new_thread(client.config,())

def readSerialLine():
    
    global read
    global message
    while 1:
        if ser.out_waiting < 1:
            if ser.in_waiting > 0:
                read = sio.readline()
                time.sleep(.100)
                #if read != "":
                print(read)
                tempMessage = read.split(',')
                if len(tempMessage) > 8:
                    message = tempMessage
                    client.messageObj = Message.Message(message[3],message[4],message[5],message[6],message[7],message[8],",".join(message[9:]))
                    if not client.messageInStore(client.messageObj):
                        checkMessageType(client.messageObj)
                        client.appendToMessageStore(client.messageObj)#client.messageObj.getMessage())
                    else:
                        print("##### MESSAGE IGNORE #########")
                        print(read+" EXIST")
                if len(tempMessage) > 10:
                    pass#break
                    
            #print("STATE = "+client.state)
            #koennte besser sein hier ebenfalls mit entsprechender Zeit einschrnkung zu arbeiten damit gebe ich allgemein den Takt fuer alle Aktionen auf dem Geraet an welches sich entsprechend besser handlen laesst
            if client.configured:
                checkForAction()
            #ser.flush()
            #ser.reset_input_buffer()
            #ser.reset_output_buffer()
        
                              
                
def checkForAction():
    if not client.coordinatorAliv and client.state == "NEW" and client.configured:
        #if client.cdis <= 3 and client.configured:
        #print("ich will --> cdis == "+str(client.cdis))
        if client.cdis == 12:
            print("cdis = "+str(client.cdis))
            #client.state = "COOR"
            #client.setAddrModul("0000")
            client.setupCoordinator()
            client.sendAlive()
            return
        else:
            timeN = time.time()
            actualDelta = timeN - client.deltaTime
            #print("DELTATIME --> " +str(actualDelta))
            if actualDelta > 1:
                client.deltaTime = time.time()
                client.adrDiscovery()
    if(client.state == "COOR"):
        timeN = time.time()
        actualDelta = timeN - client.deltaTime
        #print("DELTATIME --> " +str(actualDelta))
        if actualDelta > 5:
            client.deltaTime = time.time()
            client.sendAlive()
            #print(client.messageStore)
            
    if(client.state == "CL"):
        pass
        '''
        timeN = time.time()
        actualDelta = timeN - client.deltaTime
        if actualDelta > 20:
            client.deltaTime = time.time()
            #client.sendNeighboorDisc()
            #print(client.messageStore)
     #   return
        '''

def checkMessageType(message):
    ####################
    ####    HANDLE MESSAGE TYPE ALIV
    ###################
    #### TODO: FORWARDING ALIV ABFANGEN !!!!!
    print("####################### imessageTYPE -> : "+message.type)
    if message.type == "ALIV":
        print("####################### i have recieve a TRUE ALIV MESSAGE!!")
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
        print("####################### ADDR REQUEST OR RESPONSE MESSAGE")
        if(client.state == "COOR"):
            print("MyState is actually = "+client.state)
            client.sendAddrResponse(message.srcAddr)
            return
        if(client.state == "NEW" and message.destAddr == client.addr):
            print("MyState is actually = "+client.state+"is set to --> ")
            client.state = "CL"
            print("MyState is actually = "+client.state)
            print("I will set me a new Address from --> "+client.addr+" --> to --> "+message.msg)
            time.sleep(.200)
            newAdress = message.msg
            #newAdress = newAdress.replace("\r\n","")
            client.setAddrModul(newAdress[0:4])#.upper.zfill(4))
            time.sleep(.200)
            #ser.reset_
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
        print("####################### ADDR REQUEST ACKNOWLEDGE")
        if(client.state == "COOR"):
            print("MyState is actually = "+client.state)
            #save the new adress and send it to the client
            client.coordinatorAddrCounter = client.coordinatorAddrCounter + 1
            aackAddr = str(message.srcAddr).upper().zfill(4)
            client.coordinatorAddrStore.append(aackAddr)
            print("ADDRESSSTORE --> "+str(client.coordinatorAddrStore))
            #client.sendAddrResponse(message.srcAddr)
            return
        if(client.state == "CL"):
            client.sendForwardMessage(message)
            return
    
    
    ####################
    ####    HANDLE MESSAGE TYPE CDIS
    ###################
    if message.type == "CDIS":
        print("####################### CDIS REQUEST MESSAGE")
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
        client.sendForwardMessage(message)
        client.config()
        
    if message.type == "DISC":
        print("####################### DISC MESSAGE")
        for i in client.nb:
            if i != str(message.srcAddr): 
                client.nb.append(str(message.srcAddr))
                client.nb.sort()
                break
        print(str(client.nb))
        client.sendForwardMessage(message)
    
    if message.type == "MSSG":
        print("####################### MSSG MESSAGE")
        if client.state == "CL":
            client.sendForwardMessage(message)
        if client.state == "COOR":
            client.sendForwardMessage(message)
        

start_new_thread(readSerialLine,())


#keyboard input
while 1:
    #readSerialLine()
    input_val = input("> ")
    if input_val == 'exit':
        ser.close()
        exit()
    else:
        client.sendMSSG(input_val)
        #sio.write(input_val + '\r\n')
        #sio.flush()
        #print(">>"+sio.readline())
 
ser.close()