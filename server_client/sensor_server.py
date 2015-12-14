import socket
import threading
import time
import sys
import MySQLdb as db

################# client MAC-name pairs ###################
clientMACList = ['277913882730528', '277913881634525', '132265794002535']
clientNameList = ['Dylan', 'Dave', 'Paul']

sensor_db = db.connect(host="localhost", user="root", passwd="xjy920802")
print "Connected to sensor database successfully"
cursor = sensor_db.cursor()

svrSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server = socket.gethostname()

print Server
Port = 567
sendDesPort = 9999

svrSoc.bind((Server, Port))
svrSoc.listen(5)


def ServerSoc():
    print threading.currentThread().getName(), 'Starting'
    
    while True:
      print "=============================================================================="
      clntSoc,address = svrSoc.accept()
      print "WE GOT CONNECTION FROM " , address


      #receive MAC addr and current location
      clntMAC = clntSoc.recv(100)
      print 'device mac:\t', clntMAC
      clntSoc.send('MACRV')

      distance = clntSoc.recv(100)
      print 'distance:\t', distance, ' cm'
      clntSoc.send('DISRV')
      
      heart_rate = clntSoc.recv(100)
      print 'heart rate:\t', heart_rate, ' pulses/s'
      clntSoc.send('HRTRV')

      avgSound = clntSoc.recv(100)
      print 'avgSound:\t', avgSound, ' dB'
      clntSoc.send('SNDRV')

      detectFlag = clntSoc.recv(100)
      print 'face detected:\t', detectFlag
      clntSoc.send('FCDRV')

      posInClientList = findClientInList(clntMAC)
      clientName = clientNameList[posInClientList]
      print 'updating database for client ', clientName     

      cursor.execute("use sensor_data;")
      cursor.execute("""INSERT INTO test_data VALUES (%s, %s, %s, %s, %s);""", (clientName, distance, heart_rate, avgSound, detectFlag))
      sensor_db.commit()

      clntSoc.close()

def findClientInList(clntMAC):
  posInClientList = 0
  for i in range(len(clientMACList)):
    if (clientMACList[i] == clntMAC):
      posInClientList = i
      break
  return posInClientList


def main():
    srvSocThrd = threading.Thread(name='srvSocThrd', target=ServerSoc)
    srvSocThrd.start()
main()
