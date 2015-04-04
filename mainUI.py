# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI.ui'
#
# Created: Sat Apr  4 17:17:46 2015
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
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.btn_Search = QtGui.QPushButton(self.centralwidget)
        self.btn_Search.setGeometry(QtCore.QRect(630, 20, 161, 41))
        self.btn_Search.setObjectName(_fromUtf8("btn_Search"))
        self.tb_Search = QtGui.QLineEdit(self.centralwidget)
        self.tb_Search.setGeometry(QtCore.QRect(12, 20, 611, 41))
        self.tb_Search.setObjectName(_fromUtf8("tb_Search"))
        self.listView_files = QtGui.QListWidget(self.centralwidget)
        self.listView_files.setGeometry(QtCore.QRect(20, 110, 771, 431))
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
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


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

