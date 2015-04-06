#!/usr/bin/python
import threading
import socket
from p2pconnection import P2PConnection
class P2PPeer:
    
    def __init__(self,maxKnownPeers,listenPort,hostId=None,hostname=None):
        
        self.maxKnownPeers= int(maxKnownPeers)
        self.listenPort=int(listenPort)
        if hostname:
            self.hostName=hostname
        else:
            self.__initHostName()
        
        if hostId: 
            self.hostId=hostId
        else:
            self.hostId= '%s:%d' %(self.hostName,self.listenPort)
        
        self.peerLock=threading.Lock()
        self.knownPeers={}
        self.breakLoop=False
        self.handlers={}
    
    def __initHostName(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("www.google.com",80))
        self.hostName=s.getsockname()[0]
        s.close();
    
    def __handlePeer(self,clientSocket):
        hostName,port=clientSocket.getpeername()
        p2pConnection=P2PConnection(None,hostName,port,clientSocket)
        
        try:
            messageType,messageData=p2pConnection.receiveData()
            if messageType:
                messageType=messageType.upper()
            if messageType not in self.handlers:
                print('Error')
            else:
                self.handlers[messageType](p2pConnection,messageData)
        except KeyboardInterrupt:
            raise
        except:
            print('Error')
        p2pConnection.close();
    
    def addHandler(self,messageType,handler):
        self.handlers[messageType]=handler;

    def addRouter(self,router):
        self.router=router
    
    def addPeer(self,peerId,hostName,port):
        if peerId not in self.knownPeers:
            self.knownPeers[peerId]=(hostName,int(port))
            
    def getPeer(self,peerId):
        return self.knownPeers[peerId]
    
    def deletePeer(self,peerId):
        if peerId in self.knownPeers:
            del self.knownPeers[peerId]
    
    def getPeerIds(self):
        return self.knownPeers.keys()
    
    def totalPeers(self):
        return len(self.knownPeers)
    
    def prepareServerSocket(self,port,maxConnnections=5):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind(('',port))
        s.listen(maxConnnections)
        return s;
    
    def sendMessageeToPeer(self,peerId,messageType,messageData,waitReply=True):
        if self.router:
            nextPeerId,hostName,port=self.router(peerId)
        if not self.router or not nextPeerId:
            return None
        return self.connectAndSend(hostName,port,messageType,messageData,peerId=nextPeerId,waitReply=waitReply)
    
    def connectAndSend(self,hostName,port,messageType,messageData,peerId=None,waitReply=True):
        messageReply=[]
        try:
            p2pConnection=P2PConnection(peerId, hostName, port)
            p2pConnection.sendData(messageType,messageData)
            
            if waitReply:
                oneReply=p2pConnection.receiveData()
            while (oneReply != (None,None)):
                messageReply.append(oneReply)
                oneReply=p2pConnection.receiveData()
            p2pConnection.close()
        except KeyboardInterrupt:
            raise
        except:
            print('Error')
        return messageReply
    
    def checkActivePeers(self):
        toRemove=[]
        for peerId in self.peers:
            isConnected=False
            try:
                hostName,port=self.knownPeers[peerId]
                p2pConnection=P2PConnection(peerId, hostName, port)
                p2pConnection.sendData('PING','')
                isConnected=True
            except:
                toRemove.append(peerId)
                if isConnected:
                    p2pConnection.close()
                self.peerLock.acquire()
                try:
                    for peerId in toRemove:
                        if peerId in self.knownPeers:
                            del self.knownPeers[peerId]
                finally:
                    self.peerLock.release()
            
    def mainLoop(self):
        s=self.prepareServerSocket(self.listenPort)
        s.settimeout(2)
        try:
            while not self.breakLoop:
                clientSocket,clientAdress=s.accept()
                clientSocket.settimeout(None)
                peerThread=threading.Thread(target=self.__handlePeer,args=[clientSocket])
                peerThread.start()
        except:
            print('Error')
        s.close()
            
    