CREATE DATABASE  IF NOT EXISTS `kylin` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `kylin`;
-- MySQL dump 10.13  Distrib 5.6.23, for Win32 (x86)
--
-- Host: localhost    Database: kylin
-- ------------------------------------------------------
-- Server version	5.7.20-log

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
-- Table structure for table `acc_management`
--

DROP TABLE IF EXISTS `acc_management`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acc_management` (
  `acc_management_id` int(11) NOT NULL AUTO_INCREMENT,
  `acc_management_account` varchar(100) DEFAULT '',
  `acc_management_name` varchar(100) DEFAULT '',
  `acc_management_password` varchar(128) DEFAULT '',
  `acc_management_organization` varchar(100) DEFAULT '',
  `acc_management_email` varchar(100) DEFAULT '',
  `acc_management_phone` varchar(45) DEFAULT '',
  `acc_management_active` tinyint(2) DEFAULT '0',
  `acc_management_acc_deadline` varchar(45) DEFAULT '',
  `acc_management_org_manager` tinyint(2) DEFAULT '0',
  `acc_management_operate_date` datetime DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`acc_management_id`),
  KEY `role_id_idx` (`role_id`),
  CONSTRAINT `role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acc_management`
--

LOCK TABLES `acc_management` WRITE;
/*!40000 ALTER TABLE `acc_management` DISABLE KEYS */;
INSERT INTO `acc_management` VALUES (1,'Admin','System Administrator','YWRtaW4=','','Admin@foxconn.com','',1,'',0,'2018-04-14 16:23:26',1),(2,'Demo','demo','ZGVtbw==','Default Organization1','demo@gmail.com','0999999999',0,'',0,'2018-04-14 09:17:57',2),(3,'Scheduler','Scheduler','c2NoZWR1bGVy','','Scheduler@foxconn.com','',1,'',0,'2018-04-14 09:17:57',2),(4,'Supervisor','System Supervisor','c3VwZXJ2aXNvcg==','','Supervisor@foxconn.com','',0,'2018-03-13 ~ 2018-03-14',0,'2018-04-14 09:17:57',2),(5,'kyLin','kyLin','a3lMaW4xMjM0','Default Organization1','kyLin@foxconn.com','0912345678',1,'',0,'2018-04-20 11:39:25',1),(6,'t1','t1','dDE=','','t1@foxconn.com','12345655555',1,'2018-03-23 ~ 2018-04-01',1,'2018-04-14 09:17:57',2),(10,'t2','t2','dDI=','Default Organization1','T2@mail.ocm','1234567890',0,'2018-03-28 ~ 2018-03-29',1,'2018-04-14 09:17:57',3),(12,'t3','t3','dDM=','','T222@mail.ocm','',1,'',0,'2018-04-14 10:23:18',3);
/*!40000 ALTER TABLE `acc_management` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_device`
--

DROP TABLE IF EXISTS `event_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_device` (
  `event_device_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_device_level` varchar(45) DEFAULT '',
  `event_device_name` varchar(200) DEFAULT '',
  `event_device_description` varchar(250) DEFAULT '',
  `event_device_time` varchar(45) DEFAULT '',
  `event_device_action` varchar(250) DEFAULT '',
  PRIMARY KEY (`event_device_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_device`
--

LOCK TABLES `event_device` WRITE;
/*!40000 ALTER TABLE `event_device` DISABLE KEYS */;
INSERT INTO `event_device` VALUES (1,'middle','T2 Cooling container (................)','t2it2 Inrow4 (Disconnect)','2016-07-14 16:23:27','a');
/*!40000 ALTER TABLE `event_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_now`
--

DROP TABLE IF EXISTS `event_now`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_now` (
  `event_now_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_now_level` varchar(45) DEFAULT '',
  `event_now_name` varchar(200) DEFAULT '',
  `event_now_description` varchar(250) DEFAULT '',
  `event_now_time` varchar(45) DEFAULT '',
  `event_now_action` varchar(250) DEFAULT '',
  PRIMARY KEY (`event_now_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_now`
--

LOCK TABLES `event_now` WRITE;
/*!40000 ALTER TABLE `event_now` DISABLE KEYS */;
INSERT INTO `event_now` VALUES (1,'low','t2it2 Inrow4','t2it2 Inrow4 (Disconnect)','2016-07-14 16:23:27',''),(2,'middle','T2 power SNUPSO','t2power SBUPSO (Disconnect)','2016-07-14 16:23:27',''),(3,'high','T2 Cooling container 環控 (................)','漏水偵測5_lowCritical','2016-07-14 16:23:27','');
/*!40000 ALTER TABLE `event_now` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_system`
--

DROP TABLE IF EXISTS `event_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_system` (
  `event_system_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_system_level` varchar(45) DEFAULT '',
  `event_system_name` varchar(200) DEFAULT '',
  `event_system_description` varchar(250) DEFAULT '',
  `event_system_time` varchar(45) DEFAULT '',
  `event_system_action` varchar(250) DEFAULT '',
  PRIMARY KEY (`event_system_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_system`
--

LOCK TABLES `event_system` WRITE;
/*!40000 ALTER TABLE `event_system` DISABLE KEYS */;
INSERT INTO `event_system` VALUES (1,'middle','T2 power SNUPSO','t2power SBUPSO (Disconnect)','2016-07-14 16:23:27','');
/*!40000 ALTER TABLE `event_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_warning`
--

DROP TABLE IF EXISTS `event_warning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_warning` (
  `event_warning_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_warning_level` varchar(45) DEFAULT '',
  `event_warning_name` varchar(200) DEFAULT '',
  `event_warning_description` varchar(250) DEFAULT '',
  `event_warning_time` varchar(45) DEFAULT '',
  `event_warning_action` varchar(250) DEFAULT '',
  PRIMARY KEY (`event_warning_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_warning`
--

LOCK TABLES `event_warning` WRITE;
/*!40000 ALTER TABLE `event_warning` DISABLE KEYS */;
INSERT INTO `event_warning` VALUES (1,'low','t2it2 Inrow4','t2it2 Inrow4 (Disconnect)','2016-07-14 16:23:27','');
/*!40000 ALTER TABLE `event_warning` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `log_module` varchar(45) DEFAULT '',
  `log_level` varchar(45) DEFAULT '',
  `log_description` varchar(250) DEFAULT '',
  `log_date` datetime DEFAULT NULL,
  `log_source` varchar(45) DEFAULT '',
  `log_user_account` varchar(100) DEFAULT '',
  `log_user_org` varchar(100) DEFAULT '',
  PRIMARY KEY (`log_id`),
  KEY `log_account_idx` (`log_user_account`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
INSERT INTO `log` VALUES (1,'Account','INFO','Modify Demo account successfully.','2018-04-11 17:16:36','10.67.19.91','kyLin','Default Organization1'),(2,'Account','INFO','Modify Admin account successfully.','2018-04-11 17:17:39','10.67.19.91','kyLin','Default Organization1'),(3,'Role','INFO','modify Manager role successfully.','2018-04-11 17:21:48','10.67.19.91','kyLin','Default Organization1'),(4,'Account','INFO','Delete t2 account successfully.','2018-04-11 17:33:24','10.67.19.91','Admin',''),(5,'IPMI','INFO','Modify server192.168.1.121 IPMI successfully.','2018-04-11 17:34:17','10.67.19.91','Admin',''),(6,'Role','INFO','modify Manager role successfully.','2018-04-11 17:35:02','10.67.19.91','Admin',''),(7,'Account','INFO','Modify Demo account successfully.','2018-04-14 08:06:10','10.67.18.183','kyLin','Default Organization1'),(8,'Tank','INFO','Create Tank 2 successfully.','2018-04-18 14:22:42','10.67.18.216','kyLin','Default Organization1'),(9,'Tank','INFO','Create Tank3 successfully.','2018-04-18 14:28:03','10.67.18.216','kyLin','Default Organization1'),(10,'Tank','INFO','Modify Tank 3 successfully.','2018-04-18 14:47:28','10.67.18.216','kyLin','Default Organization1'),(11,'Tank','INFO','Modify Tank 3 successfully.','2018-04-18 14:51:26','10.67.18.216','kyLin','Default Organization1'),(12,'Tank','INFO','Modify Tank 3 successfully.','2018-04-18 14:52:00','10.67.18.216','kyLin','Default Organization1'),(13,'Tank','INFO','Modify Tank 1 successfully.','2018-04-18 14:54:05','10.67.18.216','kyLin','Default Organization1'),(14,'Role','INFO','modify Manager role successfully.','2018-04-18 14:55:37','10.67.18.216','kyLin','Default Organization1'),(15,'Role','INFO','modify Manager role successfully.','2018-04-18 14:58:06','10.67.18.216','kyLin','Default Organization1'),(16,'Role','INFO','modify Operator role successfully.','2018-04-18 14:58:38','10.67.18.216','kyLin','Default Organization1'),(17,'Role','INFO','modify Manager role successfully.','2018-04-18 15:00:35','10.67.18.216','kyLin','Default Organization1'),(18,'Tank','INFO','Modify Tank 3 successfully.','2018-04-18 15:07:16','10.67.18.216','kyLin','Default Organization1'),(19,'Tank','INFO','Delete Tank 3 tank successfully.','2018-04-18 15:16:21','10.67.18.216','kyLin','Default Organization1'),(20,'Tank','INFO','Add server 30:0e:d5:ca:c4:96 into tank Tank 1.','2018-04-18 17:09:46','10.67.18.216','kyLin','Default Organization1'),(21,'Tank','INFO','Add server E4:11:5B:12:c0:t2 into tank Tank 1.','2018-04-18 17:26:30','10.67.18.216','kyLin','Default Organization1'),(22,'Tank','INFO','Add server E4:11:5B:12:c0:t3 into tank Tank 1.','2018-04-18 17:26:30','10.67.18.216','kyLin','Default Organization1'),(23,'Tank','INFO','Delete server 30:0e:d5:ca:c4:96 from tank Tank 1.','2018-04-18 18:15:12','10.67.18.216','kyLin','Default Organization1'),(24,'Tank','INFO','Delete server E4:11:5B:12:c0:t2 from tank Tank 1.','2018-04-18 18:15:13','10.67.18.216','kyLin','Default Organization1'),(25,'Tank','INFO','Delete server E4:11:5B:12:c0:t3 from tank Tank 1.','2018-04-18 18:30:29','10.67.18.216','kyLin','Default Organization1'),(26,'Tank','INFO','Add server E4:11:5B:12:c0:t2 into tank Tank 1.','2018-04-18 18:32:16','10.67.18.216','kyLin','Default Organization1'),(27,'Tank','INFO','Add server E4:11:5B:12:c0:t3 into tank Tank 1.','2018-04-18 18:32:16','10.67.18.216','kyLin','Default Organization1'),(28,'Tank','INFO','Add server E4:11:5B:12:c0:t2 into tank Tank 2.','2018-04-18 18:32:35','10.67.18.216','kyLin','Default Organization1'),(29,'Tank','INFO','Add server E4:11:5B:12:c0:t3 into tank Tank 2.','2018-04-18 18:32:35','10.67.18.216','kyLin','Default Organization1'),(30,'Tank','INFO','Add server 30:0e:d5:ca:c4:96 into tank Tank 3.','2018-04-18 18:32:55','10.67.18.216','kyLin','Default Organization1'),(31,'Tank','INFO','Delete server E4:11:5B:12:c0:t2 from tank Tank 2.','2018-04-18 18:49:00','10.67.18.216','kyLin','Default Organization1'),(32,'Tank','INFO','Delete server E4:11:5B:12:c0:t3 from tank Tank 2.','2018-04-18 18:49:00','10.67.18.216','kyLin','Default Organization1'),(33,'Tank','INFO','Add server E4:11:5B:12:c0:t2 into tank Tank 1.','2018-04-18 18:55:49','10.67.18.216','kyLin','Default Organization1'),(34,'Tank','INFO','Add server E4:11:5B:12:c0:t3 into tank Tank 1.','2018-04-18 18:55:49','10.67.18.216','kyLin','Default Organization1'),(35,'Tank','INFO','Delete server E4:11:5B:12:c0:t2 from tank Tank 1.','2018-04-18 18:59:46','10.67.18.216','kyLin','Default Organization1'),(36,'Tank','INFO','Delete server E4:11:5B:12:c0:t3 from tank Tank 1.','2018-04-18 18:59:46','10.67.18.216','kyLin','Default Organization1'),(37,'Tank','INFO','Add server E4:11:5B:12:c0:t2 into tank Tank 1.','2018-04-18 19:00:16','10.67.18.216','kyLin','Default Organization1'),(38,'Tank','INFO','Add server E4:11:5B:12:c0:t3 into tank Tank 1.','2018-04-18 19:00:16','10.67.18.216','kyLin','Default Organization1'),(39,'Account','INFO','Create t4 account successfully.','2018-04-19 14:05:16','10.67.18.216','kyLin','Default Organization1'),(40,'Tank','INFO','Create T4 tank successfully.','2018-04-19 14:05:29','10.67.18.216','kyLin','Default Organization1'),(41,'Tank','INFO','Delete T4 tank successfully.','2018-04-19 14:05:40','10.67.18.216','kyLin','Default Organization1'),(44,'Tank','INFO','Delete server E4:11:5B:12:c0:t4 from tank Tank 1.','2018-04-19 14:21:30','10.67.18.216','kyLin','Default Organization1'),(45,'Tank','INFO','Modify server168.95.1.2 IPMI successfully.','2018-04-19 19:25:40','10.67.18.216','kyLin','Default Organization1'),(46,'Tank','INFO','Modify server168.95.1.3 IPMI successfully.','2018-04-19 19:25:47','10.67.18.216','kyLin','Default Organization1'),(47,'Tank','INFO','Modify server168.95.1.2 IPMI successfully.','2018-04-19 19:26:06','10.67.18.216','kyLin','Default Organization1'),(48,'Tank','INFO','Modify serverUnmonitored IPMI successfully.','2018-04-20 08:17:09','10.67.18.216','kyLin','Default Organization1'),(49,'Tank','INFO','Modify server168.95.1.2 IPMI successfully.','2018-04-20 08:22:05','10.67.18.216','kyLin','Default Organization1'),(50,'Tank','INFO','Modify serverUnmonitored IPMI successfully.','2018-04-20 08:23:23','10.67.18.216','kyLin','Default Organization1'),(51,'Tank','INFO','Delete server  from tank Tank 3.','2018-04-20 09:14:22','10.67.18.216','kyLin','Default Organization1'),(52,'Tank','INFO','Modify server192.168.1.121 IPMI successfully.','2018-04-20 11:14:19','10.67.18.216','kyLin','Default Organization1'),(53,'Tank','INFO','Modify server192.168.1.121 IPMI successfully.','2018-04-20 11:14:27','10.67.18.216','kyLin','Default Organization1'),(54,'Account','INFO','Delete t4 account successfully.','2018-04-20 11:15:20','10.67.18.216','kyLin','Default Organization1'),(56,'Tank','INFO','Delete Tank 3 tank successfully.','2018-04-20 11:21:06','10.67.18.216','kyLin','Default Organization1'),(57,'Tank','INFO','Delete Tank 3 tank successfully.','2018-04-20 11:39:22','10.67.18.216','kyLin','Default Organization1');
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(45) DEFAULT '',
  `role_description` varchar(250) DEFAULT '',
  `role_group` varchar(45) DEFAULT '',
  `role_auth` int(11) DEFAULT '2',
  `role_server` tinyint(2) DEFAULT '1',
  `role_event` tinyint(2) DEFAULT '1',
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'Manager','Kylin Manager','KyLin Group',1,1,1),(2,'Operator','Kylin Operator','KyLin Group',2,1,1),(3,'Viewer','Kylin Viewer','KyLin Group',3,1,0);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server`
--

DROP TABLE IF EXISTS `server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server` (
  `server_id` int(11) NOT NULL AUTO_INCREMENT,
  `server_slot` varchar(45) DEFAULT '',
  `server_ip` varchar(45) DEFAULT '',
  `server_mac` varchar(45) DEFAULT '',
  `server_status` int(11) DEFAULT '0',
  `server_tag` varchar(250) DEFAULT '',
  `server_power` varchar(45) DEFAULT '',
  `server_power_detail` varchar(250) DEFAULT '',
  `server_degree` varchar(45) DEFAULT '',
  `server_degree_detail` varchar(250) DEFAULT '',
  `server_note` varchar(250) DEFAULT '',
  `server_update_time` varchar(45) DEFAULT '',
  `server_account` varchar(100) DEFAULT '',
  `server_password` varchar(128) DEFAULT '',
  `server_active` tinyint(2) DEFAULT '1',
  `tank_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`server_id`),
  KEY `tank_id_idx` (`tank_id`),
  CONSTRAINT `tank_id` FOREIGN KEY (`tank_id`) REFERENCES `tank` (`tank_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server`
--

LOCK TABLES `server` WRITE;
/*!40000 ALTER TABLE `server` DISABLE KEYS */;
INSERT INTO `server` VALUES (1,'10','192.168.1.121','30:0e:d5:ca:c4:96',0,'FunctionTag Demo','24 W','PSU0 Consumption:0.00W\r Psu01 Consumption:32.00 W','25℃','PECI _CPU0_DTS:0.00 ℃\r PECI_CPU01_DTS:0.00 ℃\r DIMM Temp:0.00 ℃\r Sys Inlet Temp: 29.00℃','Server Note Demo','2018-04-11 17:34:16','admin','YWRtaW4=',1,3),(2,'11','168.95.1.1','E4:11:5B:12:c0:t2',1,'168.95.1.2 Function Tag','2 W','PSU1 Consumption:0.00W \r\nPsu11 Consumption:32.00 W','250℃','PECI _CPU01_DTS:0.00 ℃ \r\nPECI_CPU11_DTS:0.00 ℃ \r\nDIMM Temp:0.00 ℃ \r\nSys Inlet Temp: 53.00℃','168.95.1.2 note 3','2018-04-20 08:22:05','root','MTIzNDU2',0,1),(3,'12','168.95.1.2','E4:11:5B:12:c0:t4',2,'F3','2 W','PSU1 Consumption:0.00W \r\n Psu11 Consumption:32.00 W','250℃','PECI _CPU01_DTS:0.00 ℃ \r\nPECI_CPU11_DTS:0.00 ℃ \r\nDIMM Temp:0.00 ℃ \r\nSys Inlet Temp: 53.00℃','n3','2018-04-20 08:23:22','root','MTIzNDU2',1,1);
/*!40000 ALTER TABLE `server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_fru`
--

DROP TABLE IF EXISTS `server_fru`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_fru` (
  `server_fru_id` int(11) NOT NULL AUTO_INCREMENT,
  `server_fru_name` varchar(45) DEFAULT '',
  `server_fru_value` varchar(45) DEFAULT '',
  `server_id` int(11) NOT NULL,
  `server_fru_json` json DEFAULT NULL,
  PRIMARY KEY (`server_fru_id`),
  KEY `fk_server_fru_server_idx` (`server_id`),
  CONSTRAINT `fk_server_fru_server` FOREIGN KEY (`server_id`) REFERENCES `server` (`server_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_fru`
--

LOCK TABLES `server_fru` WRITE;
/*!40000 ALTER TABLE `server_fru` DISABLE KEYS */;
INSERT INTO `server_fru` VALUES (1,'SDR[001b] IPMB','BMC',1,NULL),(2,'Baseboard FRU Size','2048',1,NULL);
/*!40000 ALTER TABLE `server_fru` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_lan`
--

DROP TABLE IF EXISTS `server_lan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_lan` (
  `server_lan_id` int(11) NOT NULL AUTO_INCREMENT,
  `server_lan_name` varchar(45) DEFAULT NULL,
  `server_lan_value` varchar(45) DEFAULT NULL,
  `server_id` int(11) NOT NULL,
  `server_lan_json` json DEFAULT NULL,
  PRIMARY KEY (`server_lan_id`),
  KEY `fk_server_lan_server1_idx` (`server_id`),
  CONSTRAINT `fk_server_lan_server1` FOREIGN KEY (`server_id`) REFERENCES `server` (`server_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_lan`
--

LOCK TABLES `server_lan` WRITE;
/*!40000 ALTER TABLE `server_lan` DISABLE KEYS */;
INSERT INTO `server_lan` VALUES (1,'PEF Control','PEFenable DoEventMsgs',1,NULL),(2,'Channel 1 IP Address','192.168.1.121',1,NULL),(3,'Channel 1 IP addr src','DHCP',1,NULL);
/*!40000 ALTER TABLE `server_lan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_sdr`
--

DROP TABLE IF EXISTS `server_sdr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_sdr` (
  `server_sdr_id` int(11) NOT NULL AUTO_INCREMENT,
  `server_sdr_name` varchar(45) DEFAULT '',
  `server_sdr_status` varchar(45) DEFAULT '',
  `server_sdr_value` varchar(45) DEFAULT '',
  `server_id` int(11) NOT NULL,
  `server_sdr_json` json DEFAULT NULL,
  PRIMARY KEY (`server_sdr_id`),
  KEY `fk_server_sdr_server1_idx` (`server_id`),
  CONSTRAINT `fk_server_sdr_server1` FOREIGN KEY (`server_id`) REFERENCES `server` (`server_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_sdr`
--

LOCK TABLES `server_sdr` WRITE;
/*!40000 ALTER TABLE `server_sdr` DISABLE KEYS */;
INSERT INTO `server_sdr` VALUES (1,'P3V3_Sensor','Absent','0.0na',1,NULL),(2,'Sys Inlet Temp','OK','25.00 C',1,NULL),(3,'P5V_Sensor','Absent','0.0na',1,NULL);
/*!40000 ALTER TABLE `server_sdr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank`
--

DROP TABLE IF EXISTS `tank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tank` (
  `tank_id` int(11) NOT NULL AUTO_INCREMENT,
  `tank_name` varchar(100) DEFAULT 'tank',
  `tank_description` varchar(255) DEFAULT '',
  PRIMARY KEY (`tank_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank`
--

LOCK TABLES `tank` WRITE;
/*!40000 ALTER TABLE `tank` DISABLE KEYS */;
INSERT INTO `tank` VALUES (1,'Tank 1','Tank 1 description'),(2,'Tank 2','Tank 2 desc '),(3,'Tank 3','Td 3');
/*!40000 ALTER TABLE `tank` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-20 11:41:38
