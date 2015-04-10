# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI.ui'
#
# Created: Thu Apr  9 15:13:13 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(807, 717)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.btn_Search = QtGui.QPushButton(self.centralwidget)
        self.btn_Search.setGeometry(QtCore.QRect(630, 20, 161, 41))
        self.btn_Search.setObjectName(_fromUtf8("btn_Search"))
        self.tb_Search = QtGui.QLineEdit(self.centralwidget)
        self.tb_Search.setGeometry(QtCore.QRect(12, 20, 611, 41))
        self.tb_Search.setObjectName(_fromUtf8("tb_Search"))
        self.listView_files = QtGui.QListWidget(self.centralwidget)
        self.listView_files.setGeometry(QtCore.QRect(20, 110, 771, 381))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_files.sizePolicy().hasHeightForWidth())
        self.listView_files.setSizePolicy(sizePolicy)
        self.listView_files.setMinimumSize(QtCore.QSize(771, 0))
        self.listView_files.setStyleSheet(_fromUtf8("background-color: rgb(170, 170, 127);\n"
"selection-color: rgb(170, 170, 0);"))
        self.listView_files.setObjectName(_fromUtf8("listView_files"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 80, 261, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.btn_download = QtGui.QPushButton(self.centralwidget)
        self.btn_download.setGeometry(QtCore.QRect(120, 500, 161, 41))
        self.btn_download.setObjectName(_fromUtf8("btn_download"))
        self.btn_addFile = QtGui.QPushButton(self.centralwidget)
        self.btn_addFile.setGeometry(QtCore.QRect(640, 580, 161, 41))
        self.btn_addFile.setObjectName(_fromUtf8("btn_addFile"))
        self.tb_addFile = QtGui.QLineEdit(self.centralwidget)
        self.tb_addFile.setGeometry(QtCore.QRect(10, 580, 611, 41))
        self.tb_addFile.setObjectName(_fromUtf8("tb_addFile"))
        self.btn_download_3 = QtGui.QPushButton(self.centralwidget)
        self.btn_download_3.setGeometry(QtCore.QRect(618, 1140, 161, 41))
        self.btn_download_3.setObjectName(_fromUtf8("btn_download_3"))
        self.btn_refresh = QtGui.QPushButton(self.centralwidget)
        self.btn_refresh.setGeometry(QtCore.QRect(490, 500, 161, 41))
        self.btn_refresh.setObjectName(_fromUtf8("btn_refresh"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 807, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "P2P FileShare", None))
        self.btn_Search.setToolTip(_translate("MainWindow", "Search", None))
        self.btn_Search.setText(_translate("MainWindow", "Search", None))
        self.tb_Search.setToolTip(_translate("MainWindow", "Search for files on the network", None))
        self.label.setText(_translate("MainWindow", "Files available to download:", None))
        self.btn_download.setToolTip(_translate("MainWindow", "Search", None))
        self.btn_download.setText(_translate("MainWindow", "Download Selected File", None))
        self.btn_addFile.setToolTip(_translate("MainWindow", "Search", None))
        self.btn_addFile.setText(_translate("MainWindow", "Add file for sharing", None))
        self.tb_addFile.setToolTip(_translate("MainWindow", "Search for files on the network", None))
        self.btn_download_3.setToolTip(_translate("MainWindow", "Search", None))
        self.btn_download_3.setText(_translate("MainWindow", "Add file for sharing", None))
        self.btn_refresh.setToolTip(_translate("MainWindow", "Search", None))
        self.btn_refresh.setText(_translate("MainWindow", "Refresh File List", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

