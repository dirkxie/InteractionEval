#import
import socket
import sys
import MySQLdb as db

#define socket
svrSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server = socket.gethostname()
Port = 567

#blind socket
svrSoc.bind((Server, Port))
svrSoc.listen(5)

#server socket function
def ServerSoc():
  while True:
    clntSoc, address = svrSoc.accept()
    print "WE GOT CONNECTION FROM ", address
    clntSoc.send('You are connected to server.')
    recv_str = clntSoc.recv(5)
    print recv_str

def main():
    ServerSoc()

main()
