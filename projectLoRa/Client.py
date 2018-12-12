import serial
import io
import time
import random
import Message as m

class Client:
    def __init__(self,state,ser,addr,nabore):
        self.state = state
        self.addr = addr
        self.ser = ser
        self.nabore = nabore
        self.sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
        self.cdis = 0 #is a counter for cdis message
        self.addressCounter = 256 #is a counter for the adress generator this is an integer
        
    def config(self):
        self.state = "NEW"
        print("initial config..")
        self.sio.write('AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4\r\n')
        self.sio.flush()
        time.sleep(1)
        self.setAddr()
 
    
    def setAddr(self):
        tempAddr = ""
        if self.state == "NEW":
            tempAddr = str(random.randint(16,100))           
        if self.state == "COOR":
            tempAddr = "0"
        if self.state == "CL":
            #(type,msgID,ttl,hops,ownAddr,destAddr,msg):
            message = m.Message("ADDR","0","0","0",self.addr,"0","")
            print(message.toString)
            #tempAddr = "300"
    
        self.addr = tempAddr
        self.sio.write('AT+ADDR='+tempAddr+'\r\n')
        self.sio.flush()
        print("Own Address is set to: "+self.addr)
    
      
    '''
    SEND ALIV AS KOORDINATOR STATE
    '''
    #PayLoad are only by request on the CoordinatorDiscovery ADDR or CDIS?!?!?
    #eventually the while must be droped
    def sendAlive(self):
        while self.state == "COOR":
            message = m.Message("ALIV","0","0","0",self.addr,"ffff","I am the captian!")
            message.send(self.sio,"ffff")
            print(message.messageSize())
            
    def sendNeighboorDisc(self):
        while self.state == "CL":
            message = m.Message("DISC","0","1","0",self.addr,"ffff","where are my bro's!")
            message.send(self.sio,"ffff")
            print(message.messageSize())
            
    def sendCoordinatorDisc(self):
        while self.state == "NEW":
            message = m.Message("CDIS","0","10","0",self.addr,"0000","where are my captain!")
            message.send(self.sio,"ffff")
            print(message.messageSize())   
    
    def sendAddrRequest(self):
        while self.state == "NEW":
            message = m.Message("ADDR","0","10","0",self.addr,"0000","captain give me a job!")
            message.send(self.sio,"ffff")
            print(message.messageSize())
    
    #this message is the only one of controlmessages that recieve an payload 
    def sendAddrResponse(self):
        while self.state == "COOR":
            newAdress = str(self.generateNewAddress())
            newAdress.replace("0x","",1)#0x0000 0x was cut for a better use
            message = m.Message("ADDR","1","10","0",self.addr,"0000",newAdress)
            message.send(self.sio,"ffff")
            print(message.messageSize())
            
                
            
              
    #need to run an dummy 
    def adrDiscovery(self, message,i):
        print("Address Discovery..")
        self.sio.write('AT+RX\r\n')
        self.sio.flush()
        time.sleep(1)
        if message == "ALIV":
            print("I am not the Captian")
            self.state = "CL"
            print("new message from coordinator")
            self.setAddr()
            #ASK for a new Adress
            setAddr()
            
        if self.state == "NEW" and i== 0:
            self.state= "COOR"
            self.setAddr()
           # coordinatorSendNotify()
        time.sleep(1)
        
        
    def generateNewAddress():
        addressCounter + 1
        newAddress = hex(addressCounter)
        return newAddress
        
    