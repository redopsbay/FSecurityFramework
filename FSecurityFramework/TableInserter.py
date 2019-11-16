#!/usr/bin/python3

import os
import pathlib
import threading
import shutil
import base64
import json
from Core import CoreException
from Core import CoreLoadConfig
from Db import DBManipulator
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import Qt

class QueryManager:

    def __init__(self, LogBrowser=None,sql_query=None):
        self.LogBrowser = LogBrowser
        self.inserted_items = None
        self.sql_queries = sql_query
        self.insertion_type = None
    
    def QueueItems(self,queuing_type=None,Table_Object=None):
        """
            @Description: Inserts the queried items from MySQL Database. The Type of insertion may differ from
                          insertion_type value.        
        """
        if queuing_type == None:
            if self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Parameter (insertion_type) should be inserted")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Parameter (insertion_type) should be inserted", self.LogBrowser)
            return False

        if Table_Object == None or Table_Object is None:
            if self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Parameter (Table_Object) should not be None value")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Parameter (Table_Object) should not be None Value", self.LogBrowser)
            return False
        
        if self.sql_queries.getDBConnectionStatus() == True:
            if queuing_type == "exploit":
                item_counter = 0
                row_count = self.sql_queries.getTotalExploitCount()
                Table_Object.setRowCount(row_count)
                for iterlist in self.sql_queries.getExploitQuery():
                    if iterlist is None or iterlist == None or iterlist == "" :
                        break
                    cols = 0
                    for values in iterlist:
                        Table_Object.setItem(item_counter, cols, QTableWidgetItem(str(values)))
                        if self.LogBrowser == None:
                            CoreLoadConfig.ConfigHandler.AccessWriteLogger("Value inserted: %s" % values)
                        else:
                            CoreLoadConfig.ConfigHandler.AccessWriteLogger("Value inserted: %s" % values, self.LogBrowser)
                            cols += 1
                    item_counter += 1
            
            if queuing_type == "malware":
                item_counter = 0
                row_count = self.sql_queries.getTotalMalwareCount()
                Table_Object.setRowCount(row_count)
                for iterlist in self.sql_queries.getMalwareQuery():
                    if iterlist is None or iterlist == None or iterlist == "":
                        break
                    cols = 0
                    for values in iterlist:
                        Table_Object.setItem(item_counter, cols, QTableWidgetItem(str(values)))
                        if self.LogBrowser == None:
                            CoreLoadConfig.ConfigHandler.AccessWriteLogger("Value inserted: %s" % values)
                        else:
                            CoreLoadConfig.ConfigHandler.AccessWriteLogger("Value inserted: %s" % values, self.LogBrowser)
                            cols += 1
                    item_counter += 1

            if queuing_type == "cve":
                item_counter = 0
                row_count = self.sql_queries.getTotalCVECount()
                Table_Object.setRowCount(row_count)
                for iterlist in self.sql_queries.getCVEQuery():
                    if iterlist is None or iterlist == None or iterlist == "" :
                        break
                    cols = 0
                    for values in iterlist:
                        Table_Object.setItem(item_counter, cols, QTableWidgetItem(str(values)))
                        if self.LogBrowser == None:
                            CoreLoadConfig.ConfigHandler.AccessWriteLogger("Value inserted: %s" % values)
                        else:
                            CoreLoadConfig.ConfigHandler.AccessWriteLogger("Value inserted: %s" % values, self.LogBrowser)
                            cols += 1
                    item_counter += 1