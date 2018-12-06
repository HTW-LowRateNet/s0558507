import time

'''
Message class is importen for the next steps ... it is a standard container for a message in the network 
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
        string = self.type + "," + self.mID + "," + self.ttl + "," + self.hops + "," + self.srcAddr + "," + self.dstAddr + "," + self.msg + ","
        return string
    
    # send Message ... source is the getMessage
    def send(self, sio):
        time.sleep(1)
        print(self.getMessage())
        sio.write('AT+SEND=' + str(len(self.getMessage())) + '\r\n')
        sio.flush()
        time.sleep(1)
        sio.write(self.getMessage())
