import socket
import threading
import time
import sys
import MySQLdb as db

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

loc_db = db.connect(host="localhost", user="root", passwd="xjy920802")
print "Connected to database successfully."

cursor = loc_db.cursor()

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

    #print current connected devices
    print 'Current Connected Devices:'
    print MAC_list
    print 'device location history:'
    print devLoc_list


    #print 'Device ', clntMAC, 'near ', devLoc
    #print clntSoc.recv(1024)
    print '=================================='

    #update database
    cursor.execute("use loc_list;")
    #cursor.execute("show tables;")
    print str(devLoc), str(clntMAC)
    cursor.execute("""INSERT INTO loc_list VALUES (%s, %s);""", (str(clntMAC), str(devLoc)))
    loc_db.commit()
    cursor.execute("""select * from loc_list;""")
    tables = cursor.fetchall()
    print tables


def main():
  srvSocThrd = threading.Thread(name='srvSocThrd', target=ServerSoc)
  srvSocThrd.start()
  #testThrd = threading.Thread(name='test', target=test)
  #testThrd.start()
  
main()
