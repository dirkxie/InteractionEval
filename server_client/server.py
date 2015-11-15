import socket
import threading
import time
import sys

svrSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Server = '131.179.59.175'
Server = socket.gethostname()
print Server
Port = 567 
sendDesPort = 9999

svrSoc.bind((Server, Port))
svrSoc.listen(10)
MAC_list = []
devLoc_list = []
clnt_IP = '169.232.86.161'

#def test():
#  while True:
#    print 'test'
#    time.sleep(2)

def ServerSoc():
  print threading.currentThread().getName(), 'Starting'
  
  while True:
    clntSoc,address = svrSoc.accept()
    print "WE GOT CONNECTION FROM " , address
   
    #echo back to device
    clntSoc.send('You are connected to server.')
    
    #receive MAC addr and current location
    clntMAC = clntSoc.recv(100)
    devLoc = clntSoc.recv(100)
    clntSoc.send('Location received by server.')
    opCode = clntSoc.recv(100)
    
    #if (opCode == 'reqDes'):
    print 'opCode = ', opCode
   
    #send destination to client
    clntSoc.send('1')
    clntSoc.send('18')

    clntSoc.close()
    
    print 'Device from: ', address, ', MAC address: ', clntMAC
    print 'Device current location: ', devLoc, '\n'

    #store MAC addr into MAC_list
    MAC_flag = 0
    MACIdx = 0
    for i in range(len(MAC_list)):
      if (MAC_list[i] == clntMAC):
        MAC_flag = 1
        MACIdx = i
        break

    if (MAC_flag == 0):
      MAC_list.append(clntMAC)
      devLoc_list.append([])
      devLoc_list[len(devLoc_list)-1].append(devLoc)
    elif (devLoc != ''):
      devLoc_list[MACIdx].append(devLoc)

    #print len(devLoc_list)

    #print current connected devices
    print 'Current Connected Devices:'
    print MAC_list
    print 'device location history:'
    print devLoc_list

    #update device location
    
    #print 'Device ', clntMAC, 'near ', devLoc
    #print clntSoc.recv(1024)
    print '=================================='

def main():
  srvSocThrd = threading.Thread(name='srvSocThrd', target=ServerSoc)
  srvSocThrd.start()
  #testThrd = threading.Thread(name='test', target=test)
  #testThrd.start()
  
  '''
  sendDesSoc = socket.socket()
  
  connectSuccess = 0
  while connectSuccess == 0:
    connectFlag = 0

    while True:
    try:
      sendDesSoc.connect((clnt_IP, sendDesPort))
    except Exception:
      print 'failed to connect client'
      connectFlag = 1
      sys.exc_clear()
      time.sleep(2)
    
    if (connectFlag == 0):
      print 'sucessfully connect client, sending destination'
      connectSuccess = 1
      sendDesSoc.send('25')
      sendDesSoc.send('12')
      sendDesSoc.close()
  '''
main()
