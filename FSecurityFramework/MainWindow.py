#!/usr/bin/python3
"""
    This is the Main Window of the framework.
    subclassing the Ui_MainWindow class.
"""
import sys
import copy
import json
import os
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as netiface
import MalwareUploadDialog
import CVEUpload
import ExpUpload
import TableInserter
import netdiscover
import CveTable
import Terminal
import AttackBrowser
import copy
import AttackOptionDialog
import subprocess
import tcpdump
from metasploit import Metasploit
import AttackLauncher
import threading
import harvester
from Ui import Ui_MainWindow
from Core import CoreLoadConfig
from ThreadHandlers import CoreThread
from Core import CoreException
from Db import DBManipulator
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pymetasploit3 import *
from TabManager import TabAdder

class MainWindow(QMainWindow,Ui_MainWindow.Ui_MainWindow):
    """
        Constructing MainWindow.
    """
    uploadExploits_Accepted = pyqtSignal()
    trigger_uploadClickedExploits = pyqtSignal()
    
    def __init__(self,parent=None,network_interface="lo"):
        """ Derived from Ui_MainWindow  """
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.cve_table = CveTable.CVETable_Widget(self.tabWidget)
        self.network_interface = network_interface
        self.ip_address = ""
        self.exploit_option_dialog = AttackOptionDialog.AttackOptionDialog(self,self.LogBrowser)
        self.android_option_dialog = AttackOptionDialog.AttackOptionDialog(self,self.LogBrowser)
        self.android_option_dialog.accepted.connect(self.runAndroidExploit)
        self.confighandler = CoreLoadConfig.ConfigHandler()
        self.uploaded_exploit_data = None
        self.uploaded_malware_data = None
        self.uploaded_cve_data = None
        self.db_connection_status = "Database Status: Connected"
        self.sql_queries = DBManipulator.SqlQueries(self.LogBrowser)
        self.cve_upload_dialog = CVEUpload.CVEUpload(LogBrowser=self.LogBrowser)
        self.exploit_upload_dialog = ExpUpload.ExpUpload(LogBrowser=self.LogBrowser)
        self.malware_upload_dialog = MalwareUploadDialog.MalwareUploadDialog(LogBrowser=self.LogBrowser)
        self.actionExploits.triggered.connect(self.exploit_upload_dialog.uploadExploitClicked)
        self.actionPayloads.triggered.connect(self.malware_upload_dialog.uploadMalwareClicked)
        self.actionCVE.triggered.connect(self.cve_upload_dialog.uploadCVEClicked)
        self.malware_upload_dialog.accepted.connect(self.SaveMalwareToDB)
        self.exploit_upload_dialog.accepted.connect(self.SaveExploitToDB)
        self.cve_upload_dialog.accepted.connect(self.SaveCVEToDB)
        self.terminal = Terminal.Terminal()
        self.AndroidAttack.clicked.connect(self.androidattack)
        self.TerminalLoader.clicked.connect(self.ShowTerminal)
        self.ReloadButton.clicked.connect(self.Reload)
        self.actionShow_CVE.triggered.connect(self.showCVE)
        self.Exploit_Table.itemDoubleClicked.connect(self.LaunchExploit)
        self.Malware_Table.itemDoubleClicked.connect(self.LaunchMalware)
        self.harvester = harvester.EmailHarvester()
        self.EHarvest.clicked.connect(self.ShowHarvester)
        self.actionFind_Public_Emails_2.triggered.connect(self.ShowHarvester)
        self.tabadder = TabAdder()
        self.inserter = TableInserter.QueryManager(self.LogBrowser,self.sql_queries)
        self.attackbrowser = AttackBrowser.AttackBrowser()
        self.attackbrowser.setupUi(self.attackbrowser)
        self.metasploit = Metasploit()
        self.IPLabel.setText("IP Address : %s" % self.getIP())
        self.netdiscover = netdiscover.NetDiscover()
        self.tcpdump = tcpdump.TcpDump()
        self.DiscoverNetwork.clicked.connect(self.ShowNetworkDiscovery)
        self.MploitLoader.clicked.connect(self.ShowMetasploit)
        self.attackbrowser_exploit_list = []
        self.attackbrowser_android_list = []
        self.attackbrowser_android_counter = 0
        self.harvester_option_dialog = AttackOptionDialog.AttackOptionDialog()
        self.harvester_option_dialog.accepted.connect(self.RunHarvester)
        self.harvester_title = "Email Harvester"
        self.harvester_module_option = None
        self.harvester_module_path_option = "etc/fsecurity/module_config/harvester.json"
        self.android_threads = []
        self.android_title = "Android Exploit"
        self.android_module = "Attacks/exploits/android_exploit.py"
        self.android_module_path_option = "etc/fsecurity/module_config/android_exploit_config.json"
        self.android_module_option = None
        self.android_threads_counter = 0
        self.attackbrowser_exploit_counter = 0
        self.attackbrowser_malware_list = []
        self.attackbrowser_malware_counter = 0
        self.malware_option_dialog = AttackOptionDialog.AttackOptionDialog(self,self.LogBrowser)
        self.malware_option_dialog.accepted.connect(self.runMalware)
        self.exploit_option_dialog.accepted.connect(self.runExploit)
        self.actionShow_Exploit.triggered.connect(self.showExploit)
        self.actionShow_Malware.triggered.connect(self.showMalware)
        self.TcpDumpLoader.clicked.connect(self.ShowTcpDump)
        self.actionEdit_Configuration.triggered.connect(self.editConfig)
        self.actionNetwork_Mapper.triggered.connect(self.runNmap)
        self.OSDetector.clicked.connect(self.runNmap)
        self.actionExit.triggered.connect(self.Exit)
        #self.actionAuthors.triggered.connect(self.showAuthors)
        self.document_threads = []
        self.malware_threads = []
        self.exploit_threads = [] 
        self.exploit_threads_counter = 0
        self.malware_threads_counter = 0
        self.document_threads_counter = 0
        self.exploit_title = None
        self.active_module_counter = 0
        self.active_module = []
        self.malware_title = None
        self.exploit_module = None
        self.malware_module = None
        self.exploit_module_option = None
        self.malware_module_option = None
        self.attack_launcher = AttackLauncher.AttackLauncher(self.LogBrowser)
        self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)

    def Exit(self):
        mysql_disabled = subprocess.Popen("/etc/init.d/mysql stop", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msfrpcd_disabled = subprocess.Popen("killall msfprcd",shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        sys.exit(0)

    def runNmap(self):
        if os.path.exists('/usr/bin/zenmap'):
            CoreLoadConfig.ConfigHandler.AccessWriteLogger("Launching Network Mapper (Nmap)", self.LogBrowser)
            subprocess.Popen("zenmap",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        else:
            messagebox = QMessageBox()
            messagebox.setText("Please install nmap and zenmap by typing into terminal\n sudo apt-get install nmap zenmap")
            messagebox.setWindowTitle("Error!")
            messagebox.exec()
            CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Nmap and Zenmap is not installed. Please install nmap before running it.", self.LogBrowser)

    def editConfig(self):
        process = subprocess.Popen("xdg-open %s" % CoreLoadConfig.ConfigHandler.getDBConfig(),shell=True)
        messagebox = QMessageBox()
        messagebox.setText("Opening Configuration file. Please wait!")
        messagebox.setWindowTitle("Opening Configuration")
        messagebox.exec()

    def getIP(self):
        try:
            self.ip_address = netiface.ifaddresses(self.network_interface)[AF_INET][0]['addr']
            return self.ip_address
        except ValueError as Ve:
            self.network_interface = "lo"
            self.ip_address = netiface.ifaddresses(self.network_interface)[AF_INET][0]['addr']
        

    def ConnectToDB(self):
        try:
            self.sql_queries.ConnectDB()
            if self.sql_queries.getDBConnectionStatus():
                self.dblabel.setText(self.db_connection_status)
            else:
                self.db_connection_status = "Database Status: Not Connected"
                self.dblabel.setText(self.db_connection_status)

        except CoreException.DatabaseConnectionArgumentError as DBError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("Argument Error: %s " % DBError)
            else:
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("Argument Error: %s " % DBError, self.LogBrowser)

    def SaveMalwareToDB(self):
        try:
            malware_data_dictionary = self.malware_upload_dialog.getSuccessData()
            self.sql_queries.saveMalware(malware_data_dictionary)

        except CoreException.DatabaseConnectionError as DBConError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("DB Connection Error: %s " % DBConError)
            else:
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("DB Connection Error: %s " % DBConError, self.LogBrowser)
                self.malware_upload_dialog.MessageBox("You are not connected to the database yet")
                return False

        if self.sql_queries.getMalwareUploadStatus() == True:
            self.malware_upload_dialog.MessageBox("Malware Uploaded","access")
            self.malware_upload_dialog.MessageBox("Table will be reloaded", "access")
            self.inserter.QueueItems("malware",self.Malware_Table)

    def SaveExploitToDB(self):

        try:
            exploit_data_dictionary = self.exploit_upload_dialog.getSuccessData()
            self.sql_queries.saveExploit(exploit_data_dictionary)

        except CoreException.DatabaseConnectionError as DBConError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("DB Connection Error: %s " % DBConError)
            else:
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("DB Connection Error: %s " % DBConError, self.LogBrowser)
                self.exploit_upload_dialog.MessageBox("You are not connected to the database yet",boxtype="error")
                return False

        if self.sql_queries.getExploitUploadStatus() == True:
            self.exploit_upload_dialog.MessageBox("Exploit Uploaded",boxtype="access")
            self.exploit_upload_dialog.MessageBox("Table will be reloaded",boxtype="access")
            self.inserter.QueueItems("exploit",self.Exploit_Table)


    def SaveCVEToDB(self):
        try:
            cve_data_dictionary = self.cve_upload_dialog.getSuccessData()
            self.sql_queries.saveCVE(cve_data_dictionary)
        except CoreException.DatabaseConnectionError as DBConError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("DB Connection Error: %s " % DBConError)
            else:
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("DB Connection Error: %s " % DBConError, self.LogBrowser)
                self.cve_upload_dialog.MessageBox("You are not connected to the database yet",boxtype="error")
                return False

        if self.sql_queries.getCVEUploadStatus() == True:
            self.cve_upload_dialog.MessageBox("CVE Document Uploaded",boxtype="access")
            self.cve_upload_dialog.MessageBox("Table will be reloaded",boxtype="access")

    def ShowHarvester(self):
        self.harvester.setupUi(self.tabWidget)
        self.harvester_option_dialog.setWindowTitle("Auxiliary - " + self.harvester_title)
        self.harvester_option_dialog.addParam(self.harvester_module_path_option)
        self.harvester_option_dialog.show()
        self.harvester.process.finished.connect(self.delharvester)
        self.harvester.process.finished.connect(self.openResult)

    def openResult(self):
        messagebox = QMessageBox()
        messagebox.setText("Opening harvested emails result!")
        messagebox.setWindowTitle("Opening Result")
        messagebox.exec()
        subprocess.Popen("mv -v *.html {OUTPUT_DIRECTORY}".format_map(self.harvester_module_option), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = subprocess.Popen("xdg-open {OUTPUT_DIRECTORY}{RESULT}".format_map(self.harvester_module_option),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        messagebox.setText("If the result does not open automatically. The harvester result can be found at: {OUTPUT_DIRECTORY}{RESULT}".format_map(self.harvester_module_option))
        messagebox.setWindowTitle("Message")
        messagebox.exec()

    def RunHarvester(self):
        self.harvester_module_option = self.harvester_option_dialog.getParseParameters() 
        if self.harvester_module_option == None:
            messagebox = QMessageBox()
            messagebox.setText("Email harvester does'nt meet required parameters!")
            messagebox.setWindowTitle("Error!")
        else:
            self.harvester.startTask(self.harvester_module_option)
            self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Email Harvester", parent=self.harvester, LogBrowser=self.LogBrowser)


    def delharvester(self):
        self.tabWidget.removeTab(self.tabWidget.indexOf(self.harvester))
        try:
            self.EHarvest.clicked.disconnect(self.ShowHarvester)
            self.actionFind_Public_Emails_2.triggered.disconnect(self.ShowHarvester)
        except TypeError as AttribError:
            CoreLoadConfig.ConfigHandler.ErrorWriteLogger("TypeError on Disconnecting [self.EHarvest.clicked signal] ", self.LogBrowser)
        self.EHarvest.clicked.connect(self.ReRunHarvester)
        self.actionFind_Public_Emails_2.triggered.connect(self.ReRunHarvester)

    def ReRunHarvester(self):
      #  self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Email Harvester", parent=self.harvester,LogBrowser=self.LogBrowser)
       # self.harvester.setupUi(self.tabWidget)
        self.harvester_option_dialog.setWindowTitle("Auxiliary - " + self.harvester_title)
        self.harvester_option_dialog.addParam(self.harvester_module_path_option)
        self.harvester_option_dialog.show()
        self.harvester.process.finished.connect(self.delharvester)

    def showCVE(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget,Title_Page="CVE",parent=self.cve_table,LogBrowser=self.LogBrowser)
        self.cve_table.setupUi(self.cve_table)
        self.cve_table.tableWidget.itemDoubleClicked.connect(self.openDocument)

    def showExploit(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget,Title_Page="Exploits",parent=self.Exploit_Table,LogBrowser=self.LogBrowser)

    def showMalware(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget,Title_Page="Malwares",parent=self.Malware_Table,LogBrowser=self.LogBrowser)

    @pyqtSlot(QTableWidgetItem)
    def openDocument(self,item):
        currentRow = self.cve_table.tableWidget.currentRow()
        currentColumn = self.cve_table.tableWidget.currentColumn()
        messagebox = QMessageBox()
        messagebox.setText("Please wait while opening CVE document %s" % self.cve_table.tableWidget.item(currentRow,6).text())
        messagebox.setWindowTitle("Opening CVE document please wait")
        messagebox.exec()
        subprocess.Popen(r"xdg-open %s" % str(self.cve_table.tableWidget.item(currentRow,6).text()), shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    def ShowTerminal(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Terminal", parent=self.terminal,LogBrowser=self.LogBrowser)
        self.terminal.setupUi(self.tabWidget)
        self.terminal.startTask()
        self.terminal.process.finished.connect(self.delterminal)

    def delterminal(self):
        self.tabWidget.removeTab(self.tabWidget.indexOf(self.terminal))
        self.TerminalLoader.clicked.disconnect(self.ShowTerminal)
        self.TerminalLoader.clicked.connect(self.RerunTerminal)

    def RerunTerminal(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Terminal", parent=self.terminal,LogBrowser=self.LogBrowser)
        self.terminal.startTask()

    def ShowMetasploit(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Metasploit Framework", parent=self.metasploit,LogBrowser=self.LogBrowser)
        self.metasploit.setupUi(self.tabWidget)
        self.metasploit.startTask()
        self.metasploit.process.finished.connect(self.delmetasploit)

    def delmetasploit(self):
        self.tabWidget.removeTab(self.tabWidget.indexOf(self.metasploit))
        self.MploitLoader.clicked.disconnect(self.ShowMetasploit)
        self.MploitLoader.clicked.connect(self.RerunMetasploit)

    def RerunMetasploit(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Metasploit Framework", parent=self.metasploit,LogBrowser=self.LogBrowser)
        self.metasploit.startTask()

    def ShowNetworkDiscovery(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Network Discovery", parent=self.netdiscover,LogBrowser=self.LogBrowser)
        self.netdiscover.setupUi(self.tabWidget)
        self.netdiscover.startTask()
        self.netdiscover.process.finished.connect(self.delnetdiscover)

    def delnetdiscover(self):
        self.tabWidget.removeTab(self.tabWidget.indexOf(self.netdiscover))
        self.DiscoverNetwork.clicked.disconnect(self.ShowNetworkDiscovery)
        self.DiscoverNetwork.clicked.connect(self.RerunNetdiscover)

    def RerunNetdiscover(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Network Discovery", parent=self.netdiscover,LogBrowser=self.LogBrowser)
        self.netdiscover.startTask()

    def ShowTcpDump(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Capture Live Packets", parent=self.tcpdump,LogBrowser=self.LogBrowser)        
        self.tcpdump.setupUi(self.tabWidget)
        self.tcpdump.startTask()
        self.tcpdump.process.finished.connect(self.deltcpdump)

    def deltcpdump(self):
        self.tabWidget.removeTab(self.tabWidget.indexOf(self.tcpdump))
        self.TcpDumpLoader.clicked.disconnect(self.ShowTcpDump)
        self.TcpDumpLoader.clicked.connect(self.Reruntcpdump)

    def Reruntcpdump(self):
        self.tabadder.AddTab(Tab_Object=self.tabWidget, Title_Page="Capture Live Packets", parent=self.tcpdump,LogBrowser=self.LogBrowser)
        self.tcpdump.startTask()

    @pyqtSlot(QTableWidgetItem)
    def LaunchExploit(self,item):
        #CSV: ID,Title,Description,Platform,Version,Arch,Language,Module, Module Option, Type,Date,Ratings,Malware_Author
        currentRow = self.Exploit_Table.currentRow()
        currentColumn = self.Exploit_Table.currentColumn()
        self.exploit_title = str(self.Exploit_Table.item(currentRow,1).text())
        self.exploit_module = str(self.Exploit_Table.item(currentRow,7).text())
        self.exploit_module_option = str(self.Exploit_Table.item(currentRow,8).text())
        self.exploit_option_dialog.setWindowTitle("Exploit - " + self.exploit_title)
        self.exploit_option_dialog.addParam(self.exploit_module_option)
        self.exploit_option_dialog.show()

    @pyqtSlot(QTableWidgetItem)
    def LaunchMalware(self,item):
        #CSV:  ID,Title,Description,Platform,Version,Arch,Language,Module,Module Option,Type,Date,Ratings,Malware_Author
        currentRow = self.Malware_Table.currentRow()
        currentColumn = self.Malware_Table.currentColumn()
        self.malware_title = self.Malware_Table.item(currentRow,1).text()
        self.malware_module = self.Malware_Table.item(currentRow,7).text()
        self.malware_module_option = self.Malware_Table.item(currentRow,8).text()
        self.malware_option_dialog.setWindowTitle("Malware - " + str(self.malware_title))
        self.malware_option_dialog.addParam(self.malware_module_option)
        self.malware_option_dialog.show()

    def runExploit(self):
        self.exploit_module_option = self.exploit_option_dialog.getParseParameters()
        if self.exploit_module_option == None:
            messagebox = QMessageBox()
            messagebox.setText("Failed to parse JSON Exploit option file!")
            messagebox.setWindowTitle("ERROR!")
            messagebox.exec()
            return False
        else:
            temp_browser = AttackBrowser.AttackBrowser()
            temp_browser.setupUi(temp_browser)
            self.attackbrowser_exploit_list.append(temp_browser)
            self.active_module.append(self.attack_launcher.start_attack(self.exploit_module,self.exploit_module_option,self.attackbrowser_exploit_list[self.attackbrowser_exploit_counter],self.tabWidget,self.exploit_title))
            self.attackbrowser_exploit_list[self.attackbrowser_exploit_counter].lineEdit.returnPressed.connect(self.active_module[self.active_module_counter].commandlistener)
            self.attackbrowser_exploit_list[self.attackbrowser_exploit_counter].pushButton.clicked.connect(self.active_module[self.active_module_counter].commandlistener)
            thread = CoreThread.CoreThread(target=self.active_module[self.active_module_counter].run(),LogBrowser=self.LogBrowser,delay=0)
            thread.start()
            self.exploit_threads_counter += 1
            self.exploit_threads.append(thread)
            self.active_module_counter += 1
            self.attackbrowser_exploit_counter += 1
            messagebox = QMessageBox()
            messagebox.setText("Launching Exploit: %s" % self.exploit_title)
            messagebox.setWindowTitle("Opening %s" % self.exploit_title)
            messagebox.exec()

    def androidattack(self):
        self.android_option_dialog.setWindowTitle("Exploit - " + self.android_title)
        self.android_option_dialog.addParam(self.android_module_path_option)
        self.android_option_dialog.show()

    def runAndroidExploit(self):
        self.android_module_option = self.android_option_dialog.getParseParameters()
        if self.android_module_option == None:
            messagebox = QMessageBox()
            messagebox.setText("Failed to parse JSON Android Exploit option file!")
            messagebox.setWindowTitle("ERROR!")
            messagebox.exec()
            return False
        else:
            temp_browser = AttackBrowser.AttackBrowser()
            temp_browser.setupUi(temp_browser)
            self.attackbrowser_android_list.append(temp_browser)
            self.active_module.append(self.attack_launcher.start_attack(self.android_module,self.android_module_option,self.attackbrowser_android_list[self.attackbrowser_android_counter],self.tabWidget,self.android_title))
            self.attackbrowser_android_list[self.attackbrowser_android_counter].lineEdit.returnPressed.connect(self.active_module[self.active_module_counter].commandlistener)
            self.attackbrowser_android_list[self.attackbrowser_android_counter].pushButton.clicked.connect(self.active_module[self.active_module_counter].commandlistener)
            thread = CoreThread.CoreThread(target=self.active_module[self.active_module_counter].run(),LogBrowser=self.LogBrowser,delay=0)
            thread.start()
            self.android_threads_counter += 1
            self.android_threads.append(thread)
            self.active_module_counter += 1
            self.attackbrowser_android_counter += 1
            messagebox = QMessageBox()
            messagebox.setText("Launching Android Exploit: %s" % self.android_title)
            messagebox.setWindowTitle("Opening %s" % self.android_title)
            messagebox.exec()

    def runMalware(self):
        self.malware_module_option = self.malware_option_dialog.getParseParameters()
        if self.malware_module_option == None:
            messagebox = QMessageBox()
            messagebox.setText("Failed to parse JSON Malware option file!")
            messagebox.setWindowTitle("ERROR!")
            messagebox.exec()
            return False
        else:
            temp_browser = AttackBrowser.AttackBrowser()
            temp_browser.setupUi(temp_browser)
            self.attackbrowser_malware_list.append(temp_browser)
            self.active_module.append(self.attack_launcher.start_attack(self.malware_module,self.malware_module_option,self.attackbrowser_malware_list[self.attackbrowser_malware_counter],self.tabWidget,self.malware_title))
            self.attackbrowser_malware_list[self.attackbrowser_malware_counter].lineEdit.returnPressed.connect(self.active_module[self.active_module_counter].commandlistener)
            self.attackbrowser_malware_list[self.attackbrowser_malware_counter].pushButton.clicked.connect(self.active_module[self.active_module_counter].commandlistener)
            thread = CoreThread.CoreThread(target=self.active_module[self.active_module_counter].run(),LogBrowser=self.LogBrowser,delay=0)
            thread.start()
            self.malware_threads_counter += 1
            self.malware_threads.append(thread)
            self.active_module_counter += 1
            self.attackbrowser_malware_counter += 1
            messagebox = QMessageBox()
            messagebox.setText("Launching Malware: %s" % self.malware_title)
            messagebox.setWindowTitle("Opening %s" % self.malware_title)
            messagebox.exec()

    def Reload(self):
        self.inserter.QueueItems("exploit",self.Exploit_Table)
        self.inserter.QueueItems("malware",self.Malware_Table)
        self.inserter.QueueItems("cve", self.cve_table.tableWidget)

if __name__ == '__main__':
    App = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    main.ConnectToDB()
    App.exec_()
    App.exit()
