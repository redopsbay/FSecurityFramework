#!/usr/bin/python3

import sys
import os
import shutil
import json
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

netdiscover = """ netdiscover -i wlp1s0"""

class NetDiscover(QWidget):
    def __init__(self,parent=None):
        super(NetDiscover,self).__init__(parent)

    def setupUi(self, Main):
        self.resize(917,512)
        self.process = QtCore.QProcess(self)
        self.netdiscovery = QWidget(Main)
        self.netdiscovery.setGeometry(QtCore.QRect(0,0, 917,512))
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.netdiscovery)
        self.setGeometry(QtCore.QRect(0,0, 917,512))           
        self.setStatusTip("Network Discovery and Device Discovery")
        self.netdiscovery.setStatusTip("Network Discovery")
        
    def startTask(self):
        if os.getuid() != 0:
            messagebox = QMessagebox()
            messagebox.setText("Network Discovery requires root access privilege!")
            messagebox.setWindowTitle("Critical ERROR!")
            self.process.start('xterm',['-into',str(int(self.netdiscovery.winId())),'-geometry','980x5000','-e',netdiscover])
        else:
            self.process.start('xterm',['-into',str(int(self.netdiscovery.winId())),'-geometry','980x5000','-e',netdiscover])
if __name__ == "__main__":
     app = QApplication(sys.argv)
     main = Metasploit()
     main.show()
     sys.exit(app.exec_())
