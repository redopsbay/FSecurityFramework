#!/usr/bin/python3

import sys
import shutil
import json
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

msfconsole = """ msfconsole """

class Metasploit(QWidget):
    def __init__(self,parent=None):
        super(Metasploit,self).__init__(parent)

    def setupUi(self, Main):
        self.resize(917,512)
        self.process = QtCore.QProcess(self)
        self.metasploit = QWidget(Main)
        self.metasploit.setGeometry(QtCore.QRect(0,0, 917,512))
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.metasploit)
        self.setGeometry(QtCore.QRect(0,0, 917,512))
        self.setStatusTip("Metasploit Framework")
        self.metasploit.setStatusTip("Metasploit Framework")
        
    def startTask(self):
        self.process.start('xterm',['-into',str(int(self.metasploit.winId())),'-geometry','980x5000','-e',msfconsole])

if __name__ == "__main__":
     app = QApplication(sys.argv)
     main = Metasploit()
     main.show()
     sys.exit(app.exec_())