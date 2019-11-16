#!/usr/bin/python3
"""
    Loads configuration before starting up the User interface.
    if some errors our found. It will ignore the errors, but depending
    on the types or levels of errors.
"""
import os
import sys
import shutil
import time
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
 
class SingletonType(type):
    def __call__(cls):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType,cls).__call__()
            return cls.__instance

class ConfigHandler(metaclass=SingletonType):

    config_directory = "etc/fsecurity/"
    config_module_directory = "etc/fsecurity/module_config/"
    config_files = {
                "SocketServer": "SockServer.json",
                "DatabaseServer": "DatabaseServer.json",
                "Conf-enabled": "Conf-enabled.json"
                }
                
    profile_file = ".profile"
    save_file_data = None
    log_path = "var/log/fsecurity/"
    access_log = "access.log"
    error_log = "error.log"
    metadata = ".metadata"
    exploit_directory = "Attacks/exploits/"
    malware_directory = "Attacks/malwares/"
    auxiliary_directory = "Attacks/auxiliary/"
    metasploit_directory = "Attacks/metasploit/"
    cve_documentation_directory = "Attacks/cve/"

    def __init__(self):
        pass
    ################################
    #   Helper methods.
    ################################

    @classmethod 
    def getModuleConfig(cls):
        return cls.config_module_directory

    @classmethod
    def getDBConfig(cls):
        return cls.config_directory + cls.config_files['DatabaseServer']
     
    ################################
    #   Writter methods.
    ################################               
    @classmethod
    def CheckLogBrowser(cls,LogBrowser=None):
        if LogBrowser is None or LogBrowser == None:
            return True
        else:
            return False

    @classmethod
    def getExploitDir(cls):
        return cls.exploit_directory
    
    @classmethod
    def getMalwareDir(cls):
        return cls.malware_directory

    @classmethod
    def getAuxiliaryDir(cls):
        return cls.auxiliary_directory
    
    @classmethod
    def getMetasploitDir(cls):
        return cls.metasploit_directory

    @classmethod
    def getCVEDocumentDir(cls):
        return cls.cve_documentation_directory

    @classmethod
    def AccessWriteLogger(cls,MessageValue,LogBrowser=None):
        """
            @Args: [string] Message Value of ErrorWriteLogger to be write.
            @default: None
            @return [int] 0 value for successful write.
        """
        
        def CurTimer():
            return datetime.datetime.now().strftime("[%D-%H:%M:%S] ---- ")

        LogText = CurTimer() + " " + MessageValue
        file_to_open = cls.log_path + cls.access_log
        with open(file_to_open, 'a+') as file_log_handler:
                file_log_handler.write(LogText + '\n')

        if LogBrowser is None or LogBrowser == None:
            return False
        LogBrowser.append("<font color=yellowgreen><b> %s </b></font>" % LogText)

    @classmethod
    def ErrorWriteLogger(cls,MessageValue,LogBrowser=None):
        """
            @Args: [string] Message Value of ErrorWriteLogger to be write.
            @default: None
            @return [int] 0 value for successful write.
        """
        
        def CurTimer():
            return datetime.datetime.now().strftime("[%D-%H:%M:%S] ---- ")

        LogText = CurTimer() + " " + MessageValue
        file_to_open = cls.log_path + cls.error_log
        with open(file_to_open, 'a+') as file_log_handler:
                file_log_handler.write(LogText + '\n')
        if LogBrowser is None or LogBrowser == None:
            return False
            
        LogBrowser.append("<font color=red><b> %s </b></font>" % LogText)

    @classmethod
    def getSaveFileData(cls):
        return cls.save_file_data

    @classmethod
    def saveFileToDir(cls, identity=None, attack_data=None):
         # Convert to lower character strings. 
        if identity == None  and attack_data == None or identity is None and attack_data is None:
            raise CoreException.ParameterError("Missing (identity) parameter")
            return False
        identity = identity.lower()
        if identity == "exploit":
            exploit_dir = cls.exploit_directory
            option_dir = cls.config_module_directory
            exploit_file = attack_data['module_name']
            option_file = attack_data['option_name']
            exploit_file_extension = '.' + os.path.basename(exploit_file).split('.')[1]
            option_file_extension = ".json"
            exploit_destination = cls.exploit_directory + os.path.basename(exploit_file).split("\"")[0]
            option_destination = cls.config_module_directory + os.path.basename(option_file).split("\"")[0]
            shutil.copy(exploit_file.split("\"")[1], exploit_destination)
            shutil.copy(option_file.split("\"")[1], option_destination)

        if identity == "malware":
            malware_dir = cls.malware_directory
            option_dir = cls.config_module_directory
            malware_file = attack_data['module_name']
            option_file = attack_data['option_name']
            malware_file_extension = '.' + os.path.basename(malware_file).split('.')[1]
            option_file_extension = ".json"
            malware_destination = cls.malware_directory + os.path.basename(malware_file).split("\"")[0]
            option_destination = cls.config_module_directory + os.path.basename(option_file).split("\"")[0]
            shutil.copy(malware_file.split("\"")[1], malware_destination)
            shutil.copy(option_file.split("\"")[1], option_destination)

        if identity == "cve":
            documentation_dir = cls.cve_documentation_directory
            document_file = attack_data['Documentation']
            document_file_extension = '.pdf'
            document_destination = cls.cve_documentation_directory + os.path.basename(document_file).split("\"")[0]
            shutil.copy(document_file.split("\"")[1], document_destination)
