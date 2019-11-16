#!/usr/bin/python3

import os
import shutil
import json
import nmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui import Ui_attackBrowser 

class AttackBrowser(QWidget,Ui_attackBrowser.Ui_AttackBrowser):
	def __init__(self,parent=None):
		super(AttackBrowser, self).__init__(parent)
		
	def setup(self,parent):
		self.setupUi(parent)
		
	def getBrowser(self):
		return self.textBrowser

	def getLineEdit(self):
		return self.lineEdit

