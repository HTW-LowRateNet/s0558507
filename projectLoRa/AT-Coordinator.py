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

read = Message.Message("ADDR","0","0","0","0100","ffff","I Not am the captian!")

    #SEND ALIV AS KOORDINATOR STATE
    
def sendAlive(self):
    while self.state == "KOOR":
        message = Message.Message("ALIV","0","0","0",self.addr,"ffff","I am the captian!")
        message.send(self.sio,"ffff")
        print(message.messageSize())
            
test = client.Client("NEW",ser,"",[])
test.config()
i= 3
while i>=0:
    test.adrDiscovery(read,i)
    print("not jet a captain but now?")
    if test.state != "NEW":
        break
    i=i-1
       
test.sendAlive()