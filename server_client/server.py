import socket
import threading
import time

svrSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Server = '131.179.59.175'
Server = socket.gethostname()
print Server
Port = 567 
svrSoc.bind((Server, Port))
svrSoc.listen(5)
MAC_list = []
devLoc_list = []

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
    clntSoc.send("You are connected\n")
    
    #receive MAC addr and current location
    clntMAC = clntSoc.recv(1024)
    devLoc = clntSoc.recv(1024)
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

    print len(devLoc_list)

    #print current connected devices
    print 'Current Connected Devices:'
    print MAC_list
    print devLoc_list

    #update device location
    
    print 'Device ', clntMAC, 'near ', devLoc
    #print clntSoc.recv(1024)
    clntSoc.close()

def main():
  srvSocThrd = threading.Thread(name='srvSocThrd', target=ServerSoc)
  srvSocThrd.start()
  #testThrd = threading.Thread(name='test', target=test)
  #testThrd.start()

main()
