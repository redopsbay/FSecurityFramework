#!/usr/bin/python3

import sys
import shutil
import json
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

harvest = """ python3 theharvester.py -d {HOST} -l {LIMIT} -b google -f {RESULT} """

class EmailHarvester(QWidget):
    def __init__(self,parent=None):
        super(EmailHarvester,self).__init__(parent)

    def setupUi(self, Main):
        self.resize(917,512)
        self.process = QtCore.QProcess(self)
        self.harvester = QWidget(Main)
        self.harvester.setGeometry(QtCore.QRect(0,0, 917,512))
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.harvester)
        self.setGeometry(QtCore.QRect(0,0, 917,512))
        self.setStatusTip("Email Harvester")
        self.harvester.setStatusTip("Email Harvester")
        
    def startTask(self,dictionary):
        self.process.start('xterm',['-into',str(int(self.harvester.winId())),'-geometry','980x5000','-e',harvest.format_map(dictionary)])
        QApplication.processEvents()

if __name__ == "__main__":
     app = QApplication(sys.argv)
     main = Metasploit()
     main.show()
     sys.exit(app.exec_())
