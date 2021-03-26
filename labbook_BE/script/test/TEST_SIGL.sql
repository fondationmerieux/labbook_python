-- MySQL dump 10.13  Distrib 5.7.21, for Linux (i686)
--
-- Host: localhost    Database: SIGL
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES UTF8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ecversion`
--

DROP TABLE IF EXISTS `ecversion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ecversion` (
  `version` varchar(16) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecversion`
--

LOCK TABLES `ecversion` WRITE;
/*!40000 ALTER TABLE `ecversion` DISABLE KEYS */;
INSERT INTO `ecversion` (`version`) VALUES ('20120917');
/*!40000 ALTER TABLE `ecversion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `premieretransition`
--

DROP TABLE IF EXISTS `premieretransition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `premieretransition` (
  `a` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `premieretransition`
--

LOCK TABLES `premieretransition` WRITE;
/*!40000 ALTER TABLE `premieretransition` DISABLE KEYS */;
/*!40000 ALTER TABLE `premieretransition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `session` (
  `id` char(32) NOT NULL,
  `modified` int(11) DEFAULT NULL,
  `lifetime` int(11) DEFAULT NULL,
  `data` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_01_data`
--

DROP TABLE IF EXISTS `sigl_01_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_01_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `date_prel` date DEFAULT NULL,
  `type_prel` int(10) unsigned NOT NULL,
  `quantite` int(2) unsigned DEFAULT NULL,
  `statut` int(10) unsigned NOT NULL,
  `id_dos` int(10) unsigned DEFAULT NULL,
  `preleveur` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_reception` date DEFAULT NULL,
  `heure_reception` time DEFAULT NULL,
  `commentaire` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lieu_prel` int(10) unsigned DEFAULT NULL,
  `lieu_prel_plus` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `localisation` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`),
  KEY `id_dos` (`id_dos`) USING BTREE,
  KEY `sigl_01_data_ibfk_3` (`type_prel`),
  KEY `sigl_01_data_ibfk_4` (`statut`),
  KEY `sigl_01_data_ibfk_1` (`lieu_prel`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_01_data`
--

LOCK TABLES `sigl_01_data` WRITE;
/*!40000 ALTER TABLE `sigl_01_data` DISABLE KEYS */;
INSERT INTO `sigl_01_data` (`id_data`, `id_owner`, `date_prel`, `type_prel`, `quantite`, `statut`, `id_dos`, `preleveur`, `date_reception`, `heure_reception`, `commentaire`, `lieu_prel`, `lieu_prel_plus`, `localisation`) VALUES (1,1001,NULL,138,NULL,8,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,1001,NULL,138,NULL,8,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sigl_01_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_01_data_group`
--

DROP TABLE IF EXISTS `sigl_01_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_01_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_01_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_01_data_group`
--

LOCK TABLES `sigl_01_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_01_data_group` DISABLE KEYS */;
INSERT INTO `sigl_01_data_group` (`id_data_group`, `id_data`, `id_group`) VALUES (1,1,1000),(2,2,1000);
/*!40000 ALTER TABLE `sigl_01_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_01_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_01_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_01_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_01_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_01_data_group_mode`
--

LOCK TABLES `sigl_01_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_01_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_01_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_01_deleted`
--

DROP TABLE IF EXISTS `sigl_01_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_01_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `date_prel` date DEFAULT NULL,
  `type_prel` int(10) unsigned NOT NULL,
  `quantite` int(2) unsigned DEFAULT NULL,
  `statut` int(10) unsigned NOT NULL,
  `id_dos` int(10) unsigned DEFAULT NULL,
  `preleveur` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_reception` date DEFAULT NULL,
  `heure_reception` time NOT NULL,
  `commentaire` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lieu_prel` int(10) unsigned DEFAULT NULL,
  `lieu_prel_plus` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `localisation` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`),
  KEY `id_dos` (`id_dos`) USING BTREE,
  KEY `sigl_01_data_ibfk_3` (`type_prel`),
  KEY `sigl_01_data_ibfk_4` (`statut`),
  KEY `sigl_01_data_ibfk_1` (`lieu_prel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_01_deleted`
--

LOCK TABLES `sigl_01_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_01_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_01_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_01_dico_analyse_data`
--

DROP TABLE IF EXISTS `sigl_01_dico_analyse_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_01_dico_analyse_data` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_pat` int(11) NOT NULL,
  `id_dico` int(11) NOT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_01_dico_analyse_data`
--

LOCK TABLES `sigl_01_dico_analyse_data` WRITE;
/*!40000 ALTER TABLE `sigl_01_dico_analyse_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_01_dico_analyse_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_01_dico_analyse_deleted`
--

DROP TABLE IF EXISTS `sigl_01_dico_analyse_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_01_dico_analyse_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_pat` int(11) NOT NULL,
  `id_dico` int(11) NOT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_01_dico_analyse_deleted`
--

LOCK TABLES `sigl_01_dico_analyse_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_01_dico_analyse_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_01_dico_analyse_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_02_data`
--

DROP TABLE IF EXISTS `sigl_02_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_02_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_patient` int(10) unsigned DEFAULT NULL,
  `type` int(10) unsigned DEFAULT NULL,
  `date_dos` date NOT NULL,
  `num_dos_jour` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `num_dos_an` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `med_prescripteur` int(10) unsigned DEFAULT NULL,
  `date_prescription` date NOT NULL,
  `service_interne` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `num_lit` int(4) unsigned DEFAULT NULL,
  `id_colis` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_reception_colis` date DEFAULT NULL,
  `rc` text COLLATE utf8_unicode_ci,
  `colis` int(10) unsigned DEFAULT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `remise` int(10) unsigned DEFAULT NULL,
  `remise_pourcent` decimal(10,2) DEFAULT NULL,
  `assu_pourcent` decimal(10,2) DEFAULT NULL,
  `a_payer` decimal(10,2) DEFAULT NULL,
  `num_quittance` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `num_fact` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `statut` int(10) unsigned DEFAULT NULL,
  `num_dos_mois` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_patient` (`id_patient`),
  KEY `id_owner` (`id_owner`),
  KEY `sigl_02_data_ibfk_4` (`type`),
  KEY `sigl_02_data_ibfk_5` (`med_prescripteur`),
  KEY `sigl_02_data_ibfk_6` (`colis`),
  KEY `sigl_02_data_ibfk_7` (`remise`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_02_data`
--

LOCK TABLES `sigl_02_data` WRITE;
/*!40000 ALTER TABLE `sigl_02_data` DISABLE KEYS */;
INSERT INTO `sigl_02_data` (`id_data`, `id_owner`, `id_patient`, `type`, `date_dos`, `num_dos_jour`, `num_dos_an`, `med_prescripteur`, `date_prescription`, `service_interne`, `num_lit`, `id_colis`, `date_reception_colis`, `rc`, `colis`, `prix`, `remise`, `remise_pourcent`, `assu_pourcent`, `a_payer`, `num_quittance`, `num_fact`, `statut`, `num_dos_mois`) VALUES (1,1001,1,184,'2018-06-01','201806010001','2018000001',NULL,'2018-06-01',NULL,NULL,NULL,NULL,NULL,NULL,0.00,NULL,NULL,NULL,0.00,NULL,NULL,182,'2018060001'),(2,1001,2,183,'2018-12-04','201812040001','2018000002',NULL,'2018-12-04',NULL,NULL,NULL,NULL,NULL,NULL,12000.00,NULL,NULL,NULL,12000.00,NULL,NULL,182,'2018120001');
/*!40000 ALTER TABLE `sigl_02_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_02_data_group`
--

DROP TABLE IF EXISTS `sigl_02_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_02_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_02_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_02_data_group`
--

LOCK TABLES `sigl_02_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_02_data_group` DISABLE KEYS */;
INSERT INTO `sigl_02_data_group` (`id_data_group`, `id_data`, `id_group`) VALUES (1,1,1000),(2,2,1000);
/*!40000 ALTER TABLE `sigl_02_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_02_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_02_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_02_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_02_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_02_data_group_mode`
--

LOCK TABLES `sigl_02_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_02_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_02_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_02_deleted`
--

DROP TABLE IF EXISTS `sigl_02_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_02_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_patient` int(10) unsigned DEFAULT NULL,
  `type` int(10) unsigned DEFAULT NULL,
  `date_dos` date NOT NULL,
  `num_dos_jour` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `num_dos_an` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `med_prescripteur` int(10) unsigned DEFAULT NULL,
  `date_prescription` date NOT NULL,
  `service_interne` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `num_lit` int(4) unsigned DEFAULT NULL,
  `id_colis` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_reception_colis` date DEFAULT NULL,
  `rc` text COLLATE utf8_unicode_ci,
  `colis` int(10) unsigned DEFAULT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `remise` int(10) unsigned DEFAULT NULL,
  `remise_pourcent` decimal(10,2) DEFAULT NULL,
  `assu_pourcent` decimal(10,2) DEFAULT NULL,
  `a_payer` decimal(10,2) DEFAULT NULL,
  `num_quittance` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `num_fact` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `statut` int(10) unsigned DEFAULT NULL,
  `num_dos_mois` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_patient` (`id_patient`),
  KEY `id_owner` (`id_owner`),
  KEY `sigl_02_data_ibfk_4` (`type`),
  KEY `sigl_02_data_ibfk_5` (`med_prescripteur`),
  KEY `sigl_02_data_ibfk_6` (`colis`),
  KEY `sigl_02_data_ibfk_7` (`remise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_02_deleted`
--

LOCK TABLES `sigl_02_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_02_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_02_deleted` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_user` (
  `id_sys_user` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `password` varchar(81) NOT NULL,
  `expire_date` date DEFAULT NULL,
  `cps_id` varchar(30) DEFAULT NULL,
  `email` varchar(200) NOT NULL,
  `project_creator` int(11) NOT NULL,
  `active` int(11) NOT NULL,
  `creation_date` datetime NOT NULL,
  PRIMARY KEY (`id_sys_user`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` (`id_sys_user`, `username`, `firstname`, `lastname`, `password`, `expire_date`, `cps_id`, `email`, `project_creator`, `active`, `creation_date`) VALUES (1,'editor',NULL,NULL,'c80bc97702842b8276a2c48e336eb23442b191a5:SLjcJuagLBTEIMdFl2-_dW0j03K8VXEl',NULL,NULL,'1team@epiconcept.fr',1,1,'2017-01-23 18:20:22');
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-07 23:16:58
