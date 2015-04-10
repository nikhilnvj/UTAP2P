'''
Created on Apr 6, 2015

@author: Nikhil
'''
import socket
import struct

if __name__ == '__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('www.google.co.se',80))
    print('PeerName:' + str(s.getpeername()))
    print('SockName:' +str(s.getsockname()))
    messageLength=10
    messageType=bytes("QUER","utf8")
    messageData=bytes("nikhilnikh","utf8")
    x=struct.pack("!4sL%ds" % messageLength, messageType, messageLength, messageData)
    print (x)
    print(int(struct.unpack("!4sL%ds"%messageLength, x)[1]))
     