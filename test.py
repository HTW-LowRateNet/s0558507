import time

'''
timeT = time.time()
print(timeT)
print(time.time)
time.sleep(1)
timeN = time.time() - timeT
print(timeN)
time.sleep(1)
timeN = time.time() - timeT
print(timeN)
'''



newAdress = str(hex(16))
print(hex(16))
addr = newAdress.replace("0x","",1).upper()

print(addr)

cAddrStore = []
cAddrStore.append(255)
cAddrStore.append("HAHAHA")
print(cAddrStore)


nb = []
nb.append("0000")
nb.append("0200")
nb.append("0100")
nb.sort()

test="1111"


for i in nb:
    if i != test: 
        nb.append(test)
        nb.sort()
        break
print(str(nb))