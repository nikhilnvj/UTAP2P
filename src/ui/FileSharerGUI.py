import sys
import threading

from PyQt4 import QtCore
from PyQt4.Qt import QMainWindow, QListWidgetItem
from PyQt4.QtGui import QMessageBox

from UI import Ui_MainWindow, QtGui
from p2p.filemanager.P2PMessageHandler import *


class FileSharerGUI(QMainWindow, Ui_MainWindow):
    
    def __init__(self, initialPeer, ttl=2, maxKnownPeers=5, initialPeerPort=1234, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        initialPeerHostName, initialPeerPort = initialPeer.split(':')
        self.peerHandler = P2PMessageHandler(maxKnownPeers, initialPeerPort, initialPeerHostName)
        t = threading.Thread(target=self.peerHandler.listenForConnections, args=[])
        t.start()
        self.peerHandler.buildPeerList(initialPeerHostName, int(initialPeerPort), ttl)
        self.updatePeers()
        QtCore.QObject.connect(self.ui.btn_download, QtCore.SIGNAL('clicked()'), self.onDownloadClicked)
        QtCore.QObject.connect(self.ui.btn_addFile, QtCore.SIGNAL('clicked()'), self.onAddFileClicked)
        QtCore.QObject.connect(self.ui.btn_Search, QtCore.SIGNAL('clicked()'), self.onSearchClicked)
        QtCore.QObject.connect(self.ui.btn_refresh, QtCore.SIGNAL('clicked()'), self.onRefreshClicked)
    
    def updatePeers(self):
        for peerId in self.peerHandler.getPeerIds():
            self.ui.listView_files.addItem(peerId)
    
    def updateFilesList(self):
        for file in self.peerHandler.files:
            fileHost = self.peerHandler.files[file]
            if not fileHost:
                fileHost = ('localhost')
            self.listView_files.addItem("%s:%s:1234" % (file, fileHost))
            self.ui.listView_files.repaint()
    
    def onDownloadClicked(self):
        selections = self.ui.listView_files.selectedItems()
        if selections:
            for s in selections:
                if(len(s.text().split(':')) > 2):
                    fileName, hostName, port = s.text().split(':')
                    response = self.peerHandler.connectAndSend(hostName, port, GETFILE, fileName)
                    if len(response) and response[0][0] == REPLY:
                        fileDescriptor = open(fileName, 'w')
                        fileDescriptor.write(response[0][1])
                        fileDescriptor.close()
                        self.peerHandler.files[fileName] = None
        else:
            self.popupErrorMessage('Please select a file before proceeding.')            
            
    def onAddFileClicked(self):
        fileName = self.ui.tb_Search.text()
        if fileName:
            fileName = fileName.lstrip().rstrip()
            self.peerHandler.files[fileName] = None
            print('File added for sharing')
        else:
            self.popupErrorMessage('Please enter a filename before adding.')
        self.ui.tb_addFile.setText(None)
            
    def onSearchClicked(self):
        searchText = self.ui.tb_Search.text()
        if searchText:
            for peerId in self.peerHandler.getPeerIds():
                self.peerHandler.sendMessageToPeer(peerId, SEARCH, '%s %s 4' % (self.peerHandler.hostId, searchText))
        else:
            self.popupErrorMessage('Please enter some search text.')
    
    def popupErrorMessage(self, errorString):
        messageBox = QMessageBox()
        messageBox.setWindowTitle('Error!!!')
        messageBox.setText(errorString)
        messageBox.exec_()
    
    def onRefreshClicked(self):
        self.updatePeers();
        self.updateFilesList()
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = FileSharerGUI("216.58.209.100:80")
    myapp.ui.listView_files.addItem("Filename:nikhil")
    myapp.show()
    sys.exit(app.exec_())
        
