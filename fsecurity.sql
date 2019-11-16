-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: fsecurityframework
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CVE`
--
CREATE DATABASE IF NOT EXISTS FSecurityFramework;
USE FSecurityFramework;
DROP TABLE IF EXISTS `CVE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CVE` (
  `CVE_ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Title` varchar(45) NOT NULL,
  `Description` longtext,
  `CVE_Author` varchar(100) NOT NULL DEFAULT 'Alfred Valderrama',
  `Documentation` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`CVE_ID`),
  UNIQUE KEY `CVE_ID_UNIQUE` (`CVE_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CVE`
--

LOCK TABLES `CVE` WRITE;
/*!40000 ALTER TABLE `CVE` DISABLE KEYS */;
INSERT INTO `CVE` VALUES (1,'Samsung Galaxy S6','The attached file causes memory corruption when iy is scanned by the face recognition library in android.media.process\n\nProof of Concept:\nhttps://github.com/offensive-security/exploit-database-bin-sploits/raw/master/bin-sploits/39425.zip','Offensive Security Note: No Email Provided','Attacks/cve/Samsung_Galaxy_S6.txt'),(2,'Local Denial of Service','Linux Kernel - \'ping\' Local Denial of Service','https://raw.githubusercontent.com/danieljiang0415/android_kernel_crash_poc/master/panic.c','Attacks/cve/Linux_Kernel_DOS.txt'),(3,'File Integer Overflow','Google Android Web Browser - \'.BMP\' File Integer Overflow','Source:  http://www.securityfocus.com/bid/28006/info','Attacks/cve/Google_Android_Web_Browser.txt'),(4,'Arbitrary JavaScript Execution','Adobe Reader for Android 11.1.3 - Arbitrary JavaScript Execution\n------------------------------------------------------------------------\nReferences\n------------------------------------------------------------------------\n[1]\nhttp://www.securify.nl/advisory/SFY20140401/adobe_reader_for_android_exposes_insecure_javascript_interfaces.html\n[2] https://play.google.com/store/apps/details?id=com.adobe.reader\n[3]\nhttp://developer.android.com/reference/android/webkit/JavascriptInterface.html\n[4]\nhttp://www.adobe.com/devnet-docs/acrobatetk/tools/Mobile/js.html#supported-javascript-apis\n[5] http://www.securify.nl/advisory/SFY20140401/mobilereader.poc.pdf\n\n','Yorick Koster','Attacks/cve/Adobe_Reader_For_Android.txt'),(5,'New TTY Privilege Level To 15','Cisco IOS - New TTY / Privilege Level To 15 / No Password Shellcode','Gyan Chawdhary','Attacks/cve/Cisco_IOS.txt'),(6,'/bin/shShellcode (141 bytes)','Shellcode execute execve /bin/sh en Irix/mips, Linux/x86, Unix/sparc by dymitr1\ndymitri666@hotmail.com\n\n','dymitri666@hotmail.com','Attacks/cve/Linux-shellcode-execve.txt');
/*!40000 ALTER TABLE `CVE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Exploit`
--

DROP TABLE IF EXISTS `Exploit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Exploit` (
  `EXP_ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Title` varchar(100) NOT NULL,
  `Description` varchar(500) NOT NULL DEFAULT 'No Description',
  `Language` varchar(45) NOT NULL DEFAULT 'Unknown',
  `Type` varchar(100) NOT NULL DEFAULT 'Local',
  `Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Ratings` varchar(100) NOT NULL DEFAULT 'Low',
  `Exploit_Author` varchar(100) NOT NULL DEFAULT 'Alfred Valderrama',
  PRIMARY KEY (`EXP_ID`),
  UNIQUE KEY `EXP_ID_UNIQUE` (`EXP_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Exploit`
--

LOCK TABLES `Exploit` WRITE;
/*!40000 ALTER TABLE `Exploit` DISABLE KEYS */;
INSERT INTO `Exploit` VALUES (1,'Adobe Embedded EXE File format exploit','This exploit Adobe Embedded EXE File format exploit is use to trick the user to run a malware into it.','Unknown','Good','2019-08-05 08:12:20','Remote','alfred98valderrama@gmail.com'),(2,'Android Exploit using TCP Connection','This exploit targets android device that will send back a command interpreter to the attacker. It can capture live webcam, send_sms, dump call logs, etc.','Unknown','Good','2019-08-05 08:14:24','Remote','alfred98valderrama@gmail.com'),(3,'ETERNALBLUE SMB buffer overflow','this type of exploit ETERNALBLUE SMB buffer overflow will corrupt the memory then run a process called spoolv.exe. And take control of the system. But not fully controlled. It just exploiting the smb vulnerability of windows 7,8,10. Tested on Windows 7','Unknown','Good','2019-08-05 08:16:55','Remote','alfred98valderrama@gmail.com'),(4,'Apple Iphone Exploit','This exploit will create a  webserver and generate a libtiff image file. and if the target downloaded it and open it. The corresponding command interpreter is launch and control the command shell of an iphone.','Unknown','Good','2019-08-05 08:19:24','Remote','alfred98valderrama@gmail.com'),(5,'Launch and Exploit the Powershell','Launch and Exploit the Powershell then run create a command interpreter.','Unknown','Good','2019-08-05 08:21:12','Remote','alfred98valderrama@gmail.com'),(6,'Ransomware Targeting Windows system','This is an example ransomware and this ransomware will encrypt all the files of the active user. And asking for bitcoin.','Unknown','Great','2019-08-05 08:23:49','Remote','alfred98valderrama@gmail.com'),(7,'Windows Exploits','Windows Exploits','Unknown','Good','2019-08-05 10:06:14','Remote','alfred98valderrama@gmail.com');
/*!40000 ALTER TABLE `Exploit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Malware`
--

DROP TABLE IF EXISTS `Malware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Malware` (
  `MW_ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Title` varchar(100) NOT NULL,
  `Description` varchar(500) DEFAULT 'No Description',
  `Language` varchar(200) DEFAULT 'Unknown',
  `Type` varchar(100) DEFAULT 'Local',
  `Date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Ratings` varchar(100) DEFAULT 'Low',
  `Malware_Author` varchar(100) DEFAULT 'Alfred Valderrama',
  PRIMARY KEY (`MW_ID`),
  UNIQUE KEY `MW_ID_UNIQUE` (`MW_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Malware`
--

LOCK TABLES `Malware` WRITE;
/*!40000 ALTER TABLE `Malware` DISABLE KEYS */;
INSERT INTO `Malware` VALUES (1,'Android Shell Malware','Android Shell Malware','Unknown','Good','2019-08-05 10:09:52','Remote','alfred98valderrama@gmail.com'),(2,'Download Malware and Execute','Download Malware and Execute','Unknown','Good','2019-08-05 10:10:42','Remote','alfred98valderrama@gmail.com'),(3,'MacOSX Malware and established a connection over tcp','MacOSX Malware and established a connection over tcp. The output may be a MacOSX .app Files. Then if the user executes it. Ka-Booom!','Unknown','Great','2019-08-05 14:53:45','Remote','alfred98valderrama@gmail.com'),(4,'MacOS Malware established a TCP connection','This malware only supports 32-bit Macintosh system.','Unknown','Great','2019-08-05 14:55:05','Remote','alfred98valderrama@gmail.com'),(5,'Windows CMD RAT over TCP','Windows CMD RAT over TCP and interpret a commands and connect back to attacker.','Unknown','Great','2019-08-05 14:56:08','Remote','alfred98valderrama@gmail.com'),(6,'MS Windows CMD RAT','MS Windows CMD RAT. This malware only supports 32-bit windows system.','Unknown','Great','2019-08-05 14:57:14','Remote','alfred98valderrama@gmail.com'),(7,'Mac OS Power PC Malware meterpreter','Mac OS Power PC Malware meterpreter','Unknown','Great','2019-08-05 14:58:31','Remote','alfred98valderrama@gmail.com'),(8,'Windows Spyware','This malware can be the desktop session of the victims PC. And can be remotely used a mouse and a keyboard.','Unknown','Great','2019-08-05 15:00:05','Remote','alfred98valderrama@gmail.com'),(9,'Spy Windows Malware','This malware can be the desktop session of the victims PC. And can be remotely used a mouse and a keyboard. And this malware only supports 32-bit windows system. And can be detectable into updated anti-virus software','Unknown','Good','2019-08-05 15:01:14','Remote','alfred98valderrama@gmail.com'),(10,'Spy Windows Malware over HTTP Connection','This malware can be the desktop session of the victims PC. And can be remotely used a mouse and a keyboard. And this malware only supports 32-bit windows system. And can be detectable into updated anti-virus software. and established a connection by using HTTP protocol.','Unknown','Good','2019-08-05 15:02:13','Remote','alfred98valderrama@gmail.com');
/*!40000 ALTER TABLE `Malware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Module`
--

DROP TABLE IF EXISTS `Module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Module` (
  `MOD_ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `EXP_ID` int(10) unsigned DEFAULT NULL,
  `MW_ID` int(10) unsigned DEFAULT NULL,
  `module_name` varchar(500) NOT NULL DEFAULT 'Not Specified',
  PRIMARY KEY (`MOD_ID`),
  UNIQUE KEY `MOD_ID_UNIQUE` (`MOD_ID`),
  UNIQUE KEY `EXP_ID_UNIQUE` (`EXP_ID`),
  UNIQUE KEY `MW_ID_UNIQUE` (`MW_ID`),
  CONSTRAINT `fk_Module_Exploit` FOREIGN KEY (`EXP_ID`) REFERENCES `Exploit` (`EXP_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Module_Malware` FOREIGN KEY (`MW_ID`) REFERENCES `Malware` (`MW_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Module`
--

LOCK TABLES `Module` WRITE;
/*!40000 ALTER TABLE `Module` DISABLE KEYS */;
INSERT INTO `Module` VALUES (1,1,NULL,'Attacks/exploits/AdobeFileFormatx64.py'),(2,2,NULL,'Attacks/exploits/android_exploit_over_TCP.py'),(3,3,NULL,'Attacks/exploits/eternalblueSMBbufoverflow.py'),(4,4,NULL,'Attacks/exploits/IPhoneExploit.py'),(5,5,NULL,'Attacks/exploits/PowerShellExploit.py'),(6,6,NULL,'Attacks/exploits/WindowsWannaCryRansomware.py'),(7,7,NULL,'Attacks/exploits/Windowsx64ShellBindTCP.py'),(8,NULL,1,'Attacks/malwares/AndroidShellMalware.py'),(9,NULL,2,'Attacks/malwares/AutoDownloadMalwarex86.py'),(10,NULL,3,'Attacks/malwares/MacOSXMalwarex64_over_TCP.py'),(11,NULL,4,'Attacks/malwares/MacOSXShellMalwarex86.py'),(12,NULL,5,'Attacks/malwares/MicrosoftWindowsx64CmdRATOverTCP.py'),(13,NULL,6,'Attacks/malwares/MicrosoftWindowsx86CmdRatOverTCP.py'),(14,NULL,7,'Attacks/malwares/OSXPowerPCMalware.py'),(15,NULL,8,'Attacks/malwares/SpyWindowsx64OverTCP.py'),(16,NULL,9,'Attacks/malwares/SpyWindowsx86OverTCP.py'),(17,NULL,10,'Attacks/malwares/SpyWindowsx86OverHTTP.py');
/*!40000 ALTER TABLE `Module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Options`
--

DROP TABLE IF EXISTS `Options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Options` (
  `OPT_ID` int(11) NOT NULL AUTO_INCREMENT,
  `EXP_ID` int(10) unsigned DEFAULT NULL,
  `MW_ID` int(10) unsigned DEFAULT NULL,
  `option_name` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`OPT_ID`),
  UNIQUE KEY `OPT_ID_UNIQUE` (`OPT_ID`),
  UNIQUE KEY `EXP_ID_UNIQUE` (`EXP_ID`),
  UNIQUE KEY `MW_ID_UNIQUE` (`MW_ID`),
  CONSTRAINT `fk_Options_Exploit` FOREIGN KEY (`EXP_ID`) REFERENCES `Exploit` (`EXP_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Options_Malware` FOREIGN KEY (`MW_ID`) REFERENCES `Malware` (`MW_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Options`
--

LOCK TABLES `Options` WRITE;
/*!40000 ALTER TABLE `Options` DISABLE KEYS */;
INSERT INTO `Options` VALUES (1,1,NULL,'etc/fsecurity/module_config/AdobeFileFormatx64.json'),(2,2,NULL,'etc/fsecurity/module_config/android_exploit_over_TCP_config.json'),(3,3,NULL,'etc/fsecurity/module_config/eternalblueSMBbufoverflow.json'),(4,4,NULL,'etc/fsecurity/module_config/IPhoneExploit.json'),(5,5,NULL,'etc/fsecurity/module_config/PowerShellExploit.json'),(6,6,NULL,'etc/fsecurity/module_config/WindowsWannaCryRansomware.json'),(7,7,NULL,'etc/fsecurity/module_config/Windowsx64ShellBindTCP.json'),(8,NULL,1,'etc/fsecurity/module_config/AndroidShellMalware.json'),(9,NULL,2,'etc/fsecurity/module_config/AutoDownloadMalwarex86.json'),(10,NULL,3,'etc/fsecurity/module_config/MacOSXMalwarex64_over_TCP.json'),(11,NULL,4,'etc/fsecurity/module_config/MacOSXShellMalwarex86.json'),(12,NULL,5,'etc/fsecurity/module_config/MicroftWindowsx64CmdRATOverTCP.json'),(13,NULL,6,'etc/fsecurity/module_config/MicrosoftWindowsx86CmdRatOverTCP.json'),(14,NULL,7,'etc/fsecurity/module_config/OSXPowerPCMalware.json'),(15,NULL,8,'etc/fsecurity/module_config/SpyWindowsx64OverTCP.json'),(16,NULL,9,'etc/fsecurity/module_config/SpyWindowsx86OverTCP.json'),(17,NULL,10,'etc/fsecurity/module_config/SpyWindowsx86OverHTTP.json');
/*!40000 ALTER TABLE `Options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Platform`
--

DROP TABLE IF EXISTS `Platform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Platform` (
  `Platform_ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `EXP_ID` int(10) unsigned DEFAULT NULL,
  `MW_ID` int(10) unsigned DEFAULT NULL,
  `CVE_ID` int(10) unsigned DEFAULT NULL,
  `Name` varchar(45) NOT NULL DEFAULT 'Any Platform',
  `Version` varchar(45) NOT NULL DEFAULT 'Any Version',
  `Arch` enum('x86','x64','x86_64','ALL') NOT NULL DEFAULT 'ALL',
  PRIMARY KEY (`Platform_ID`),
  UNIQUE KEY `Platform_ID_UNIQUE` (`Platform_ID`),
  UNIQUE KEY `EXP_ID_UNIQUE` (`EXP_ID`),
  UNIQUE KEY `MW_ID_UNIQUE` (`MW_ID`),
  UNIQUE KEY `CVE_ID_UNIQUE` (`CVE_ID`),
  CONSTRAINT `fk_Platform_CVE` FOREIGN KEY (`CVE_ID`) REFERENCES `CVE` (`CVE_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Platform_Exploit` FOREIGN KEY (`EXP_ID`) REFERENCES `Exploit` (`EXP_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Platform_Malware` FOREIGN KEY (`MW_ID`) REFERENCES `Malware` (`MW_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Platform`
--

LOCK TABLES `Platform` WRITE;
/*!40000 ALTER TABLE `Platform` DISABLE KEYS */;
INSERT INTO `Platform` VALUES (1,1,NULL,NULL,'Adobe Reader','v8.x, v9.x','x86'),(2,2,NULL,NULL,'Android','Any Version','ALL'),(3,3,NULL,NULL,'Windows','7,8,10','x86_64'),(4,4,NULL,NULL,'Apple Iphone','4s,5s,6s','ALL'),(5,5,NULL,NULL,'Windows Powershell','7,8,10','x86'),(6,6,NULL,NULL,'Windows','7,8,10','x86'),(7,7,NULL,NULL,'Windows','7,8,10','x64'),(8,NULL,1,NULL,'Android','Any Version','x86_64'),(9,NULL,2,NULL,'Windows','7,8,10','x86'),(10,NULL,3,NULL,'MacOSX','Sierra and above.','x64'),(11,NULL,4,NULL,'MacOSX','Old MacOses','x86'),(12,NULL,5,NULL,'Microsoft Windows','7,8,10','x64'),(13,NULL,6,NULL,'Microsoft Windows','7,8,10','x86'),(14,NULL,7,NULL,'MacOS Power PC','Any Version','ALL'),(15,NULL,8,NULL,'Microsoft Windows','7,8,10','x64'),(16,NULL,9,NULL,'Microsoft Windows','7,8,10','x86'),(17,NULL,10,NULL,'Microsoft Windows','7,8,10','x86'),(18,NULL,NULL,1,'Android','Galaxy S6','ALL'),(19,NULL,NULL,2,'Android','Any Version','ALL'),(20,NULL,NULL,3,'Google Android Web Browser','Not Implemented','ALL'),(21,NULL,NULL,4,'Adobe Reader For android','Adobe Reader for android - 11.1.3','ALL'),(22,NULL,NULL,5,'Cisco IOS','C2600-IK9S-M','ALL'),(23,NULL,NULL,6,'Linux/x86','Not Implemented','ALL');
/*!40000 ALTER TABLE `Platform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'fsecurityframework'
--

--
-- Dumping routines for database 'fsecurityframework'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-08-08 21:14:01
