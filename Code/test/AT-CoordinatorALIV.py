import serial
import io
import time
import random
import Client as client
import Message
from _thread import start_new_thread

ser = serial.Serial ("/dev/ttyUSB0")
ser.timeout = 0.9
ser.baudrate = 115200
sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))

#SEND ALIV AS KOORDINATOR STATE
def sendAlive(self):
    while self.state == "COOR":
        message = Message.Message("ALIV","0","0","0",self.addr,"ffff","I am the captian!")
        message.send(self.sio,"ffff")
        print("Meesge"+message.getMessage())
        time.sleep(5)
        
           
test = client.Client("COOR",ser,"",[])
test.config()
test.setAddrModul("0000")
 
def loop():
    while 1:
        if ser.inWaiting():
            read = sio.readline()
            #if read != "":
            print(read)
        test.sendAlive()
        #test.sendCoordinatorDisc()
        #test.sendAddrRequest()
    
start_new_thread(loop(),())