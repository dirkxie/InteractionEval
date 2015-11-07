import time
import socket
import sys
from uuid import getnode as get_mac
import threading
import inquiry_with_rssi as BTinq
from route import mapGen
from route import actualDir

def RSSI_scan():
    print 'RSSI scan Started, ~10 sec time interval \n'

    while True:
        result = BTinq.device_inquiry_with_with_rssi(BTsock)
        print 'RSSI scanning result:'
        print result
        nearest = 0
        
        for i in range(len(result)):
            if (result[i][1] > result[nearest][1]):
                nearest = i
        
        if (len(result)!=0):
            currentLoc = result[nearest][0]
            print 'current at location: ', result[nearest][0], 'within: ', result[nearest][2], ' meters\n'
            
            #upload current location    
            s = socket.socket()
            s.connect((server, port))
            
            welcome = s.recv(100)
            print welcome

            ##send MAC addr to server
            s.send(str(mac))
            opCode = 'reqDes'
            s.send(str(currentLoc))
            echoback = s.recv(100)
            print echoback
            s.send(opCode)
            
            #if (opCode == 'reqDes'):
            print 'x_des =', s.recv(1024)
            print 'y_des =', s.recv(1024)
            s.close()
         
        time.sleep(3)

def waitSvr():
    while True:
        print 'waiting for server'
        svrSoc, svrAddr = waitSoc.accept()       
        print "Incoming connect: ", svrAddr
        x_des = svrSoc.recv(100)
        y_des = svrSoc.recv(100)
        print 'x_des = ', x_des, 'y_des = ', y_des
        svrSoc.close()

def main():
    print 'generating demo map'
    mapTemp = [['#' for i in range (width)] for j in range(length)] 
    mapGen(mapTemp)
    print mapTemp

    #get MAC address of this device
    print 'MAC address of this device is ', mac
    
    #create client socket
    s = socket.socket()
    s.connect((server, port))

    ##send MAC addr to server
    s.send(str(mac))
    print s.recv(1024)

    s.send(str(currentLoc))
    s.close()
   
    #waitSvrThrd = threading.Thread(name='waitSvrThrd', target=waitSvr)
    RSSIThrd = threading.Thread(name='RSSIThrd', target=RSSI_scan)
    
    #waitSvrThrd.start()
    RSSIThrd.start()
    

mac = get_mac()
server = '169.232.87.241'
port = 567
result = []
currentLoc = ''

width = 20
length = 20
#print start info
print 'Welcome to use our system'
print 'Initializing client socket'
waitSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
waitSocName = socket.gethostname()
print 'client socket name: ', waitSocName
waitSocPort = 9999
waitSoc.bind(('169.232.86.92', waitSocPort))
waitSoc.listen(5)


#initialize bluetooth
print 'initializing Bluetooth'
BTsock = BTinq.bluetooth_init()

main()
