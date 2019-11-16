#!/usr/bin/python3

from Ui import Ui_GetInterfaceDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from Core import CoreLoadConfig
from Core import CoreException
import MainWindow
import pathlib
import socket
import getpass
import subprocess
import os
import sys

class Main(QDialog, Ui_GetInterfaceDialog.Ui_GetInterface_Dialog):
	def __init__(self,parent=None):
		super(Main, self).__init__(parent)
		self.setupUi(self)
		self.accepted.connect(self.ShowMain)
		self.rejected.connect(self.rejectNow)
		self.main = None
		self.interface = None
		self.messagebox = QMessageBox()
		
		if os.getuid() != 0:
			self.messagebox.setText("Critical Error: You must run the program as root user!")
			self.messagebox.setWindowTitle("Error")
			self.messagebox.exec()
			sys.exit(-1)

	def ShowMain(self):
		self.interface = str(self.lineEdit.text())
		if self.interface == "" or self.interface == None:
			self.interface = "lo"
			messagebox = QMessageBox()
			messagebox.setText("You did not specify the interface. So the local interface will be use!")
			messagebox.setWindowTitle("Note")
			messagebox.exec()
			self.main = MainWindow.MainWindow(network_interface=self.interface)
		else:
			messagebox = QMessageBox()
			messagebox.setText("Happy Hacking %s!" % getpass.getuser())
			messagebox.setWindowTitle("Welcome")
			messagebox.exec()
			self.main = MainWindow.MainWindow(network_interface=self.interface)
		self.main.ConnectToDB()
		self.main.show()

	def rejectNow(self):
		sys.exit(1)

if __name__ == '__main__':
	App = QApplication(sys.argv)
	main = Main()
	main.show()
	App.exec_()