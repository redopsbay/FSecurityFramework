#!/usr/bin/python3

import threading
import json
import sys
import os
import shutil
from Core.CoreLoadConfig import ConfigHandler 
import time
import queue
import multiprocessing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CoreThread(threading.Thread):
	def __init__(self,group=None,target=None, name=None, args=(),kwargs=None,daemon=None,LogBrowser=None,delay=5):
		super(CoreThread,self).__init__(group=group,target=target,name=name ,args=args,kwargs=kwargs,daemon=daemon)
		self.LogBrowser = None
		self.delay = delay

	def run(self):
		time.sleep(self.delay)
		if self.LogBrowser == None:
			ConfigHandler.AccessWriteLogger("Thread starting: %s at %s" % (threading.currentThread().name, time.time()))
		else:
			ConfigHandler.AccessWriteLogger("Thread starting: %s at %s" % (threading.currentThread().name, time.time()),self.LogBrowser)

