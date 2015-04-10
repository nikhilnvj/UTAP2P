import socket
import struct
class P2PCoreFramework:
    def __init__(self,peerId,peerHostName,peerPort,clientSocket=None):
        self.peerId=peerId
        if not clientSocket:
            self.clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.clientSocket.connect((peerHostName,int(peerPort)))
        else:
            self.clientSocket=clientSocket
        self.socketDescriptor=self.clientSocket.makefile('rw',0)

    def receiveData(self):
        try:
            messageLength = int(struct.unpack("!L4s%ds", self.socketDescriptor.read(4))[0])
            messageType=self.socketDescriptor.read(4)
            if not messageType:
                return (None,None)
            peerMessage=""
            
            while len(peerMessage) != messageLength:
                socketDataBytes=self.socketDescriptor.read(min(2048,messageLength-len(peerMessage)))
                if not len(socketDataBytes):
                    break;
                peerMessage+=socketDataBytes;
            if len(peerMessage)!=messageLength:
                return(None,None)
        except KeyboardInterrupt:
            raise
        except:
            return (None,None)
        return (messageType,peerMessage)
            
    def sendData(self,messageType,messageData):
        try:
            message=self.packMessageForSending(messageType, messageData)
            self.socketDescriptor.write(message)
            self.socketDescriptor.flush()
        except KeyboardInterrupt:
            raise
        except:
            return False
        return True
    
    def packMessageForSending(self,messageType,messageData):
        messageLength=len(messageData)
        message=struct.pack("!L4s%ds" % messageLength, messageLength, messageType, messageData)
        return message
    
    def close(self):
        self.clientSocket.close();
        self.clientSocket=None
        self.socketDescriptor=None
        
    def __str__(self):
        return "|%clientSocket|" % self.peerId