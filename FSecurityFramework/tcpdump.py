#!/usr/bin/python3

import sys
import shutil
import json
import threading
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

tcpdumper = """ tcpdump -vv"""

class TcpDump(QWidget):
    def __init__(self,parent=None):
        super(TcpDump,self).__init__(parent)

    def setupUi(self, Main):
        self.resize(917,512)
        self.process = QtCore.QProcess(self)
        self.tcpdump = QWidget(Main)
        self.tcpdump.setGeometry(QtCore.QRect(0,0, 917,512))
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tcpdump)
        self.setGeometry(QtCore.QRect(0,0, 917,512))           
        self.setStatusTip("Capture Live Packets")
        self.tcpdump.setStatusTip("Capture Live Packets")

    def startTask(self):
        if os.getuid() != 0:
            messagebox = QMessageBox()
            messagebox.setText("Capturing live packets requires root access privilege!")
            messagebox.setWindowTitle("Critical ERROR!")
            self.process.start('xterm',['-into',str(int(self.tcpdump.winId())),'-geometry','980x5000','-e',tcpdumper])
        else:
            self.process.start('xterm',['-into',str(int(self.tcpdump.winId())),'-geometry','980x5000','-e',tcpdumper])
    
if __name__ == "__main__":
     app = QApplication(sys.argv)
     main = Metasploit()
     main.show()
     sys.exit(app.exec_())