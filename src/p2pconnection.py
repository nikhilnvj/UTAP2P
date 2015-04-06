import socket
import struct
class P2PConnection:
    def __init__(self,peerId,hostName,port,clientSocket=None):
        
        self.id=peerId
        
        if not clientSocket:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.s.connect((hostName,int(port)))
        else:
            self.s=clientSocket
        
        self.sd=self.s.makefile('rw',0)
        
    def __makeMessage(self,messageType,messageData):
        messageLength=len(messageData)
        message=struct.pack("!4sL%ds" % messageLength, messageType, messageLength, messageData)
        return message
    
    def sendData(self,messageType,messageData):
        try:
            message=self.__makeMessage(messageType, messageData)
            self.sd.write(message)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        except:
            return False
        return True
    
    def receiveData(self):
        try:
            messageType=self.sd.read(4)
            if not messageType:return (None,None)
            lengthString=self.sd.read(4)
            messageLength = int(struct.unpack("!L", lengthString)[0])
            message=""
            
            while len(message) != messageLength:
                data=self.sd.read(min(2048,messageLength-len(message)))
                if not len(data):
                    break;
                message+=data;
            if len(message)!=messageLength:
                return(None,None)
        except KeyboardInterrupt:
            raise
        except:
            return (None,None)
        return (messageType,message)
    
    def close(self):
        self.s.close();
        self.s=None
        self.sd=None
        
    def __str__(self):
        return "|%s|" % self.id