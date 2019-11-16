#!/usr/bin/python3

import threading
import json
import sys
import os
import shutil
from time import ctime, time
import queue
import multiprocessing
from Core import CoreLoadConfig
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidgetItem
from Ui import Ui_AttackOptionDialog

class AttackOptionDialog(QDialog,Ui_AttackOptionDialog.Ui_AttackOptionDialog):
	def __init__(self, parent=None,LogBrowser=None):
			super(AttackOptionDialog,self).__init__(parent)
			self.LogBrowser = LogBrowser
			self.setupUi(self)
			self.option = []
			self.dictionary =  { }

	def getTable(self):
		return self.tableWidget

	def getRowCount(self):
		return self.rowCount()

	def getColCount(self):
		return self.columnCount()

	def addParam(self,dictionary=None):
		if dictionary == None:
			messagebox = QMessageBox()
			messagebox.setText("Dictionary option is not specified!")
			messagebox.setWindowTitle("ERROR!")
			messagebox.exec()
			return False
		try:
			with open(dictionary, 'r') as file:
				dictionary_option = json.load(file)
		except FileNotFoundError as FnE:
			print("[!] File not found Error!")
			messageBox = QMessageBox()
			messageBox.setWindowTitle("Exception: File Not Found!")
			messageBox.setText("Exception: File Not Found!")
			messageBox.exec()
	#	finally:
	#		continue
		try:
			if type(dictionary_option) != dict:
				messagebox = QMessageBox()
				messagebox.setText("Dictionary option is not specified!")
				messagebox.setWindowTitle("ERROR!")
				messagebox.exec()
				return False
				
		except UnboundLocalError as ULError:
			print("[!] Unbound Local Error")
			messageBox = QMessageBox()
			messageBox.setWindowTitle("Error found!")
			messageBox.setText("Exception: Not Continuing")
			messageBox.exec()
			dictionary_option = None

		if dictionary_option is None or dictionary_option == None:
			return None
		else:
			row_counter = len(dictionary_option)
			self.Option_Table_Widget.setRowCount(row_counter)
			counter = 0
			print(dictionary_option)
			for key, value in dictionary_option.items():
				if key is None and value is None:
					return False
				self.option.append((str(key),str(value)))
				print(dictionary_option)
				self.Option_Table_Widget.setItem(counter, 0, QTableWidgetItem(str(self.option[counter][0])))
				self.Option_Table_Widget.setItem(counter, 1, QTableWidgetItem(str(self.option[counter][1])))
				if self.LogBrowser == None:
					CoreLoadConfig.ConfigHandler.AccessWriteLogger("Required option parameter: %s" % key)
				else:
					CoreLoadConfig.ConfigHandler.AccessWriteLogger("Required value: %s" % value, self.LogBrowser)
				counter += 1
			self.option = []
			self.show()

	def getParseParameters(self):
		row_counter = self.Option_Table_Widget.rowCount()
		counter = 0
		self.dictionary = { }
		row_counter = row_counter
		while counter != row_counter:
			self.dictionary[str(self.Option_Table_Widget.item(counter,0).text())] = str(self.Option_Table_Widget.item(counter,1).text())
			counter += 1
			print("Updated Values: ", self.dictionary)
		return self.dictionary