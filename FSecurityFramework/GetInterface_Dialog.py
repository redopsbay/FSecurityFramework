#!/usr/bin/python3

from Ui import Ui_GetInterfaceDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from Core import CoreLoadConfig
from Core import CoreException
import pathlib
import socket
import sys

class Main(QDialog, Ui_GetInterfaceDialog.Ui_GetInterface_Dialog):
	def __init__(self,parent=None):
		super(Main, self).__init__(parent)
		self.setupUi(self)
		self.accepted.connect(self.ShowMain)
		self.rejected.connect(self.rejectNow)
		self.main = None

	def ShowMain(self):
		interface = str(interface_dialog.lineEdit.text())
		self.main = MainWindow.MainWindow(network_interface=interface)
		self.main.show()

	def rejectNow(self):
		sys.exit(1)

if __name__ == '__main__':
	App = QApplication(sys.argv)
	main = Main()
	main.show()
	App.exec_()