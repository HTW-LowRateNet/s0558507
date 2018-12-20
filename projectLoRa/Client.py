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
        
        #messageQueue
        self.messageSet = {}
        
        
        self.coordinatorAddrCounter = 256 #is a counter for the adress generator this is an integer
        #coordinatorAddrStore.append(WERT)
        self.coordinatorAddrStore = []
        #coordinatorAddrStore.append(256)
        self.coordinatorAliv = False
        
        
    def config(self):
        self.state = "NEW"
        print("initial config..")
        rstAT = "AT+RST"
        rxAT = "AT+RX"
        saveAT = "AT+SAVE"
        saveDST = "AT+DEST=FFFF"
        
        self.sio.write('AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4\r\n')
        self.sio.flush()
        time.sleep(1)
        
        self.setAddr()
        
        self.sio.write('AT+SAVE\r\n')
        self.sio.flush()
        time.sleep(1)
        
        #self.sio.write('AT+RST\r\n')
        #self.sio.flush()
        #time.sleep(1)
        
        self.sio.write('AT+RX\r\n')
        self.sio.flush()
        time.sleep(1)
        
        self.sio.write('AT+DEST=FFFF\r\n')
        self.sio.flush()
        time.sleep(1) 
  
    def setAddrModul(self,addr):
        self.addr =addr
        self.sio.write('AT+ADDR='+self.addr+'\r\n')
        self.sio.flush()
        
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
        #while self.state == "COOR":
        message = m.Message("ALIV","0","0","0",self.addr,"FFFF","I am the captian!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage())    
            
    def sendNeighboorDisc(self):
        #while self.state == "CL":
        message = m.Message("DISC","0","1","0",self.addr,"FFFF","where are my bro's!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage())    
            
    def sendCoordinatorDisc(self):
        #while self.state == "NEW":
        message = m.Message("CDIS","0","10","0",self.addr,"FFFF","where are my captain!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage()) 
            
    def sendAddrRequest(self):
        #while self.state == "NEW":
        message = m.Message("ADDR","0","10","0",self.addr,"0000","captain give me a job!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage()) 
        
    def sendAddrAckknowledge(self):
        #while self.state == "NEW":
        message = m.Message("AACK","0","10","0",self.addr,"0000","captain thanks for the job!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage()) 
    
    #this message is the only one of controlmessages that recieve an payload 
    def sendAddrResponse(self,requestAddress):
        #while self.state == "COOR":
        newAdress = str(self.generateNewAddress())
        #0x0000 0x was cut for a better use
        newAdress.replace("0x","",1).upper 
        message = m.Message("ADDR","1","10","0",self.addr,requestAddress,newAdress)
        message.send(self.sio,requestAddress)
        print("Sended Message -> "+message.getMessage())

    
    def sendALIVForward(self,sio,forwardAlivMessage):
        if(forwardAlivMessage.ttl > 1):
            forwardAlivMessage.hops = forwardAliv.hops + 1
            forwardAlivMessage.ttl = forwardAliv.ttl - 1
            forwardAlivMessage.send(self.sio,"FFFF")
            return
    
    def sendForwardMessage(self, sio, forwardMessage):
        if(forwardMessage.ttl > 1):
            forwardMessage.hops = forwardMessage.hops + 1
            forwardMessage.ttl = forwardMessage.ttl - 1
            forwardMessage.send(self.sio,"FFFF")
            return
    
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
        
    #CommandSend Method
    def sendCommand(command):
        sio.write(command + '\r\n')
        sio.flush()
        sio.readline()
    
    def generateNewAddress():
        #addressCounter + 1
        newAddress = hex(addressCounter)
        return newAddress
        
    
    