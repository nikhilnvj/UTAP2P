import threading
from p2p.framework.P2PPeer import *

NAMEPEER=bytes("NAME","UTF8")
SHOWPEERS=bytes("DISP","UTF8")
ADDPEER=bytes("ADDP","UTF8")
SEARCH=bytes("QUER","UTF8")
RESPONSE=bytes("RESP","UTF8")
GETFILE=bytes("GETF","UTF8")
LEAVE=bytes("QUIT","UTF8")
REPLY=bytes("REPL","UTF8")
ERROR=bytes("ERRO","UTF8")

class P2PMessageHandler(P2PPeer):
    def __init__(self,maxKnownPeers,listenPort,hostName):
        P2PPeer.__init__(self, maxKnownPeers,listenPort,hostName=hostName)
        self.files={}
        self.addRouter(self.__router)
        print('Initializing handlers.')
        handlers={SHOWPEERS:self.handleShowPeers,
                  ADDPEER:self.handleAddPeer,
                  SEARCH:self.handleSearchQuery,
                  NAMEPEER:self.handleNamePeer,
                  RESPONSE:self.handleResponse,
                  GETFILE:self.handleGetFile,
                  LEAVE:self.handleLeave
                  }
        for messageType in handlers:
            self.addP2PMessageHandler(messageType,handlers[messageType])
    
    def handleAddPeer(self,p2pPeer,messageData):
        self.peerLock.acquire()
        try:
            peerId,hostName,port=messageData.split()
            if peerId not in self.getPeerIds:
                self.addPeer(peerId,hostName,port)
                p2pPeer.sendData(REPLY,'ADDP: Peer %s added' %peerId)
            else:
                p2pPeer.sendData(ERROR,'ADDP: Peer %s already added' %peerId)
        finally:
            self.peerLock.release()
    
    def handleShowPeers(self,p2pPeer,messageData):
        self.peerLock.acquire()
        try:
            p2pPeer.sendData(REPLY,'%d' %self.totalPeers)
            for peerId in self.getPeerIds:
                hostName,port=self.getPeer(peerId)
                p2pPeer.sendData(REPLY,'%s %s %d' %(peerId,hostName,int(port)))  
        finally:
            self.peerLock.release()
            
    def handleNamePeer(self,p2pPeer,messageData):
        p2pPeer.sendData(REPLY,self.hostId)
        
    def handleSearchQuery(self,p2pPeer,messageData):
        try:
            peerId,fileName,searchDepth=messageData.split()
            p2pPeer.sendData(REPLY,'ACK: %s',fileName)
        except:
            p2pPeer.sendData(ERROR,"Invalid search parameters")
        
        processSearchQueryThread= threading.Thread(target=self.processSearchQuery,args=[peerId,fileName,int(searchDepth)])
        processSearchQueryThread.start()
    
    def processSearchQuery(self,hostId,fileName,searchDepth):
        for file in self.files.keys():
            if fileName in file:
                filePeerId=self.files[fileName]
                if not filePeerId:
                    filePeerId=self.hostId
                hostName,port=hostId.split(':')
                self.connectAndSend(hostName,int(port),RESPONSE,'%s %s' %(file,filePeerId),peerId=hostId)
                return
        if searchDepth > 0:
            messageData='%s %s %s' %(hostId,fileName,int(searchDepth)-1)
            for nextPeerId in self.getPeerIds:
                self.sendMessageToPeer(nextPeerId,SEARCH,messageData)
                
    def handleResponse(self,p2pPeer,messageData):
        try:
            fileName,fileHostId=messageData.split()
            self.files[fileName]=fileHostId
        except:
            print('Error in handling response')
    
    def handleGetFile(self,p2pPeer,messageData):
        fileName=messageData
        if fileName not in self.files:
            p2pPeer.sendData(ERROR,'File %s not found' %fileName)
            return
        try:
            fileDescriptor=open(fileName,'r')
            fileData=''
            while True:
                data=fileDescriptor.read(2048)
                if not len(fileData):
                    break;
            fileData+=data
            fileDescriptor.close()
        except:
            p2pPeer.sendData(ERROR,'Error reading file')
            return
        p2pPeer.sendData(REPLY,fileData)     
        
    def handleLeave(self,p2pPeer,messageData):
        self.peerlock.acquire()
        try:
            hostId=messageData.lstrip().rstrip()
            if hostId in self.getPeerIds:
                p2pPeer.sendData(REPLY,'QUIT: peer %s removed' %hostId)
                self.deletePeer(hostId)
            else:
                p2pPeer.sendData(ERROR,'QUIT: peer not found' %hostId)
        finally:
            self.peerlock.release()
            
    def __router(self,hostId):
        if hostId not in self.getPeerIds:
            return(None,None,None)
        else:
            router=[hostId]
            router.extend(self.knownPeers[hostId])
            
    def addFile(self,fileName):
        self.files[fileName]=None
        
    def buildPeerList(self,hostName,port,ttl=1):
        hostId=None
        try:
            _,hostId=self.connectAndSend(hostName,port,NAMEPEER,bytes("","UTF8"),peerId=hostId)[0]
                
            response=self.connectAndSend(hostName,port,ADDPEER,'%s %s %d' %(self.hostId,self.hostName,self.listenPort))[0]
            
            if (response[0]!=REPLY) or (hostId in self.getPeerIds()):
                return
            self.addPeer(hostId,hostName,port)
            
            response=self.connectAndSend(hostName,port,SHOWPEERS,'',peerId=hostId)
            
            if len(response) >1 :
                response.reverse()
                response.pop()
            while len(response):
                nextPeerId,hostName,port = response.pop()[1].split()
                if nextPeerId != self.hostId:
                    self.buildpeerList(hostName, port, ttl - 1)
        except:
            self.deletePeer(hostId)    