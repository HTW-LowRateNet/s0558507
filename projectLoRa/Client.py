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
        self.nb = []
        self.sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
        self.cdis = 0 #is a counter for cdis message
        #messageQueue
        self.messageStore = []
        self.messageObj = m.Message("type","msgID","ttl","hops","srcAddr","destAddr","msg")
        
        self.messageTupel = (self.messageObj,time.time())
        
        self.coordinatorAddrCounter = 256 #is a counter for the adress generator this is an integer
        #coordinatorAddrStore.append(WERT)
        self.coordinatorAddrStore = []
        #coordinatorAddrStore.append(256)
        self.coordinatorAliv = False
        self.configured = False
        #self.config()
        self.deltaTime = time.time()
        
        
    def config(self):
        count = 0
        self.state = "NEW"
        self.configured = False
        print("initial config..")
        #time.sleep(1)
        #self.configured = True
        self.sio.write('AT+RST\r\n')
        self.sio.flush()
        time.sleep(0.1)
        count = count + 1
       
        
        self.sio.write('AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4\r\n')
        self.sio.flush()
        time.sleep(0.1)
        count = count + 1
        
        #self.setAddr()
        
        self.sio.write('AT+SAVE\r\n')
        self.sio.flush()
        time.sleep(0.1)
        count = count + 1
        
        self.sio.write('AT+RX\r\n')
        self.sio.flush()
        time.sleep(0.1)
        count = count + 1
        
        self.sio.write('AT+DEST=FFFF\r\n')
        self.sio.flush()
        time.sleep(0.1)
        count = count + 1
        
        self.setAddr()
        count = count + 1
        
        if count == 6:
            self.configured = True
        self.cdis = 0
        self.coordinatorAddrCounter = 256
        self.coordinatorAddrStore = []
        self.coordinatorAliv = False
        
        '''
        rxAT = "AT+RX"
        saveAT = "AT+SAVE"
        dstAT = "AT+DEST=FFFF"
        cfgAT = "AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4"
        commands = ([cfgAT, saveAT, rxAT])
        for i in commands:
            print(i)
            self.sendCommand(i)
            if i == len(commands):
                self.configured = True
        '''
       
        '''
        self.sio.write('AT+RST\r\n')
        self.sio.flush()
        time.sleep(0.500)
        '''
        
        '''
        cfgAT = "AT+CFG=433000000,20,9,10,1,1,0,0,0,0,3000,8,4"
        rstAT = "AT+RST"
        rxAT = "AT+RX"
        saveAT = "AT+SAVE"
        saveDST
        = "AT+DEST=FFFF"
        '''
        
        
        
    
    def setAddrModul(self,newAddr):
        #addrCMD = "AT+ADDR="+addr+"\r\n"
        #self.sendCommand(addrCMD)
        self.sio.write('AT+RST\r\n')
        self.sio.flush()
        time.sleep(0.2)
        self.sio.write('AT+ADDR='+newAddr+'\r\n')
        self.sio.flush()
        time.sleep(0.2)
        self.sio.write('AT+SAVE\r\n')
        self.sio.flush()
        self.addr = newAddr
        
        
    def setAddr(self):
        tempAddr = ""
        if self.state == "NEW":
            tempAddr = str(random.randint(16,100))           
        if self.state == "COOR":
            tempAddr = "0000"
        if self.state == "CL":
            #(type,msgID,ttl,hops,ownAddr,destAddr,msg):
            message = m.Message("ADDR","0","0","0",self.addr,"0","")
            print(message.toString)
            #tempAddr = "300"
        self.addr = tempAddr
        self.sio.write('AT+ADDR='+tempAddr+'\r\n')
        self.sio.flush()
        print("Own Address is set to: "+self.addr)
    
      
    
    
    #PayLoad are only by request on the CoordinatorDiscovery ADDR or CDIS?!?!?
    #eventually the while must be droped
    def sendAlive(self):
        #while self.state == "COOR":
        time.sleep(0.01)
        message = m.Message("ALIV",self.uniqueMID(),"100","0",self.addr,"FFFF","I am the captian!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage())
        #self.appendToMessageStore(message.getMessage())
        self.messageTupel = (message,time.time())
        #self.appendToMessageStore( self.messageTupel)
            
    def sendNeighboorDisc(self):
        #while self.state == "CL":
        time.sleep(0.01)
        message = m.Message("DISC",self.uniqueMID(),"1","0",self.addr,"FFFF","NeighBROO's???")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage())
        #self.appendToMessageStore(message.getMessage())
        self.messageTupel = (message,time.time())
        #self.appendToMessageStore( self.messageTupel)
                                   
    def sendCoordinatorDisc(self):
        #while self.state == "NEW":
        time.sleep(0.01)
        message = m.Message("CDIS",self.uniqueMID(),"100","0",self.addr,"FFFF","where is my captain!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage())
        #self.appendToMessageStore(message.getMessage())
        self.messageTupel = (message,time.time())
        #self.appendToMessageStore( self.messageTupel)
            
    def sendAddrRequest(self):
        #while self.state == "NEW":
        time.sleep(0.01)
        message = m.Message("ADDR",self.uniqueMID(),"10","0",self.addr,"0000","captain give me a job!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage())
        #self.appendToMessageStore(message.getMessage())
        self.messageTupel = (message,time.time())
        #self.appendToMessageStore( self.messageTupel)
        
    def sendAddrAckknowledge(self):
        #while self.state == "NEW":
        time.sleep(0.01)
        message = m.Message("AACK",self.uniqueMID(),"10","0",self.addr,"0000","captain thanks for the job!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage())
        #self.appendToMessageStore(message.getMessage())
        self.messageTupel = (message,time.time())
        #self.appendToMessageStore( self.messageTupel)
    
    #this message is the only one of controlmessages that recieve an payload 
    def sendAddrResponse(self,requestAddress):
        #while self.state == "COOR":
        time.sleep(0.01)
        generatedAdress = str(self.generateNewAddress())
        #0x0000 0x was cut for a better use
        newAdress = generatedAdress.replace("0x","",1).upper() 
        message = m.Message("ADDR",self.uniqueMID(),"10","0",self.addr,requestAddress,newAdress)
        message.send(self.sio,requestAddress)
        print("Sended Message -> "+message.getMessage())
        #self.appendToMessageStore(message.getMessage())
        self.messageTupel = (message,time.time())
        #self.appendToMessageStore( self.messageTupel)

    def sendForwardMessage(self, forwardMessage):
        if int(forwardMessage.ttl) > 1:
            time.sleep(0.01)
            forwardMessage.hops = int(forwardMessage.hops) + 1
            forwardMessage.ttl = int(forwardMessage.ttl) - 1
            forwardMessage.send(self.sio,"FFFF")
            #self.appendToMessageStore(forwardMessage.getMessage())
            self.messageTupel = (forwardMessage,time.time())
            #self.appendToMessageStore( self.messageTupel)
            return
    
    #need to run an dummy 
    def adrDiscovery(self):
        #while i==0:
        print("!!!!!!!!!!CDIS AUFRUF!!!!!!!!!")
        print("Address Discovery..")
        time.sleep(0.1)
        self.sendCoordinatorDisc()
        time.sleep(0.1)
        if self.coordinatorAliv:
            return
        self.cdis = self.cdis + 1
        
            
    #CommandSend Method
    def sendCommand(self,command):
        self.sio.write(command + '\r\n')
        self.sio.flush()
        self.sio.readline()
        time.sleep(0.2)
    
    def generateNewAddress(self):
        #self.coordinatorAddrCounter = self.coordinatorAddrCounter + 1
        newAddress = hex(self.coordinatorAddrCounter+1)
        return newAddress
        
    def setupCoordinator(self):
        self.state = "COOR"
        self.cdis = 0
        self.coordinatorAliv = True
        self.setAddr()
    
    def resetCoordinator(self):
        #for i in xrange(3):
        message = m.Message("NRST",self.uniqueMID(),"100","0",self.addr,"FFFF","RESET THE NETWORK ... KNOW!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage())
        time.sleep(1)
        message = m.Message("NRST",self.uniqueMID(),"100","0",self.addr,"FFFF","RESET THE NETWORK ... KNOW!")
        message.send(self.sio,"FFFF")
        print("Sended Message -> "+message.getMessage())
        self.config()
        
        #self.state = "NEW"
        
        #self.setAddr()
        
    def uniqueMID(self):
        return str(random.randint(0,999999))
    
    def appendToMessageStore(self,messageTupel):
        self.messageStore.append(messageTupel)