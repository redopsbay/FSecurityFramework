#!/usr/bin/python3

from Ui import Ui_ExpUpload
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from Core import CoreLoadConfig
from Core import CoreException
import pathlib
import socket
import sys


class ExpUpload(QDialog, Ui_ExpUpload.Ui_Exp_Dialog):
    """
        Exploit Upload Dialog.
    """
    trigger_messageBox = pyqtSignal("QString")
    trigger_success = pyqtSignal()
    trigger_reject = pyqtSignal()
    def __init__(self,parent=None, LogBrowser=None):
        """
            Setup Default Values.
            Generate Required data's.
        """
        super(ExpUpload,self).__init__(parent)
        self.LogBrowser=LogBrowser
        self.setupUi(self)
        self.empty_string = ""
        self.NoneString = None
        self.Exp_Ratings.MaxCount = 4
        self.Exp_Type.MaxCount = 2
        self.ratings = ["Great","Good","Low"]
        self.counterRatings = 0
        self.types = ["Local", "Remote"]
        self.counterTypes = 0
        self.ExpButtonBox.accepted.connect(self.successfulValidation)
        self.ExpButtonBox.rejected.connect(self.Reject)
        self.trigger_success.connect(self.Save)
        self.trigger_reject.connect(self.Reject)
        self.trigger_messageBox.connect(self.MessageBox)
        self.Exp_Architectures_Options = {"ALL": self.Exp_ALL_Opt,
                                  "x86": self.Exp_x86_Opt,
                                  "x64": self.Exp_x64_Opt,
                                  "x86_64": self.Exp_x86_64_Opt }
        self.platform_name = ""
        self.platform_version = ""
        self.exploit_title = ""
        self.exploit_description = ""
        self.exploit_author = ""
        self.option_name = ""
        self.module_name = ""
        self.arch_name = ""
        self.Exp_Opt_JSON.clicked.connect(self.getOption)
        self.Exp_Mod_Push.clicked.connect(self.getModule)
        self.filename = None

        for rates in self.ratings: 
            self.counterRatings += 1
            self.Exp_Ratings.addItem(rates)
            self.Exp_Ratings.setCurrentIndex(self.counterRatings)
            self.counterRatings += 1


        for types in self.types:
            self.Exp_Type.addItem(types)
            self.Exp_Type.setCurrentIndex(self.counterTypes)
            self.counterTypes += 1

        for key, value in self.Exp_Architectures_Options.items():
            self.Exp_Architectures_Options[key].pressed.connect(self.setArch)

        self.required_data = {
                            "Name": None,
                            "Version": None, 
                            "Arch": None,
                            "Title": None,
                            "module_name": None,
                            "option_name": None,
                            "Exploit_Author": None,
                            "Ratings": None,
                            "Type": None,
                            "Description": None,
                            "UPLOAD_TYPE_ID": "EXP_ID"
                            }

    ################################
    #   Input Validation methods
    ################################

    def isPlatformEmpty(self):
        if self.Exp_Platform_Edit.text() == self.empty_string or self.Exp_Platform_Edit.text() is self.NoneString:
            self.platform_name = self.Exp_Platform_Edit.text()
            return True

    def isPlatformVersionEmpty(self):
        if self.Exp_Platform_Version_Edit.text() == self.empty_string or self.Exp_Platform_Version_Edit.text() is self.NoneString:
            self.platform_version = self.Exp_Platform_Version_Edit.text()
            return True
    
    def isTitle_Empty(self):
        """
            @Args: None
            @Default: None
            @Return: True if it is empty.
        """
        if self.Exp_Title_Edit.text() == self.empty_string or self.Exp_Title_Edit.text() is self.NoneString:
            self.exploit_title = self.Exp_Title_Edit.text()
            return True

    def isModuleEmpty(self):
        
        if self.module_name == self.empty_string or self.module_name is self.NoneString:
            return True

    def isOptionsEmpty(self):
        if self.option_name == self.empty_string or self.option_name is self.NoneString:
            return True

    def isAuthorEmpty(self):
        if self.Exp_Author_Edit.text() == self.empty_string or self.Exp_Author_Edit.text() is self.NoneString:
            return True

    def isDescriptionEmpty(self):
        """
            @Args: None
            @Default: None
            @Return: True if it is empty.
        """
        if self.Exp_Description_Text.toPlainText() == self.empty_string or self.Exp_Description_Text.toPlainText is self.NoneString:
            self.exploit_description = self.Exp_Description_Text.toPlainText()
            return True

    def Clean(self):

        self.Exp_Platform_Edit.setText('')
        self.Exp_Platform_Version_Edit.setText('')
        self.Exp_Title_Edit.setText('')
        self.Exp_Mod_Edit.setText('')
        self.Exp_Author_Edit.setText('')
        self.Exp_Description_Text.setText('')
        self.Exp_Opt_Edit.setText('')
        self.platform_name = ""
        self.platform_version = ""
        self.exploit_author = ""
        self.exploit_description = ""
        self.exploit_title = ""
        self.module_name = ""
        self.option_name = ""

    def setArch(self):
         for key, value in self.Exp_Architectures_Options.items():
            if self.Exp_Architectures_Options[key].isDown():
                self.arch_name = key

    def Save(self):
        self.Clean()
        CoreLoadConfig.ConfigHandler.AccessWriteLogger("Exploit Uploaded %s" % self.module_name,self.LogBrowser)
        self.accept()

    def Reject(self):
        self.Clean()
        CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Upload Cancelled",self.LogBrowser)
        self.reject()

    def getSuccessData(self):
        """
            Return the required_data.
        """
        return self.required_data

    def checkFile(self,selected_file):
        """
            Validate the given file. Check for any possible errors.
            @Args: None
            @Default: None
            @return: 
        """
        path_holder = pathlib.Path(selected_file)
        if path_holder.exists():
            if path_holder.is_file():
                if path_holder.stat().st_size == 0 or path_holder.stat().st_size is None:
                    raise CoreException.FileEmptyError("File should not be empty!")
                    return False

                if path_holder.is_symlink():
                    raise CoreException.FileNotSupportedError("Symbolic link not supported")
                    return False
              
               # File Clean if they pass the required identity of file.
                return True

    def MessageBox(self, stringvalue, boxtype="error"):
        """
            Provide Message Box for any types of unknown or invalid inputs.
        """
        if boxtype == "error":
            CoreLoadConfig.ConfigHandler.ErrorWriteLogger(stringvalue,self.LogBrowser)
            messagebox = QMessageBox()
            messagebox.setText(stringvalue)
            messagebox.setWindowTitle("ERROR!")
            messagebox.exec()

        if boxtype == "access":
            CoreLoadConfig.ConfigHandler.AccessWriteLogger(stringvalue,self.LogBrowser)
            messagebox = QMessageBox()
            messagebox.setText(stringvalue)
            messagebox.setWindowTitle("Message")
            messagebox.exec()
            
    ################################
    #   Getter methods
    ################################
    def getAuthor(self):

        if self.isAuthorEmpty():
            return self.empty_string
        self.exploit_author = self.Exp_Author_Edit.text()

        return self.exploit_author

    def getPlatform(self):
        if self.isPlatformEmpty():
            return self.empty_string
        self.platform_name = self.Exp_Platform_Edit.text()
    
    def getPlatformVersion(self):
        if self.isPlatformVersionEmpty():
            return self.empty_string
        self.platform_version = self.Exp_Platform_Version_Edit.text()
        return self.platform_version
        
    def getArch(self):
        """
            @Args: None.)
            @Default: None.
            @Return: Architecture.
        """
        return self.arch_name

    def getTitle(self):
        if self.Exp_Title_Edit.text() == self.empty_string or self.Exp_Title_Edit.text() is self.NoneString:
            return self.empty_string
        self.exploit_title = self.Exp_Title_Edit.text()
        return self.exploit_title

    def getDescription(self):
        if self.Exp_Description_Text.toPlainText() == self.empty_string or self.Exp_Description_Text.toPlainText() is self.NoneString:
            return self.empty_string

        self.exploit_description = self.Exp_Description_Text.toPlainText()
        return self.exploit_description

    def getAuthor(self):
        if self.Exp_Author_Edit.text() == self.empty_string or self.Exp_Author_Edit.text() is self.NoneString:
            return self.empty_string

        self.exploit_author = self.Exp_Author_Edit.text()
        return self.exploit_author
    
    def getRatings(self):
        return self.ratings[self.Exp_Ratings.currentIndex()]

    def getType(self):
        return self.types[self.Exp_Type.currentIndex()]

    def getModule(self):
        self.module_name = QFileDialog.getOpenFileName(self,"Open File","/home")
        if self.module_name != ('',''):
            try:
                self.checkFile(self.module_name[0])
            except CoreException.FileEmptyError as error:
                self.trigger_messageBox.emit("File is empty. Cause: %s" % error)
            except CoreException.FileNotSupportedError as FileNotSupport:
                self.trigger_messageBox.emit("File symbolic link not supported. Cause: %s" % FileNotSupport)
            finally:
                self.Exp_Mod_Edit.setText(self.module_name[0])
                self.module_name  = self.module_name[0]
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("Exploit Module chosen %s" % self.module_name,self.LogBrowser)

    def getModuleName(self):
        return self.module_name

    def getOption(self):
        self.option_name = QFileDialog.getOpenFileName(self,"Open File","/home","*.JSON")
        if self.option_name != ('',''):
            try:
                self.checkFile(self.option_name[0])
            except CoreException.FileEmptyError as error:
                self.trigger_messageBox.emit("File is empty. Cause: %s" % error)
            except CoreException.FileNotSupportedError as FileNotSupport:
                self.trigger_messageBox.emit("File symbolic link not supported. Cause: %s" % FileNotSupport)
            finally:
                self.Exp_Opt_Edit.setText(self.option_name[0])
                self.option_name = self.option_name[0]
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("Exploit option chosen %s" % self.option_name,self.LogBrowser)

    def getOptionName(self):
        return self.option_name

    def successfulValidation(self):
        if self.getPlatform() == self.empty_string or self.getPlatform is self.NoneString:
            self.trigger_messageBox.emit("Platform should be provided")
            self.reject()
            return False

        self.required_data['Name'] = "\"" + str(self.platform_name) + "\""

        if self.getPlatformVersion() == self.empty_string or self.getPlatformVersion is self.NoneString:
            self.trigger_messageBox.emit("Platform version should be provided")
            self.reject()
            return False

        self.required_data['Version'] = "\"" + str(self.platform_version) + "\""

        if self.getTitle() == self.empty_string or self.getTitle() is None:
            self.trigger_messageBox.emit("Exploit Title should be provided")
            self.reject()
            return False

        self.required_data['Title'] = "\"" + str(self.exploit_title) + "\""

        if self.getArch() == self.empty_string or self.getArch() is self.NoneString:
            self.trigger_messageBox.emit("Architecture should be chosen")
            self.reject()
            return False

        self.required_data['Arch'] = "\"" + str(self.getArch()) + "\""

        if self.getModuleName() == self.empty_string or self.getModuleName() is self.NoneString:
            self.trigger_messageBox.emit("Module should be provided")
            self.reject()
            return False

        self.required_data['module_name'] = "\"" + str(self.module_name) + "\""


        if self.getOptionName() == self.empty_string or self.getOptionName() is self.NoneString:
            self.trigger_messageBox.emit("Option should be provided")
            self.reject()
            return False

        self.required_data['option_name'] = "\"" + str(self.option_name) + "\""

        if self.getAuthor() == self.empty_string or self.getAuthor is self.NoneString:
            self.trigger_messageBox.emit("Exploit Author should be provided")
            self.reject()
            return False

        self.required_data['Exploit_Author'] = "\"" + str(self.exploit_author) + "\""

        if self.getDescription() == self.empty_string or self.getDescription() is None:
            self.trigger_messageBox.emit("Description should be provided")
            self.reject()
            return False

        self.required_data['Description'] = "\"" + str(self.exploit_description) + "\""
        self.required_data['Ratings'] = "\"" + str(self.getRatings()) + "\""
        self.required_data['Type'] = "\"" + str(self.getType()) + "\""

        self.trigger_success.emit()

    def uploadExploitClicked(self):
        CoreLoadConfig.ConfigHandler.AccessWriteLogger("Upload Exploit Active",self.LogBrowser)
        self.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    upload = ExpUpload()
    upload.UploadExploitClicked()
    app.exec_()
