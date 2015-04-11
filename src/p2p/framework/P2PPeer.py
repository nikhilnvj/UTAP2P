#!/usr/bin/python
import threading
import socket
import traceback
from p2p.framework.P2PCoreFramework import P2PCoreFramework
class P2PPeer:
    
    def __init__(self,maxKnownPeers,listenPort,hostId=None,hostName=None):
        
        self.maxKnownPeers= int(maxKnownPeers)
        self.listenPort=int(listenPort)
        if hostName:
            self.hostName=hostName
        else:
            self.initHostName()
        
        if hostId: 
            self.hostId=hostId
        else:
            self.hostId= '%s:%d' %(self.hostName,self.listenPort)
        self.listen=True
        self.peerLock=threading.Lock()
        self.knownPeers={}
        self.handlers={}
        self.maxServerConnections=5
    
    def listenForConnections(self):
        print('Preparing to listen for incoming connections.')
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind(('',self.listenPort))
        s.listen(self.maxServerConnections)
        #s.settimeout(2)
        try:
            while self.listen:
                print('Server Started. Listening for incoming connections...')
                clientSocket,clientAdress=s.accept()
                clientSocket.settimeout(None)
                handlePeerThread=threading.Thread(target=self.handlePeer,args=[clientSocket])
                handlePeerThread.start()
        except:
            traceback.print_exc()
        s.close()
    
    def handlePeer(self,clientSocket):
        peerHostName,peerPort=clientSocket.getpeername()
        p2pCoreFramework=P2PCoreFramework(None,peerHostName,peerPort,clientSocket)
        try:
            messageType,messageData=p2pCoreFramework.receiveData()
            if messageType:
                messageType=messageType.upper()
            if messageType not in self.handlers:
                print('No handler was found for the message')
            else:
                self.handlers[messageType](p2pCoreFramework,messageData)
        except KeyboardInterrupt:
            raise
        except:
            print('P2PPeer : Unknown Exception occurred')
        p2pCoreFramework.close();
        
    def initHostName(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("www.google.com",80))
        self.hostName=s.getsockname()[0]
        s.close();
    
    def addP2PMessageHandler(self,messageType,handler):
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
    
    def sendMessageToPeer(self,peerId,messageType,messageData,waitReply=True):
        if self.router:
            nextPeerId,hostName,port=self.router(peerId)
        if not self.router or not nextPeerId:
            return None
        return self.connectAndSend(hostName,port,messageType,messageData,peerId=nextPeerId,waitReply=waitReply)
    
    def connectAndSend(self,hostName,port,messageType,messageData,peerId=None,waitReply=True):
        messageReply=[]
        try:
            p2pPeer=P2PCoreFramework(peerId, hostName, port)
            print('Sending data to the peer.')
            p2pPeer.sendData(messageType,messageData)
            print('Awaiting response from the peer')
            if waitReply:
                oneReply=p2pPeer.receiveData()
            while (oneReply != (None,None)):
                messageReply.append(oneReply)
                oneReply=p2pPeer.receiveData()
            p2pPeer.close()
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()
        return messageReply
    
    def checkActivePeers(self):
        toRemove=[]
        for peerId in self.peers:
            isConnected=False
            try:
                hostName,port=self.knownPeers[peerId]
                p2pConnection=P2PCoreFramework(peerId, hostName, port)
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