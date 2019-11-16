#!/usr/bin/python3

import json
import imp
import shutil
import os
import sys
import queue
import multiprocessing
import TabManager
import pprint
import threading
from ThreadHandlers import CoreThread
from Core import CoreLoadConfig
from Core.CoreLoadConfig import ConfigHandler
import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class AttackLauncher:
	def __init__(self,LogBrowser=None):
		self.LogBrowser = LogBrowser
		self.required_attributes = ['run','setupParam','commandlistener']
		self.attack_data = None
		self.config_handler = CoreLoadConfig.ConfigHandler

	def start_attack(self,module_name=None, options=None, commandBrowser=None,TabWidget=None,Title=None):
		if module_name != None and options != None and commandBrowser != None and TabWidget != None and Title != None:
			fp, pathname, description = imp.find_module(module_name.split(".py")[0])
			self.attack_data = options
			imported_module = imp.load_module(pathname,fp,pathname,description)
			try:
				attacker = imported_module.Attack(Browser=commandBrowser,LogBrowser=self.LogBrowser,config_handler=self.config_handler)
			except AttributeError as Aerror:
				messagebox = QMessageBox()
				messagebox.setText("The given modules has no class called Attack(). Make sure your scripts will meet the requirements!")
				messagebox.setWindowTitle("ERROR!")
				messagebox.exec()
				if self.LogBrowser == None:
					CoreLoadConfig.ConfigHandler.ErrorWriteLogger("The parameter is not enough!")
				else:
					CoreLoadConfig.ConfigHandler.ErrorWriteLogger("The parameter is not enough!",self.LogBrowser)
				return False

			for value in self.required_attributes:
				if hasattr(attacker,value):
					TabManager.TabAdder.AddTab(Tab_Object=TabWidget,Title_Page=Title, parent=commandBrowser,LogBrowser=self.LogBrowser)
					attacker.setupParam(data_options=self.attack_data)
					return attacker #return the attacker object
				else:
					messagebox = QMessageBox()
					messagebox.setText("Please modify the attack script and include the required functions and classes!")
					messagebox.setWindowTitle("ERROR!")
					messagebox.exec()
					if self.LogBrowser == None:
						CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Please modify the attack script and include the required functions and classes!")
					else:
						CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Please modify the attack script and include the required functions and classes!",self.LogBrowser)
					return False
		else:
			messagebox = QMessageBox()
			messagebox.setText("The parameter is not enough!")
			messagebox.setWindowTitle("ERROR!")
			messagebox.exec()
			if self.LogBrowser == None:
				CoreLoadConfig.ConfigHandler.ErrorWriteLogger("The parameter is not enough!")
			else:
				CoreLoadConfig.ConfigHandler.ErrorWriteLogger("The parameter is not enough!",self.LogBrowser)
			return False