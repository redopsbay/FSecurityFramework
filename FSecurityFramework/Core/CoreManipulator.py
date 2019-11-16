#!/usr/bin/python3

import shutil
import os
import sys
import json
import LoadConfig

try:
    import pymysql
except ImportError as Ie:
    LoadConfig.ConfigHandler.ErrorWriteLogger(Ie)

class Core:
    def __init__(self, *args, **kwargs):
        self.json_holder = None

    def DBAttackQuery(self, Platform_ID=None, Exploit_Title=None, Malware_Title=None, Auxiliary_Title=None):
        if Platform == "" or Platform is None:

    def JsonLoader(self,jsonfile=None):
        """
            @Args: [string] containing json contents or simply as json string.
            @default: [None]
            @return: [dict] Parse json contents.
        """
        if jsonfile is None and jsonfile == "":
            raise FileEmptyError("The File is empty")
        else:
            self.json_holder = None
            self.parameters = json.load(self.json_holder, jsonfile)
            if self.json_holder is not None or self.json_holder != "":
            return self.json_holder

class CoreUpload:
    def __init__(self):
        pass
    def ExpUploadType(self,Exp_Dialog):
        pass
        
class DBQueries:
    def __init__(self):
        pass    

class Algorithm:
    def __init__(self):
        pass