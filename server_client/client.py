import time
import socket
import sys
from uuid import getnode as get_mac
import threading
import inquiry_with_rssi as BTinq
from route import mapGen
from route import actualDir
from route import navigate

#############global variables##############################
mac = get_mac()
#server = input ('Please enter the IP address of the server machine, ensure both server and client are in the same network.') 
server = '169.232.87.141'
port = 567
result = []
currentLoc = ''

width = 20
length = 20

mapTemp = [['#' for i in range (width)] for j in range(length)] 

##############store beacon MAC-coordinates pairs############
beaconMAC = ['98:4F:EE:03:35:B6', '98:4F:EE:03:3A:41', '98:4F:EE:04:A1:F3', '6C:83:36:DE:27:BF', 'D4:97:0B:CB:BC:DC']
beaconName = ['Yang', 'Dave', 'Paul', 'Bob', 'Adam']
beaconCo = [[1,18,1], [18,1,0], [18,10,0], [18,18,0], [10,18,0]]
topologyReMappingMap = [1, 2, 3 ,4 ,5 ,6]

##############current and previous coordinates of device####
x_crnt = -1
y_crnt = -1
z_crnt = -1
x_prev = -1
y_prev = -1
z_prev = -1
x_des = -1
y_des = -1
z_des = -1

############## ANSI color ##################################
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#######################

def localize(result, nearest, posInBeaconList):
    global x_crnt, y_crnt, z_crnt, x_prev, y_prev, z_prev
    
    #temp to compare new coordinates with previous
    x_temp = int(x_crnt)
    y_temp = int(y_crnt)
    z_temp = int(z_crnt)
    #print 'temp crnt x,y:', x_temp, y_temp

    #update prev and crnt coordinates
    if (x_crnt == -1):
        x_crnt = beaconCo[posInBeaconList][0]
    if (y_crnt == -1):
        y_crnt = beaconCo[posInBeaconList][1]
    if (z_crnt == -1):
        z_crnt = beaconCo[posInBeaconList][2]
    if (x_prev == -1):
        x_prev = beaconCo[posInBeaconList][0]
    if (y_prev == -1):
        y_prev = beaconCo[posInBeaconList][1]
    if (z_prev == -1):
        z_prev = beaconCo[posInBeaconList][2]

    #if (result[nearest][1] > -50):
    x_crnt = beaconCo[posInBeaconList][0]
    y_crnt = beaconCo[posInBeaconList][1]
    z_crnt = beaconCo[posInBeaconList][2]

    #temp coordinates
    if (x_temp != x_crnt or y_temp != y_crnt or z_temp != z_crnt):
        x_prev = x_temp
        y_prev = y_temp
        z_prev = z_temp

    #print 'x,y_prev:', x_prev, ',', y_prev, 'x,y_crnt:', x_crnt, ',', y_crnt

def RSSI_scan():
    global x_crnt, y_crnt, z_crnt, x_prev, y_prev, z_crnt, x_des, y_des, z_des

    global mapTemp, beaconMAC
    
    print bcolors.OKBLUE + '[PHASE 0] ' + bcolors.ENDC,
    print 'RSSI scan and server upload start: 6~8 sec time interval \n'

    while True:
        result = BTinq.device_inquiry_with_with_rssi(BTsock)
        print bcolors.OKGREEN + '[PHASE 1] ' + bcolors.ENDC, 
        print 'RSSI scan result:\n', result
        
        nearest = 0
        
        for i in range(len(result)):
            for j in range(len(beaconMAC)):
                if (result[i][0] == beaconMAC[j]):
                    if (result[i][1] > result[nearest][1]):
                        nearest = i

        if (len(result) != 0):
            posInBeaconList = 2 
            for i in range(len(beaconMAC)):
                if (beaconMAC[i] == result[nearest][0]):
                    posInBeaconList = i
           
            #print bcolors.WARNING + '[PHASE 1]  nearest beacon: ', beaconName[posInBeaconList] + bcolors.ENDC
            print bcolors.OKGREEN + '[PHASE 1] ' + bcolors.ENDC,
            print 'Nearest beacon: ', bcolors.WARNING + beaconName[posInBeaconList] + bcolors.ENDC, ', within: ', bcolors.WARNING + str(result[nearest][2]), 'meters'+ bcolors.ENDC

            currentLoc = result[nearest][0]
            #print 'current at location: ', result[nearest][0], 'within: ', result[nearest][2], ' meters\n'
            ### server connection ###
            #upload current location    
            s = socket.socket()
            s.connect((server, port))
            
            connectedToSvr = s.recv(100)
            print bcolors.OKGREEN + '[PHASE 2] ' + bcolors.ENDC, connectedToSvr

            ##send MAC addr to server
            s.send(str(mac))
            s.send(str(currentLoc))
            locRcvSvr = s.recv(100)
            print bcolors.OKGREEN + '[PHASE 2] ' + bcolors.ENDC, locRcvSvr          
            opCode = 'reqDes'
            s.send(opCode)
            
            #if (opCode == 'reqDes'):
            x_desR = s.recv(4)
            s.send('dummy1')
            y_desR = s.recv(4)
            s.send('dummy2')
            z_desR = s.recv(4)
            x_des = int(x_desR)
            y_des = int(y_desR)
            z_des = int(z_desR)
            print bcolors.OKGREEN + '[PHASE 3] ' + bcolors.ENDC,
            print 'Destination received from server: ', bcolors.WARNING + x_desR, ',', y_desR, ',', z_desR + bcolors.ENDC
            
            s.close()
            ### server connection ###

            ### localization and navigation ###
            localize (result, nearest, posInBeaconList)
            navigate (x_prev, y_prev, z_prev, x_crnt, y_crnt, z_crnt, x_des, y_des, z_des, mapTemp)
                       
            print '=============================='

        #time.sleep(3)

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
    mapGen(mapTemp)
    print mapTemp

    #get MAC address of this device
    print 'MAC address of this device is ', mac
    
    #create client socket
    s = socket.socket()
    print 'initial ping to server'
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
    

#print start info
print 'Welcome to use our system'
print 'Initializing client socket'
waitSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
waitSocName = socket.gethostname()
print 'client socket name: ', waitSocName
waitSocPort = 9999
#waitSoc.bind(('169.232.86.92', waitSocPort))
#waitSoc.listen(5)


#initialize bluetooth
print 'initializing Bluetooth'
BTsock = BTinq.bluetooth_init()

main()
