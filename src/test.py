'''
Created on Apr 6, 2015

@author: Nikhil
'''
import socket
import struct

if __name__ == '__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('www.google.com',80))
    print(s.getpeername())
    x=struct.pack("!4sL2s%d",bytes("Nikh","ASCII"),22,bytes("Nu","ASCII"),2)
    print (x)
    print(struct.unpack("4sL2s", x)[2])
    