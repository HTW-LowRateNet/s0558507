import time

'''
Message class is importen for the next steps ... it is a standard container for a message in the network 
'''

'''
class Message:
    rn = "\r\n"

    def __init__(self, type, mID, ttl, hops, srcAddr, dstAddr, msg):
        self.type = type
        self.mID = mID
        self.ttl = ttl
        self.hops = hops
        self.srcAddr = srcAddr
        self.dstAddr = dstAddr
        self.msg = msg

    
    # this message Pattern was given by the team
    def getMessage(self):
        string = self.type + "," + self.mID + "," + self.ttl + "," + self.hops + "," + self.srcAddr + "," + self.dstAddr + "," + self.msg
        return string
    
    # send Message ... source is the getMessage
    def send(self, sio):
        time.sleep(1)
        print(self.getMessage())
        sio.write('AT+SEND=' + str(len(self.getMessage())) + '\r\n')
        sio.flush()
        time.sleep(1)
        sio.write(self.getMessage())
'''
class Message:
    rn = "\r\n"
    def __init__(self,type,msgID,ttl,hops,srcAddr,destAddr,msg):
        self.type = type
        self.msgID = msgID
        self.ttl = ttl
        self.hops = hops
        self.srcAddr = srcAddr
        self.destAddr = destAddr
        self.msg = msg
        
    
    def messageSize(self):
        string = self.getMessage()
        size = len(string)
        return str(size)
           
    def getMessage(self):
        string = str(self.type)+","+str(self.msgID)+","+str(self.ttl)+","+str(self.hops)+","+str(self.srcAddr)+","+str(self.destAddr)+","+str(self.msg)
        return string
    
    def send(self,sio,dest):
        
        size = self.messageSize()
        sio.write('AT+SEND='+size+'\r\n')
        sio.flush()
        time.sleep(.100)
        #time.sleep(.100)
        #if sio.writable:
        #while not sio.writable:
        self.srcAddr = self.srcAddr.upper().zfill(4)
        sio.write(self.getMessage()+'\r\n')
        sio.flush
        time.sleep(.100)
        
        #time.sleep(0.2)
