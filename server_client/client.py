import time
import socket
import sys
from uuid import getnode as get_mac
import threading
import inquiry_with_rssi as BTinq

mac = get_mac()
server = '131.179.59.209'
port = 567
result = []
currentLoc = ''

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
            ##send MAC addr to server
            s.send(str(mac))
            s.send(str(currentLoc))
            s.close()
         
        time.sleep(3)

def main():
    
    #get MAC address of this device
    print 'MAC address of this device is ', mac
    
    #create client socket
    s = socket.socket()
    #connect to server
    #connectSuccess = 0
    
    #while connectSuccess == 0:
    #    try:
    #        s.connect((server, port))
    #        connectSucess = 1
    #    except Exception:
    #        reconTime = 2
    #        print 'connect failed, reconnecting in ', reconTime, 'sec' 
    #        time.sleep(1.8)
    #        sys.exc_clear()
    s.connect((server, port))

    ##send MAC addr to server
    s.send(str(mac))

    print s.recv(1024)

    s.send(str(currentLoc))
    s.close()
    
    RSSIThrd = threading.Thread (name='RSSIThrd', target=RSSI_scan)
    RSSIThrd.start()

#print start info
print 'Welcome to use our system'

#initialize bluetooth
print 'initializing Bluetooth'
BTsock = BTinq.bluetooth_init()

main()
