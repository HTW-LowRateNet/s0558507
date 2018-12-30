import serial
import io
import time
import random
import Client as client
import Message
from _thread import start_new_thread

ser = serial.Serial ("/dev/ttyUSB0")
ser.timeout = 0.3
ser.baudrate = 115200
sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))

read = Message.Message("ADDR","0","0","0","0100","ffff","I am Not the captian!")

    #SEND ALIV AS KOORDINATOR STATE
    
def sendAlive(self):
    while self.state == "COOR":
        message = Message.Message("ALIV","0","0","0",self.addr,"ffff","I am the captian!")
        message.send(self.sio,"ffff")
        print("Meesge"+message.getMessage())
        time.sleep(5)
        
def sendAddr(self):
    while self.state == "COOR":
        message = Message.Message("ALIV","0","0","0",self.addr,"ffff","I am the captian!")
        message.send(self.sio,"ffff")
        print("Meesge"+message.getMessage())
        
test = client.Client("NEW",ser,"",[])
#test.config()
i= 3
while i>=0:
    test.adrDiscovery(read,i)
    print("not yet a captain but now?")
    if test.state != "NEW":
        break
    i=i-1
 
 
def loop():
    while 1:
        #test.sendAlive()
        #test.sendCoordinatorDisc()
        test.sendAddrRequest()
    
start_new_thread(loop(),())