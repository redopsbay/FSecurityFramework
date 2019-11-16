#!/usr/bin/python3

import sys
import shutil
import json
import mysql.connector
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Terminal(QWidget):
    def __init__(self,parent=None):
        super(Terminal,self).__init__(parent)

    def setupUi(self, Main):
        self.resize(917,512)
        self.process = QtCore.QProcess(self)
        self.terminal = QWidget(Main)
        self.terminal.setGeometry(QtCore.QRect(0,0, 917,512))
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.terminal)
        self.setGeometry(QtCore.QRect(0,0, 917,512))           
        self.setStatusTip("Embedded Terminal")
        self.terminal.setStatusTip("Embedded Terminal")

    def startTask(self):
        self.process.start('xterm',['-into',str(int(self.terminal.winId())),'-geometry','980x5000'])
        
if __name__ == "__main__":
     app = QApplication(sys.argv)
     main = embeddedTerminal()
     main.show()
     sys.exit(app.exec_())
