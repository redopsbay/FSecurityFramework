#!/usr/bin/python3

from Ui import Ui_CVEUpload
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
import pathlib
import sys
import os
from Core import CoreException
from Core import CoreLoadConfig

class CVEUpload(QDialog,Ui_CVEUpload.Ui_CVE_Dialog):
    """
        Malware Upload Dialog.
    """
    trigger_messageBox = pyqtSignal("QString")
    trigger_success = pyqtSignal()
    trigger_reject = pyqtSignal()

    def __init__(self,parent=None, LogBrowser=None):
        """
            Setup Default Values.
            Generate Required data's.
        """
        super(CVEUpload,self).__init__(parent)
        self.setupUi(self)
        self.empty_string = ""
        self.NoneString = None
        self.LogBrowser = LogBrowser
        self.CVE_buttonBox.accepted.connect(self.successfulValidation)
        self.CVE_buttonBox.rejected.connect(self.Reject)
        self.CVE_pdf.clicked.connect(self.getPdf)
        self.trigger_success.connect(self.Save)
        self.trigger_reject.connect(self.Reject)
        self.trigger_messageBox.connect(self.MessageBox)
        self.platform_name = ""
        self.platform_version = ""
        self.cve_title = ""
        self.cve_description = ""
        self.cve_author = ""
        self.pdf_filename = None

        self.required_data = {
                            "Name": None,
                            "Version": None, 
                            "Title": None,
                            "CVE_Author": None,
                            "Documentation": None,
                            "Description": None
                            }

    ################################
    #   Input Validation methods
    ################################

    def isPlatformEmpty(self):
        if self.CVE_Platform_Edit.text() == self.empty_string or self.CVE_Platform_Edit.text() is self.NoneString:
            self.platform_name = self.CVE_Platform_Edit.text()
            return True

    def isPlatformVersionEmpty(self):
        if self.CVE_Platform_Version_Edit.text() == self.empty_string or self.CVE_Platform_Version_Edit.text() is self.NoneString:
            self.platform_version = self.CVE_Platform_Version_Edit.text()
            return True
    
    def isTitle_Empty(self):
        """
            @Args: None
            @Default: None
            @Return: True if it is empty.
        """
        if self.CVE_Title_Edit.text() == self.empty_string or self.CVE_Title_Edit.text() is self.NoneString:
            self.cve_title = self.CVE_Title_Edit.text()
            return True

    def isAuthorEmpty(self):
        if self.CVE_Author_Edit.text() == self.empty_string or self.CVE_Author_Edit.text() is self.NoneString:
            self.cve_author = self.CVE_Author_Edit.text()
            return True

    def isDescriptionEmpty(self):
        """
            @Args: None
            @Default: None
            @Return: True if it is empty.
        """
        if self.CVE_Description_Text.toPlainText() == self.empty_string or self.CVE_Description_Text.toPlainText is self.NoneString:
            self.cve_description = self.CVE_Description_Text.toPlainText()
            return True
            
    def Clean(self):

        self.CVE_Platform_Edit.setText('')
        self.CVE_Platform_Version_Edit.setText('')
        self.CVE_Title_Edit.setText('')
        self.CVE_Author_Edit.setText('')
        self.CVE_Description_Text.setText('')
        self.platform_name = ""
        self.platform_version = ""
        self.cve_author = ""
        self.cve_description = ""
        self.cve_title = ""

    def Save(self):
        self.Clean()
        CoreLoadConfig.ConfigHandler.AccessWriteLogger("CVE Uploaded %s" % self.pdf_filename,self.LogBrowser)
        self.accept()

    def Reject(self):
        self.Clean()
        CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Upload CVE cancelled",self.LogBrowser)
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
            @return: isFileClean = True
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

    def MessageBox(self, stringvalue,boxtype="error"):
        """
            Provide Message Box for any types of unknown or invalid inputs.
        """
        messagebox = QMessageBox()
        messagebox.setText(stringvalue)
        messagebox.exec()
        if boxtype == "error":
            CoreLoadConfig.ConfigHandler.ErrorWriteLogger(stringvalue,self.LogBrowser)
        if boxtype == "access":
            CoreLoadConfig.ConfigHandler.AccessWriteLogger(stringvalue,self.LogBrowser)
       

    ################################
    #   Getter methods
    ################################
    def getAuthor(self):

        if self.isAuthorEmpty():
            return self.empty_string

        self.cve_author = self.CVE_Author_Edit.text()
        return self.cve_author

    def getPlatform(self):
        if self.isPlatformEmpty():
            return self.empty_string
        self.platform_name = self.CVE_Platform_Edit.text()
    
    def getPlatformVersion(self):
        if self.isPlatformVersionEmpty():
            return self.empty_string
        self.platform_version = self.CVE_Platform_Version_Edit.text()
        return self.platform_version

    def getTitle(self):
        if self.CVE_Title_Edit.text() == self.empty_string or self.CVE_Title_Edit.text() is self.NoneString:
            return self.empty_string
        self.cve_title = self.CVE_Title_Edit.text()
        return self.cve_title
    
    def getDocumentName(self):
        return self.pdf_filename

    def getDescription(self):
        if self.CVE_Description_Text.toPlainText() == self.empty_string or self.CVE_Description_Text.toPlainText() is self.NoneString:
            return self.empty_string

        self.cve_description = self.CVE_Description_Text.toPlainText()
        return self.cve_description

    def getPdf(self):
        self.pdf_filename = QFileDialog.getOpenFileName(self,"Open File","/home")
        if self.pdf_filename != ('',''):
            try:
                self.checkFile(self.pdf_filename[0])
            except CoreException.FileEmptyError as error:
                self.trigger_messageBox.emit("File is empty. Cause: %s" % error)
            except CoreException.FileNotSupportedError as FileNotSupport:
                self.trigger_messageBox.emit("File symbolic link not supported. Cause: %s" % FileNotSupport)
            finally:
                self.CVE_Document_Edit.setText(self.pdf_filename[0])
                self.pdf_filename  = self.pdf_filename[0]
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("Document chosen %s" % self.pdf_filename,self.LogBrowser)

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

        self.required_data['Version'] = "\"" +  str(self.platform_version) + "\""

        if self.getTitle() == self.empty_string or self.getTitle() is None:
            self.trigger_messageBox.emit("CVE Title should be provided")
            self.reject()
            return False

        self.required_data['Title'] = "\"" + str(self.cve_title) + "\""

        if self.getDocumentName() == self.empty_string or self.getDocumentName() is self.NoneString:
            self.trigger_messageBox.emit("Portable Document Format should be provided")
            self.reject()
            return False

        self.required_data['Documentation'] = "\"" + str(self.pdf_filename) + "\""

        if self.getAuthor() == self.empty_string or self.getAuthor() is self.NoneString:
            self.trigger_messageBox.emit("CVE Author should be provided")
            self.reject()
            return False

        self.required_data['CVE_Author'] = "\"" + str(self.cve_author) + "\""

        if self.getDescription() == self.empty_string or self.getDescription() is None:
            self.trigger_messageBox.emit("Description should be provided")
            self.reject()
            return False

        self.required_data['Description'] = "\"" + str(self.cve_description) + "\""
        self.trigger_success.emit()

    def uploadCVEClicked(self):
        CoreLoadConfig.ConfigHandler.AccessWriteLogger("Upload CVE Active",self.LogBrowser)
        self.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    upload = CVEUpload()
    upload.uploadCVEClicked()
    app.exec_()
