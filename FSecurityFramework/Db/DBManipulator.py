#!/usr/bin/python3

import os
import shutil
import pathlib
import mysql.connector
import json
import base64
from Core import CoreLoadConfig
from Core import CoreException
import ExpUpload
import MalwareUploadDialog
import CVEUpload
import copy
from PyQt5.QtWidgets import QTableWidgetItem

class DBConnector:
    """
        Class use to connect to database server.
    """
    def __init__(self,LogBrowser=None):
        self.db_connection = None
        self.cursor_connection_status = False
        self.db_config = CoreLoadConfig.ConfigHandler.getDBConfig()
        self.db_credentials = None
        self.db_cred_status = False
        self.LogBrowser = LogBrowser
        self.server_alive = False

    def DecodePassword(self):
        if self.db_cred_status == False or self.db_cred_status is False:
            if CoreLoadConfig.ConfigHandler.CheckLogBrowser(self.LogBrowser):
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Database configuration should be parse first")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Database configuration should be parse first", self.LogBrowser)
            return self.db_cred_status 
        self.db_credentials['password'] = base64.b64decode(self.db_credentials['password'])
        
    def ParseDBConfig(self):
        try:
            with open(self.db_config,'r') as fp:
                self.db_credentials = json.load(fp)
        except FileNotFoundError as FNError:
            if CoreLoadConfig.ConfigHandler.CheckLogBrowser(self.LogBrowser):
                CoreLoadConfig.ConfigHandler.ErrorWrite("Error: %s" % FNError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Error: %s" % FNError,self.LogBrowser)
            self.db_cred_status = False
        self.db_cred_status = True

    def ChangeHost(self, host=None):
        """
            @Args: host
            @return: True or False
        """
        if host is None or host == None:
            return False
        self.db_credentials['host'] = host
        return True

    def ChangePort(self, port=None):
        """
            @Args: port
            @return: True or False
        """
        if port is None or port == None:
            return False
        self.db_credentials['port'] = port
        return True

    def getDBConnectionStatus(self):
        return self.cursor_connection_status

    def ConnectDatabase(self):
        
        if self.db_cred_status == False or self.db_cred_status is False:
            if CoreLoadConfig.ConfigHandler.CheckLogBrowser(self.LogBrowser):
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Database configuration should be parse first")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Database configuration should be parse first",self.LogBrowser)
            return self.cursor_connection_status

        else:
            try:
                self.db_connection = mysql.connector.connect(**self.db_credentials)
            except mysql.connector.Error as err:
                if CoreLoadConfig.ConfigHandler.CheckLogBrowser(self.LogBrowser):
                    CoreLoadConfig.ConfigHandler.ErrorWriteLogger(err)
                else:
                    CoreLoadConfig.ConfigHandler.ErrorWriteLogger(err,self.LogBrowser)
                if err.errno == mysql.connector.errorcode.CR_CONNECTION_ERROR:
                    if CoreLoadConfig.ConfigHandler.CheckLogBrowser(self.LogBrowser):
                        CoreLoadConfig.ConfigHandler.ErrorWriteLogger("%s Database Connection error" % mysql.connector.errorcode.CR_CONNECTION_ERROR)
                    else:
                        CoreLoadConfig.ConfigHandler.ErrorWriteLogger("%s Database Connection error" % mysql.connector.errorcode.CR_CONNECTION_ERROR,self.LogBrowser)   
                    self.cursor_connection_status = False

            except mysql.connector.InterfaceError as Ie:
                if CoreLoadConfig.ConfigHandler.CheckLogBrowser(self.LogBrowser):
                    CoreLoadConfig.ConfigHandler.ErrorWriteLogger(Ie)
                else:
                    CoreLoadConfig.ConfigHandler.ErrorWriteLogger(err,self.LogBrowser)
                    if CoreLoadConfig.ConfigHandler.CheckLogBrowser(self.LogBrowser):
                        CoreLoadConfig.ConfigHandler.ErrorWriteLogger("%s Database Connection error" % Ie)
                    else:
                        CoreLoadConfig.ConfigHandler.ErrorWriteLogger("%s Database Connection error" % Ie,self.LogBrowser)   
                    self.cursor_connection_status = False

            self.cursor_connection_status = True
            if CoreLoadConfig.ConfigHandler.CheckLogBrowser(self.LogBrowser):
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("Database Connected")
            else:
                CoreLoadConfig.ConfigHandler.AccessWriteLogger("Database Connected",self.LogBrowser)
            return self.cursor_connection_status
    
    def getCursor(self):
        if self.cursor_connection_status == False or self.cursor_connection_status is False:
            if CoreLoadConfig.ConfigHandler.CheckLogBrowser(self.LogBrowser):
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Database Connection error")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Database Connection error",self.LogBrowser)
            raise CoreException.DatabaseConnectionError("Database Connection Error")
            return False
            
        return self.db_connection.cursor()

    def getDBObject(self):
        return self.db_connection

    def CommitChanges(self):
        self.db_connection.commit()

    def RollbackChanges(self):
        self.db_connection.rollback()

    def useDefaultConnection(self):
        self.ParseDBConfig()
        self.DecodePassword()
        self.ConnectDatabase()

    def Ping(self, attempts=1):
        try:
            self.db_connection.ping(attempts)
            self.server_alive=True
        except mysql.connector.errors.InterfaceError as IE:
            self.server_alive=False
    
    def ServerAlive(self):
        if self.server_alive:
            return True
        else:
            return False


class SqlQueries(DBConnector):
    def __init__(self, LogBrowser=None):
        """
            @Args: LogBrowser to insert active logs.
            @Description:  
        """
        self.LogBrowser = LogBrowser
        super(SqlQueries,self).__init__(LogBrowser)
        self.exploit_data = None
        self.cve_data = None
        self.malware_data = None
        self.last_inserted_id = None
        self.db_cursor = None
        self.current_exploit_id = None
        self.current_module_id = None
        self.current_malware_id = None
        self.current_auxiliary_id = None
        self.current_cve_id = None
        self.exploit_upload_status = False
        self.malware_upload_status = False
        self.cve_upload_status = False
        self.default_connection = True # If the default connection will be used.
        self.total_available_exploits = None
        self.total_available_malware = None
        self.total_available_cve = None
        
        # Named Placeholders is used. Because Exploit Data Dictionary is non-sorted sequence.
        # And Named Placeholders is helpful in this kind of situation.
        self.total_query = """ SELECT COUNT(*) FROM %s """
        self.insert_platform_query = """ INSERT INTO Platform(Name, Version, Arch, {UPLOAD_TYPE_ID}) VALUES({Name}, {Version} ,{Arch}, @ID) """
        self.last_insert = "SELECT LAST_INSERT_ID() INTO @ID;"
        self.insert_exploit_query = """ INSERT INTO Exploit(Title,Description,Type,Ratings,Exploit_Author) Values({Title}, {Description}, {Ratings}, {Type}, {Exploit_Author}) """
        self.insert_malware_query = "INSERT INTO Malware(Title,Description,Type,Ratings,Malware_Author) Values({Title}, {Description}, {Ratings}, {Type}, {Malware_Author})"
        self.insert_cve_query = """
             INSERT INTO CVE(Title,Description,Documentation,CVE_Author) 
             Values({Title},{Description},{Documentation}, {CVE_Author})
        """
        self.insert_cve_platform_query = """ INSERT INTO Platform(Name, Version, CVE_ID) VALUES({Name}, {Version}, @ID) """
        self.count_total_values_query = """ SELECT COUNT(*) FROM %s"""
        self.request_malware_query = """ SELECT Malware.MW_ID, Title, Description, Name, Version, Arch, Language, module_name, option_name,Type, Date, Ratings, Malware_Author FROM Malware 
                                        INNER JOIN Platform ON Malware.MW_ID = Platform.MW_ID 
                                        INNER JOIN Module ON Malware.MW_ID = Module.MW_ID INNER JOIN Options ON Malware.MW_ID = Options.MW_ID
                                     """

        self.request_cve_query = """ SELECT CVE.CVE_ID,Title, Description, Name, Version, CVE_Author, Documentation FROM CVE
                                     INNER JOIN Platform ON CVE.CVE_ID = Platform.CVE_ID """

        self.request_exploit_query = """ SELECT Exploit.EXP_ID, Title, Description, Name, Version, Arch, Language, module_name, option_name, Type, Date, Ratings, Exploit_Author FROM Exploit
                                         INNER JOIN Platform ON Exploit.EXP_ID = Platform.EXP_ID INNER JOIN Module ON Exploit.EXP_ID = Module.EXP_ID
                                         INNER JOIN Options ON Exploit.EXP_ID = Options.EXP_ID
                                     """
        
        self.insert_module_query = "INSERT INTO Module({UPLOAD_TYPE_ID},module_name) Values(@ID,{module_name})"
        self.insert_option_query = "INSERT INTO Options({UPLOAD_TYPE_ID},option_name) Values(@ID,{option_name})"

    def ConnectDB(self,host=None,port=None,default=True):
        self.default_connection = default
        if self.default_connection:
            self.useDefaultConnection()
            self.db_cursor = self.getCursor()
        else:
            if host == None or host is None and port == None or port is None:
                raise CoreException.DatabaseConnectionArgumentError("Host and Port must be specified if the default connection is set to False")
            else:
                self.ChangeHost(host)
                self.ChangePort(port)
                self.db_cursor = self.getCursor()

    def getLastInsertID(self):
        connection_status = self.getDBConnectionStatus()
        if connection_status == False or connection_status is False:
            return False
        statement = "SELECT LAST_INSERT_ID()"
        self.db_cursor.execute(statement)
        for value in self.db_cursor:
            self.last_inserted_id = value[0]
        if self.last_inserted_id is None or self.last_inserted_id == None:
            return False
        
        return int(self.last_inserted_id)

    def saveExploit(self,exploit_data=None):
        connection_status = self.getDBConnectionStatus()
        self.exploit_data = exploit_data
        if connection_status == False or connection_status is False:
            raise CoreException.DatabaseConnectionError("Not Connected to the database")
            self.exploit_upload_status = False
            return False
        
        #   Assign to temporary dictionary.
        #   When using formatting string. like str.format_map(dictionary)
        #   the inserted values or formatted value should be prefix and suffix with a \' single character set.
        #   Because when it was formatted into a string and executed in a SQL statement the following values will
        #   be read as a word not a string character.        
        #   There is more than one try, except clause below the code here.
        #   To program some sort of data integrity. and capture any possible and any unhandled exception. 
        #   To avoid incorrectly upload data in the database.
        #   and it is okay not to delete the current temporary data. Because the query uses a named placeholders.
        #   so it will not raise an overloaded parameter error.
        #   And in python3 dictionary.format(**dictionary_data) will raise an error. To use it correctly use dictionary.format_map() 

        try:
            self.db_cursor.execute(self.insert_exploit_query.format_map(self.exploit_data))
            self.CommitChanges()
        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to exploit table: Cause --> %s" % ProgramError)
                self.exploit_upload_status = False
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to exploit table: Cause --> %s" % ProgramError,self.LogBrowser)
                self.exploit_upload_status = False
                return False

        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to exploit table: Cause --> %s" % Ie)
                self.exploit_upload_status = False
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to exploit table: Cause --> %s" % Ie,self.LogBrowser)
                self.exploit_upload_status = False
                return False
        
        try:
            self.db_cursor.execute(self.last_insert)
            self.db_cursor.execute(self.insert_platform_query.format_map(self.exploit_data))
            self.CommitChanges()
        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to platform table: Cause --> %s" % ProgramError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to platform table: Cause --> %s" % ProgramError,self.LogBrowser)
            return False

        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to platform table: Cause --> %s" % Ie)
                self.exploit_upload_status = False
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to platform table: Cause --> %s" % Ie,self.LogBrowser)
                self.exploit_upload_status = False
                return False

        except:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to platform table")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to platform table",self.LogBrowser)

            return False

        try:
            CoreLoadConfig.ConfigHandler.saveFileToDir(identity="exploit", attack_data=self.exploit_data)
            self.exploit_data['module_name'] = "\"" + CoreLoadConfig.ConfigHandler.getExploitDir() + os.path.basename(self.exploit_data['module_name']).split("\"")[0] + "\""
            self.exploit_data['option_name'] = "\"" + CoreLoadConfig.ConfigHandler.getModuleConfig() + os.path.basename(self.exploit_data['option_name']).split("\"")[0] + "\""

        except CoreException.ParameterError as ParamError:
            if self.LogBrowser is None or self.LogBrowser == None:
                    CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Parameter on saving to specified directory: Cause --> %s" % ParamError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Parameter on saving to specified directory: Cause --> %s" % ParamError,self.LogBrowser)
            self.RollbackChanges()
        try:
            self.db_cursor.execute(self.insert_module_query.format_map(self.exploit_data))
            self.CommitChanges()
        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to module table: Cause --> %s" % ProgramError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to module table: Cause --> %s" % ProgramError,self.LogBrowser)
            self.exploit_upload_status = False
            self.RollbackChanges()
            return False

        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to module table: Cause --> %s" % Ie)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to module table: Cause --> %s" % Ie,self.LogBrowser)
            self.exploit_upload_status = False
            self.RollbackChanges()
            return False

        except:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to module table")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to module table",self.LogBrowser)
            self.exploit_upload_status = False
            self.RollbackChanges()
            return False
        try:
            self.db_cursor.execute(self.insert_option_query.format_map(self.exploit_data))
            self.CommitChanges()
        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to option table: Cause --> %s" % ProgramError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to option table: Cause --> %s" % ProgramError,self.LogBrowser)
            self.exploit_upload_status = False
            self.RollbackChanges()
            return False

        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to option table: Cause --> %s" % Ie)
            
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to option table: Cause --> %s" % Ie,self.LogBrowser)
            self.exploit_upload_status = False
            self.RollbackChanges()
            return False


        except:
            if self.LogBrowser is None or self.LogBrowser == None:
                    CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to option table")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to option table",self.LogBrowser) 

        self.CommitChanges()
        self.exploit_data = { }
        self.exploit_upload_status = True
                    
    def getExploitUploadStatus(self):
        return self.exploit_upload_status        
    
    def saveMalware(self,malware_data=None):
        connection_status = self.getDBConnectionStatus()
        self.malware_data = malware_data
        if connection_status == False or connection_status is False:
            raise CoreException.DatabaseConnectionError("Not Connected to the database")
            self.malware_upload_status = False
            return False
        
        #   Assign to temporary dictionary.
        #   When using formatting string. like str.format_map(dictionary)
        #   the inserted values or formatted value should be prefix and suffix with a \' single character set.
        #   Because when it was formatted into a string and executed in a SQL statement the following values will
        #   be read as a word not a string character.
        temp_data = { }
        temp_data['UPLOAD_TYPE_ID'] = self.malware_data['UPLOAD_TYPE_ID']
        temp_data['Title'] = self.malware_data['Title']
        temp_data['Description'] = self.malware_data['Description']
        temp_data['Ratings'] = self.malware_data['Ratings']
        temp_data['Type'] = self.malware_data['Type']
        temp_data['Malware_Author'] = self.malware_data['Malware_Author']
        
        # There is more than one try, except clause below the code here.
        # To program some sort of data integrity. and capture any possible and any unhandled exception. 
        # To avoid incorrectly upload data in the database.
        # and it is okay not to delete the current temporary data. Because the query uses a named placeholders.
        # so it will not raise an overloaded parameter error.
        # And in python3 dictionary.format(**dictionary_data) will raise an error. To use it correctly use dictionary.format_map() 

        try:
            self.db_cursor.execute(self.insert_malware_query.format_map(self.malware_data))
            self.CommitChanges()
        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to malware table: Cause --> %s" % ProgramError)
                self.malware_upload_status = False
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to malware table: Cause --> %s" % ProgramError,self.LogBrowser)
                self.malware_upload_status = False
                return False

        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to malware table: Cause --> %s" % Ie)
                self.malware_upload_status = False
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to malware table: Cause --> %s" % Ie,self.LogBrowser)
                self.malware_upload_status = False
                return False

       # except:
        #    if self.LogBrowser is None or self.LogBrowser == None:
       #         CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to malware table")
        #    else:
        #        CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to malware table",self.LogBrowser)
        
        self.current_malware_id = int(self.getLastInsertID())
        temp_data['ID'] = self.current_malware_id
        temp_data['Name'] = self.malware_data['Name']
        temp_data['Version'] = self.malware_data['Version']
        temp_data['Arch'] = self.malware_data['Arch']
        
        try:
            self.db_cursor.execute(self.last_insert)
            self.db_cursor.execute(self.insert_platform_query.format_map(self.malware_data))
            self.CommitChanges()
        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to platform table: Cause --> %s" % ProgramError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to platform table: Cause --> %s" % ProgramError,self.LogBrowser)
            return False

        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to platform table: Cause --> %s" % Ie)
                self.malware_upload_status = False
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to platform table: Cause --> %s" % Ie,self.LogBrowser)
                self.malware_upload_status = False
                return False

        except:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to platform table")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to platform table",self.LogBrowser)

            return False
        try:
            CoreLoadConfig.ConfigHandler.saveFileToDir(identity="malware", attack_data=self.malware_data)
            self.malware_data['module_name'] = "\"" + CoreLoadConfig.ConfigHandler.getMalwareDir() + os.path.basename(self.malware_data['module_name']).split("\"")[0] + "\""
            self.malware_data['option_name'] = "\"" + CoreLoadConfig.ConfigHandler.getModuleConfig() + os.path.basename(self.malware_data['option_name']).split("\"")[0] + "\""

        except CoreException.ParameterError as ParamError:
            if self.LogBrowser is None or self.LogBrowser == None:
                    CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Parameter on saving to specified directory: Cause --> %s" % ParamError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Parameter on saving to specified directory: Cause --> %s" % ParamError,self.LogBrowser)
            self.RollbackChanges()
        

        temp_data['module_name'] = self.malware_data['module_name']
        try:
            self.db_cursor.execute(self.insert_module_query.format_map(self.malware_data))
            self.CommitChanges()
        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to module table: Cause --> %s" % ProgramError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to module table: Cause --> %s" % ProgramError,self.LogBrowser)
            return False
        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to module table: Cause --> %s" % Ie)
                self.malware_upload_status = False
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to module table: Cause --> %s" % Ie,self.LogBrowser)
                self.malware_upload_status = False
                return False

        except:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to module table")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to module table",self.LogBrowser)
            return False
        temp_data['option_name'] = self.malware_data['option_name']
        try:
            self.db_cursor.execute(self.insert_option_query.format_map(self.malware_data))
            self.CommitChanges()
        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to option table: Cause --> %s" % ProgramError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to option table: Cause --> %s" % ProgramError,self.LogBrowser)

        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to option table: Cause --> %s" % Ie)
                self.malware_upload_status = False
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to option table: Cause --> %s" % Ie,self.LogBrowser)
                self.malware_upload_status = False
                return False

        except:
            if self.LogBrowser is None or self.LogBrowser == None:
                    CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to option table")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to option table",self.LogBrowser) 

        self.CommitChanges()
        self.malware_data = { } #empty the malware data incase of another insertion.
        self.malware_upload_status = True
                    
    def getMalwareUploadStatus(self):
        return self.malware_upload_status

    def saveCVE(self,cve_data=None):
        """
            @Description: Uploads the current cve documentation and some sort of required data to 
                          identify potential vulnerabilities.

            @Args: cve_data dictionary.
            @Return: cve_upload_status
        """
        connection_status = self.getDBConnectionStatus()
        self.cve_data = cve_data
        if connection_status == False or connection_status is False:
            raise CoreException.DatabaseConnectionError("Not Connected to the database")
            self.cve_upload_status = False
            return False
        
        #   Assign to temporary dictionary.
        #   When using formatting string. like str.format_map(dictionary)
        #   the inserted values or formatted value should be prefix and suffix with a \' single character set.
        #   Because when it was formatted into a string and executed in a SQL statement the following values will
        #   be read as a word not a string character.        
        # There is more than one try, except clause below the code here.
        # To program some sort of data integrity. and capture any possible and any unhandled exception. 
        # To avoid incorrectly upload data in the database.
        # and it is okay not to delete the current temporary data. Because the query uses a named placeholders.
        # so it will not raise an overloaded parameter error.
        # And in python3 dictionary.format(**dictionary_data) will raise an error. To use it correctly use dictionary.format_map() 

        try:
            CoreLoadConfig.ConfigHandler.saveFileToDir("cve",attack_data=self.cve_data)
            self.cve_data['Documentation'] = "\"" + CoreLoadConfig.ConfigHandler.getCVEDocumentDir() + os.path.basename(self.cve_data['Documentation']).split("\"")[0] + "\""
            self.db_cursor.execute(self.insert_cve_query.format_map(self.cve_data))
            self.CommitChanges()

        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to cve table: Cause --> %s" % ProgramError)
                self.cve_upload_status = False
                self.RollbackChanges()
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to cve table: Cause --> %s" % ProgramError,self.LogBrowser)
                self.cve_upload_status = False
                self.RollbackChanges()
                return False

        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to cve table: Cause --> %s" % Ie)
                self.cve_upload_status = False
                self.RollbackChanges()
                return False
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to cve table: Cause --> %s" % Ie,self.LogBrowser)
                self.cve_upload_status = False
                self.RollbackChanges()
                return False
        
        try:
            self.db_cursor.execute(self.last_insert)
            self.db_cursor.execute(self.insert_cve_platform_query.format_map(self.cve_data))
            self.CommitChanges()
        except mysql.connector.errors.ProgrammingError as ProgramError:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to platform table: Cause --> %s" % ProgramError)
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Programming Error on inserting to platform table: Cause --> %s" % ProgramError,self.LogBrowser)
            self.cve_upload_status = False
            self.RollbackChanges()
            return False

        except mysql.connector.errors.InterfaceError as Ie:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to platform table: Cause --> %s" % Ie)
             
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Interface Error on inserting to platform table: Cause --> %s" % Ie,self.LogBrowser)
            self.cve_upload_status = False
            self.RollbackChanges()
            return False

        except:
            if self.LogBrowser is None or self.LogBrowser == None:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to platform table")
            else:
                CoreLoadConfig.ConfigHandler.ErrorWriteLogger("Unhandled Exception on inserting to platform table",self.LogBrowser)
            self.RollbackChanges()
            return False
 
        self.CommitChanges()
        self.cve_data = { } #clear the cve data incase of another insertion.
        self.cve_upload_status = True
    
    def getCVEUploadStatus(self):
        return self.cve_upload_status

    def getTotalExploitCount(self):
        """ Return Total Exploits. """
        self.Ping(5)
        if self.ServerAlive:
            exploit_string = "Exploit"
            self.db_cursor.execute(self.total_query % exploit_string)
            total = self.db_cursor.fetchall()
            self.total_available_exploits = total[0]
            return int(self.total_available_exploits[0])
    
    def getExploitQuery(self):
        self.Ping(5) # Ping the server. Then sets self.ServerAlive = True if the database server is alive.
        if self.ServerAlive: # Check if the database server is alive.
            # To avoid the same result when other cursor values is change.
            # Format: EXP_ID,Title,Description,Name,Language,module_name,Type,Date,Ratings,Exploit_Author
            self.db_cursor.execute(self.request_exploit_query)
            sequence = self.db_cursor.fetchone()
            item_counter = 0
            while sequence is not None: 
               temp = []
               for index,value in enumerate(sequence):
                   temp.insert(index,value)
               sequence = self.db_cursor.fetchone()
               yield temp

    def getTotalMalwareCount(self):
        """ Return Total Malware. """
        self.Ping(5)
        if self.ServerAlive:
            malware_string = "Malware"
            self.db_cursor.execute(self.total_query % malware_string)
            total = self.db_cursor.fetchall()
            self.total_available_malware = total[0]
            return int(self.total_available_malware[0])

    def getMalwareQuery(self):
        self.Ping(5) # Ping the server. Then sets self.ServerAlive = True if the database server is alive.
        if self.ServerAlive: # Check if the database server is alive.
            # To avoid the same result when other cursor values is change.
            # Format: MW_ID,Title,Description,Name,Language,module_name,Type,Date,Ratings,Malware_Author
            self.db_cursor.execute(self.request_malware_query)
            sequence = self.db_cursor.fetchone()
            item_counter = 0
            while sequence is not None: 
               temp = []
               for index,value in enumerate(sequence):
                   temp.insert(index,value)
               sequence = self.db_cursor.fetchone()
               yield temp
                # return an iterator or generator object.

    def getTotalCVECount(self):
        """ Return Total CVE. """
        self.Ping(5)
        if self.ServerAlive:
            CVE_string = "CVE"
            self.db_cursor.execute(self.total_query % CVE_string)
            total = self.db_cursor.fetchall()
            self.total_available_cve = total[0]
            return int(self.total_available_cve[0])

    def getCVEQuery(self):
        self.Ping(5) # Ping the server. Then sets self.ServerAlive = True if the database server is alive.
        if self.ServerAlive: # Check if the database server is alive.
            # To avoid the same result when other cursor values is change.
            # Format: CVE_ID, Title, Description, Name, CVE_Author, Documentation.
            self.db_cursor.execute(self.request_cve_query)
            sequence = self.db_cursor.fetchone()
            item_counter = 0
            while sequence is not None: 
               temp = []
               for index,value in enumerate(sequence):
                   temp.insert(index,value)
               sequence = self.db_cursor.fetchone()
               yield temp
                
            # return an iterator or generator object.
if __name__ == '__main__':
    anon = SqlQueries()