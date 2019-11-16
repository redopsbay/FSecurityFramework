#!/usr/bin/python3

import os
import sys
import shutil
import json
import threading
from Db import DBManipulator
import TabManager
from Ui import Ui_CVETable
from Ui import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets

class CVETable_Widget(QWidget,Ui_CVETable.Ui_CVETable):
	def __init__(self, parent=None,LogBrowser=None):
		super(CVETable_Widget,self).__init__(parent)
		self.LogBrowser = LogBrowser
	