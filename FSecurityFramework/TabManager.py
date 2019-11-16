#!/usr/bin/python3

import os
import shutil
import threading
import base64
import hashlib
import requests
from Core import CoreException
from Core.CoreLoadConfig import ConfigHandler
from Db import DBManipulator
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import Qt, QtCore, QtGui, QtWidgets

class SingletonType(type):
    def __call__(cls):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType,cls).__call__()
            return cls.__instance

class TabAdder(metaclass=SingletonType):
    def __init__(self):
    	pass
    @classmethod
    def AddTab(cls,Tab_Object=None, Title_Page=None, x=917, y=512,parent=None,LogBrowser=None):
        Tab_Object.addTab(parent,"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/icons/FSecurity.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Tab_Object.setTabText(Tab_Object.indexOf(parent),Title_Page)
        Tab_Object.setTabIcon(Tab_Object.indexOf(parent),icon)
        if LogBrowser == None:
        	ConfigHandler.AccessWriteLogger("Tab Created: %s" % Title_Page)
        else:
        	ConfigHandler.AccessWriteLogger("Tab Created: %s" % Title_Page, LogBrowser)