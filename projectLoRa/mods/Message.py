import time

'''
Message class is importen for the next steps ... it is a standard container for a message in the network 
'''
class Message:
    rn = "\r\n"

    def __init__(self, type, mID, srcAddr, dstAddr, ttl, hops, msg):
        self.type = type
        self.msgID = mID
        self.srcAddr = srcAddr
        self.dstAddr = dstAddr
        self.ttl = ttl
        self.hops = hops
        self.msg = msg

    # this message Pattern was given by the team
    def getMessage(self):
        return str(
            self.type + "," + self.mID + "," + self.ttl + "," + self.hops + "," + self.ownAddr + "," + self.destAddr + "," + self.msg + ",")

    # send Message ... source is the getMessage
    def send(self, sio, dest):
        time.sleep(1)
        sio.write('AT+SEND=' + str(len(self.getMessage())) + '\r\n')
        sio.flush()
        time.sleep(1)
        sio.write(self.getMessage())
