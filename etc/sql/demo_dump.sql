-- MySQL dump 10.13  Distrib 5.7.31, for Linux (x86_64)
--
-- Host: localhost    Database: SIGL
-- ------------------------------------------------------
-- Server version	5.7.31-0ubuntu0.18.04.1

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
-- Table structure for table `age_interval_setting`
--

DROP TABLE IF EXISTS `age_interval_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `age_interval_setting` (
  `ais_ser` int(11) NOT NULL AUTO_INCREMENT,
  `ais_rank` int(11) NOT NULL,
  `ais_lower_bound` int(11) DEFAULT NULL,
  `ais_upper_bound` int(11) DEFAULT NULL,
  PRIMARY KEY (`ais_ser`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `age_interval_setting`
--

LOCK TABLES `age_interval_setting` WRITE;
/*!40000 ALTER TABLE `age_interval_setting` DISABLE KEYS */;
INSERT INTO `age_interval_setting` VALUES (1,0,NULL,5),(2,1,5,20),(3,2,20,40),(4,3,40,NULL);
/*!40000 ALTER TABLE `age_interval_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('71b4a9a97b7a');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup_setting`
--

DROP TABLE IF EXISTS `backup_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backup_setting` (
  `bks_ser` int(11) NOT NULL AUTO_INCREMENT,
  `bks_start_time` time NOT NULL,
  PRIMARY KEY (`bks_ser`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_setting`
--

LOCK TABLES `backup_setting` WRITE;
/*!40000 ALTER TABLE `backup_setting` DISABLE KEYS */;
INSERT INTO `backup_setting` VALUES (1,'12:00:00');
/*!40000 ALTER TABLE `backup_setting` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `ecversion` VALUES ('20120917');
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
-- Table structure for table `product_details`
--

DROP TABLE IF EXISTS `product_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_details` (
  `prd_ser` int(11) NOT NULL AUTO_INCREMENT,
  `prd_date` datetime DEFAULT NULL,
  `prd_name` varchar(100) NOT NULL,
  `prd_type` int(11) DEFAULT '0',
  `prd_nb_by_pack` int(11) DEFAULT '0',
  `prd_supplier` int(11) DEFAULT '0',
  `prd_ref_supplier` varchar(50) DEFAULT NULL,
  `prd_conserv` int(11) DEFAULT '0',
  PRIMARY KEY (`prd_ser`),
  KEY `prd_name` (`prd_name`),
  KEY `prd_type` (`prd_type`),
  KEY `prd_supplier` (`prd_supplier`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_details`
--

LOCK TABLES `product_details` WRITE;
/*!40000 ALTER TABLE `product_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_supply`
--

DROP TABLE IF EXISTS `product_supply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_supply` (
  `prs_ser` int(11) NOT NULL AUTO_INCREMENT,
  `prs_date` datetime DEFAULT NULL,
  `prs_prd` int(11) NOT NULL,
  `prs_nb_pack` int(11) DEFAULT '0',
  `prs_status` int(11) DEFAULT '0',
  `prs_receipt_date` datetime DEFAULT NULL,
  `prs_expir_date` datetime DEFAULT NULL,
  `prs_rack` varchar(100) DEFAULT NULL,
  `prs_batch_num` varchar(50) DEFAULT NULL,
  `prs_buy_price` int(11) DEFAULT '0',
  `prs_sell_price` int(11) DEFAULT '0',
  PRIMARY KEY (`prs_ser`),
  KEY `prs_prd` (`prs_prd`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_supply`
--

LOCK TABLES `product_supply` WRITE;
/*!40000 ALTER TABLE `product_supply` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_supply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_use`
--

DROP TABLE IF EXISTS `product_use`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_use` (
  `pru_ser` int(11) NOT NULL AUTO_INCREMENT,
  `pru_date` datetime DEFAULT NULL,
  `pru_user` int(11) NOT NULL,
  `pru_prs` int(11) NOT NULL,
  `pru_nb_pack` int(11) NOT NULL,
  PRIMARY KEY (`pru_ser`),
  KEY `pru_prs` (`pru_prs`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_use`
--

LOCK TABLES `product_use` WRITE;
/*!40000 ALTER TABLE `product_use` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_use` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_01_data`
--

LOCK TABLES `sigl_01_data` WRITE;
/*!40000 ALTER TABLE `sigl_01_data` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_01_data_group`
--

LOCK TABLES `sigl_01_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_01_data_group` DISABLE KEYS */;
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
  `date_hosp` date DEFAULT NULL,
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
-- Dumping data for table `sigl_02_data`
--

LOCK TABLES `sigl_02_data` WRITE;
/*!40000 ALTER TABLE `sigl_02_data` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_02_data_group`
--

LOCK TABLES `sigl_02_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_02_data_group` DISABLE KEYS */;
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
-- Table structure for table `sigl_03_data`
--

DROP TABLE IF EXISTS `sigl_03_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_03_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `anonyme` int(10) unsigned DEFAULT NULL,
  `code` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `code_patient` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nom` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `prenom` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ddn` date DEFAULT NULL,
  `sexe` int(10) unsigned DEFAULT NULL,
  `ethnie` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `adresse` text COLLATE utf8_unicode_ci,
  `cp` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ville` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `tel` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `profession` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nom_jf` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `quartier` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bp` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ddn_approx` int(10) unsigned DEFAULT NULL,
  `age` int(3) unsigned DEFAULT NULL,
  `annee_naiss` int(4) unsigned DEFAULT NULL,
  `semaine_naiss` int(2) unsigned DEFAULT NULL,
  `mois_naiss` int(2) unsigned DEFAULT NULL,
  `unite` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`),
  KEY `sigl_03_data_ibfk_2` (`ddn_approx`),
  KEY `sigl_03_data_anonyme_dico` (`anonyme`),
  KEY `sigl_03_data_sexe_dico` (`sexe`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_03_data`
--

LOCK TABLES `sigl_03_data` WRITE;
/*!40000 ALTER TABLE `sigl_03_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_03_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_03_data_group`
--

DROP TABLE IF EXISTS `sigl_03_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_03_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_03_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_03_data_group`
--

LOCK TABLES `sigl_03_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_03_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_03_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_03_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_03_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_03_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_03_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_03_data_group_mode`
--

LOCK TABLES `sigl_03_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_03_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_03_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_03_deleted`
--

DROP TABLE IF EXISTS `sigl_03_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_03_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `anonyme` int(10) unsigned DEFAULT NULL,
  `code` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `code_patient` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nom` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `prenom` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ddn` date DEFAULT NULL,
  `sexe` int(10) unsigned DEFAULT NULL,
  `ethnie` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `adresse` text COLLATE utf8_unicode_ci,
  `cp` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ville` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `tel` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `profession` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `semaine_naiss` int(2) unsigned DEFAULT NULL,
  `mois_naiss` int(2) unsigned DEFAULT NULL,
  `nom_jf` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ddn_approx` int(10) unsigned DEFAULT NULL,
  `age` int(3) unsigned DEFAULT NULL,
  `annee_naiss` int(4) unsigned DEFAULT NULL,
  `bp` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `quartier` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `unite` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_03_deleted`
--

LOCK TABLES `sigl_03_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_03_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_03_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_04_data`
--

DROP TABLE IF EXISTS `sigl_04_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_04_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_dos` int(10) unsigned DEFAULT NULL,
  `ref_analyse` int(10) unsigned NOT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `paye` int(10) unsigned DEFAULT NULL,
  `urgent` int(10) unsigned DEFAULT NULL,
  `demande` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`),
  KEY `id_prel` (`id_dos`) USING BTREE,
  KEY `sigl_04_data_ibfk_3` (`ref_analyse`),
  KEY `sigl_04_data_ibfk_4` (`paye`),
  KEY `sigl_04_data_ibfk_6` (`urgent`),
  KEY `sigl_04_data_ibfk_7` (`demande`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_04_data`
--

LOCK TABLES `sigl_04_data` WRITE;
/*!40000 ALTER TABLE `sigl_04_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_04_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_04_data_group`
--

DROP TABLE IF EXISTS `sigl_04_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_04_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_04_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_04_data_group`
--

LOCK TABLES `sigl_04_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_04_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_04_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_04_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_04_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_04_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_04_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_04_data_group_mode`
--

LOCK TABLES `sigl_04_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_04_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_04_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_04_deleted`
--

DROP TABLE IF EXISTS `sigl_04_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_04_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_dos` int(10) unsigned DEFAULT NULL,
  `ref_analyse` int(10) unsigned NOT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `paye` int(10) unsigned DEFAULT NULL,
  `urgent` int(10) unsigned DEFAULT NULL,
  `demande` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`),
  KEY `id_prel` (`id_dos`) USING BTREE,
  KEY `sigl_04_data_ibfk_3` (`ref_analyse`),
  KEY `sigl_04_data_ibfk_4` (`paye`),
  KEY `sigl_04_data_ibfk_6` (`urgent`),
  KEY `sigl_04_data_ibfk_7` (`demande`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_04_deleted`
--

LOCK TABLES `sigl_04_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_04_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_04_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_05_data`
--

DROP TABLE IF EXISTS `sigl_05_05_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_05_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_complexe` int(10) unsigned NOT NULL,
  `id_individuelle` int(10) unsigned NOT NULL,
  `position` int(10) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `unique` (`id_complexe`,`id_individuelle`),
  KEY `id_owner` (`id_owner`),
  KEY `id_complexe` (`id_complexe`) USING BTREE,
  KEY `id_individuelle` (`id_individuelle`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_05_data`
--

LOCK TABLES `sigl_05_05_data` WRITE;
/*!40000 ALTER TABLE `sigl_05_05_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_05_05_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_05_data_group`
--

DROP TABLE IF EXISTS `sigl_05_05_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_05_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_05_05_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_05_data_group`
--

LOCK TABLES `sigl_05_05_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_05_05_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_05_05_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_05_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_05_05_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_05_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_05_05_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_05_data_group_mode`
--

LOCK TABLES `sigl_05_05_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_05_05_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_05_05_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_05_deleted`
--

DROP TABLE IF EXISTS `sigl_05_05_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_05_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_complexe` int(10) unsigned NOT NULL,
  `id_individuelle` int(10) unsigned NOT NULL,
  `position` int(10) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `unique` (`id_complexe`,`id_individuelle`),
  KEY `id_owner` (`id_owner`),
  KEY `id_complexe` (`id_complexe`) USING BTREE,
  KEY `id_individuelle` (`id_individuelle`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_05_deleted`
--

LOCK TABLES `sigl_05_05_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_05_05_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_05_05_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_07_data`
--

DROP TABLE IF EXISTS `sigl_05_07_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_07_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_refanalyse` int(10) unsigned NOT NULL,
  `id_refvariable` int(10) unsigned NOT NULL,
  `position` int(2) unsigned DEFAULT NULL,
  `num_var` int(2) unsigned DEFAULT NULL,
  `obligatoire` int(11) DEFAULT '4',
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `UNIQUE` (`id_refanalyse`,`id_refvariable`),
  KEY `FK_sigl_05_07_data_1` (`id_owner`),
  KEY `FK_sigl_05_07_data_3` (`id_refvariable`)
) ENGINE=InnoDB AUTO_INCREMENT=1767 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_07_data`
--

LOCK TABLES `sigl_05_07_data` WRITE;
/*!40000 ALTER TABLE `sigl_05_07_data` DISABLE KEYS */;
INSERT INTO `sigl_05_07_data` VALUES (1,1010,7,1,NULL,NULL,4),(2,1010,24,2,NULL,1,4),(3,1010,25,3,NULL,1,4),(4,1010,26,4,NULL,1,4),(5,1010,27,5,NULL,1,4),(6,1010,28,6,NULL,1,4),(7,1010,29,7,NULL,1,4),(8,1010,30,8,NULL,1,4),(9,1010,31,9,NULL,1,4),(10,1010,32,10,NULL,1,4),(11,1010,33,11,NULL,1,4),(12,1010,33,12,10,1,4),(13,1010,34,13,NULL,NULL,4),(14,1010,34,14,10,NULL,4),(15,1010,35,15,NULL,1,4),(16,1010,38,14,NULL,NULL,4),(17,1010,38,16,10,NULL,4),(18,1010,38,17,20,NULL,4),(19,1010,39,18,NULL,1,4),(20,1010,40,19,NULL,1,4),(21,1010,41,20,NULL,1,4),(22,1010,42,21,NULL,1,4),(23,1010,43,22,NULL,NULL,4),(24,1010,43,23,10,NULL,4),(25,1010,44,24,NULL,NULL,4),(26,1010,44,16,10,NULL,4),(27,1010,45,25,NULL,NULL,4),(28,1010,45,17,10,NULL,4),(29,1010,46,26,NULL,1,4),(30,1010,47,27,NULL,2,4),(31,1010,48,28,NULL,1,4),(32,1010,49,29,NULL,1,4),(33,1010,49,27,10,2,4),(34,1010,49,30,20,3,4),(35,1010,49,31,30,4,4),(36,1010,49,32,40,NULL,4),(37,1010,49,26,50,1,4),(38,1010,49,33,60,3,4),(39,1010,50,34,NULL,NULL,4),(40,1010,50,35,10,NULL,4),(41,1010,50,36,20,NULL,4),(42,1010,50,37,30,NULL,4),(43,1010,50,38,40,NULL,4),(44,1010,51,39,NULL,NULL,4),(45,1010,52,40,NULL,NULL,4),(46,1010,54,33,NULL,3,4),(47,1010,55,41,NULL,NULL,4),(48,1010,56,42,NULL,NULL,4),(49,1010,56,41,10,NULL,4),(50,1010,57,43,NULL,NULL,4),(51,1010,60,44,NULL,NULL,4),(52,1010,60,45,10,NULL,4),(53,1010,60,46,20,NULL,4),(54,1010,60,47,30,NULL,4),(55,1010,60,48,40,NULL,4),(56,1010,60,49,50,NULL,4),(57,1010,61,50,NULL,NULL,4),(58,1010,62,51,NULL,NULL,4),(59,1010,63,52,NULL,NULL,4),(60,1010,64,53,NULL,NULL,4),(61,1010,65,54,NULL,NULL,4),(62,1010,65,55,10,NULL,4),(63,1010,66,56,NULL,NULL,4),(64,1010,67,57,NULL,NULL,4),(65,1010,68,58,NULL,NULL,4),(66,1010,69,59,NULL,NULL,4),(67,1010,70,59,NULL,NULL,4),(68,1010,71,60,NULL,NULL,4),(69,1010,72,61,NULL,NULL,4),(70,1010,73,3,NULL,1,4),(71,1010,73,62,10,NULL,4),(72,1010,73,63,20,NULL,4),(73,1010,73,64,30,NULL,4),(74,1010,73,65,40,NULL,4),(75,1010,73,66,50,NULL,4),(76,1010,74,67,NULL,NULL,4),(77,1010,75,68,NULL,NULL,4),(78,1010,76,69,NULL,NULL,4),(79,1010,77,70,NULL,NULL,4),(80,1010,78,71,NULL,NULL,4),(81,1010,79,72,NULL,NULL,4),(82,1010,80,73,NULL,NULL,4),(83,1010,81,74,NULL,NULL,4),(84,1010,82,75,NULL,NULL,4),(85,1010,83,76,NULL,NULL,4),(86,1010,84,77,NULL,NULL,4),(87,1010,85,76,NULL,NULL,4),(88,1010,85,77,10,NULL,4),(89,1010,86,78,NULL,NULL,4),(90,1010,87,79,NULL,NULL,4),(91,1010,88,80,NULL,NULL,4),(92,1010,89,81,NULL,NULL,4),(93,1010,90,82,NULL,NULL,4),(94,1010,91,83,NULL,NULL,4),(95,1010,92,84,NULL,NULL,4),(96,1010,93,85,NULL,NULL,4),(97,1010,94,86,NULL,NULL,4),(98,1010,95,87,NULL,NULL,4),(99,1010,96,88,NULL,NULL,4),(100,1010,97,89,NULL,NULL,4),(101,1010,98,90,NULL,NULL,4),(102,1010,99,91,NULL,NULL,4),(103,1010,100,92,NULL,NULL,4),(104,1010,101,93,NULL,NULL,4),(105,1010,102,94,NULL,NULL,4),(106,1010,103,95,NULL,NULL,4),(107,1010,104,96,NULL,NULL,4),(108,1010,105,97,NULL,NULL,4),(109,1010,106,98,NULL,1,4),(110,1010,107,99,NULL,NULL,4),(111,1010,108,100,NULL,1,4),(112,1010,109,101,NULL,NULL,4),(113,1010,109,102,10,NULL,4),(114,1010,110,103,NULL,NULL,4),(115,1010,111,104,NULL,NULL,4),(116,1010,111,105,10,NULL,4),(117,1010,112,102,NULL,NULL,4),(118,1010,112,105,10,NULL,4),(119,1010,114,106,NULL,1,4),(120,1010,114,107,10,NULL,4),(121,1010,114,8,20,1,4),(122,1010,114,108,30,NULL,4),(123,1010,115,109,NULL,1,4),(124,1010,116,110,NULL,1,4),(125,1010,117,13,NULL,NULL,4),(126,1010,117,14,10,NULL,4),(127,1010,118,111,NULL,1,4),(128,1010,118,21,10,1,4),(129,1010,119,112,NULL,NULL,4),(130,1010,120,113,NULL,NULL,4),(131,1010,121,114,NULL,NULL,4),(132,1010,123,115,NULL,NULL,4),(133,1010,124,116,NULL,NULL,4),(134,1010,125,117,NULL,NULL,4),(135,1010,127,118,NULL,NULL,4),(136,1010,127,119,10,NULL,4),(137,1010,128,120,NULL,NULL,4),(138,1010,129,121,NULL,NULL,4),(139,1010,130,122,NULL,NULL,4),(140,1010,132,123,NULL,NULL,4),(141,1010,133,124,NULL,1,4),(142,1010,134,125,NULL,NULL,4),(143,1010,135,126,NULL,1,4),(144,1010,135,127,10,2,4),(145,1010,135,128,20,3,4),(146,1010,135,129,30,NULL,4),(147,1010,136,126,NULL,1,4),(148,1010,136,130,10,2,4),(149,1010,136,131,20,3,4),(150,1010,136,132,30,NULL,4),(151,1010,137,126,NULL,1,4),(152,1010,137,133,10,2,4),(153,1010,137,134,20,3,4),(154,1010,137,135,30,NULL,4),(155,1010,138,136,NULL,NULL,4),(156,1010,138,137,10,NULL,4),(157,1010,138,138,20,NULL,4),(158,1010,138,139,30,NULL,4),(159,1010,138,140,40,NULL,4),(160,1010,138,141,50,NULL,4),(161,1010,138,142,60,NULL,4),(162,1010,139,136,NULL,NULL,4),(163,1010,139,138,10,NULL,4),(164,1010,143,143,NULL,NULL,4),(165,1010,144,144,NULL,NULL,4),(166,1010,145,145,NULL,NULL,4),(167,1010,147,146,NULL,NULL,4),(168,1010,147,147,10,NULL,4),(169,1010,147,148,20,NULL,4),(170,1010,149,149,NULL,NULL,4),(171,1010,150,150,NULL,NULL,4),(172,1010,150,151,10,NULL,4),(173,1010,151,152,NULL,NULL,4),(174,1010,152,153,NULL,NULL,4),(175,1010,155,154,NULL,1,4),(176,1010,155,151,10,2,4),(177,1010,155,155,20,3,4),(178,1010,155,156,30,NULL,4),(179,1010,155,157,40,NULL,4),(180,1010,155,158,50,NULL,4),(181,1010,155,159,60,4,4),(182,1010,155,160,70,5,4),(183,1010,155,161,80,6,4),(184,1010,155,162,90,7,4),(185,1010,155,163,100,8,4),(186,1010,155,164,110,9,4),(187,1010,155,165,120,NULL,4),(188,1010,155,166,130,NULL,4),(189,1010,155,167,140,NULL,4),(190,1010,155,168,150,NULL,4),(191,1010,155,169,160,1,4),(192,1010,155,170,170,NULL,4),(193,1010,155,171,180,NULL,4),(194,1010,155,172,190,4,4),(195,1010,155,173,200,5,4),(196,1010,155,174,210,6,4),(197,1010,155,175,220,7,4),(198,1010,155,176,230,8,4),(199,1010,155,177,240,9,4),(200,1010,155,178,250,NULL,4),(201,1010,157,179,NULL,1,4),(202,1010,157,180,10,2,4),(203,1010,157,181,20,3,4),(204,1010,157,182,30,4,4),(205,1010,158,183,NULL,NULL,4),(206,1010,159,184,NULL,NULL,4),(207,1010,160,185,NULL,NULL,4),(208,1010,162,186,NULL,NULL,4),(209,1010,163,187,NULL,NULL,4),(210,1010,164,188,NULL,NULL,4),(211,1010,165,189,NULL,NULL,4),(212,1010,166,190,NULL,NULL,4),(213,1010,167,191,NULL,NULL,4),(214,1010,168,192,NULL,NULL,4),(215,1010,169,193,NULL,NULL,4),(216,1010,171,194,NULL,NULL,4),(217,1010,172,195,NULL,NULL,4),(218,1010,173,196,NULL,NULL,4),(219,1010,173,197,10,NULL,4),(220,1010,174,198,NULL,NULL,4),(221,1010,175,199,NULL,NULL,4),(222,1010,175,200,10,NULL,4),(223,1010,176,201,NULL,NULL,4),(224,1010,177,202,NULL,NULL,4),(225,1010,178,203,NULL,NULL,4),(226,1010,178,204,10,NULL,4),(227,1010,182,205,NULL,NULL,4),(228,1010,184,206,NULL,NULL,4),(229,1010,185,207,NULL,NULL,4),(230,1010,186,208,NULL,NULL,4),(231,1010,187,209,NULL,NULL,4),(232,1010,188,210,NULL,NULL,4),(233,1010,189,211,NULL,NULL,4),(234,1010,191,212,20,NULL,4),(235,1010,191,213,10,NULL,4),(237,1010,193,215,NULL,NULL,4),(238,1010,195,216,NULL,NULL,4),(240,1010,196,218,10,NULL,4),(241,1010,196,219,20,NULL,4),(242,1010,196,220,30,NULL,4),(243,1010,196,221,40,NULL,4),(244,1010,196,222,50,NULL,4),(245,1010,196,223,60,NULL,4),(246,1010,196,224,70,NULL,4),(247,1010,196,225,80,NULL,4),(248,1010,196,226,90,NULL,4),(249,1010,196,227,100,NULL,4),(250,1010,196,228,110,NULL,4),(251,1010,197,229,NULL,NULL,4),(252,1010,197,230,10,NULL,4),(253,1010,198,231,NULL,NULL,4),(254,1010,198,230,10,NULL,4),(255,1010,199,232,NULL,NULL,4),(256,1010,199,233,10,NULL,4),(257,1010,200,234,NULL,NULL,4),(258,1010,200,235,10,NULL,4),(259,1010,201,236,NULL,NULL,4),(260,1010,202,237,NULL,NULL,4),(261,1010,203,238,NULL,NULL,4),(262,1010,204,239,NULL,NULL,4),(263,1010,204,240,10,NULL,4),(264,1010,204,241,20,NULL,4),(265,1010,205,242,NULL,NULL,4),(266,1010,206,243,NULL,NULL,4),(267,1010,206,244,10,NULL,4),(268,1010,206,245,20,NULL,4),(269,1010,207,246,NULL,NULL,4),(270,1010,208,247,NULL,NULL,4),(271,1010,209,248,NULL,NULL,4),(272,1010,210,249,NULL,NULL,4),(273,1010,211,250,NULL,NULL,4),(274,1010,212,251,NULL,NULL,4),(275,1010,212,252,10,NULL,4),(276,1010,212,253,20,NULL,4),(277,1010,213,254,NULL,NULL,4),(278,1010,214,255,NULL,NULL,4),(279,1010,215,256,NULL,NULL,4),(280,1010,216,257,NULL,NULL,4),(281,1010,217,258,NULL,NULL,4),(282,1010,218,259,NULL,NULL,4),(283,1010,219,260,NULL,NULL,4),(284,1010,219,261,10,NULL,4),(285,1010,220,262,NULL,NULL,4),(286,1010,221,263,NULL,NULL,4),(287,1010,222,264,NULL,NULL,4),(288,1010,222,265,10,NULL,4),(289,1010,223,266,NULL,NULL,4),(290,1010,223,267,10,NULL,4),(291,1010,224,268,NULL,NULL,4),(292,1010,225,269,NULL,NULL,4),(293,1010,225,213,10,NULL,4),(294,1010,225,270,30,NULL,4),(295,1010,226,271,NULL,NULL,4),(296,1010,226,272,10,NULL,4),(297,1010,227,273,NULL,NULL,4),(298,1010,227,274,10,NULL,4),(299,1010,228,275,NULL,NULL,4),(300,1010,229,276,NULL,NULL,4),(301,1010,229,213,10,NULL,4),(302,1010,229,277,30,NULL,4),(303,1010,230,278,NULL,NULL,4),(304,1010,231,279,NULL,NULL,4),(305,1010,231,280,10,NULL,4),(306,1010,232,281,NULL,NULL,4),(307,1010,232,282,10,NULL,4),(308,1010,232,283,20,NULL,4),(309,1010,234,284,NULL,NULL,4),(310,1010,235,285,NULL,NULL,4),(311,1010,236,286,NULL,NULL,4),(312,1010,237,287,NULL,NULL,4),(313,1010,237,288,10,NULL,4),(314,1010,239,245,10,NULL,4),(317,1010,241,291,NULL,NULL,4),(318,1010,242,292,NULL,NULL,4),(319,1010,244,293,NULL,NULL,4),(320,1010,245,294,NULL,NULL,4),(321,1010,246,295,NULL,NULL,4),(322,1010,247,296,NULL,NULL,4),(323,1010,248,297,NULL,NULL,4),(324,1010,249,298,NULL,NULL,4),(325,1010,250,299,NULL,NULL,4),(326,1010,251,300,NULL,NULL,4),(327,1010,252,301,NULL,NULL,4),(328,1010,252,302,10,NULL,4),(329,1010,252,303,20,NULL,4),(330,1010,252,304,30,NULL,4),(331,1010,252,305,40,NULL,4),(332,1010,252,306,50,NULL,4),(333,1010,252,307,60,NULL,4),(334,1010,252,308,70,NULL,4),(335,1010,253,309,NULL,NULL,4),(336,1010,254,310,NULL,NULL,4),(337,1010,255,311,NULL,NULL,4),(338,1010,256,312,NULL,NULL,4),(339,1010,256,313,10,NULL,4),(340,1010,257,314,NULL,NULL,4),(341,1010,257,614,10,NULL,4),(342,1010,257,316,20,NULL,4),(343,1010,258,317,NULL,NULL,4),(344,1010,258,318,10,NULL,4),(345,1010,258,319,20,NULL,4),(346,1010,259,317,NULL,NULL,4),(347,1010,259,320,10,NULL,4),(348,1010,259,318,20,NULL,4),(349,1010,260,321,NULL,NULL,4),(350,1010,260,322,10,NULL,4),(351,1010,261,323,NULL,NULL,4),(352,1010,262,324,NULL,NULL,4),(353,1010,262,325,10,NULL,4),(354,1010,263,326,NULL,NULL,4),(355,1010,263,327,10,NULL,4),(356,1010,263,328,20,NULL,4),(357,1010,264,329,NULL,NULL,4),(358,1010,265,330,NULL,NULL,4),(359,1010,265,331,10,NULL,4),(360,1010,265,332,20,NULL,4),(361,1010,265,333,30,NULL,4),(362,1010,265,334,40,NULL,4),(363,1010,265,335,50,NULL,4),(364,1010,265,336,60,NULL,4),(365,1010,265,337,70,NULL,4),(366,1010,265,338,80,NULL,4),(367,1010,265,339,90,NULL,4),(368,1010,265,340,100,NULL,4),(369,1010,266,330,NULL,NULL,4),(370,1010,266,341,10,NULL,4),(371,1010,266,332,20,NULL,4),(372,1010,266,333,30,NULL,4),(373,1010,266,342,40,NULL,4),(374,1010,266,334,50,NULL,4),(375,1010,266,335,60,NULL,4),(376,1010,266,336,70,NULL,4),(377,1010,266,337,80,NULL,4),(378,1010,266,338,90,NULL,4),(379,1010,266,340,100,NULL,4),(380,1010,266,343,110,NULL,4),(381,1010,266,344,120,NULL,4),(382,1010,267,332,14,NULL,4),(383,1010,267,345,10,NULL,4),(384,1010,267,346,20,NULL,4),(385,1010,267,347,30,NULL,4),(386,1010,267,348,40,NULL,4),(387,1010,267,349,50,NULL,4),(388,1010,267,335,60,NULL,4),(389,1010,267,336,70,NULL,4),(390,1010,267,338,80,NULL,4),(391,1010,267,350,90,NULL,4),(393,1010,267,352,110,NULL,4),(394,1010,267,353,120,NULL,4),(396,1010,267,355,140,NULL,4),(397,1010,268,332,17,NULL,4),(398,1010,268,345,10,NULL,4),(399,1010,268,356,20,NULL,4),(400,1010,268,346,30,NULL,4),(401,1010,268,347,40,NULL,4),(402,1010,268,357,50,NULL,4),(403,1010,268,348,60,NULL,4),(404,1010,268,349,70,NULL,4),(405,1010,268,335,80,NULL,4),(406,1010,268,350,90,NULL,4),(408,1010,268,358,110,NULL,4),(409,1010,268,256,120,NULL,4),(411,1010,268,355,140,NULL,4),(412,1010,268,353,150,NULL,4),(413,1010,268,352,160,NULL,4),(414,1010,268,361,170,NULL,4),(415,1010,269,362,NULL,NULL,4),(416,1010,269,363,10,NULL,4),(417,1010,269,351,20,NULL,4),(418,1010,269,358,30,NULL,4),(419,1010,269,256,40,NULL,4),(420,1010,269,364,50,NULL,4),(421,1010,269,353,60,NULL,4),(422,1010,269,366,70,NULL,4),(423,1010,270,332,14,NULL,4),(424,1010,270,356,10,NULL,4),(425,1010,270,346,20,NULL,4),(426,1010,270,357,30,NULL,4),(427,1010,270,367,40,NULL,4),(428,1010,270,348,50,NULL,4),(429,1010,270,349,60,NULL,4),(430,1010,270,344,70,NULL,4),(431,1010,270,350,80,NULL,4),(433,1010,270,358,100,NULL,4),(435,1010,270,363,120,NULL,4),(436,1010,270,353,130,NULL,4),(437,1010,270,366,140,NULL,4),(438,1010,271,368,19,NULL,4),(439,1010,271,369,10,NULL,4),(440,1010,271,332,20,NULL,4),(441,1010,271,370,30,NULL,4),(442,1010,271,356,40,NULL,4),(443,1010,271,346,50,NULL,4),(444,1010,271,347,60,NULL,4),(445,1010,271,357,70,NULL,4),(446,1010,271,349,80,NULL,4),(447,1010,271,301,90,NULL,4),(448,1010,271,371,100,NULL,4),(449,1010,271,372,110,NULL,4),(450,1010,271,353,120,NULL,4),(458,1010,272,376,NULL,NULL,4),(459,1010,272,256,10,NULL,4),(460,1010,272,375,20,NULL,4),(461,1010,272,377,30,NULL,4),(462,1010,272,333,40,NULL,4),(463,1010,272,378,50,NULL,4),(464,1010,272,379,60,NULL,4),(465,1010,273,333,NULL,NULL,4),(466,1010,273,380,10,NULL,4),(467,1010,273,381,20,NULL,4),(468,1010,273,146,30,NULL,4),(469,1010,273,382,40,NULL,4),(470,1010,273,383,50,NULL,4),(471,1010,273,384,60,NULL,4),(472,1010,273,344,70,NULL,4),(473,1010,273,385,80,NULL,4),(474,1010,273,386,90,NULL,4),(475,1010,273,387,100,NULL,4),(476,1010,274,388,NULL,NULL,4),(477,1010,274,389,10,NULL,4),(478,1010,274,390,20,NULL,4),(479,1010,274,333,30,NULL,4),(480,1010,275,356,NULL,NULL,4),(481,1010,275,391,10,NULL,4),(482,1010,275,392,20,NULL,4),(483,1010,275,350,30,NULL,4),(484,1010,275,393,40,NULL,4),(485,1010,275,344,50,NULL,4),(486,1010,275,256,60,NULL,4),(487,1010,275,394,70,NULL,4),(488,1010,275,395,80,NULL,4),(489,1010,275,363,90,NULL,4),(490,1010,276,333,NULL,NULL,4),(491,1010,276,380,10,NULL,4),(492,1010,276,344,20,NULL,4),(493,1010,276,396,30,NULL,4),(494,1010,276,397,40,NULL,4),(495,1010,276,398,50,NULL,4),(496,1010,276,378,60,NULL,4),(497,1010,276,399,70,NULL,4),(498,1010,276,400,80,NULL,4),(499,1010,276,363,90,NULL,4),(500,1010,276,341,100,NULL,4),(501,1010,277,380,NULL,NULL,4),(502,1010,278,385,NULL,NULL,4),(503,1010,278,386,10,NULL,4),(504,1010,278,396,20,NULL,4),(505,1010,278,397,30,NULL,4),(506,1010,279,401,NULL,NULL,4),(507,1010,280,402,NULL,NULL,4),(508,1010,281,403,NULL,NULL,4),(509,1010,282,404,NULL,NULL,4),(510,1010,283,405,NULL,NULL,4),(511,1010,284,406,NULL,NULL,4),(512,1010,285,407,NULL,NULL,4),(513,1010,286,408,NULL,NULL,4),(514,1010,287,409,NULL,NULL,4),(515,1010,288,410,NULL,NULL,4),(516,1010,289,411,NULL,NULL,4),(517,1010,290,412,NULL,NULL,4),(518,1010,291,413,NULL,NULL,4),(519,1010,292,414,NULL,NULL,4),(520,1010,293,415,NULL,NULL,4),(521,1010,294,416,NULL,NULL,4),(522,1010,295,417,NULL,NULL,4),(523,1010,296,418,NULL,NULL,4),(524,1010,296,419,10,NULL,4),(525,1010,297,420,NULL,NULL,4),(526,1010,298,421,NULL,NULL,4),(527,1010,299,422,NULL,NULL,4),(528,1010,300,423,NULL,NULL,4),(529,1010,301,424,NULL,NULL,4),(530,1010,302,425,NULL,NULL,4),(531,1010,303,426,NULL,NULL,4),(532,1010,304,427,NULL,NULL,4),(533,1010,305,29,NULL,1,4),(534,1010,305,27,10,2,4),(535,1010,305,32,20,NULL,4),(536,1010,305,26,30,1,4),(537,1010,306,428,NULL,NULL,4),(538,1010,306,429,10,NULL,4),(539,1010,307,430,NULL,NULL,4),(540,1010,307,431,10,NULL,4),(541,1010,308,432,NULL,NULL,4),(542,1010,308,433,10,NULL,4),(543,1010,309,434,NULL,NULL,4),(544,1010,309,435,10,NULL,4),(545,1010,310,436,NULL,NULL,4),(546,1010,310,437,10,NULL,4),(547,1010,311,438,NULL,NULL,4),(548,1010,311,439,10,NULL,4),(549,1010,312,440,NULL,NULL,4),(550,1010,312,441,10,NULL,4),(551,1010,312,442,20,NULL,4),(552,1010,313,443,NULL,NULL,4),(553,1010,313,444,10,NULL,4),(554,1010,314,445,NULL,NULL,4),(555,1010,314,442,10,NULL,4),(556,1010,315,446,NULL,NULL,4),(557,1010,315,447,10,NULL,4),(558,1010,316,448,NULL,NULL,4),(559,1010,316,449,10,NULL,4),(560,1010,317,450,NULL,NULL,4),(561,1010,317,451,10,NULL,4),(562,1010,318,452,NULL,NULL,4),(563,1010,318,453,10,NULL,4),(564,1010,319,454,NULL,NULL,4),(565,1010,319,455,10,NULL,4),(566,1010,320,456,NULL,NULL,4),(567,1010,320,457,10,NULL,4),(568,1010,321,458,NULL,NULL,4),(569,1010,321,459,10,NULL,4),(570,1010,322,460,NULL,NULL,4),(571,1010,322,461,10,NULL,4),(572,1010,323,462,NULL,NULL,4),(573,1010,323,463,10,NULL,4),(574,1010,324,464,NULL,NULL,4),(575,1010,324,465,10,NULL,4),(576,1010,325,466,NULL,NULL,4),(577,1010,325,467,10,NULL,4),(578,1010,326,468,NULL,NULL,4),(579,1010,326,469,10,NULL,4),(580,1010,327,470,NULL,NULL,4),(581,1010,327,471,10,NULL,4),(582,1010,328,472,NULL,NULL,4),(583,1010,328,473,10,NULL,4),(584,1010,329,474,NULL,NULL,4),(585,1010,329,475,10,NULL,4),(586,1010,330,476,NULL,NULL,4),(587,1010,330,477,10,NULL,4),(588,1010,331,478,NULL,NULL,4),(589,1010,331,479,10,NULL,4),(590,1010,332,480,NULL,NULL,4),(591,1010,332,481,10,NULL,4),(592,1010,333,482,NULL,NULL,4),(593,1010,333,483,10,NULL,4),(594,1010,334,484,NULL,NULL,4),(595,1010,334,485,10,NULL,4),(596,1010,335,486,NULL,NULL,4),(597,1010,335,487,10,NULL,4),(598,1010,336,488,NULL,NULL,4),(599,1010,336,489,10,NULL,4),(600,1010,337,490,NULL,NULL,4),(601,1010,337,491,10,NULL,4),(602,1010,338,492,NULL,NULL,4),(603,1010,338,493,10,NULL,4),(604,1010,339,494,NULL,NULL,4),(605,1010,339,495,10,NULL,4),(606,1010,340,496,NULL,NULL,4),(607,1010,340,497,10,NULL,4),(608,1010,341,498,NULL,NULL,4),(609,1010,341,499,10,NULL,4),(610,1010,342,500,NULL,NULL,4),(611,1010,342,501,10,NULL,4),(612,1010,343,502,NULL,NULL,4),(613,1010,343,503,10,NULL,4),(614,1010,344,504,NULL,NULL,4),(615,1010,344,505,10,NULL,4),(616,1010,345,506,NULL,NULL,4),(617,1010,345,507,10,NULL,4),(618,1010,346,508,NULL,NULL,4),(619,1010,346,509,10,NULL,4),(620,1010,347,510,NULL,NULL,4),(621,1010,347,511,10,NULL,4),(622,1010,348,512,NULL,NULL,4),(623,1010,348,513,10,NULL,4),(624,1010,349,514,NULL,NULL,4),(625,1010,349,515,10,NULL,4),(626,1010,350,516,NULL,NULL,4),(627,1010,350,517,10,NULL,4),(628,1010,351,518,NULL,NULL,4),(629,1010,351,519,10,NULL,4),(630,1010,352,520,NULL,NULL,4),(631,1010,352,521,10,NULL,4),(632,1010,353,522,NULL,NULL,4),(633,1010,353,523,10,NULL,4),(634,1010,354,524,NULL,NULL,4),(635,1010,354,525,10,NULL,4),(636,1010,355,526,NULL,NULL,4),(637,1010,355,527,10,NULL,4),(638,1010,356,528,NULL,NULL,4),(639,1010,356,529,10,NULL,4),(640,1010,357,530,NULL,NULL,4),(641,1010,357,531,10,NULL,4),(642,1010,358,532,NULL,NULL,4),(643,1010,358,533,10,NULL,4),(644,1010,359,534,NULL,NULL,4),(645,1010,359,535,10,NULL,4),(646,1010,360,536,NULL,NULL,4),(647,1010,360,537,10,NULL,4),(648,1010,361,538,NULL,NULL,4),(649,1010,361,503,10,NULL,4),(650,1010,362,539,NULL,NULL,4),(651,1010,362,507,10,NULL,4),(652,1010,363,540,NULL,NULL,4),(653,1010,363,541,10,NULL,4),(654,1010,364,542,NULL,NULL,4),(655,1010,364,543,10,NULL,4),(656,1010,365,544,NULL,NULL,4),(657,1010,365,545,10,NULL,4),(658,1010,366,546,NULL,NULL,4),(659,1010,366,547,10,NULL,4),(660,1010,367,548,NULL,NULL,4),(661,1010,367,549,10,NULL,4),(662,1010,368,550,NULL,NULL,4),(663,1010,368,551,10,NULL,4),(664,1010,369,552,NULL,NULL,4),(665,1010,369,553,10,NULL,4),(666,1010,370,554,NULL,NULL,4),(667,1010,370,555,10,NULL,4),(668,1010,371,556,NULL,NULL,4),(669,1010,371,557,10,NULL,4),(670,1010,372,558,NULL,NULL,4),(671,1010,372,559,10,NULL,4),(672,1010,373,560,NULL,NULL,4),(673,1010,373,505,10,NULL,4),(674,1010,374,561,NULL,NULL,4),(675,1010,374,562,10,NULL,4),(676,1010,375,563,NULL,NULL,4),(677,1010,375,564,10,NULL,4),(678,1010,376,565,NULL,NULL,4),(679,1010,376,566,10,NULL,4),(680,1010,377,567,NULL,NULL,4),(681,1010,377,568,10,NULL,4),(682,1010,378,569,NULL,NULL,4),(683,1010,378,570,10,NULL,4),(684,1010,379,571,NULL,NULL,4),(685,1010,379,572,10,NULL,4),(686,1010,380,573,NULL,NULL,4),(687,1010,380,574,10,NULL,4),(688,1010,381,575,NULL,NULL,4),(689,1010,381,576,10,NULL,4),(690,1010,382,577,NULL,NULL,4),(691,1010,382,578,10,NULL,4),(692,1010,383,579,NULL,NULL,4),(693,1010,383,580,10,NULL,4),(694,1010,384,581,NULL,NULL,4),(695,1010,384,505,10,NULL,4),(696,1010,385,582,NULL,NULL,4),(697,1010,385,583,10,NULL,4),(698,1010,386,584,NULL,NULL,4),(699,1010,386,585,10,NULL,4),(700,1010,387,586,NULL,NULL,4),(701,1010,387,578,10,NULL,4),(702,1010,388,587,NULL,NULL,4),(703,1010,388,588,10,NULL,4),(704,1010,389,589,NULL,NULL,4),(705,1010,389,590,10,NULL,4),(706,1010,390,591,NULL,NULL,4),(707,1010,390,592,10,NULL,4),(708,1010,391,593,NULL,NULL,4),(709,1010,391,594,10,NULL,4),(710,1010,392,595,NULL,NULL,4),(711,1010,392,596,10,NULL,4),(712,1010,393,597,NULL,NULL,4),(713,1010,393,598,10,NULL,4),(714,1010,394,599,NULL,NULL,4),(715,1010,394,600,10,NULL,4),(716,1010,395,601,NULL,NULL,4),(717,1010,395,602,10,NULL,4),(718,1010,396,603,NULL,NULL,4),(719,1010,396,604,10,NULL,4),(720,1010,397,605,NULL,NULL,4),(721,1010,397,606,10,NULL,4),(722,1010,398,607,NULL,NULL,4),(723,1010,398,608,10,NULL,4),(724,1010,399,609,NULL,NULL,4),(725,1010,399,610,10,NULL,4),(726,1010,401,611,NULL,NULL,4),(727,1010,401,612,10,NULL,4),(728,1010,401,613,20,NULL,4),(729,1010,402,614,NULL,NULL,4),(730,1010,402,314,10,NULL,4),(731,1010,402,616,20,NULL,4),(732,1010,402,617,30,NULL,4),(733,1010,403,301,NULL,NULL,4),(734,1010,403,618,10,NULL,4),(735,1010,404,619,NULL,NULL,4),(736,1010,404,620,10,NULL,4),(737,1010,405,621,NULL,NULL,4),(738,1010,405,622,10,NULL,4),(739,1010,406,623,NULL,NULL,4),(740,1010,406,624,10,NULL,4),(741,1010,407,625,10,NULL,4),(752,1010,410,628,NULL,NULL,4),(753,1010,410,629,10,NULL,4),(754,1010,410,245,20,NULL,4),(757,1010,411,625,10,NULL,4),(761,1010,412,632,20,NULL,4),(762,1010,412,627,10,NULL,4),(765,1010,413,634,20,NULL,4),(768,1010,414,363,NULL,NULL,4),(769,1010,414,636,10,NULL,4),(770,1010,414,637,20,NULL,4),(771,1010,414,638,30,NULL,4),(772,1010,414,639,40,NULL,4),(773,1010,414,640,50,NULL,4),(775,1010,415,641,20,NULL,4),(776,1010,415,627,10,NULL,4),(778,1010,417,159,NULL,4,4),(779,1010,417,321,10,NULL,4),(780,1010,417,642,20,NULL,4),(781,1010,417,643,30,NULL,4),(782,1010,417,644,40,NULL,4),(783,1010,417,172,50,4,4),(784,1010,417,322,60,NULL,4),(785,1010,417,645,70,NULL,4),(786,1010,417,646,80,NULL,4),(787,1010,417,647,90,NULL,4),(788,1010,418,324,NULL,NULL,4),(789,1010,418,648,10,NULL,4),(790,1010,418,325,20,NULL,4),(791,1010,419,430,NULL,NULL,4),(792,1010,419,443,10,NULL,4),(793,1010,419,492,20,NULL,4),(794,1010,419,502,30,NULL,4),(795,1010,419,504,40,NULL,4),(796,1010,419,510,50,NULL,4),(797,1010,419,520,60,NULL,4),(798,1010,419,441,70,NULL,4),(799,1010,419,439,80,NULL,4),(800,1010,419,442,90,NULL,4),(801,1010,419,469,100,NULL,4),(802,1010,419,483,110,NULL,4),(803,1010,419,497,120,NULL,4),(804,1010,419,529,130,NULL,4),(805,1010,419,531,140,NULL,4),(806,1010,419,649,150,NULL,4),(807,1010,420,650,NULL,1,4),(808,1010,421,651,NULL,1,4),(809,1010,422,44,NULL,NULL,4),(810,1010,422,652,10,NULL,4),(811,1010,422,653,20,NULL,4),(812,1010,423,654,NULL,NULL,4),(813,1010,425,655,NULL,NULL,4),(814,1010,425,656,10,NULL,4),(815,1010,426,657,NULL,NULL,4),(816,1010,426,658,10,NULL,4),(817,1010,426,659,20,NULL,4),(818,1010,427,370,NULL,NULL,4),(819,1010,428,581,NULL,NULL,4),(820,1010,428,587,10,NULL,4),(821,1010,428,418,20,NULL,4),(822,1010,428,621,30,NULL,4),(823,1010,428,623,40,NULL,4),(824,1010,429,660,NULL,NULL,4),(825,1010,429,661,10,NULL,4),(826,1010,429,662,20,NULL,4),(827,1010,431,663,NULL,NULL,4),(828,1010,432,151,NULL,2,4),(829,1010,432,155,10,3,4),(830,1010,432,166,20,NULL,4),(831,1010,432,167,30,NULL,4),(832,1010,432,168,40,NULL,4),(833,1010,432,172,50,4,4),(834,1010,432,178,60,NULL,4),(835,1010,432,664,70,1,4),(836,1010,432,665,80,NULL,4),(837,1010,432,666,90,NULL,4),(838,1010,432,667,100,NULL,4),(839,1010,432,668,110,5,4),(840,1010,432,669,120,6,4),(841,1010,432,670,130,7,4),(842,1010,432,671,140,8,4),(843,1010,432,672,150,9,4),(844,1010,432,673,160,NULL,4),(845,1010,433,151,NULL,2,4),(846,1010,433,166,10,NULL,4),(847,1010,433,167,20,NULL,4),(848,1010,433,168,30,NULL,4),(849,1010,433,172,40,4,4),(850,1010,433,178,50,NULL,4),(851,1010,433,664,60,1,4),(852,1010,433,668,70,5,4),(853,1010,433,669,80,6,4),(854,1010,433,670,90,7,4),(855,1010,433,671,100,8,4),(856,1010,433,672,110,9,4),(857,1010,433,674,120,3,4),(858,1010,433,675,130,NULL,4),(859,1010,433,676,140,NULL,4),(860,1010,433,677,150,NULL,4),(861,1010,433,678,160,NULL,4),(862,1010,434,151,NULL,2,4),(863,1010,434,166,10,NULL,4),(864,1010,434,167,20,NULL,4),(865,1010,434,168,30,NULL,4),(866,1010,434,172,40,4,4),(867,1010,434,178,50,NULL,4),(868,1010,434,664,60,1,4),(869,1010,434,665,70,NULL,4),(870,1010,434,667,80,NULL,4),(871,1010,434,668,90,5,4),(872,1010,434,669,100,6,4),(873,1010,434,670,110,7,4),(874,1010,434,671,120,8,4),(875,1010,434,672,130,9,4),(876,1010,434,673,140,NULL,4),(877,1010,434,674,150,3,4),(878,1010,434,679,160,NULL,4),(879,1010,435,151,NULL,2,4),(880,1010,435,166,10,NULL,4),(881,1010,435,167,20,NULL,4),(882,1010,435,168,30,NULL,4),(883,1010,435,172,40,4,4),(884,1010,435,178,50,NULL,4),(885,1010,435,664,60,1,4),(886,1010,435,668,70,5,4),(887,1010,435,669,80,6,4),(888,1010,435,670,90,7,4),(889,1010,435,671,100,8,4),(890,1010,435,672,110,9,4),(891,1010,435,673,120,NULL,4),(892,1010,435,674,130,3,4),(893,1010,435,675,140,NULL,4),(894,1010,435,677,150,NULL,4),(895,1010,435,680,160,NULL,4),(896,1010,436,151,NULL,2,4),(897,1010,436,166,10,NULL,4),(898,1010,436,167,20,NULL,4),(899,1010,436,168,30,NULL,4),(900,1010,436,172,40,4,4),(901,1010,436,178,50,NULL,4),(902,1010,436,664,60,1,4),(903,1010,436,665,70,NULL,4),(904,1010,436,667,80,NULL,4),(905,1010,436,668,90,5,4),(906,1010,436,669,100,6,4),(907,1010,436,670,110,7,4),(908,1010,436,671,120,8,4),(909,1010,436,672,130,9,4),(910,1010,436,673,140,NULL,4),(911,1010,436,674,150,3,4),(912,1010,436,679,160,NULL,4),(913,1010,437,151,NULL,NULL,4),(914,1010,437,166,10,NULL,4),(915,1010,437,167,20,NULL,4),(916,1010,437,168,30,NULL,4),(917,1010,437,172,40,NULL,4),(918,1010,437,178,50,NULL,4),(919,1010,437,664,60,NULL,4),(920,1010,437,665,70,NULL,4),(921,1010,437,667,80,NULL,4),(922,1010,437,668,90,NULL,4),(923,1010,437,669,100,NULL,4),(924,1010,437,670,110,NULL,4),(925,1010,437,671,120,NULL,4),(926,1010,437,672,130,NULL,4),(927,1010,437,673,140,NULL,4),(928,1010,437,674,150,NULL,4),(929,1010,437,679,160,NULL,4),(930,1010,438,151,NULL,2,4),(931,1010,438,166,10,NULL,4),(932,1010,438,167,20,NULL,4),(933,1010,438,168,30,NULL,4),(934,1010,438,172,40,4,4),(935,1010,438,178,50,NULL,4),(936,1010,438,665,60,NULL,4),(937,1010,438,666,70,NULL,4),(938,1010,438,667,80,NULL,4),(939,1010,438,668,90,5,4),(940,1010,438,669,100,6,4),(941,1010,438,670,110,7,4),(942,1010,438,671,120,8,4),(943,1010,438,672,130,9,4),(944,1010,438,673,140,NULL,4),(945,1010,438,674,150,3,4),(946,1010,438,681,160,1,4),(947,1010,439,151,NULL,2,4),(948,1010,439,166,10,NULL,4),(949,1010,439,167,20,NULL,4),(950,1010,439,168,30,NULL,4),(951,1010,439,172,40,4,4),(952,1010,439,178,50,NULL,4),(953,1010,439,664,60,1,4),(954,1010,439,665,70,NULL,4),(955,1010,439,666,80,NULL,4),(956,1010,439,667,90,NULL,4),(957,1010,439,668,100,5,4),(958,1010,439,669,110,6,4),(959,1010,439,670,120,7,4),(960,1010,439,671,130,8,4),(961,1010,439,672,140,9,4),(962,1010,439,673,150,NULL,4),(963,1010,439,674,160,3,4),(964,1010,440,151,NULL,2,4),(965,1010,440,166,10,NULL,4),(966,1010,440,167,20,NULL,4),(967,1010,440,168,30,NULL,4),(968,1010,440,172,40,4,4),(969,1010,440,178,50,NULL,4),(970,1010,440,664,60,1,4),(971,1010,440,665,70,NULL,4),(972,1010,440,666,80,NULL,4),(973,1010,440,667,90,NULL,4),(974,1010,440,668,100,5,4),(975,1010,440,669,110,6,4),(976,1010,440,670,120,7,4),(977,1010,440,671,130,8,4),(978,1010,440,672,140,9,4),(979,1010,440,673,150,NULL,4),(980,1010,440,674,160,3,4),(981,1010,441,151,NULL,2,4),(982,1010,441,166,10,NULL,4),(983,1010,441,167,20,NULL,4),(984,1010,441,168,30,NULL,4),(985,1010,441,172,40,4,4),(986,1010,441,178,50,NULL,4),(987,1010,441,665,60,NULL,4),(988,1010,441,666,70,NULL,4),(989,1010,441,667,80,NULL,4),(990,1010,441,668,90,5,4),(991,1010,441,669,100,6,4),(992,1010,441,670,110,7,4),(993,1010,441,671,120,8,4),(994,1010,441,672,130,9,4),(995,1010,441,673,140,NULL,4),(996,1010,441,674,150,3,4),(997,1010,441,681,160,1,4),(998,1010,442,151,NULL,2,4),(999,1010,442,166,10,NULL,4),(1000,1010,442,167,20,NULL,4),(1001,1010,442,168,30,NULL,4),(1002,1010,442,172,40,4,4),(1003,1010,442,178,50,NULL,4),(1004,1010,442,665,60,NULL,4),(1005,1010,442,666,70,NULL,4),(1006,1010,442,667,80,NULL,4),(1007,1010,442,668,90,5,4),(1008,1010,442,669,100,6,4),(1009,1010,442,670,110,7,4),(1010,1010,442,671,120,8,4),(1011,1010,442,672,130,9,4),(1012,1010,442,673,140,NULL,4),(1013,1010,442,674,150,3,4),(1014,1010,442,681,160,1,4),(1015,1010,443,151,NULL,2,4),(1016,1010,443,166,10,NULL,4),(1017,1010,443,167,20,NULL,4),(1018,1010,443,168,30,NULL,4),(1019,1010,443,172,40,4,4),(1020,1010,443,665,50,NULL,4),(1021,1010,443,666,60,NULL,4),(1022,1010,443,667,70,NULL,4),(1023,1010,443,668,80,5,4),(1024,1010,443,669,90,6,4),(1025,1010,443,670,100,7,4),(1026,1010,443,671,110,8,4),(1027,1010,443,672,120,9,4),(1028,1010,443,673,130,NULL,4),(1029,1010,443,674,140,3,4),(1030,1010,443,681,150,1,4),(1031,1010,443,682,160,NULL,4),(1032,1010,444,538,NULL,NULL,4),(1033,1010,444,577,10,NULL,4),(1034,1010,444,442,20,NULL,4),(1035,1010,444,523,30,NULL,4),(1036,1010,444,507,40,NULL,4),(1037,1010,444,566,50,NULL,4),(1038,1010,444,505,60,NULL,4),(1039,1010,444,610,70,NULL,4),(1040,1010,444,683,80,NULL,4),(1041,1010,444,649,90,NULL,4),(1042,1010,445,442,NULL,NULL,4),(1043,1010,445,497,10,NULL,4),(1044,1010,445,505,20,NULL,4),(1045,1010,445,511,30,NULL,4),(1046,1010,445,596,40,NULL,4),(1047,1010,445,683,50,NULL,4),(1048,1010,445,684,60,NULL,4),(1049,1010,445,685,70,NULL,4),(1050,1010,445,649,80,NULL,4),(1051,1010,446,581,NULL,NULL,4),(1052,1010,446,475,10,NULL,4),(1053,1010,446,503,20,NULL,4),(1054,1010,446,686,30,NULL,4),(1055,1010,446,687,40,NULL,4),(1056,1010,446,688,50,NULL,4),(1057,1010,446,649,60,NULL,4),(1058,1010,446,689,90,NULL,4),(1059,1010,447,470,NULL,NULL,4),(1060,1010,447,431,10,NULL,4),(1061,1010,447,497,20,NULL,4),(1062,1010,447,505,30,NULL,4),(1063,1010,447,596,40,NULL,4),(1064,1010,447,683,50,NULL,4),(1065,1010,447,687,60,NULL,4),(1066,1010,447,688,70,NULL,4),(1067,1010,447,689,80,NULL,4),(1068,1010,447,649,90,NULL,4),(1069,1010,447,690,120,NULL,4),(1070,1010,448,581,NULL,NULL,4),(1071,1010,448,442,10,NULL,4),(1072,1010,448,503,20,NULL,4),(1073,1010,448,523,30,NULL,4),(1074,1010,448,529,40,NULL,4),(1075,1010,448,507,50,NULL,4),(1076,1010,448,505,60,NULL,4),(1077,1010,448,578,70,NULL,4),(1078,1010,448,610,80,NULL,4),(1079,1010,448,649,90,NULL,4),(1080,1010,449,440,NULL,NULL,4),(1081,1010,449,538,10,NULL,4),(1082,1010,449,565,20,NULL,4),(1083,1010,449,497,30,NULL,4),(1084,1010,449,505,40,NULL,4),(1085,1010,449,523,50,NULL,4),(1086,1010,449,507,60,NULL,4),(1087,1010,449,566,70,NULL,4),(1088,1010,449,578,80,NULL,4),(1089,1010,449,610,90,NULL,4),(1090,1010,449,683,100,NULL,4),(1091,1010,449,687,110,NULL,4),(1092,1010,449,688,120,NULL,4),(1093,1010,449,689,130,NULL,4),(1094,1010,449,649,140,NULL,4),(1095,1010,449,691,210,NULL,4),(1096,1010,449,692,220,NULL,4),(1097,1010,450,468,NULL,NULL,4),(1098,1010,450,504,10,NULL,4),(1099,1010,450,538,20,NULL,4),(1100,1010,450,575,30,NULL,4),(1101,1010,450,599,40,NULL,4),(1102,1010,450,439,50,NULL,4),(1103,1010,450,493,60,NULL,4),(1104,1010,450,511,70,NULL,4),(1105,1010,450,531,80,NULL,4),(1106,1010,450,598,90,NULL,4),(1107,1010,450,604,100,NULL,4),(1108,1010,450,649,110,NULL,4),(1109,1010,451,428,NULL,NULL,4),(1110,1010,451,577,10,NULL,4),(1111,1010,451,581,20,NULL,4),(1112,1010,451,609,30,NULL,4),(1113,1010,451,483,40,NULL,4),(1114,1010,451,505,50,NULL,4),(1115,1010,451,523,60,NULL,4),(1116,1010,451,527,70,NULL,4),(1117,1010,451,529,80,NULL,4),(1118,1010,451,507,90,NULL,4),(1119,1010,451,683,100,NULL,4),(1120,1010,451,693,110,NULL,4),(1121,1010,451,688,120,NULL,4),(1122,1010,451,649,130,NULL,4),(1123,1010,451,694,240,NULL,4),(1124,1010,452,695,NULL,NULL,4),(1125,1010,453,333,NULL,NULL,4),(1126,1010,453,363,10,NULL,4),(1127,1010,453,344,20,NULL,4),(1128,1010,453,392,30,NULL,4),(1129,1010,453,350,40,NULL,4),(1130,1010,453,696,50,NULL,4),(1131,1010,454,333,NULL,NULL,4),(1132,1010,454,363,10,NULL,4),(1133,1010,454,344,20,NULL,4),(1134,1010,454,392,30,NULL,4),(1135,1010,454,350,40,NULL,4),(1136,1010,455,333,NULL,NULL,4),(1137,1010,455,344,10,NULL,4),(1138,1010,455,392,20,NULL,4),(1139,1010,456,697,NULL,NULL,4),(1140,1010,457,698,NULL,NULL,4),(1141,1010,458,333,NULL,NULL,4),(1142,1010,458,344,10,NULL,4),(1143,1010,458,699,20,NULL,4),(1144,1010,458,700,30,NULL,4),(1145,1010,458,701,40,NULL,4),(1146,1010,458,702,50,NULL,4),(1147,1010,458,703,60,NULL,4),(1148,1010,459,704,NULL,NULL,4),(1149,1010,460,705,NULL,NULL,4),(1150,1010,461,673,NULL,NULL,4),(1151,1010,461,397,10,NULL,4),(1152,1010,461,706,20,NULL,4),(1153,1010,461,707,30,NULL,4),(1154,1010,461,708,40,NULL,4),(1155,1010,461,709,50,NULL,4),(1156,1010,462,333,NULL,NULL,4),(1157,1010,462,344,10,NULL,4),(1158,1010,462,392,20,NULL,4),(1159,1010,462,350,30,NULL,4),(1160,1010,462,710,40,NULL,4),(1161,1010,463,344,NULL,NULL,4),(1162,1010,463,710,10,NULL,4),(1163,1010,464,333,NULL,NULL,4),(1164,1010,464,363,10,NULL,4),(1165,1010,464,711,20,NULL,4),(1166,1010,464,712,30,NULL,4),(1167,1010,464,713,40,NULL,4),(1168,1010,464,703,50,NULL,4),(1169,1010,465,333,NULL,NULL,4),(1170,1010,465,703,10,NULL,4),(1171,1010,465,392,20,NULL,4),(1172,1010,465,713,30,NULL,4),(1173,1010,466,714,NULL,NULL,4),(1174,1010,466,713,10,NULL,4),(1175,1010,467,714,NULL,NULL,4),(1176,1010,467,713,10,NULL,4),(1177,1010,468,430,NULL,NULL,4),(1178,1010,468,438,10,NULL,4),(1179,1010,468,443,20,NULL,4),(1180,1010,468,445,30,NULL,4),(1181,1010,468,468,40,NULL,4),(1182,1010,468,474,50,NULL,4),(1183,1010,468,482,60,NULL,4),(1184,1010,468,492,70,NULL,4),(1185,1010,468,502,80,NULL,4),(1186,1010,468,504,90,NULL,4),(1187,1010,468,510,100,NULL,4),(1188,1010,468,520,110,NULL,4),(1189,1010,468,528,120,NULL,4),(1190,1010,468,530,130,NULL,4),(1191,1010,468,649,140,NULL,4),(1192,100,413,715,10,NULL,4),(1193,100,407,716,20,NULL,4),(1194,100,411,717,20,NULL,4),(1195,100,408,718,10,NULL,4),(1196,100,408,719,20,NULL,4),(1197,100,239,720,20,NULL,4),(1198,100,239,721,30,NULL,4),(1199,1000,469,571,1,NULL,4),(1200,1000,469,753,2,NULL,4),(1201,1000,469,565,3,NULL,4),(1202,1000,469,749,4,NULL,4),(1203,1000,469,440,5,NULL,4),(1204,1000,469,726,6,NULL,4),(1205,1000,469,474,7,NULL,4),(1206,1000,469,733,8,NULL,4),(1207,1000,469,496,9,NULL,4),(1208,1000,469,737,10,NULL,4),(1209,1000,469,502,11,NULL,4),(1210,1000,469,738,12,NULL,4),(1211,1000,469,504,13,NULL,4),(1212,1000,469,739,14,NULL,4),(1213,1000,469,581,15,NULL,4),(1214,1000,469,757,16,NULL,4),(1215,1000,470,571,1,NULL,4),(1216,1000,470,753,2,NULL,4),(1217,1000,470,565,3,NULL,4),(1218,1000,470,749,4,NULL,4),(1219,1000,470,482,5,NULL,4),(1220,1000,470,734,6,NULL,4),(1221,1000,470,528,7,NULL,4),(1222,1000,470,745,8,NULL,4),(1223,1000,470,534,9,NULL,4),(1224,1000,470,747,10,NULL,4),(1225,1000,470,603,11,NULL,4),(1226,1000,470,761,12,NULL,4),(1227,1000,470,522,13,NULL,4),(1228,1000,470,743,14,NULL,4),(1229,1000,470,539,15,NULL,4),(1230,1000,470,748,16,NULL,4),(1231,1000,470,577,17,NULL,4),(1232,1000,470,756,18,NULL,4),(1233,1000,470,595,19,NULL,4),(1234,1000,470,758,20,NULL,4),(1235,1000,470,569,21,NULL,4),(1236,1000,470,752,22,NULL,4),(1237,1000,470,504,23,NULL,4),(1238,1000,470,739,24,NULL,4),(1239,1000,470,609,25,NULL,4),(1240,1000,470,762,26,NULL,4),(1241,1000,470,502,27,NULL,4),(1242,1000,470,738,28,NULL,4),(1243,1000,470,428,29,NULL,4),(1244,1000,470,723,30,NULL,4),(1245,1000,470,526,31,NULL,4),(1246,1000,470,744,32,NULL,4),(1247,1000,470,510,33,NULL,4),(1248,1000,470,741,34,NULL,4),(1249,1000,471,571,1,NULL,4),(1250,1000,471,753,2,NULL,4),(1251,1000,471,565,3,NULL,4),(1252,1000,471,749,4,NULL,4),(1253,1000,471,440,5,NULL,4),(1254,1000,471,726,6,NULL,4),(1255,1000,471,474,7,NULL,4),(1256,1000,471,733,8,NULL,4),(1257,1000,471,528,9,NULL,4),(1258,1000,471,745,10,NULL,4),(1259,1000,471,534,11,NULL,4),(1260,1000,471,747,12,NULL,4),(1261,1000,471,595,13,NULL,4),(1262,1000,471,758,14,NULL,4),(1263,1000,471,522,15,NULL,4),(1264,1000,471,743,16,NULL,4),(1265,1000,471,539,17,NULL,4),(1266,1000,471,748,18,NULL,4),(1267,1000,471,577,19,NULL,4),(1268,1000,471,756,20,NULL,4),(1269,1000,471,560,21,NULL,4),(1270,1000,471,751,22,NULL,4),(1271,1000,471,502,23,NULL,4),(1272,1000,471,738,24,NULL,4),(1273,1000,471,609,25,NULL,4),(1274,1000,471,762,26,NULL,4),(1275,1000,471,526,27,NULL,4),(1276,1000,471,744,28,NULL,4),(1277,1000,471,510,29,NULL,4),(1278,1000,471,741,30,NULL,4),(1279,1000,472,445,1,NULL,4),(1280,1000,472,728,2,NULL,4),(1281,1000,472,443,3,NULL,4),(1282,1000,472,727,4,NULL,4),(1283,1000,472,460,5,NULL,4),(1284,1000,472,731,6,NULL,4),(1285,1000,472,496,7,NULL,4),(1286,1000,472,737,8,NULL,4),(1287,1000,472,595,9,NULL,4),(1288,1000,472,758,10,NULL,4),(1289,1000,472,502,11,NULL,4),(1290,1000,472,738,12,NULL,4),(1291,1000,472,504,13,NULL,4),(1292,1000,472,739,14,NULL,4),(1293,1000,472,528,15,NULL,4),(1294,1000,472,745,16,NULL,4),(1295,1000,472,534,17,NULL,4),(1296,1000,472,747,18,NULL,4),(1297,1000,472,722,19,NULL,4),(1298,1000,472,730,20,NULL,4),(1299,1000,473,597,1,NULL,4),(1300,1000,473,759,2,NULL,4),(1301,1000,473,599,3,NULL,4),(1302,1000,473,760,4,NULL,4),(1303,1000,473,573,5,NULL,4),(1304,1000,473,754,6,NULL,4),(1305,1000,473,450,7,NULL,4),(1306,1000,473,729,8,NULL,4),(1307,1000,473,490,9,NULL,4),(1308,1000,473,735,10,NULL,4),(1309,1000,473,492,11,NULL,4),(1310,1000,473,736,12,NULL,4),(1311,1000,473,530,13,NULL,4),(1312,1000,473,746,14,NULL,4),(1313,1000,473,528,15,NULL,4),(1314,1000,473,745,16,NULL,4),(1315,1000,473,534,17,NULL,4),(1316,1000,473,747,18,NULL,4),(1317,1000,473,603,19,NULL,4),(1318,1000,473,761,20,NULL,4),(1319,1000,473,438,21,NULL,4),(1320,1000,473,725,22,NULL,4),(1321,1000,473,556,23,NULL,4),(1322,1000,473,750,24,NULL,4),(1323,1000,473,508,25,NULL,4),(1324,1000,473,740,26,NULL,4),(1325,1000,473,502,27,NULL,4),(1326,1000,473,738,28,NULL,4),(1327,1000,473,569,29,NULL,4),(1328,1000,473,752,30,NULL,4),(1329,1000,473,504,31,NULL,4),(1330,1000,473,739,32,NULL,4),(1331,1000,474,597,1,NULL,4),(1332,1000,474,759,2,NULL,4),(1333,1000,474,599,3,NULL,4),(1334,1000,474,760,4,NULL,4),(1335,1000,474,573,5,NULL,4),(1336,1000,474,754,6,NULL,4),(1337,1000,474,575,7,NULL,4),(1338,1000,474,755,8,NULL,4),(1339,1000,474,492,9,NULL,4),(1340,1000,474,736,10,NULL,4),(1341,1000,474,468,11,NULL,4),(1342,1000,474,732,12,NULL,4),(1343,1000,474,530,13,NULL,4),(1344,1000,474,746,14,NULL,4),(1345,1000,474,528,15,NULL,4),(1346,1000,474,745,16,NULL,4),(1347,1000,474,534,17,NULL,4),(1348,1000,474,747,18,NULL,4),(1349,1000,474,556,19,NULL,4),(1350,1000,474,750,20,NULL,4),(1351,1000,474,438,21,NULL,4),(1352,1000,474,725,22,NULL,4),(1353,1000,474,502,23,NULL,4),(1354,1000,474,738,24,NULL,4),(1355,1000,474,595,25,NULL,4),(1356,1000,474,758,26,NULL,4),(1357,1000,474,508,27,NULL,4),(1358,1000,474,740,28,NULL,4),(1359,1000,474,510,29,NULL,4),(1360,1000,474,741,30,NULL,4),(1361,1000,474,504,31,NULL,4),(1362,1000,474,739,32,NULL,4),(1363,1000,475,440,1,NULL,4),(1364,1000,475,726,2,NULL,4),(1365,1000,475,443,3,NULL,4),(1366,1000,475,727,4,NULL,4),(1367,1000,475,597,5,NULL,4),(1368,1000,475,759,6,NULL,4),(1369,1000,475,573,7,NULL,4),(1370,1000,475,754,8,NULL,4),(1371,1000,475,450,9,NULL,4),(1372,1000,475,729,10,NULL,4),(1373,1000,475,530,11,NULL,4),(1374,1000,475,746,12,NULL,4),(1375,1000,475,460,13,NULL,4),(1376,1000,475,731,14,NULL,4),(1377,1000,475,482,15,NULL,4),(1378,1000,475,734,16,NULL,4),(1379,1000,475,496,17,NULL,4),(1380,1000,475,737,18,NULL,4),(1381,1000,475,492,19,NULL,4),(1382,1000,475,736,20,NULL,4),(1383,1000,475,534,21,NULL,4),(1384,1000,475,747,22,NULL,4),(1385,1000,475,603,23,NULL,4),(1386,1000,475,761,24,NULL,4),(1387,1000,475,528,25,NULL,4),(1388,1000,475,745,26,NULL,4),(1389,1000,475,502,27,NULL,4),(1390,1000,475,738,28,NULL,4),(1391,1000,475,508,29,NULL,4),(1392,1000,475,740,30,NULL,4),(1393,1000,475,430,31,NULL,4),(1394,1000,475,724,32,NULL,4),(1395,1000,475,560,33,NULL,4),(1396,1000,475,751,34,NULL,4),(1397,1000,475,504,35,NULL,4),(1398,1000,475,739,36,NULL,4),(1399,1000,475,595,37,NULL,4),(1400,1000,475,758,38,NULL,4),(1401,1000,475,516,39,NULL,4),(1402,1000,475,742,40,NULL,4),(1403,1000,476,440,1,NULL,4),(1404,1000,476,726,2,NULL,4),(1405,1000,476,443,3,NULL,4),(1406,1000,476,727,4,NULL,4),(1407,1000,476,597,5,NULL,4),(1408,1000,476,759,6,NULL,4),(1409,1000,476,573,7,NULL,4),(1410,1000,476,754,8,NULL,4),(1411,1000,476,450,9,NULL,4),(1412,1000,476,729,10,NULL,4),(1413,1000,476,530,11,NULL,4),(1414,1000,476,746,12,NULL,4),(1415,1000,476,460,13,NULL,4),(1416,1000,476,731,14,NULL,4),(1417,1000,476,482,15,NULL,4),(1418,1000,476,734,16,NULL,4),(1419,1000,476,496,17,NULL,4),(1420,1000,476,737,18,NULL,4),(1421,1000,476,492,19,NULL,4),(1422,1000,476,736,20,NULL,4),(1423,1000,476,534,21,NULL,4),(1424,1000,476,747,22,NULL,4),(1425,1000,476,603,23,NULL,4),(1426,1000,476,761,24,NULL,4),(1427,1000,476,528,25,NULL,4),(1428,1000,476,745,26,NULL,4),(1429,1000,476,502,27,NULL,4),(1430,1000,476,738,28,NULL,4),(1431,1000,476,508,29,NULL,4),(1432,1000,476,740,30,NULL,4),(1433,1000,476,430,31,NULL,4),(1434,1000,476,724,32,NULL,4),(1435,1000,476,560,33,NULL,4),(1436,1000,476,751,34,NULL,4),(1437,1000,476,504,35,NULL,4),(1438,1000,476,739,36,NULL,4),(1439,1000,476,595,37,NULL,4),(1440,1000,476,758,38,NULL,4),(1441,1000,476,516,39,NULL,4),(1442,1000,476,742,40,NULL,4),(1443,1000,477,440,1,NULL,4),(1444,1000,477,726,2,NULL,4),(1445,1000,477,443,3,NULL,4),(1446,1000,477,727,4,NULL,4),(1447,1000,477,597,5,NULL,4),(1448,1000,477,759,6,NULL,4),(1449,1000,477,573,7,NULL,4),(1450,1000,477,754,8,NULL,4),(1451,1000,477,450,9,NULL,4),(1452,1000,477,729,10,NULL,4),(1453,1000,477,530,11,NULL,4),(1454,1000,477,746,12,NULL,4),(1455,1000,477,460,13,NULL,4),(1456,1000,477,731,14,NULL,4),(1457,1000,477,482,15,NULL,4),(1458,1000,477,734,16,NULL,4),(1459,1000,477,496,17,NULL,4),(1460,1000,477,737,18,NULL,4),(1461,1000,477,492,19,NULL,4),(1462,1000,477,736,20,NULL,4),(1463,1000,477,534,21,NULL,4),(1464,1000,477,747,22,NULL,4),(1465,1000,477,603,23,NULL,4),(1466,1000,477,761,24,NULL,4),(1467,1000,477,528,25,NULL,4),(1468,1000,477,745,26,NULL,4),(1469,1000,477,502,27,NULL,4),(1470,1000,477,738,28,NULL,4),(1471,1000,477,508,29,NULL,4),(1472,1000,477,740,30,NULL,4),(1473,1000,477,430,31,NULL,4),(1474,1000,477,724,32,NULL,4),(1475,1000,477,560,33,NULL,4),(1476,1000,477,751,34,NULL,4),(1477,1000,477,504,35,NULL,4),(1478,1000,477,739,36,NULL,4),(1479,1000,477,595,37,NULL,4),(1480,1000,477,758,38,NULL,4),(1481,1000,477,516,39,NULL,4),(1482,1000,477,742,40,NULL,4),(1483,1000,478,571,1,NULL,4),(1484,1000,478,793,2,NULL,4),(1485,1000,478,565,3,NULL,4),(1486,1000,478,789,4,NULL,4),(1487,1000,478,440,5,NULL,4),(1488,1000,478,766,6,NULL,4),(1489,1000,478,474,7,NULL,4),(1490,1000,478,773,8,NULL,4),(1491,1000,478,496,9,NULL,4),(1492,1000,478,777,10,NULL,4),(1493,1000,478,502,11,NULL,4),(1494,1000,478,778,12,NULL,4),(1495,1000,478,504,13,NULL,4),(1496,1000,478,779,14,NULL,4),(1497,1000,478,581,15,NULL,4),(1498,1000,478,797,16,NULL,4),(1499,1000,479,571,1,NULL,4),(1500,1000,479,793,2,NULL,4),(1501,1000,479,565,3,NULL,4),(1502,1000,479,789,4,NULL,4),(1503,1000,479,482,5,NULL,4),(1504,1000,479,774,6,NULL,4),(1505,1000,479,528,7,NULL,4),(1506,1000,479,785,8,NULL,4),(1507,1000,479,534,9,NULL,4),(1508,1000,479,787,10,NULL,4),(1509,1000,479,603,11,NULL,4),(1510,1000,479,801,12,NULL,4),(1511,1000,479,522,13,NULL,4),(1512,1000,479,783,14,NULL,4),(1513,1000,479,539,15,NULL,4),(1514,1000,479,788,16,NULL,4),(1515,1000,479,577,17,NULL,4),(1516,1000,479,796,18,NULL,4),(1517,1000,479,595,19,NULL,4),(1518,1000,479,798,20,NULL,4),(1519,1000,479,569,21,NULL,4),(1520,1000,479,792,22,NULL,4),(1521,1000,479,504,23,NULL,4),(1522,1000,479,779,24,NULL,4),(1523,1000,479,609,25,NULL,4),(1524,1000,479,802,26,NULL,4),(1525,1000,479,502,27,NULL,4),(1526,1000,479,778,28,NULL,4),(1527,1000,479,428,29,NULL,4),(1528,1000,479,763,30,NULL,4),(1529,1000,479,526,31,NULL,4),(1530,1000,479,784,32,NULL,4),(1531,1000,479,510,33,NULL,4),(1532,1000,479,781,34,NULL,4),(1533,1000,480,571,1,NULL,4),(1534,1000,480,793,2,NULL,4),(1535,1000,480,565,3,NULL,4),(1536,1000,480,789,4,NULL,4),(1537,1000,480,440,5,NULL,4),(1538,1000,480,766,6,NULL,4),(1539,1000,480,474,7,NULL,4),(1540,1000,480,773,8,NULL,4),(1541,1000,480,528,9,NULL,4),(1542,1000,480,785,10,NULL,4),(1543,1000,480,534,11,NULL,4),(1544,1000,480,787,12,NULL,4),(1545,1000,480,595,13,NULL,4),(1546,1000,480,798,14,NULL,4),(1547,1000,480,522,15,NULL,4),(1548,1000,480,783,16,NULL,4),(1549,1000,480,539,17,NULL,4),(1550,1000,480,788,18,NULL,4),(1551,1000,480,577,19,NULL,4),(1552,1000,480,796,20,NULL,4),(1553,1000,480,560,21,NULL,4),(1554,1000,480,791,22,NULL,4),(1555,1000,480,502,23,NULL,4),(1556,1000,480,778,24,NULL,4),(1557,1000,480,609,25,NULL,4),(1558,1000,480,802,26,NULL,4),(1559,1000,480,526,27,NULL,4),(1560,1000,480,784,28,NULL,4),(1561,1000,480,510,29,NULL,4),(1562,1000,480,781,30,NULL,4),(1563,1000,481,445,1,NULL,4),(1564,1000,481,768,2,NULL,4),(1565,1000,481,443,3,NULL,4),(1566,1000,481,767,4,NULL,4),(1567,1000,481,460,5,NULL,4),(1568,1000,481,771,6,NULL,4),(1569,1000,481,496,7,NULL,4),(1570,1000,481,777,8,NULL,4),(1571,1000,481,595,9,NULL,4),(1572,1000,481,798,10,NULL,4),(1573,1000,481,502,11,NULL,4),(1574,1000,481,778,12,NULL,4),(1575,1000,481,504,13,NULL,4),(1576,1000,481,779,14,NULL,4),(1577,1000,481,528,15,NULL,4),(1578,1000,481,785,16,NULL,4),(1579,1000,481,534,17,NULL,4),(1580,1000,481,787,18,NULL,4),(1581,1000,481,722,19,NULL,4),(1582,1000,481,770,20,NULL,4),(1583,1000,482,597,1,NULL,4),(1584,1000,482,799,2,NULL,4),(1585,1000,482,599,3,NULL,4),(1586,1000,482,800,4,NULL,4),(1587,1000,482,573,5,NULL,4),(1588,1000,482,794,6,NULL,4),(1589,1000,482,450,7,NULL,4),(1590,1000,482,769,8,NULL,4),(1591,1000,482,490,9,NULL,4),(1592,1000,482,775,10,NULL,4),(1593,1000,482,492,11,NULL,4),(1594,1000,482,776,12,NULL,4),(1595,1000,482,530,13,NULL,4),(1596,1000,482,786,14,NULL,4),(1597,1000,482,528,15,NULL,4),(1598,1000,482,785,16,NULL,4),(1599,1000,482,534,17,NULL,4),(1600,1000,482,787,18,NULL,4),(1601,1000,482,603,19,NULL,4),(1602,1000,482,801,20,NULL,4),(1603,1000,482,438,21,NULL,4),(1604,1000,482,765,22,NULL,4),(1605,1000,482,556,23,NULL,4),(1606,1000,482,790,24,NULL,4),(1607,1000,482,508,25,NULL,4),(1608,1000,482,780,26,NULL,4),(1609,1000,482,502,27,NULL,4),(1610,1000,482,778,28,NULL,4),(1611,1000,482,569,29,NULL,4),(1612,1000,482,792,30,NULL,4),(1613,1000,482,504,31,NULL,4),(1614,1000,482,779,32,NULL,4),(1615,1000,483,597,1,NULL,4),(1616,1000,483,799,2,NULL,4),(1617,1000,483,599,3,NULL,4),(1618,1000,483,800,4,NULL,4),(1619,1000,483,573,5,NULL,4),(1620,1000,483,794,6,NULL,4),(1621,1000,483,575,7,NULL,4),(1622,1000,483,795,8,NULL,4),(1623,1000,483,492,9,NULL,4),(1624,1000,483,776,10,NULL,4),(1625,1000,483,468,11,NULL,4),(1626,1000,483,772,12,NULL,4),(1627,1000,483,530,13,NULL,4),(1628,1000,483,786,14,NULL,4),(1629,1000,483,528,15,NULL,4),(1630,1000,483,785,16,NULL,4),(1631,1000,483,534,17,NULL,4),(1632,1000,483,787,18,NULL,4),(1633,1000,483,556,19,NULL,4),(1634,1000,483,790,20,NULL,4),(1635,1000,483,438,21,NULL,4),(1636,1000,483,765,22,NULL,4),(1637,1000,483,502,23,NULL,4),(1638,1000,483,778,24,NULL,4),(1639,1000,483,595,25,NULL,4),(1640,1000,483,798,26,NULL,4),(1641,1000,483,508,27,NULL,4),(1642,1000,483,780,28,NULL,4),(1643,1000,483,510,29,NULL,4),(1644,1000,483,781,30,NULL,4),(1645,1000,483,504,31,NULL,4),(1646,1000,483,779,32,NULL,4),(1647,1000,484,440,1,NULL,4),(1648,1000,484,766,2,NULL,4),(1649,1000,484,443,3,NULL,4),(1650,1000,484,767,4,NULL,4),(1651,1000,484,597,5,NULL,4),(1652,1000,484,799,6,NULL,4),(1653,1000,484,573,7,NULL,4),(1654,1000,484,794,8,NULL,4),(1655,1000,484,450,9,NULL,4),(1656,1000,484,769,10,NULL,4),(1657,1000,484,530,11,NULL,4),(1658,1000,484,786,12,NULL,4),(1659,1000,484,460,13,NULL,4),(1660,1000,484,771,14,NULL,4),(1661,1000,484,482,15,NULL,4),(1662,1000,484,774,16,NULL,4),(1663,1000,484,496,17,NULL,4),(1664,1000,484,777,18,NULL,4),(1665,1000,484,492,19,NULL,4),(1666,1000,484,776,20,NULL,4),(1667,1000,484,534,21,NULL,4),(1668,1000,484,787,22,NULL,4),(1669,1000,484,603,23,NULL,4),(1670,1000,484,801,24,NULL,4),(1671,1000,484,528,25,NULL,4),(1672,1000,484,785,26,NULL,4),(1673,1000,484,502,27,NULL,4),(1674,1000,484,778,28,NULL,4),(1675,1000,484,508,29,NULL,4),(1676,1000,484,780,30,NULL,4),(1677,1000,484,430,31,NULL,4),(1678,1000,484,764,32,NULL,4),(1679,1000,484,560,33,NULL,4),(1680,1000,484,791,34,NULL,4),(1681,1000,484,504,35,NULL,4),(1682,1000,484,779,36,NULL,4),(1683,1000,484,595,37,NULL,4),(1684,1000,484,798,38,NULL,4),(1685,1000,484,516,39,NULL,4),(1686,1000,484,782,40,NULL,4),(1687,1000,485,440,1,NULL,4),(1688,1000,485,766,2,NULL,4),(1689,1000,485,443,3,NULL,4),(1690,1000,485,767,4,NULL,4),(1691,1000,485,597,5,NULL,4),(1692,1000,485,799,6,NULL,4),(1693,1000,485,573,7,NULL,4),(1694,1000,485,794,8,NULL,4),(1695,1000,485,450,9,NULL,4),(1696,1000,485,769,10,NULL,4),(1697,1000,485,530,11,NULL,4),(1698,1000,485,786,12,NULL,4),(1699,1000,485,460,13,NULL,4),(1700,1000,485,771,14,NULL,4),(1701,1000,485,482,15,NULL,4),(1702,1000,485,774,16,NULL,4),(1703,1000,485,496,17,NULL,4),(1704,1000,485,777,18,NULL,4),(1705,1000,485,492,19,NULL,4),(1706,1000,485,776,20,NULL,4),(1707,1000,485,534,21,NULL,4),(1708,1000,485,787,22,NULL,4),(1709,1000,485,603,23,NULL,4),(1710,1000,485,801,24,NULL,4),(1711,1000,485,528,25,NULL,4),(1712,1000,485,785,26,NULL,4),(1713,1000,485,502,27,NULL,4),(1714,1000,485,778,28,NULL,4),(1715,1000,485,508,29,NULL,4),(1716,1000,485,780,30,NULL,4),(1717,1000,485,430,31,NULL,4),(1718,1000,485,764,32,NULL,4),(1719,1000,485,560,33,NULL,4),(1720,1000,485,791,34,NULL,4),(1721,1000,485,504,35,NULL,4),(1722,1000,485,779,36,NULL,4),(1723,1000,485,595,37,NULL,4),(1724,1000,485,798,38,NULL,4),(1725,1000,485,516,39,NULL,4),(1726,1000,485,782,40,NULL,4),(1727,1000,486,440,1,NULL,4),(1728,1000,486,766,2,NULL,4),(1729,1000,486,443,3,NULL,4),(1730,1000,486,767,4,NULL,4),(1731,1000,486,597,5,NULL,4),(1732,1000,486,799,6,NULL,4),(1733,1000,486,573,7,NULL,4),(1734,1000,486,794,8,NULL,4),(1735,1000,486,450,9,NULL,4),(1736,1000,486,769,10,NULL,4),(1737,1000,486,530,11,NULL,4),(1738,1000,486,786,12,NULL,4),(1739,1000,486,460,13,NULL,4),(1740,1000,486,771,14,NULL,4),(1741,1000,486,482,15,NULL,4),(1742,1000,486,774,16,NULL,4),(1743,1000,486,496,17,NULL,4),(1744,1000,486,777,18,NULL,4),(1745,1000,486,492,19,NULL,4),(1746,1000,486,776,20,NULL,4),(1747,1000,486,534,21,NULL,4),(1748,1000,486,787,22,NULL,4),(1749,1000,486,603,23,NULL,4),(1750,1000,486,801,24,NULL,4),(1751,1000,486,528,25,NULL,4),(1752,1000,486,785,26,NULL,4),(1753,1000,486,502,27,NULL,4),(1754,1000,486,778,28,NULL,4),(1755,1000,486,508,29,NULL,4),(1756,1000,486,780,30,NULL,4),(1757,1000,486,430,31,NULL,4),(1758,1000,486,764,32,NULL,4),(1759,1000,486,560,33,NULL,4),(1760,1000,486,791,34,NULL,4),(1761,1000,486,504,35,NULL,4),(1762,1000,486,779,36,NULL,4),(1763,1000,486,595,37,NULL,4),(1764,1000,486,798,38,NULL,4),(1765,1000,486,516,39,NULL,4),(1766,1000,486,782,40,NULL,4);
/*!40000 ALTER TABLE `sigl_05_07_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_07_data_group`
--

DROP TABLE IF EXISTS `sigl_05_07_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_07_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_05_07_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=1218 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_07_data_group`
--

LOCK TABLES `sigl_05_07_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_05_07_data_group` DISABLE KEYS */;
INSERT INTO `sigl_05_07_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000),(8,8,1000),(9,9,1000),(10,10,1000),(11,11,1000),(12,12,1000),(13,13,1000),(14,14,1000),(15,15,1000),(16,16,1000),(17,17,1000),(18,18,1000),(19,19,1000),(20,20,1000),(21,21,1000),(22,22,1000),(23,23,1000),(24,24,1000),(25,25,1000),(26,26,1000),(27,27,1000),(28,28,1000),(29,29,1000),(30,30,1000),(31,31,1000),(32,32,1000),(33,33,1000),(34,34,1000),(35,35,1000),(36,36,1000),(37,37,1000),(38,38,1000),(39,39,1000),(40,40,1000),(41,41,1000),(42,42,1000),(43,43,1000),(44,44,1000),(45,45,1000),(46,46,1000),(47,47,1000),(48,48,1000),(49,49,1000),(50,50,1000),(51,51,1000),(52,52,1000),(53,53,1000),(54,54,1000),(55,55,1000),(56,56,1000),(57,57,1000),(58,58,1000),(59,59,1000),(60,60,1000),(61,61,1000),(62,62,1000),(63,63,1000),(64,64,1000),(65,65,1000),(66,66,1000),(67,67,1000),(68,68,1000),(69,69,1000),(70,70,1000),(71,71,1000),(72,72,1000),(73,73,1000),(74,74,1000),(75,75,1000),(76,76,1000),(77,77,1000),(78,78,1000),(79,79,1000),(80,80,1000),(81,81,1000),(82,82,1000),(83,83,1000),(84,84,1000),(85,85,1000),(86,86,1000),(87,87,1000),(88,88,1000),(89,89,1000),(90,90,1000),(91,91,1000),(92,92,1000),(93,93,1000),(94,94,1000),(95,95,1000),(96,96,1000),(97,97,1000),(98,98,1000),(99,99,1000),(100,100,1000),(101,101,1000),(102,102,1000),(103,103,1000),(104,104,1000),(105,105,1000),(106,106,1000),(107,107,1000),(108,108,1000),(109,109,1000),(110,110,1000),(111,111,1000),(112,112,1000),(113,113,1000),(114,114,1000),(115,115,1000),(116,116,1000),(117,117,1000),(118,118,1000),(119,119,1000),(120,120,1000),(121,121,1000),(122,122,1000),(123,123,1000),(124,124,1000),(125,125,1000),(126,126,1000),(127,127,1000),(128,128,1000),(129,129,1000),(130,130,1000),(131,131,1000),(132,132,1000),(133,133,1000),(134,134,1000),(135,135,1000),(136,136,1000),(137,137,1000),(138,138,1000),(139,139,1000),(140,140,1000),(141,141,1000),(142,142,1000),(143,143,1000),(144,144,1000),(145,145,1000),(146,146,1000),(147,147,1000),(148,148,1000),(149,149,1000),(150,150,1000),(151,151,1000),(152,152,1000),(153,153,1000),(154,154,1000),(155,155,1000),(156,156,1000),(157,157,1000),(158,158,1000),(159,159,1000),(160,160,1000),(161,161,1000),(162,162,1000),(163,163,1000),(164,164,1000),(165,165,1000),(166,166,1000),(167,167,1000),(168,168,1000),(169,169,1000),(170,170,1000),(171,171,1000),(172,172,1000),(173,173,1000),(174,174,1000),(175,175,1000),(176,176,1000),(177,177,1000),(178,178,1000),(179,179,1000),(180,180,1000),(181,181,1000),(182,182,1000),(183,183,1000),(184,184,1000),(185,185,1000),(186,186,1000),(187,187,1000),(188,188,1000),(189,189,1000),(190,190,1000),(191,191,1000),(192,192,1000),(193,193,1000),(194,194,1000),(195,195,1000),(196,196,1000),(197,197,1000),(198,198,1000),(199,199,1000),(200,200,1000),(201,201,1000),(202,202,1000),(203,203,1000),(204,204,1000),(205,205,1000),(206,206,1000),(207,207,1000),(208,208,1000),(209,209,1000),(210,210,1000),(211,211,1000),(212,212,1000),(213,213,1000),(214,214,1000),(215,215,1000),(216,216,1000),(217,217,1000),(218,218,1000),(219,219,1000),(220,220,1000),(221,221,1000),(222,222,1000),(223,223,1000),(224,224,1000),(225,225,1000),(226,226,1000),(227,227,1000),(228,228,1000),(229,229,1000),(230,230,1000),(231,231,1000),(232,232,1000),(233,233,1000),(1199,234,1000),(235,235,1000),(237,237,1000),(238,238,1000),(240,240,1000),(241,241,1000),(242,242,1000),(243,243,1000),(244,244,1000),(245,245,1000),(246,246,1000),(247,247,1000),(248,248,1000),(249,249,1000),(250,250,1000),(251,251,1000),(252,252,1000),(253,253,1000),(254,254,1000),(255,255,1000),(256,256,1000),(257,257,1000),(258,258,1000),(259,259,1000),(260,260,1000),(261,261,1000),(262,262,1000),(263,263,1000),(264,264,1000),(265,265,1000),(266,266,1000),(267,267,1000),(268,268,1000),(269,269,1000),(270,270,1000),(271,271,1000),(272,272,1000),(273,273,1000),(274,274,1000),(275,275,1000),(276,276,1000),(277,277,1000),(278,278,1000),(279,279,1000),(280,280,1000),(281,281,1000),(282,282,1000),(283,283,1000),(284,284,1000),(285,285,1000),(286,286,1000),(287,287,1000),(288,288,1000),(289,289,1000),(290,290,1000),(291,291,1000),(292,292,1000),(293,293,1000),(294,294,1000),(295,295,1000),(296,296,1000),(297,297,1000),(298,298,1000),(299,299,1000),(300,300,1000),(301,301,1000),(302,302,1000),(303,303,1000),(304,304,1000),(305,305,1000),(306,306,1000),(307,307,1000),(308,308,1000),(309,309,1000),(310,310,1000),(311,311,1000),(312,312,1000),(313,313,1000),(1211,314,1000),(317,317,1000),(318,318,1000),(319,319,1000),(320,320,1000),(321,321,1000),(322,322,1000),(323,323,1000),(324,324,1000),(325,325,1000),(326,326,1000),(327,327,1000),(328,328,1000),(329,329,1000),(330,330,1000),(331,331,1000),(332,332,1000),(333,333,1000),(334,334,1000),(335,335,1000),(336,336,1000),(337,337,1000),(338,338,1000),(339,339,1000),(340,340,1000),(341,341,1000),(342,342,1000),(343,343,1000),(344,344,1000),(345,345,1000),(346,346,1000),(347,347,1000),(348,348,1000),(349,349,1000),(350,350,1000),(351,351,1000),(352,352,1000),(353,353,1000),(354,354,1000),(355,355,1000),(356,356,1000),(357,357,1000),(358,358,1000),(359,359,1000),(360,360,1000),(361,361,1000),(362,362,1000),(363,363,1000),(364,364,1000),(365,365,1000),(366,366,1000),(367,367,1000),(368,368,1000),(369,369,1000),(370,370,1000),(371,371,1000),(372,372,1000),(373,373,1000),(374,374,1000),(375,375,1000),(376,376,1000),(377,377,1000),(378,378,1000),(379,379,1000),(380,380,1000),(381,381,1000),(1200,382,1000),(383,383,1000),(384,384,1000),(385,385,1000),(386,386,1000),(387,387,1000),(388,388,1000),(389,389,1000),(390,390,1000),(391,391,1000),(393,393,1000),(394,394,1000),(396,396,1000),(1201,397,1000),(398,398,1000),(399,399,1000),(400,400,1000),(401,401,1000),(402,402,1000),(403,403,1000),(404,404,1000),(405,405,1000),(406,406,1000),(408,408,1000),(409,409,1000),(411,411,1000),(412,412,1000),(413,413,1000),(414,414,1000),(415,415,1000),(416,416,1000),(417,417,1000),(418,418,1000),(419,419,1000),(420,420,1000),(421,421,1000),(422,422,1000),(1198,423,1000),(424,424,1000),(425,425,1000),(426,426,1000),(427,427,1000),(428,428,1000),(429,429,1000),(430,430,1000),(431,431,1000),(433,433,1000),(435,435,1000),(436,436,1000),(437,437,1000),(1196,438,1000),(439,439,1000),(440,440,1000),(441,441,1000),(442,442,1000),(443,443,1000),(444,444,1000),(445,445,1000),(446,446,1000),(447,447,1000),(448,448,1000),(449,449,1000),(450,450,1000),(458,458,1000),(459,459,1000),(460,460,1000),(461,461,1000),(462,462,1000),(463,463,1000),(464,464,1000),(465,465,1000),(466,466,1000),(467,467,1000),(468,468,1000),(469,469,1000),(470,470,1000),(471,471,1000),(472,472,1000),(473,473,1000),(474,474,1000),(475,475,1000),(476,476,1000),(477,477,1000),(478,478,1000),(479,479,1000),(480,480,1000),(481,481,1000),(482,482,1000),(483,483,1000),(484,484,1000),(485,485,1000),(486,486,1000),(487,487,1000),(488,488,1000),(489,489,1000),(490,490,1000),(491,491,1000),(492,492,1000),(493,493,1000),(494,494,1000),(495,495,1000),(496,496,1000),(497,497,1000),(498,498,1000),(499,499,1000),(500,500,1000),(501,501,1000),(502,502,1000),(503,503,1000),(504,504,1000),(505,505,1000),(506,506,1000),(507,507,1000),(508,508,1000),(509,509,1000),(510,510,1000),(511,511,1000),(512,512,1000),(513,513,1000),(514,514,1000),(515,515,1000),(516,516,1000),(517,517,1000),(518,518,1000),(519,519,1000),(520,520,1000),(521,521,1000),(522,522,1000),(523,523,1000),(524,524,1000),(525,525,1000),(526,526,1000),(527,527,1000),(528,528,1000),(529,529,1000),(530,530,1000),(531,531,1000),(532,532,1000),(533,533,1000),(534,534,1000),(535,535,1000),(536,536,1000),(537,537,1000),(538,538,1000),(539,539,1000),(540,540,1000),(541,541,1000),(542,542,1000),(543,543,1000),(544,544,1000),(545,545,1000),(546,546,1000),(547,547,1000),(548,548,1000),(549,549,1000),(550,550,1000),(551,551,1000),(552,552,1000),(553,553,1000),(554,554,1000),(555,555,1000),(556,556,1000),(557,557,1000),(558,558,1000),(559,559,1000),(560,560,1000),(561,561,1000),(562,562,1000),(563,563,1000),(564,564,1000),(565,565,1000),(566,566,1000),(567,567,1000),(568,568,1000),(569,569,1000),(570,570,1000),(571,571,1000),(572,572,1000),(573,573,1000),(574,574,1000),(575,575,1000),(576,576,1000),(577,577,1000),(578,578,1000),(579,579,1000),(580,580,1000),(581,581,1000),(582,582,1000),(583,583,1000),(584,584,1000),(585,585,1000),(586,586,1000),(587,587,1000),(588,588,1000),(589,589,1000),(590,590,1000),(591,591,1000),(592,592,1000),(593,593,1000),(594,594,1000),(595,595,1000),(596,596,1000),(597,597,1000),(598,598,1000),(599,599,1000),(600,600,1000),(601,601,1000),(602,602,1000),(603,603,1000),(604,604,1000),(605,605,1000),(606,606,1000),(607,607,1000),(608,608,1000),(609,609,1000),(610,610,1000),(611,611,1000),(612,612,1000),(613,613,1000),(614,614,1000),(615,615,1000),(616,616,1000),(617,617,1000),(618,618,1000),(619,619,1000),(620,620,1000),(621,621,1000),(622,622,1000),(623,623,1000),(624,624,1000),(625,625,1000),(626,626,1000),(627,627,1000),(628,628,1000),(629,629,1000),(630,630,1000),(631,631,1000),(632,632,1000),(633,633,1000),(634,634,1000),(635,635,1000),(636,636,1000),(637,637,1000),(638,638,1000),(639,639,1000),(640,640,1000),(641,641,1000),(642,642,1000),(643,643,1000),(644,644,1000),(645,645,1000),(646,646,1000),(647,647,1000),(648,648,1000),(649,649,1000),(650,650,1000),(651,651,1000),(652,652,1000),(653,653,1000),(654,654,1000),(655,655,1000),(656,656,1000),(657,657,1000),(658,658,1000),(659,659,1000),(660,660,1000),(661,661,1000),(662,662,1000),(663,663,1000),(664,664,1000),(665,665,1000),(666,666,1000),(667,667,1000),(668,668,1000),(669,669,1000),(670,670,1000),(671,671,1000),(672,672,1000),(673,673,1000),(674,674,1000),(675,675,1000),(676,676,1000),(677,677,1000),(678,678,1000),(679,679,1000),(680,680,1000),(681,681,1000),(682,682,1000),(683,683,1000),(684,684,1000),(685,685,1000),(686,686,1000),(687,687,1000),(688,688,1000),(689,689,1000),(690,690,1000),(691,691,1000),(692,692,1000),(693,693,1000),(694,694,1000),(695,695,1000),(696,696,1000),(697,697,1000),(698,698,1000),(699,699,1000),(700,700,1000),(701,701,1000),(702,702,1000),(703,703,1000),(704,704,1000),(705,705,1000),(706,706,1000),(707,707,1000),(708,708,1000),(709,709,1000),(710,710,1000),(711,711,1000),(712,712,1000),(713,713,1000),(714,714,1000),(715,715,1000),(716,716,1000),(717,717,1000),(718,718,1000),(719,719,1000),(720,720,1000),(721,721,1000),(722,722,1000),(723,723,1000),(724,724,1000),(725,725,1000),(726,726,1000),(727,727,1000),(728,728,1000),(729,729,1000),(730,730,1000),(731,731,1000),(732,732,1000),(733,733,1000),(734,734,1000),(735,735,1000),(736,736,1000),(737,737,1000),(738,738,1000),(739,739,1000),(740,740,1000),(1192,741,1000),(752,752,1000),(753,753,1000),(754,754,1000),(1203,757,1000),(1216,761,1000),(1217,762,1000),(1193,765,1000),(768,768,1000),(769,769,1000),(770,770,1000),(771,771,1000),(772,772,1000),(773,773,1000),(1214,775,1000),(1215,776,1000),(778,778,1000),(779,779,1000),(780,780,1000),(781,781,1000),(782,782,1000),(783,783,1000),(784,784,1000),(785,785,1000),(786,786,1000),(787,787,1000),(788,788,1000),(789,789,1000),(790,790,1000),(791,791,1000),(792,792,1000),(793,793,1000),(794,794,1000),(795,795,1000),(796,796,1000),(797,797,1000),(798,798,1000),(799,799,1000),(800,800,1000),(801,801,1000),(802,802,1000),(803,803,1000),(804,804,1000),(805,805,1000),(806,806,1000),(807,807,1000),(808,808,1000),(809,809,1000),(810,810,1000),(811,811,1000),(812,812,1000),(813,813,1000),(814,814,1000),(815,815,1000),(816,816,1000),(817,817,1000),(818,818,1000),(819,819,1000),(820,820,1000),(821,821,1000),(822,822,1000),(823,823,1000),(824,824,1000),(825,825,1000),(826,826,1000),(827,827,1000),(828,828,1000),(829,829,1000),(830,830,1000),(831,831,1000),(832,832,1000),(833,833,1000),(834,834,1000),(835,835,1000),(836,836,1000),(837,837,1000),(838,838,1000),(839,839,1000),(840,840,1000),(841,841,1000),(842,842,1000),(843,843,1000),(844,844,1000),(845,845,1000),(846,846,1000),(847,847,1000),(848,848,1000),(849,849,1000),(850,850,1000),(851,851,1000),(852,852,1000),(853,853,1000),(854,854,1000),(855,855,1000),(856,856,1000),(857,857,1000),(858,858,1000),(859,859,1000),(860,860,1000),(861,861,1000),(862,862,1000),(863,863,1000),(864,864,1000),(865,865,1000),(866,866,1000),(867,867,1000),(868,868,1000),(869,869,1000),(870,870,1000),(871,871,1000),(872,872,1000),(873,873,1000),(874,874,1000),(875,875,1000),(876,876,1000),(877,877,1000),(878,878,1000),(879,879,1000),(880,880,1000),(881,881,1000),(882,882,1000),(883,883,1000),(884,884,1000),(885,885,1000),(886,886,1000),(887,887,1000),(888,888,1000),(889,889,1000),(890,890,1000),(891,891,1000),(892,892,1000),(893,893,1000),(894,894,1000),(895,895,1000),(896,896,1000),(897,897,1000),(898,898,1000),(899,899,1000),(900,900,1000),(901,901,1000),(902,902,1000),(903,903,1000),(904,904,1000),(905,905,1000),(906,906,1000),(907,907,1000),(908,908,1000),(909,909,1000),(910,910,1000),(911,911,1000),(912,912,1000),(913,913,1000),(914,914,1000),(915,915,1000),(916,916,1000),(917,917,1000),(918,918,1000),(919,919,1000),(920,920,1000),(921,921,1000),(922,922,1000),(923,923,1000),(924,924,1000),(925,925,1000),(926,926,1000),(927,927,1000),(928,928,1000),(929,929,1000),(930,930,1000),(931,931,1000),(932,932,1000),(933,933,1000),(934,934,1000),(935,935,1000),(936,936,1000),(937,937,1000),(938,938,1000),(939,939,1000),(940,940,1000),(941,941,1000),(942,942,1000),(943,943,1000),(944,944,1000),(945,945,1000),(946,946,1000),(947,947,1000),(948,948,1000),(949,949,1000),(950,950,1000),(951,951,1000),(952,952,1000),(953,953,1000),(954,954,1000),(955,955,1000),(956,956,1000),(957,957,1000),(958,958,1000),(959,959,1000),(960,960,1000),(961,961,1000),(962,962,1000),(963,963,1000),(964,964,1000),(965,965,1000),(966,966,1000),(967,967,1000),(968,968,1000),(969,969,1000),(970,970,1000),(971,971,1000),(972,972,1000),(973,973,1000),(974,974,1000),(975,975,1000),(976,976,1000),(977,977,1000),(978,978,1000),(979,979,1000),(980,980,1000),(981,981,1000),(982,982,1000),(983,983,1000),(984,984,1000),(985,985,1000),(986,986,1000),(987,987,1000),(988,988,1000),(989,989,1000),(990,990,1000),(991,991,1000),(992,992,1000),(993,993,1000),(994,994,1000),(995,995,1000),(996,996,1000),(997,997,1000),(998,998,1000),(999,999,1000),(1000,1000,1000),(1001,1001,1000),(1002,1002,1000),(1003,1003,1000),(1004,1004,1000),(1005,1005,1000),(1006,1006,1000),(1007,1007,1000),(1008,1008,1000),(1009,1009,1000),(1010,1010,1000),(1011,1011,1000),(1012,1012,1000),(1013,1013,1000),(1014,1014,1000),(1015,1015,1000),(1016,1016,1000),(1017,1017,1000),(1018,1018,1000),(1019,1019,1000),(1020,1020,1000),(1021,1021,1000),(1022,1022,1000),(1023,1023,1000),(1024,1024,1000),(1025,1025,1000),(1026,1026,1000),(1027,1027,1000),(1028,1028,1000),(1029,1029,1000),(1030,1030,1000),(1031,1031,1000),(1032,1032,1000),(1033,1033,1000),(1034,1034,1000),(1035,1035,1000),(1036,1036,1000),(1037,1037,1000),(1038,1038,1000),(1039,1039,1000),(1040,1040,1000),(1041,1041,1000),(1042,1042,1000),(1043,1043,1000),(1044,1044,1000),(1045,1045,1000),(1046,1046,1000),(1047,1047,1000),(1048,1048,1000),(1049,1049,1000),(1050,1050,1000),(1051,1051,1000),(1052,1052,1000),(1053,1053,1000),(1054,1054,1000),(1055,1055,1000),(1056,1056,1000),(1057,1057,1000),(1058,1058,1000),(1059,1059,1000),(1060,1060,1000),(1061,1061,1000),(1062,1062,1000),(1063,1063,1000),(1064,1064,1000),(1065,1065,1000),(1066,1066,1000),(1067,1067,1000),(1068,1068,1000),(1069,1069,1000),(1070,1070,1000),(1071,1071,1000),(1072,1072,1000),(1073,1073,1000),(1074,1074,1000),(1075,1075,1000),(1076,1076,1000),(1077,1077,1000),(1078,1078,1000),(1079,1079,1000),(1080,1080,1000),(1081,1081,1000),(1082,1082,1000),(1083,1083,1000),(1084,1084,1000),(1085,1085,1000),(1086,1086,1000),(1087,1087,1000),(1088,1088,1000),(1089,1089,1000),(1090,1090,1000),(1091,1091,1000),(1092,1092,1000),(1093,1093,1000),(1094,1094,1000),(1095,1095,1000),(1096,1096,1000),(1097,1097,1000),(1098,1098,1000),(1099,1099,1000),(1100,1100,1000),(1101,1101,1000),(1102,1102,1000),(1103,1103,1000),(1104,1104,1000),(1105,1105,1000),(1106,1106,1000),(1107,1107,1000),(1108,1108,1000),(1109,1109,1000),(1110,1110,1000),(1111,1111,1000),(1112,1112,1000),(1113,1113,1000),(1114,1114,1000),(1115,1115,1000),(1116,1116,1000),(1117,1117,1000),(1118,1118,1000),(1119,1119,1000),(1120,1120,1000),(1121,1121,1000),(1122,1122,1000),(1123,1123,1000),(1124,1124,1000),(1125,1125,1000),(1126,1126,1000),(1127,1127,1000),(1128,1128,1000),(1129,1129,1000),(1130,1130,1000),(1131,1131,1000),(1132,1132,1000),(1133,1133,1000),(1134,1134,1000),(1135,1135,1000),(1136,1136,1000),(1137,1137,1000),(1138,1138,1000),(1139,1139,1000),(1140,1140,1000),(1141,1141,1000),(1142,1142,1000),(1143,1143,1000),(1144,1144,1000),(1145,1145,1000),(1146,1146,1000),(1147,1147,1000),(1148,1148,1000),(1149,1149,1000),(1150,1150,1000),(1151,1151,1000),(1152,1152,1000),(1153,1153,1000),(1154,1154,1000),(1155,1155,1000),(1156,1156,1000),(1157,1157,1000),(1158,1158,1000),(1159,1159,1000),(1160,1160,1000),(1161,1161,1000),(1162,1162,1000),(1163,1163,1000),(1164,1164,1000),(1165,1165,1000),(1166,1166,1000),(1167,1167,1000),(1168,1168,1000),(1169,1169,1000),(1170,1170,1000),(1171,1171,1000),(1172,1172,1000),(1173,1173,1000),(1174,1174,1000),(1175,1175,1000),(1176,1176,1000),(1177,1177,1000),(1178,1178,1000),(1179,1179,1000),(1180,1180,1000),(1181,1181,1000),(1182,1182,1000),(1183,1183,1000),(1184,1184,1000),(1185,1185,1000),(1186,1186,1000),(1187,1187,1000),(1188,1188,1000),(1189,1189,1000),(1190,1190,1000),(1191,1191,1000),(1195,1192,1000),(1197,1193,1000),(1204,1194,1000),(1209,1195,1000),(1210,1196,1000),(1212,1197,1000),(1213,1198,1000);
/*!40000 ALTER TABLE `sigl_05_07_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_07_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_05_07_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_07_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_05_07_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_07_data_group_mode`
--

LOCK TABLES `sigl_05_07_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_05_07_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_05_07_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_07_deleted`
--

DROP TABLE IF EXISTS `sigl_05_07_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_07_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_refanalyse` int(10) unsigned NOT NULL,
  `id_refvariable` int(10) unsigned NOT NULL,
  `position` int(2) unsigned DEFAULT NULL,
  `num_var` int(2) unsigned DEFAULT NULL,
  `obligatoire` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `UNIQUE` (`id_refanalyse`,`id_refvariable`),
  KEY `FK_sigl_05_07_data_1` (`id_owner`),
  KEY `FK_sigl_05_07_data_3` (`id_refvariable`)
) ENGINE=InnoDB AUTO_INCREMENT=778 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_07_deleted`
--

LOCK TABLES `sigl_05_07_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_05_07_deleted` DISABLE KEYS */;
INSERT INTO `sigl_05_07_deleted` VALUES (236,1010,191,214,20,NULL,4),(239,1010,196,217,NULL,NULL,4),(315,1010,239,289,10,NULL,4),(316,1010,239,290,20,NULL,4),(392,1010,267,351,100,NULL,4),(395,1010,267,354,130,NULL,4),(407,1010,268,351,100,NULL,4),(410,1010,268,354,130,NULL,4),(432,1010,270,351,90,NULL,4),(434,1010,270,359,110,NULL,4),(451,1010,271,335,130,NULL,4),(452,1010,271,336,140,NULL,4),(453,1010,271,351,150,NULL,4),(454,1010,271,359,160,NULL,4),(455,1010,271,374,170,NULL,4),(456,1010,271,375,180,NULL,4),(457,1010,271,365,190,NULL,4),(742,1010,407,626,10,NULL,4),(743,1010,407,627,20,NULL,4),(744,1010,408,628,10,NULL,4),(745,1010,408,629,20,NULL,4),(746,1010,408,289,20,NULL,4),(747,1010,408,290,30,NULL,4),(748,1010,409,628,NULL,NULL,4),(749,1010,409,629,10,NULL,4),(750,1010,409,289,20,NULL,4),(751,1010,409,290,30,NULL,4),(755,1010,410,630,30,NULL,4),(756,1010,410,631,40,NULL,4),(758,1010,411,626,20,NULL,4),(759,1010,411,627,30,NULL,4),(760,1010,412,626,NULL,NULL,4),(763,1010,412,633,30,NULL,4),(764,1010,413,626,NULL,NULL,4),(766,1010,413,627,10,NULL,4),(767,1010,413,635,30,NULL,4),(774,1010,415,626,NULL,NULL,4),(777,1010,415,633,30,NULL,4);
/*!40000 ALTER TABLE `sigl_05_07_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_data`
--

DROP TABLE IF EXISTS `sigl_05_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `code` varchar(4) NOT NULL,
  `nom` varchar(120) NOT NULL,
  `abbr` varchar(20) DEFAULT NULL,
  `famille` int(10) unsigned DEFAULT NULL,
  `paillasse` int(10) unsigned DEFAULT NULL,
  `cote_unite` varchar(2) DEFAULT NULL,
  `cote_valeur` int(3) unsigned DEFAULT NULL,
  `commentaire` text,
  `produit_biologique` int(10) unsigned DEFAULT NULL,
  `type_prel` int(10) unsigned DEFAULT NULL,
  `type_analyse` int(10) unsigned DEFAULT NULL,
  `actif` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `code` (`code`),
  KEY `id_owner` (`id_owner`),
  KEY `sigl_05_data_ibfk_3` (`famille`),
  KEY `sigl_05_data_ibfk_4` (`paillasse`),
  KEY `sigl_05_data_ibfk_5` (`produit_biologique`),
  KEY `sigl_05_data_ibfk_6` (`type_prel`),
  KEY `sigl_05_data_ibfk_7` (`type_analyse`),
  KEY `sigl_05_data_ibfk_8` (`actif`)
) ENGINE=InnoDB AUTO_INCREMENT=487 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_data`
--

LOCK TABLES `sigl_05_data` WRITE;
/*!40000 ALTER TABLE `sigl_05_data` DISABLE KEYS */;
INSERT INTO `sigl_05_data` VALUES (1,1010,'PB1','Prélèvement de sang veineux',NULL,NULL,NULL,'PB',2,NULL,NULL,NULL,NULL,4),(2,1010,'PB2','Prélèvements  multiples de sang veineux (au moins 3)',NULL,NULL,NULL,'PB',6,NULL,NULL,NULL,NULL,4),(3,1010,'PB3','Prélèvement d\'urines',NULL,NULL,NULL,'PB',NULL,NULL,NULL,NULL,NULL,4),(4,1010,'PB4','Prélèvement de selles',NULL,NULL,NULL,'PB',NULL,NULL,NULL,NULL,NULL,4),(5,1010,'PB5','Prélèvement de liquide de ponction',NULL,NULL,NULL,'PB',NULL,NULL,NULL,NULL,NULL,4),(6,1010,'PB6','Prélèvement de crachats',NULL,NULL,NULL,'PB',NULL,NULL,NULL,NULL,NULL,4),(7,1010,'PB7','Prélèvement Vaginal',NULL,NULL,NULL,'PB',4,NULL,NULL,NULL,NULL,4),(8,1010,'PB8','Prélèvement Urétral',NULL,NULL,NULL,'PB',4,NULL,NULL,NULL,NULL,4),(9,1010,'PB9','Prélèvement de sang artériel',NULL,NULL,NULL,'PB',3,NULL,NULL,NULL,NULL,4),(10,1010,'PB10','Prélèvement de gorge',NULL,NULL,NULL,'PB',2,NULL,NULL,NULL,NULL,4),(11,1010,'PB11','Prélèvement auriculaire',NULL,NULL,NULL,'PB',2,NULL,NULL,NULL,NULL,4),(12,1010,'PB12','Prélèvement de sang capillaire',NULL,NULL,NULL,'PB',1,NULL,NULL,NULL,NULL,4),(13,1010,'PB13','Prélèvement nasal',NULL,NULL,NULL,'PB',2,NULL,NULL,NULL,NULL,4),(14,1010,'PB14','Prélèvement anal',NULL,NULL,NULL,'PB',2,NULL,NULL,NULL,NULL,4),(15,1010,'PB15','Prélèvement buccal',NULL,NULL,NULL,'PB',2,NULL,NULL,NULL,NULL,4),(16,1010,'PB16','Prélèvement oculaire',NULL,NULL,NULL,'PB',3,NULL,NULL,NULL,NULL,4),(17,1010,'PB17','Prélèvement de pus',NULL,NULL,NULL,'PB',3,NULL,NULL,NULL,NULL,4),(18,1010,'PB18','Prélèvement de cheveux- squames et phanères',NULL,NULL,NULL,'PB',2,NULL,NULL,NULL,NULL,4),(19,1010,'PB19','Prélèvement médullaire',NULL,NULL,NULL,'PB',20,NULL,NULL,NULL,NULL,4),(20,1010,'PB20','Prélèvement ganglionnaire',NULL,NULL,NULL,'PB',10,NULL,NULL,NULL,NULL,4),(21,1010,'PB21','Prélèvement bronchique',NULL,NULL,NULL,'PB',NULL,NULL,NULL,NULL,NULL,4),(22,1010,'PB22','Prélèvement de sperme',NULL,NULL,NULL,'PB',NULL,NULL,NULL,NULL,NULL,4),(23,1010,'PB23','Autres prélèvements',NULL,NULL,NULL,'PB',NULL,NULL,NULL,NULL,NULL,4),(24,1010,'B001','Acide urique (uricémie)',NULL,11,NULL,'B',15,NULL,1,138,170,4),(25,1010,'B002','Bicarbonates ',NULL,11,NULL,'B',20,NULL,1,138,170,4),(26,1010,'B003','Bilirubine totale',NULL,11,NULL,'B',30,NULL,1,138,171,4),(27,1010,'B502','Bilirubine directe (conjuguée)',NULL,11,NULL,'B',NULL,NULL,1,138,170,4),(28,1010,'B501','Bilirubine libre',NULL,11,NULL,'B',NULL,NULL,1,138,170,4),(29,1010,'B004','Créatininémie',NULL,11,NULL,'B',10,NULL,1,138,170,4),(30,1010,'B005','Glucose',NULL,11,NULL,'B',10,NULL,1,138,170,4),(31,1010,'B006','Urée',NULL,11,NULL,'B',10,NULL,1,138,170,4),(32,1010,'B007','Ammoniaque par colorimétrie',NULL,11,NULL,'B',40,NULL,1,138,170,4),(33,1010,'B008','Calcium (calcémie)',NULL,11,NULL,'B',15,NULL,1,138,170,4),(34,1010,'B009','Chlore (chlorémie)',NULL,11,NULL,'B',15,NULL,1,138,170,4),(35,1010,'B010','Fer sérique',NULL,11,NULL,'B',20,NULL,1,138,170,4),(36,1010,'B011','Ionogramme complet (comprend au minimum Na, K, Cl, Bicarbonates, protéines)','Ionogramme complet',11,NULL,'B',60,NULL,1,138,171,4),(37,1010,'B012','Ionogramme étendu (complet   Ca   Phosphates)','Ionogramme étendu',11,NULL,'B',80,NULL,1,138,171,4),(38,1010,'B013','Ionogramme 3 paramètres (Na, K, Cl)',NULL,11,NULL,'B',30,NULL,1,138,171,4),(39,1010,'B014','Lithium',NULL,11,NULL,'B',30,NULL,1,138,170,4),(40,1010,'B015','Magnésium plasmatique',NULL,11,NULL,'B',15,NULL,1,138,170,4),(41,1010,'B016','Magnésium érythrocytaire',NULL,11,NULL,'B',60,NULL,1,138,170,4),(42,1010,'B017','Phosphates (phosphorémie)',NULL,11,NULL,'B',15,NULL,1,138,170,4),(43,1010,'B018','Potassium    Sodium (photométrie de flamme ou potentiométrie)',NULL,11,NULL,'B',20,NULL,1,138,171,4),(44,1010,'B019','Potassium par colorimétrie',NULL,11,NULL,'B',10,NULL,1,138,170,4),(45,1010,'B020','Sodium par colorimétrie',NULL,11,NULL,'B',10,NULL,1,138,170,4),(46,1010,'B021','Cholestérol total',NULL,11,NULL,'B',15,NULL,1,138,170,4),(47,1010,'B022','Cholestérol HDL',NULL,11,NULL,'B',30,NULL,1,138,170,4),(48,1010,'B023','Cholestérol LDL',NULL,11,NULL,'B',30,NULL,1,138,170,4),(49,1010,'B503','Bilan lipidique (cholestérol Total   HDL LDL Trigly)',NULL,11,NULL,'B',40,NULL,1,138,170,4),(50,1010,'B025','Electrophorèse des lipides (lipidogramme)',NULL,11,NULL,'B',60,NULL,1,138,170,4),(51,1010,'B026','Lipoprotéine A1 par immunologie',NULL,11,NULL,'B',80,NULL,1,138,170,4),(52,1010,'B027','Lipoprotéine B par immunologie',NULL,11,NULL,'B',80,NULL,1,138,170,4),(53,1010,'B028','Lipoprotéines A1   B par immunologie',NULL,11,NULL,'B',150,NULL,1,138,171,4),(54,1010,'B029','Triglycérides',NULL,11,NULL,'B',15,NULL,1,138,170,4),(55,1010,'B030','Albumine par méthode colorimétrique',NULL,11,NULL,'B',15,NULL,1,138,170,4),(56,1010,'B031','Albumine par méthode immunologique',NULL,11,NULL,'B',40,NULL,1,138,170,4),(57,1010,'B032','Electrophorèse de l\'Hémoglobine sans tracé',NULL,11,NULL,'B',20,NULL,1,138,170,4),(58,1010,'B033','Electrophorèse de l\'Hémoglobine avec quantification par densitométrie',NULL,11,NULL,'B',40,NULL,1,138,170,4),(59,1010,'B034','Electrophorèse de l\'Hémoglobine par HPLC',NULL,11,NULL,'B',60,NULL,1,138,170,4),(60,1010,'B035','Electrophorèse des protides (protéinogramme)',NULL,11,NULL,'B',50,'Avec détermination des pourcentages, dosage des protéines totales',1,138,170,4),(61,1010,'B036','Hémoglobine glyquée (Hb A1c)',NULL,11,NULL,'B',50,NULL,1,138,170,4),(62,1010,'B037','Hémoglobine F : dosage par HPLC',NULL,11,NULL,'B',60,NULL,1,138,170,4),(63,1010,'B038','Hémoglobine S : test de solubilité',NULL,11,NULL,'B',10,NULL,1,138,170,4),(64,1010,'B039','Myoglobine',NULL,11,NULL,'B',80,NULL,1,138,170,4),(65,1010,'B040','Protéines de Bences Jones (recherche)',NULL,11,NULL,'B',20,NULL,1,138,170,4),(66,1010,'B041','Protéines de Bences Jones par électrophorèse',NULL,11,NULL,'B',100,NULL,1,138,170,4),(67,1010,'B042','Protéines totales',NULL,11,NULL,'B',15,NULL,1,138,170,4),(68,1010,'B043','Protéine C Réactive semi-quantitative (CRP : test au latex)','CRP',11,NULL,'B',10,NULL,1,138,170,4),(69,1010,'B044','Protéine C Réactive quantitative par immunologie',NULL,11,NULL,'B',80,NULL,1,138,170,4),(70,1010,'B045','Protéine C Réactive quantitative par spectrophotométrie',NULL,11,NULL,'B',50,NULL,1,138,170,4),(71,1010,'B046','Troponine  semi-quantitative par test rapide',NULL,11,NULL,'B',20,NULL,1,138,170,4),(72,1010,'B047','Troponine par méthode immunologique',NULL,11,NULL,'B',80,NULL,1,138,170,4),(73,1010,'B048','Gaz du sang (pH, pO2, pCO2, SaO2)','GDS',11,NULL,'B',80,NULL,9,138,170,4),(74,1010,'B049','Amylase',NULL,11,NULL,'B',20,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(75,1010,'B050','Créatine PhosphoKinase','CPK',11,NULL,'B',30,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(76,1010,'B051','Créatine PhosphoKinase MB','CPK-MB',11,NULL,'B',30,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(77,1010,'B052','5\'Nucléotidase',NULL,11,NULL,'B',40,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(78,1010,'B053','Gamma glutamyl transférase (Gamma GT)','GGT',11,NULL,'B',20,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(79,1010,'B054','Glucose -6-Phosphate Déshydrogénase','G6PD',11,NULL,'B',60,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(80,1010,'B055','Lactate Déshydrogénase (LDH)',NULL,11,NULL,'B',30,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(81,1010,'B056','Phosphatases Alcalines (PAL)',NULL,11,NULL,'B',20,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(82,1010,'B057','Phosphatases Acides',NULL,11,NULL,'B',20,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(83,1010,'B058','Transaminases (ASAT)',NULL,11,NULL,'B',15,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(84,1010,'B059','Transaminases (ALAT)',NULL,11,NULL,'B',15,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(85,1010,'B060','Transaminases (ALAT/TGP ASAT/TGO)',NULL,11,NULL,'B',25,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,171,4),(86,1010,'B061','Lipase',NULL,11,NULL,'B',40,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(87,1010,'B062','Béta HCG dosage',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(88,1010,'B063','Cortisol',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(89,1010,'B064','Erythropoïtine',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(90,1010,'B065','Estradiol',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(91,1010,'B066','Ferritine',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(92,1010,'B067','FSH',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(93,1010,'B068','Insuline',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(94,1010,'B069','Insuline libre',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(95,1010,'B070','LH',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(96,1010,'B071','Progestérone',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(97,1010,'B072','Prolactine',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(98,1010,'B073','Thyroglobuline',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(99,1010,'B074','Thyroxine libre (FT4)',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(100,1010,'B075','Testostérone',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(101,1010,'B077','Transferrine',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(102,1010,'B078','Triiodothyronine libre (FT3)',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(103,1010,'B079','TSH Ultrasensible',NULL,11,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(104,1010,'B080','TSH (Hormone ThyreoStimulante)',NULL,19,NULL,'B',100,'Le compte rendu doit mentionner la ou les techniques utilisées.',1,138,170,4),(105,1010,'B081','Acétone',NULL,12,NULL,'B',5,NULL,3,153,170,4),(106,1010,'B082','Acide urique (uricurie)',NULL,12,NULL,'B',15,NULL,3,153,170,4),(107,1010,'B083','pH urinaire',NULL,12,NULL,'B',10,NULL,3,153,170,4),(108,1010,'B084','Créatininurie',NULL,12,NULL,'B',15,NULL,3,153,170,4),(109,1010,'B085','Pigments biliaires (recherche)',NULL,12,NULL,'B',5,NULL,3,153,170,4),(110,1010,'B086','Recherche de sang (hématies et/ou hémoglobine)',NULL,12,NULL,'B',5,NULL,3,153,170,4),(111,1010,'B087','Sels biliaires',NULL,12,NULL,'B',5,NULL,3,153,170,4),(112,1010,'B088','Sels et pigments biliaires (recherche)',NULL,12,NULL,'B',5,NULL,3,153,171,4),(113,1010,'B089','Glucose   Protéines (recherche)',NULL,12,NULL,'B',5,NULL,3,153,171,4),(114,1010,'B090','Glucose (recherche)',NULL,12,NULL,'B',5,NULL,3,153,170,4),(115,1010,'B091','Urée',NULL,12,NULL,'B',10,NULL,3,153,170,4),(116,1010,'B092','Calcium',NULL,12,NULL,'B',15,NULL,3,153,170,4),(117,1010,'B093','Chlore',NULL,12,NULL,'B',15,NULL,3,153,170,4),(118,1010,'B094','Phosphates',NULL,12,NULL,'B',15,NULL,3,153,170,4),(119,1010,'B095','Potassium',NULL,12,NULL,'B',20,NULL,3,153,170,4),(120,1010,'B096','Sodium',NULL,12,NULL,'B',20,NULL,3,153,170,4),(121,1010,'B097','Protéines (recherche)',NULL,12,NULL,'B',5,NULL,3,153,170,4),(122,1010,'B098','Electrophorèse des protéines urinaires',NULL,12,NULL,'B',70,NULL,3,153,170,4),(123,1010,'B099','Microalbumine (dosage à l\'exclusion des bandelettes)',NULL,12,NULL,'B',60,NULL,3,153,170,4),(124,1010,'B100','Protéinurie (24h)',NULL,12,NULL,'B',20,NULL,3,153,170,4),(125,1010,'B102','Porphyrines (recherche)',NULL,12,NULL,'B',5,NULL,3,153,170,4),(126,1010,'B103','Porphyrines (recherche, dosage et identification)',NULL,12,NULL,'B',70,NULL,3,153,170,4),(127,1010,'B104','Test de grossesse',NULL,12,NULL,'B',10,NULL,3,153,170,4),(128,1010,'B105','Alpha 1-4 glucosidase séminale',NULL,301,NULL,'B',200,NULL,22,152,170,4),(129,1010,'B106','Carnitine libre séminale',NULL,301,NULL,'B',200,NULL,22,152,170,4),(130,1010,'B107','Citrate séminal',NULL,301,NULL,'B',150,NULL,22,152,170,4),(131,1010,'B109','Electrophorèse des protéines du LCR',NULL,301,NULL,'B',60,NULL,5,99,170,4),(132,1010,'B110','Fructose séminal',NULL,301,NULL,'B',60,NULL,22,152,170,4),(133,1010,'B112','Protéines totales (LCR)',NULL,301,NULL,'B',15,NULL,5,99,170,4),(134,1010,'B113','Rivalta',NULL,301,NULL,'B',5,NULL,5,102,170,4),(135,1010,'B114','Clairance de l\'acide urique',NULL,12,NULL,'B',30,NULL,3,153,170,4),(136,1010,'B115','Clairance de l\'urée',NULL,12,NULL,'B',30,NULL,3,153,170,4),(137,1010,'B116','Clairance de la créatinine (rénale)',NULL,12,NULL,'B',30,NULL,3,153,170,4),(138,1010,'B117','Epreuve d\'Hyperglycémie Provoquée par voie Orale (HGPO) : = 4 dosages',NULL,301,NULL,'B',60,NULL,1,138,170,4),(139,1010,'B118','HGPO simplifiée : 2 dosages',NULL,301,NULL,'B',30,NULL,1,138,170,4),(140,1010,'B119','Epreuve à l\'insuline : dosage du glucose',NULL,301,NULL,'B',60,NULL,1,138,170,4),(141,1010,'B120','Epreuve au glucagon : dosage du glucose et de l\'insulinémie',NULL,301,NULL,'B',60,NULL,1,138,170,4),(142,1010,'B121','Test au LH- RH : (4 temps) : dosage de FSH et LH',NULL,301,NULL,'B',600,NULL,1,138,170,4),(143,1010,'B122','Test à HCG : dosage de la testostérone',NULL,301,NULL,'B',300,NULL,1,138,170,4),(144,1010,'B123','Test à HCG : dosage de l\'estradiol',NULL,301,NULL,'B',300,NULL,1,138,170,4),(145,1010,'B124','Test à la déxaméthasone : dosage du cortisol',NULL,301,NULL,'B',300,NULL,1,138,170,4),(146,1010,'B125','Test au TRH (4 temps) : dosage de prolactine et TSH',NULL,301,NULL,'B',600,NULL,1,138,170,4),(147,1010,'B126','Adénogramme ',NULL,279,NULL,'B',100,NULL,20,38,170,4),(148,1010,'B127','Immunophénotypage des cellules malignes',NULL,279,NULL,'B',150,NULL,19,104,170,4),(149,1010,'B128','Hématocrite (taux)',NULL,279,NULL,'B',10,NULL,1,138,170,4),(150,1010,'B129','Hémoglobine (dosage par spectrophotomètre)',NULL,279,NULL,'B',10,NULL,1,138,170,4),(151,1010,'B130','Mesure de la vitesse de sédimentation (VS)','VS',279,NULL,'B',10,NULL,1,138,170,4),(152,1010,'B131','Mesure de la résistance globulaire',NULL,279,NULL,'B',50,NULL,1,138,170,4),(153,1010,'B132','Myélogramme: étude cytologique',NULL,279,NULL,'B',100,NULL,19,104,170,4),(154,1010,'B133','Myélogramme: étude cytochimique (peroxydases, Estérases, Perls et PAL)',NULL,279,NULL,'B',25,'Cotation pour chaque acte.',19,104,170,4),(155,1010,'B134','Hémogramme (Numération Formule Sanguine)','NFS',279,NULL,'B',35,'Comprend: numération des hématies, des leucocytes et des plaquettes/ dosage de l\'hémoglobine, mesure de l\'hématocrite, détermination des constantes érythrocytaires et de la formule leucocytaire complète (automatique ou manuelle), comprend également un contrôle sur frottis sanguin en cas d\'anomalie.',1,138,170,4),(156,1010,'B135','NFS   VS','NFS + VS',279,NULL,'B',40,NULL,1,138,171,4),(157,1010,'B136','Numération des lymphocytes CD4, CD8',NULL,279,NULL,'B',50,NULL,1,138,170,4),(158,1010,'B137','Numération blanche (méthode manuelle)',NULL,279,NULL,'B',10,NULL,1,138,170,4),(159,1010,'B138','Numération des réticulocytes (méthode manuelle)',NULL,279,NULL,'B',40,NULL,1,138,170,4),(160,1010,'B139','Numération des plaquettes',NULL,279,NULL,'B',25,NULL,1,138,170,4),(161,1010,'B140','Recherche d\'anomalies morphologiques des hématies',NULL,279,NULL,'B',20,NULL,1,138,170,4),(162,1010,'B141','Recherche d\'hématies foetales',NULL,279,NULL,'B',30,NULL,1,138,170,4),(163,1010,'B142','Recherche de corps de Heinz',NULL,279,NULL,'B',20,NULL,1,138,170,4),(164,1010,'B143','Test de falciformation des hématies = Test d\'EMMEL',NULL,279,NULL,'B',10,NULL,1,138,170,4),(165,1010,'B144','Recherche de polynucléaires éosinophiles dans le mucus nasal',NULL,279,NULL,'B',15,NULL,9,75,170,4),(166,1010,'B145','Recherche de polynucléaires éosinophiles dans les crachats',NULL,279,NULL,'B',15,NULL,6,50,170,4),(167,1010,'B146','D Dimères par technique agglutination de particules de latex',NULL,279,NULL,'B',50,NULL,1,138,170,4),(168,1010,'B147','D Dimères par technique ELISA ',NULL,279,NULL,'B',100,NULL,1,138,170,4),(169,1010,'B148','Dosage du fibrinogène (préciser la technique sur le compte rendu)',NULL,279,NULL,'B',30,NULL,1,138,170,4),(170,1010,'B149','Dosage des facteurs de la coagulation',NULL,279,NULL,'B',30,'Cotation pour chaque facteur.',1,138,170,4),(171,1010,'B150','Dosage des D dimères: (préciser la technique sur le compte rendu)',NULL,279,NULL,'B',120,NULL,1,138,170,4),(172,1010,'B151','Héparinémie',NULL,279,NULL,'B',100,NULL,1,138,170,4),(173,1010,'B152','Taux de prothrombine + INR (Temps de Quick)','TP',279,NULL,'B',30,NULL,1,138,170,4),(174,1010,'B153','Temps de saignement (test d\'Ivy 3 points)',NULL,279,NULL,'B',15,NULL,23,NULL,170,4),(175,1010,'B154','Temps de Céphaline   Activateurs (TCA / TCK)',NULL,279,NULL,'B',30,NULL,1,138,170,4),(176,1010,'B155','Temps de Thrombine (TT)',NULL,279,NULL,'B',30,NULL,1,138,170,4),(177,1010,'B156','Titrage des Produits de Dégradation de la Fibrine  et/ ou du Fibrinogène(PDF)',NULL,279,NULL,'B',60,NULL,1,138,170,4),(178,1010,'B157','Détermination du groupe sanguin ABO et Rhésus standard (D)',NULL,279,NULL,'B',35,'Avec deux épreuves (globulaire et sérique) effectuées par deux techniciens différents avec deux lots de réactifs différents.',1,138,170,4),(179,1010,'B158','Phénotypage Rhésus et Kell  ',NULL,279,NULL,'B',60,NULL,1,138,170,4),(180,1010,'B159','Autres antigènes érythrocytaires ',NULL,279,NULL,'B',15,'Cotation pour chaque acte.',1,138,170,4),(181,1010,'B160','Recherche d\'Agglutinines Irrégulières (RAI) par un panel d\'au moins 11hématies tests',NULL,279,NULL,'B',200,NULL,1,138,170,4),(182,1010,'B161','Test de Coombs direct ',NULL,279,NULL,'B',40,NULL,1,138,170,4),(183,1010,'B162','Test de Coombs indirect ',NULL,279,NULL,'B',40,NULL,1,138,170,4),(184,1010,'B163','Test de compatibilité',NULL,279,NULL,'B',20,NULL,1,138,170,4),(185,1010,'B164','Facteur rhumatoïde (test au latex)',NULL,1003,NULL,'B',40,NULL,1,138,170,4),(186,1010,'B165','Antistreptolysine O','ASLO',302,NULL,'B',30,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(187,1010,'B166','Antistreptokinase','ASK',302,NULL,'B',30,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(188,1010,'B167','Borrelioses (IFI ou EIA)',NULL,302,NULL,'B',60,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(189,1010,'B168','Brucelloses (IFI ou EIA)',NULL,302,NULL,'B',80,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(190,1010,'B169','Chlamydiae trachomatis (IgG et IgM et/ou IgA)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(191,1010,'B170','Chlamydiae trachomatis par PCR',NULL,24,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',7,162,170,4),(192,1010,'B171','Diagnostic sérologique des bactéries responsables des méningites (test rapide)',NULL,302,NULL,'B',60,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',5,99,170,4),(193,1010,'B172','Hélicobacter pylori (EIA)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(194,1010,'B173','Mycoplasmes génitaux par EIA',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(195,1010,'B174','Mycoplasma pneumoniae (IgG par EIA)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(196,1010,'B175','Salmonelloses : (sérodiagnostic de Widal, agglutination)',NULL,302,NULL,'B',40,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(197,1010,'B176','RPR / VDRL qualitatif (Syphilis)',NULL,302,NULL,'B',10,'En cas de réaction positive au RPR  et au TPHA, un titrage doit être pratiqué. - Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(198,1010,'B177','TPHA  (Syphilis)',NULL,302,NULL,'B',20,'En cas de réaction positive au RPR  et au TPHA, un titrage doit être pratiqué. - Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(199,1010,'B178','FTA Absorbens IgG (Syphilis)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(200,1010,'B179','Recherche des IgM (Syphilis)',NULL,302,NULL,'B',60,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(201,1010,'B180','Recherche directe de chlamydiae par technique immunologique',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(202,1010,'B181','Recherche d\'une toxine bactérienne par technique immunologique',NULL,302,NULL,'B',80,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(203,1010,'B182','Aspergillose (dépistage)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(204,1010,'B183','Candidose (recherche sérologique par au moins deux techniques)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(205,1010,'B184','Cryptococcose (recherche d\'antigènes solubles de Cryptococcus néoformans)',NULL,302,NULL,'B',60,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',5,99,170,4),(206,1010,'B185','Dépistage Cysticercose  (EIA ou IFI)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(207,1010,'B186','Test de confirmation Cysticercose (IE)',NULL,302,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(208,1010,'B187','Dépistage Filariose (EIA ou IFI)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(209,1010,'B188','Test de confirmation Filariose par IE',NULL,302,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(210,1010,'B189','Dépistage Leishmaniose viscérale (EIA ou IFI)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(211,1010,'B190','Test de confirmation Leishmaniose viscérale par IE',NULL,302,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(212,1010,'B191','Paludisme (test sérologique rapide)',NULL,302,NULL,'B',25,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(213,1010,'B504','Détection des IgG (Toxoplasmose)',NULL,302,NULL,'B',NULL,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(214,1010,'B193','Détection et titrage des IgA (Toxoplasmose)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité.',1,138,170,4),(215,1010,'B194','Recherche AgHBs (Hépatite B par test rapide)',NULL,302,NULL,'B',40,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(216,1010,'B195','Recherche Ac anti HBs (Hépatite B par test rapide)',NULL,302,NULL,'B',40,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(217,1010,'B196','Recherche Ag HBe (Hépatite B par test rapide)',NULL,302,NULL,'B',40,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(218,1010,'B197','Recherche Ac anti HBc (Hépatite B par test rapide)',NULL,302,NULL,'B',40,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(219,1010,'B505','Recherche AgHBs (Hépatite B par automate d\'immunoanalyse)',NULL,302,NULL,'B',NULL,NULL,1,138,170,4),(220,1010,'B198','Recherche Ac anti HBs (Hépatite B par automate d\'immunoanalyse)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(221,1010,'B199','Recherche Ag HBe (Hépatite B par automate d\'immunoanalyse)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(222,1010,'B200','Recherche Ac anti HBc (Hépatite B par automate d\'immunoanalyse)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(223,1010,'B201','Recherche Ac anti HBc IgM (Hépatite B par automate d\'immunoanalyse)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(224,1010,'B202','Test de neutralisation de l\'hépatite B',NULL,302,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(225,1010,'B203','Hépatite B ADN par PCR',NULL,19,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(226,1010,'B204','Hépatite C (par test rapide)',NULL,302,NULL,'B',60,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(227,1010,'B205','Recherche des Ac anti VHC (par automate d\'immunoanalyse)',NULL,302,NULL,'B',40,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(228,1010,'B208','Test de confirmation Hépatite C',NULL,302,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(229,1010,'B209','Hépatite C ARN par PCR',NULL,19,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(230,1010,'B210','Recherche des Ac anti-VIH (test rapide)',NULL,302,NULL,'B',30,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(231,1010,'B211','Recherche des Ac anti-VIH (par automate d\'immunoanalyse)',NULL,302,NULL,'B',100,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(232,1010,'B212','Recherche et titrage de l\'antigène P24',NULL,302,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(233,1010,'B213','Diagnostic du VIH (Western Blot) (test de confirmation)',NULL,302,NULL,'B',200,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(234,1010,'B214','Mesure de la charge virale ARN VIH-1',NULL,302,NULL,'B',300,'Le compte rendu doit préciser le réactif utilisé, la valeur seuil de la technique et le nombre de copies ou d?équivalent copies par ml de plasma, - Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(235,1010,'B216','Herpes virus simplex type 1 (IgG ou IgM)',NULL,302,NULL,'B',150,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(236,1010,'B217','Herpes virus simplex type II (IgG ou IgM)',NULL,302,NULL,'B',150,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(237,1010,'B218','Rotavirus et Adénovirus',NULL,302,NULL,'B',50,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',4,141,170,4),(239,1010,'B220','Rubéole (IgG et IgM)',NULL,302,NULL,'B',150,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(240,1010,'B221','Virus respiratoire Syncitial (IgM/IgG)',NULL,302,NULL,'B',150,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(241,1010,'B222','Dosage des immunoglobulines (IgE) totales',NULL,302,NULL,'B',150,NULL,1,138,170,4),(242,1010,'B224','Identification des IgE spécifiques individuelles : Un seul allergène',NULL,302,NULL,'B',100,NULL,1,138,170,4),(243,1010,'B225','Identification des IgE spécifiques individuelles : Deux ou trois allergènes',NULL,302,NULL,'B',200,NULL,1,138,170,4),(244,1010,'B226','Dosage des IgG dans le sang, le LCR',NULL,302,NULL,'B',100,NULL,1,138,170,4),(245,1010,'B227','Dosage des IgM dans le sang, le LCR ',NULL,302,NULL,'B',100,NULL,1,138,170,4),(246,1010,'B228','Dosage des IgA dans le sang, le LCR ',NULL,302,NULL,'B',100,NULL,1,138,170,4),(247,1010,'B229','Recherche et titrage de l\'alpha foetoprotéine (dans le sérum ou liquide amniotique)',NULL,302,NULL,'B',150,NULL,1,138,170,4),(248,1010,'B230','Recherche et titrage de l\'Antigène CarcinoEmbryonnaire (ACE)',NULL,302,NULL,'B',150,NULL,1,138,170,4),(249,1010,'B231','Recherche et titrage de l\'Antigène Prostatique Spécifique (PSA)',NULL,302,NULL,'B',100,NULL,1,138,170,4),(250,1010,'B232','Recherche et titrage de l\'Antigène Prostatique Spécifique  libre (PSA libre)',NULL,302,NULL,'B',100,NULL,1,138,170,4),(251,1010,'B233','Recherche et titrage de 2 microglobuline (dans le sérum ou urine)',NULL,302,NULL,'B',150,NULL,1,138,170,4),(252,1010,'B235','Examen parasitologique des selles',NULL,15,NULL,'B',15,NULL,4,141,170,4),(253,1010,'B236','Recherche de cryptosporidies par coloration élective',NULL,15,NULL,'B',30,NULL,4,141,170,4),(254,1010,'B237','Recherche de cryptosporidies par immunofluorescence',NULL,15,NULL,'B',60,NULL,4,141,170,4),(255,1010,'B238','Recherche de microsporidies dans les selles par coloration élective',NULL,15,NULL,'B',100,NULL,4,141,170,4),(256,1010,'B239','Recherche de pneumocystis carinii dans le liquide bronchoalvéolaire',NULL,16,NULL,'B',100,NULL,21,56,170,4),(257,1010,'B240','Recherche de plasmodium (goutte épaisse et frottis mince)',NULL,15,NULL,'B',10,NULL,1,138,170,4),(258,1010,'B241','Recherche de microfilaires sanguicoles (frottis mince)',NULL,15,NULL,'B',10,'Par prélèvement.',1,138,170,4),(259,1010,'B242','Recherche de microfilaires dans une biopsie cutanée (SNIP)',NULL,15,NULL,'B',10,NULL,23,38,170,4),(260,1010,'B243','Recherche de levures dans le LCR',NULL,16,NULL,'B',10,NULL,5,99,170,4),(261,1010,'B244','Recherche de leishmanies dans une sérosité cutanée',NULL,15,NULL,'B',15,NULL,23,NULL,170,4),(262,1010,'B245','Recherche de trypanosomes dans le sang ',NULL,15,NULL,'B',10,NULL,1,138,170,4),(263,1010,'B246','Recherche des champignons dans les prélèvements de peau et phanères',NULL,16,NULL,'B',15,NULL,18,163,170,4),(264,1010,'B247','Culture des levures',NULL,16,NULL,'B',80,NULL,15,75,170,4),(265,1010,'B248','Culot urinaire : examen direct (état frais, cytologie   coloration)',NULL,18,NULL,'B',15,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',3,153,170,4),(266,1010,'B249','Examen cytobactériologique des urines (uroculture)','ECBU',18,NULL,'B',80,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',3,153,170,4),(267,1010,'B250','Examen direct du prélèvement vaginal/cervico-vaginal',NULL,18,NULL,'B',15,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',7,162,170,4),(268,1010,'B251','Examen cytobactériologique du prélèvement vaginal/cervico-vaginal',NULL,18,NULL,'B',80,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',7,162,170,4),(269,1010,'B252','Examen direct du prélèvement urétral',NULL,18,NULL,'B',15,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',8,152,170,4),(270,1010,'B253','Examen cytobactériologique du prélèvement urétral',NULL,18,NULL,'B',80,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',8,152,170,4),(271,1010,'B254','Examen cytobactériologique du sperme (spermoculture)',NULL,18,NULL,'B',80,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',22,152,170,4),(272,1010,'B255','Examen direct du LCR',NULL,18,NULL,'B',15,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',5,99,170,4),(273,1010,'B256','Examen cytobactériologique du LCR',NULL,18,NULL,'B',80,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',5,99,170,4),(274,1010,'B257','Hémoculture',NULL,18,NULL,'B',100,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',1,138,170,4),(275,1010,'B258','Examen cytobactériologique des selles (coproculture)',NULL,18,NULL,'B',80,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',4,141,170,4),(276,1010,'B259','Examen cytobactériologique des liquides d\'épanchements ou de ponction',NULL,18,NULL,'B',80,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',5,NULL,170,4),(277,1010,'B260','Examen direct des liquides d\'épanchements ou de ponction',NULL,18,NULL,'B',20,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',5,NULL,170,4),(278,1010,'B261','Examen cytologique des liquides de ponction (numération et formule leucocytaire)',NULL,18,NULL,'B',30,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',5,NULL,170,4),(279,1010,'B262','Recherche et identification de campylobacter',NULL,18,NULL,'B',150,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',4,141,170,4),(280,1010,'B263','Recherche et identification des germes anaérobies',NULL,18,NULL,'B',150,'La culture comprend : examen microscopique direct, isolement avec éventuellement identification complète de (s) germe(s) et antibiogramme.',NULL,NULL,170,4),(281,1010,'B264','Spermogramme et spermocytogramme:',NULL,304,NULL,'B',100,'Comprenant la mesure du volume de l\'éjaculat, le pH, l\'estimation de la viscosité du sperme, l\'estimation de la mobilité des spermatozoïdes 30 mn, 2h,4h après éjaculation, numération des spermatozoïdes, recherche de cellules rondes, recherche d\'une agglutination spontanée, numération des formes anormales en détaillant les anomalies de la tête, de la pièce intermédiaire et du flagelle en mentionnant l\'index des anomalies multiples. - ',22,152,170,4),(282,1010,'B265','Test post- coïtal (test de Huhner)',NULL,304,NULL,'B',60,'Le compte rendu comportera le jour du cycle, le temps écoulé après rapport sexuel, la qualité de la glaire (abondance, filance et transparence) le nombre et la mobilité des spermatozoïdes par champ.',7,162,170,4),(283,1010,'B266','Recherche d\'une éjaculation rétrograde en cas d\'hypospermie sévère ou anéjaculation',NULL,304,NULL,'B',50,NULL,22,152,170,4),(284,1010,'B267','Coloration des spermatozoïdes au bleu d\'aniline',NULL,304,NULL,'B',50,NULL,22,152,170,4),(285,1010,'B268','Recherche d\'une immunisation antispermatozoïdes',NULL,19,NULL,'B',120,NULL,NULL,NULL,170,4),(286,1010,'B269','Acide salicylique (dosage)',NULL,303,NULL,'B',100,NULL,1,163,170,4),(287,1010,'B270','Alcool (éthanol ou méthanol)',NULL,303,NULL,'B',50,NULL,1,163,170,4),(288,1010,'B271','Amphétamine (dosage)',NULL,303,NULL,'B',150,NULL,1,163,170,4),(289,1010,'B272','Aluminium',NULL,303,NULL,'B',60,NULL,1,163,170,4),(290,1010,'B273','Antidépresseurs tricycliques (recherche)',NULL,303,NULL,'B',150,NULL,1,163,170,4),(291,1010,'B274','Barbituriques (recherche)',NULL,303,NULL,'B',150,NULL,1,163,170,4),(292,1010,'B275','Barbituriques (dosage)',NULL,303,NULL,'B',200,NULL,1,163,170,4),(293,1010,'B276','Benzodiazépines (recherche)',NULL,303,NULL,'B',150,NULL,1,163,170,4),(294,1010,'B277','Diazépam et son métabolite (dosage)',NULL,303,NULL,'B',100,NULL,1,163,170,4),(295,1010,'B278','Digoxine (dosage)',NULL,303,NULL,'B',200,NULL,1,163,170,4),(296,1010,'B279','Isoniazide (INH)',NULL,303,NULL,'B',150,NULL,1,163,170,4),(297,1010,'B280','Mesure des concentrations plasmatiques des Antrétroviraux',NULL,303,NULL,'B',200,NULL,1,163,170,4),(298,1010,'B281','Oxyde de carbone',NULL,303,NULL,'B',50,NULL,1,163,170,4),(299,1010,'B282','Parcétamol (dosage)',NULL,303,NULL,'B',100,NULL,1,163,170,4),(300,1010,'B283','Plomb par Spectrophotométrie d\'absorption atomique',NULL,303,NULL,'B',60,NULL,1,163,170,4),(301,1010,'B284','Quinidine (dosage)',NULL,303,NULL,'B',200,NULL,1,163,170,4),(302,1010,'B285','Rifampicine',NULL,303,NULL,'B',150,NULL,1,163,170,4),(303,1010,'B286','Théophylline',NULL,303,NULL,'B',150,NULL,1,163,170,4),(304,1010,'B287','Arsenic',NULL,303,NULL,'B',50,NULL,18,163,170,4),(305,1010,'B024','Cholestérol total  HDL (Indice d\'athérogénicité)',NULL,11,NULL,'B',40,NULL,1,138,171,4),(306,1010,'B506','Acide fusidique',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(307,1010,'B507','Acide nalidixique',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(308,1010,'B508','Acide oxolinique',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(309,1010,'B509','Acide pipémidique',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(310,1010,'B510','Acide piromidique',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(311,1010,'B511','Amikacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(312,1010,'B512','Amoxicilline',NULL,1018,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(313,1010,'B513','Amoxicilline/ac. Clavulanique',NULL,1018,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(314,1010,'B514','Ampicilline',NULL,1018,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(315,1010,'B515','Ampicilline/sulbactam',NULL,1018,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(316,1010,'B516','Azithromycine',NULL,1018,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(317,1010,'B517','Aztréonam',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(318,1010,'B518','Bacitracine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(319,1010,'B519','Céfaclor',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(320,1010,'B520','Céfadroxil',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(321,1010,'B521','Céfalexine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(322,1010,'B522','Céfalotine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(323,1010,'B523','Céfamandole',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(324,1010,'B524','Céfatrizine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(325,1010,'B525','Céfazoline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(326,1010,'B526','Céfépime',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(327,1010,'B527','Céfixime',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(328,1010,'B528','Céfopérazone',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(329,1010,'B529','Céfotaxime',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(330,1010,'B530','Céfotétan',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(331,1010,'B531','Céfotiam',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(332,1010,'B532','Céfotiam-héxétil',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(333,1010,'B533','Céfoxitine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(334,1010,'B534','Cefpirome',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(335,1010,'B535','Cefpodoxime-proxétil',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(336,1010,'B536','Céfradine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(337,1010,'B537','Cefsulodine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(338,1010,'B538','Ceftazidime',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(339,1010,'B539','Ceftizoxime',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(340,1010,'B540','Ceftriaxone',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(341,1010,'B541','Céfuroxime',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(342,1010,'B542','Céfuroxime-axétil',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(343,1010,'B543','Chloramphénicol',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(344,1010,'B544','Ciprofloxacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(345,1010,'B545','Clindamycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(346,1010,'B546','Colistine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(347,1010,'B547','Cotrimoxazole',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(348,1010,'B548','Dirithromycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(349,1010,'B549','Doripénème (H)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(350,1010,'B550','Doxycycline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(351,1010,'B551','Enoxacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(352,1010,'B552','Ertapénème',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(353,1010,'B553','Erythromycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(354,1010,'B554','Fluméquine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(355,1010,'B555','Fosfomycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(356,1010,'B556','Gentamicine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(357,1010,'B557','Imipénème',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(358,1010,'B558','Isépamicine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(359,1010,'B559','kanamycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(360,1010,'B560','Latamoxef',NULL,1018,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(361,1010,'B561','Lévofloxacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(362,1010,'B562','Lincomycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(363,1010,'B563','Linézolide',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(364,1010,'B564','Loméfloxacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(365,1010,'B565','Loracarbef',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(366,1010,'B566','Méropénème',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(367,1010,'B567','Metronidazole',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(368,1010,'B568','Minocycline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(369,1010,'B569','Moxifloxacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(370,1010,'B570','Mupirocine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(371,1010,'B571','Nétilmicine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(372,1010,'B572','Nitroxoline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(373,1010,'B573','Norfloxacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(374,1010,'B574','Ofloxacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(375,1010,'B575','Optochine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(376,1010,'B576','Oxacilline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(377,1010,'B577','Oxytétracycline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(378,1010,'B578','Péfloxacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(379,1010,'B579','Pénicilline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(380,1010,'B580','Pipéracilline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(381,1010,'B581','Pipéracilline/tazobactam',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(382,1010,'B582','Pristinamycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(383,1010,'B583','Quinupristine-dalfopristine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(384,1010,'B584','Rifampicine',NULL,1018,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(385,1010,'B585','Sparfloxacine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(386,1010,'B586','Spectinomycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(387,1010,'B588','Spiramycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(388,1010,'B589','Streptomycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(389,1010,'B590','Sulbactam',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(390,1010,'B591','Teicoplanine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(391,1010,'B592','Télithromycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(392,1010,'B593','Tétracycline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(393,1010,'B594','Ticarcilline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(394,1010,'B595','Ticarcilline/ac. Clavulanique',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(395,1010,'B596','Tigécycline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(396,1010,'B597','Tobramycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(397,1010,'B598','Triméthoprime',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(398,1010,'B599','Triméthoprime/sulfaméthoxazole',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(399,1010,'B600','Vancomycine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(400,1010,'B601','Antibiogramme','ATB',18,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(401,1010,'B602','Examen cytobactériologique des crachats (Ziehl Neelsen)',NULL,18,NULL,'B',NULL,NULL,6,50,170,4),(402,1010,'B603','Recherche de Plasmodium (Goutte épaisse   Frottis)',NULL,15,NULL,'B',NULL,NULL,1,138,170,4),(403,1010,'B604','Examen parasitologique des urines',NULL,15,NULL,'B',15,NULL,3,153,170,4),(404,1010,'B605','Isionazide',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(405,1010,'B606','Ethambutol',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(406,1010,'B607','Pyrazinamide',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,170,4),(407,1010,'B608','Fièvre jaune',NULL,11,NULL,'B',NULL,NULL,1,138,170,4),(408,1010,'B609','Rougeole',NULL,11,NULL,'B',NULL,NULL,1,138,170,4),(410,1010,'B611','Toxoplasmose',NULL,11,NULL,'B',NULL,NULL,1,138,170,4),(411,1010,'B612','Poliomyélite (DPV)','DPV',12,NULL,'B',NULL,NULL,3,153,170,4),(412,1010,'B614','Schistosomiase (urines)',NULL,15,NULL,'B',NULL,NULL,3,153,170,4),(413,1010,'B616','Filariose',NULL,11,NULL,'B',NULL,NULL,1,138,170,4),(414,1010,'B617','Choléra',NULL,18,NULL,'B',NULL,NULL,4,141,170,4),(415,1010,'B615','Schistosomiase (selles)',NULL,15,NULL,'B',NULL,NULL,4,141,170,4),(416,1010,'B700','potassium par photométrie de flamme',NULL,11,NULL,'B',20,NULL,NULL,138,NULL,4),(417,1010,'B702','Recherche de Cryptococcus neoformans',NULL,16,NULL,'B',NULL,NULL,NULL,99,NULL,4),(418,1010,'B703','Recherche de Trypanosomes dans le LCR',NULL,15,NULL,'B',NULL,NULL,5,99,NULL,4),(419,1010,'B705','Antibiogramme enterobacteries',NULL,18,NULL,'B',NULL,NULL,23,NULL,NULL,4),(420,1010,'B750','Glycémie Postprandiale','PP',11,NULL,'B',10,NULL,1,138,NULL,4),(421,1010,'B751','Glycorachie',NULL,13,NULL,'B',NULL,NULL,5,99,NULL,4),(422,1010,'B752','Bandelettes urinaires',NULL,12,NULL,'B',NULL,NULL,3,153,NULL,4),(423,1010,'B756','Facteur rhumatoïde (Waaler-Rose)',NULL,302,NULL,'B',NULL,NULL,1,138,NULL,4),(424,1010,'PB24','Prélèvement génital',NULL,NULL,NULL,'PB',NULL,NULL,NULL,NULL,NULL,4),(425,1010,'GX','Genexpert MTBRIf','GX TUB',23,NULL,'B',50,NULL,6,50,NULL,4),(426,1010,'BEB','Bactériologie des eaux de boisson','BACEAUB',24,NULL,'B',40,NULL,NULL,1014,NULL,4),(427,1010,'CLMB','Culture liquide des mycobatéries','CLMB TUB',18,NULL,'B',NULL,NULL,NULL,50,NULL,4),(428,1010,'ABCL','Antibiogramme 1ère ligne des mycobactéries en milieu liquide','ATBBKML TUB',18,NULL,'B',NULL,NULL,NULL,163,NULL,4),(429,1010,'LPA','Line Probe Assay 1ère ligne tuberculose','LPA',23,NULL,'B',NULL,NULL,NULL,50,NULL,4),(430,1010,'NFR','num formule reticu','Nfr',1001,NULL,'B',21,NULL,1,138,NULL,4),(431,1010,'TBMI','Microscopie ZN de la tuberculose','TB ZN TUB',18,NULL,'B',NULL,NULL,NULL,50,NULL,4),(432,1010,'B757','Hémogramme ','NFS naissance',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(433,1010,'B758','Hémogramme ','NFS 1 semaine',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(434,1010,'B759','Hémogramme ','NFS - 1 mois',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(435,1010,'B760','Hémogramme ','NFS - 2 mois',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(436,1010,'B761','Hémogramme ','NFS - 3 mois',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(437,1010,'B762','Hémogramme ','NFS - 6 mois',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(438,1010,'B763','Hémogramme','NFS - 1 an',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(439,1010,'B764','Hémogramme','NFS - 3 ans',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(440,1010,'B765','Hémogramme','NFS - 3 - 6 ans ',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(441,1010,'B766','Hémogramme','NFS - 7 à 10 ans',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(442,1010,'B767','Hémogramme','NFS - Femmes ',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(443,1010,'B768','Hémogramme','NFS - Hommes',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(444,1010,'B769','ATB Streptococcus sp',NULL,18,NULL,'B',NULL,NULL,NULL,NULL,NULL,4),(445,1010,'B770','ATB Haemophilus influenzae',NULL,18,NULL,'B',NULL,NULL,NULL,NULL,NULL,4),(446,1010,'B771','ATB Neisseria meningitidis ',NULL,18,NULL,'B',NULL,NULL,NULL,NULL,NULL,4),(447,1010,'B772','ATB Neisseria gonorrhoae',NULL,18,NULL,'B',NULL,NULL,NULL,NULL,NULL,4),(448,1010,'B773','ATB Enterococcus sp',NULL,18,NULL,'B',NULL,NULL,NULL,NULL,NULL,4),(449,1010,'B774','ATB Pneumocoque',NULL,18,NULL,'B',NULL,NULL,NULL,NULL,NULL,4),(450,1010,'B775','ATB BGN non fermentaires',NULL,18,NULL,'B',NULL,NULL,NULL,NULL,NULL,4),(451,1010,'B776','ATB Staphylococcus sp',NULL,18,NULL,'B',NULL,NULL,NULL,NULL,NULL,4),(452,1010,'B777','Protéines Liquide de ponction',NULL,13,NULL,'B',NULL,NULL,NULL,35,NULL,4),(453,1010,'B778','Examen cytobactériologique de prélèvement auriculaire','ECB auriculaire',18,NULL,'B',NULL,NULL,NULL,163,NULL,4),(454,1010,'B779','Examen cytobactériologique de prélèvement occulaire','ECB occulaire',18,NULL,'B',NULL,NULL,NULL,163,NULL,4),(455,1010,'B780','Examen cytobactériologique de prélèvement de gorge ','ECB gorge ',18,NULL,'B',NULL,NULL,NULL,75,NULL,4),(456,1010,'781','Dépistage syphilis ',NULL,1003,NULL,'B',NULL,NULL,NULL,138,NULL,4),(457,1010,'B781','Depistage syphilis ','Syphilis SD Bioline',1003,NULL,'B',NULL,NULL,NULL,138,NULL,4),(458,1010,'B782','Examen cytobactériologique des crachats ','ECBC',18,NULL,'B',NULL,NULL,NULL,50,NULL,4),(459,1010,'b783','Recherche de schizocytes ','Recherche schizo',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(460,1010,'B784','Recherche de cellules anormales','cellules ano',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(461,1010,'B785','Formule leucocytaire','Formu leuco',1001,NULL,'B',NULL,NULL,NULL,138,NULL,4),(462,1010,'B786','Examen Cytobactériologique de Pus ','ECB Pus',18,NULL,'B',NULL,NULL,NULL,163,NULL,4),(463,1010,'B787','Examen cytobactériologique de liquide de drainage','ECB LD',18,NULL,'B',NULL,NULL,NULL,163,NULL,4),(464,1010,'B788','Examen bacteriologique d\'aspiration tracheale','ASPI TRACH',18,NULL,'B',NULL,NULL,NULL,163,NULL,4),(465,1010,'B789','Examen bacteriologique de liquide de lavage bronchoalveolaire','LBA',18,NULL,'B',NULL,NULL,NULL,102,NULL,4),(466,1010,'B790','Examen bacteriologique de materiel','EBM',NULL,NULL,'B',NULL,NULL,NULL,163,NULL,4),(467,1010,'B791','Examen bacteriologique de materiels','EBM',18,NULL,'B',NULL,NULL,NULL,163,NULL,4),(468,1010,'B793','ATB Enterobacteries','ATB Enterobac',18,NULL,'B',NULL,NULL,NULL,NULL,NULL,4),(469,1000,'B650','Antibiogramme Méningocoques [DISK]','ABG Méningocoques',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(470,1000,'B651','Antibiogramme Staphylococcus aureus [DISK]','ABG Staphylo. aureus',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(471,1000,'B652','Antibiogramme Pneumocoques [DISK]','ABG Pneumocoques',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(472,1000,'B653','Antibiogramme Haemophilus influenzae [DISK]','ABG H. influenzae',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(473,1000,'B654','Antibiogramme Pseudomonas [DISK]','ABG Pseudomonas',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(474,1000,'B655','Antibiogramme Acinetobacter [DISK]','ABG Acinetobacter',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(475,1000,'B656','Antibiogramme Escherichia coli [DISK]','ABG Escherichia coli',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(476,1000,'B657','Antibiogramme Salmonella spp [DISK]','ABG Salmonella spp',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(477,1000,'B658','Antibiogramme Shigella spp [DISK]','ABG Shigella spp',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(478,1000,'B670','Antibiogramme Méningocoques [CMI]','ABG Méningocoques',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(479,1000,'B671','Antibiogramme Staphylococcus aureus [CMI]','ABG Staphylo. aureus',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(480,1000,'B672','Antibiogramme Pneumocoques [CMI]','ABG Pneumocoques',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(481,1000,'B673','Antibiogramme Haemophilus influenzae [CMI]','ABG H. influenzae',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(482,1000,'B674','Antibiogramme Pseudomonas [CMI]','ABG Pseudomonas',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(483,1000,'B675','Antibiogramme Acinetobacter [CMI]','ABG Acinetobacter',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(484,1000,'B676','Antibiogramme Escherichia coli [CMI]','ABG Escherichia coli',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(485,1000,'B677','Antibiogramme Salmonella spp [CMI]','ABG Salmonella spp',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4),(486,1000,'B678','Antibiogramme Shigella spp [CMI]','ABG Shigella spp',18,NULL,'B',NULL,'[WHONET]',NULL,NULL,NULL,4);
/*!40000 ALTER TABLE `sigl_05_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_data_group`
--

DROP TABLE IF EXISTS `sigl_05_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_05_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=501 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_data_group`
--

LOCK TABLES `sigl_05_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_05_data_group` DISABLE KEYS */;
INSERT INTO `sigl_05_data_group` VALUES (472,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000),(8,8,1000),(9,9,1000),(10,10,1000),(11,11,1000),(12,12,1000),(13,13,1000),(14,14,1000),(15,15,1000),(16,16,1000),(17,17,1000),(18,18,1000),(19,19,1000),(20,20,1000),(21,21,1000),(22,22,1000),(23,23,1000),(471,24,1000),(25,25,1000),(26,26,1000),(27,27,1000),(28,28,1000),(29,29,1000),(30,30,1000),(31,31,1000),(32,32,1000),(33,33,1000),(34,34,1000),(35,35,1000),(36,36,1000),(469,37,1000),(38,38,1000),(39,39,1000),(40,40,1000),(41,41,1000),(42,42,1000),(43,43,1000),(44,44,1000),(45,45,1000),(46,46,1000),(47,47,1000),(48,48,1000),(49,49,1000),(50,50,1000),(51,51,1000),(52,52,1000),(53,53,1000),(54,54,1000),(55,55,1000),(56,56,1000),(473,57,1000),(474,58,1000),(475,59,1000),(60,60,1000),(61,61,1000),(62,62,1000),(63,63,1000),(64,64,1000),(65,65,1000),(66,66,1000),(67,67,1000),(68,68,1000),(69,69,1000),(70,70,1000),(71,71,1000),(72,72,1000),(73,73,1000),(74,74,1000),(75,75,1000),(76,76,1000),(476,77,1000),(78,78,1000),(79,79,1000),(80,80,1000),(81,81,1000),(82,82,1000),(83,83,1000),(84,84,1000),(85,85,1000),(86,86,1000),(87,87,1000),(88,88,1000),(89,89,1000),(90,90,1000),(91,91,1000),(92,92,1000),(93,93,1000),(94,94,1000),(95,95,1000),(96,96,1000),(97,97,1000),(98,98,1000),(99,99,1000),(100,100,1000),(101,101,1000),(102,102,1000),(103,103,1000),(104,104,1000),(105,105,1000),(106,106,1000),(107,107,1000),(108,108,1000),(109,109,1000),(110,110,1000),(111,111,1000),(112,112,1000),(113,113,1000),(114,114,1000),(115,115,1000),(116,116,1000),(117,117,1000),(118,118,1000),(119,119,1000),(120,120,1000),(121,121,1000),(122,122,1000),(477,123,1000),(124,124,1000),(125,125,1000),(126,126,1000),(127,127,1000),(128,128,1000),(129,129,1000),(130,130,1000),(131,131,1000),(132,132,1000),(133,133,1000),(134,134,1000),(478,135,1000),(479,136,1000),(137,137,1000),(480,138,1000),(139,139,1000),(481,140,1000),(141,141,1000),(142,142,1000),(143,143,1000),(482,144,1000),(145,145,1000),(146,146,1000),(147,147,1000),(148,148,1000),(149,149,1000),(150,150,1000),(151,151,1000),(152,152,1000),(153,153,1000),(154,154,1000),(155,155,1000),(156,156,1000),(157,157,1000),(158,158,1000),(159,159,1000),(160,160,1000),(161,161,1000),(483,162,1000),(163,163,1000),(164,164,1000),(165,165,1000),(166,166,1000),(167,167,1000),(168,168,1000),(169,169,1000),(170,170,1000),(171,171,1000),(172,172,1000),(173,173,1000),(174,174,1000),(175,175,1000),(176,176,1000),(177,177,1000),(178,178,1000),(179,179,1000),(180,180,1000),(181,181,1000),(182,182,1000),(183,183,1000),(184,184,1000),(185,185,1000),(186,186,1000),(187,187,1000),(188,188,1000),(189,189,1000),(190,190,1000),(191,191,1000),(192,192,1000),(193,193,1000),(194,194,1000),(195,195,1000),(196,196,1000),(197,197,1000),(198,198,1000),(199,199,1000),(200,200,1000),(201,201,1000),(484,202,1000),(203,203,1000),(204,204,1000),(485,205,1000),(206,206,1000),(207,207,1000),(208,208,1000),(209,209,1000),(210,210,1000),(211,211,1000),(212,212,1000),(213,213,1000),(214,214,1000),(215,215,1000),(216,216,1000),(217,217,1000),(218,218,1000),(500,219,1000),(486,220,1000),(487,221,1000),(488,222,1000),(489,223,1000),(490,224,1000),(225,225,1000),(226,226,1000),(491,227,1000),(228,228,1000),(229,229,1000),(230,230,1000),(492,231,1000),(493,232,1000),(233,233,1000),(234,234,1000),(235,235,1000),(236,236,1000),(237,237,1000),(239,239,1000),(240,240,1000),(241,241,1000),(242,242,1000),(243,243,1000),(244,244,1000),(245,245,1000),(246,246,1000),(247,247,1000),(494,248,1000),(495,249,1000),(496,250,1000),(497,251,1000),(252,252,1000),(253,253,1000),(254,254,1000),(255,255,1000),(256,256,1000),(257,257,1000),(258,258,1000),(259,259,1000),(260,260,1000),(261,261,1000),(262,262,1000),(263,263,1000),(264,264,1000),(265,265,1000),(266,266,1000),(267,267,1000),(268,268,1000),(269,269,1000),(270,270,1000),(271,271,1000),(272,272,1000),(273,273,1000),(274,274,1000),(275,275,1000),(498,276,1000),(499,277,1000),(278,278,1000),(279,279,1000),(280,280,1000),(281,281,1000),(282,282,1000),(283,283,1000),(284,284,1000),(285,285,1000),(286,286,1000),(287,287,1000),(288,288,1000),(289,289,1000),(290,290,1000),(291,291,1000),(292,292,1000),(293,293,1000),(294,294,1000),(295,295,1000),(296,296,1000),(297,297,1000),(298,298,1000),(299,299,1000),(300,300,1000),(301,301,1000),(302,302,1000),(303,303,1000),(304,304,1000),(305,305,1000),(470,306,1000),(307,307,1000),(308,308,1000),(309,309,1000),(310,310,1000),(311,311,1000),(312,312,1000),(313,313,1000),(314,314,1000),(315,315,1000),(316,316,1000),(317,317,1000),(318,318,1000),(319,319,1000),(320,320,1000),(321,321,1000),(322,322,1000),(323,323,1000),(324,324,1000),(325,325,1000),(326,326,1000),(327,327,1000),(328,328,1000),(329,329,1000),(330,330,1000),(331,331,1000),(332,332,1000),(333,333,1000),(334,334,1000),(335,335,1000),(336,336,1000),(337,337,1000),(338,338,1000),(339,339,1000),(340,340,1000),(341,341,1000),(342,342,1000),(343,343,1000),(344,344,1000),(345,345,1000),(346,346,1000),(347,347,1000),(348,348,1000),(349,349,1000),(350,350,1000),(351,351,1000),(352,352,1000),(353,353,1000),(354,354,1000),(355,355,1000),(356,356,1000),(357,357,1000),(358,358,1000),(359,359,1000),(360,360,1000),(361,361,1000),(362,362,1000),(363,363,1000),(364,364,1000),(365,365,1000),(366,366,1000),(367,367,1000),(368,368,1000),(369,369,1000),(370,370,1000),(371,371,1000),(372,372,1000),(373,373,1000),(374,374,1000),(375,375,1000),(376,376,1000),(377,377,1000),(378,378,1000),(379,379,1000),(380,380,1000),(381,381,1000),(382,382,1000),(383,383,1000),(384,384,1000),(385,385,1000),(386,386,1000),(387,387,1000),(388,388,1000),(389,389,1000),(390,390,1000),(391,391,1000),(392,392,1000),(393,393,1000),(394,394,1000),(395,395,1000),(396,396,1000),(397,397,1000),(398,398,1000),(399,399,1000),(400,400,1000),(401,401,1000),(402,402,1000),(403,403,1000),(404,404,1000),(405,405,1000),(406,406,1000),(407,407,1000),(408,408,1000),(410,410,1000),(411,411,1000),(412,412,1000),(413,413,1000),(414,414,1000),(415,415,1000),(416,416,1000),(417,417,1000),(418,418,1000),(419,419,1000),(420,420,1000),(421,421,1000),(422,422,1000),(423,423,1000),(424,424,1000),(425,425,1000),(426,426,1000),(427,427,1000),(428,428,1000),(429,429,1000),(430,430,1000),(431,431,1000),(432,432,1000),(433,433,1000),(434,434,1000),(435,435,1000),(436,436,1000),(437,437,1000),(438,438,1000),(439,439,1000),(440,440,1000),(441,441,1000),(442,442,1000),(443,443,1000),(444,444,1000),(445,445,1000),(446,446,1000),(447,447,1000),(448,448,1000),(449,449,1000),(450,450,1000),(451,451,1000),(452,452,1000),(453,453,1000),(454,454,1000),(455,455,1000),(456,456,1000),(457,457,1000),(458,458,1000),(459,459,1000),(460,460,1000),(461,461,1000),(462,462,1000),(463,463,1000),(464,464,1000),(465,465,1000),(466,466,1000),(467,467,1000),(468,468,1000);
/*!40000 ALTER TABLE `sigl_05_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_05_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_05_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_data_group_mode`
--

LOCK TABLES `sigl_05_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_05_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_05_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_05_deleted`
--

DROP TABLE IF EXISTS `sigl_05_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_05_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `code` varchar(4) NOT NULL,
  `nom` varchar(120) NOT NULL,
  `abbr` varchar(20) DEFAULT NULL,
  `famille` int(10) unsigned DEFAULT NULL,
  `paillasse` int(10) unsigned DEFAULT NULL,
  `cote_unite` varchar(2) DEFAULT NULL,
  `cote_valeur` int(3) unsigned DEFAULT NULL,
  `commentaire` text,
  `produit_biologique` int(10) unsigned DEFAULT NULL,
  `type_prel` int(10) unsigned DEFAULT NULL,
  `type_analyse` int(10) unsigned DEFAULT NULL,
  `actif` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `code` (`code`),
  KEY `id_owner` (`id_owner`),
  KEY `sigl_05_data_ibfk_3` (`famille`),
  KEY `sigl_05_data_ibfk_4` (`paillasse`),
  KEY `sigl_05_data_ibfk_5` (`produit_biologique`),
  KEY `sigl_05_data_ibfk_6` (`type_prel`),
  KEY `sigl_05_data_ibfk_7` (`type_analyse`),
  KEY `sigl_05_data_ibfk_8` (`actif`)
) ENGINE=InnoDB AUTO_INCREMENT=410 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_05_deleted`
--

LOCK TABLES `sigl_05_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_05_deleted` DISABLE KEYS */;
INSERT INTO `sigl_05_deleted` VALUES (238,1010,'B219','Rougeole (IgG et IgM)',NULL,302,NULL,'B',150,'Recherche et titrage éventuel des anticorps, préciser la ou les techniques utilisées avec leur seuil de sensibilité. Une technique de confirmation s?impose quand les tests de dépistage sont positifs ou discordants. Une seule technique de confirmation peut être cotée.',1,138,170,4),(409,1010,'B610','Rubéole',NULL,11,NULL,'B',NULL,NULL,1,138,170,4);
/*!40000 ALTER TABLE `sigl_05_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_06_data`
--

DROP TABLE IF EXISTS `sigl_06_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_06_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `identifiant` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `label` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `value` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `identifiant` (`identifiant`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_06_data`
--

LOCK TABLES `sigl_06_data` WRITE;
/*!40000 ALTER TABLE `sigl_06_data` DISABLE KEYS */;
INSERT INTO `sigl_06_data` VALUES (1,100,'prix_acte','Prix unitaire des actes de prélévements et d\'analyses','1000'),(2,100,'entete_1','Entête de document 1','Nom du laboratoire'),(3,100,'entete_2','Entête de document 2','Sxxx au capital de xxx € RCS xxx xxx xxx autorisation n°xx xxx'),(4,100,'entete_3','Entête de document 3','Horaires : du lundi au vendredi : 07h00-19h00, le samedi : 07h30-12h00    www.example.com'),(5,100,'entete_adr','Entête de document - Adresse','100 place de la République 10000 Maville'),(6,100,'entete_tel','Entête de document - Téléphone','01 23 45 67 89'),(7,100,'entete_fax','Entête de document - Fax','01 98 76 54 32'),(8,100,'entete_email','Entête de document - Email','labo@examples.com'),(9,100,'entete_ville','Entête de document - Ville','Ma ville'),(10,100,'facturation_pat_hosp','Facturation des patients hospitalisés (1/0)','0'),(11,100,'unite_age_defaut','Unité de l\'age par défaut (Jours, Semaines, Mois, Années)','Années'),(12,100,'auto_logout','Déconnexion automatique (mn)','23'),(13,100,'qualite','Module qualité activé (1/0)','1'),(14,100,'facturation','Module facturation activé (1/0)','1');
/*!40000 ALTER TABLE `sigl_06_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_06_data_group`
--

DROP TABLE IF EXISTS `sigl_06_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_06_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_06_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_06_data_group`
--

LOCK TABLES `sigl_06_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_06_data_group` DISABLE KEYS */;
INSERT INTO `sigl_06_data_group` VALUES (15,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(12,6,1000),(13,7,1000),(8,8,1000),(9,9,1000),(16,10,1000),(17,11,1000),(19,12,1000),(20,13,1000),(21,14,1000);
/*!40000 ALTER TABLE `sigl_06_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_06_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_06_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_06_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_06_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_06_data_group_mode`
--

LOCK TABLES `sigl_06_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_06_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_06_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_06_deleted`
--

DROP TABLE IF EXISTS `sigl_06_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_06_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `identifiant` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `label` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `value` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `identifiant` (`identifiant`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_06_deleted`
--

LOCK TABLES `sigl_06_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_06_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_06_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_07_data`
--

DROP TABLE IF EXISTS `sigl_07_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_07_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `libelle` varchar(120) DEFAULT NULL,
  `description` varchar(120) DEFAULT NULL,
  `unite` int(10) unsigned DEFAULT NULL,
  `normal_min` varchar(20) DEFAULT NULL,
  `normal_max` varchar(20) DEFAULT NULL,
  `commentaire` text,
  `type_resultat` int(10) unsigned DEFAULT NULL,
  `unite2` int(10) unsigned DEFAULT NULL,
  `formule_unite2` varchar(120) DEFAULT NULL,
  `formule` varchar(120) DEFAULT NULL,
  `precision` int(1) unsigned DEFAULT NULL,
  `precision2` int(1) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_07_data_ibfk_1` (`id_owner`),
  KEY `sigl_07_data_ibfk_2` (`unite`),
  KEY `sigl_07_data_ibfk_3` (`type_resultat`),
  KEY `sigl_07_data_ibfk_4` (`unite2`)
) ENGINE=InnoDB AUTO_INCREMENT=803 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_07_data`
--

LOCK TABLES `sigl_07_data` WRITE;
/*!40000 ALTER TABLE `sigl_07_data` DISABLE KEYS */;
INSERT INTO `sigl_07_data` VALUES (1,1010,'Détection et titrage des IgG et de IgM (Toxoplasmose)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,1010,'Acide urique','sang',281,'140','420','Homme : 180 - 420\nFemme : 140 - 360',227,NULL,NULL,NULL,NULL,NULL),(3,1010,'Bicarbonates ',NULL,235,'20','30',NULL,228,NULL,NULL,NULL,NULL,NULL),(4,1010,'Bilirubine totale',NULL,280,NULL,'10',NULL,228,281,'$_1*1.71',NULL,2,2),(5,1010,'Bilirubine directe (conjuguée)',NULL,280,NULL,'2',NULL,228,281,'$_1 * 1.7105',NULL,1,1),(6,1010,'Bilirubine libre',NULL,280,NULL,'9.9',NULL,228,281,'$_1 * 1.7105',NULL,1,1),(7,1010,'Créatinine','sang',281,NULL,NULL,'1 - 4 ans : 18 - 35\n4 - 13 ans : 31 - 68 \n13 - 17 ans : 37 - 88\nfemme : 45 - 103\nhomme : 55 - 120',227,NULL,NULL,NULL,1,NULL),(8,1010,'Glucose','à jeun',235,'4.20','6.40',NULL,228,NULL,NULL,NULL,2,NULL),(9,1010,'Urée',NULL,235,'1.70 ','8.30','prématuré : 1.10 - 8.90\n< 1 an : 1.40 - 6.80\nenfant: 1.80 - 6.40\n',228,NULL,NULL,NULL,2,NULL),(10,1010,'Ammoniaque',NULL,281,NULL,NULL,'Technique : calorimétrie',228,NULL,NULL,NULL,NULL,NULL),(11,1010,'Calcium (Calcémie)',NULL,280,'88','104',NULL,227,235,'$_1 * 0.0249',NULL,NULL,1),(12,1010,'Calcémie totale',NULL,235,'2. 15 ','2.50','prématuré: 1.55 - 2.75\nJ0 - 10j: 1.90 - 2.60\n10 j - 24 mois: 2.25 - 2.75\n24 mois - 12 ans: 2.20 - 2.70\n12 ans - 18 ans : 2.10 - 2.55',228,NULL,NULL,NULL,1,NULL),(13,1010,'Chlore (chlorémie)',NULL,297,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(14,1010,'Chlore ',NULL,235,'98','106',NULL,228,NULL,NULL,NULL,NULL,NULL),(15,1010,'Fer sérique',NULL,280,'0.5','1.7',NULL,228,281,'$_1*17.92',NULL,1,2),(16,1010,'Potassium ',NULL,235,'3.6','4.5',NULL,228,NULL,NULL,NULL,1,NULL),(17,1010,'Sodium ',NULL,235,'135','145',NULL,228,NULL,NULL,NULL,NULL,NULL),(18,1010,'Lithium',NULL,235,NULL,NULL,'Zone thérapeutique : 0.5 à 1.5',228,NULL,NULL,NULL,2,NULL),(19,1010,'Magnésium plasmatique',NULL,235,'0.70','1',NULL,228,NULL,NULL,NULL,2,NULL),(20,1010,'Magnésium érythrocytaire',NULL,280,NULL,NULL,NULL,228,235,NULL,NULL,NULL,NULL),(21,1010,'Phosphates','sang',235,'0.81 ','1.62','enfant: 1.29 - 2.25',228,NULL,NULL,NULL,2,NULL),(22,1010,'Potassium par photométrie de flamme',NULL,297,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(23,1010,'sodium par photométrie de flamme',NULL,297,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(24,1010,'Potassium sanguin',NULL,297,NULL,NULL,'Méthode : colorimétrie',228,NULL,NULL,NULL,NULL,NULL),(25,1010,'Sodium sanguin',NULL,297,NULL,NULL,'Méthode : colorimétrie',228,NULL,NULL,NULL,NULL,NULL),(26,1010,'Cholestérol total',NULL,235,'3.60 ','6.20',NULL,228,NULL,NULL,NULL,2,NULL),(27,1010,'Cholestérol HDL',NULL,282,'0.35','0.62',NULL,228,235,'$_2*2.58',NULL,2,2),(28,1010,'Cholestérol LDL (saisie manuelle)',NULL,282,NULL,'1.6',NULL,228,235,'$_1 * 2.578',NULL,NULL,NULL),(29,1010,'Cholestérol total',NULL,282,'1.36','2.4',NULL,228,235,'$_1*2.58',NULL,2,2),(30,1010,'Triglycérides',NULL,282,'0.44','1.5',NULL,228,235,'$_3*1.14',NULL,2,2),(31,1010,'Cholésterol LDL calculé',NULL,282,NULL,'1.6',NULL,229,235,'($_1 - $_2 - ($_3 / 5.6))*2.58','$_1 - $_2 - ($_3 / 5.6)',NULL,2),(32,1010,'Indice d\'athérogénicité',NULL,NULL,NULL,'4.5',NULL,229,NULL,NULL,'$_1/$_2',2,NULL),(33,1010,'Triglycérides',NULL,235,'0.46','1.71',NULL,228,NULL,NULL,NULL,2,NULL),(34,1010,'Alpha-lipoprotéines',NULL,236,'20','30',NULL,228,NULL,NULL,NULL,NULL,NULL),(35,1010,'Pré-béta-lipoprotéines',NULL,237,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(36,1010,'Béta-lipoprotéine',NULL,236,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(37,1010,'Chylomicrons',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(38,1010,'Chylomicrons',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(39,1010,'Lipoprotéine A1 par immunologie',NULL,282,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(40,1010,'Lipoprotéine B par immunologie',NULL,282,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(41,1010,'Albumine',NULL,282,'35','50','0 - 4 jours: 28 -44 \n4j - 14 ans: 38 - 54 \n14 - 18 ans: 32 - 45 \n18 - 60 ans: 34 - 48',227,NULL,NULL,NULL,NULL,NULL),(42,1010,'Albumine','Dosage générique',282,'35','50',NULL,227,NULL,NULL,NULL,NULL,NULL),(43,1010,'Hémoglobine sans tracé',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(44,1010,'Albumine','urines',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(45,1010,'Alpha 1 globuline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(46,1010,'Alpha 2 globuline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(47,1010,'Bétaglobuline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(48,1010,'Gammaglobuline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(49,1010,'Albumine','urines',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(50,1010,'Hémoglobine glyquée (Hb A1c)',NULL,239,NULL,'6.5',NULL,228,NULL,NULL,NULL,1,NULL),(51,1010,'Hémoglobine F',NULL,239,NULL,NULL,'Dosage par HPLC',228,NULL,NULL,NULL,NULL,NULL),(52,1010,'Hémoglobine S',NULL,239,NULL,NULL,'Test de solubilité',228,NULL,NULL,NULL,NULL,NULL),(53,1010,'Myoglobine',NULL,283,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(54,1010,'Protéines de Bences Jones (recherche)',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(55,1010,'Protéines de Bences Jones (recherche)',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(56,1010,'Protéines de Bences Jones par électrophorèse',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(57,1010,'Protéines totales','sang',282,'60','80',NULL,227,NULL,NULL,NULL,2,NULL),(58,1010,'CRP',NULL,280,NULL,'6','Par test rapide',227,NULL,NULL,NULL,NULL,NULL),(59,1010,'Protéine C Réactive quantitative',NULL,280,NULL,'6','Par spectrophotométrie',227,NULL,NULL,NULL,NULL,NULL),(60,1010,'Troponine  semi-quantitative',NULL,283,NULL,NULL,'Par test rapide',228,NULL,NULL,NULL,NULL,NULL),(61,1010,'Troponine',NULL,283,NULL,'0.1','Par méthode immunologique',228,NULL,NULL,NULL,NULL,NULL),(62,1010,'pH',NULL,NULL,'7.37','7.49',NULL,228,NULL,NULL,NULL,NULL,NULL),(63,1010,'Pression artérielle d\'oxygène (PaO2)',NULL,238,'90',NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(64,1010,'Pression artérielle de gaz carbonique (PCO2)',NULL,238,'38','42',NULL,228,NULL,NULL,NULL,NULL,NULL),(65,1010,'Saturation en oxygène (SaO2)',NULL,239,'5','98',NULL,228,NULL,NULL,NULL,NULL,NULL),(66,1010,'CO2 total',NULL,235,'26','30',NULL,228,NULL,NULL,NULL,NULL,NULL),(67,1010,'Amylase',NULL,284,'18','102',NULL,227,NULL,NULL,NULL,NULL,NULL),(68,1010,'Créatine PhosphoKinase (CPK)',NULL,284,'29','200',NULL,227,NULL,NULL,NULL,NULL,NULL),(69,1010,'Créatine PhosphoKinase MB (CPK-MB)',NULL,284,NULL,'25',NULL,227,NULL,NULL,NULL,NULL,NULL),(70,1010,'5\'Nucléotidase',NULL,284,'0.5','5.5','Normales : Enfant : 0.5 - 3.5 / Adultes : 1.5 - 5.5',228,NULL,NULL,NULL,1,NULL),(71,1010,'Gamma glutamyl transférase (GGT)',NULL,284,'7','65',NULL,227,NULL,NULL,NULL,NULL,NULL),(72,1010,'Glucose -6-Phosphate Déshydrogénase (G6PD) ',NULL,284,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(73,1010,'Lactate Déshydrogénase (LDH)',NULL,284,'228','456',NULL,227,NULL,NULL,NULL,NULL,NULL),(74,1010,'Phosphatases Alcalines',NULL,284,'75','240',NULL,227,NULL,NULL,NULL,NULL,NULL),(75,1010,'Phosphatases Acides',NULL,284,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(76,1010,'Transaminases (ASAT)',NULL,284,'10','40',NULL,227,NULL,NULL,NULL,NULL,NULL),(77,1010,'Transaminases (ALAT)',NULL,284,'10','45',NULL,227,NULL,NULL,NULL,NULL,NULL),(78,1010,'Lipase',NULL,284,'7','58',NULL,227,NULL,NULL,NULL,NULL,NULL),(79,1010,'Béta HCG dosage',NULL,284,NULL,'5',NULL,227,NULL,NULL,NULL,NULL,NULL),(80,1010,'Cortisol',NULL,285,'275','685',NULL,227,NULL,NULL,NULL,NULL,NULL),(81,1010,'Erythropoïtine',NULL,284,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(82,1010,'Estradiol',NULL,287,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(83,1010,'Ferritine',NULL,286,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(84,1010,'FSH',NULL,284,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(85,1010,'Insuline',NULL,298,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(86,1010,'Insuline libre',NULL,298,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(87,1010,'LH',NULL,284,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(88,1010,'Progestérone',NULL,285,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(89,1010,'Prolactine',NULL,286,'5','35',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(90,1010,'Thyroglobuline',NULL,283,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(91,1010,'Thyroxine libre (FT4)',NULL,288,'9','20',NULL,228,NULL,NULL,NULL,NULL,NULL),(92,1010,'Testostérone',NULL,286,'0.1','10.6',NULL,228,NULL,NULL,NULL,NULL,NULL),(93,1010,'Transferrine',NULL,282,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(94,1010,'Triiodothyronine libre (FT3)',NULL,288,'4','8.3',NULL,228,NULL,NULL,NULL,NULL,NULL),(95,1010,'TSH Ultrasensible',NULL,289,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(96,1010,'TSH (Hormone ThyreoStimulante)',NULL,289,'0.25','5',NULL,228,NULL,NULL,NULL,NULL,NULL),(97,1010,'Acétone',NULL,235,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(98,1010,'Acide urique','Dans les urines',249,'400','800','Biochimie LDP',227,234,'$_1 * 0.00595',NULL,NULL,1),(99,1010,'pH urinaire',NULL,NULL,'5.4','7.2','Méthode électrométrique',228,NULL,NULL,NULL,NULL,NULL),(100,1010,'Créatinine','urines',249,'1000','1800',NULL,227,NULL,NULL,NULL,NULL,NULL),(101,1010,'Pigments biliaires',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(102,1010,'Pigments biliaires',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(103,1010,'Recherche de sang (hématies et/ou hémoglobine)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(104,1010,'Sels biliaires',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(105,1010,'Sels biliaires',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(106,1010,'Glucose','à jeun',282,'0.7','1.04',NULL,228,235,'$_1 * 5.551',NULL,2,2),(107,1010,'Glucose','bandelettes',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(108,1010,'Glucose','bandelettes',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(109,1010,'Urée',NULL,290,NULL,NULL,NULL,228,234,'$_1 * 16.65',NULL,NULL,NULL),(110,1010,'Calcium (Calciurie)',NULL,249,'102','251',NULL,227,234,'$_1 * 0.0249',NULL,NULL,NULL),(111,1010,'Phosphates','sang',280,'24.8','44.9',NULL,228,235,'$_1 * 0.0323',NULL,2,2),(112,1010,'Potassium urinaire',NULL,235,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(113,1010,'Sodium urinaire',NULL,235,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(114,1010,'Protéines',NULL,282,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(115,1010,'Microalbumine',NULL,249,NULL,'20','Dosage à l?exclusion des bandelettes',228,NULL,NULL,NULL,1,NULL),(116,1010,'Protéinurie des 24h','urines',290,NULL,'0.15','Femme enceinte < 0.30',228,NULL,NULL,NULL,2,NULL),(117,1010,'Porphyrines (recherche)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(118,1010,'Test de grossesse',NULL,284,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(119,1010,'Test de grossesse',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(120,1010,'Alpha 1-4 glucosidase séminale',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(121,1010,'Carnitine libre séminale',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(122,1010,'Citrate séminal',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(123,1010,'Fructose séminal',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(124,1010,'Protéines totales (LCR)',NULL,282,'0.2','0.6',NULL,228,NULL,NULL,NULL,1,NULL),(125,1010,'Rivalta',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(126,1010,'Volume des urines de 24h',NULL,295,NULL,NULL,NULL,228,NULL,NULL,NULL,3,NULL),(127,1010,'Acide urique plasmatique',NULL,280,NULL,NULL,NULL,228,NULL,NULL,NULL,2,NULL),(128,1010,'Acide urique urinaire',NULL,280,NULL,NULL,NULL,228,NULL,NULL,NULL,2,NULL),(129,1010,'Clairance de l\'acide urique',NULL,296,'88','138','Normales : Homme : 97 - 137 / Femme : 88 - 138',229,NULL,NULL,'$_3 * $_1 * 1000 / 1440 / $_2',2,NULL),(130,1010,'Urée plasmatique',NULL,280,NULL,NULL,NULL,228,NULL,NULL,NULL,2,NULL),(131,1010,'Urée urinaire',NULL,287,NULL,NULL,NULL,228,NULL,NULL,NULL,2,NULL),(132,1010,'Clairance de l\'urée',NULL,296,'88','138','Normales : Homme : 97 - 137 / Femme : 88 - 138',229,NULL,NULL,'$_3 * $_1 * 1000 / 1440 / $_2',2,NULL),(133,1010,'Créatinine plasmatique',NULL,280,NULL,NULL,NULL,228,NULL,NULL,NULL,2,NULL),(134,1010,'Créatinine urinaire',NULL,280,NULL,NULL,NULL,228,NULL,NULL,NULL,2,NULL),(135,1010,'Clairance de la créatinine',NULL,296,'80',NULL,'Normales : Homme : 97 - 137 / Femme : 88 - 138',229,NULL,NULL,'$_3 * $_1 * 1000 / 1440 / $_2',2,NULL),(136,1010,'GLC à T0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(137,1010,'GLC à 30mn',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(138,1010,'GLC à 60mn',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(139,1010,'GLC à 90mn',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(140,1010,'GLC à 120mn',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(141,1010,'GLC à 150mn',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(142,1010,'GLC à 180mn',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(143,1010,'Test à HCG : dosage de la testostérone',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(144,1010,'Test à HCG : dosage de l\'estradiol',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(145,1010,'Test à la déxaméthasone : dosage du cortisol',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(146,1010,'Lymphocytes',NULL,239,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(147,1010,'Lymphoblastes',NULL,239,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(148,1010,'Plasmocytes',NULL,239,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(149,1010,'Hématocrite (taux)',NULL,239,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(150,1010,'Hémoglobine (dosage par spectrophotomètre)',NULL,243,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(151,1010,'Hémoglobine',NULL,243,'12.0','17.0','Normales : 3 à 10 ans : 12.0 - 14.5 /  Femme : 12.5 - 15.5 / Homme : 14.0 - 17.0',228,NULL,NULL,NULL,1,NULL),(152,1010,'VS 1ère heure',NULL,240,NULL,'10',NULL,227,NULL,NULL,NULL,NULL,NULL),(153,1010,'VS 2ème heure',NULL,240,NULL,'30',NULL,228,NULL,NULL,NULL,2,NULL),(154,1010,'Hématies','Sang',241,'3.5','5.7','Normales : 3 à 10 ans : 3.5 - 5 /  Femme : 4.0 - 5.3 / Homme : 4.2 - 5.7',228,NULL,NULL,NULL,1,NULL),(155,1010,'Hématocrite',NULL,239,'36','52','Normales : 3 à 10 ans : 36 - 45 /  Femme : 37 - 46 / Homme : 40 - 52',227,NULL,NULL,NULL,NULL,NULL),(156,1010,'Volume globulaire (VGM)',NULL,244,'74.0','95.0','Normales : 3 à 10 ans : 74 - 91 / Femme : 80 - 95 / Homme : 80 - 95',229,NULL,NULL,'$_3 * 10 / $_1',1,NULL),(157,1010,'Charge (TCMH)',NULL,245,'24.0','32.0','Normales : 3 à 10 ans : 24 - 30 / Femme : 28 - 32 / Homme : 28 - 32',229,NULL,NULL,'$_2 * 10 / $_1',1,NULL),(158,1010,'Concentration (CCMH)',NULL,239,'28','35','Normales : 3 à 10 ans : 28 - 33 / Femme : 30 - 35 / Homme : 30 - 35',229,NULL,NULL,'100 * $_2 / $_3',1,NULL),(159,1010,'Leucocytes (LCR)',NULL,242,'4.0','13.0','Normales : 3 à 10 ans : 4.5 - 13 / Femme : 4 - 10 / Homme : 4 - 10',228,NULL,NULL,NULL,1,NULL),(160,1010,'Polynucléaires neutrophiles',NULL,239,'40','70',NULL,228,242,'$_4 * $_5 /100',NULL,1,2),(161,1010,'Polynucléaires éosinophiles',NULL,239,'1','3',NULL,228,242,'$_4 * $_6 /100',NULL,1,2),(162,1010,'Polynucléaires basophiles',NULL,239,'1','3',NULL,228,242,'$_4 * $_7 /100',NULL,1,2),(163,1010,'Lymphocytes',NULL,239,'10','30',NULL,228,242,'$_4 * $_8 /100',NULL,1,2),(164,1010,'Monocytes',NULL,239,'4',NULL,NULL,228,242,'$_4 * $_9 /100',NULL,1,2),(165,1010,'Plaquettes',NULL,242,'150','400',NULL,227,NULL,NULL,NULL,NULL,NULL),(166,1010,'Numération',NULL,NULL,NULL,NULL,NULL,265,NULL,NULL,NULL,NULL,NULL),(167,1010,'Formule leucocytaire',NULL,NULL,NULL,NULL,NULL,265,NULL,NULL,NULL,NULL,NULL),(168,1010,'Plaquettes',NULL,NULL,NULL,NULL,NULL,265,NULL,NULL,NULL,NULL,NULL),(169,1010,'Hématies','Sang',1143,'3.0','3.8',NULL,228,NULL,NULL,NULL,1,NULL),(170,1010,'Volume globulaire (VGM)',NULL,244,'98','112',NULL,227,NULL,NULL,NULL,1,NULL),(171,1010,'Concentration (CCMH)',NULL,239,'30.0','34.0',NULL,228,NULL,NULL,NULL,1,NULL),(172,1010,'Leucocytes',NULL,1144,NULL,NULL,NULL,228,NULL,NULL,NULL,1,NULL),(173,1010,'Polynucléaires neutrophiles',NULL,239,NULL,NULL,NULL,228,1144,'$_4 * $_5 /100',NULL,1,2),(174,1010,'Polynucléaires éosinophiles',NULL,239,NULL,NULL,NULL,228,1144,'$_4 * $_6 /100',NULL,1,2),(175,1010,'Polynucléaires basophiles',NULL,239,NULL,NULL,NULL,228,1144,'$_4 * $_7 /100',NULL,1,2),(176,1010,'Lymphocytes',NULL,239,NULL,NULL,NULL,228,1144,'$_4 * $_8 /100',NULL,1,2),(177,1010,'Monocytes',NULL,239,NULL,NULL,NULL,228,1144,'$_4 * $_9 /100',NULL,1,2),(178,1010,'Plaquettes',NULL,1144,'160','500',NULL,227,NULL,NULL,NULL,NULL,NULL),(179,1010,'Nombre de CD4',NULL,626,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(180,1010,'Nombre de CD8',NULL,626,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(181,1010,'Nombre de lumphocytes totaux',NULL,626,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(182,1010,'Taux',NULL,239,NULL,NULL,NULL,229,NULL,NULL,'($1 + $2) * 100 / $3',NULL,NULL),(183,1010,'Numération blanche (méthode manuelle)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(184,1010,'Taux de réticulocyte',NULL,239,'1','3',NULL,228,NULL,NULL,NULL,2,NULL),(185,1010,'Numération des plaquettes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(186,1010,'Recherche d\'hématies foetales',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(187,1010,'Recherche de corps de Heinz',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(188,1010,'Test d\'Emmel',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(189,1010,'Recherche de polynucléaires éosinophiles dans le mucus nasal',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(190,1010,'Recherche de polynucléaires éosinophiles dans les crachats',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(191,1010,'D Dimères',NULL,NULL,NULL,NULL,'Technique : agglutination de particules de latex',NULL,NULL,NULL,NULL,NULL,NULL),(192,1010,'D Dimères',NULL,286,NULL,'500','Technique : ELISA',227,NULL,NULL,NULL,NULL,NULL),(193,1010,'Dosage du fibrinogène',NULL,282,'2','4',NULL,228,NULL,NULL,NULL,NULL,NULL),(194,1010,'Dosage des D dimères: (préciser la technique sur le compte rendu)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(195,1010,'Héparinémie',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(196,1010,'Taux de prothrombine',NULL,239,'80','100',NULL,227,NULL,NULL,NULL,NULL,NULL),(197,1010,'INR',NULL,NULL,NULL,'1',NULL,228,NULL,NULL,NULL,2,NULL),(198,1010,'Temps de saignement',NULL,291,'180','360',NULL,227,NULL,NULL,NULL,NULL,NULL),(199,1010,'TCA ou TCK',NULL,291,'27','35',NULL,227,NULL,NULL,NULL,NULL,NULL),(200,1010,'TCA ou TCK témoin : 28s',NULL,NULL,NULL,NULL,NULL,265,NULL,NULL,NULL,NULL,NULL),(201,1010,'Temps de Thrombine (TT)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(202,1010,'Titrage des Produits de Dégradation de la Fibrine  et/ ou du Fibrinogène(PDF)',NULL,292,NULL,'0.5',NULL,228,NULL,NULL,NULL,NULL,NULL),(203,1010,'Groupe sanguin',NULL,NULL,NULL,NULL,NULL,900,NULL,NULL,NULL,NULL,NULL),(204,1010,'Rhésus',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(205,1010,'Test de Coombs direct ',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(206,1010,'Test de compatibilité',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(207,1010,'Facteur rhumatoïde (test au latex)',NULL,293,NULL,'80',NULL,228,NULL,NULL,NULL,NULL,NULL),(208,1010,'Antistreptolysine O (ASLO)',NULL,293,NULL,'200',NULL,228,NULL,NULL,NULL,NULL,NULL),(209,1010,'Antistreptokinase (ASK)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(210,1010,'Borrelioses (IFI ou EIA)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(211,1010,'Brucelloses (IFI ou EIA)',NULL,293,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(212,1010,'Chlamydiae trachomatis par PCR',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(213,1010,'Titrage',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(215,1010,'Hélicobacter pylori (EIA)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(216,1010,'Mycoplasma pneumoniae (IgG par EIA)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(218,1010,'AO',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(219,1010,'BO',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(220,1010,'CO',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(221,1010,'TO',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(222,1010,'AH',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(223,1010,'BH',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(224,1010,'CH',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(225,1010,'TH',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(226,1010,'ENH',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(227,1010,'Vi',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(228,1010,'Sérodiagnostic de Widal',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(229,1010,'RPR qualitatif (Syphilis)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(230,1010,'Titre','Générique',NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(231,1010,'TPHA  (Syphilis)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(232,1010,'FTA Absorbens IgG (Syphilis)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(233,1010,'FTA Absorbens IgG (Syphilis)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(234,1010,'Recherche des IgM (Syphilis)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(235,1010,'Recherche des IgM (Syphilis)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(236,1010,'Recherche directe de chlamydiae par technique immunologique',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(237,1010,'Recherche d\'une toxine bactérienne par technique immunologique',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(238,1010,'Aspergillose (dépistage)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(239,1010,'Candidose',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(240,1010,'Sérologie',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(241,1010,'Candidose',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(242,1010,'Cryptococcose',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(243,1010,'Dépistage Cysticercose  (EIA ou IFI)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(244,1010,'Dépistage Cysticercose  (EIA ou IFI)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(245,1010,'Titre',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(246,1010,'Test de confirmation Cysticercose (IE)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(247,1010,'Dépistage Filariose (EIA ou IFI)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(248,1010,'Test de confirmation Filariose par IE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(249,1010,'Dépistage Leishmaniose viscérale (EIA ou IFI)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(250,1010,'Test de confirmation Leishmaniose viscérale par IE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(251,1010,'Commentaires',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(252,1010,'Recherche de plasmodium',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(253,1010,'Espece',NULL,NULL,NULL,NULL,NULL,1137,NULL,NULL,NULL,NULL,NULL),(254,1010,'Détection des IgG (Toxoplasmose)',NULL,293,NULL,'8',NULL,227,NULL,NULL,NULL,NULL,NULL),(255,1010,'Détection et titrage des IgA (Toxoplasmose)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(256,1010,'Recherche AgHBs (Hépatite B par test rapide)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(257,1010,'Recherche Ac anti HBs (Hépatite B par test rapide)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(258,1010,'Recherche Ag HBe (Hépatite B par test rapide)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(259,1010,'Recherche Ac anti HBc (Hépatite B par test rapide)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(260,1010,'Recherche AgHBs (Hépatite B par automate d\'immunoanalyse)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(261,1010,'Recherche AgHBs (Hépatite B par automate d\'immunoanalyse)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(262,1010,'Recherche Ac anti HBs (Hépatite B par automate d\'immunoanalyse)',NULL,284,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(263,1010,'Recherche Ag HBe (Hépatite B par automate d\'immunoanalyse)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(264,1010,'Recherche Ac anti HBc (Hépatite B par automate d\'immunoanalyse)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(265,1010,'Recherche Ac anti HBc (Hépatite B)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(266,1010,'Recherche Ac anti HBc IgM (Hépatite B par automate d\'immunoanalyse)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(267,1010,'Recherche Ac anti HBc IgM (Hépatite B par automate d\'immunoanalyse)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(268,1010,'Test de neutralisation de l\'hépatite B',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(269,1010,'Hépatite B ADN par PCR',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(270,1010,'Hépatite B ADN par PCR',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(271,1010,'Hépatite C (par test rapide)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(272,1010,'Hépatite C (par test rapide)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(273,1010,'Recherche des Ac anti VHC (par automate d\'immunoanalyse)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(274,1010,'Recherche des Ac anti VHC (par automate d\'immunoanalyse)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(275,1010,'Test de confirmation Hépatite C',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(276,1010,'Hépatite C ARN par PCR',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(277,1010,'Hépatite C ARN par PCR',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(278,1010,'VIH (test rapide)',NULL,NULL,NULL,NULL,NULL,625,NULL,NULL,NULL,NULL,NULL),(279,1010,'Recherche des Ac anti-VIH (par automate d\'immunoanalyse)',NULL,NULL,NULL,NULL,NULL,625,NULL,NULL,NULL,NULL,NULL),(280,1010,'Recherche des Ac anti-VIH (Test Elisa)',NULL,NULL,NULL,NULL,NULL,625,NULL,NULL,NULL,NULL,NULL),(281,1010,'Recherche',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(282,1010,'Titrage',NULL,293,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(283,1010,'Recherche',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(284,1010,'Mesure de la charge virale ARN VIH-1',NULL,293,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(285,1010,'Herpes virus simplex type 1 (IgG ou IgM)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(286,1010,'Herpes virus simplex type II (IgG ou IgM)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(287,1010,'Recherche de Rotavirus',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(288,1010,'Densité optique ',NULL,NULL,NULL,NULL,'DO > COV  : Positif DO < COV  : Négatif COV -0.010 < DO < COV + 0.010: Indeterminé ',228,NULL,NULL,NULL,2,NULL),(291,1010,'Dosage des immunoglobulines (IgE) totales',NULL,294,NULL,'150',NULL,227,NULL,NULL,NULL,NULL,NULL),(292,1010,'Un seul allergène',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(293,1010,'Dosage des IgG dans le sang, le LCR',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(294,1010,'Dosage des IgM dans le sang, le LCR ',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(295,1010,'Dosage des IgA dans le sang, le LCR ',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(296,1010,'Recherche et titrage de a foetoprotéine (dans le sérum ou liquide amniotique)',NULL,293,NULL,'10',NULL,227,NULL,NULL,NULL,NULL,NULL),(297,1010,'Recherche et titrage de l\'Antigène CarcinoEmbryonnaire (ACE)',NULL,286,NULL,'5',NULL,228,NULL,NULL,NULL,NULL,NULL),(298,1010,'Recherche et titrage de l\'Antigène Prostatique Spécifique (PSA)',NULL,286,NULL,'6.5',NULL,228,NULL,NULL,NULL,NULL,NULL),(299,1010,'Recherche et titrage de l\'Antigène Prostatique Spécifique  libre (PSA libre)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(300,1010,'Recherche et titrage de ß2 microglobuline (dans le sérum ou urine)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(301,1010,'Autres','générique',NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(302,1010,'Shistosoma mansoni',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(303,1010,'Giardia',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(304,1010,'Amibes',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(305,1010,'Anguillules',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(306,1010,'Tenia',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(307,1010,'Ascaris',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(308,1010,'Oxyures',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(309,1010,'Recherche de cryptosporidies par coloration élective',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(310,1010,'Recherche de cryptosporidies par immunofluorescence',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(311,1010,'Recherche de microsporidies dans les selles par coloration élective',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(312,1010,'Recherche de pneumocystis carinii dans le liquide bronchoalvéolaire',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(313,1010,'Recherche de pneumocystis carinii dans le liquide bronchoalvéolaire',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(314,1010,'Densité parasitaire','goutte épaisse ',NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(316,1010,'Goutte épaisse - Frottis mince ',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(317,1010,'Recherche de microfilaires ','recherche générique (biopsie ou sang)',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(318,1010,'Recherche de microfilaires ','recherche générique (biopsie ou sang)',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(319,1010,'Recherche de microfilaire dans le sang',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(320,1010,'espèce','microfilaire',NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(321,1010,'Recherche de levures dans le LCR',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(322,1010,'Recherche de levures dans le LCR',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(323,1010,'Recherche de leishmanies dans une sérosité cutanée',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(324,1010,'Recherche de trypanosomes ','Recherche générique ',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(325,1010,'Recherche de trypanosomes ','Recherche générique ',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(326,1010,'Recherche des champignons dans les prélèvements de peau et phanères',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(327,1010,'champignon (espèce)',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(328,1010,'Recherche des champignons dans les prélèvements de peau et phanères',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(329,1010,'Culture des levures',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(330,1010,'Parasites','ECBU',NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(331,1010,'Autre','Urines',NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(332,1010,'Flore bactérienne','générique ',NULL,NULL,NULL,NULL,590,NULL,NULL,NULL,NULL,NULL),(333,1010,'Coloration de Gram',NULL,NULL,NULL,NULL,NULL,593,NULL,NULL,NULL,NULL,NULL),(334,1010,'Aspect macroscopique',NULL,NULL,NULL,NULL,NULL,598,NULL,NULL,NULL,NULL,NULL),(335,1010,'Cellules épithéliales','semi quantitatif (néant à très nombreux )',NULL,NULL,NULL,NULL,1133,NULL,NULL,NULL,NULL,NULL),(336,1010,'Leucocytes ',NULL,1004,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(337,1010,'Hématies','Urinaire',1004,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(338,1010,'Levures ',NULL,NULL,NULL,NULL,NULL,597,NULL,NULL,NULL,NULL,NULL),(339,1010,'Cristaux',NULL,NULL,NULL,NULL,NULL,1129,NULL,NULL,NULL,NULL,NULL),(340,1010,'Cylindres',NULL,NULL,NULL,NULL,NULL,1130,NULL,NULL,NULL,NULL,NULL),(341,1010,'Cristaux',NULL,NULL,NULL,NULL,NULL,588,NULL,NULL,NULL,NULL,NULL),(342,1010,'Deuxième bactérie identifiée',NULL,NULL,NULL,NULL,NULL,586,NULL,NULL,NULL,NULL,NULL),(343,1010,'Bactériurie',NULL,1145,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(344,1010,'Culture',NULL,NULL,NULL,NULL,NULL,1128,NULL,NULL,NULL,NULL,NULL),(345,1010,'Aspect du prélèvement vaginal',NULL,NULL,NULL,NULL,NULL,585,NULL,NULL,NULL,NULL,NULL),(346,1010,'Forme des levures',NULL,NULL,NULL,NULL,NULL,591,NULL,NULL,NULL,NULL,NULL),(347,1010,'Trichomonas vaginalis',NULL,NULL,NULL,NULL,NULL,231,NULL,NULL,NULL,NULL,NULL),(348,1010,'Score',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(349,1010,'Coloration de Gram ','prélèvement génitaux',NULL,NULL,NULL,NULL,594,NULL,NULL,NULL,NULL,NULL),(350,1010,'Hématies ',NULL,NULL,NULL,NULL,NULL,1133,NULL,NULL,NULL,NULL,NULL),(351,1010,'Forme des levures',NULL,NULL,NULL,NULL,NULL,1131,NULL,NULL,NULL,NULL,NULL),(352,1010,'score de nugent ',NULL,NULL,NULL,NULL,'Score 0-3: Flore normale\nScore 4-6: Flore intermediaire\nScore >= 7: Flore de vaginose bacterienne',226,NULL,NULL,NULL,NULL,NULL),(353,1010,'Diplocoque Gram negatif ',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(355,1010,'Aspect du col',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(356,1010,'Levures','semiquantitatif (néant à très nombreux)',NULL,NULL,NULL,NULL,599,NULL,NULL,NULL,NULL,NULL),(357,1010,'Germe identifié ','germe',NULL,NULL,NULL,NULL,592,NULL,NULL,NULL,NULL,NULL),(358,1010,'Leucocytes (nombre)',NULL,NULL,NULL,NULL,NULL,1133,NULL,NULL,NULL,NULL,NULL),(361,1010,'culture et identification',NULL,NULL,NULL,NULL,NULL,586,NULL,NULL,NULL,NULL,NULL),(362,1010,'Hématies (nombre)',NULL,NULL,NULL,NULL,NULL,599,NULL,NULL,NULL,NULL,NULL),(363,1010,'Examen direct',NULL,NULL,NULL,NULL,NULL,265,NULL,NULL,NULL,NULL,NULL),(364,1010,'Aspect du prélèvement urétral',NULL,NULL,NULL,NULL,NULL,1127,NULL,NULL,NULL,NULL,NULL),(366,1010,'autres',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(367,1010,'Aspect du prélèvement urétral',NULL,NULL,NULL,NULL,NULL,585,NULL,NULL,NULL,NULL,NULL),(368,1010,'Cellules épithéliales','semi quantitatif (néant à très nombreux )',NULL,NULL,NULL,NULL,599,NULL,NULL,NULL,NULL,NULL),(369,1010,'Leucocytes ',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(370,1010,'Culture','Recherche des mycobactéries',NULL,NULL,NULL,NULL,603,NULL,NULL,NULL,NULL,NULL),(371,1010,'aspect du sperme','texte libre ',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(372,1010,'hematies ','semi quantitatif (neant à très nombreux)',NULL,NULL,NULL,NULL,599,NULL,NULL,NULL,NULL,NULL),(375,1010,'hematies ','semi quantitatif (neant à très nombreux)',1146,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(376,1010,'Aspect du LCR',NULL,NULL,NULL,NULL,NULL,596,NULL,NULL,NULL,NULL,NULL),(377,1010,'Polynucléaires neutrophiles',NULL,239,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(378,1010,'Leucocytes ',NULL,1146,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(379,1010,'Lymphocyte ',NULL,239,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(380,1010,'Aspect du liquide',NULL,NULL,NULL,NULL,NULL,596,NULL,NULL,NULL,NULL,NULL),(381,1010,'Polynucléaires',NULL,239,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(382,1010,'Lévure',NULL,NULL,NULL,NULL,NULL,609,NULL,NULL,NULL,NULL,NULL),(383,1010,'Technique',NULL,NULL,NULL,NULL,NULL,631,NULL,NULL,NULL,NULL,NULL),(384,1010,'PCR',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(385,1010,'Leucocytes ',NULL,1146,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(386,1010,'Hématies',NULL,1146,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(387,1010,'Recherche d\'Antigène soluble',NULL,NULL,NULL,NULL,NULL,595,NULL,NULL,NULL,NULL,NULL),(388,1010,'Culture (  + / -)',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(389,1010,'Germe identifié (bactérie)',NULL,NULL,NULL,NULL,NULL,586,NULL,NULL,NULL,NULL,NULL),(390,1010,'Delai de pousse',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(391,1010,'Aspect des selles',NULL,NULL,NULL,NULL,NULL,584,NULL,NULL,NULL,NULL,NULL),(392,1010,'Leucocytes ',NULL,NULL,NULL,NULL,NULL,1133,NULL,NULL,NULL,NULL,NULL),(393,1010,'Flore bactérienne (abondance)',NULL,NULL,NULL,NULL,NULL,583,NULL,NULL,NULL,NULL,NULL),(394,1010,'Selles KAOP',NULL,NULL,NULL,NULL,NULL,1135,NULL,NULL,NULL,NULL,NULL),(395,1010,'Flore bactérienne ',NULL,NULL,NULL,NULL,NULL,1142,NULL,NULL,NULL,NULL,NULL),(396,1010,'Polynucléaires',NULL,239,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(397,1010,'Lymphocytes',NULL,239,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(398,1010,'Recherche de BAAR',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(399,1010,'Hématies ',NULL,1146,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(400,1010,'Type de Liquide',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(401,1010,'Recherche et identification de campylobacter',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(402,1010,'Recherche et identification des germes anaérobies',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(403,1010,'Spermogramme et spermocytogramme:',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(404,1010,'Test post- coïtal (test de Huhner)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(405,1010,'Recherche d\'une éjaculation rétrograde en cas d\'hypospermie sévère ou anéjaculation',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(406,1010,'Coloration des spermatozoïdes au bleu d\'aniline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(407,1010,'Recherche d\'une immunisation antispermatozoïdes',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(408,1010,'Acide salicylique (dosage)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(409,1010,'Alcool (éthanol ou méthanol)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(410,1010,'Amphétamine (dosage)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(411,1010,'Aluminium',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(412,1010,'Antidépresseurs tricycliques (recherche)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(413,1010,'Barbituriques (recherche)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(414,1010,'Barbituriques (dosage)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(415,1010,'Benzodiazépines (recherche)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(416,1010,'Diazépam et son métabolite (dosage)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(417,1010,'Digoxine (dosage)',NULL,286,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(418,1010,'Isoniazide (INH)',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(419,1010,'Isoniazide (INH)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(420,1010,'Mesure des concentrations plasmatiques des Antrétroviraux',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(421,1010,'Oxyde de carbone',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(422,1010,'Parcétamol (dosage)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(423,1010,'Plomb',NULL,NULL,NULL,NULL,'Technique : Spectrophotométrie d\'absorption atomique',NULL,NULL,NULL,NULL,NULL,NULL),(424,1010,'Quinidine (dosage)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(425,1010,'Rifampicine',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(426,1010,'Théophylline',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(427,1010,'Arsenic',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(428,1010,'Acide fusidique',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(429,1010,'Acide fusidique',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(430,1010,'Acide nalidixique',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(431,1010,'Acide nalidixique',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(432,1010,'Acide oxolinique',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(433,1010,'Acide oxolinique',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(434,1010,'Acide pipémidique',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(435,1010,'Acide pipémidique',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(436,1010,'Acide piromidique',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(437,1010,'Acide piromidique',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(438,1010,'Amikacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(439,1010,'Amikacine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(440,1010,'Amoxicilline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(441,1010,'diamètre inhibition','de l\'antibiogramme',240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(442,1010,'Ampicilline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(443,1010,'Amoxicilline/ac. Clavulanique',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(444,1010,'Amoxicilline/ac. Clavulanique',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(445,1010,'Ampicilline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(446,1010,'Ampicilline/sulbactam',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(447,1010,'Ampicilline/sulbactam',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(448,1010,'Azithromycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(449,1010,'Azithromycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(450,1010,'Aztréonam',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(451,1010,'Aztréonam',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(452,1010,'Bacitracine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(453,1010,'Bacitracine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(454,1010,'Céfaclor',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(455,1010,'Céfaclor',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(456,1010,'Céfadroxil',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(457,1010,'Céfadroxil',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(458,1010,'Céfalexine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(459,1010,'Céfalexine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(460,1010,'céfalotine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(461,1010,'céfalotine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(462,1010,'Céfamandole',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(463,1010,'Céfamandole',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(464,1010,'Céfatrizine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(465,1010,'Céfatrizine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(466,1010,'Céfazoline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(467,1010,'Céfazoline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(468,1010,'Céfépime',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(469,1010,'Céfépime',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(470,1010,'Céfixime',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(471,1010,'Céfixime',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(472,1010,'Céfopérazone',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(473,1010,'Céfopérazone',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(474,1010,'Céfotaxime',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(475,1010,'Céfotaxime',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(476,1010,'Céfotétan',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(477,1010,'Céfotétan',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(478,1010,'Céfotiam',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(479,1010,'Céfotiam',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(480,1010,'Céfotiam-héxétil',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(481,1010,'Céfotiam-héxétil',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(482,1010,'Céfoxitine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(483,1010,'Céfoxitine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(484,1010,'Cefpirome',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(485,1010,'Cefpirome',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(486,1010,'Cefpodoxime-proxétil',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(487,1010,'Cefpodoxime-proxétil',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(488,1010,'Céfradine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(489,1010,'Céfradine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(490,1010,'Cefsulodine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(491,1010,'Cefsulodine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(492,1010,'Ceftazidime',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(493,1010,'Ceftazidime',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(494,1010,'Ceftizoxime',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(495,1010,'Ceftizoxime',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(496,1010,'Ceftriaxone',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(497,1010,'Ceftriaxone',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(498,1010,'Céfuroxime',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(499,1010,'Céfuroxime',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(500,1010,'Céfuroxime-axétil',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(501,1010,'Céfuroxime-axétil',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(502,1010,'Chloramphénicol',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(503,1010,'Levofloxacine ',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(504,1010,'Ciprofloxacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(505,1010,'Norfloxacine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(506,1010,'Clindamycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(507,1010,'Clindamycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(508,1010,'Colistine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(509,1010,'Colistine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(510,1010,'Cotrimoxazole',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(511,1010,'Cotrimoxazole',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(512,1010,'Dirithromycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(513,1010,'Dirithromycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(514,1010,'Doripénème (H)',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(515,1010,'Doripénème (H)',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(516,1010,'Doxycycline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(517,1010,'Doxycycline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(518,1010,'Enoxacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(519,1010,'Enoxacine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(520,1010,'Ertapénème',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(521,1010,'Ertapénème',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(522,1010,'Erythromycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(523,1010,'Erythromycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(524,1010,'Fluméquine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(525,1010,'Fluméquine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(526,1010,'Fosfomycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(527,1010,'Fosfomycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(528,1010,'Gentamicine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(529,1010,'Gentamicine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(530,1010,'Imipénème',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(531,1010,'Imipénème',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(532,1010,'Isépamicine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(533,1010,'Isépamicine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(534,1010,'kanamycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(535,1010,'kanamycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(536,1010,'Latamoxef',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(537,1010,'Latamoxef',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(538,1010,'Lévofloxacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(539,1010,'Lincomycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(540,1010,'Linézolide',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(541,1010,'Linézolide',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(542,1010,'Loméfloxacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(543,1010,'Loméfloxacine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(544,1010,'Loracarbef',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(545,1010,'Loracarbef',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(546,1010,'Méropénème',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(547,1010,'Méropénème',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(548,1010,'Metronidazole',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(549,1010,'Metronidazole',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(550,1010,'Minocycline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(551,1010,'Minocycline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(552,1010,'Moxifloxacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(553,1010,'Moxifloxacine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(554,1010,'Mupirocine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(555,1010,'Mupirocine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(556,1010,'Nétilmicine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(557,1010,'Nétilmicine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(558,1010,'Nitroxoline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(559,1010,'Nitroxoline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(560,1010,'Norfloxacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(561,1010,'Ofloxacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(562,1010,'Ofloxacine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(563,1010,'Optochine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(564,1010,'Optochine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(565,1010,'Oxacilline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(566,1010,'gentamicine (fortememt charge)',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(567,1010,'Oxytétracycline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(568,1010,'Oxytétracycline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(569,1010,'Péfloxacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(570,1010,'Péfloxacine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(571,1010,'Pénicilline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(572,1010,'Pénicilline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(573,1010,'Pipéracilline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(574,1010,'Pipéracilline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(575,1010,'Pipéracilline/tazobactam',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(576,1010,'Pipéracilline/tazobactam',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(577,1010,'Pristinamycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(578,1010,'Pristinamycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(579,1010,'Quinupristine-dalfopristine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(580,1010,'Quinupristine-dalfopristine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(581,1010,'Rifampicine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(582,1010,'Sparfloxacine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(583,1010,'Sparfloxacine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(584,1010,'Spectinomycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(585,1010,'Spectinomycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(586,1010,'Spiramycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(587,1010,'Streptomycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(588,1010,'Streptomycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(589,1010,'Sulbactam',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(590,1010,'Sulbactam',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(591,1010,'Teicoplanine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(592,1010,'Teicoplanine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(593,1010,'Télithromycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(594,1010,'Télithromycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(595,1010,'Tétracycline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(596,1010,'Tétracycline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(597,1010,'Ticarcilline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(598,1010,'Ticarcilline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(599,1010,'Ticarcilline/ac. Clavulanique',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(600,1010,'Ticarcilline/ac. Clavulanique',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(601,1010,'Tigécycline',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(602,1010,'Tigécycline',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(603,1010,'Tobramycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(604,1010,'Tobramycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(605,1010,'Triméthoprime',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(606,1010,'Triméthoprime',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(607,1010,'Triméthoprime/sulfaméthoxazole',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(608,1010,'Triméthoprime/sulfaméthoxazole',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(609,1010,'vancomycine',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(610,1010,'vancomycine',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(611,1010,'Quantification',NULL,NULL,NULL,NULL,NULL,614,NULL,NULL,NULL,NULL,NULL),(612,1010,'Culture',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(613,1010,'BAAR',NULL,NULL,NULL,NULL,NULL,614,NULL,NULL,NULL,NULL,NULL),(614,1010,'Espece',NULL,NULL,NULL,NULL,NULL,617,NULL,NULL,NULL,NULL,NULL),(616,1010,'Frottis',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(617,1010,'Goutte épaisse',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(618,1010,'Shistosomiase (Bilharziose) haematobium',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(619,1010,'Isionazide',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(620,1010,'Isionazide',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(621,1010,'Ethambutol',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(622,1010,'Ethambutol',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(623,1010,'Pyrazinamide',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(624,1010,'Pyrazinamide',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(625,1010,'Référé',NULL,NULL,NULL,NULL,NULL,231,NULL,NULL,NULL,NULL,NULL),(627,1010,'Résultat',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(628,1010,'IgM',NULL,NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(629,1010,'IgG',NULL,NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(632,1010,'Type de schistosomiase',NULL,NULL,NULL,NULL,NULL,642,NULL,NULL,NULL,NULL,NULL),(634,1010,'Type',NULL,NULL,NULL,NULL,NULL,644,NULL,NULL,NULL,NULL,NULL),(636,1010,'Bacilles à mobilité polaire',NULL,NULL,NULL,NULL,NULL,231,NULL,NULL,NULL,NULL,NULL),(637,1010,'BGN incurvés',NULL,NULL,NULL,NULL,NULL,231,NULL,NULL,NULL,NULL,NULL),(638,1010,'Culture',NULL,NULL,NULL,NULL,NULL,265,NULL,NULL,NULL,NULL,NULL),(639,1010,'V.cholerae O1',NULL,NULL,NULL,NULL,NULL,231,NULL,NULL,NULL,NULL,NULL),(640,1010,'V. cholerae O139',NULL,NULL,NULL,NULL,NULL,231,NULL,NULL,NULL,NULL,NULL),(641,1010,'Type de schistosomiase',NULL,NULL,NULL,NULL,NULL,643,NULL,NULL,NULL,NULL,NULL),(642,1010,'coloration à l\'encre de chine',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(643,1010,'Cryptococcus neoformans',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(644,1010,'Hématies (LCR)',NULL,241,NULL,NULL,NULL,228,NULL,NULL,NULL,2,NULL),(645,1010,'coloration à l\'encre de chine',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(646,1010,'Cryptococcus neoformans',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(647,1010,'Hématies (LCR)',NULL,1143,NULL,NULL,NULL,228,NULL,NULL,NULL,2,NULL),(648,1010,'espèce trypano',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(649,1010,'Diametre d\'inhibition',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(650,1010,'Glucose','PP',282,NULL,'1.6',NULL,228,235,'$_1*5.551',NULL,2,2),(651,1010,'glucose (LCR)','LCR',235,'2.50',NULL,NULL,228,NULL,NULL,NULL,2,NULL),(652,1010,'Glucose','urines',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(653,1010,'Acetone','urines ',NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(654,1010,'Waaler-Rose',NULL,293,NULL,'30',NULL,227,NULL,NULL,NULL,NULL,NULL),(655,1010,'TB GX',NULL,NULL,NULL,NULL,NULL,230,NULL,NULL,NULL,NULL,NULL),(656,1010,'RMP GX',NULL,NULL,NULL,NULL,NULL,1012,NULL,NULL,NULL,NULL,NULL),(657,1010,'Coliformes thermotolérants',NULL,1017,NULL,NULL,'0 CFU/100 ml',227,NULL,NULL,NULL,NULL,NULL),(658,1010,'Streptocoques fécaux',NULL,1017,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(659,1010,'Coliformes totaux',NULL,1017,NULL,NULL,'0 CFU pour 100 ml dans 95% des\néchantillons d\'eaux traitées',227,NULL,NULL,NULL,NULL,NULL),(660,1010,'LPA TB','Résultat de la détection des mycobactéries par LPA',NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(661,1010,'RMP LPA','Sensibilité à la rifampicine par le LPA',NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(662,1010,'INH LPA','Sensibilité à l\'INH par LPA',NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(663,1010,'Microscopie TB',NULL,NULL,NULL,NULL,NULL,1033,NULL,NULL,NULL,NULL,NULL),(664,1010,'Globules rouges ','sang',1143,'4.3','5.7',NULL,228,NULL,NULL,NULL,1,NULL),(665,1010,'VGM',NULL,244,'110','128',NULL,227,NULL,NULL,NULL,NULL,NULL),(666,1010,'TCMH',NULL,245,'36.0','40.0',NULL,229,NULL,NULL,'$_2*10/$_1',1,NULL),(667,1010,'CCMH',NULL,239,'30.0','34.0',NULL,228,NULL,NULL,NULL,1,NULL),(668,1010,'Polynucléaires neutrophiles',NULL,1144,'5.0','17.0',NULL,228,NULL,NULL,NULL,2,NULL),(669,1010,'Polynucléaires eosinophiles',NULL,1144,'0.1','0.6',NULL,228,NULL,NULL,NULL,2,NULL),(670,1010,'Polynucléaires basophiles',NULL,1144,'0.0','0.15',NULL,228,NULL,NULL,NULL,2,NULL),(671,1010,'Lymphocytes',NULL,1144,'2.5','8.5',NULL,228,NULL,NULL,NULL,2,NULL),(672,1010,'Monocytes',NULL,1144,'0.2','1.8',NULL,228,NULL,NULL,NULL,NULL,NULL),(673,1010,'Autres cellules',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(674,1010,'Hématocrite',NULL,239,'47.0','65.0',NULL,228,NULL,NULL,NULL,1,NULL),(675,1010,'Volume globulaire moyen (VGM)',NULL,244,'109','121',NULL,227,NULL,NULL,NULL,NULL,NULL),(676,1010,'Teneur corpusculaire moyen (TCMH)',NULL,245,'35.0','39.0',NULL,229,NULL,NULL,'$_2*10/$_1',1,NULL),(677,1010,'Concentration corpusculaire moyen (CCMH)',NULL,239,'30.0','34.0',NULL,228,NULL,NULL,NULL,1,NULL),(678,1010,'Autres cellulles ',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(679,1010,'TCMH',NULL,245,'33.0','37.0',NULL,228,NULL,NULL,NULL,1,NULL),(680,1010,'Teneur corpusculaire moyen (TCMH)',NULL,245,'31.0','35.0',NULL,228,NULL,NULL,NULL,1,NULL),(681,1010,'Globules rouges',NULL,1143,'3.7','4.8',NULL,228,NULL,NULL,NULL,1,NULL),(682,1010,'Plaquettes',NULL,1144,'160','350',NULL,228,NULL,NULL,NULL,NULL,NULL),(683,1010,'Penicilline G',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(684,1010,'Amoxicilline/ Ac .Clavulanique',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(685,1010,'Acide  nalidixique',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(686,1010,'Pencilline G',NULL,NULL,NULL,NULL,NULL,1134,NULL,NULL,NULL,NULL,NULL),(687,1010,'Methode de diffusion de disque',NULL,NULL,NULL,NULL,NULL,265,NULL,NULL,NULL,NULL,NULL),(688,1010,'CMI (E test)',NULL,NULL,NULL,NULL,NULL,265,NULL,NULL,NULL,NULL,NULL),(689,1010,'CMI Cefotaxime',NULL,280,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(690,1010,'CMI Cefixime',NULL,280,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(691,1010,'CMI Penicilline G',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(692,1010,'CMI Amoxicilline',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(693,1010,'Cotrimoxazole',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(694,1010,'CMI Vancomycine',NULL,280,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(695,1010,'Protéines ','Liquide de ponction',282,NULL,NULL,'Transudat : < 30g/l\nExsudat: > 30g/l',227,NULL,NULL,NULL,NULL,NULL),(696,1010,'Recheche de BAAR',NULL,NULL,NULL,NULL,NULL,614,NULL,NULL,NULL,NULL,NULL),(697,1010,'Dépistage syphilis (SD Bioline)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(698,1010,'Dépistage de la syphilis (SD Bioline)',NULL,NULL,NULL,NULL,NULL,1138,NULL,NULL,NULL,NULL,NULL),(699,1010,'aspect macroscopique ','crachat ',NULL,NULL,NULL,NULL,598,NULL,NULL,NULL,NULL,NULL),(700,1010,'leucocytes /champ',NULL,NULL,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(701,1010,'Cellules épithéliales /champ',NULL,NULL,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(702,1010,'Levures ',NULL,NULL,NULL,NULL,NULL,1133,NULL,NULL,NULL,NULL,NULL),(703,1010,'Numeration ',NULL,1145,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(704,1010,'Recherche de schizocytes',NULL,NULL,NULL,NULL,NULL,246,NULL,NULL,NULL,NULL,NULL),(705,1010,'Recherche de cellules anormales',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(706,1010,'Monocytes ',NULL,239,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(707,1010,'P.neutrophiles',NULL,239,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(708,1010,'P.eosinophiles',NULL,239,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(709,1010,'P.basophiles',NULL,239,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(710,1010,'Aspect du pus',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(711,1010,'Leucocytes/champ',NULL,NULL,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(712,1010,'Cellules epitheliales/champ',NULL,NULL,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(713,1010,'Culture',NULL,NULL,NULL,NULL,NULL,586,NULL,NULL,NULL,NULL,NULL),(714,1010,'Type de materiel',NULL,NULL,NULL,NULL,NULL,226,NULL,NULL,NULL,NULL,NULL),(715,100,'Résultat (filariose)',NULL,NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(716,100,'Résultat (fièvre jaune)',NULL,NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(717,100,'Résultat (poliomyélite)',NULL,NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(718,100,'IgM (rougeole)',NULL,NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(719,100,'IgG (rougeole)',NULL,NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(720,100,'IgM (rubéole)',NULL,NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(721,100,'IgG (rubéole)',NULL,NULL,NULL,NULL,NULL,635,NULL,NULL,NULL,NULL,NULL),(722,1000,'B-lactamase',NULL,NULL,NULL,NULL,NULL,600,NULL,NULL,NULL,NULL,NULL),(723,1000,'Diam. inhibition Acide fusidique',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(724,1000,'Diam. inhibition Acide nalidixique',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(725,1000,'Diam. inhibition Amikacine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(726,1000,'Diam. inhibition Amoxicilline',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(727,1000,'Diam. inhibition Amoxicilline/ac. Clavulanique',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(728,1000,'Diam. inhibition Ampicilline',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(729,1000,'Diam. inhibition Aztréonam',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(730,1000,'Diam. inhibition B-lactamase',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(731,1000,'Diam. inhibition Céfalotine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(732,1000,'Diam. inhibition Céfépime',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(733,1000,'Diam. inhibition Céfotaxime',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(734,1000,'Diam. inhibition Céfoxitine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(735,1000,'Diam. inhibition Cefsulodine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(736,1000,'Diam. inhibition Ceftazidime',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(737,1000,'Diam. inhibition Céftriaxone',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(738,1000,'Diam. inhibition Chloramphénicol',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(739,1000,'Diam. inhibition Ciprofloxacine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(740,1000,'Diam. inhibition Colistine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(741,1000,'Diam. inhibition Cotrimoxazole',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(742,1000,'Diam. inhibition Doxycycline',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(743,1000,'Diam. inhibition Erythromycine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(744,1000,'Diam. inhibition Fosfomycine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(745,1000,'Diam. inhibition Gentamicine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(746,1000,'Diam. inhibition Imipénème',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(747,1000,'Diam. inhibition Kanamycine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(748,1000,'Diam. inhibition Lincomycine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(749,1000,'Diam. inhibition Oxacilline',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(750,1000,'Diam. inhibition Nétilmicine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(751,1000,'Diam. inhibition Norfloxacine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(752,1000,'Diam. inhibition Péfloxacine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(753,1000,'Diam. inhibition Pénicilline',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(754,1000,'Diam. inhibition Pipéracilline',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(755,1000,'Diam. inhibition Pipéracilline/tazobactam',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(756,1000,'Diam. inhibition Pristinamycine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(757,1000,'Diam. inhibition Rifamycine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(758,1000,'Diam. inhibition Tétracycline',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(759,1000,'Diam. inhibition Ticarcilline',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(760,1000,'Diam. inhibition Ticarcilline/ac. Clavulanique',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(761,1000,'Diam. inhibition Tobramycine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(762,1000,'Diam. inhibition Vancomycine',NULL,240,NULL,NULL,NULL,227,NULL,NULL,NULL,NULL,NULL),(763,1000,'CMI Acide fusidique',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(764,1000,'CMI Acide nalidixique',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(765,1000,'CMI Amikacine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(766,1000,'CMI Amoxicilline',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(767,1000,'CMI Amoxicilline/ac. Clavulanique',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(768,1000,'CMI Ampicilline',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(769,1000,'CMI Aztréonam',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(770,1000,'CMI B-lactamase',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(771,1000,'CMI Céfalotine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(772,1000,'CMI Céfépime',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(773,1000,'CMI Céfotaxime',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(774,1000,'CMI Céfoxitine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(775,1000,'CMI Cefsulodine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(776,1000,'CMI Ceftazidime',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(777,1000,'CMI Céftriaxone',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(778,1000,'CMI Chloramphénicol',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(779,1000,'CMI Ciprofloxacine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(780,1000,'CMI Colistine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(781,1000,'CMI Cotrimoxazole',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(782,1000,'CMI Doxycycline',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(783,1000,'CMI Erythromycine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(784,1000,'CMI Fosfomycine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(785,1000,'CMI Gentamicine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(786,1000,'CMI Imipénème',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(787,1000,'CMI Kanamycine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(788,1000,'CMI Lincomycine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(789,1000,'CMI Oxacilline',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(790,1000,'CMI Nétilmicine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(791,1000,'CMI Norfloxacine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(792,1000,'CMI Péfloxacine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(793,1000,'CMI Pénicilline',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(794,1000,'CMI Pipéracilline',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(795,1000,'CMI Pipéracilline/tazobactam',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(796,1000,'CMI Pristinamycine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(797,1000,'CMI Rifamycine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(798,1000,'CMI Tétracycline',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(799,1000,'CMI Ticarcilline',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(800,1000,'CMI Ticarcilline/ac. Clavulanique',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(801,1000,'CMI Tobramycine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL),(802,1000,'CMI Vancomycine',NULL,NULL,NULL,NULL,NULL,228,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sigl_07_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_07_data_group`
--

DROP TABLE IF EXISTS `sigl_07_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_07_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_07_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=723 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_07_data_group`
--

LOCK TABLES `sigl_07_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_07_data_group` DISABLE KEYS */;
INSERT INTO `sigl_07_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000),(8,8,1000),(9,9,1000),(10,10,1000),(11,11,1000),(12,12,1000),(13,13,1000),(14,14,1000),(15,15,1000),(16,16,1000),(17,17,1000),(18,18,1000),(19,19,1000),(20,20,1000),(21,21,1000),(22,22,1000),(23,23,1000),(24,24,1000),(25,25,1000),(26,26,1000),(27,27,1000),(28,28,1000),(29,29,1000),(30,30,1000),(31,31,1000),(32,32,1000),(33,33,1000),(34,34,1000),(35,35,1000),(36,36,1000),(37,37,1000),(38,38,1000),(39,39,1000),(40,40,1000),(41,41,1000),(42,42,1000),(43,43,1000),(44,44,1000),(45,45,1000),(46,46,1000),(47,47,1000),(48,48,1000),(49,49,1000),(50,50,1000),(51,51,1000),(52,52,1000),(53,53,1000),(54,54,1000),(55,55,1000),(56,56,1000),(57,57,1000),(58,58,1000),(59,59,1000),(60,60,1000),(61,61,1000),(62,62,1000),(63,63,1000),(64,64,1000),(65,65,1000),(66,66,1000),(67,67,1000),(68,68,1000),(69,69,1000),(70,70,1000),(71,71,1000),(72,72,1000),(73,73,1000),(74,74,1000),(75,75,1000),(76,76,1000),(77,77,1000),(78,78,1000),(79,79,1000),(80,80,1000),(81,81,1000),(82,82,1000),(83,83,1000),(84,84,1000),(85,85,1000),(86,86,1000),(87,87,1000),(88,88,1000),(89,89,1000),(90,90,1000),(91,91,1000),(92,92,1000),(93,93,1000),(94,94,1000),(95,95,1000),(96,96,1000),(97,97,1000),(98,98,1000),(99,99,1000),(100,100,1000),(101,101,1000),(102,102,1000),(103,103,1000),(104,104,1000),(105,105,1000),(106,106,1000),(107,107,1000),(108,108,1000),(109,109,1000),(110,110,1000),(111,111,1000),(112,112,1000),(113,113,1000),(114,114,1000),(115,115,1000),(116,116,1000),(117,117,1000),(118,118,1000),(119,119,1000),(120,120,1000),(121,121,1000),(122,122,1000),(123,123,1000),(124,124,1000),(125,125,1000),(126,126,1000),(127,127,1000),(128,128,1000),(129,129,1000),(130,130,1000),(131,131,1000),(132,132,1000),(133,133,1000),(134,134,1000),(135,135,1000),(136,136,1000),(137,137,1000),(138,138,1000),(139,139,1000),(140,140,1000),(141,141,1000),(142,142,1000),(143,143,1000),(144,144,1000),(145,145,1000),(146,146,1000),(147,147,1000),(148,148,1000),(149,149,1000),(150,150,1000),(151,151,1000),(152,152,1000),(153,153,1000),(154,154,1000),(155,155,1000),(156,156,1000),(157,157,1000),(158,158,1000),(159,159,1000),(160,160,1000),(161,161,1000),(162,162,1000),(163,163,1000),(164,164,1000),(165,165,1000),(166,166,1000),(167,167,1000),(168,168,1000),(169,169,1000),(170,170,1000),(171,171,1000),(172,172,1000),(173,173,1000),(174,174,1000),(175,175,1000),(176,176,1000),(177,177,1000),(178,178,1000),(179,179,1000),(180,180,1000),(181,181,1000),(182,182,1000),(183,183,1000),(184,184,1000),(185,185,1000),(186,186,1000),(187,187,1000),(188,188,1000),(189,189,1000),(190,190,1000),(191,191,1000),(192,192,1000),(193,193,1000),(194,194,1000),(195,195,1000),(196,196,1000),(197,197,1000),(198,198,1000),(199,199,1000),(200,200,1000),(201,201,1000),(202,202,1000),(203,203,1000),(204,204,1000),(205,205,1000),(206,206,1000),(207,207,1000),(208,208,1000),(209,209,1000),(210,210,1000),(211,211,1000),(212,212,1000),(213,213,1000),(214,214,1000),(215,215,1000),(216,216,1000),(217,217,1000),(218,218,1000),(219,219,1000),(220,220,1000),(221,221,1000),(222,222,1000),(223,223,1000),(224,224,1000),(225,225,1000),(226,226,1000),(227,227,1000),(228,228,1000),(229,229,1000),(230,230,1000),(231,231,1000),(232,232,1000),(233,233,1000),(234,234,1000),(235,235,1000),(236,236,1000),(237,237,1000),(238,238,1000),(239,239,1000),(240,240,1000),(241,241,1000),(242,242,1000),(243,243,1000),(244,244,1000),(245,245,1000),(246,246,1000),(247,247,1000),(248,248,1000),(249,249,1000),(250,250,1000),(251,251,1000),(252,252,1000),(253,253,1000),(254,254,1000),(255,255,1000),(256,256,1000),(257,257,1000),(258,258,1000),(259,259,1000),(260,260,1000),(261,261,1000),(262,262,1000),(263,263,1000),(264,264,1000),(265,265,1000),(266,266,1000),(267,267,1000),(268,268,1000),(269,269,1000),(270,270,1000),(271,271,1000),(272,272,1000),(273,273,1000),(274,274,1000),(275,275,1000),(276,276,1000),(277,277,1000),(278,278,1000),(279,279,1000),(280,280,1000),(281,281,1000),(282,282,1000),(283,283,1000),(284,284,1000),(285,285,1000),(286,286,1000),(287,287,1000),(288,288,1000),(289,289,1000),(290,290,1000),(291,291,1000),(292,292,1000),(293,293,1000),(294,294,1000),(295,295,1000),(296,296,1000),(297,297,1000),(298,298,1000),(299,299,1000),(300,300,1000),(301,301,1000),(302,302,1000),(303,303,1000),(304,304,1000),(305,305,1000),(306,306,1000),(307,307,1000),(308,308,1000),(309,309,1000),(310,310,1000),(311,311,1000),(312,312,1000),(313,313,1000),(314,314,1000),(315,315,1000),(316,316,1000),(317,317,1000),(318,318,1000),(319,319,1000),(320,320,1000),(321,321,1000),(322,322,1000),(323,323,1000),(324,324,1000),(325,325,1000),(326,326,1000),(327,327,1000),(328,328,1000),(329,329,1000),(330,330,1000),(331,331,1000),(332,332,1000),(333,333,1000),(334,334,1000),(335,335,1000),(336,336,1000),(337,337,1000),(338,338,1000),(339,339,1000),(340,340,1000),(341,341,1000),(342,342,1000),(343,343,1000),(344,344,1000),(345,345,1000),(346,346,1000),(347,347,1000),(348,348,1000),(349,349,1000),(350,350,1000),(351,351,1000),(352,352,1000),(353,353,1000),(354,354,1000),(355,355,1000),(356,356,1000),(357,357,1000),(358,358,1000),(359,359,1000),(360,360,1000),(361,361,1000),(362,362,1000),(363,363,1000),(364,364,1000),(365,365,1000),(366,366,1000),(367,367,1000),(368,368,1000),(369,369,1000),(370,370,1000),(371,371,1000),(372,372,1000),(373,373,1000),(374,374,1000),(375,375,1000),(376,376,1000),(377,377,1000),(378,378,1000),(379,379,1000),(380,380,1000),(381,381,1000),(382,382,1000),(383,383,1000),(384,384,1000),(385,385,1000),(386,386,1000),(387,387,1000),(388,388,1000),(389,389,1000),(390,390,1000),(391,391,1000),(392,392,1000),(393,393,1000),(394,394,1000),(395,395,1000),(396,396,1000),(397,397,1000),(398,398,1000),(399,399,1000),(400,400,1000),(401,401,1000),(402,402,1000),(403,403,1000),(404,404,1000),(405,405,1000),(406,406,1000),(407,407,1000),(408,408,1000),(409,409,1000),(410,410,1000),(411,411,1000),(412,412,1000),(413,413,1000),(414,414,1000),(415,415,1000),(416,416,1000),(417,417,1000),(418,418,1000),(419,419,1000),(420,420,1000),(421,421,1000),(422,422,1000),(423,423,1000),(424,424,1000),(425,425,1000),(426,426,1000),(427,427,1000),(428,428,1000),(429,429,1000),(430,430,1000),(431,431,1000),(432,432,1000),(433,433,1000),(434,434,1000),(435,435,1000),(436,436,1000),(437,437,1000),(438,438,1000),(439,439,1000),(440,440,1000),(441,441,1000),(442,442,1000),(443,443,1000),(444,444,1000),(445,445,1000),(446,446,1000),(447,447,1000),(448,448,1000),(449,449,1000),(450,450,1000),(451,451,1000),(452,452,1000),(453,453,1000),(454,454,1000),(455,455,1000),(456,456,1000),(457,457,1000),(458,458,1000),(459,459,1000),(460,460,1000),(461,461,1000),(462,462,1000),(463,463,1000),(464,464,1000),(465,465,1000),(466,466,1000),(467,467,1000),(468,468,1000),(469,469,1000),(470,470,1000),(471,471,1000),(472,472,1000),(473,473,1000),(474,474,1000),(475,475,1000),(476,476,1000),(477,477,1000),(478,478,1000),(479,479,1000),(480,480,1000),(481,481,1000),(482,482,1000),(483,483,1000),(484,484,1000),(485,485,1000),(486,486,1000),(487,487,1000),(488,488,1000),(489,489,1000),(490,490,1000),(491,491,1000),(492,492,1000),(493,493,1000),(494,494,1000),(495,495,1000),(496,496,1000),(497,497,1000),(498,498,1000),(499,499,1000),(500,500,1000),(501,501,1000),(502,502,1000),(503,503,1000),(504,504,1000),(505,505,1000),(506,506,1000),(507,507,1000),(508,508,1000),(509,509,1000),(510,510,1000),(511,511,1000),(512,512,1000),(513,513,1000),(514,514,1000),(515,515,1000),(516,516,1000),(517,517,1000),(518,518,1000),(519,519,1000),(520,520,1000),(521,521,1000),(522,522,1000),(523,523,1000),(524,524,1000),(525,525,1000),(526,526,1000),(527,527,1000),(528,528,1000),(529,529,1000),(530,530,1000),(531,531,1000),(532,532,1000),(533,533,1000),(534,534,1000),(535,535,1000),(536,536,1000),(537,537,1000),(538,538,1000),(539,539,1000),(540,540,1000),(541,541,1000),(542,542,1000),(543,543,1000),(544,544,1000),(545,545,1000),(546,546,1000),(547,547,1000),(548,548,1000),(549,549,1000),(550,550,1000),(551,551,1000),(552,552,1000),(553,553,1000),(554,554,1000),(555,555,1000),(556,556,1000),(557,557,1000),(558,558,1000),(559,559,1000),(560,560,1000),(561,561,1000),(562,562,1000),(563,563,1000),(564,564,1000),(565,565,1000),(566,566,1000),(567,567,1000),(568,568,1000),(569,569,1000),(570,570,1000),(571,571,1000),(572,572,1000),(573,573,1000),(574,574,1000),(575,575,1000),(576,576,1000),(577,577,1000),(578,578,1000),(579,579,1000),(580,580,1000),(581,581,1000),(582,582,1000),(583,583,1000),(584,584,1000),(585,585,1000),(586,586,1000),(587,587,1000),(588,588,1000),(589,589,1000),(590,590,1000),(591,591,1000),(592,592,1000),(593,593,1000),(594,594,1000),(595,595,1000),(596,596,1000),(597,597,1000),(598,598,1000),(599,599,1000),(600,600,1000),(601,601,1000),(602,602,1000),(603,603,1000),(604,604,1000),(605,605,1000),(606,606,1000),(607,607,1000),(608,608,1000),(609,609,1000),(610,610,1000),(611,611,1000),(612,612,1000),(613,613,1000),(614,614,1000),(615,615,1000),(616,616,1000),(617,617,1000),(618,618,1000),(619,619,1000),(620,620,1000),(621,621,1000),(622,622,1000),(623,623,1000),(624,624,1000),(625,625,1000),(626,626,1000),(627,627,1000),(628,628,1000),(629,629,1000),(630,630,1000),(631,631,1000),(632,632,1000),(633,633,1000),(634,634,1000),(635,635,1000),(636,636,1000),(637,637,1000),(638,638,1000),(639,639,1000),(640,640,1000),(641,641,1000),(642,642,1000),(643,643,1000),(644,644,1000),(645,645,1000),(646,646,1000),(647,647,1000),(648,648,1000),(649,649,1000),(650,650,1000),(651,651,1000),(652,652,1000),(653,653,1000),(654,654,1000),(655,655,1000),(656,656,1000),(657,657,1000),(658,658,1000),(659,659,1000),(660,660,1000),(661,661,1000),(662,662,1000),(663,663,1000),(664,664,1000),(665,665,1000),(666,666,1000),(667,667,1000),(668,668,1000),(669,669,1000),(670,670,1000),(671,671,1000),(672,672,1000),(673,673,1000),(674,674,1000),(675,675,1000),(676,676,1000),(677,677,1000),(678,678,1000),(679,679,1000),(680,680,1000),(681,681,1000),(682,682,1000),(683,683,1000),(684,684,1000),(685,685,1000),(686,686,1000),(687,687,1000),(688,688,1000),(689,689,1000),(690,690,1000),(691,691,1000),(692,692,1000),(693,693,1000),(694,694,1000),(695,695,1000),(696,696,1000),(697,697,1000),(698,698,1000),(699,699,1000),(700,700,1000),(701,701,1000),(702,702,1000),(703,703,1000),(704,704,1000),(705,705,1000),(706,706,1000),(707,707,1000),(708,708,1000),(709,709,1000),(710,710,1000),(711,711,1000),(712,712,1000),(713,713,1000),(714,714,1000),(715,715,1000),(716,716,1000),(718,717,1000),(719,718,1000),(720,719,1000),(721,720,1000),(722,721,1000);
/*!40000 ALTER TABLE `sigl_07_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_07_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_07_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_07_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_07_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_07_data_group_mode`
--

LOCK TABLES `sigl_07_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_07_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_07_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_07_deleted`
--

DROP TABLE IF EXISTS `sigl_07_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_07_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `libelle` varchar(120) DEFAULT NULL,
  `description` varchar(120) DEFAULT NULL,
  `unite` int(10) unsigned DEFAULT NULL,
  `normal_min` varchar(20) DEFAULT NULL,
  `normal_max` varchar(20) DEFAULT NULL,
  `commentaire` text,
  `type_resultat` int(10) unsigned DEFAULT NULL,
  `unite2` int(10) unsigned DEFAULT NULL,
  `formule_unite2` varchar(120) DEFAULT NULL,
  `formule` varchar(120) DEFAULT NULL,
  `precision` int(1) unsigned DEFAULT NULL,
  `precision2` int(1) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_07_data_ibfk_1` (`id_owner`),
  KEY `sigl_07_data_ibfk_2` (`unite`),
  KEY `sigl_07_data_ibfk_3` (`type_resultat`),
  KEY `sigl_07_data_ibfk_4` (`unite2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_07_deleted`
--

LOCK TABLES `sigl_07_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_07_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_07_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_08_data`
--

DROP TABLE IF EXISTS `sigl_08_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_08_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `code` varchar(7) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nom` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `prenom` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ville` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `etablissement` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `specialite` int(10) unsigned DEFAULT NULL,
  `tel` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `titre` int(10) unsigned DEFAULT NULL,
  `initiale` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `service` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `adresse` text COLLATE utf8_unicode_ci,
  `mobile` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fax` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`),
  KEY `sigl_08_data_ibfk_2` (`specialite`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_08_data`
--

LOCK TABLES `sigl_08_data` WRITE;
/*!40000 ALTER TABLE `sigl_08_data` DISABLE KEYS */;
INSERT INTO `sigl_08_data` VALUES (1,100,'DEMO','PRESCR','Patrick','','',204,'','',260,'PP','','','','');
/*!40000 ALTER TABLE `sigl_08_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_08_data_group`
--

DROP TABLE IF EXISTS `sigl_08_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_08_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_08_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_08_data_group`
--

LOCK TABLES `sigl_08_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_08_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_08_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_08_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_08_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_08_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_08_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_08_data_group_mode`
--

LOCK TABLES `sigl_08_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_08_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_08_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_08_deleted`
--

DROP TABLE IF EXISTS `sigl_08_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_08_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `code` varchar(7) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nom` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `prenom` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ville` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `etablissement` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `specialite` int(10) unsigned DEFAULT NULL,
  `tel` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `titre` int(10) unsigned DEFAULT NULL,
  `initiale` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `service` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `adresse` text COLLATE utf8_unicode_ci,
  `mobile` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fax` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`),
  KEY `sigl_08_data_ibfk_2` (`specialite`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_08_deleted`
--

LOCK TABLES `sigl_08_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_08_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_08_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_09_data`
--

DROP TABLE IF EXISTS `sigl_09_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_09_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_analyse` int(10) unsigned NOT NULL,
  `ref_variable` int(10) unsigned NOT NULL,
  `valeur` varchar(120) DEFAULT NULL,
  `obligatoire` int(11) DEFAULT '4',
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `Unique` (`id_analyse`,`ref_variable`),
  KEY `sigl_09_data_ibfk_1` (`id_owner`),
  KEY `sigl_09_data_ibfk_2` (`id_analyse`),
  KEY `sigl_09_data_ibfk_3` (`ref_variable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_09_data`
--

LOCK TABLES `sigl_09_data` WRITE;
/*!40000 ALTER TABLE `sigl_09_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_09_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_09_data_group`
--

DROP TABLE IF EXISTS `sigl_09_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_09_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_09_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_09_data_group`
--

LOCK TABLES `sigl_09_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_09_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_09_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_09_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_09_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_09_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_09_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_09_data_group_mode`
--

LOCK TABLES `sigl_09_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_09_data_group_mode` DISABLE KEYS */;
INSERT INTO `sigl_09_data_group_mode` VALUES (1,138,56,NULL),(2,139,56,NULL),(3,140,56,NULL),(4,141,56,NULL),(5,142,56,NULL),(6,143,56,NULL),(7,144,56,NULL),(8,145,56,NULL),(9,146,56,NULL),(10,147,56,NULL),(11,148,56,NULL);
/*!40000 ALTER TABLE `sigl_09_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_09_deleted`
--

DROP TABLE IF EXISTS `sigl_09_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_09_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_analyse` int(10) unsigned NOT NULL,
  `ref_variable` int(10) unsigned NOT NULL,
  `valeur` varchar(120) DEFAULT NULL,
  `obligatoire` int(11) DEFAULT '4',
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `Unique` (`id_analyse`,`ref_variable`),
  KEY `sigl_09_data_ibfk_1` (`id_owner`),
  KEY `sigl_09_data_ibfk_2` (`id_analyse`),
  KEY `sigl_09_data_ibfk_3` (`ref_variable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_09_deleted`
--

LOCK TABLES `sigl_09_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_09_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_09_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_10_data`
--

DROP TABLE IF EXISTS `sigl_10_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_10_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_resultat` int(10) unsigned DEFAULT NULL,
  `date_validation` datetime NOT NULL,
  `utilisateur` int(10) unsigned NOT NULL,
  `valeur` varchar(120) DEFAULT NULL,
  `type_validation` int(10) unsigned DEFAULT NULL,
  `commentaire` text,
  `motif_annulation` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `FK_sigl_10_data_1` (`id_owner`),
  KEY `FK_sigl_10_data_2` (`id_resultat`),
  KEY `FK_sigl_10_data_4` (`type_validation`),
  KEY `FK_sigl_10_data_3` (`utilisateur`),
  KEY `FK_sigl_10_data_5` (`motif_annulation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_10_data`
--

LOCK TABLES `sigl_10_data` WRITE;
/*!40000 ALTER TABLE `sigl_10_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_10_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_10_data_group`
--

DROP TABLE IF EXISTS `sigl_10_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_10_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_10_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_10_data_group`
--

LOCK TABLES `sigl_10_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_10_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_10_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_10_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_10_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_10_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_10_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_10_data_group_mode`
--

LOCK TABLES `sigl_10_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_10_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_10_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_10_delete`
--

DROP TABLE IF EXISTS `sigl_10_delete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_10_delete` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_resultat` int(11) NOT NULL,
  `date_validation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `utilisateur` int(11) NOT NULL,
  `valeur` varchar(120) DEFAULT NULL,
  `type_validation` int(11) NOT NULL,
  `commentaire` text,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_10_delete`
--

LOCK TABLES `sigl_10_delete` WRITE;
/*!40000 ALTER TABLE `sigl_10_delete` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_10_delete` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_10_deleted`
--

DROP TABLE IF EXISTS `sigl_10_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_10_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_resultat` int(10) unsigned DEFAULT NULL,
  `date_validation` datetime NOT NULL,
  `utilisateur` int(10) unsigned NOT NULL,
  `valeur` varchar(120) DEFAULT NULL,
  `type_validation` int(10) unsigned DEFAULT NULL,
  `commentaire` text,
  `motif_annulation` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `FK_sigl_10_data_1` (`id_owner`),
  KEY `FK_sigl_10_data_2` (`id_resultat`),
  KEY `FK_sigl_10_data_4` (`type_validation`),
  KEY `FK_sigl_10_data_3` (`utilisateur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_10_deleted`
--

LOCK TABLES `sigl_10_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_10_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_10_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_11_data`
--

DROP TABLE IF EXISTS `sigl_11_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_11_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_dos` int(10) unsigned NOT NULL,
  `file` varchar(36) NOT NULL,
  `file_type` int(10) unsigned DEFAULT NULL,
  `doc_type` int(10) unsigned DEFAULT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `Unique` (`file`),
  KEY `sigl_11_data_ibfk_1` (`id_owner`),
  KEY `sigl_11_data_ibfk_2` (`id_dos`),
  KEY `sigl_11_data_ibfk_3` (`file_type`),
  KEY `sigl_11_data_ibfk_4` (`doc_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_11_data`
--

LOCK TABLES `sigl_11_data` WRITE;
/*!40000 ALTER TABLE `sigl_11_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_11_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_11_data_group`
--

DROP TABLE IF EXISTS `sigl_11_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_11_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_11_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_11_data_group`
--

LOCK TABLES `sigl_11_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_11_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_11_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_11_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_11_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_11_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_11_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_11_data_group_mode`
--

LOCK TABLES `sigl_11_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_11_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_11_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_11_deleted`
--

DROP TABLE IF EXISTS `sigl_11_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_11_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_dos` int(10) unsigned NOT NULL,
  `file` varchar(36) NOT NULL,
  `file_type` int(10) unsigned DEFAULT NULL,
  `doc_type` int(10) unsigned DEFAULT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `Unique` (`file`),
  KEY `sigl_11_data_ibfk_1` (`id_owner`),
  KEY `sigl_11_data_ibfk_2` (`id_dos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_11_deleted`
--

LOCK TABLES `sigl_11_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_11_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_11_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_12_data`
--

DROP TABLE IF EXISTS `sigl_12_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_12_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_patient` int(10) unsigned NOT NULL,
  `lot` varchar(40) NOT NULL,
  `type` int(10) unsigned NOT NULL,
  `date_expiration` date NOT NULL,
  `producteur` varchar(40) DEFAULT NULL,
  `produit_pathologique` int(10) unsigned NOT NULL,
  `ref_analyse` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data`),
  KEY `FK_sigl_12_data_1` (`id_owner`),
  KEY `FK_sigl_12_data_2` (`id_patient`),
  KEY `FK_sigl_12_data_3` (`type`),
  KEY `FK_sigl_12_data_4` (`produit_pathologique`),
  KEY `FK_sigl_12_data_5` (`ref_analyse`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_12_data`
--

LOCK TABLES `sigl_12_data` WRITE;
/*!40000 ALTER TABLE `sigl_12_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_12_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_12_data_group`
--

DROP TABLE IF EXISTS `sigl_12_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_12_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_12_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_12_data_group`
--

LOCK TABLES `sigl_12_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_12_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_12_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_12_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_12_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_12_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_12_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_12_data_group_mode`
--

LOCK TABLES `sigl_12_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_12_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_12_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_12_deleted`
--

DROP TABLE IF EXISTS `sigl_12_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_12_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_patient` int(10) unsigned NOT NULL,
  `lot` varchar(40) NOT NULL,
  `type` int(10) unsigned NOT NULL,
  `date_expiration` date NOT NULL,
  `producteur` varchar(40) DEFAULT NULL,
  `produit_pathologique` int(10) unsigned NOT NULL,
  `ref_analyse` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_12_deleted`
--

LOCK TABLES `sigl_12_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_12_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_12_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_13_data`
--

DROP TABLE IF EXISTS `sigl_13_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_13_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_controle_qualite` int(10) unsigned NOT NULL,
  `date` date NOT NULL,
  `id_dossier` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `FK_sigl_13_data_1` (`id_owner`),
  KEY `FK_sigl_13_data_2` (`id_controle_qualite`),
  KEY `FK_sigl_13_data_3` (`id_dossier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_13_data`
--

LOCK TABLES `sigl_13_data` WRITE;
/*!40000 ALTER TABLE `sigl_13_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_13_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_13_data_group`
--

DROP TABLE IF EXISTS `sigl_13_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_13_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_13_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_13_data_group`
--

LOCK TABLES `sigl_13_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_13_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_13_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_13_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_13_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_13_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_13_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_13_data_group_mode`
--

LOCK TABLES `sigl_13_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_13_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_13_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_13_deleted`
--

DROP TABLE IF EXISTS `sigl_13_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_13_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_controle_qualite` int(10) unsigned NOT NULL,
  `date` date NOT NULL,
  `id_dossier` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_13_deleted`
--

LOCK TABLES `sigl_13_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_13_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_13_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_14_data`
--

DROP TABLE IF EXISTS `sigl_14_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_14_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL DEFAULT '100',
  `surveillance` varchar(150) DEFAULT NULL,
  `nature_prel` int(10) unsigned DEFAULT NULL,
  `dhis2_tab` varchar(25) DEFAULT NULL,
  `dhis2_tab_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_14_data_owner` (`id_owner`),
  KEY `sigl_14_data_nature_prel_dico` (`nature_prel`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_14_data`
--

LOCK TABLES `sigl_14_data` WRITE;
/*!40000 ALTER TABLE `sigl_14_data` DISABLE KEYS */;
INSERT INTO `sigl_14_data` VALUES (113,100,'Méningite',99,'Méningite',1),(114,100,'Choléra',141,'Choléra',2),(115,100,'Shigelloses',141,'Shigelloses',3),(116,100,'Salmonelloses',141,NULL,NULL),(117,100,'Paludisme',138,'Paludisme',5),(118,100,'Tuberculose',163,'Tuberculose',4),(119,100,'VIH/Sida (Test rapide)',138,'VIH/Sida',8),(120,100,'VIH/Sida (Automate)',138,NULL,NULL),(121,100,'VIH/Sida (CD4 - CD8)',138,NULL,NULL),(122,100,'IST (prel. sang)',138,'IST',6),(123,100,'IST (prel. vaginal))',162,NULL,NULL),(124,100,'IST (prel uretral)',152,NULL,NULL),(125,100,'Fièvre jaune',138,NULL,NULL),(126,100,'Rougeole',138,NULL,NULL),(127,100,'Rubéole',138,NULL,NULL),(128,100,'Toxoplasmose',138,NULL,NULL),(129,100,'Poliomyélite',141,NULL,NULL),(130,100,'Schistosomiase (prel. urine)',153,NULL,NULL),(131,100,'Schistosomiase (prel. selles)',141,NULL,NULL),(132,100,'Filariose',138,NULL,NULL),(133,100,NULL,NULL,'Schistosomiases',7);
/*!40000 ALTER TABLE `sigl_14_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_14_data_group`
--

DROP TABLE IF EXISTS `sigl_14_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_14_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_14_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_14_data_group`
--

LOCK TABLES `sigl_14_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_14_data_group` DISABLE KEYS */;
INSERT INTO `sigl_14_data_group` VALUES (113,113,1000),(114,114,1000),(115,115,1000),(116,116,1000),(117,117,1000),(118,118,1000),(119,119,1000),(120,120,1000),(121,121,1000),(122,122,1000),(123,123,1000),(124,124,1000),(125,125,1000),(126,126,1000),(127,127,1000),(128,128,1000),(129,129,1000),(130,130,1000),(131,131,1000),(132,132,1000),(133,133,1000);
/*!40000 ALTER TABLE `sigl_14_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_14_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_14_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_14_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_14_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_14_data_group_mode`
--

LOCK TABLES `sigl_14_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_14_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_14_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_14_deleted`
--

DROP TABLE IF EXISTS `sigl_14_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_14_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL DEFAULT '100',
  `surveillance` varchar(150) NOT NULL,
  `nature_prel` int(10) unsigned DEFAULT NULL,
  `dhis2_tab` varchar(25) DEFAULT NULL,
  `dhis2_tab_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_14_data_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_14_deleted`
--

LOCK TABLES `sigl_14_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_14_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_14_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_15_data`
--

DROP TABLE IF EXISTS `sigl_15_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_15_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL DEFAULT '100',
  `nom_amont` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `formule` text COLLATE utf8_unicode_ci,
  `id_surveillance` int(10) unsigned DEFAULT NULL,
  `libelle_ind` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `methode_calcul` text COLLATE utf8_unicode_ci,
  `label_dhis2` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `label_exp_dhis2` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dhis2_pos` int(11) DEFAULT NULL,
  `id_surveillance_dhis2` int(10) unsigned DEFAULT NULL,
  `nature_prel` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_15_data_owner` (`id_owner`),
  KEY `sigl_15_data_id_surveillance_surveillance` (`id_surveillance`)
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_15_data`
--

LOCK TABLES `sigl_15_data` WRITE;
/*!40000 ALTER TABLE `sigl_15_data` DISABLE KEYS */;
INSERT INTO `sigl_15_data` VALUES (1,100,'Coloration de Gram','$_333 = 495',113,'Absence de germe',NULL,NULL,NULL,NULL,NULL,99),(2,100,'Coloration de Gram','$_333 = [gram.21]',113,'DGN',NULL,'Diplocoque Gram négatif','Diplocoque a Gram (-)',10,113,99),(3,100,'Coloration de Gram','$_333 = [gram.20]',113,'DGP',NULL,'Diplocoque Gram positif','Diplocoque a Gram (+)',11,113,99),(4,100,'Coloration de Gram','$_333 = [gram.2]',113,'BGN',NULL,'Bacilles à Gram négatif','Bacilles a Gram (-) polymorphes',12,113,99),(5,100,'Coloration de Gram','$_333 NOT IN (495,496,514,515)',113,'Autre',NULL,NULL,NULL,NULL,NULL,99),(6,100,'Culture','$_344 NOT IN ([bacterie.7], [bacterie.8], [bacterie.9], [bacterie.10], [bacterie.11], [bacterie.12], [bacterie.13], [bacterie.29], [bacterie.14], [bacterie.15])',113,'Négative',NULL,'Total -','Total (-) (Meningite)',2,113,99),(7,100,'Culture','$_344 IN ([bacterie.7], [bacterie.8], [bacterie.9], [bacterie.10], [bacterie.11], [bacterie.12], [bacterie.13], [bacterie.29], [bacterie.14], [bacterie.15])',113,'Positive',NULL,'Total +','Total (+) (Meningite)',3,113,99),(8,100,'Culture','$_344 = [bacterie.29]',113,'Pneumo',NULL,'Pneumocoque','Pneumocoque',8,113,99),(9,100,'Culture','$_344 = [bacterie.7]',113,'Meningo',NULL,NULL,NULL,NULL,NULL,99),(10,100,'Culture','$_344 = [bacterie.8]',113,'Meningo A',NULL,'Meningo A','Meningo A',4,113,99),(11,100,'Culture','$_344 = [bacterie.9]',113,'Meningo B',NULL,'Meningo B','Meningo B',5,113,99),(12,100,'Culture','$_344 = [bacterie.10]',113,'Meningo C',NULL,'Meningo C','Meningo C',6,113,99),(13,100,'Culture','$_344 = [bacterie.12]',113,'Meningo X',NULL,NULL,NULL,NULL,NULL,99),(14,100,'Culture','$_344 = [bacterie.13]',113,'Meningo Y',NULL,NULL,NULL,NULL,NULL,99),(15,100,'Culture','$_344 = [bacterie.11]',113,'Meningo W135',NULL,'Meningo W135','Meningo W135',7,113,99),(16,100,'Culture','$_344 = [bacterie.15]',113,'HIB',NULL,'Hib','Hib',9,113,99),(17,100,'PCR','$_384 = [posneg.-]',113,'Négatif',NULL,NULL,NULL,NULL,NULL,99),(18,100,'PCR','$_384 = [posneg.+]',113,'Positif',NULL,NULL,NULL,NULL,NULL,99),(19,100,'Latex','$_387 = [latex.11]',113,'Négative',NULL,NULL,NULL,NULL,NULL,99),(20,100,'Latex','$_387 != [latex.11]',113,'Positive',NULL,NULL,NULL,NULL,NULL,99),(21,100,'Latex','$_387 = [latex.12]',113,'Pneumo',NULL,NULL,NULL,NULL,NULL,99),(22,100,'Latex','$_387 = [latex.5]',113,'Meningo A',NULL,NULL,NULL,NULL,NULL,99),(23,100,'Latex','$_387 = [latex.6]',113,'Meningo B',NULL,NULL,NULL,NULL,NULL,99),(24,100,'Latex','$_387 = [latex.7]',113,'Meningo C',NULL,NULL,NULL,NULL,NULL,99),(25,100,'Latex','$_387 = [latex.8]',113,'Meningo X',NULL,NULL,NULL,NULL,NULL,99),(26,100,'Latex','$_387 = [latex.9]',113,'Meningo Y',NULL,NULL,NULL,NULL,NULL,99),(27,100,'Latex','$_387 = [latex.10]',113,'Meningo W135',NULL,NULL,NULL,NULL,NULL,99),(28,100,'Latex','$_387 = [latex.13]',113,'HIB',NULL,NULL,NULL,NULL,NULL,99),(29,100,'Examen direct','$_636 = [yorn.1]',114,'Bacilles à mobilité polaire',NULL,NULL,NULL,NULL,NULL,141),(30,100,'Examen direct','$_637 = [yorn.1]',114,'BGN incurvés',NULL,NULL,NULL,NULL,NULL,141),(31,100,'Culture','$_639 != [yorn.1] AND $_640 != [yorn.1]',114,'Négatif',NULL,NULL,NULL,NULL,NULL,141),(32,100,'Culture','$_639 = [yorn.1] OR $_640 = [yorn.1]',114,'Positif',NULL,'Total (+) à vibrio','Total (+) a vibro',4,114,141),(33,100,'Culture','$_639 = [yorn.1]',114,'V. cholerae O1',NULL,'V.Cholera01','V.Cholera01',5,114,141),(34,100,'Culture','$_640 = [yorn.1]',114,'V. cholerae O139',NULL,'V.Cholera0139','V.Cholera0139',6,114,141),(35,100,'Culture','$_344 NOT IN ([bacterie.25], [bacterie.26], [bacterie.27], [bacterie.28])',115,'Négatifs',NULL,NULL,NULL,NULL,NULL,141),(36,100,'Culture','$_344 IN ([bacterie.25], [bacterie.26], [bacterie.27], [bacterie.28])',115,'Positifs',NULL,'Total (+) à shigella ','Total (+) a shigella',4,115,141),(37,100,'Culture','$_344 = [bacterie.25]',115,'S. dysenteria',NULL,'Shigella dysenteriae','Shigella dysenteriae',5,115,141),(38,100,'Culture','$_344 IN ([bacterie.26], [bacterie.27], [bacterie.28])',115,'Autres shigelles',NULL,'Autres shigelles','Autres shigelles',6,115,141),(39,100,'Culture','$_344 IN ([bacterie.1],[bacterie.2])',116,'Négatifs',NULL,NULL,NULL,NULL,NULL,141),(40,100,'Culture','$_344 NOT IN ([bacterie.1],[bacterie.2])',116,'Positifs',NULL,NULL,NULL,NULL,NULL,141),(41,100,'Culture','$_344 = [bacterie.21]',116,'S. Typhi',NULL,NULL,NULL,NULL,NULL,141),(42,100,'Culture','$_344 IN ([bacterie.22],[bacterie.23],[bacterie.24])',116,'S. para Typhi ',NULL,NULL,NULL,NULL,NULL,141),(43,100,'Culture','$_344 = [bacterie.48]',116,'Autres salmonelleoses',NULL,NULL,NULL,NULL,NULL,141),(44,100,'GE/frottis','$_316 != [posnegind.Positif] AND $_616 != [posnegind.Positif] AND $_617 != [posnegind.Positif]',117,'Négatifs',NULL,'Total (-)','Total (-) (Paludisme)',2,117,138),(45,100,'GE/frottis','$_316 = [posnegind.Positif] OR $_616 = [posnegind.Positif] OR $_617 = [posnegind.Positif]',117,'Positifs',NULL,'Total (+)','Total (+) (Paludisme)',3,117,138),(46,100,'GE/frottis','$_614 = [especepalu.pl_falc]',117,'P. falciparum',NULL,'Pl. falciparum','Pl. falciparum',4,117,138),(47,100,'GE/frottis','$_614 = [especepalu.autres]',117,'Autres espèces',NULL,'Autres espèces','Autres especes',5,117,138),(48,100,'TDR','$_252 = [posnegind.Négatif]',117,'Négatifs',NULL,NULL,NULL,NULL,NULL,138),(49,100,'TDR','$_252 = [posnegind.Positif]',117,'Positifs',NULL,NULL,NULL,NULL,NULL,138),(50,100,'TDR','$_253 = [especepalu.pl_falc]',117,'P. falciparum',NULL,NULL,NULL,NULL,NULL,138),(51,100,'TDR','$_253 != [especepalu.pl_falc]',117,'Autres espèces',NULL,NULL,NULL,NULL,NULL,138),(52,100,'Recherche de BAAR ','$_611 = [baar.-]',118,'Négatifs',NULL,'Total (-)','Total (-) (Tuberculose)',2,118,50),(53,100,'Recherche de BAAR ','$_611 IN ([baar.+], [baar.++], [baar.+++])',118,'Positifs (1-9 BAAR)',NULL,'Total (+)','Total (+) (Tuberculose)',3,118,50),(54,100,'Recherche de BAAR ','$_611 = [baar.+]',118,'Positifs (+)',NULL,'Total TPM +','Total TPM +',5,118,50),(55,100,'Recherche de BAAR ','$_611 = [baar.++]',118,'Positifs (++)',NULL,'Total TPM ++','Total TPM ++',6,118,50),(56,100,'Recherche de BAAR ','$_611 = [baar.+++]',118,'Positifs (+++)',NULL,'Total TPM +++','Total TPM +++',7,118,50),(57,100,'Culture','$_612 = [posneg.-]',118,'Négatifs',NULL,NULL,NULL,NULL,NULL,50),(58,100,'Culture','$_612 = [posneg.+]',118,'Positifs',NULL,NULL,NULL,NULL,NULL,50),(59,100,'Diagnostic sérologique','$_278 = [vih.neg]',119,'Négatifs',NULL,'Total (-)','Total (-) (VIH)',2,119,138),(60,100,'Diagnostic sérologique','$_278 IN ([vih.vih1], [vih.vih2], [vih.vih1-vih2])',119,'Total positifs',NULL,'Total (+)','Total (+) (VIH)',3,119,138),(61,100,'Diagnostic sérologique','$_278 = [vih.vih1]',119,'VIH1',NULL,'VIH1','VIH1',5,119,138),(62,100,'Diagnostic sérologique','$_278 = [vih.vih2]',119,'VIH 2',NULL,'VIH2','VIH2',6,119,138),(63,100,'Diagnostic sérologique','$_278 = [vih.vih1-vih2]',119,'VIH 1&2',NULL,'VIH 1/2','VIH 1/2',7,119,138),(64,100,'Diagnostic sérologique','$_278 = [vih.ind]',119,'Indéterminés',NULL,NULL,NULL,NULL,NULL,138),(65,100,'Diagnostic précoce (PCR)','$_279 = [vih.neg] AND $_280 = [vih.neg]',120,'Négatifs',NULL,NULL,NULL,NULL,NULL,138),(66,100,'Diagnostic précoce (PCR)','$_279 NOT IN ([vih.neg], [vih.ind]) OR $_280 NOT IN ([vih.neg], [vih.ind])',120,'Positifs',NULL,NULL,NULL,NULL,NULL,138),(67,100,'Suivi biologique','$_179 < 500',121,'Total CD4',NULL,NULL,NULL,NULL,NULL,138),(68,100,'Suivi biologique','$_182 > 1000',121,'Total CV',NULL,NULL,NULL,NULL,NULL,138),(69,100,'RPR','$_229 = [posneg.+]',122,'Total RPR+',NULL,NULL,NULL,NULL,NULL,138),(70,100,'TPHA','$_231 = [posneg.+]',122,'Total TPHA +',NULL,NULL,NULL,NULL,NULL,138),(71,100,'RPR et TPHA','$_229 = [posneg.+] AND $_231 = [posneg.+]',122,'Total RPR&TPHA +',NULL,'Sérol.Syphilis (+) (RPR + TPHA)','Serol.Syphilis (+) (RPR + TPHA)',22,122,138),(72,100,'Chlamydiae','N/A',122,'Total Chlamydiae +',NULL,'Sérol Chlamydia (+)','Serol Chlamydia (+)',23,122,138),(73,100,'Examen direct','$_353  = [absent.present]',123,'Diplocoq. à Gram',NULL,'Diplocoq. à Gram (-) (Prélévement Vaginal)','Diplocoq. a Gram (-) (Prelevement Vaginal)',5,122,162),(74,100,'Examen direct','$_347  = [yorn.1]',123,'Trichomo. Vaginalis',NULL,'Trichomo. vaginalis (Prélèvement Vaginal) ','Trichomo. vaginalis (Prelevement Vaginal)',6,122,162),(75,100,'Examen direct','$_212  = [absent.present]',123,'C. trachomatis direct',NULL,'Chlamydia trachomatis direct (Prélèvement Vaginal) ','Chlamydia trachomatis direct (Prelevement Vaginal)',9,122,162),(76,100,'Examen direct','$_356  IN ([nombre.3], [nombre.4], [nombre.5])',123,'Levures',NULL,'Levures (Prélèvement Vaginal) ','Levures (Prelevement Vaginal)',8,122,162),(77,100,'Culture','$_361 = [bacterie.n_gono]',123,'Neisseria gonorrhoeae',NULL,'Neisseria gonorrhoeae (Prélèvement Vaginal) ','Neisseria gonorrhoeae (Prelevement Vaginal)',4,122,162),(78,100,'Culture','$_361 = [bacterie.33]',123,'C. albicans ',NULL,'Candida albicans (Prelevement Vaginal) ','Candida albicans (Prelevement Vaginal)',7,122,162),(79,100,'Culture','N/A',123,'Autres levures',NULL,NULL,NULL,NULL,NULL,NULL),(80,100,'Examen direct','$_353  = [absent.present]',124,'DGN',NULL,'Diplocoq. à Gram (-) (Prélèvement Urétral)','Diplocoq. a Gram (-) (Prelevement Uretral)',14,122,152),(81,100,'Examen direct','$_356  IN ([nombre.3], [nombre.4], [nombre.5])',124,'Levures',NULL,'Levures (Prélèvement Urétral)','Levures (Prelevement Uretral)',17,122,152),(82,100,'Culture','$_344 = [bacterie.n_gono]',124,'Neisseria gonorrhoeae',NULL,'Neisseria gonorrhoeae (Prélèvement Urétral) ','Neisseria gonorrhoeae (Prelevement Uretral)',13,122,152),(83,100,'Culture','$_344 = [bacterie.33]',124,'C. albicans ',NULL,'Candida albicans (Prélèvement Urétral)','Chlamydia trachomatis direct (Prelevement Uretral)',16,122,152),(84,100,'Culture','N/A',124,'Autres levures',NULL,NULL,NULL,NULL,NULL,NULL),(85,100,NULL,'$_625  = [yorn.1]',125,'Total referés',NULL,NULL,NULL,NULL,NULL,138),(86,100,NULL,'$_716  = [posnegind.Positif]',125,'Total Positif',NULL,NULL,NULL,NULL,NULL,138),(87,100,NULL,'$_718  = [posnegind.Positif]',126,'Positif IgM',NULL,NULL,NULL,NULL,NULL,138),(88,100,NULL,'$_719  = [posnegind.Positif]',126,'Positif IgG',NULL,NULL,NULL,NULL,NULL,138),(89,100,NULL,'$_718  = [posnegind.Négatif] AND $_719  = [posnegind.Négatif]',126,'Négatifs',NULL,NULL,NULL,NULL,NULL,138),(90,100,NULL,'$_718  = [posnegind.Indétermin] AND $_719  = [posnegind.Indétermin]',126,'Total Indéterminés',NULL,NULL,NULL,NULL,NULL,138),(91,100,NULL,'$_720  = [posnegind.Positif]',127,'Positif IgM',NULL,NULL,NULL,NULL,NULL,138),(92,100,NULL,'$_721  = [posnegind.Positif]',127,'Positif IgG',NULL,NULL,NULL,NULL,NULL,138),(93,100,NULL,'$_720  = [posnegind.Négatif] AND $_721  = [posnegind.Négatif]',127,'Négatifs',NULL,NULL,NULL,NULL,NULL,138),(94,100,NULL,'$_720  = [posnegind.Indétermin] AND $_721  = [posnegind.Indétermin]',127,'Total Indéterminés',NULL,NULL,NULL,NULL,NULL,138),(95,100,NULL,'$_628  = [posnegind.Positif]',128,'Positif IgM',NULL,NULL,NULL,NULL,NULL,138),(96,100,NULL,'$_629  = [posnegind.Positif]',128,'Positif IgG',NULL,NULL,NULL,NULL,NULL,138),(97,100,NULL,'$_628  = [posnegind.Négatif] AND $_629  = [posnegind.Négatif]',128,'Négatifs',NULL,NULL,NULL,NULL,NULL,138),(98,100,NULL,'$_628  = [posnegind.Indétermin] AND $_629  = [posnegind.Indétermin]',128,'Total Indéterminés',NULL,NULL,NULL,NULL,NULL,138),(99,100,NULL,'$_625 = [yorn.1]',129,'Total referés',NULL,NULL,NULL,NULL,NULL,153),(100,100,NULL,'$_717 = [posnegind.Positif]',129,'Total Positif',NULL,NULL,NULL,NULL,NULL,153),(101,100,NULL,'$_627 = [posnegind.Négatif]',130,'Négatifs',NULL,'Total (-) urines','Total (-) urines (Shistosomiases)',6,133,153),(102,100,NULL,'$_627 = [posnegind.Positif]',130,'Positifs',NULL,'Total (+) urines','Total (+) urines (Shistosomiases)',7,133,153),(103,100,NULL,'$_632 = [shisto.S_HAEMA]',130,'S. haematobium',NULL,'S. haematobium (+)','S. haematobium (+)',8,133,153),(104,100,NULL,'$_632 = [shisto.autres]',130,'Autres',NULL,NULL,NULL,NULL,NULL,153),(105,100,NULL,'$_627 = [posnegind.Négatif]',131,'Négatifs',NULL,'Total (-) selles','Total (-) selles (Shistosomiases)',2,133,141),(106,100,NULL,'$_627 = [posnegind.Positif]',131,'Positifs',NULL,'Total (+) selles','Total (+) selles (Shistosomiases)',3,133,141),(107,100,NULL,'$_641 = [shisto2.S.mansoni]',131,'S. mansoni ',NULL,'D - S. mansoni ','D - S. mansoni',4,133,141),(108,100,NULL,'$_641 = [shisto2.autres]',131,'Autres',NULL,NULL,NULL,NULL,NULL,141),(109,100,NULL,'$_715 = [posnegind.Négatif]',132,'Négatifs',NULL,NULL,NULL,NULL,NULL,138),(110,100,NULL,'$_715 = [posnegind.Positif]',132,'Positifs',NULL,NULL,NULL,NULL,NULL,138),(111,100,NULL,'$_634 = [filariose.wb]',132,'W. bancrofti',NULL,NULL,NULL,NULL,NULL,138),(112,100,NULL,'$_634 = [filariose.autres]',132,'Autres',NULL,NULL,NULL,NULL,NULL,138),(113,100,NULL,'{333, 344}',NULL,NULL,NULL,'Total échantillons LCR','Total echantillons LCR',1,113,99),(114,100,NULL,'{636,637,639,640}',NULL,NULL,NULL,'Total échantillons selles','Total echantillon selles (cholera)',1,114,141),(115,100,NULL,'N/A',NULL,NULL,NULL,'Total échantillons selles liquidiennes','Total echantillons selles liquidiennes (Cholera)',2,114,141),(116,100,NULL,'N/A',NULL,NULL,NULL,'Total échantillons selles autres aspects','Total echantillons Autres aspects(Cholera)',3,114,141),(117,100,NULL,'$_636 = [yorn.1] AND $_637 = [yorn.1]',NULL,NULL,NULL,'Bacilles mobiles polaires, incurvés à Gram (-) ','Bacilles mobiles polaires, incurves a Gram (-)',7,114,141),(118,100,NULL,'{391, 344}',NULL,NULL,NULL,'Total échantillons selles','Total echantillon selles (shigellose)',1,115,141),(119,100,NULL,'$_391 = [aspestselles.5]',NULL,NULL,NULL,'Total échantillons selles glairo-sanglantes ','Total echantillons selles glairo-sanglantes',2,115,141),(120,100,NULL,'$_391 != [aspestselles.5]',NULL,NULL,NULL,'Total échantillons selles autres aspects','Total echantillons Autres aspects (Shigelloses)',3,115,141),(121,100,NULL,'N/A',NULL,NULL,NULL,'Bacilles immobiles à Gram (-) ','Bacilles immobiles a Gram (-)',7,115,141),(122,100,NULL,'{611}',NULL,NULL,NULL,'Total expectorations','Total Expectorations',1,118,50),(123,100,NULL,'N/A',NULL,NULL,NULL,'TPM + nouveaux','TPM + nouveaux',4,118,50),(124,100,NULL,'{316,616,617}',NULL,NULL,NULL,'Total sang (GE/Frottis)','Total SANG (SG ; Frottis)',1,117,138),(125,100,NULL,'{212, 347, 353, 356, 361}',NULL,NULL,NULL,'Total échantillons prél. vaginal','Total echantillons Prel Vaginal (IST)',1,122,162),(126,100,NULL,'N/A',NULL,NULL,NULL,'Total (-) (PV)','Total (-) (PV - IST)',2,122,162),(127,100,NULL,'N/A',NULL,NULL,NULL,'Total (+) (PV)','Total (+) (PV - IST)',3,122,162),(128,100,NULL,'{344, 353, 356, 347}',NULL,NULL,NULL,'Total echantillons prél. uretral','Total echantillons Prel uretral (IST)',10,122,152),(129,100,NULL,'N/A',NULL,NULL,NULL,'Total (-) (PU)','Total (-) (PU - IST)',11,122,152),(130,100,NULL,'N/A',NULL,NULL,NULL,'Total (+) (PU)','Total (+) (PU - IST)',12,122,152),(131,100,NULL,'$_347  = [yorn.1]',NULL,NULL,NULL,'Trichomo. vaginalis (Prélèvement Urétral)','Trichomo. vaginalis (Prelevement Uretral)',15,122,152),(132,100,NULL,'N/A',NULL,NULL,NULL,'Chlamydia trachomatis direct (Prélèvement Urétral)','Chlamydia trachomatis direct (Prelevement Uretral)',18,122,152),(133,100,NULL,'{229,231}',NULL,NULL,NULL,'Total echantillons Sang','Total echantillons Sang (IST)',19,122,138),(134,100,NULL,'N/A',NULL,NULL,NULL,'Total (-) (Sang)','Total (-) (Sang IST)',20,122,138),(135,100,NULL,'N/A',NULL,NULL,NULL,'Total (+) (Sang)','Total (+) (Sang IST)',21,122,138),(136,100,NULL,'{627,641}',NULL,NULL,NULL,'Total échantillons selles','Total echantillons  Selles (Shistosomiases)',1,133,141),(137,100,NULL,'{627,632}',NULL,NULL,NULL,'Total échantillons urines','Total echantillons  Urines (Shistosomiases)',5,133,153),(138,100,NULL,'{278}',NULL,NULL,NULL,'Total échantillons','Total echantillons (VIH)',1,119,138),(139,100,NULL,'N/A',NULL,NULL,NULL,'Total référés (VIH)','Total referes (VIH)',4,119,138);
/*!40000 ALTER TABLE `sigl_15_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_15_data_group`
--

DROP TABLE IF EXISTS `sigl_15_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_15_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_15_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_15_data_group`
--

LOCK TABLES `sigl_15_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_15_data_group` DISABLE KEYS */;
INSERT INTO `sigl_15_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000),(8,8,1000),(9,9,1000),(10,10,1000),(11,11,1000),(12,12,1000),(13,13,1000),(14,14,1000),(15,15,1000),(16,16,1000),(17,17,1000),(18,18,1000),(19,19,1000),(20,20,1000),(21,21,1000),(22,22,1000),(23,23,1000),(24,24,1000),(25,25,1000),(26,26,1000),(27,27,1000),(28,28,1000),(29,29,1000),(30,30,1000),(31,31,1000),(32,32,1000),(33,33,1000),(34,34,1000),(35,35,1000),(36,36,1000),(37,37,1000),(38,38,1000),(39,39,1000),(40,40,1000),(41,41,1000),(42,42,1000),(43,43,1000),(44,44,1000),(45,45,1000),(46,46,1000),(47,47,1000),(48,48,1000),(49,49,1000),(50,50,1000),(51,51,1000),(52,52,1000),(53,53,1000),(54,54,1000),(55,55,1000),(56,56,1000),(57,57,1000),(58,58,1000),(59,59,1000),(60,60,1000),(61,61,1000),(62,62,1000),(63,63,1000),(64,64,1000),(65,65,1000),(66,66,1000),(67,67,1000),(68,68,1000),(69,69,1000),(70,70,1000),(71,71,1000),(72,72,1000),(73,73,1000),(74,74,1000),(75,75,1000),(76,76,1000),(77,77,1000),(78,78,1000),(79,79,1000),(80,80,1000),(81,81,1000),(82,82,1000),(83,83,1000),(84,84,1000),(85,85,1000),(86,86,1000),(87,87,1000),(88,88,1000),(89,89,1000),(90,90,1000),(91,91,1000),(92,92,1000),(93,93,1000),(94,94,1000),(95,95,1000),(96,96,1000),(97,97,1000),(98,98,1000),(99,99,1000),(100,100,1000),(101,101,1000),(102,102,1000),(103,103,1000),(104,104,1000),(105,105,1000),(106,106,1000),(107,107,1000),(108,108,1000),(109,109,1000),(110,110,1000),(111,111,1000),(112,112,1000);
/*!40000 ALTER TABLE `sigl_15_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_15_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_15_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_15_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_15_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_15_data_group_mode`
--

LOCK TABLES `sigl_15_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_15_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_15_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_15_deleted`
--

DROP TABLE IF EXISTS `sigl_15_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_15_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL DEFAULT '100',
  `nom_amont` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `formule` text COLLATE utf8_unicode_ci NOT NULL,
  `id_surveillance` int(10) unsigned NOT NULL,
  `libelle_ind` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `methode_calcul` text COLLATE utf8_unicode_ci,
  `label_dhis2` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `label_exp_dhis2` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dhis2_pos` int(11) DEFAULT NULL,
  `id_surveillance_dhis2` int(10) unsigned DEFAULT NULL,
  `nature_prel` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_15_data_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_15_deleted`
--

LOCK TABLES `sigl_15_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_15_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_15_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_16_data`
--

DROP TABLE IF EXISTS `sigl_16_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_16_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL DEFAULT '100',
  `id_indicateur` int(10) unsigned NOT NULL,
  `id_refvariable` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_16_data_owner` (`id_owner`),
  KEY `sigl_16_data_id_indicateur_indicateur` (`id_indicateur`),
  KEY `sigl_16_data_id_refvariable_refvariable` (`id_refvariable`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_16_data`
--

LOCK TABLES `sigl_16_data` WRITE;
/*!40000 ALTER TABLE `sigl_16_data` DISABLE KEYS */;
INSERT INTO `sigl_16_data` VALUES (1,100,1,240),(2,100,2,240),(3,100,3,240),(4,100,4,240),(5,100,5,240),(6,100,6,290),(7,100,7,290),(8,100,8,290),(9,100,9,290),(10,100,10,290),(11,100,11,290),(12,100,12,290),(13,100,13,290),(14,100,14,290),(15,100,15,290),(16,100,16,290),(17,100,17,488),(18,100,18,488),(19,100,19,305),(20,100,20,305),(21,100,21,305),(22,100,22,305),(23,100,23,305),(24,100,24,305),(25,100,25,305),(26,100,26,305),(27,100,27,305),(28,100,28,305),(29,100,29,507),(30,100,30,508),(31,100,31,508),(32,100,32,508),(33,100,33,510),(34,100,34,511),(35,100,35,300),(36,100,36,300),(37,100,37,300),(38,100,38,300),(39,100,39,300),(40,100,40,300),(41,100,41,300),(42,100,42,300),(43,100,43,300),(44,100,44,465),(45,100,45,465),(46,100,46,466),(47,100,47,466),(48,100,48,180),(49,100,49,180),(50,100,50,462),(51,100,51,462),(52,100,52,461),(53,100,53,461),(54,100,54,461),(55,100,55,461),(56,100,56,461),(57,100,57,489),(58,100,58,489),(59,100,59,199),(60,100,60,199),(61,100,61,199),(62,100,62,199),(63,100,63,199),(64,100,64,199),(65,100,65,200),(66,100,66,200),(67,100,67,481),(68,100,68,484),(69,100,69,166),(70,100,70,167),(71,100,71,167),(72,100,72,163),(73,100,73,486),(74,100,74,253),(75,100,75,485),(76,100,76,250),(77,100,77,258),(78,100,78,258),(79,100,79,250),(80,100,80,240),(81,100,81,234),(82,100,82,258),(83,100,83,243),(84,100,84,234),(85,100,85,490),(86,100,86,491),(87,100,87,492),(88,100,88,493),(89,100,89,493),(90,100,90,493),(91,100,91,494),(92,100,92,495),(93,100,93,495),(94,100,94,495),(95,100,95,496),(96,100,96,497),(97,100,97,498),(98,100,98,498),(99,100,99,498),(100,100,100,499),(101,100,101,500),(102,100,102,500),(103,100,103,501),(104,100,104,501),(105,100,105,502),(106,100,106,502),(107,100,107,503),(108,100,108,503),(109,100,109,504),(110,100,110,504),(111,100,111,505),(112,100,112,505);
/*!40000 ALTER TABLE `sigl_16_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_16_data_group`
--

DROP TABLE IF EXISTS `sigl_16_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_16_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_16_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_16_data_group`
--

LOCK TABLES `sigl_16_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_16_data_group` DISABLE KEYS */;
INSERT INTO `sigl_16_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000),(8,8,1000),(9,9,1000),(10,10,1000),(11,11,1000),(12,12,1000),(13,13,1000),(14,14,1000),(15,15,1000),(16,16,1000),(17,17,1000),(18,18,1000),(19,19,1000),(20,20,1000),(21,21,1000),(22,22,1000),(23,23,1000),(24,24,1000),(25,25,1000),(26,26,1000),(27,27,1000),(28,28,1000),(29,29,1000),(30,30,1000),(31,31,1000),(32,32,1000),(33,33,1000),(34,34,1000),(35,35,1000),(36,36,1000),(37,37,1000),(38,38,1000),(39,39,1000),(40,40,1000),(41,41,1000),(42,42,1000),(43,43,1000),(44,44,1000),(45,45,1000),(46,46,1000),(47,47,1000),(48,48,1000),(49,49,1000),(50,50,1000),(51,51,1000),(52,52,1000),(53,53,1000),(54,54,1000),(55,55,1000),(56,56,1000),(57,57,1000),(58,58,1000),(59,59,1000),(60,60,1000),(61,61,1000),(62,62,1000),(63,63,1000),(64,64,1000),(65,65,1000),(66,66,1000),(67,67,1000),(68,68,1000),(69,69,1000),(70,70,1000),(71,71,1000),(72,72,1000),(73,73,1000),(74,74,1000),(75,75,1000),(76,76,1000),(77,77,1000),(78,78,1000),(79,79,1000),(80,80,1000),(81,81,1000),(82,82,1000),(83,83,1000),(84,84,1000),(85,85,1000),(86,86,1000),(87,87,1000),(88,88,1000),(89,89,1000),(90,90,1000),(91,91,1000),(92,92,1000),(93,93,1000),(94,94,1000),(95,95,1000),(96,96,1000),(97,97,1000),(98,98,1000),(99,99,1000),(100,100,1000),(101,101,1000),(102,102,1000),(103,103,1000),(104,104,1000),(105,105,1000),(106,106,1000),(107,107,1000),(108,108,1000),(109,109,1000),(110,110,1000),(111,111,1000),(112,112,1000);
/*!40000 ALTER TABLE `sigl_16_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_16_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_16_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_16_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_16_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_16_data_group_mode`
--

LOCK TABLES `sigl_16_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_16_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_16_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_16_deleted`
--

DROP TABLE IF EXISTS `sigl_16_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_16_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL DEFAULT '100',
  `id_indicateur` int(10) unsigned NOT NULL,
  `id_refvariable` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_16_data_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_16_deleted`
--

LOCK TABLES `sigl_16_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_16_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_16_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_ctrl_resultat__file_data`
--

DROP TABLE IF EXISTS `sigl_controle_externe_ctrl_resultat__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_ctrl_resultat__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_ctrl_resultat__file_data`
--

LOCK TABLES `sigl_controle_externe_ctrl_resultat__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_ctrl_resultat__file_data_group`
--

DROP TABLE IF EXISTS `sigl_controle_externe_ctrl_resultat__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_ctrl_resultat__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_ctrl_resultat__file_data_group`
--

LOCK TABLES `sigl_controle_externe_ctrl_resultat__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_ctrl_resultat__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_controle_externe_ctrl_resultat__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_ctrl_resultat__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_ctrl_resultat__file_data_group_mode`
--

LOCK TABLES `sigl_controle_externe_ctrl_resultat__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_ctrl_resultat__file_deleted`
--

DROP TABLE IF EXISTS `sigl_controle_externe_ctrl_resultat__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_ctrl_resultat__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_ctrl_resultat__file_deleted`
--

LOCK TABLES `sigl_controle_externe_ctrl_resultat__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_ctrl_resultat_cr__file_data`
--

DROP TABLE IF EXISTS `sigl_controle_externe_ctrl_resultat_cr__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_ctrl_resultat_cr__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_ctrl_resultat_cr__file_data`
--

LOCK TABLES `sigl_controle_externe_ctrl_resultat_cr__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat_cr__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat_cr__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_ctrl_resultat_cr__file_data_group`
--

DROP TABLE IF EXISTS `sigl_controle_externe_ctrl_resultat_cr__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_ctrl_resultat_cr__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_ctrl_resultat_cr__file_data_group`
--

LOCK TABLES `sigl_controle_externe_ctrl_resultat_cr__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat_cr__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat_cr__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_ctrl_resultat_cr__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_controle_externe_ctrl_resultat_cr__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_ctrl_resultat_cr__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_ctrl_resultat_cr__file_data_group_mode`
--

LOCK TABLES `sigl_controle_externe_ctrl_resultat_cr__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat_cr__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat_cr__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_ctrl_resultat_cr__file_deleted`
--

DROP TABLE IF EXISTS `sigl_controle_externe_ctrl_resultat_cr__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_ctrl_resultat_cr__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_ctrl_resultat_cr__file_deleted`
--

LOCK TABLES `sigl_controle_externe_ctrl_resultat_cr__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat_cr__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_ctrl_resultat_cr__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_data`
--

DROP TABLE IF EXISTS `sigl_controle_externe_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `date_ctrl` date DEFAULT NULL,
  `organisateur_nom` varchar(255) DEFAULT NULL,
  `organisateur_contact` text,
  `resultat` text,
  `commentaire` text,
  `id_planning_ctrl_ext` int(10) unsigned DEFAULT NULL,
  `date_recep_result` date DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_data`
--

LOCK TABLES `sigl_controle_externe_data` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_data_group`
--

DROP TABLE IF EXISTS `sigl_controle_externe_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_data_group`
--

LOCK TABLES `sigl_controle_externe_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_controle_externe_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_data_group_mode`
--

LOCK TABLES `sigl_controle_externe_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_externe_deleted`
--

DROP TABLE IF EXISTS `sigl_controle_externe_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_externe_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `date_ctrl` date DEFAULT NULL,
  `organisateur_nom` varchar(255) DEFAULT NULL,
  `organisateur_contact` text,
  `resultat` text,
  `commentaire` text,
  `id_planning_ctrl_ext` int(10) unsigned DEFAULT NULL,
  `date_recep_result` date DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_externe_deleted`
--

LOCK TABLES `sigl_controle_externe_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_controle_externe_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_externe_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_interne_data`
--

DROP TABLE IF EXISTS `sigl_controle_interne_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_interne_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `valeur` text,
  `resultat` text,
  `commentaire` text,
  `id_planning_ctrl_int` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_interne_data`
--

LOCK TABLES `sigl_controle_interne_data` WRITE;
/*!40000 ALTER TABLE `sigl_controle_interne_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_interne_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_interne_data_group`
--

DROP TABLE IF EXISTS `sigl_controle_interne_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_interne_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_interne_data_group`
--

LOCK TABLES `sigl_controle_interne_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_controle_interne_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_interne_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_interne_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_controle_interne_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_interne_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_interne_data_group_mode`
--

LOCK TABLES `sigl_controle_interne_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_controle_interne_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_interne_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_controle_interne_deleted`
--

DROP TABLE IF EXISTS `sigl_controle_interne_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_controle_interne_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `valeur` text,
  `resultat` text,
  `commentaire` text,
  `id_planning_ctrl_int` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_controle_interne_deleted`
--

LOCK TABLES `sigl_controle_interne_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_controle_interne_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_controle_interne_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dico_data`
--

DROP TABLE IF EXISTS `sigl_dico_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dico_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `dico_name` varchar(20) NOT NULL,
  `label` varchar(255) NOT NULL,
  `short_label` varchar(20) NOT NULL,
  `position` int(10) DEFAULT NULL,
  `code` varchar(10) DEFAULT NULL,
  `dico_id` varchar(40) DEFAULT NULL,
  `dico_value_id` varchar(40) DEFAULT NULL,
  `archived` int(1) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `idx_dico_name` (`dico_name`),
  KEY `sigl_dico_data_owner` (`id_owner`)
) ENGINE=InnoDB AUTO_INCREMENT=1163 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dico_data`
--

LOCK TABLES `sigl_dico_data` WRITE;
/*!40000 ALTER TABLE `sigl_dico_data` DISABLE KEYS */;
INSERT INTO `sigl_dico_data` VALUES (1,100,'sexe','Masculin','M',10,'M',NULL,NULL,NULL),(2,100,'sexe','Féminin','F',20,'F',NULL,NULL,NULL),(3,100,'sexe','Inconnu','I',30,'I',NULL,NULL,NULL),(4,100,'yorn','Oui','1',10,'1',NULL,NULL,NULL),(5,100,'yorn','Non','0',20,'0',NULL,NULL,NULL),(6,100,'facturation','Analyse','A',10,'A',NULL,NULL,NULL),(7,100,'facturation','Prélèvement','P',20,'P',NULL,NULL,NULL),(8,100,'prel_statut','Fait','FAIT',10,'FAIT',NULL,NULL,NULL),(9,100,'prel_statut','A faire','A FAIRE',20,'A FAIRE',NULL,NULL,NULL),(10,100,'prel_statut','Apporté','APPORTE',30,'APPORTE',NULL,NULL,NULL),(11,100,'famille_analyse','Biochimie sanguine','BIOS',10,'BIOS',NULL,NULL,NULL),(12,100,'famille_analyse','Biochimie urinaire','BIOU',20,'BIOU',NULL,NULL,NULL),(13,100,'famille_analyse','Biochimie LDP','BIOL',30,'BIOL',NULL,NULL,NULL),(15,100,'famille_analyse','Parasitologie','PARA',80,'PARA',NULL,NULL,NULL),(16,100,'famille_analyse','Mycologie','MYCO',90,'MYCO',NULL,NULL,NULL),(17,100,'famille_analyse','Virologie','VIRO',100,'VIRO',NULL,NULL,NULL),(18,100,'famille_analyse','Bactériologie','BACT',110,'BACT',NULL,NULL,NULL),(19,100,'famille_analyse','Immunologie / hormonologie / protéines spécifiques','IHPS',40,'IHPS',NULL,NULL,NULL),(20,100,'famille_analyse','Anatomie et cytologie pathologiques','ANAP',120,'ANAP',NULL,NULL,NULL),(23,100,'famille_analyse','Biologie moléculaire','BIOM',130,'BIOM',NULL,NULL,NULL),(24,100,'famille_analyse','Analyses sanitaires','SANI',140,'SANI',NULL,NULL,NULL),(25,100,'famille_analyse','Divers','DIVE',150,'DIVE',NULL,NULL,NULL),(26,100,'paillasse','Numération sanguine','NUMSANG',10,'NUMSANG',NULL,NULL,NULL),(27,100,'paillasse','Biochimie sanguine de routine','BIOSR',20,'BIOSR',NULL,NULL,NULL),(28,100,'paillasse','Sérologies virales','SV',30,'SV',NULL,NULL,NULL),(34,100,'type_prel','Liquide de ponction articulaire','Articulaire',60,'LPA',NULL,NULL,NULL),(35,100,'type_prel','Liquide de ponction ascite','Ascite',70,'Ascite',NULL,NULL,NULL),(38,100,'type_prel','Biopsie','Biopsie',100,'Biopsie',NULL,NULL,NULL),(50,100,'type_prel','Crachat','Crachat',220,'Crachat',NULL,NULL,NULL),(56,100,'type_prel','Lavage Broncho Alvéolaire','LBA',280,'LBA',NULL,NULL,NULL),(75,100,'type_prel','Prélèvement gorge','Gorge',470,'Gorge',NULL,NULL,NULL),(99,100,'type_prel','Liquide Céphalo-Rachidien','LCR',710,'LCR',NULL,NULL,NULL),(100,100,'type_prel','Liquide de ponction bronchique','Bronchique',720,'Bronchique',NULL,NULL,NULL),(102,100,'type_prel','Liquide de ponction alvéolaire','Alveolaire',740,'Alveolaire',NULL,NULL,NULL),(104,100,'type_prel','Liquide de ponction pleural','Pleural',760,'Pleural',NULL,NULL,NULL),(138,100,'type_prel','Sang','Sang',1100,'Sang',NULL,NULL,NULL),(141,100,'type_prel','Selles','Selles',1130,'Selles',NULL,NULL,NULL),(152,100,'type_prel','Prélèvement urétral','Uretral',1240,'Uretral',NULL,NULL,NULL),(153,100,'type_prel','Urine','Urine',1250,'Urine',NULL,NULL,NULL),(162,100,'type_prel','Prélèvement vaginal','Vaginal',1340,'Vaginal',NULL,NULL,NULL),(163,100,'type_prel','Autre','Autre',1350,'Autre',NULL,NULL,NULL),(170,100,'type_analyse','Individuelle','INDIVIDUELLE',10,'INDIV',NULL,NULL,NULL),(171,100,'type_analyse','Combinée','COMBINEE',20,'COMBINEE',NULL,NULL,NULL),(173,100,'statut_analyse','A faire','A FAIRE',10,'A FAIRE',NULL,NULL,NULL),(174,100,'statut_analyse','Faite','FAITE',20,'FAITE',NULL,NULL,NULL),(175,100,'profil','Secrétaire','secretaire',10,'secretaire',NULL,NULL,NULL),(176,100,'profil','Technicien','technicien',20,'technicien',NULL,NULL,NULL),(177,100,'profil','Biologiste','biologiste',30,'biologiste',NULL,NULL,NULL),(178,100,'profil_bis','Bactério','Bactério',10,'Bactério',NULL,NULL,NULL),(179,100,'profil_bis','Virologie','Virologie',20,'Virologie',NULL,NULL,NULL),(180,100,'profil_bis','Macro','Macro',30,'Macro',NULL,NULL,NULL),(181,100,'statut_dossier','Nouveau','NOUVEAU',10,'NOUVEAU',NULL,NULL,NULL),(182,100,'statut_dossier','Validé administrativement','VALID_ADM',20,'VALID_ADM',NULL,NULL,NULL),(183,100,'type_dossier','Externe','EXTERNE',10,'EXTERNE',NULL,NULL,NULL),(184,100,'type_dossier','Interne','INTERNE',20,'INTERNE',NULL,NULL,NULL),(186,100,'specialite','Allergologue','Allergologue',10,'ALLERG',NULL,NULL,NULL),(187,100,'specialite','Andrologue','Andrologue',20,'Andrologue',NULL,NULL,NULL),(189,100,'specialite','Anatomopathologiste','Anapath',40,'Anapath',NULL,NULL,NULL),(190,100,'specialite','Anesthésiste','Anesthésiste',50,'ANESTH',NULL,NULL,NULL),(192,100,'specialite','Cancérologue','Cancérologue',70,'CANCER',NULL,NULL,NULL),(193,100,'specialite','Cardiologue','Cardiologue',80,'CARDIO',NULL,NULL,NULL),(194,100,'specialite','Chirurgien','Chirurgien',90,'Chirurgien',NULL,NULL,NULL),(195,100,'specialite','Dermatologue','Dermato',100,'Dermato',NULL,NULL,NULL),(196,100,'specialite','Endocrinologue','Endocrino',110,'Endocrino',NULL,NULL,NULL),(197,100,'specialite','Gastro-entérologue','Gastroenterologue',120,'GASTRO',NULL,NULL,NULL),(198,100,'specialite','Généticien','Généticien',130,'GENET',NULL,NULL,NULL),(199,100,'specialite','Gériatre','Gériatre',140,'Gériatre',NULL,NULL,NULL),(200,100,'specialite','Gynécologue','Gynéco',150,'Gynéco',NULL,NULL,NULL),(201,100,'specialite','Hématologue','Hémato',160,'Hémato',NULL,NULL,NULL),(202,100,'specialite','Inféctiologue','Inféctiologue',170,'INFECTIO',NULL,NULL,NULL),(204,100,'specialite','Généraliste','Généraliste',190,'GEN',NULL,NULL,NULL),(205,100,'specialite','Urgentiste','Urgentiste',200,'Urgentiste',NULL,NULL,NULL),(206,100,'specialite','Médecine du travail','Médecine du travail',210,'MED_TRAV',NULL,NULL,NULL),(207,100,'specialite','Nutritionniste - diététicien','Nutritionniste',220,'NUTRI',NULL,NULL,NULL),(208,100,'specialite','Néphrologue','Néphro',230,'Néphro',NULL,NULL,NULL),(209,100,'specialite','Neurochirurgien','Neurochirurgien',240,'NEUROCHIR',NULL,NULL,NULL),(210,100,'specialite','Neurologue','Neurologue',250,'Neurologue',NULL,NULL,NULL),(211,100,'specialite','Oncologue','Oncologue',260,'Oncologue',NULL,NULL,NULL),(212,100,'specialite','Ophtalmologiste','Ophtalmo',270,'Ophtalmo',NULL,NULL,NULL),(213,100,'specialite','Otorhinolaryngologiste','ORL',280,'ORL',NULL,NULL,NULL),(215,100,'specialite','Pédiatre','Pédiatre',300,'Pédiatre',NULL,NULL,NULL),(216,100,'specialite','Pédopsychiatre','Pédopsychiatre',310,'PEDOPSY',NULL,NULL,NULL),(217,100,'specialite','Psychiatre','Psychiatre',320,'Psychiatre',NULL,NULL,NULL),(219,100,'specialite','Radiologue','Radiologue',340,'Radiologue',NULL,NULL,NULL),(220,100,'specialite','Rhumatologue','Rhumatologue',350,'RHUMATO',NULL,NULL,NULL),(221,100,'specialite','Stomatologue','Stomatologue',360,'STOMATO',NULL,NULL,NULL),(222,100,'specialite','Urologue','Urologue',370,'Urologue',NULL,NULL,NULL),(225,100,'specialite','Dentiste','Dentiste',400,'Dentiste',NULL,NULL,NULL),(226,100,'type_resultat','Chaîne de caractère','varchar',20,'varchar',NULL,NULL,NULL),(227,100,'type_resultat','Entier','integer',30,'integer',NULL,NULL,NULL),(228,100,'type_resultat','Réel','float',40,'float',NULL,NULL,NULL),(229,100,'type_resultat','Calculée','calculee',50,'calculee',NULL,NULL,NULL),(230,100,'type_resultat','Positif / négatif','dico_posneg',60,'D_POS_NEG',NULL,NULL,NULL),(231,100,'type_resultat','Oui / Non','dico_yorn',70,'dico_yorn',NULL,NULL,NULL),(232,100,'posneg','Positif','+',10,'+',NULL,NULL,NULL),(233,100,'posneg','Négatif','-',20,'-',NULL,NULL,NULL),(234,100,'unite_valeur','mmol/24h','mmol/24h',280,'mmol/24h',NULL,NULL,NULL),(235,100,'unite_valeur','mmol/l','mmol/l',210,'mmol/l',NULL,NULL,NULL),(236,100,'unite_valeur','% (HDL)','% (HDL)',20,'% (HDL)',NULL,NULL,NULL),(237,100,'unite_valeur','% (VLDL)','% (VLDL)',30,'% (VLDL)',NULL,NULL,NULL),(238,100,'unite_valeur','mm Hg','mm Hg',300,'mm Hg',NULL,NULL,NULL),(239,100,'unite_valeur','%','%',10,'%',NULL,NULL,NULL),(240,100,'unite_valeur','mm','mm',50,'mm',NULL,NULL,NULL),(241,100,'unite_valeur','million/mm3','million/mm3',260,'10^6/mm3',NULL,NULL,NULL),(242,100,'unite_valeur','mille/mm3','mille/mm3',250,'mille/mm3',NULL,NULL,NULL),(243,100,'unite_valeur','g/dl','g/dl',140,'g/dl',NULL,NULL,NULL),(244,100,'unite_valeur','fl','fl',80,'fl',NULL,NULL,NULL),(245,100,'unite_valeur','pg','pg',90,'pg',NULL,NULL,NULL),(246,100,'type_resultat','Absent / Présent','dico_absent',80,'D_ABS',NULL,NULL,NULL),(247,100,'absent','Absent','absent',10,'absent',NULL,NULL,NULL),(248,100,'absent','Présent','present',20,'present',NULL,NULL,NULL),(249,100,'unite_valeur','mg/24h','mg/24h',200,'mg/24h',NULL,NULL,NULL),(250,100,'type_validation','Administratif','A',10,'A',NULL,NULL,NULL),(251,100,'type_validation','Technique','T',20,'T',NULL,NULL,NULL),(252,100,'type_validation','Biologique','B',30,'B',NULL,NULL,NULL),(253,100,'statut_dossier','Intermédiaire (validé admin.)','INT_VALID_ADM',30,'INT_ADM',NULL,NULL,NULL),(254,100,'statut_dossier','Validé techniquement','VALID_TECH',40,'VALID_TECH',NULL,NULL,NULL),(255,100,'statut_dossier','Intermédiaire (validé tech.)','INT_VALID_TECH',50,'INT_TECH',NULL,NULL,NULL),(256,100,'statut_dossier','Validé biologiquement','VALID_BIO',60,'VALID_BIO',NULL,NULL,NULL),(257,100,'doc_type','Compte rendu','CR',10,'CR',NULL,NULL,NULL),(258,100,'doc_type','Facture','F',20,'F',NULL,NULL,NULL),(259,100,'file_type','PDF','pdf',10,'pdf',NULL,NULL,NULL),(260,100,'titre_civilite','Monsieur','Mr',10,'Mr',NULL,NULL,NULL),(261,100,'titre_civilite','Madame','Mme',20,'Mme',NULL,NULL,NULL),(262,100,'titre_civilite','Mademoiselle','Mlle',30,'Mlle',NULL,NULL,NULL),(263,100,'titre_civilite','Docteur','Dr',40,'Dr',NULL,NULL,NULL),(264,100,'titre_civilite','Professeur','Pr',50,'Pr',NULL,NULL,NULL),(265,100,'type_resultat','Libellé','label',10,'label',NULL,NULL,NULL),(266,100,'profil','Administrateur','admin',40,'admin',NULL,NULL,NULL),(267,100,'remise_facturation','Personnel hospitalier','Personnel',10,'Personnel',NULL,NULL,NULL),(268,100,'remise_facturation','Exonération','Exonération',20,'EXON',NULL,NULL,NULL),(269,100,'remise_facturation','Autre','Autre',30,'Autre',NULL,NULL,NULL),(270,100,'motif_annulation','Produit pathologique insuffisant','manque_p_pathol',10,'MANQ_PATHO',NULL,NULL,NULL),(271,100,'motif_annulation','Examen supprimé pour cause de résultats précédents','atcd',20,'atcd',NULL,NULL,NULL),(272,100,'motif_annulation','Problème de produit pathologique','pb_p_pathol',30,'PB_PATHO',NULL,NULL,NULL),(273,100,'motif_annulation','Culture négative','c_neg',40,'c_neg',NULL,NULL,NULL),(274,100,'motif_annulation','Autre','autre',100,'autre',NULL,NULL,NULL),(275,100,'lieu_prel','Interne au labo','labo',10,'labo',NULL,NULL,NULL),(276,100,'lieu_prel','Hôpital','hopital',20,'hopital',NULL,NULL,NULL),(277,100,'lieu_prel','Extérieur','exterieur',40,'exterieur',NULL,NULL,NULL),(278,100,'famille_analyse','Cytologie','CYTO',50,'CYTO',NULL,NULL,NULL),(279,100,'famille_analyse','Hématologie, Immunohématologie et Hémostase','IMMU',70,'IMMU',NULL,NULL,NULL),(280,100,'unite_valeur','mg/l','mg/l',150,'mg/l',NULL,NULL,NULL),(281,100,'unite_valeur','µmol/l','µmol/l',220,'µmol/l',NULL,NULL,NULL),(282,100,'unite_valeur','g/l','g/l',100,'g/l',NULL,NULL,NULL),(283,100,'unite_valeur','µg/l','µg/l',105,'µg/l',NULL,NULL,NULL),(284,100,'unite_valeur','UI/l','UI/l',155,'UI/l',NULL,NULL,NULL),(285,100,'unite_valeur','nmol/l','nmol/l',230,'nmol/l',NULL,NULL,NULL),(286,100,'unite_valeur','ng/ml','ng/ml',130,'ng/ml',NULL,NULL,NULL),(287,100,'unite_valeur','pg/ml','pg/ml',110,'pg/ml',NULL,NULL,NULL),(288,100,'unite_valeur','pmol/l','pmol/l',240,'pmol/l',NULL,NULL,NULL),(289,100,'unite_valeur','µUI/ml','µUI/ml',185,'µUI/ml',NULL,NULL,NULL),(290,100,'unite_valeur','g/24h','g/24h',240,'g/24h',NULL,NULL,NULL),(291,100,'unite_valeur','sec','s',40,'s',NULL,NULL,NULL),(292,100,'unite_valeur','µg/ml','µg/ml',120,'µg/ml',NULL,NULL,NULL),(293,100,'unite_valeur','UI/ml','UI/ml',160,'UI/ml',NULL,NULL,NULL),(294,100,'unite_valeur','KUI/ml','KUI/ml',170,'KUI/ml',NULL,NULL,NULL),(295,100,'unite_valeur','litres','l',60,'l',NULL,NULL,NULL),(296,100,'unite_valeur','ml/min','ml/min',270,'ml/min',NULL,NULL,NULL),(297,100,'unite_valeur','mEq/l','mEq/l',290,'mEq/l',NULL,NULL,NULL),(298,100,'unite_valeur','mUI/l','mUI/l',180,'mUI/l',NULL,NULL,NULL),(299,100,'type_cq','Controle qualité interne','CQI',10,'CQI',NULL,NULL,NULL),(300,100,'type_cq','Controle qualité externe','CQE',10,'CQE',NULL,NULL,NULL),(301,100,'famille_analyse','Biochimie','BIO',5,'BIO',NULL,NULL,NULL),(302,100,'famille_analyse','Immuno- Sérologie et Biologie moléculaire','ISBM',75,'ISBM',NULL,NULL,NULL),(303,100,'famille_analyse','Médicaments et toxiques','MED',160,'MED',NULL,NULL,NULL),(304,100,'famille_analyse','Spermiologie','SPER',170,'SPER',NULL,NULL,NULL),(305,100,'aspestselles','Moulées','1',10,'1',NULL,NULL,NULL),(306,100,'aspestselles','Pâteuses','2',20,'2',NULL,NULL,NULL),(307,100,'aspestselles','Dures','3',30,'3',NULL,NULL,NULL),(308,100,'aspestselles','Glaireuses','4',40,'4',NULL,NULL,NULL),(309,100,'aspestselles','Glairo-sanguinolentes','5',50,'5',NULL,NULL,NULL),(310,100,'aspestselles','Pâteuses sanguinolentes','6',60,'6',NULL,NULL,NULL),(311,100,'aspestselles','Liquides sanguinolentes','7',70,'7',NULL,NULL,NULL),(312,100,'aspestselles','Liquides','8',80,'8',NULL,NULL,NULL),(313,100,'aspestselles','Semi-liquides','9',90,'9',NULL,NULL,NULL),(314,100,'aspestselles','verdâtres','10',100,'10',NULL,NULL,NULL),(315,100,'nombre','Néant','1',10,'1',NULL,NULL,NULL),(316,100,'nombre','Rares','2',20,'2',NULL,NULL,NULL),(317,100,'nombre','Quelques','3',30,'3',NULL,NULL,NULL),(318,100,'nombre','Nombreux','4',40,'4',NULL,NULL,NULL),(319,100,'nombre','Très nombreux','5',50,'5',NULL,NULL,NULL),(320,100,'parasite','Néant','1',10,'1',NULL,NULL,NULL),(321,100,'parasite','Kystes d\'Entamoeba coli','2',20,'2',NULL,NULL,NULL),(322,100,'parasite','Kystes d\'Entamoeba histolytica ','3',30,'3',NULL,NULL,NULL),(323,100,'parasite','Kystes de Giardia lamblia','4',40,'4',NULL,NULL,NULL),(324,100,'parasite','Trichomonas intestinalis','5',50,'5',NULL,NULL,NULL),(325,100,'parasite','Trichomonas intestinalis et  kystes d\'Entamoeba coli','6',60,'6',NULL,NULL,NULL),(326,100,'abondance','Pauvre','1',10,'1',NULL,NULL,NULL),(327,100,'abondance','Peu adondante','2',20,'2',NULL,NULL,NULL),(328,100,'abondance','Abondante','3',30,'3',NULL,NULL,NULL),(329,100,'abondance','Très abondante','4',40,'4',NULL,NULL,NULL),(330,100,'bacterie','Négative','1',10,'1',NULL,NULL,NULL),(331,100,'bacterie','Absente','2',20,'2',NULL,NULL,NULL),(332,100,'bacterie','Non identifié','3',30,'3',NULL,NULL,NULL),(333,100,'bacterie','Escherichia coli','e_coli',40,'e_coli',NULL,NULL,NULL),(334,100,'bacterie','Staphylococcus sp','5',50,'5',NULL,NULL,NULL),(335,100,'bacterie','Staphylococcus aureus','6',60,'6',NULL,NULL,NULL),(336,100,'bacterie','Neisseria meningitidis','7',70,'7',NULL,NULL,NULL),(337,100,'bacterie','Neisseria meningitidis A','8',80,'8',NULL,NULL,NULL),(338,100,'bacterie','Neisseria meningitidis B','9',90,'9',NULL,NULL,NULL),(339,100,'bacterie','Neisseria meningitidis C','10',100,'10',NULL,NULL,NULL),(340,100,'bacterie','Neisseria meningitidis W135','11',110,'11',NULL,NULL,NULL),(341,100,'bacterie','Neisseria meningitidis X','12',120,'12',NULL,NULL,NULL),(342,100,'bacterie','Neisseria meningitidis Y','13',130,'13',NULL,NULL,NULL),(343,100,'bacterie','Haemophilus influenzae','14',140,'14',NULL,NULL,NULL),(344,100,'bacterie','Haemophilus influenzae b','15',150,'15',NULL,NULL,NULL),(345,100,'bacterie','Souillure','16',160,'16',NULL,NULL,NULL),(346,100,'bacterie','Enterobacter sp','17',170,'17',NULL,NULL,NULL),(347,100,'bacterie','Klebsiella pneumoniae','18',180,'18',NULL,NULL,NULL),(348,100,'bacterie','Enterobacter aerogenes','19',190,'19',NULL,NULL,NULL),(349,100,'bacterie','Enterobacter cloacae','20',200,'20',NULL,NULL,NULL),(350,100,'bacterie','Salmonella Typhi','21',210,'21',NULL,NULL,NULL),(351,100,'bacterie','Salmonella Paratyphi A','22',220,'22',NULL,NULL,NULL),(352,100,'bacterie','Salmonella Paratyphi B','23',230,'23',NULL,NULL,NULL),(353,100,'bacterie','Salmonella Paratyphi C','24',240,'24',NULL,NULL,NULL),(354,100,'bacterie','Shigella dysenteriae','25',250,'25',NULL,NULL,NULL),(355,100,'bacterie','Shigella sonnei','26',260,'26',NULL,NULL,NULL),(356,100,'bacterie','Shigella flexneri','27',270,'27',NULL,NULL,NULL),(357,100,'bacterie','Shigella sp','28',280,'28',NULL,NULL,NULL),(358,100,'bacterie','Streptococcus pneumoniae','29',290,'29',NULL,NULL,NULL),(359,100,'bacterie','Citrobacter freundii','30',300,'30',NULL,NULL,NULL),(360,100,'bacterie','Streptocoque du groupe D','31',310,'31',NULL,NULL,NULL),(361,100,'bacterie','Haemophilus parainfluenzae','32',320,'32',NULL,NULL,NULL),(362,100,'bacterie','Candida albicans','33',330,'33',NULL,NULL,NULL),(363,100,'bacterie','Gardnerella vaginalis','34',340,'34',NULL,NULL,NULL),(364,100,'bacterie','Mobilincus sp','35',350,'35',NULL,NULL,NULL),(365,100,'bacterie','Candida sp','36',360,'36',NULL,NULL,NULL),(366,100,'bacterie','Streptocoque du groupe B','37',370,'37',NULL,NULL,NULL),(367,100,'bacterie','Streptocoque du groupe C','38',380,'38',NULL,NULL,NULL),(368,100,'bacterie','Streptocoque du groupe A','39',390,'39',NULL,NULL,NULL),(369,100,'bacterie','Streptocoque du groupe F','40',400,'40',NULL,NULL,NULL),(370,100,'bacterie','Streptocoque du groupe G','41',410,'41',NULL,NULL,NULL),(371,100,'bacterie','Enterococcus sp','42',420,'42',NULL,NULL,NULL),(372,100,'bacterie','Enterococcus feacalis','43',430,'43',NULL,NULL,NULL),(373,100,'bacterie','Staphylococcus saprophyticus','44',440,'44',NULL,NULL,NULL),(374,100,'bacterie','Acinetobacter baumannii','45',450,'45',NULL,NULL,NULL),(375,100,'bacterie','Staphylococcus epidermidis','46',460,'46',NULL,NULL,NULL),(376,100,'bacterie','Streptococcus sp','47',470,'47',NULL,NULL,NULL),(377,100,'bacterie','Salmonella sp','48',480,'48',NULL,NULL,NULL),(378,100,'bacterie','Providencia stuartii','49',490,'49',NULL,NULL,NULL),(379,100,'bacterie','Stenotrophomonas maltophilia','50',500,'50',NULL,NULL,NULL),(380,100,'bacterie','Pseudomonas sp','51',510,'51',NULL,NULL,NULL),(381,100,'bacterie','Proteus vulgaris','52',520,'52',NULL,NULL,NULL),(382,100,'bacterie','Proteus mirabilis','53',530,'53',NULL,NULL,NULL),(383,100,'bouillon','Positif','1',10,'1',NULL,NULL,NULL),(384,100,'bouillon','Négatif','2',20,'2',NULL,NULL,NULL),(385,100,'bouillon','Hémolysé','3',30,'3',NULL,NULL,NULL),(386,100,'bouillon','Trouble','4',40,'4',NULL,NULL,NULL),(387,100,'bouillon','légèrement Hémolysé','5',50,'5',NULL,NULL,NULL),(388,100,'bouillon','légèrement trouble','6',60,'6',NULL,NULL,NULL),(389,100,'urine','urines troubles','1',10,'1',NULL,NULL,NULL),(390,100,'urine','urines claires','2',20,'2',NULL,NULL,NULL),(391,100,'urine','urines légèrement troubles','3',30,'3',NULL,NULL,NULL),(392,100,'urine','urines troubles avec dépôts','4',40,'4',NULL,NULL,NULL),(393,100,'urine','urines foncées limpides','5',50,'5',NULL,NULL,NULL),(394,100,'urine','urines foncées troubles','6',60,'6',NULL,NULL,NULL),(395,100,'urine','urines jaune claires, limpides','7',70,'7',NULL,NULL,NULL),(396,100,'urine','urines jaune foncées, limpides','8',80,'8',NULL,NULL,NULL),(397,100,'urine','urines jaune foncées, troubles','9',90,'9',NULL,NULL,NULL),(398,100,'urine','urines jaune foncées, troubles avec un dépôt blanchâtre','10',100,'10',NULL,NULL,NULL),(399,100,'urine','urines hématiques','11',110,'11',NULL,NULL,NULL),(400,100,'urine','urines purulentes','12',120,'12',NULL,NULL,NULL),(401,100,'urine','urines jaune pailles, limpides avec suspension','13',130,'13',NULL,NULL,NULL),(402,100,'urine','urines jaune foncées, troubles legèrement','14',140,'14',NULL,NULL,NULL),(403,100,'levure','rares','1',10,'1',NULL,NULL,NULL),(404,100,'levure','quelques','2',20,'2',NULL,NULL,NULL),(405,100,'levure','nombreuses','3',30,'3',NULL,NULL,NULL),(406,100,'levure','très nombreuses','4',40,'4',NULL,NULL,NULL),(407,100,'levure','rares, filamentées','5',50,'5',NULL,NULL,NULL),(408,100,'levure','quelques, filamentées','6',60,'6',NULL,NULL,NULL),(409,100,'levure','nombreuses, filamentées','7',70,'7',NULL,NULL,NULL),(410,100,'levure','très nombreuses,filamentées','8',80,'8',NULL,NULL,NULL),(411,100,'cristaux','phosphates amorphes (rares)','1',10,'1',NULL,NULL,NULL),(412,100,'cristaux','phosphates amorphes (quelques)','2',20,'2',NULL,NULL,NULL),(413,100,'cristaux','phosphates amorphes (nombreux)','3',30,'3',NULL,NULL,NULL),(414,100,'cristaux','phosphates amorphes (très nombreux)','4',40,'4',NULL,NULL,NULL),(415,100,'cristaux','urates amorphes (rares)','5',50,'5',NULL,NULL,NULL),(416,100,'cristaux','urates amorphes (quelques)','6',60,'6',NULL,NULL,NULL),(417,100,'cristaux','urates amorphes (nombreux)','7',70,'7',NULL,NULL,NULL),(418,100,'cristaux','urates amorphes (très nombreux)','8',80,'8',NULL,NULL,NULL),(419,100,'cristaux','oxalate de calcium (rares)','9',90,'9',NULL,NULL,NULL),(420,100,'cristaux','oxalate de calcium (quelques)','10',100,'10',NULL,NULL,NULL),(421,100,'cristaux','oxalate de calcium (nombreux)','11',110,'11',NULL,NULL,NULL),(422,100,'cristaux','oxalate de calcium (très nombreux)','12',120,'12',NULL,NULL,NULL),(423,100,'cristaux','acide urique  (rares)','13',130,'13',NULL,NULL,NULL),(424,100,'cristaux','acide urique  (quelques)','14',140,'14',NULL,NULL,NULL),(425,100,'cristaux','acide urique  (nombreux)','15',150,'15',NULL,NULL,NULL),(426,100,'cristaux','acide urique  (très nombreux)','16',160,'16',NULL,NULL,NULL),(427,100,'cristaux','urates (rares)','17',170,'17',NULL,NULL,NULL),(428,100,'cristaux','urates (quelques)','18',180,'18',NULL,NULL,NULL),(429,100,'cristaux','urates (nombreux)','19',190,'19',NULL,NULL,NULL),(430,100,'cristaux','urates  (très nombreux)','20',200,'20',NULL,NULL,NULL),(431,100,'cristaux','phosphates triples (rares)','21',210,'21',NULL,NULL,NULL),(432,100,'cristaux','phosphates triples (quelques)','22',220,'22',NULL,NULL,NULL),(433,100,'cristaux','phosphates triples (nombreux)','23',230,'23',NULL,NULL,NULL),(434,100,'cristaux','phosphates triples (très nombreux)','24',240,'24',NULL,NULL,NULL),(435,100,'cristaux','phosphate bicalcique (rares)','25',250,'25',NULL,NULL,NULL),(436,100,'cristaux','phosphate bicalcique (quelques)','26',260,'26',NULL,NULL,NULL),(437,100,'cristaux','phosphate bicalcique (nombreux)','27',270,'27',NULL,NULL,NULL),(438,100,'cristaux','phosphate bicalcique (très nombreux)','28',280,'28',NULL,NULL,NULL),(439,100,'cristaux','carbonate de calcium (rares)','29',290,'29',NULL,NULL,NULL),(440,100,'cristaux','carbonate de calcium (quelques)','30',300,'30',NULL,NULL,NULL),(441,100,'cristaux','carbonate de calcium (nombreux)','31',310,'31',NULL,NULL,NULL),(442,100,'cristaux','carbonate de calcium (très nombreux)','32',320,'32',NULL,NULL,NULL),(443,100,'cristaux','sulfate de calcium (rares)','33',330,'33',NULL,NULL,NULL),(444,100,'cristaux','sulfate de calcium (quelques)','34',340,'34',NULL,NULL,NULL),(445,100,'cristaux','sulfate de calcium (nombreux)','35',350,'35',NULL,NULL,NULL),(446,100,'cristaux','sulfate de calcium (très nombreux)','36',360,'36',NULL,NULL,NULL),(447,100,'cristaux','cystine (rares)','37',370,'37',NULL,NULL,NULL),(448,100,'cristaux','cystine (quelques)','38',380,'38',NULL,NULL,NULL),(449,100,'cristaux','cystine (nombreux)','39',390,'39',NULL,NULL,NULL),(450,100,'cristaux','cystine (très nombreux)','40',400,'40',NULL,NULL,NULL),(451,100,'cristaux','cholestérol (rares)','41',410,'41',NULL,NULL,NULL),(452,100,'cristaux','cholestérol (quelques)','42',420,'42',NULL,NULL,NULL),(453,100,'cristaux','cholestérol (nombreux)','43',430,'43',NULL,NULL,NULL),(454,100,'cristaux','cholestérol (très nombreux)','44',440,'44',NULL,NULL,NULL),(455,100,'cristaux','bilirubine (rares)','45',450,'45',NULL,NULL,NULL),(456,100,'cristaux','bilirubine (quelques)','46',460,'46',NULL,NULL,NULL),(457,100,'cristaux','bilirubine (nombreux)','47',470,'47',NULL,NULL,NULL),(458,100,'cristaux','bilirubine (très nombreux)','48',480,'48',NULL,NULL,NULL),(459,100,'cristaux','sulfamides (rares)','49',490,'49',NULL,NULL,NULL),(460,100,'cristaux','sulfamides (quelques)','50',500,'50',NULL,NULL,NULL),(461,100,'cristaux','sulfamides (nombreux)','51',510,'51',NULL,NULL,NULL),(462,100,'cristaux','sulfamides (très nombreux)','52',520,'52',NULL,NULL,NULL),(463,100,'cylindre','semi-granuleux (rares)','1',10,'1',NULL,NULL,NULL),(464,100,'cylindre','semi-granuleux (quelques)','2',20,'2',NULL,NULL,NULL),(465,100,'cylindre','semi-granuleux (nombreux)','3',30,'3',NULL,NULL,NULL),(466,100,'cylindre','semi-granuleux (très nombreux)','4',40,'4',NULL,NULL,NULL),(467,100,'cylindre','granuleux (rares)','5',50,'5',NULL,NULL,NULL),(468,100,'cylindre','granuleux (quelques)','6',60,'6',NULL,NULL,NULL),(469,100,'cylindre','granuleux (nombreux)','7',70,'7',NULL,NULL,NULL),(470,100,'cylindre','granuleux (très nombreux)','8',80,'8',NULL,NULL,NULL),(471,100,'cylindre','leucocytaires (rares)','9',90,'9',NULL,NULL,NULL),(472,100,'cylindre','leucocytaires (quelques)','10',100,'10',NULL,NULL,NULL),(473,100,'cylindre','leucocytaires (nombreux)','11',110,'11',NULL,NULL,NULL),(474,100,'cylindre','leucocytaires (très nombreux)','12',120,'12',NULL,NULL,NULL),(475,100,'cylindre','hématiques (rares)','13',130,'13',NULL,NULL,NULL),(476,100,'cylindre','hématiques (quelques)','14',140,'14',NULL,NULL,NULL),(477,100,'cylindre','hématiques (nombreux)','15',150,'15',NULL,NULL,NULL),(478,100,'cylindre','hématiques (très nombreux)','16',160,'16',NULL,NULL,NULL),(479,100,'cylindre','graisseux (rares)','17',170,'17',NULL,NULL,NULL),(480,100,'cylindre','graisseux (quelques)','18',180,'18',NULL,NULL,NULL),(481,100,'cylindre','graisseux (nombreux)','19',190,'19',NULL,NULL,NULL),(482,100,'cylindre','graisseux (très nombreux)','20',200,'20',NULL,NULL,NULL),(483,100,'cylindre','hyalins (rares)','21',210,'21',NULL,NULL,NULL),(484,100,'cylindre','hyalins (quelques)','22',220,'22',NULL,NULL,NULL),(485,100,'cylindre','hyalins (nombreux)','23',230,'23',NULL,NULL,NULL),(486,100,'cylindre','hyalins (très nombreux)','24',240,'24',NULL,NULL,NULL),(487,100,'cylindre','épithéliaux (rares)','25',250,'25',NULL,NULL,NULL),(488,100,'cylindre','épithéliaux (quelques)','26',260,'26',NULL,NULL,NULL),(489,100,'cylindre','épithéliaux (nombreux)','27',270,'27',NULL,NULL,NULL),(490,100,'cylindre','épithéliaux (très nombreux)','28',280,'28',NULL,NULL,NULL),(491,100,'flore','pauvre','1',10,'1',NULL,NULL,NULL),(492,100,'flore','peu abondante','2',20,'2',NULL,NULL,NULL),(493,100,'flore','abondante','3',30,'3',NULL,NULL,NULL),(494,100,'flore','très abondante','4',40,'4',NULL,NULL,NULL),(495,100,'gram','absence de germe visible','1',10,'1',NULL,NULL,NULL),(496,100,'gram','bacilles à Gram négatif','2',20,'2',NULL,NULL,NULL),(497,100,'gram','bacilles à Gram positif','3',30,'3',NULL,NULL,NULL),(498,100,'gram','rares bacilles à Gram négatif','4',40,'4',NULL,NULL,NULL),(499,100,'gram','bacilles à Gram négatif, bacilles à Gram positif','5',50,'5',NULL,NULL,NULL),(500,100,'gram','bacilles à Gram négatif, cocci à Gram positif','6',60,'6',NULL,NULL,NULL),(501,100,'gram','bacilles à Gram négatif, cocci à Gram positif, lévures','7',70,'7',NULL,NULL,NULL),(502,100,'gram','bacilles à Gram négatif, levures','8',80,'8',NULL,NULL,NULL),(503,100,'gram','bacilles à Gram négatif, bacilles à Gram positif, cocci à Gram positif','9',90,'9',NULL,NULL,NULL),(504,100,'gram','bacilles à Gram positif, cocci à Gram positif','10',100,'10',NULL,NULL,NULL),(505,100,'gram','bacilles à Gram négatif, bacilles à Gram positif, levures','11',110,'11',NULL,NULL,NULL),(506,100,'gram','bacilles à Gram positif, cocci à Gram positif, levures','12',120,'12',NULL,NULL,NULL),(507,100,'gram','bacilles à Gram négatif, bacilles à Gram positif, cocci à Gram positif, levures','13',130,'13',NULL,NULL,NULL),(508,100,'gram','cocci à Gram positif','14',140,'14',NULL,NULL,NULL),(509,100,'gram','rares cocci à Gram positif','15',150,'15',NULL,NULL,NULL),(510,100,'gram','rares cocci à Gram positif, lévures','16',160,'16',NULL,NULL,NULL),(511,100,'gram','cocci à Gram positif, levures','17',170,'17',NULL,NULL,NULL),(512,100,'gram','cocci à Gram positif, nombreuses levures','18',180,'18',NULL,NULL,NULL),(513,100,'gram','levures','19',190,'19',NULL,NULL,NULL),(514,100,'gram','diplocoque Gram positif','20',200,'20',NULL,NULL,NULL),(515,100,'gram','diplocoque Gram négatif','21',210,'21',NULL,NULL,NULL),(516,100,'res_cult','négative','1',10,'1',NULL,NULL,NULL),(517,100,'res_cult','positive','2',20,'2',NULL,NULL,NULL),(518,100,'res_cult','polymicrobienne (2 types de colonies)','3',30,'3',NULL,NULL,NULL),(519,100,'res_cult','polymicrobienne (3 types de colonies)','4',40,'4',NULL,NULL,NULL),(520,100,'res_cult','polymicrobienne (4 types de colonies)','5',50,'5',NULL,NULL,NULL),(521,100,'res_cult','polymicrobienne (5 types de colonies)','6',60,'6',NULL,NULL,NULL),(522,100,'res_cult','polymicrobienne (6 types de colonies)','7',70,'7',NULL,NULL,NULL),(523,100,'res_cult','polymicrobienne (7 types de colonies)','8',80,'8',NULL,NULL,NULL),(524,100,'resist_sensible','Résistant','R',10,'R',NULL,NULL,NULL),(525,100,'resist_sensible','Intermédiaire','I',20,'I',NULL,NULL,NULL),(526,100,'resist_sensible','Sensible','S',30,'S',NULL,NULL,NULL),(527,100,'lcr','Clair','1',10,'1',NULL,NULL,NULL),(528,100,'lcr','Louche','2',20,'2',NULL,NULL,NULL),(529,100,'lcr','Trouble','3',30,'3',NULL,NULL,NULL),(530,100,'lcr','Purulent','4',40,'4',NULL,NULL,NULL),(531,100,'lcr','Xantochromique','5',50,'5',NULL,NULL,NULL),(532,100,'lcr','Hématique','6',60,'6',NULL,NULL,NULL),(533,100,'lcr','Citrin','7',70,'7',NULL,NULL,NULL),(534,100,'lcr','Hialin','8',80,'8',NULL,NULL,NULL),(535,100,'lcr','Hématique surnageant clair','9',90,'9',NULL,NULL,NULL),(536,100,'lcr','Hématique surnageant citrin','10',100,'10',NULL,NULL,NULL),(537,100,'latex','Streptocoque B','1',10,'1',NULL,NULL,NULL),(538,100,'latex','Autoagglutination','2',20,'2',NULL,NULL,NULL),(539,100,'latex','Polyagglutination','3',30,'3',NULL,NULL,NULL),(540,100,'latex','Non faite','4',40,'4',NULL,NULL,NULL),(541,100,'latex','N.meningitidis A','5',50,'5',NULL,NULL,NULL),(542,100,'latex','N.meningitidis B','6',60,'6',NULL,NULL,NULL),(543,100,'latex','N.meningitidis C','7',70,'7',NULL,NULL,NULL),(544,100,'latex','N.meningitidis X','8',80,'8',NULL,NULL,NULL),(545,100,'latex','N.meningitidis Y','9',90,'9',NULL,NULL,NULL),(546,100,'latex','N.meningitidis W135','10',100,'10',NULL,NULL,NULL),(547,100,'latex','Négative','11',110,'11',NULL,NULL,NULL),(548,100,'latex','Streptococcus pneumoniae','12',120,'12',NULL,NULL,NULL),(549,100,'latex','Haemophilus influenzae b (Hib)','13',130,'13',NULL,NULL,NULL),(550,100,'aspestprelgen','Absence de Leucorrhées','1',10,'1',NULL,NULL,NULL),(551,100,'aspestprelgen','Leucorrhées minimes','2',20,'2',NULL,NULL,NULL),(552,100,'aspestprelgen','Leucorrhées Abondantes','3',30,'3',NULL,NULL,NULL),(553,100,'aspestprelgen','Leucorrhées Abondantes épaisses','4',40,'4',NULL,NULL,NULL),(554,100,'aspestprelgen','Leucorrhées Abondantes fluides','5',50,'5',NULL,NULL,NULL),(555,100,'aspestprelgen','Leucorrhées cailloboteuses','6',60,'6',NULL,NULL,NULL),(556,100,'aspestprelgen','Leucorrhées cailloboteuses abondantes','7',70,'7',NULL,NULL,NULL),(557,100,'aspestprelgen','Leucorrhées d\'odeur fétide','8',80,'8',NULL,NULL,NULL),(558,100,'aspestprelgen','Leucorrhées peu abondantes','9',90,'9',NULL,NULL,NULL),(559,100,'aspestprelgen','Leucorrhées moussantes','10',100,'10',NULL,NULL,NULL),(560,100,'aspestprelgen','Leucorrhées moussantes abondantes','11',110,'11',NULL,NULL,NULL),(561,100,'aspestprelgen','Ecouvillonnage','12',120,'12',NULL,NULL,NULL),(562,100,'aspestprelgen','Leucorrhées peu abondantes liquides','13',130,'13',NULL,NULL,NULL),(563,100,'aspestprelgen','Leucorrhées peu abondantes épaisses','14',140,'14',NULL,NULL,NULL),(564,100,'formlevure','Filamenteuses','F',10,'F',NULL,NULL,NULL),(565,100,'formlevure','Bourgeonnantes','B',20,'B',NULL,NULL,NULL),(566,100,'gram2','Lactobacillus','1',10,'1',NULL,NULL,NULL),(567,100,'gram2','Lactobacillus, Cocci à Gram +','2',20,'2',NULL,NULL,NULL),(568,100,'gram2','Lactobacillus, Cocci à Gram -','3',30,'3',NULL,NULL,NULL),(569,100,'gram2','Lactobacillus, Bacilles à Gram -','4',40,'4',NULL,NULL,NULL),(570,100,'gram2','Lactobacillus, Gardnerella vaginalis','5',50,'5',NULL,NULL,NULL),(571,100,'gram2','Lactobacillus, Gardnerella vaginalis, Mobilincus sp','6',60,'6',NULL,NULL,NULL),(572,100,'gram2','Gardnerella vaginalis, Mobilincus sp','7',70,'7',NULL,NULL,NULL),(573,100,'gram2','Gardnerella vaginalis','8',80,'8',NULL,NULL,NULL),(574,100,'gram2',' Mobilincus sp','9',90,'9',NULL,NULL,NULL),(575,100,'gram2','Cocci à Gram +','10',100,'10',NULL,NULL,NULL),(576,100,'gram2','Bacilles à Gram -','11',110,'11',NULL,NULL,NULL),(577,100,'type_i_iv','I','1',10,'1',NULL,NULL,NULL),(578,100,'type_i_iv','II','2',20,'2',NULL,NULL,NULL),(579,100,'type_i_iv','III','3',30,'3',NULL,NULL,NULL),(580,100,'type_i_iv','IV','4',40,'4',NULL,NULL,NULL),(583,100,'type_resultat','Abondance','dico_abondance',90,'D_ABOND',NULL,NULL,NULL),(584,100,'type_resultat','Aspect selles','dico_aspestselles',100,'D_ASP_SEL',NULL,NULL,NULL),(585,100,'type_resultat','Aspect prélélèvement génital','dico_aspestprelgen',110,'D_ASP_PREL',NULL,NULL,NULL),(586,100,'type_resultat','Bactérie','dico_bacterie',120,'D_BACT',NULL,NULL,NULL),(587,100,'type_resultat','Bouillon','dico_bouillon',130,'D_BOUIL',NULL,NULL,NULL),(588,100,'type_resultat','Cristaux','dico_cristaux',140,'D_CRIST',NULL,NULL,NULL),(589,100,'type_resultat','Cylindre','dico_cylindre',150,'D_CYL',NULL,NULL,NULL),(590,100,'type_resultat','Flore','dico_flore',160,'dico_flore',NULL,NULL,NULL),(591,100,'type_resultat','Forme levure','dico_formlevure',170,'D_F_LEVURE',NULL,NULL,NULL),(592,100,'type_resultat','Germe','dico_germe',180,'dico_germe',NULL,NULL,NULL),(593,100,'type_resultat','Gram','dico_gram',190,'dico_gram',NULL,NULL,NULL),(594,100,'type_resultat','Gram (2)','dico_gram2',190,'dico_gram2',NULL,NULL,NULL),(595,100,'type_resultat','Latex','dico_latex',200,'dico_latex',NULL,NULL,NULL),(596,100,'type_resultat','LCR','dico_lcr',210,'dico_lcr',NULL,NULL,NULL),(597,100,'type_resultat','Levure','dico_levure',220,'D_LEVURE',NULL,NULL,NULL),(598,100,'type_resultat','Urine','dico_urine',230,'dico_urine',NULL,NULL,NULL),(599,100,'type_resultat','Néant à Très nombreux','dico_nombre',240,'D_NOMBRE',NULL,NULL,NULL),(600,100,'type_resultat','Résistant / Sensible','dico_resist_sensible',250,'D_R_S',NULL,NULL,NULL),(601,100,'type_resultat','I / II / III / IV','dico_type_i_iv',260,'D_I_IV',NULL,NULL,NULL),(602,100,'type_resultat','Parasite','dico_parasite',270,'D_PARAS',NULL,NULL,NULL),(603,100,'type_resultat','Résultat culture','dico_res_cult',280,'D_RES_C',NULL,NULL,NULL),(604,100,'unite_valeur','ml','ml',70,'ml',NULL,NULL,NULL),(605,100,'levurelcr','Absence de levures','1',10,'1',NULL,NULL,NULL),(606,100,'levurelcr','Candida albicans','2',20,'2',NULL,NULL,NULL),(607,100,'levurelcr','Cryptococcus neoformans','3',30,'3',NULL,NULL,NULL),(608,100,'levurelcr','Candida sp','4',40,'4',NULL,NULL,NULL),(609,100,'type_resultat','Levure (présence)','dico_levurelcr',290,'D_LEV_PRES',NULL,NULL,NULL),(610,100,'baar','Négatif','-',10,'-',NULL,NULL,NULL),(611,100,'baar','+','+',20,'+',NULL,NULL,NULL),(612,100,'baar','++','++',30,'++',NULL,NULL,NULL),(613,100,'baar','+++','+++',40,'+++',NULL,NULL,NULL),(614,100,'type_resultat','Baar','dico_baar',115,'dico_baar',NULL,NULL,NULL),(615,100,'especepalu','Pl. falciparum','pl_falc',10,'pl_falc',NULL,NULL,NULL),(616,100,'especepalu','Autres plasmodies','autres',999,'autres',NULL,NULL,NULL),(617,100,'type_resultat','Espece palu','dico_especepalu',30,'D_ESP_PALU',NULL,NULL,NULL),(618,100,'bacterie','Escherichia coli O157 H7','e_coli_o157_h7',45,'D_E_COLI',NULL,NULL,NULL),(619,100,'bacterie','Vibrio Cholerae','v_chol',540,'v_chol',NULL,NULL,NULL),(620,100,'vih','Négatif','neg',10,'neg',NULL,NULL,NULL),(621,100,'vih','Positif','vih1',20,'vih1',NULL,NULL,NULL),(622,100,'vih','VIH-2 positif','vih2',30,'vih2',NULL,NULL,NULL),(623,100,'vih','VIH-1 et VIH-2 positifs','vih1-vih2',40,'vih1-vih2',NULL,NULL,NULL),(624,100,'vih','Indéterminé ','ind',50,'ind',NULL,NULL,NULL),(625,100,'type_resultat','VIH','dico_vih',300,'dico_vih',NULL,NULL,NULL),(626,100,'unite_valeur','UI/m3','UI/m3',157,'UI/m3',NULL,NULL,NULL),(627,100,'techpcr','Microscopie','Microscopie',10,'MICROSC',NULL,NULL,NULL),(628,100,'techpcr','Latex','Latex',20,'Latex',NULL,NULL,NULL),(629,100,'techpcr','Culture','Culture',30,'Culture',NULL,NULL,NULL),(630,100,'techpcr','PCR','PCR',40,'PCR',NULL,NULL,NULL),(631,100,'type_resultat','Technique PCR','dico_techpcr',290,'D_T_PCR',NULL,NULL,NULL),(632,100,'posnegind','Positif','Positif',10,'Positif',NULL,NULL,NULL),(633,100,'posnegind','Négatif','Négatif',20,'Négatif',NULL,NULL,NULL),(635,100,'type_resultat','Positif/Négatif/Indéterminé','dico_posnegind',65,'POS_NEG_IN',NULL,NULL,NULL),(636,100,'shisto','S.haematobium','S.haematobium',10,'S_HAEMA',NULL,NULL,NULL),(637,100,'shisto','autres','autres',20,'autres',NULL,NULL,NULL),(638,100,'shisto2','S.mansoni','S.mansoni',10,'S.mansoni',NULL,NULL,NULL),(639,100,'shisto2','autres','autres',20,'autres',NULL,NULL,NULL),(640,100,'filariose','W.bancrofti','W.bancrofti',10,'wb',NULL,NULL,NULL),(641,100,'filariose','autres','autres',20,'autres',NULL,NULL,NULL),(642,100,'type_resultat','Shisto','dico_shisto',300,'D_SHISTO',NULL,NULL,NULL),(643,100,'type_resultat','Shisto2','dico_shisto2',310,'D_SHISTO2',NULL,NULL,NULL),(644,100,'type_resultat','Filariose','dico_filariose',320,'D_FILAR',NULL,NULL,NULL),(645,100,'germe','Néant','10',10,'10',NULL,NULL,NULL),(646,100,'germe','Absente','20',20,'20',NULL,NULL,NULL),(647,100,'germe','Non identifié','30',30,'30',NULL,NULL,NULL),(648,100,'germe','Escherichia coli','40',40,'40',NULL,NULL,NULL),(649,100,'germe','Staphylococcus sp','50',50,'50',NULL,NULL,NULL),(650,100,'germe','Staphylococcus aureus','60',60,'60',NULL,NULL,NULL),(651,100,'germe','Neisseria meningitidis','70',70,'70',NULL,NULL,NULL),(652,100,'germe','Neisseria meningitidis A','80',80,'80',NULL,NULL,NULL),(653,100,'germe','Neisseria meningitidis B','90',90,'90',NULL,NULL,NULL),(654,100,'germe','Neisseria meningitidis C','100',100,'100',NULL,NULL,NULL),(655,100,'germe','Neisseria meningitidis W135','110',110,'110',NULL,NULL,NULL),(656,100,'germe','Neisseria meningitidis X','120',120,'120',NULL,NULL,NULL),(657,100,'germe','Neisseria meningitidis Y','130',130,'130',NULL,NULL,NULL),(658,100,'germe','Haemophilus influenzae','140',140,'140',NULL,NULL,NULL),(659,100,'germe','Haemophilus influenzae b','150',150,'150',NULL,NULL,NULL),(660,100,'germe','Souillure','160',160,'160',NULL,NULL,NULL),(661,100,'germe','Enterobacter sp','170',170,'170',NULL,NULL,NULL),(662,100,'germe','Klebsiella pneumoniae','180',180,'180',NULL,NULL,NULL),(663,100,'germe','Enterobacter aerogenes','190',190,'190',NULL,NULL,NULL),(664,100,'germe','Enterobacter cloacae','200',200,'200',NULL,NULL,NULL),(665,100,'germe','Salmonella Typhi','210',210,'210',NULL,NULL,NULL),(666,100,'germe','Salmonella Paratyphi A','220',220,'220',NULL,NULL,NULL),(667,100,'germe','Salmonella Paratyphi B','230',230,'230',NULL,NULL,NULL),(668,100,'germe','Salmonella Paratyphi C','240',240,'240',NULL,NULL,NULL),(669,100,'germe','Shigella dysenteriae','250',250,'250',NULL,NULL,NULL),(670,100,'germe','Shigella sonnei','260',260,'260',NULL,NULL,NULL),(671,100,'germe','Shigella flexneri','270',270,'270',NULL,NULL,NULL),(672,100,'germe','Shigella boydii','280',280,'280',NULL,NULL,NULL),(673,100,'germe','Streptococcus pneumoniae','290',290,'290',NULL,NULL,NULL),(674,100,'germe','Citrobacter freundii','300',300,'300',NULL,NULL,NULL),(675,100,'germe','Streptocoque du groupe D','310',310,'310',NULL,NULL,NULL),(676,100,'germe','Haemophilus parainfluenzae','320',320,'320',NULL,NULL,NULL),(677,100,'germe','Candida albicans','330',330,'330',NULL,NULL,NULL),(678,100,'germe','Gardnerella vaginalis','340',340,'340',NULL,NULL,NULL),(679,100,'germe','Mobilincus sp','350',350,'350',NULL,NULL,NULL),(680,100,'germe','Candida sp','360',360,'360',NULL,NULL,NULL),(681,100,'germe','Streptocoque du groupe B','370',370,'370',NULL,NULL,NULL),(682,100,'germe','Streptocoque du groupe C','380',380,'380',NULL,NULL,NULL),(683,100,'germe','Streptocoque du groupe A','390',390,'390',NULL,NULL,NULL),(684,100,'germe','Streptocoque du groupe F','400',400,'400',NULL,NULL,NULL),(685,100,'germe','Streptocoque du groupe G','410',410,'410',NULL,NULL,NULL),(686,100,'germe','Enterococcus sp','420',420,'420',NULL,NULL,NULL),(687,100,'germe','Enterococcus feacalis','430',430,'430',NULL,NULL,NULL),(688,100,'germe','Identification en cours','999',999,'999',NULL,NULL,NULL),(689,100,'germe','Staphylococcus saprophyticus','440',440,'440',NULL,NULL,NULL),(690,100,'germe','Acinetobacter baumannii','450',450,'450',NULL,NULL,NULL),(691,100,'germe','Staphylococcus epidermidis','460',460,'460',NULL,NULL,NULL),(692,100,'germe','Streptococcus sp','470',470,'470',NULL,NULL,NULL),(693,100,'germe','Salmonella sp','480',480,'480',NULL,NULL,NULL),(694,100,'germe','Providencia stuartii','490',490,'490',NULL,NULL,NULL),(695,100,'germe','Stenotrophomonas maltophilia','500',500,'500',NULL,NULL,NULL),(696,100,'germe','Pseudomonas aeruginosa','510',510,'510',NULL,NULL,NULL),(697,100,'germe','Proteus vulgaris','520',520,'520',NULL,NULL,NULL),(698,100,'germe','Proteus mirabilis','530',530,'530',NULL,NULL,NULL),(699,100,'bacterie','Neisseria gonorrhoeae','n_gono',545,'n_gono',NULL,NULL,NULL),(800,100,'unite_valeur','parasites/µl','parasites/µl',300,'PARAS/UL',NULL,NULL,NULL),(801,100,'unite_valeur','µg/dl','µg/dl',310,'µg/dl',NULL,NULL,NULL),(802,100,'gram2','Diplocoque Gram négatif intra cellulaire','12',320,'12',NULL,NULL,NULL),(803,100,'gram2','Diplocoque Gram négatif extra cellulaire','13',330,'13',NULL,NULL,NULL),(804,100,'gram2','Diplocoque Gram négatif intra et extra cellulaire','14',340,'14',NULL,NULL,NULL),(805,100,'gram2','Absence de germe','15',350,'15',NULL,NULL,NULL),(806,100,'gram2','Levure','16',360,'16',NULL,NULL,NULL),(807,100,'gram2','Autre','17',370,'17',NULL,NULL,NULL),(808,100,'type_resultat','Aspect prélèvement urétral','dico_aspprelur',115,'D_ASP_URT',NULL,NULL,NULL),(809,100,'aspprelur','Ecouvillonnage','1',10,'1',NULL,NULL,NULL),(810,100,'aspprelur','Absence d\'écoulement','2',20,'2',NULL,NULL,NULL),(811,100,'aspprelur','Ecoulement purulent','3',30,'3',NULL,NULL,NULL),(812,100,'aspprelur','Ecoulement incolore','4',40,'4',NULL,NULL,NULL),(813,100,'aspprelur','Ecoulement sanglant','5',50,'5',NULL,NULL,NULL),(814,100,'especepalu','Ovalé','ovale',20,'ovale',NULL,NULL,NULL),(815,100,'especepalu','Vivax','vivax',30,'vivax',NULL,NULL,NULL),(816,100,'especepalu','Malariae','malariae',40,'malariae',NULL,NULL,NULL),(817,100,'especepalu','Knowlesi','knowlesi',50,'knowlesi',NULL,NULL,NULL),(900,100,'type_resultat','Groupe sanguin','dico_groupesang',330,'D_GPE_SANG',NULL,NULL,NULL),(901,100,'groupesang','A','A',10,'A',NULL,NULL,NULL),(902,100,'groupesang','B','B',20,'B',NULL,NULL,NULL),(903,100,'groupesang','AB','AB',30,'AB',NULL,NULL,NULL),(904,100,'groupesang','O','O',40,'O',NULL,NULL,NULL),(1000,100,'type_prel','Prélèvement génital','Genital',1345,'Genital',NULL,NULL,NULL),(1001,100,'famille_analyse','Hématologie','HEMA',43,'HEMA',NULL,NULL,NULL),(1002,100,'famille_analyse','Hémostase','HEMO',47,'HEMO',NULL,NULL,NULL),(1003,100,'famille_analyse','Immunologie','IMNO',72,'IMNO',NULL,NULL,NULL),(1004,100,'unite_valeur','/ml','/ml',320,'/ml',NULL,NULL,NULL),(1005,100,'levure','Absence ','0',5,'0',NULL,NULL,NULL),(1006,100,'specialite','Chirurgien orthopédiste','Chirurgien ortho',410,'CHIR_ORTHO',NULL,NULL,NULL),(1007,100,'specialite','Infirmier/Infirmière','Infirmier/Infirmière',420,'INFIRM',NULL,NULL,NULL),(1008,100,'specialite','Sage femme','Sage femme',430,'Sage femme',NULL,NULL,NULL),(1009,100,'specialite','Pneumologue','Pneumologue',440,'PNEUMO',NULL,NULL,NULL),(1010,100,'specialite','Médecine interne','Médecine interne',450,'MED_INT',NULL,NULL,NULL),(1011,1010,'cylindre','Pas de cylindres','29',290,'29',NULL,NULL,NULL),(1012,1010,'type_resultat','Résistant/Sensible/Non applicable','RSNA',350,'RSNA',NULL,NULL,NULL),(1013,1010,'resist_sensible','Non effectué','NE',40,'NE',NULL,NULL,NULL),(1014,1010,'type_prel','Eau potable','EAU',150,'EAU',NULL,NULL,NULL),(1015,1010,'type_prel','Eau usée','EAUU',NULL,'EAUU',NULL,NULL,NULL),(1016,1010,'type_prel','Eau de surface','EAUS',NULL,'EAUS',NULL,NULL,NULL),(1017,1010,'unite_valeur','CFU','CFU',350,'CFU',NULL,NULL,NULL),(1018,1010,'famille_analyse','Antibiotique','ATB',170,'ATB',NULL,NULL,NULL),(1019,1010,'Prelv_sanitR','Food','Food',1,'Food',NULL,NULL,NULL),(1020,1009,'microscopie_tb','Négatif','-',10,'-',NULL,NULL,NULL),(1021,1009,'microscopie_tb','Scanty 1','Scanty 1',20,'Scanty 1',NULL,NULL,NULL),(1022,1009,'microscopie_tb','Scanty 2','Scanty 2',30,'Scanty 2',NULL,NULL,NULL),(1023,1009,'microscopie_tb','Scanty 3','Scanty 3',40,'Scanty 3',NULL,NULL,NULL),(1024,1009,'microscopie_tb','Scanty 4','Scanty 4',50,'Scanty 4',NULL,NULL,NULL),(1025,1009,'microscopie_tb','Scanty 5','Scanty 5',60,'Scanty 5',NULL,NULL,NULL),(1026,1009,'microscopie_tb','Scanty 6','Scanty 6',70,'Scanty 6',NULL,NULL,NULL),(1027,1009,'microscopie_tb','Scanty 7','Scanty 7',80,'Scanty 7',NULL,NULL,NULL),(1028,1009,'microscopie_tb','Scanty 8','Scanty 8',90,'Scanty 8',NULL,NULL,NULL),(1029,1009,'microscopie_tb','Scanty 9','Scanty 9',100,'Scanty 9',NULL,NULL,NULL),(1030,1009,'microscopie_tb','Positif +','+',110,'+',NULL,NULL,NULL),(1031,1009,'microscopie_tb','Positif ++','++',120,'++',NULL,NULL,NULL),(1032,1009,'microscopie_tb','Positif +++','+++',130,'+++',NULL,NULL,NULL),(1033,1010,'type_resultat','microscopie TB','dico_microscopie_tb',360,'D_M_TB',NULL,NULL,NULL),(1034,100,'periode_unite','Jours','jours',NULL,'jours',NULL,NULL,NULL),(1035,100,'periode_unite','Semaines','semaines',NULL,'semaines',NULL,NULL,NULL),(1036,100,'periode_unite','Mois','mois',NULL,'mois',NULL,NULL,NULL),(1037,100,'periode_unite','Années','annees',NULL,'annees',NULL,NULL,NULL),(1038,0,'sections','Administration','Administration',1,'0','ndjnyeytph1485176734016','uzowdgfnrn1485176791594',0),(1039,0,'sections','Prélèvement','Prélèvement',2,'1','ndjnyeytph1485176734016','ujhqxmihaj1485176791594',0),(1040,0,'sections','Biochimie','Biochimie',3,'2','ndjnyeytph1485176734016','ahadqmysfk1485176791594',0),(1041,0,'sections','Hématologie','Hématologie',4,'3','ndjnyeytph1485176734016','obzrnqglxs1485176791594',0),(1042,0,'sections','Sérologie','Sérologie',5,'4','ndjnyeytph1485176734016','xcmmsttjdq1485176791594',0),(1043,0,'sections','Microbiologie','Microbiologie',6,'5','ndjnyeytph1485176734016','oxqhgxdbsr1485176791594',0),(1044,0,'type_reu','Réunion d’équipe','Réunion d’équipe',1,'staff','veabwchhdm1485189275163','abvxesdftg1485189334220',0),(1045,0,'type_reu','Réunion qualité','Réunion qualité',2,'qlt','veabwchhdm1485189275163','eiisnpwxux1485189334220',0),(1046,0,'type_reu','Réunion de direction','Réunion de direction',3,'dir','veabwchhdm1485189275163','qmokpahpkr1485189334220',0),(1047,NULL,'oui','Oui','Oui',1,'1','osutsiwcyx1485356912133','xwptmvphyl1485356922359',0),(1049,NULL,'editeur_yorn','Oui','Oui',1,'1','qgzeaqsxho1485365824603','mwlpnirdgz1485365847726',0),(1051,NULL,'editeur_yorn','Non','Non',2,'0','qgzeaqsxho1485365824603','xbewsptiff1485365847726',0),(1053,NULL,'impact_patient','faible','faible',1,'1','gxmhexoill1485365992466','bflesommjq1485366031221',0),(1055,NULL,'impact_patient','important','important',2,'2','gxmhexoill1485365992466','bepttlkpbh1485366031221',0),(1057,NULL,'impact_patient','grave','grave',3,'3','gxmhexoill1485365992466','huyvkjzytf1485366031221',0),(1059,NULL,'periode_ctrl','Non','Non',1,'0','nberwqopkf1485768649608','abthalqsqy1485768659146',0),(1061,NULL,'periode_ctrl','Journalière','Journalière',2,'1','nberwqopkf1485768649608','etzuldcddr1485768659146',0),(1063,NULL,'periode_ctrl','Hebdomadère','Hebdomadère',3,'2','nberwqopkf1485768649608','dxybkelnmt1485768660936',0),(1065,NULL,'periode_ctrl','Mensuelle','Mensuelle',4,'3','nberwqopkf1485768649608','wxhxlkyagg1485768679839',0),(1067,NULL,'periode_ctrl','Annuelle','Annuelle',5,'4','nberwqopkf1485768649608','tdniinjejh1485768687873',0),(1068,NULL,'type_cr','Complet','Complet',1,'1','jxaqjodgah1492161179097','nnmcyhidfz1492161511031',0),(1069,NULL,'type_cr','Simple','Simple',2,'2','jxaqjodgah1492161179097','rrloxjgjfi1492161511031',0),(1070,NULL,'per_num_dos','Mois','Mois',1,'mois','mnbbvollaq1492177619188','sprjwnimfg1492177657075',0),(1071,NULL,'per_num_dos','Année','Année',2,'annee','mnbbvollaq1492177619188','pztbuhwxrd1492177657075',0),(1072,NULL,'court_long','Court','Court',1,'court','astkgyaecd1492177620456','cxlmpoeebx1492177804697',0),(1073,NULL,'court_long','Long','Long',2,'long','astkgyaecd1492177620456','rgeannqyut1492177804698',0),(1074,100,'doc_type','Code bar','CB',30,'CB',NULL,NULL,NULL),(1075,100,'posneg','Indeterminé','EQUI',30,'EQUI',NULL,NULL,NULL),(1076,100,'aspestselles','molles ','molles ',110,'molles ',NULL,NULL,NULL),(1077,100,'parasite','Négative ','Neg',70,'Neg',NULL,NULL,NULL),(1078,100,'parasite','Oeufs d\'Ascaris ','Ascaris',80,'Ascaris',NULL,NULL,NULL),(1079,100,'parasite','Oeufs d\'oxyure','Oxyure ',90,'Oxyure ',NULL,NULL,NULL),(1080,100,'parasite','Kystes d\'Entamoeba hartmanii','E. hartmanii',100,'E. hartman',NULL,NULL,NULL),(1081,100,'bacterie','Escherichia coli O157 H7','e_coli_o157_h7',45,'e_coli_o15',NULL,NULL,NULL),(1082,100,'bacterie','N.Gonorrhoae','N.Gonorrhoae',5,'N.Gonorrho',NULL,NULL,NULL),(1083,100,'bacterie','Campylobacter sp','Campylo',590,'Campylo',NULL,NULL,NULL),(1084,100,'bacterie','polymicrobienne (2 types de colonies)','polymicrobienne',NULL,'polymicrob',NULL,NULL,NULL),(1085,100,'bacterie','polymicrobienne ( 3 types de colonies) ','polymicrobienne',NULL,'polymicrob',NULL,NULL,NULL),(1086,100,'bacterie','polymicrobienne (plus de 3 types de colonies)','polymicrobienne',620,'polymicrob',NULL,NULL,NULL),(1087,100,'bacterie','Absence de germe pathogène','AGP',630,'AGP',NULL,NULL,NULL),(1088,100,'bacterie','en cours','en cours',640,'en cours',NULL,NULL,NULL),(1089,100,'bacterie','Staphylocoque coagulase négative ','SCN',650,'SCN',NULL,NULL,NULL),(1090,100,'bacterie','Corynebacterium sp','Corynebacterium sp',660,'Corynebact',NULL,NULL,NULL),(1091,100,'bacterie','Klebsiella sp','klebsiella sp',670,'klebsiella',NULL,NULL,NULL),(1092,100,'bacterie','Flore oropharynge','FOP',NULL,NULL,NULL,NULL,NULL),(1093,100,'bacterie','Flore de type cutane','FTC',NULL,NULL,NULL,NULL,NULL),(1094,100,'bacterie','Flore de type vaginal','FVAG',700,'',NULL,NULL,NULL),(1095,100,'urine','muqueuse ','muqueuse ',150,'muqueuse ',NULL,NULL,NULL),(1096,100,'urine','salivaire ','salivaire ',160,'salivaire ',NULL,NULL,NULL),(1097,100,'urine','muco- salivaire ','muco - salivaire ',170,'muco - sal',NULL,NULL,NULL),(1098,100,'urine','purulent ','purulent ',180,'purulent ',NULL,NULL,NULL),(1099,100,'urine','muco - purulent ','muco - purulent ',190,'muco - pur',NULL,NULL,NULL),(1100,100,'urine','muqueux strié de sang','muqueux ',200,'muqueux ',NULL,NULL,NULL),(1101,100,'urine','hemoptoique','HMP',210,'',NULL,NULL,NULL),(1102,100,'cristaux','absence','abs',5,'abs',NULL,NULL,NULL),(1103,100,'cristaux','non recherche','NR',540,'',NULL,NULL,NULL),(1104,100,'cylindre','absence ','absence ',300,'absence ',NULL,NULL,NULL),(1105,100,'flore','absente','absente',50,'absente',NULL,NULL,NULL),(1106,100,'gram','Cocci Gram positif en amas','CGP en amas',220,'CGP en ama',NULL,NULL,NULL),(1107,100,'gram','Cocci gram positif en chainettes, Cocci gram positif en amas','CGP en chainettes,',230,'CGP en cha',NULL,NULL,NULL),(1108,100,'gram','Cocci Gram positif en chainettes','CGP',240,'',NULL,NULL,NULL),(1109,100,'lcr','chyleux ','chyleux ',110,'chyleux ',NULL,NULL,NULL),(1110,100,'lcr','visqueux ','visqu',120,'visqu',NULL,NULL,NULL),(1111,100,'lcr','Légèrement trouble','Légèrement trouble',130,'Légèrement',NULL,NULL,NULL),(1112,100,'latex','Escherichia coli','ESCO',140,'ESCO',NULL,NULL,NULL),(1113,100,'baar','O','O',10,'O',NULL,NULL,NULL),(1114,100,'baar','Non recherche','NR',60,'',NULL,NULL,NULL),(1115,100,'especepalu','Néant','neant',5,'neant',NULL,NULL,NULL),(1116,100,'vih','Non réactif ','Non réactif ',60,'Non réacti',NULL,NULL,NULL),(1117,100,'vih','Réactif ','Réactif ',70,'Réactif ',NULL,NULL,NULL),(1118,100,'techpcr','meningocoque/Pneumocoque/Haemophilus influenzae typeb','Nm',NULL,NULL,NULL,NULL,NULL),(1119,100,'techpcr','Non realise','NR',60,'',NULL,NULL,NULL),(1120,100,'posnegind','Indéterminé','Indéterminé',30,'Indétermin',NULL,NULL,NULL),(1123,100,'équi_desequi','équilibrée','équi',1,'équi',NULL,NULL,NULL),(1124,100,'équi_desequi','desequilibrée','desequi',2,'desequi',NULL,NULL,NULL),(1125,100,'type_resultat','Positif / négatif','dico_posneg',60,'dico_posne',NULL,NULL,NULL),(1126,100,'type_resultat','Absent / Présent','dico_absent',80,'dico_absen',NULL,NULL,NULL),(1127,100,'type_resultat','Aspect prélélèvement génital','dico_aspestprelgen',110,'dico_aspes',NULL,NULL,NULL),(1128,100,'type_resultat','Bactérie','dico_bacterie',120,'dico_bacte',NULL,NULL,NULL),(1129,100,'type_resultat','Cristaux','dico_cristaux',140,'dico_crist',NULL,NULL,NULL),(1130,100,'type_resultat','Cylindre','dico_cylindre',150,'dico_cylin',NULL,NULL,NULL),(1131,100,'type_resultat','Forme levure','dico_formlevure',170,'dico_forml',NULL,NULL,NULL),(1132,100,'type_resultat','Levure','dico_levure',220,'dico_levur',NULL,NULL,NULL),(1133,100,'type_resultat','Néant à Très nombreux','dico_nombre',240,'dico_nombr',NULL,NULL,NULL),(1134,100,'type_resultat','Résistant / Sensible','dico_resist_sensible',250,'dico_resis',NULL,NULL,NULL),(1135,100,'type_resultat','Parasite','dico_parasite',270,'dico_paras',NULL,NULL,NULL),(1136,100,'type_resultat','Résultat culture','dico_res_cult',280,'dico_res_c',NULL,NULL,NULL),(1137,100,'type_resultat','Espece palu','dico_especepalu',30,'dico_espec',NULL,NULL,NULL),(1138,100,'type_resultat','Positif/Négatif/Indéterminé','dico_posnegind',65,'dico_posne',NULL,NULL,NULL),(1139,100,'type_resultat','Shisto','dico_shisto',300,'dico_shist',NULL,NULL,NULL),(1140,100,'type_resultat','Shisto2','dico_shisto2',310,'dico_shist',NULL,NULL,NULL),(1141,100,'type_resultat','Filariose','dico_filariose',320,'dico_filar',NULL,NULL,NULL),(1142,100,'type_resultat','équi/desequilibrée','dico_équi_desequi',175,'dico_équi_',NULL,NULL,NULL),(1143,100,'unite_valeur','million/mm3','million/mm3',260,'million/mm',NULL,NULL,NULL),(1144,100,'unite_valeur','G/l','G/l',370,'G/l',NULL,NULL,NULL),(1145,100,'unite_valeur','UFC/ml','UFC/ml',5,'UFC/ml',NULL,NULL,NULL),(1146,100,'unite_valeur','/mm3','/mm3',390,'/mm3',NULL,NULL,NULL),(1147,100,'product_type','Consommables','consommables',10,'consommabl',NULL,NULL,NULL),(1148,100,'product_type','Réactifs microbio','reactif_microbio',20,'reactif_mi',NULL,NULL,NULL),(1149,100,'product_type','Hygiène sécurité','hygiene',30,'hygiene',NULL,NULL,NULL),(1150,100,'product_type','Matériel de prélèvement','materiel_prel',40,'materiel_p',NULL,NULL,NULL),(1151,100,'product_type','Matériel microscopie','materiel_micro',50,'materiel_m',NULL,NULL,NULL),(1152,100,'product_status','Bon','bon',10,'bon',NULL,NULL,NULL),(1153,100,'product_status','Cassé','casse',20,'casse',NULL,NULL,NULL),(1154,100,'product_status','Périmé','perime',30,'perime',NULL,NULL,NULL),(1155,100,'product_conserv','Ambiante','ambiante',10,'ambiante',NULL,NULL,NULL),(1156,100,'product_conserv','2 - 8°C','frigo',20,'frigo',NULL,NULL,NULL),(1157,100,'product_conserv','-18°C','congel',30,'congel',NULL,NULL,NULL),(1158,100,'profil','Technicien avancé','tech_avance',22,'tech_avanc',NULL,NULL,NULL),(1159,100,'profil','Technicien qualiticien','tech_qualiticien',24,'tech_quali',NULL,NULL,NULL),(1160,100,'profil','Secretaire avancée','secr_avance',12,'secr_avanc',NULL,NULL,NULL),(1161,100,'profil','Qualiticien','qualiticien',14,'qualiticie',NULL,NULL,NULL),(1162,100,'profil','Prescripteur','prescripteur',16,'prescripte',NULL,NULL,NULL);
/*!40000 ALTER TABLE `sigl_dico_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dico_data_group`
--

DROP TABLE IF EXISTS `sigl_dico_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dico_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_dico_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=2644 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dico_data_group`
--

LOCK TABLES `sigl_dico_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_dico_data_group` DISABLE KEYS */;
INSERT INTO `sigl_dico_data_group` VALUES (2259,1,1000),(2260,2,1000),(2261,3,1000),(2443,4,1000),(2444,5,1000),(2058,6,1000),(2059,7,1000),(2235,8,1000),(2236,9,1000),(2237,10,1000),(2060,11,1000),(2061,12,1000),(2062,13,1000),(2063,15,1000),(2064,16,1000),(2065,17,1000),(2066,18,1000),(2067,19,1000),(2068,20,1000),(2069,23,1000),(2070,24,1000),(2071,25,1000),(2221,26,1000),(2222,27,1000),(2223,28,1000),(2333,34,1000),(2334,35,1000),(2335,38,1000),(2336,50,1000),(2337,56,1000),(2338,75,1000),(2339,99,1000),(2340,100,1000),(2341,102,1000),(2342,104,1000),(2343,138,1000),(2344,141,1000),(2345,152,1000),(2346,153,1000),(2347,162,1000),(2348,163,1000),(2323,170,1000),(2324,171,1000),(2306,173,1000),(2307,174,1000),(2238,175,1000),(2239,176,1000),(2240,177,1000),(2242,178,1000),(2243,179,1000),(2244,180,1000),(2308,181,1000),(2309,182,1000),(2327,183,1000),(2328,184,1000),(2266,186,1000),(2267,187,1000),(2269,189,1000),(2270,190,1000),(2272,192,1000),(2273,193,1000),(2274,194,1000),(2275,195,1000),(2276,196,1000),(2277,197,1000),(2278,198,1000),(2279,199,1000),(2280,200,1000),(2281,201,1000),(2282,202,1000),(2284,204,1000),(2285,205,1000),(2286,206,1000),(2287,207,1000),(2288,208,1000),(2289,209,1000),(2290,210,1000),(2291,211,1000),(2292,212,1000),(2293,213,1000),(2295,215,1000),(2296,216,1000),(2297,217,1000),(2299,219,1000),(2300,220,1000),(2301,221,1000),(2302,222,1000),(2305,225,1000),(2349,226,1000),(2350,227,1000),(2351,228,1000),(2352,229,1000),(2353,230,1000),(2354,231,1000),(2230,232,1000),(2231,233,1000),(2390,234,1000),(2391,235,1000),(2392,236,1000),(2393,237,1000),(2394,238,1000),(2395,239,1000),(2396,240,1000),(2397,241,1000),(2398,242,1000),(2399,243,1000),(2400,244,1000),(2401,245,1000),(2355,246,1000),(1883,247,1000),(1884,248,1000),(2402,249,1000),(2387,250,1000),(2388,251,1000),(2389,252,1000),(2310,253,1000),(2311,254,1000),(2312,255,1000),(2313,256,1000),(2054,257,1000),(2055,258,1000),(2080,259,1000),(2318,260,1000),(2319,261,1000),(2320,262,1000),(2321,263,1000),(2322,264,1000),(2356,265,1000),(2241,266,1000),(2245,267,1000),(2246,268,1000),(2247,269,1000),(2211,270,1000),(2212,271,1000),(2213,272,1000),(2214,273,1000),(2215,274,1000),(2208,275,1000),(2209,276,1000),(2210,277,1000),(2072,278,1000),(2073,279,1000),(2403,280,1000),(2404,281,1000),(2405,282,1000),(2406,283,1000),(2407,284,1000),(2408,285,1000),(2409,286,1000),(2410,287,1000),(2411,288,1000),(2412,289,1000),(2413,290,1000),(2414,291,1000),(2415,292,1000),(2416,293,1000),(2417,294,1000),(2418,295,1000),(2419,296,1000),(2420,297,1000),(2421,298,1000),(2325,299,1000),(2326,300,1000),(2074,301,1000),(2075,302,1000),(2076,303,1000),(2077,304,1000),(1899,305,1000),(1900,306,1000),(1901,307,1000),(1902,308,1000),(1903,309,1000),(1904,310,1000),(1905,311,1000),(1906,312,1000),(1907,313,1000),(1908,314,1000),(2216,315,1000),(2217,316,1000),(2218,317,1000),(2219,318,1000),(2220,319,1000),(2224,320,1000),(2225,321,1000),(2226,322,1000),(2227,323,1000),(2228,324,1000),(2229,325,1000),(1879,326,1000),(1880,327,1000),(1881,328,1000),(1882,329,1000),(1913,330,1000),(1914,331,1000),(1915,332,1000),(1916,333,1000),(1917,334,1000),(1918,335,1000),(1919,336,1000),(1920,337,1000),(1921,338,1000),(1922,339,1000),(1923,340,1000),(1924,341,1000),(1925,342,1000),(1926,343,1000),(1927,344,1000),(1928,345,1000),(1929,346,1000),(1930,347,1000),(1931,348,1000),(1932,349,1000),(1933,350,1000),(1934,351,1000),(1935,352,1000),(1936,353,1000),(1937,354,1000),(1938,355,1000),(1939,356,1000),(1940,357,1000),(1941,358,1000),(1942,359,1000),(1943,360,1000),(1944,361,1000),(1945,362,1000),(1946,363,1000),(1947,364,1000),(1948,365,1000),(1949,366,1000),(1950,367,1000),(1951,368,1000),(1952,369,1000),(1953,370,1000),(1954,371,1000),(1955,372,1000),(1956,373,1000),(1957,374,1000),(1958,375,1000),(1959,376,1000),(1960,377,1000),(1961,378,1000),(1962,379,1000),(1963,380,1000),(1964,381,1000),(1965,382,1000),(1968,383,1000),(1969,384,1000),(1970,385,1000),(1971,386,1000),(1972,387,1000),(1973,388,1000),(2424,389,1000),(2425,390,1000),(2426,391,1000),(2427,392,1000),(2428,393,1000),(2429,394,1000),(2430,395,1000),(2431,396,1000),(2432,397,1000),(2433,398,1000),(2434,399,1000),(2435,400,1000),(2436,401,1000),(2437,402,1000),(2196,403,1000),(2197,404,1000),(2198,405,1000),(2199,406,1000),(2200,407,1000),(2201,408,1000),(2202,409,1000),(2203,410,1000),(1974,411,1000),(1975,412,1000),(1976,413,1000),(1977,414,1000),(1978,415,1000),(1979,416,1000),(1980,417,1000),(1981,418,1000),(1982,419,1000),(1983,420,1000),(1984,421,1000),(1985,422,1000),(1986,423,1000),(1987,424,1000),(1988,425,1000),(1989,426,1000),(1990,427,1000),(1991,428,1000),(1992,429,1000),(1993,430,1000),(1994,431,1000),(1995,432,1000),(1996,433,1000),(1997,434,1000),(1998,435,1000),(1999,436,1000),(2000,437,1000),(2001,438,1000),(2002,439,1000),(2003,440,1000),(2004,441,1000),(2005,442,1000),(2006,443,1000),(2007,444,1000),(2008,445,1000),(2009,446,1000),(2010,447,1000),(2011,448,1000),(2012,449,1000),(2013,450,1000),(2014,451,1000),(2015,452,1000),(2016,453,1000),(2017,454,1000),(2018,455,1000),(2019,456,1000),(2020,457,1000),(2021,458,1000),(2022,459,1000),(2023,460,1000),(2024,461,1000),(2025,462,1000),(2026,463,1000),(2027,464,1000),(2028,465,1000),(2029,466,1000),(2030,467,1000),(2031,468,1000),(2032,469,1000),(2033,470,1000),(2034,471,1000),(2035,472,1000),(2036,473,1000),(2037,474,1000),(2038,475,1000),(2039,476,1000),(2040,477,1000),(2041,478,1000),(2042,479,1000),(2043,480,1000),(2044,481,1000),(2045,482,1000),(2046,483,1000),(2047,484,1000),(2048,485,1000),(2049,486,1000),(2050,487,1000),(2051,488,1000),(2052,489,1000),(2053,490,1000),(2081,491,1000),(2082,492,1000),(2083,493,1000),(2084,494,1000),(2141,495,1000),(2142,496,1000),(2143,497,1000),(2144,498,1000),(2145,499,1000),(2146,500,1000),(2147,501,1000),(2148,502,1000),(2149,503,1000),(2150,504,1000),(2151,505,1000),(2152,506,1000),(2153,507,1000),(2154,508,1000),(2155,509,1000),(2156,510,1000),(2157,511,1000),(2158,512,1000),(2159,513,1000),(2160,514,1000),(2161,515,1000),(2251,516,1000),(2252,517,1000),(2253,518,1000),(2254,519,1000),(2255,520,1000),(2256,521,1000),(2257,522,1000),(2258,523,1000),(2248,524,1000),(2249,525,1000),(2250,526,1000),(2186,527,1000),(2187,528,1000),(2188,529,1000),(2189,530,1000),(2190,531,1000),(2191,532,1000),(2192,533,1000),(2193,534,1000),(2194,535,1000),(2195,536,1000),(2173,537,1000),(2174,538,1000),(2175,539,1000),(2176,540,1000),(2177,541,1000),(2178,542,1000),(2179,543,1000),(2180,544,1000),(2181,545,1000),(2182,546,1000),(2183,547,1000),(2184,548,1000),(2185,549,1000),(1885,550,1000),(1886,551,1000),(1887,552,1000),(1888,553,1000),(1889,554,1000),(1890,555,1000),(1891,556,1000),(1892,557,1000),(1893,558,1000),(1894,559,1000),(1895,560,1000),(1896,561,1000),(1897,562,1000),(1898,563,1000),(2085,564,1000),(2086,565,1000),(2162,566,1000),(2163,567,1000),(2164,568,1000),(2165,569,1000),(2166,570,1000),(2167,571,1000),(2168,572,1000),(2169,573,1000),(2170,574,1000),(2171,575,1000),(2172,576,1000),(2329,577,1000),(2330,578,1000),(2331,579,1000),(2332,580,1000),(2357,583,1000),(2358,584,1000),(2359,585,1000),(2360,586,1000),(2361,587,1000),(2362,588,1000),(2363,589,1000),(2364,590,1000),(2365,591,1000),(2366,592,1000),(2367,593,1000),(2368,594,1000),(2369,595,1000),(2370,596,1000),(2371,597,1000),(2372,598,1000),(2373,599,1000),(2374,600,1000),(2375,601,1000),(2376,602,1000),(2377,603,1000),(2422,604,1000),(2204,605,1000),(2205,606,1000),(2206,607,1000),(2207,608,1000),(2378,609,1000),(1909,610,1000),(1910,611,1000),(1911,612,1000),(1912,613,1000),(2379,614,1000),(2056,615,1000),(2057,616,1000),(2380,617,1000),(1966,618,1000),(1967,619,1000),(2438,620,1000),(2439,621,1000),(2440,622,1000),(2441,623,1000),(2442,624,1000),(2381,625,1000),(2423,626,1000),(2314,627,1000),(2315,628,1000),(2316,629,1000),(2317,630,1000),(2382,631,1000),(2232,632,1000),(2233,633,1000),(2383,635,1000),(2262,636,1000),(2263,637,1000),(2264,638,1000),(2265,639,1000),(2643,640,1000),(2079,641,1000),(2384,642,1000),(2385,643,1000),(2386,644,1000),(2087,645,1000),(2088,646,1000),(2089,647,1000),(2090,648,1000),(2091,649,1000),(2092,650,1000),(2093,651,1000),(2094,652,1000),(2095,653,1000),(2096,654,1000),(2097,655,1000),(2098,656,1000),(2099,657,1000),(2100,658,1000),(2101,659,1000),(2102,660,1000),(2103,661,1000),(2104,662,1000),(2105,663,1000),(2106,664,1000),(2107,665,1000),(2108,666,1000),(2109,667,1000),(2110,668,1000),(2111,669,1000),(2112,670,1000),(2113,671,1000),(2114,672,1000),(2115,673,1000),(2116,674,1000),(2117,675,1000),(2118,676,1000),(2119,677,1000),(2120,678,1000),(2121,679,1000),(2122,680,1000),(2123,681,1000),(2124,682,1000),(2125,683,1000),(2126,684,1000),(2127,685,1000),(2128,686,1000),(2129,687,1000),(2130,688,1000),(2131,689,1000),(2132,690,1000),(2133,691,1000),(2134,692,1000),(2135,693,1000),(2136,694,1000),(2137,695,1000),(2138,696,1000),(2139,697,1000),(2140,698,1000),(2445,800,1000),(2446,801,1000),(2447,802,1000),(2448,803,1000),(2449,804,1000),(2450,805,1000),(2451,806,1000),(2452,807,1000),(2453,808,1000),(2454,809,1000),(2455,810,1000),(2456,811,1000),(2457,812,1000),(2458,813,1000),(2459,814,1000),(2460,815,1000),(2461,816,1000),(2462,817,1000),(2480,900,1000),(2481,901,1000),(2482,902,1000),(2483,903,1000),(2484,904,1000),(2500,1000,1000),(2501,1001,1000),(2502,1002,1000),(2503,1003,1000),(2504,1004,1000),(2505,1005,1000),(2506,1006,1000),(2507,1007,1000),(2508,1008,1000),(2509,1009,1000),(2510,1010,1000),(2511,1011,1000),(2512,1012,1000),(2513,1013,1000),(2514,1014,1000),(2515,1015,1000),(2516,1016,1000),(2517,1017,1000),(2518,1018,1000),(2519,1019,1000),(2520,1020,1000),(2521,1021,1000),(2522,1022,1000),(2523,1023,1000),(2524,1024,1000),(2525,1025,1000),(2526,1026,1000),(2527,1027,1000),(2528,1028,1000),(2529,1029,1000),(2530,1030,1000),(2531,1031,1000),(2532,1032,1000),(2533,1033,1000),(2535,1034,1000),(2537,1035,1000),(2539,1036,1000),(2541,1037,1000),(2543,1047,1000),(2545,1049,1000),(2547,1051,1000),(2549,1053,1000),(2551,1055,1000),(2553,1057,1000),(2555,1059,1000),(2557,1061,1000),(2559,1063,1000),(2561,1065,1000),(2563,1067,1000),(2564,1068,1000),(2565,1069,1000),(2566,1070,1000),(2567,1071,1000),(2568,1072,1000),(2569,1073,1000),(2570,1074,1000),(2571,1075,1000),(2572,1076,1000),(2573,1077,1000),(2574,1078,1000),(2575,1079,1000),(2576,1080,1000),(2577,1081,1000),(2578,1082,1000),(2579,1083,1000),(2580,1084,1000),(2581,1085,1000),(2582,1086,1000),(2583,1087,1000),(2584,1088,1000),(2585,1089,1000),(2586,1090,1000),(2587,1091,1000),(2588,1092,1000),(2589,1093,1000),(2590,1094,1000),(2591,1095,1000),(2592,1096,1000),(2593,1097,1000),(2594,1098,1000),(2595,1099,1000),(2596,1100,1000),(2597,1101,1000),(2598,1102,1000),(2599,1103,1000),(2600,1104,1000),(2601,1105,1000),(2602,1106,1000),(2603,1107,1000),(2604,1108,1000),(2605,1109,1000),(2606,1110,1000),(2607,1111,1000),(2608,1112,1000),(2609,1113,1000),(2610,1114,1000),(2611,1115,1000),(2612,1116,1000),(2613,1117,1000),(2614,1118,1000),(2615,1119,1000),(2616,1120,1000),(2619,1123,1000),(2620,1124,1000),(2621,1125,1000),(2622,1126,1000),(2623,1127,1000),(2624,1128,1000),(2625,1129,1000),(2626,1130,1000),(2627,1131,1000),(2628,1132,1000),(2629,1133,1000),(2630,1134,1000),(2631,1135,1000),(2632,1136,1000),(2633,1137,1000),(2634,1138,1000),(2635,1139,1000),(2636,1140,1000),(2637,1141,1000),(2638,1142,1000),(2639,1143,1000),(2640,1144,1000),(2641,1145,1000),(2642,1146,1000);
/*!40000 ALTER TABLE `sigl_dico_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dico_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_dico_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dico_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_dico_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dico_data_group_mode`
--

LOCK TABLES `sigl_dico_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_dico_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_dico_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dico_deleted`
--

DROP TABLE IF EXISTS `sigl_dico_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dico_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `dico_name` varchar(20) NOT NULL,
  `label` varchar(255) NOT NULL,
  `short_label` varchar(20) NOT NULL,
  `position` int(10) DEFAULT NULL,
  `code` varchar(10) DEFAULT NULL,
  `dico_id` varchar(40) DEFAULT NULL,
  `dico_value_id` varchar(40) DEFAULT NULL,
  `archived` int(1) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `idx_dico_name` (`dico_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1123 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dico_deleted`
--

LOCK TABLES `sigl_dico_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_dico_deleted` DISABLE KEYS */;
INSERT INTO `sigl_dico_deleted` VALUES (634,100,'posnegind','Indéterminé','Indéterminé',30,'INDETERM',NULL,NULL,NULL),(1121,100,'shisto','S.haematobium','S.haematobium',10,'S.haematob',NULL,NULL,NULL),(1122,100,'filariose','W.bancrofti','W.bancrofti',10,'W.bancroft',NULL,NULL,NULL);
/*!40000 ALTER TABLE `sigl_dico_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dicostatus_data`
--

DROP TABLE IF EXISTS `sigl_dicostatus_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dicostatus_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  `status` int(10) unsigned DEFAULT NULL,
  `effective_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dicostatus_data`
--

LOCK TABLES `sigl_dicostatus_data` WRITE;
/*!40000 ALTER TABLE `sigl_dicostatus_data` DISABLE KEYS */;
INSERT INTO `sigl_dicostatus_data` VALUES (1,100,'2017-12-20 16:37:09','2017-12-20 16:37:09',100,632,119,'2017-12-20 16:37:09'),(2,100,'2017-12-20 16:37:10','2017-12-20 16:37:10',100,633,119,'2017-12-20 16:37:10'),(3,100,'2017-12-20 16:37:10','2017-12-20 16:37:10',100,1120,119,'2017-12-20 16:37:10'),(4,100,'2017-12-20 17:04:44','2017-12-20 17:04:44',100,640,119,'2017-12-20 17:04:44'),(5,100,'2017-12-20 17:04:44','2017-12-20 17:04:44',100,641,119,'2017-12-20 17:04:44'),(6,100,'2017-12-20 22:52:57','2017-12-20 22:52:57',100,636,119,'2017-12-20 22:52:57'),(7,100,'2017-12-20 22:52:57','2017-12-20 22:52:57',100,637,119,'2017-12-20 22:52:57');
/*!40000 ALTER TABLE `sigl_dicostatus_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dicostatus_data_group`
--

DROP TABLE IF EXISTS `sigl_dicostatus_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dicostatus_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dicostatus_data_group`
--

LOCK TABLES `sigl_dicostatus_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_dicostatus_data_group` DISABLE KEYS */;
INSERT INTO `sigl_dicostatus_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000);
/*!40000 ALTER TABLE `sigl_dicostatus_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dicostatus_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_dicostatus_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dicostatus_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dicostatus_data_group_mode`
--

LOCK TABLES `sigl_dicostatus_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_dicostatus_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_dicostatus_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dicostatus_deleted`
--

DROP TABLE IF EXISTS `sigl_dicostatus_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dicostatus_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  `status` int(10) unsigned DEFAULT NULL,
  `effective_date` datetime DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dicostatus_deleted`
--

LOCK TABLES `sigl_dicostatus_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_dicostatus_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_dicostatus_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dos_valisedoc__file_data`
--

DROP TABLE IF EXISTS `sigl_dos_valisedoc__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dos_valisedoc__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dos_valisedoc__file_data`
--

LOCK TABLES `sigl_dos_valisedoc__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_dos_valisedoc__file_data` DISABLE KEYS */;
/* AlC DESACT 23/03/2021 INSERT INTO `sigl_dos_valisedoc__file_data` VALUES (1,1009,'2017-06-14 18:11:42','2017-06-14 18:11:42',1009,1,13); */
/*!40000 ALTER TABLE `sigl_dos_valisedoc__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dos_valisedoc__file_data_group`
--

DROP TABLE IF EXISTS `sigl_dos_valisedoc__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dos_valisedoc__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dos_valisedoc__file_data_group`
--

LOCK TABLES `sigl_dos_valisedoc__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_dos_valisedoc__file_data_group` DISABLE KEYS */;
INSERT INTO `sigl_dos_valisedoc__file_data_group` VALUES (1,1,1000);
/*!40000 ALTER TABLE `sigl_dos_valisedoc__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dos_valisedoc__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_dos_valisedoc__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dos_valisedoc__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dos_valisedoc__file_data_group_mode`
--

LOCK TABLES `sigl_dos_valisedoc__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_dos_valisedoc__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_dos_valisedoc__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_dos_valisedoc__file_deleted`
--

DROP TABLE IF EXISTS `sigl_dos_valisedoc__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_dos_valisedoc__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_dos_valisedoc__file_deleted`
--

LOCK TABLES `sigl_dos_valisedoc__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_dos_valisedoc__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_dos_valisedoc__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_certif_etalonnage__file_data`
--

DROP TABLE IF EXISTS `sigl_equipement_certif_etalonnage__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_certif_etalonnage__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_certif_etalonnage__file_data`
--

LOCK TABLES `sigl_equipement_certif_etalonnage__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_certif_etalonnage__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_certif_etalonnage__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_certif_etalonnage__file_data_group`
--

DROP TABLE IF EXISTS `sigl_equipement_certif_etalonnage__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_certif_etalonnage__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_certif_etalonnage__file_data_group`
--

LOCK TABLES `sigl_equipement_certif_etalonnage__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_certif_etalonnage__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_certif_etalonnage__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_certif_etalonnage__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_equipement_certif_etalonnage__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_certif_etalonnage__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_certif_etalonnage__file_data_group_mode`
--

LOCK TABLES `sigl_equipement_certif_etalonnage__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_certif_etalonnage__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_certif_etalonnage__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_certif_etalonnage__file_deleted`
--

DROP TABLE IF EXISTS `sigl_equipement_certif_etalonnage__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_certif_etalonnage__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_certif_etalonnage__file_deleted`
--

LOCK TABLES `sigl_equipement_certif_etalonnage__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_certif_etalonnage__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_certif_etalonnage__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_contrat_maintenance__file_data`
--

DROP TABLE IF EXISTS `sigl_equipement_contrat_maintenance__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_contrat_maintenance__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_contrat_maintenance__file_data`
--

LOCK TABLES `sigl_equipement_contrat_maintenance__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_contrat_maintenance__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_contrat_maintenance__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_contrat_maintenance__file_data_group`
--

DROP TABLE IF EXISTS `sigl_equipement_contrat_maintenance__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_contrat_maintenance__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_contrat_maintenance__file_data_group`
--

LOCK TABLES `sigl_equipement_contrat_maintenance__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_contrat_maintenance__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_contrat_maintenance__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_contrat_maintenance__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_equipement_contrat_maintenance__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_contrat_maintenance__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_contrat_maintenance__file_data_group_mode`
--

LOCK TABLES `sigl_equipement_contrat_maintenance__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_contrat_maintenance__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_contrat_maintenance__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_contrat_maintenance__file_deleted`
--

DROP TABLE IF EXISTS `sigl_equipement_contrat_maintenance__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_contrat_maintenance__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_contrat_maintenance__file_deleted`
--

LOCK TABLES `sigl_equipement_contrat_maintenance__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_contrat_maintenance__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_contrat_maintenance__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_data`
--

DROP TABLE IF EXISTS `sigl_equipement_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `nom_fabriquant` varchar(255) DEFAULT NULL,
  `modele` varchar(255) DEFAULT NULL,
  `fonction` varchar(255) DEFAULT NULL,
  `localisation` varchar(255) DEFAULT NULL,
  `section` int(10) unsigned DEFAULT NULL,
  `no_serie` varchar(255) DEFAULT NULL,
  `no_inventaire` varchar(255) DEFAULT NULL,
  `pannes` text,
  `maintenance_preventive` text,
  `certif_etalonnage` varchar(255) DEFAULT NULL,
  `contrat_maintenance` varchar(255) DEFAULT NULL,
  `date_fin_contrat` date DEFAULT NULL,
  `controle_interne` int(10) unsigned DEFAULT NULL,
  `controle_externe` int(10) unsigned DEFAULT NULL,
  `date_reception` date DEFAULT NULL,
  `date_mise_en_service` date DEFAULT NULL,
  `date_de_retrait` date DEFAULT NULL,
  `commentaires` text,
  `fournisseur_id` int(10) unsigned DEFAULT NULL,
  `responsable_id` int(10) unsigned DEFAULT NULL,
  `manuel_id` int(10) unsigned DEFAULT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `date_achat` date DEFAULT NULL,
  `date_acquisition` date DEFAULT NULL,
  `procedures_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_data`
--

LOCK TABLES `sigl_equipement_data` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_data_group`
--

DROP TABLE IF EXISTS `sigl_equipement_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_data_group`
--

LOCK TABLES `sigl_equipement_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_equipement_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_data_group_mode`
--

LOCK TABLES `sigl_equipement_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_deleted`
--

DROP TABLE IF EXISTS `sigl_equipement_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `nom_fabriquant` varchar(255) DEFAULT NULL,
  `modele` varchar(255) DEFAULT NULL,
  `fonction` varchar(255) DEFAULT NULL,
  `localisation` varchar(255) DEFAULT NULL,
  `section` int(10) unsigned DEFAULT NULL,
  `no_serie` varchar(255) DEFAULT NULL,
  `no_inventaire` varchar(255) DEFAULT NULL,
  `pannes` text,
  `maintenance_preventive` text,
  `certif_etalonnage` varchar(255) DEFAULT NULL,
  `contrat_maintenance` varchar(255) DEFAULT NULL,
  `date_fin_contrat` date DEFAULT NULL,
  `controle_interne` int(10) unsigned DEFAULT NULL,
  `controle_externe` int(10) unsigned DEFAULT NULL,
  `date_reception` date DEFAULT NULL,
  `date_mise_en_service` date DEFAULT NULL,
  `date_de_retrait` date DEFAULT NULL,
  `commentaires` text,
  `fournisseur_id` int(10) unsigned DEFAULT NULL,
  `responsable_id` int(10) unsigned DEFAULT NULL,
  `manuel_id` int(10) unsigned DEFAULT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `date_achat` date DEFAULT NULL,
  `date_acquisition` date DEFAULT NULL,
  `procedures_id` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_deleted`
--

LOCK TABLES `sigl_equipement_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_facture__file_data`
--

DROP TABLE IF EXISTS `sigl_equipement_facture__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_facture__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_facture__file_data`
--

LOCK TABLES `sigl_equipement_facture__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_facture__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_facture__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_facture__file_data_group`
--

DROP TABLE IF EXISTS `sigl_equipement_facture__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_facture__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_facture__file_data_group`
--

LOCK TABLES `sigl_equipement_facture__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_facture__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_facture__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_facture__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_equipement_facture__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_facture__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_facture__file_data_group_mode`
--

LOCK TABLES `sigl_equipement_facture__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_facture__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_facture__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_facture__file_deleted`
--

DROP TABLE IF EXISTS `sigl_equipement_facture__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_facture__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_facture__file_deleted`
--

LOCK TABLES `sigl_equipement_facture__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_facture__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_facture__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_maintenance_preventive__file_data`
--

DROP TABLE IF EXISTS `sigl_equipement_maintenance_preventive__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_maintenance_preventive__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_maintenance_preventive__file_data`
--

LOCK TABLES `sigl_equipement_maintenance_preventive__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_maintenance_preventive__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_maintenance_preventive__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_maintenance_preventive__file_data_group`
--

DROP TABLE IF EXISTS `sigl_equipement_maintenance_preventive__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_maintenance_preventive__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_maintenance_preventive__file_data_group`
--

LOCK TABLES `sigl_equipement_maintenance_preventive__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_maintenance_preventive__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_maintenance_preventive__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_maintenance_preventive__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_equipement_maintenance_preventive__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_maintenance_preventive__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_maintenance_preventive__file_data_group_mode`
--

LOCK TABLES `sigl_equipement_maintenance_preventive__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_maintenance_preventive__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_maintenance_preventive__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_maintenance_preventive__file_deleted`
--

DROP TABLE IF EXISTS `sigl_equipement_maintenance_preventive__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_maintenance_preventive__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_maintenance_preventive__file_deleted`
--

LOCK TABLES `sigl_equipement_maintenance_preventive__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_maintenance_preventive__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_maintenance_preventive__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_pannes__file_data`
--

DROP TABLE IF EXISTS `sigl_equipement_pannes__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_pannes__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_pannes__file_data`
--

LOCK TABLES `sigl_equipement_pannes__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_pannes__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_pannes__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_pannes__file_data_group`
--

DROP TABLE IF EXISTS `sigl_equipement_pannes__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_pannes__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_pannes__file_data_group`
--

LOCK TABLES `sigl_equipement_pannes__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_pannes__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_pannes__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_pannes__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_equipement_pannes__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_pannes__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_pannes__file_data_group_mode`
--

LOCK TABLES `sigl_equipement_pannes__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_pannes__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_pannes__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_pannes__file_deleted`
--

DROP TABLE IF EXISTS `sigl_equipement_pannes__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_pannes__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_pannes__file_deleted`
--

LOCK TABLES `sigl_equipement_pannes__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_pannes__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_pannes__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_photo__file_data`
--

DROP TABLE IF EXISTS `sigl_equipement_photo__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_photo__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_photo__file_data`
--

LOCK TABLES `sigl_equipement_photo__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_photo__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_photo__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_photo__file_data_group`
--

DROP TABLE IF EXISTS `sigl_equipement_photo__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_photo__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_photo__file_data_group`
--

LOCK TABLES `sigl_equipement_photo__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_photo__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_photo__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_photo__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_equipement_photo__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_photo__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_photo__file_data_group_mode`
--

LOCK TABLES `sigl_equipement_photo__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_photo__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_photo__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_equipement_photo__file_deleted`
--

DROP TABLE IF EXISTS `sigl_equipement_photo__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_equipement_photo__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_equipement_photo__file_deleted`
--

LOCK TABLES `sigl_equipement_photo__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_equipement_photo__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_equipement_photo__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_evtlog_data`
--

DROP TABLE IF EXISTS `sigl_evtlog_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_evtlog_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `evt_datetime` datetime DEFAULT NULL,
  `evt_type` int(10) unsigned DEFAULT NULL,
  `evt_name` varchar(255) DEFAULT NULL,
  `message` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB AUTO_INCREMENT=135 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_evtlog_data`
--

LOCK TABLES `sigl_evtlog_data` WRITE;
/*!40000 ALTER TABLE `sigl_evtlog_data` DISABLE KEYS */;
INSERT INTO `sigl_evtlog_data` VALUES (1,100,'2017-08-29 15:38:55',17,'VZN_EVT_CONNEXION','Core_Library_Controller_Auth_Index::_HandleAuthForm'),(2,100,'2017-08-29 15:50:51',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(3,100,'2017-08-29 15:51:17',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(4,100,'2017-08-29 15:51:26',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(5,100,'2017-08-29 15:51:31',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(6,100,'2017-08-29 16:07:09',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(7,100,'2017-08-29 16:28:05',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(8,100,'2017-08-29 16:37:59',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(9,100,'2017-08-29 16:38:29',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(10,100,'2017-08-29 16:39:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(11,100,'2017-08-29 16:42:14',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(12,100,'2017-10-13 18:03:06',17,'VZN_EVT_CONNEXION','Core_Library_Controller_Auth_Index::_HandleAuthForm'),(13,100,'2017-10-23 11:06:28',17,'VZN_EVT_CONNEXION','Core_Library_Controller_Auth_Index::_HandleAuthForm'),(14,100,'2017-10-23 11:10:27',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(15,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(16,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(17,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(18,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(19,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(20,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(21,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(22,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(23,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(24,100,'2017-10-23 11:10:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(25,100,'2017-10-23 11:10:29',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(26,100,'2017-10-23 11:10:29',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(27,100,'2017-10-23 11:10:29',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(28,100,'2017-10-23 11:10:29',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(29,100,'2017-10-23 11:12:39',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(30,100,'2017-10-23 11:12:39',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(31,100,'2017-10-23 11:12:39',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(32,100,'2017-10-23 11:12:39',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(33,100,'2017-10-23 11:12:39',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(34,100,'2017-10-23 11:12:39',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(35,100,'2017-10-23 11:12:39',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(36,100,'2017-10-23 11:12:39',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(37,100,'2017-10-23 11:12:40',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(38,100,'2017-10-23 11:12:40',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(39,100,'2017-10-23 11:12:40',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(40,100,'2017-10-23 11:12:40',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(41,100,'2017-10-23 11:12:40',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(42,100,'2017-12-19 18:56:00',17,'VZN_EVT_CONNEXION','Core_Library_Controller_Auth_Index::_HandleAuthForm'),(43,100,'2017-12-20 09:29:15',17,'VZN_EVT_CONNEXION','Core_Library_Controller_Auth_Index::_HandleAuthForm'),(44,100,'2017-12-20 16:32:21',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(45,100,'2017-12-20 16:32:35',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(46,100,'2017-12-20 16:37:03',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(47,100,'2017-12-20 16:37:09',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(48,100,'2017-12-20 16:37:10',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(49,100,'2017-12-20 16:37:10',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(50,100,'2017-12-20 17:00:00',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(51,100,'2017-12-20 17:00:53',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(52,100,'2017-12-20 17:01:27',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(53,100,'2017-12-20 17:01:28',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(54,100,'2017-12-20 17:04:17',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(55,100,'2017-12-20 17:04:43',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(56,100,'2017-12-20 17:04:44',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(57,100,'2017-12-20 17:04:44',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(58,100,'2017-12-20 17:10:03',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(59,100,'2017-12-20 17:10:20',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(60,100,'2017-12-20 17:10:20',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(61,100,'2017-12-20 17:24:05',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(62,100,'2017-12-20 17:25:45',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(63,100,'2017-12-20 17:26:36',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(64,100,'2017-12-20 17:27:39',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(65,100,'2017-12-20 18:14:45',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(66,100,'2017-12-20 18:15:55',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(67,100,'2017-12-20 18:16:41',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(68,100,'2017-12-20 18:17:06',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(69,100,'2017-12-20 18:40:19',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(70,100,'2017-12-20 18:40:28',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(71,100,'2017-12-20 18:40:29',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(72,100,'2017-12-20 18:53:05',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(73,100,'2017-12-20 18:54:17',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(74,100,'2017-12-20 18:54:50',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(75,100,'2017-12-20 19:17:23',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(76,100,'2017-12-20 19:17:35',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(77,100,'2017-12-20 19:25:17',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(78,100,'2017-12-20 19:25:23',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(79,100,'2017-12-20 19:25:58',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(80,100,'2017-12-20 19:26:07',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(81,100,'2017-12-20 19:27:10',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(82,100,'2017-12-20 19:29:21',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(83,100,'2017-12-20 21:50:06',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(84,100,'2017-12-20 21:50:12',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(85,100,'2017-12-20 22:01:16',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(86,100,'2017-12-20 22:01:21',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(87,100,'2017-12-20 22:01:22',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(88,100,'2017-12-20 22:01:22',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(89,100,'2017-12-20 22:02:23',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(90,100,'2017-12-20 22:11:01',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(91,100,'2017-12-20 22:13:16',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(92,100,'2017-12-20 22:13:24',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(93,100,'2017-12-20 22:13:35',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(94,100,'2017-12-20 22:13:35',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(95,100,'2017-12-20 22:16:14',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(96,100,'2017-12-20 22:16:14',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(97,100,'2017-12-20 22:16:15',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(98,100,'2017-12-20 22:16:15',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(99,100,'2017-12-20 22:16:37',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(100,100,'2017-12-20 22:16:42',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(101,100,'2017-12-20 22:16:54',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(102,100,'2017-12-20 22:16:54',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(103,100,'2017-12-20 22:22:08',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(104,100,'2017-12-20 22:22:15',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(105,100,'2017-12-20 22:22:38',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(106,100,'2017-12-20 22:22:39',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(107,100,'2017-12-20 22:22:39',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(108,100,'2017-12-20 22:22:39',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(109,100,'2017-12-20 22:22:39',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(110,100,'2017-12-20 22:23:11',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(111,100,'2017-12-20 22:23:16',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(112,100,'2017-12-20 22:23:21',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(113,100,'2017-12-20 22:23:30',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(114,100,'2017-12-20 22:24:14',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(115,100,'2017-12-20 22:28:23',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(116,100,'2017-12-20 22:44:24',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(117,100,'2017-12-20 22:45:32',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(118,100,'2017-12-20 22:45:49',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(119,100,'2017-12-20 22:45:49',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(120,100,'2017-12-20 22:49:47',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(121,100,'2017-12-20 22:50:28',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(122,100,'2017-12-20 22:51:02',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(123,100,'2017-12-20 22:51:02',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(124,100,'2017-12-20 22:52:54',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(125,100,'2017-12-20 22:52:57',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(126,100,'2017-12-20 22:52:57',14,'VZN_REC_INSERT','Core_Library_Resource_XML_VarSet::SimpleInsertData'),(127,100,'2017-12-20 22:59:15',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(128,100,'2017-12-20 22:59:21',16,'VZN_REC_DELETE','Core_Library_Resource_XML_VarSet::SimpleDeleteData'),(129,100,'2017-12-21 09:13:45',17,'VZN_EVT_CONNEXION','Core_Library_Controller_Auth_Index::_HandleAuthForm'),(130,NULL,'2019-04-02 11:33:42',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(131,NULL,'2019-04-02 11:33:43',15,'VZN_REC_UPDATE','Core_Library_Resource_XML_VarSet::SimpleUpdateData'),(132,100,'2020-03-06 09:29:03',17,'VZN_EVT_CONNEXION','Core_Library_Controller_Auth_Index::_HandleAuthForm'),(133,100,'2020-03-09 09:49:05',17,'VZN_EVT_CONNEXION','Core_Library_Controller_Auth_Index::_HandleAuthForm'),(134,100,'2020-06-03 11:34:56',17,'VZN_EVT_CONNEXION','Core_Library_Controller_Auth_Index::_HandleAuthForm');
/*!40000 ALTER TABLE `sigl_evtlog_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_evtlog_data_group`
--

DROP TABLE IF EXISTS `sigl_evtlog_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_evtlog_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(11) NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_query_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_evtlog_data_group`
--

LOCK TABLES `sigl_evtlog_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_evtlog_data_group` DISABLE KEYS */;
INSERT INTO `sigl_evtlog_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000),(8,8,1000),(9,9,1000),(10,10,1000),(11,11,1000),(12,12,1000),(13,13,1000),(14,14,1000),(15,15,1000),(16,16,1000),(17,17,1000),(18,18,1000),(19,19,1000),(20,20,1000),(21,21,1000),(22,22,1000),(23,23,1000),(24,24,1000),(25,25,1000),(26,26,1000),(27,27,1000),(28,28,1000),(29,29,1000),(30,30,1000),(31,31,1000),(32,32,1000),(33,33,1000),(34,34,1000),(35,35,1000),(36,36,1000),(37,37,1000),(38,38,1000),(39,39,1000),(40,40,1000),(41,41,1000),(42,42,1000),(43,43,1000),(44,44,1000),(45,45,1000),(46,46,1000),(47,47,1000),(48,48,1000),(49,49,1000),(50,50,1000),(51,51,1000),(52,52,1000),(53,53,1000),(54,54,1000),(55,55,1000),(56,56,1000),(57,57,1000),(58,58,1000),(59,59,1000),(60,60,1000),(61,61,1000),(62,62,1000),(63,63,1000),(64,64,1000),(65,65,1000),(66,66,1000),(67,67,1000),(68,68,1000),(69,69,1000),(70,70,1000),(71,71,1000),(72,72,1000),(73,73,1000),(74,74,1000),(75,75,1000),(76,76,1000),(77,77,1000),(78,78,1000),(79,79,1000),(80,80,1000),(81,81,1000),(82,82,1000),(83,83,1000),(84,84,1000),(85,85,1000),(86,86,1000),(87,87,1000),(88,88,1000),(89,89,1000),(90,90,1000),(91,91,1000),(92,92,1000),(93,93,1000),(94,94,1000),(95,95,1000),(96,96,1000),(97,97,1000),(98,98,1000),(99,99,1000),(100,100,1000),(101,101,1000),(102,102,1000),(103,103,1000),(104,104,1000),(105,105,1000),(106,106,1000),(107,107,1000),(108,108,1000),(109,109,1000),(110,110,1000),(111,111,1000),(112,112,1000),(113,113,1000),(114,114,1000),(115,115,1000),(116,116,1000),(117,117,1000),(118,118,1000),(119,119,1000),(120,120,1000),(121,121,1000),(122,122,1000),(123,123,1000),(124,124,1000),(125,125,1000),(126,126,1000),(127,127,1000),(128,128,1000),(129,129,1000),(130,132,1000),(131,133,1000),(132,134,1000);
/*!40000 ALTER TABLE `sigl_evtlog_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_evtlog_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_evtlog_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_evtlog_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_evtlog_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_evtlog_data_group_mode`
--

LOCK TABLES `sigl_evtlog_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_evtlog_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_evtlog_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_evtlog_deleted`
--

DROP TABLE IF EXISTS `sigl_evtlog_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_evtlog_deleted` (
  `id_data` int(11) NOT NULL,
  `id_owner` int(11) NOT NULL,
  `evt_datetime` datetime DEFAULT NULL,
  `evt_type` int(10) unsigned DEFAULT NULL,
  `evt_name` varchar(255) DEFAULT NULL,
  `message` varchar(255) DEFAULT NULL,
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_evtlog_deleted`
--

LOCK TABLES `sigl_evtlog_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_evtlog_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_evtlog_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_file_data`
--

DROP TABLE IF EXISTS `sigl_file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `date_creation` datetime DEFAULT NULL,
  `original_name` varchar(128) DEFAULT NULL,
  `generated_name` varchar(32) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `hash` varchar(32) DEFAULT NULL,
  `ext` varchar(8) DEFAULT NULL,
  `content_type` varchar(100) DEFAULT NULL,
  `id_storage` int(10) unsigned DEFAULT NULL,
  `path` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_file_data`
--

LOCK TABLES `sigl_file_data` WRITE;
/*!40000 ALTER TABLE `sigl_file_data` DISABLE KEYS */;
INSERT INTO `sigl_file_data` VALUES (1,100,'2017-04-21 12:10:29','2017-04-21 12:10:55',100,1,'2017-04-21 12:10:28','Systéme de gestion de la qualité au Laboratoire.pdf','a69fa918a5e8034f177666d6c4a55cf9',3947344,'3aedce75e45963cd42ab13d38e9c152b','pdf','application/pdf',1,'a6/9f/'),(2,100,'2017-04-21 12:12:03','2017-04-21 12:12:32',100,1,'2017-04-21 12:12:03','Laboratory Quality Management System.pdf','c3639f168cb57b598756cfa6afcf7e3e',6191879,'5459492907b860fb911d0a63de9fef74','pdf','application/pdf',1,'c3/63/'),(3,100,'2017-04-21 12:13:48','2017-04-21 12:14:07',100,1,'2017-04-21 12:13:48','Manuel d\'entretien et maintenance.pdf','8b3c07729c252dddc70ae954e9abcf29',2668523,'099db95d73257fabe46a474cd778b135','pdf','application/pdf',1,'8b/3c/'),(4,100,'2017-04-21 12:14:35','2017-04-21 12:14:55',100,1,'2017-04-21 12:14:35','Maintenance Manual.pdf','f5c89bc1e688413de27954552c85e815',2939236,'a0a83c74a49afbb601dbe9cc69b03c73','pdf','application/pdf',1,'f5/c8/'),(5,100,'2017-04-21 12:17:03','2017-04-21 12:17:25',100,1,'2017-04-21 12:17:02','Biosécurité OMS.pdf','2401ecd6403b0a970b276c2a6d600931',3623457,'bbb2036249243148c6670faa09a6ebec','pdf','application/pdf',1,'24/01/'),(7,100,'2017-04-21 12:22:23','2017-04-21 12:22:37',100,1,'2017-04-21 12:22:23','Biosafety WHO.pdf','1d950e5909c258dfa5ab74ad4cffdd44',4143909,'41fb6b53a131ceea554167171b8f0498','pdf','application/pdf',1,'1d/95/'),(9,100,'2017-04-21 12:34:54','2017-04-21 12:34:59',100,1,'2017-04-21 12:34:54','WHO Guidance on regulations for transport of infectious substances 2019-FR.pdf','31dddf91a9c9ecaf3795cd857ca8ba86',1169244,'c4eba2b5088578af224f9b4285b7564d','pdf','application/pdf',1,'31/dd/'),(10,100,'2017-04-21 12:35:18','2017-04-21 12:35:35',100,1,'2017-04-21 12:35:18','WHO Guidance on regulations for transport of infectious substances 2019.pdf','7233ecea9c818eeb303ca486f3ac780b',994915,'f580557c384b1698c2c51f2f08005b14','pdf','application/pdf',1,'72/33/'),(11,100,'2017-04-21 12:35:51','2017-04-21 12:36:12',100,1,'2017-04-21 12:35:51','EQA - WHO.pdf','0d1eadb6cb164ef792493a39d225f748',1386265,'5c2d3540e6ee45cbebabe6e0b157acac','pdf','application/pdf',1,'0d/1e/'),(12,100,'2020-06-03 11:33:37','2020-06-03 11:33:37',100,1,'2020-06-03 11:33:37','CASFM2020_Avril2020_V1.1.pdf','313a6ac28def417fc1dcd067a155012f',2476091,'76bbaf5c56f64a60b73a24d038cab4de','pdf','application/pdf',1,'31/3a/'),(13,100,'2020-06-03 11:37:08','2020-06-03 11:37:08',100,1,'2020-06-03 11:37:08','v_10.0_Breakpoint_Tables.pdf','83cba374ab42879dbbecd6051f26ea6d',3445398,'c051d0d23efcb6ec42d11b56f1d46e25','pdf','application/pdf',1,'83/cb/');
/*!40000 ALTER TABLE `sigl_file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_file_data_group`
--

DROP TABLE IF EXISTS `sigl_file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_file_data_group`
--

LOCK TABLES `sigl_file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_file_data_group` DISABLE KEYS */;
INSERT INTO `sigl_file_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(7,7,1000),(9,9,1000),(10,10,1000),(11,11,1000),(12,12,1000),(13,13,1000);
/*!40000 ALTER TABLE `sigl_file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_file_data_group_mode`
--

LOCK TABLES `sigl_file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_file_deleted`
--

DROP TABLE IF EXISTS `sigl_file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `date_creation` datetime DEFAULT NULL,
  `original_name` varchar(128) DEFAULT NULL,
  `generated_name` varchar(32) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `hash` varchar(32) DEFAULT NULL,
  `ext` varchar(8) DEFAULT NULL,
  `content_type` varchar(100) DEFAULT NULL,
  `id_storage` int(10) unsigned DEFAULT NULL,
  `path` varchar(6) DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_file_deleted`
--

LOCK TABLES `sigl_file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_fournisseurs_data`
--

DROP TABLE IF EXISTS `sigl_fournisseurs_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_fournisseurs_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `fournisseur_nom` varchar(255) DEFAULT NULL,
  `contact_nom` varchar(255) DEFAULT NULL,
  `contact_prenom` varchar(255) DEFAULT NULL,
  `contact_fonction` varchar(255) DEFAULT NULL,
  `fournisseur_adresse` text,
  `contact_tel` varchar(255) DEFAULT NULL,
  `contact_mobile` varchar(255) DEFAULT NULL,
  `contact_fax` varchar(255) DEFAULT NULL,
  `contact_email` varchar(255) DEFAULT NULL,
  `commentaire` text,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_fournisseurs_data`
--

LOCK TABLES `sigl_fournisseurs_data` WRITE;
/*!40000 ALTER TABLE `sigl_fournisseurs_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_fournisseurs_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_fournisseurs_data_group`
--

DROP TABLE IF EXISTS `sigl_fournisseurs_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_fournisseurs_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_fournisseurs_data_group`
--

LOCK TABLES `sigl_fournisseurs_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_fournisseurs_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_fournisseurs_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_fournisseurs_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_fournisseurs_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_fournisseurs_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_fournisseurs_data_group_mode`
--

LOCK TABLES `sigl_fournisseurs_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_fournisseurs_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_fournisseurs_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_fournisseurs_deleted`
--

DROP TABLE IF EXISTS `sigl_fournisseurs_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_fournisseurs_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `fournisseur_nom` varchar(255) DEFAULT NULL,
  `contact_nom` varchar(255) DEFAULT NULL,
  `contact_prenom` varchar(255) DEFAULT NULL,
  `contact_fonction` varchar(255) DEFAULT NULL,
  `fournisseur_adresse` text,
  `contact_tel` varchar(255) DEFAULT NULL,
  `contact_mobile` varchar(255) DEFAULT NULL,
  `contact_fax` varchar(255) DEFAULT NULL,
  `contact_email` varchar(255) DEFAULT NULL,
  `commentaire` text,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_fournisseurs_deleted`
--

LOCK TABLES `sigl_fournisseurs_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_fournisseurs_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_fournisseurs_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_laboratoire_data`
--

DROP TABLE IF EXISTS `sigl_laboratoire_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_laboratoire_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_laboratoire_data`
--

LOCK TABLES `sigl_laboratoire_data` WRITE;
/*!40000 ALTER TABLE `sigl_laboratoire_data` DISABLE KEYS */;
INSERT INTO `sigl_laboratoire_data` VALUES (1,100,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sigl_laboratoire_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_laboratoire_data_group`
--

DROP TABLE IF EXISTS `sigl_laboratoire_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_laboratoire_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_laboratoire_data_group`
--

LOCK TABLES `sigl_laboratoire_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_laboratoire_data_group` DISABLE KEYS */;
INSERT INTO `sigl_laboratoire_data_group` VALUES (1,1,1000);
/*!40000 ALTER TABLE `sigl_laboratoire_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_laboratoire_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_laboratoire_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_laboratoire_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_laboratoire_data_group_mode`
--

LOCK TABLES `sigl_laboratoire_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_laboratoire_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_laboratoire_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_laboratoire_deleted`
--

DROP TABLE IF EXISTS `sigl_laboratoire_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_laboratoire_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_laboratoire_deleted`
--

LOCK TABLES `sigl_laboratoire_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_laboratoire_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_laboratoire_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_laboratoire_organigramme__file_data`
--

DROP TABLE IF EXISTS `sigl_laboratoire_organigramme__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_laboratoire_organigramme__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_laboratoire_organigramme__file_data`
--

LOCK TABLES `sigl_laboratoire_organigramme__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_laboratoire_organigramme__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_laboratoire_organigramme__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_laboratoire_organigramme__file_data_group`
--

DROP TABLE IF EXISTS `sigl_laboratoire_organigramme__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_laboratoire_organigramme__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_laboratoire_organigramme__file_data_group`
--

LOCK TABLES `sigl_laboratoire_organigramme__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_laboratoire_organigramme__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_laboratoire_organigramme__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_laboratoire_organigramme__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_laboratoire_organigramme__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_laboratoire_organigramme__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_laboratoire_organigramme__file_data_group_mode`
--

LOCK TABLES `sigl_laboratoire_organigramme__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_laboratoire_organigramme__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_laboratoire_organigramme__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_laboratoire_organigramme__file_deleted`
--

DROP TABLE IF EXISTS `sigl_laboratoire_organigramme__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_laboratoire_organigramme__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_laboratoire_organigramme__file_deleted`
--

LOCK TABLES `sigl_laboratoire_organigramme__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_laboratoire_organigramme__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_laboratoire_organigramme__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_manuels_data`
--

DROP TABLE IF EXISTS `sigl_manuels_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_manuels_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `titre` varchar(255) DEFAULT NULL,
  `reference` varchar(255) DEFAULT NULL,
  `redacteur_id` int(10) unsigned DEFAULT NULL,
  `verificateur_id` int(10) unsigned DEFAULT NULL,
  `approbateur_id` int(10) unsigned DEFAULT NULL,
  `section` int(10) unsigned DEFAULT NULL,
  `date_update` date DEFAULT NULL,
  `date_apply` date DEFAULT NULL,
  `date_insert` date DEFAULT NULL,
  `date_revue` date DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_manuels_data`
--

LOCK TABLES `sigl_manuels_data` WRITE;
/*!40000 ALTER TABLE `sigl_manuels_data` DISABLE KEYS */;
INSERT INTO `sigl_manuels_data` VALUES (1,100,'2017-04-21 12:10:55','2017-04-21 12:10:55',100,'Systéme de gestion de la qualité au Laboratoire',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(2,100,'2017-04-21 12:12:32','2017-04-21 12:12:32',100,'Laboratory Quality Management System',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(3,100,'2017-04-21 12:14:07','2017-04-21 12:14:07',100,'Manuel d\'entretien et maintenance',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(4,100,'2017-04-21 12:14:55','2017-04-21 12:14:55',100,'Maintenance Manual',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(5,100,'2017-04-21 12:17:25','2017-04-21 12:17:25',100,'Biosécurité OMS',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(6,100,'2017-04-21 12:22:37','2017-04-21 12:22:37',100,'Biosafety WHO',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(7,100,'2017-04-21 12:34:59','2017-04-21 12:34:59',100,'Guide pratique sur l\'application du Reglement relatif au transport des matieres infectieuses 2019-2020',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(8,100,'2017-04-21 12:35:34','2017-04-21 12:35:34',100,'WHO Guidance on regulations for transport of infectious substances 2019',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(9,100,'2017-04-21 12:36:12','2017-06-15 18:58:29',1010,'EQA - WHO',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(10,100,'2020-06-03 11:34:17','2020-06-03 11:34:17',100,'Comite de l\'antibiogramme de la Societe Francaise de Microbiologie ; Recommandations 2020 ; V.1.1 Avril',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL),(11,100,'2020-06-03 11:37:20','2020-06-03 11:37:20',100,'The European Committee on Antimicrobial Susceptibility Testing. Breakpoint tables for interpretation of MICs and zone diameters. Version 10.0, 2020',NULL,1,1,1,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sigl_manuels_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_manuels_data_group`
--

DROP TABLE IF EXISTS `sigl_manuels_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_manuels_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_manuels_data_group`
--

LOCK TABLES `sigl_manuels_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_manuels_data_group` DISABLE KEYS */;
INSERT INTO `sigl_manuels_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000),(8,8,1000),(11,9,1000),(12,10,1000),(13,11,1000);
/*!40000 ALTER TABLE `sigl_manuels_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_manuels_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_manuels_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_manuels_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_manuels_data_group_mode`
--

LOCK TABLES `sigl_manuels_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_manuels_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_manuels_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_manuels_deleted`
--

DROP TABLE IF EXISTS `sigl_manuels_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_manuels_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `titre` varchar(255) DEFAULT NULL,
  `reference` varchar(255) DEFAULT NULL,
  `redacteur_id` int(10) unsigned DEFAULT NULL,
  `verificateur_id` int(10) unsigned DEFAULT NULL,
  `approbateur_id` int(10) unsigned DEFAULT NULL,
  `section` int(10) unsigned DEFAULT NULL,
  `date_update` date DEFAULT NULL,
  `date_apply` date DEFAULT NULL,
  `date_insert` date DEFAULT NULL,
  `date_revue` date DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_manuels_deleted`
--

LOCK TABLES `sigl_manuels_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_manuels_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_manuels_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_manuels_document__file_data`
--

DROP TABLE IF EXISTS `sigl_manuels_document__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_manuels_document__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_manuels_document__file_data`
--

LOCK TABLES `sigl_manuels_document__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_manuels_document__file_data` DISABLE KEYS */;
INSERT INTO `sigl_manuels_document__file_data` VALUES (1,100,'2017-04-21 12:10:56','2017-04-21 12:10:56',100,1,1),(2,100,'2017-04-21 12:12:32','2017-04-21 12:12:32',100,2,2),(3,100,'2017-04-21 12:14:07','2017-04-21 12:14:07',100,3,3),(4,100,'2017-04-21 12:14:56','2017-04-21 12:14:56',100,4,4),(5,100,'2017-04-21 12:17:25','2017-04-21 12:17:25',100,5,5),(6,100,'2017-04-21 12:22:37','2017-04-21 12:22:37',100,6,7),(7,100,'2017-04-21 12:34:59','2017-04-21 12:34:59',100,7,9),(8,100,'2017-04-21 12:35:35','2017-04-21 12:35:35',100,8,10),(9,100,'2017-04-21 12:36:12','2017-04-21 12:36:12',100,9,11),(10,100,'2020-06-03 11:34:32','2020-06-03 11:34:32',100,10,12),(11,100,'2020-06-03 11:37:30','2020-06-03 11:37:30',100,11,13);
/*!40000 ALTER TABLE `sigl_manuels_document__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_manuels_document__file_data_group`
--

DROP TABLE IF EXISTS `sigl_manuels_document__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_manuels_document__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_manuels_document__file_data_group`
--

LOCK TABLES `sigl_manuels_document__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_manuels_document__file_data_group` DISABLE KEYS */;
INSERT INTO `sigl_manuels_document__file_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000),(8,8,1000),(9,9,1000),(10,10,1000),(11,11,1000);
/*!40000 ALTER TABLE `sigl_manuels_document__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_manuels_document__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_manuels_document__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_manuels_document__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_manuels_document__file_data_group_mode`
--

LOCK TABLES `sigl_manuels_document__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_manuels_document__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_manuels_document__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_manuels_document__file_deleted`
--

DROP TABLE IF EXISTS `sigl_manuels_document__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_manuels_document__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_manuels_document__file_deleted`
--

LOCK TABLES `sigl_manuels_document__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_manuels_document__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_manuels_document__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_mgt_qlt_data`
--

DROP TABLE IF EXISTS `sigl_mgt_qlt_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_mgt_qlt_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_mgt_qlt_data`
--

LOCK TABLES `sigl_mgt_qlt_data` WRITE;
/*!40000 ALTER TABLE `sigl_mgt_qlt_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_mgt_qlt_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_mgt_qlt_data_group`
--

DROP TABLE IF EXISTS `sigl_mgt_qlt_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_mgt_qlt_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_mgt_qlt_data_group`
--

LOCK TABLES `sigl_mgt_qlt_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_mgt_qlt_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_mgt_qlt_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_mgt_qlt_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_mgt_qlt_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_mgt_qlt_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_mgt_qlt_data_group_mode`
--

LOCK TABLES `sigl_mgt_qlt_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_mgt_qlt_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_mgt_qlt_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_mgt_qlt_deleted`
--

DROP TABLE IF EXISTS `sigl_mgt_qlt_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_mgt_qlt_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_mgt_qlt_deleted`
--

LOCK TABLES `sigl_mgt_qlt_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_mgt_qlt_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_mgt_qlt_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `user_id` int(10) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `pre_anal` int(10) unsigned DEFAULT NULL,
  `anal` int(10) unsigned DEFAULT NULL,
  `post_anal` int(10) unsigned DEFAULT NULL,
  `trans_result` int(10) unsigned DEFAULT NULL,
  `rh` int(10) unsigned DEFAULT NULL,
  `eqpm` int(10) unsigned DEFAULT NULL,
  `reac_conso` int(10) unsigned DEFAULT NULL,
  `loc_env` int(10) unsigned DEFAULT NULL,
  `si` int(10) unsigned DEFAULT NULL,
  `ss_trait` int(10) unsigned DEFAULT NULL,
  `recl_clients` int(10) unsigned DEFAULT NULL,
  `pre_analytique_prescription` int(10) unsigned DEFAULT NULL,
  `pre_anal_oubli` int(10) unsigned DEFAULT NULL,
  `pre_anal_dos_pat` int(10) unsigned DEFAULT NULL,
  `pre_anal_prel` int(10) unsigned DEFAULT NULL,
  `pre_anal_heure_prel` int(10) unsigned DEFAULT NULL,
  `pre_anal_vol_prel` int(10) unsigned DEFAULT NULL,
  `pre_anal_ident_prel` int(10) unsigned DEFAULT NULL,
  `pre_anal_rsgnmt_clin` int(10) unsigned DEFAULT NULL,
  `pre_anal_transp_echant` int(10) unsigned DEFAULT NULL,
  `pre_anal_respect_proc` int(10) unsigned DEFAULT NULL,
  `pre_anal_urg` int(10) unsigned DEFAULT NULL,
  `pre_anal_tracab` int(10) unsigned DEFAULT NULL,
  `pre_anal_autre` int(10) unsigned DEFAULT NULL,
  `pre_analytique_autre_content` text,
  `anal_conserv` int(10) unsigned DEFAULT NULL,
  `anal_urg` int(10) unsigned DEFAULT NULL,
  `anal_centrif` int(10) unsigned DEFAULT NULL,
  `anal_aliquo` int(10) unsigned DEFAULT NULL,
  `anal_ctrl_qualite_int` int(10) unsigned DEFAULT NULL,
  `anal_ctrl_qualite_ext` int(10) unsigned DEFAULT NULL,
  `anal_trac` int(10) unsigned DEFAULT NULL,
  `anal_proce` int(10) unsigned DEFAULT NULL,
  `anal_abs_result` int(10) unsigned DEFAULT NULL,
  `anal_crit_de_rep` int(10) unsigned DEFAULT NULL,
  `anal_autre` int(10) unsigned DEFAULT NULL,
  `analytique_autre_content` text,
  `post_anal_dos_non_valide` int(10) unsigned DEFAULT NULL,
  `post_anal_valid_part` int(10) unsigned DEFAULT NULL,
  `post_anal_res_errone` int(10) unsigned DEFAULT NULL,
  `post_anal_abs_result` int(10) unsigned DEFAULT NULL,
  `post_anal_err_saisie` int(10) unsigned DEFAULT NULL,
  `post_anal_interp` int(10) unsigned DEFAULT NULL,
  `post_anal_presta_conseil` int(10) unsigned DEFAULT NULL,
  `post_anal_conserv` int(10) unsigned DEFAULT NULL,
  `post_anal_proc` int(10) unsigned DEFAULT NULL,
  `post_anal_autre` int(10) unsigned DEFAULT NULL,
  `post_analytique_autre_content` text,
  `trans_result_non_trans_pat` int(10) unsigned DEFAULT NULL,
  `trans_result_non_trans_presc` int(10) unsigned DEFAULT NULL,
  `trans_result_acces_result` int(10) unsigned DEFAULT NULL,
  `trans_result_date_rendu` int(10) unsigned DEFAULT NULL,
  `trans_result_delai_non_resp` int(10) unsigned DEFAULT NULL,
  `trans_result_proc` int(10) unsigned DEFAULT NULL,
  `trans_result_autre` int(10) unsigned DEFAULT NULL,
  `trans_result_autre_content` text,
  `rh_proc` int(10) unsigned DEFAULT NULL,
  `rh_abs` int(10) unsigned DEFAULT NULL,
  `rh_habilit` int(10) unsigned DEFAULT NULL,
  `rh_aes_hyg_secu` int(10) unsigned DEFAULT NULL,
  `rh_autre` int(10) unsigned DEFAULT NULL,
  `rh_autre_contenu` text,
  `eqpm_etal` int(10) unsigned DEFAULT NULL,
  `eqpm_calibr` int(10) unsigned DEFAULT NULL,
  `eqpm_alarme` int(10) unsigned DEFAULT NULL,
  `eqpm_panne` int(10) unsigned DEFAULT NULL,
  `eqpm_proc` int(10) unsigned DEFAULT NULL,
  `eqpm_autre` int(10) unsigned DEFAULT NULL,
  `equipements_autre_content` text,
  `reac_conso_recep` int(10) unsigned DEFAULT NULL,
  `reac_conso_delais` int(10) unsigned DEFAULT NULL,
  `reac_conso_reactifs` int(10) unsigned DEFAULT NULL,
  `reac_conso_rupture` int(10) unsigned DEFAULT NULL,
  `reac_conso_destock` int(10) unsigned DEFAULT NULL,
  `reac_conso_tracab` int(10) unsigned DEFAULT NULL,
  `reac_conso_autre` int(10) unsigned DEFAULT NULL,
  `reac_conso_autre_content` text,
  `loc_env_nettoy_labo` int(10) unsigned DEFAULT NULL,
  `loc_env_entretien` int(10) unsigned DEFAULT NULL,
  `loc_env_coup_elec` int(10) unsigned DEFAULT NULL,
  `loc_env_coup_eau` int(10) unsigned DEFAULT NULL,
  `loc_env_dechets` int(10) unsigned DEFAULT NULL,
  `loc_env_autre` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_autre_content` text,
  `si_no_co` int(10) unsigned DEFAULT NULL,
  `si_erreur` int(10) unsigned DEFAULT NULL,
  `si_panne_reseau` int(10) unsigned DEFAULT NULL,
  `si_panne_systeme` int(10) unsigned DEFAULT NULL,
  `si_panne_materiel` int(10) unsigned DEFAULT NULL,
  `si_autre` int(10) unsigned DEFAULT NULL,
  `si_autre_content` text,
  `ss_trait_delai` int(10) unsigned DEFAULT NULL,
  `ss_trait_erreur` int(10) unsigned DEFAULT NULL,
  `ss_trait_conservation` int(10) unsigned DEFAULT NULL,
  `ss_trait_fact` int(10) unsigned DEFAULT NULL,
  `ss_trait_autre` int(10) unsigned DEFAULT NULL,
  `ss_trait_autre_content` text,
  `autre` int(10) unsigned DEFAULT NULL,
  `autre_contenu` text,
  `recl_clients_contenu` text,
  `relation_dos_client` int(10) unsigned DEFAULT NULL,
  `no_dos` varchar(255) DEFAULT NULL,
  `description` text,
  `impact_patient` int(10) unsigned DEFAULT NULL,
  `impacts_perso_visit` int(10) unsigned DEFAULT NULL,
  `traitement_quoi` text,
  `traitement_qui_id` int(10) unsigned DEFAULT NULL,
  `traitement_quand` date DEFAULT NULL,
  `traitement_action_corrective` int(10) unsigned DEFAULT NULL,
  `traitement_action_description` text,
  `traitement_date_real` date DEFAULT NULL,
  `traitement_correctif_responsable_id` int(10) unsigned DEFAULT NULL,
  `cloture_commentaire` text,
  `cloture_validateur_id` int(10) unsigned DEFAULT NULL,
  `cloture_date` date DEFAULT NULL,
  `equipement_id` int(10) unsigned DEFAULT NULL,
  `fournisseur_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_data`
--

LOCK TABLES `sigl_non_conf_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_data_group`
--

DROP TABLE IF EXISTS `sigl_non_conf_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_data_group`
--

LOCK TABLES `sigl_non_conf_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_non_conf_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_data_group_mode`
--

LOCK TABLES `sigl_non_conf_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `user_id` int(10) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `pre_anal` int(10) unsigned DEFAULT NULL,
  `anal` int(10) unsigned DEFAULT NULL,
  `post_anal` int(10) unsigned DEFAULT NULL,
  `trans_result` int(10) unsigned DEFAULT NULL,
  `rh` int(10) unsigned DEFAULT NULL,
  `eqpm` int(10) unsigned DEFAULT NULL,
  `reac_conso` int(10) unsigned DEFAULT NULL,
  `loc_env` int(10) unsigned DEFAULT NULL,
  `si` int(10) unsigned DEFAULT NULL,
  `ss_trait` int(10) unsigned DEFAULT NULL,
  `recl_clients` int(10) unsigned DEFAULT NULL,
  `pre_analytique_prescription` int(10) unsigned DEFAULT NULL,
  `pre_anal_oubli` int(10) unsigned DEFAULT NULL,
  `pre_anal_dos_pat` int(10) unsigned DEFAULT NULL,
  `pre_anal_prel` int(10) unsigned DEFAULT NULL,
  `pre_anal_heure_prel` int(10) unsigned DEFAULT NULL,
  `pre_anal_vol_prel` int(10) unsigned DEFAULT NULL,
  `pre_anal_ident_prel` int(10) unsigned DEFAULT NULL,
  `pre_anal_rsgnmt_clin` int(10) unsigned DEFAULT NULL,
  `pre_anal_transp_echant` int(10) unsigned DEFAULT NULL,
  `pre_anal_respect_proc` int(10) unsigned DEFAULT NULL,
  `pre_anal_urg` int(10) unsigned DEFAULT NULL,
  `pre_anal_tracab` int(10) unsigned DEFAULT NULL,
  `pre_anal_autre` int(10) unsigned DEFAULT NULL,
  `pre_analytique_autre_content` text,
  `anal_conserv` int(10) unsigned DEFAULT NULL,
  `anal_urg` int(10) unsigned DEFAULT NULL,
  `anal_centrif` int(10) unsigned DEFAULT NULL,
  `anal_aliquo` int(10) unsigned DEFAULT NULL,
  `anal_ctrl_qualite_int` int(10) unsigned DEFAULT NULL,
  `anal_ctrl_qualite_ext` int(10) unsigned DEFAULT NULL,
  `anal_trac` int(10) unsigned DEFAULT NULL,
  `anal_proce` int(10) unsigned DEFAULT NULL,
  `anal_abs_result` int(10) unsigned DEFAULT NULL,
  `anal_crit_de_rep` int(10) unsigned DEFAULT NULL,
  `anal_autre` int(10) unsigned DEFAULT NULL,
  `analytique_autre_content` text,
  `post_anal_dos_non_valide` int(10) unsigned DEFAULT NULL,
  `post_anal_valid_part` int(10) unsigned DEFAULT NULL,
  `post_anal_res_errone` int(10) unsigned DEFAULT NULL,
  `post_anal_abs_result` int(10) unsigned DEFAULT NULL,
  `post_anal_err_saisie` int(10) unsigned DEFAULT NULL,
  `post_anal_interp` int(10) unsigned DEFAULT NULL,
  `post_anal_presta_conseil` int(10) unsigned DEFAULT NULL,
  `post_anal_conserv` int(10) unsigned DEFAULT NULL,
  `post_anal_proc` int(10) unsigned DEFAULT NULL,
  `post_anal_autre` int(10) unsigned DEFAULT NULL,
  `post_analytique_autre_content` text,
  `trans_result_non_trans_pat` int(10) unsigned DEFAULT NULL,
  `trans_result_non_trans_presc` int(10) unsigned DEFAULT NULL,
  `trans_result_acces_result` int(10) unsigned DEFAULT NULL,
  `trans_result_date_rendu` int(10) unsigned DEFAULT NULL,
  `trans_result_delai_non_resp` int(10) unsigned DEFAULT NULL,
  `trans_result_proc` int(10) unsigned DEFAULT NULL,
  `trans_result_autre` int(10) unsigned DEFAULT NULL,
  `trans_result_autre_content` text,
  `rh_proc` int(10) unsigned DEFAULT NULL,
  `rh_abs` int(10) unsigned DEFAULT NULL,
  `rh_habilit` int(10) unsigned DEFAULT NULL,
  `rh_aes_hyg_secu` int(10) unsigned DEFAULT NULL,
  `rh_autre` int(10) unsigned DEFAULT NULL,
  `rh_autre_contenu` text,
  `eqpm_etal` int(10) unsigned DEFAULT NULL,
  `eqpm_calibr` int(10) unsigned DEFAULT NULL,
  `eqpm_alarme` int(10) unsigned DEFAULT NULL,
  `eqpm_panne` int(10) unsigned DEFAULT NULL,
  `eqpm_proc` int(10) unsigned DEFAULT NULL,
  `eqpm_autre` int(10) unsigned DEFAULT NULL,
  `equipements_autre_content` text,
  `reac_conso_recep` int(10) unsigned DEFAULT NULL,
  `reac_conso_delais` int(10) unsigned DEFAULT NULL,
  `reac_conso_reactifs` int(10) unsigned DEFAULT NULL,
  `reac_conso_rupture` int(10) unsigned DEFAULT NULL,
  `reac_conso_destock` int(10) unsigned DEFAULT NULL,
  `reac_conso_tracab` int(10) unsigned DEFAULT NULL,
  `reac_conso_autre` int(10) unsigned DEFAULT NULL,
  `reac_conso_autre_content` text,
  `loc_env_nettoy_labo` int(10) unsigned DEFAULT NULL,
  `loc_env_entretien` int(10) unsigned DEFAULT NULL,
  `loc_env_coup_elec` int(10) unsigned DEFAULT NULL,
  `loc_env_coup_eau` int(10) unsigned DEFAULT NULL,
  `loc_env_dechets` int(10) unsigned DEFAULT NULL,
  `loc_env_autre` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_autre_content` text,
  `si_no_co` int(10) unsigned DEFAULT NULL,
  `si_erreur` int(10) unsigned DEFAULT NULL,
  `si_panne_reseau` int(10) unsigned DEFAULT NULL,
  `si_panne_systeme` int(10) unsigned DEFAULT NULL,
  `si_panne_materiel` int(10) unsigned DEFAULT NULL,
  `si_autre` int(10) unsigned DEFAULT NULL,
  `si_autre_content` text,
  `ss_trait_delai` int(10) unsigned DEFAULT NULL,
  `ss_trait_erreur` int(10) unsigned DEFAULT NULL,
  `ss_trait_conservation` int(10) unsigned DEFAULT NULL,
  `ss_trait_fact` int(10) unsigned DEFAULT NULL,
  `ss_trait_autre` int(10) unsigned DEFAULT NULL,
  `ss_trait_autre_content` text,
  `autre` int(10) unsigned DEFAULT NULL,
  `autre_contenu` text,
  `recl_clients_contenu` text,
  `relation_dos_client` int(10) unsigned DEFAULT NULL,
  `no_dos` varchar(255) DEFAULT NULL,
  `description` text,
  `impact_patient` int(10) unsigned DEFAULT NULL,
  `impacts_perso_visit` int(10) unsigned DEFAULT NULL,
  `traitement_quoi` text,
  `traitement_qui_id` int(10) unsigned DEFAULT NULL,
  `traitement_quand` date DEFAULT NULL,
  `traitement_action_corrective` int(10) unsigned DEFAULT NULL,
  `traitement_action_description` text,
  `traitement_date_real` date DEFAULT NULL,
  `traitement_correctif_responsable_id` int(10) unsigned DEFAULT NULL,
  `cloture_commentaire` text,
  `cloture_validateur_id` int(10) unsigned DEFAULT NULL,
  `cloture_date` date DEFAULT NULL,
  `equipement_id` int(10) unsigned DEFAULT NULL,
  `fournisseur_id` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_deleted`
--

LOCK TABLES `sigl_non_conf_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_abs_result_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_abs_result_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_abs_result_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_abs_result_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_abs_result_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_abs_result_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_abs_result_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_abs_result_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_abs_result_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_abs_result_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_abs_result_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_abs_result_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_abs_result_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_abs_result_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_aliquo_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_aliquo_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_aliquo_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_aliquo_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_aliquo_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_aliquo_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_aliquo_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_aliquo_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_aliquo_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_aliquo_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_aliquo_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_aliquo_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_aliquo_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_aliquo_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_centrif_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_centrif_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_centrif_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_centrif_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_centrif_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_centrif_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_centrif_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_centrif_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_centrif_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_centrif_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_centrif_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_centrif_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_centrif_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_centrif_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_conserv_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_conserv_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_conserv_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_conserv_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_conserv_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_conserv_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_conserv_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_conserv_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_conserv_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_conserv_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_conserv_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_conserv_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_conserv_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_conserv_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_crit_de_rep_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_crit_de_rep_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_crit_de_rep_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_crit_de_rep_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_crit_de_rep_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_crit_de_rep_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_crit_de_rep_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_crit_de_rep_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_crit_de_rep_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_crit_de_rep_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_crit_de_rep_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_crit_de_rep_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_crit_de_rep_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_crit_de_rep_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_ctrl_qualite_ext_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_ctrl_qualite_ext_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_ctrl_qualite_ext_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_ctrl_qualite_ext_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_ctrl_qualite_ext_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_ctrl_qualite_ext_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_ctrl_qualite_ext_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_ctrl_qualite_ext_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_ctrl_qualite_ext_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_ctrl_qualite_ext_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_ctrl_qualite_ext_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_ctrl_qualite_ext_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_ctrl_qualite_ext_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_ctrl_qualite_ext_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_ctrl_qualite_int_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_ctrl_qualite_int_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_ctrl_qualite_int_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_ctrl_qualite_int_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_ctrl_qualite_int_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_ctrl_qualite_int_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_ctrl_qualite_int_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_ctrl_qualite_int_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_ctrl_qualite_int_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_ctrl_qualite_int_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_ctrl_qualite_int_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_ctrl_qualite_int_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_ctrl_qualite_int_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_ctrl_qualite_int_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_proce_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_proce_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_proce_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_proce_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_proce_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_proce_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_proce_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_proce_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_proce_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_proce_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_proce_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_proce_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_proce_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_proce_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_trac_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_trac_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_trac_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_trac_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_trac_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_trac_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_trac_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_trac_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_trac_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_trac_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_trac_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_trac_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_trac_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_trac_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_urg_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_urg_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_urg_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_urg_data`
--

LOCK TABLES `sigl_non_conf_dico_anal_urg_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_urg_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_urg_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_anal_urg_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_anal_urg_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_anal_urg_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_anal_urg_deleted`
--

LOCK TABLES `sigl_non_conf_dico_anal_urg_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_urg_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_anal_urg_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_alarme_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_alarme_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_alarme_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_alarme_data`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_alarme_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_alarme_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_alarme_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_alarme_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_alarme_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_alarme_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_alarme_deleted`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_alarme_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_alarme_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_alarme_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_calibr_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_calibr_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_calibr_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_calibr_data`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_calibr_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_calibr_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_calibr_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_calibr_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_calibr_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_calibr_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_calibr_deleted`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_calibr_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_calibr_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_calibr_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_data`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_deleted`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_etal_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_etal_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_etal_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_etal_data`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_etal_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_etal_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_etal_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_etal_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_etal_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_etal_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_etal_deleted`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_etal_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_etal_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_etal_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_panne_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_panne_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_panne_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_panne_data`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_panne_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_panne_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_panne_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_panne_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_panne_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_panne_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_panne_deleted`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_panne_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_panne_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_panne_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_proc_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_proc_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_proc_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_proc_data`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_proc_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_proc_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_proc_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_eqpm_proc_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_eqpm_proc_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_eqpm_proc_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_eqpm_proc_deleted`
--

LOCK TABLES `sigl_non_conf_dico_eqpm_proc_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_proc_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_eqpm_proc_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_coup_eau_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_coup_eau_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_coup_eau_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_coup_eau_data`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_coup_eau_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_coup_eau_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_coup_eau_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_coup_eau_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_coup_eau_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_coup_eau_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_coup_eau_deleted`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_coup_eau_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_coup_eau_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_coup_eau_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_coup_elec_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_coup_elec_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_coup_elec_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_coup_elec_data`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_coup_elec_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_coup_elec_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_coup_elec_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_coup_elec_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_coup_elec_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_coup_elec_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_coup_elec_deleted`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_coup_elec_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_coup_elec_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_coup_elec_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_data`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_dechets_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_dechets_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_dechets_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_dechets_data`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_dechets_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_dechets_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_dechets_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_dechets_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_dechets_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_dechets_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_dechets_deleted`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_dechets_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_dechets_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_dechets_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_deleted`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_entretien_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_entretien_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_entretien_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_entretien_data`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_entretien_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_entretien_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_entretien_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_entretien_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_entretien_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_entretien_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_entretien_deleted`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_entretien_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_entretien_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_entretien_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_nettoy_labo_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_nettoy_labo_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_nettoy_labo_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_nettoy_labo_data`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_nettoy_labo_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_nettoy_labo_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_nettoy_labo_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_loc_env_nettoy_labo_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_loc_env_nettoy_labo_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_loc_env_nettoy_labo_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_loc_env_nettoy_labo_deleted`
--

LOCK TABLES `sigl_non_conf_dico_loc_env_nettoy_labo_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_nettoy_labo_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_loc_env_nettoy_labo_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_abs_result_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_abs_result_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_abs_result_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_abs_result_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_abs_result_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_abs_result_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_abs_result_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_abs_result_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_abs_result_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_abs_result_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_abs_result_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_abs_result_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_abs_result_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_abs_result_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_conserv_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_conserv_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_conserv_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_conserv_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_conserv_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_conserv_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_conserv_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_conserv_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_conserv_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_conserv_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_conserv_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_conserv_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_conserv_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_conserv_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_dos_non_valide_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_dos_non_valide_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_dos_non_valide_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_dos_non_valide_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_dos_non_valide_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_dos_non_valide_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_dos_non_valide_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_dos_non_valide_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_dos_non_valide_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_dos_non_valide_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_dos_non_valide_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_dos_non_valide_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_dos_non_valide_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_dos_non_valide_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_err_saisie_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_err_saisie_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_err_saisie_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_err_saisie_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_err_saisie_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_err_saisie_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_err_saisie_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_err_saisie_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_err_saisie_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_err_saisie_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_err_saisie_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_err_saisie_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_err_saisie_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_err_saisie_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_interp_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_interp_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_interp_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_interp_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_interp_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_interp_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_interp_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_interp_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_interp_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_interp_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_interp_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_interp_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_interp_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_interp_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_presta_conseil_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_presta_conseil_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_presta_conseil_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_presta_conseil_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_presta_conseil_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_presta_conseil_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_presta_conseil_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_presta_conseil_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_presta_conseil_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_presta_conseil_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_presta_conseil_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_presta_conseil_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_presta_conseil_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_presta_conseil_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_proc_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_proc_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_proc_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_proc_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_proc_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_proc_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_proc_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_proc_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_proc_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_proc_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_proc_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_proc_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_proc_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_proc_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_res_errone_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_res_errone_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_res_errone_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_res_errone_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_res_errone_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_res_errone_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_res_errone_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_res_errone_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_res_errone_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_res_errone_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_res_errone_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_res_errone_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_res_errone_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_res_errone_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_valid_part_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_valid_part_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_valid_part_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_valid_part_data`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_valid_part_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_valid_part_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_valid_part_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_post_anal_valid_part_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_post_anal_valid_part_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_post_anal_valid_part_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_post_anal_valid_part_deleted`
--

LOCK TABLES `sigl_non_conf_dico_post_anal_valid_part_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_valid_part_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_post_anal_valid_part_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_dos_pat_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_dos_pat_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_dos_pat_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_dos_pat_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_dos_pat_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_dos_pat_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_dos_pat_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_dos_pat_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_dos_pat_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_dos_pat_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_dos_pat_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_dos_pat_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_dos_pat_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_dos_pat_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_heure_prel_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_heure_prel_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_heure_prel_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_heure_prel_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_heure_prel_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_heure_prel_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_heure_prel_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_heure_prel_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_heure_prel_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_heure_prel_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_heure_prel_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_heure_prel_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_heure_prel_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_heure_prel_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_ident_prel_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_ident_prel_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_ident_prel_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_ident_prel_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_ident_prel_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_ident_prel_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_ident_prel_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_ident_prel_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_ident_prel_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_ident_prel_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_ident_prel_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_ident_prel_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_ident_prel_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_ident_prel_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_oubli_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_oubli_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_oubli_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_oubli_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_oubli_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_oubli_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_oubli_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_oubli_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_oubli_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_oubli_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_oubli_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_oubli_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_oubli_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_oubli_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_prel_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_prel_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_prel_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_prel_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_prel_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_prel_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_prel_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_prel_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_prel_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_prel_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_prel_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_prel_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_prel_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_prel_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_respect_proc_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_respect_proc_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_respect_proc_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_respect_proc_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_respect_proc_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_respect_proc_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_respect_proc_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_respect_proc_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_respect_proc_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_respect_proc_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_respect_proc_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_respect_proc_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_respect_proc_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_respect_proc_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_rsgnmt_clin_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_rsgnmt_clin_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_rsgnmt_clin_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_rsgnmt_clin_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_rsgnmt_clin_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_rsgnmt_clin_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_rsgnmt_clin_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_rsgnmt_clin_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_rsgnmt_clin_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_rsgnmt_clin_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_rsgnmt_clin_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_rsgnmt_clin_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_rsgnmt_clin_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_rsgnmt_clin_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_tracab_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_tracab_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_tracab_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_tracab_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_tracab_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_tracab_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_tracab_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_tracab_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_tracab_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_tracab_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_tracab_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_tracab_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_tracab_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_tracab_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_transp_echant_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_transp_echant_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_transp_echant_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_transp_echant_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_transp_echant_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_transp_echant_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_transp_echant_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_transp_echant_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_transp_echant_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_transp_echant_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_transp_echant_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_transp_echant_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_transp_echant_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_transp_echant_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_urg_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_urg_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_urg_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_urg_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_urg_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_urg_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_urg_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_urg_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_urg_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_urg_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_urg_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_urg_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_urg_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_urg_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_vol_prel_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_vol_prel_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_vol_prel_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_vol_prel_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_vol_prel_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_vol_prel_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_vol_prel_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_anal_vol_prel_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_anal_vol_prel_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_anal_vol_prel_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_anal_vol_prel_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_anal_vol_prel_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_vol_prel_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_anal_vol_prel_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_analytique_prescription_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_analytique_prescription_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_analytique_prescription_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_analytique_prescription_data`
--

LOCK TABLES `sigl_non_conf_dico_pre_analytique_prescription_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_analytique_prescription_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_analytique_prescription_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_pre_analytique_prescription_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_pre_analytique_prescription_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_pre_analytique_prescription_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_pre_analytique_prescription_deleted`
--

LOCK TABLES `sigl_non_conf_dico_pre_analytique_prescription_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_analytique_prescription_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_pre_analytique_prescription_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_data`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_delais_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_delais_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_delais_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_delais_data`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_delais_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_delais_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_delais_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_delais_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_delais_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_delais_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_delais_deleted`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_delais_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_delais_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_delais_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_deleted`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_destock_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_destock_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_destock_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_destock_data`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_destock_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_destock_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_destock_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_destock_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_destock_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_destock_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_destock_deleted`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_destock_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_destock_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_destock_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_reactifs_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_reactifs_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_reactifs_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_reactifs_data`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_reactifs_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_reactifs_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_reactifs_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_reactifs_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_reactifs_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_reactifs_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_reactifs_deleted`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_reactifs_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_reactifs_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_reactifs_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_recep_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_recep_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_recep_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_recep_data`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_recep_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_recep_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_recep_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_recep_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_recep_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_recep_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_recep_deleted`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_recep_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_recep_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_recep_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_rupture_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_rupture_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_rupture_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_rupture_data`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_rupture_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_rupture_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_rupture_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_rupture_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_rupture_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_rupture_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_rupture_deleted`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_rupture_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_rupture_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_rupture_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_tracab_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_tracab_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_tracab_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_tracab_data`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_tracab_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_tracab_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_tracab_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_reac_conso_tracab_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_reac_conso_tracab_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_reac_conso_tracab_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_reac_conso_tracab_deleted`
--

LOCK TABLES `sigl_non_conf_dico_reac_conso_tracab_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_tracab_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_reac_conso_tracab_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_recl_clients_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_recl_clients_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_recl_clients_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_recl_clients_data`
--

LOCK TABLES `sigl_non_conf_dico_recl_clients_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_recl_clients_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_recl_clients_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_recl_clients_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_recl_clients_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_recl_clients_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_recl_clients_deleted`
--

LOCK TABLES `sigl_non_conf_dico_recl_clients_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_recl_clients_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_recl_clients_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_abs_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_abs_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_abs_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_abs_data`
--

LOCK TABLES `sigl_non_conf_dico_rh_abs_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_abs_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_abs_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_abs_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_abs_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_abs_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_abs_deleted`
--

LOCK TABLES `sigl_non_conf_dico_rh_abs_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_abs_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_abs_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_aes_hyg_secu_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_aes_hyg_secu_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_aes_hyg_secu_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_aes_hyg_secu_data`
--

LOCK TABLES `sigl_non_conf_dico_rh_aes_hyg_secu_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_aes_hyg_secu_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_aes_hyg_secu_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_aes_hyg_secu_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_aes_hyg_secu_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_aes_hyg_secu_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_aes_hyg_secu_deleted`
--

LOCK TABLES `sigl_non_conf_dico_rh_aes_hyg_secu_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_aes_hyg_secu_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_aes_hyg_secu_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_rh_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_rh_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_data`
--

LOCK TABLES `sigl_non_conf_dico_rh_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_deleted`
--

LOCK TABLES `sigl_non_conf_dico_rh_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_habilit_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_habilit_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_habilit_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_habilit_data`
--

LOCK TABLES `sigl_non_conf_dico_rh_habilit_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_habilit_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_habilit_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_habilit_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_habilit_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_habilit_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_habilit_deleted`
--

LOCK TABLES `sigl_non_conf_dico_rh_habilit_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_habilit_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_habilit_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_proc_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_proc_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_proc_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_proc_data`
--

LOCK TABLES `sigl_non_conf_dico_rh_proc_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_proc_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_proc_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_rh_proc_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_rh_proc_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_rh_proc_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_rh_proc_deleted`
--

LOCK TABLES `sigl_non_conf_dico_rh_proc_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_proc_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_rh_proc_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_si_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_si_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_data`
--

LOCK TABLES `sigl_non_conf_dico_si_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_deleted`
--

LOCK TABLES `sigl_non_conf_dico_si_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_erreur_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_erreur_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_erreur_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_erreur_data`
--

LOCK TABLES `sigl_non_conf_dico_si_erreur_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_erreur_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_erreur_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_erreur_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_erreur_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_erreur_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_erreur_deleted`
--

LOCK TABLES `sigl_non_conf_dico_si_erreur_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_erreur_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_erreur_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_no_co_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_no_co_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_no_co_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_no_co_data`
--

LOCK TABLES `sigl_non_conf_dico_si_no_co_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_no_co_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_no_co_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_no_co_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_no_co_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_no_co_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_no_co_deleted`
--

LOCK TABLES `sigl_non_conf_dico_si_no_co_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_no_co_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_no_co_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_panne_materiel_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_panne_materiel_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_panne_materiel_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_panne_materiel_data`
--

LOCK TABLES `sigl_non_conf_dico_si_panne_materiel_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_materiel_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_materiel_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_panne_materiel_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_panne_materiel_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_panne_materiel_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_panne_materiel_deleted`
--

LOCK TABLES `sigl_non_conf_dico_si_panne_materiel_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_materiel_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_materiel_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_panne_reseau_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_panne_reseau_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_panne_reseau_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_panne_reseau_data`
--

LOCK TABLES `sigl_non_conf_dico_si_panne_reseau_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_reseau_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_reseau_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_panne_reseau_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_panne_reseau_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_panne_reseau_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_panne_reseau_deleted`
--

LOCK TABLES `sigl_non_conf_dico_si_panne_reseau_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_reseau_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_reseau_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_panne_systeme_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_panne_systeme_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_panne_systeme_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_panne_systeme_data`
--

LOCK TABLES `sigl_non_conf_dico_si_panne_systeme_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_systeme_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_systeme_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_si_panne_systeme_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_si_panne_systeme_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_si_panne_systeme_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_si_panne_systeme_deleted`
--

LOCK TABLES `sigl_non_conf_dico_si_panne_systeme_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_systeme_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_si_panne_systeme_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_conservation_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_conservation_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_conservation_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_conservation_data`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_conservation_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_conservation_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_conservation_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_conservation_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_conservation_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_conservation_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_conservation_deleted`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_conservation_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_conservation_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_conservation_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_data`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_delai_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_delai_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_delai_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_delai_data`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_delai_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_delai_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_delai_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_delai_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_delai_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_delai_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_delai_deleted`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_delai_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_delai_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_delai_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_deleted`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_erreur_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_erreur_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_erreur_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_erreur_data`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_erreur_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_erreur_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_erreur_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_erreur_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_erreur_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_erreur_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_erreur_deleted`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_erreur_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_erreur_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_erreur_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_fact_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_fact_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_fact_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_fact_data`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_fact_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_fact_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_fact_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_ss_trait_fact_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_ss_trait_fact_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_ss_trait_fact_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_ss_trait_fact_deleted`
--

LOCK TABLES `sigl_non_conf_dico_ss_trait_fact_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_fact_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_ss_trait_fact_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_acces_result_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_acces_result_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_acces_result_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_acces_result_data`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_acces_result_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_acces_result_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_acces_result_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_acces_result_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_acces_result_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_acces_result_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_acces_result_deleted`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_acces_result_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_acces_result_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_acces_result_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_autre_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_autre_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_autre_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_autre_data`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_autre_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_autre_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_autre_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_autre_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_autre_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_autre_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_autre_deleted`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_autre_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_autre_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_autre_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_data`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_date_rendu_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_date_rendu_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_date_rendu_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_date_rendu_data`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_date_rendu_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_date_rendu_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_date_rendu_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_date_rendu_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_date_rendu_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_date_rendu_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_date_rendu_deleted`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_date_rendu_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_date_rendu_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_date_rendu_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_delai_non_resp_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_delai_non_resp_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_delai_non_resp_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_delai_non_resp_data`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_delai_non_resp_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_delai_non_resp_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_delai_non_resp_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_delai_non_resp_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_delai_non_resp_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_delai_non_resp_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_delai_non_resp_deleted`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_delai_non_resp_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_delai_non_resp_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_delai_non_resp_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_deleted`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_non_trans_pat_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_non_trans_pat_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_non_trans_pat_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_non_trans_pat_data`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_non_trans_pat_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_non_trans_pat_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_non_trans_pat_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_non_trans_pat_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_non_trans_pat_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_non_trans_pat_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_non_trans_pat_deleted`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_non_trans_pat_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_non_trans_pat_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_non_trans_pat_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_non_trans_presc_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_non_trans_presc_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_non_trans_presc_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_non_trans_presc_data`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_non_trans_presc_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_non_trans_presc_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_non_trans_presc_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_non_trans_presc_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_non_trans_presc_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_non_trans_presc_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_non_trans_presc_deleted`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_non_trans_presc_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_non_trans_presc_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_non_trans_presc_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_proc_data`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_proc_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_proc_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_proc_data`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_proc_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_proc_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_proc_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conf_dico_trans_result_proc_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conf_dico_trans_result_proc_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conf_dico_trans_result_proc_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_non_conf` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_dico` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id_data` (`id_data`),
  KEY `id_non_conf` (`id_non_conf`),
  KEY `id_dico` (`id_dico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conf_dico_trans_result_proc_deleted`
--

LOCK TABLES `sigl_non_conf_dico_trans_result_proc_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_proc_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conf_dico_trans_result_proc_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conformite_data`
--

DROP TABLE IF EXISTS `sigl_non_conformite_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conformite_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `user_id` int(10) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `pre_analytique` int(10) unsigned DEFAULT NULL,
  `analytique` int(10) unsigned DEFAULT NULL,
  `post_analytique` int(10) unsigned DEFAULT NULL,
  `transmission_resultats` int(10) unsigned DEFAULT NULL,
  `rh` int(10) unsigned DEFAULT NULL,
  `equipements` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables` int(10) unsigned DEFAULT NULL,
  `locaux_environnement` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques` int(10) unsigned DEFAULT NULL,
  `sous_traitance` int(10) unsigned DEFAULT NULL,
  `reclamations_clients` int(10) unsigned DEFAULT NULL,
  `pre_analytique_prescription` int(10) unsigned DEFAULT NULL,
  `pre_analytique_oubli_examen_error` int(10) unsigned DEFAULT NULL,
  `pre_analytique_dossier_pat` int(10) unsigned DEFAULT NULL,
  `pre_analytique_prel` int(10) unsigned DEFAULT NULL,
  `pre_analytique_heure_prel` int(10) unsigned DEFAULT NULL,
  `pre_analytique_vol_prel` int(10) unsigned DEFAULT NULL,
  `pre_analytique_ident_prel` int(10) unsigned DEFAULT NULL,
  `pre_analytique_renseignement_clin` int(10) unsigned DEFAULT NULL,
  `pre_analytique_transport_echant` int(10) unsigned DEFAULT NULL,
  `pre_analytique_respect_proc` int(10) unsigned DEFAULT NULL,
  `pre_analytique_urgence` int(10) unsigned DEFAULT NULL,
  `pre_analytique_tracabilite` int(10) unsigned DEFAULT NULL,
  `pre_analytique_autre` int(10) unsigned DEFAULT NULL,
  `pre_analytique_autre_content` text,
  `analytique_conservation` int(10) unsigned DEFAULT NULL,
  `analytique_urgence` int(10) unsigned DEFAULT NULL,
  `analytique_centrifugation` int(10) unsigned DEFAULT NULL,
  `analytique_aliquotage` int(10) unsigned DEFAULT NULL,
  `analytique_ctrl_qualite_int` int(10) unsigned DEFAULT NULL,
  `analytique_ctrl_qualite_ext` int(10) unsigned DEFAULT NULL,
  `analytique_tracabilite` int(10) unsigned DEFAULT NULL,
  `analytique_procedures` int(10) unsigned DEFAULT NULL,
  `analytique_absence_resultat` int(10) unsigned DEFAULT NULL,
  `analytique_critere_de_repasse` int(10) unsigned DEFAULT NULL,
  `analytique_autre` int(10) unsigned DEFAULT NULL,
  `analytique_autre_content` text,
  `post_analytique_dos_non_valide` int(10) unsigned DEFAULT NULL,
  `post_analytique_validation_partiel` int(10) unsigned DEFAULT NULL,
  `post_analytique_res_errone` int(10) unsigned DEFAULT NULL,
  `post_analytique_absence_resultat` int(10) unsigned DEFAULT NULL,
  `post_analytique_erreur_saisie` int(10) unsigned DEFAULT NULL,
  `post_analytique_interpretation` int(10) unsigned DEFAULT NULL,
  `post_analytique_presta_conseil` int(10) unsigned DEFAULT NULL,
  `post_analytique_conservation` int(10) unsigned DEFAULT NULL,
  `post_analytique_procedures` int(10) unsigned DEFAULT NULL,
  `post_analytique_autre` int(10) unsigned DEFAULT NULL,
  `post_analytique_autre_content` text,
  `transmission_resultats_non_transmis_patient` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_non_transmis_presc` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_acces_result` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_date_rendu` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_delai_non_resp` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_procedure` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_autre` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_autre_content` text,
  `rh_procedures` int(10) unsigned DEFAULT NULL,
  `rh_absence` int(10) unsigned DEFAULT NULL,
  `rh_habilitation` int(10) unsigned DEFAULT NULL,
  `rh_aes_hygiene_secu` int(10) unsigned DEFAULT NULL,
  `rh_autre` int(10) unsigned DEFAULT NULL,
  `rh_autre_contenu` text,
  `equipements_etalonnage` int(10) unsigned DEFAULT NULL,
  `equipements_calibration` int(10) unsigned DEFAULT NULL,
  `equipements_alarme` int(10) unsigned DEFAULT NULL,
  `equipements_panne` int(10) unsigned DEFAULT NULL,
  `equipements_procedures` int(10) unsigned DEFAULT NULL,
  `equipements_autre` int(10) unsigned DEFAULT NULL,
  `equipements_autre_content` text,
  `reactifs_consommables_reception` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_delais` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_reactifs` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_rupture` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_destockage` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_tracabilite` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_autre` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_autre_content` text,
  `locaux_environnement_nettoyage` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_entretien` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_coupure_elec` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_coupure_eau` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_dechets` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_autre` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_autre_content` text,
  `systemes_informatiques_absence` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_erreur` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_panne_reseau` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_panne_systeme` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_panne_materiel` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_autre` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_autre_content` text,
  `sous_traitance_delai` int(10) unsigned DEFAULT NULL,
  `sous_traitance_erreur` int(10) unsigned DEFAULT NULL,
  `sous_traitance_conservation` int(10) unsigned DEFAULT NULL,
  `sous_traitance_facturation` int(10) unsigned DEFAULT NULL,
  `sous_traitance_autre` int(10) unsigned DEFAULT NULL,
  `sous_traitance_autre_content` text,
  `autre` int(10) unsigned DEFAULT NULL,
  `autre_contenu` text,
  `reclamations_clients_contenu` text,
  `relation_dos_client` int(10) unsigned DEFAULT NULL,
  `no_dos` varchar(255) DEFAULT NULL,
  `description` text,
  `impact_patient` int(10) unsigned DEFAULT NULL,
  `impacts_perso_visit` int(10) unsigned DEFAULT NULL,
  `traitement_quoi` text,
  `traitement_qui_id` int(10) unsigned DEFAULT NULL,
  `traitement_quand` date DEFAULT NULL,
  `traitement_action_corrective` int(10) unsigned DEFAULT NULL,
  `traitement_action_description` text,
  `traitement_date_real` date DEFAULT NULL,
  `traitement_correctif_responsable_id` int(10) unsigned DEFAULT NULL,
  `cloture_commentaire` text,
  `cloture_validateur_id` int(10) unsigned DEFAULT NULL,
  `cloture_date` date DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conformite_data`
--

LOCK TABLES `sigl_non_conformite_data` WRITE;
/*!40000 ALTER TABLE `sigl_non_conformite_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conformite_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conformite_data_group`
--

DROP TABLE IF EXISTS `sigl_non_conformite_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conformite_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conformite_data_group`
--

LOCK TABLES `sigl_non_conformite_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_non_conformite_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conformite_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conformite_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_non_conformite_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conformite_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conformite_data_group_mode`
--

LOCK TABLES `sigl_non_conformite_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_non_conformite_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conformite_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_non_conformite_deleted`
--

DROP TABLE IF EXISTS `sigl_non_conformite_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_non_conformite_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `user_id` int(10) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `pre_analytique` int(10) unsigned DEFAULT NULL,
  `analytique` int(10) unsigned DEFAULT NULL,
  `post_analytique` int(10) unsigned DEFAULT NULL,
  `transmission_resultats` int(10) unsigned DEFAULT NULL,
  `rh` int(10) unsigned DEFAULT NULL,
  `equipements` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables` int(10) unsigned DEFAULT NULL,
  `locaux_environnement` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques` int(10) unsigned DEFAULT NULL,
  `sous_traitance` int(10) unsigned DEFAULT NULL,
  `reclamations_clients` int(10) unsigned DEFAULT NULL,
  `pre_analytique_prescription` int(10) unsigned DEFAULT NULL,
  `pre_analytique_oubli_examen_error` int(10) unsigned DEFAULT NULL,
  `pre_analytique_dossier_pat` int(10) unsigned DEFAULT NULL,
  `pre_analytique_prel` int(10) unsigned DEFAULT NULL,
  `pre_analytique_heure_prel` int(10) unsigned DEFAULT NULL,
  `pre_analytique_vol_prel` int(10) unsigned DEFAULT NULL,
  `pre_analytique_ident_prel` int(10) unsigned DEFAULT NULL,
  `pre_analytique_renseignement_clin` int(10) unsigned DEFAULT NULL,
  `pre_analytique_transport_echant` int(10) unsigned DEFAULT NULL,
  `pre_analytique_respect_proc` int(10) unsigned DEFAULT NULL,
  `pre_analytique_urgence` int(10) unsigned DEFAULT NULL,
  `pre_analytique_tracabilite` int(10) unsigned DEFAULT NULL,
  `pre_analytique_autre` int(10) unsigned DEFAULT NULL,
  `pre_analytique_autre_content` text,
  `analytique_conservation` int(10) unsigned DEFAULT NULL,
  `analytique_urgence` int(10) unsigned DEFAULT NULL,
  `analytique_centrifugation` int(10) unsigned DEFAULT NULL,
  `analytique_aliquotage` int(10) unsigned DEFAULT NULL,
  `analytique_ctrl_qualite_int` int(10) unsigned DEFAULT NULL,
  `analytique_ctrl_qualite_ext` int(10) unsigned DEFAULT NULL,
  `analytique_tracabilite` int(10) unsigned DEFAULT NULL,
  `analytique_procedures` int(10) unsigned DEFAULT NULL,
  `analytique_absence_resultat` int(10) unsigned DEFAULT NULL,
  `analytique_critere_de_repasse` int(10) unsigned DEFAULT NULL,
  `analytique_autre` int(10) unsigned DEFAULT NULL,
  `analytique_autre_content` text,
  `post_analytique_dos_non_valide` int(10) unsigned DEFAULT NULL,
  `post_analytique_validation_partiel` int(10) unsigned DEFAULT NULL,
  `post_analytique_res_errone` int(10) unsigned DEFAULT NULL,
  `post_analytique_absence_resultat` int(10) unsigned DEFAULT NULL,
  `post_analytique_erreur_saisie` int(10) unsigned DEFAULT NULL,
  `post_analytique_interpretation` int(10) unsigned DEFAULT NULL,
  `post_analytique_presta_conseil` int(10) unsigned DEFAULT NULL,
  `post_analytique_conservation` int(10) unsigned DEFAULT NULL,
  `post_analytique_procedures` int(10) unsigned DEFAULT NULL,
  `post_analytique_autre` int(10) unsigned DEFAULT NULL,
  `post_analytique_autre_content` text,
  `transmission_resultats_non_transmis_patient` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_non_transmis_presc` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_acces_result` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_date_rendu` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_delai_non_resp` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_procedure` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_autre` int(10) unsigned DEFAULT NULL,
  `transmission_resultats_autre_content` text,
  `rh_procedures` int(10) unsigned DEFAULT NULL,
  `rh_absence` int(10) unsigned DEFAULT NULL,
  `rh_habilitation` int(10) unsigned DEFAULT NULL,
  `rh_aes_hygiene_secu` int(10) unsigned DEFAULT NULL,
  `rh_autre` int(10) unsigned DEFAULT NULL,
  `rh_autre_contenu` text,
  `equipements_etalonnage` int(10) unsigned DEFAULT NULL,
  `equipements_calibration` int(10) unsigned DEFAULT NULL,
  `equipements_alarme` int(10) unsigned DEFAULT NULL,
  `equipements_panne` int(10) unsigned DEFAULT NULL,
  `equipements_procedures` int(10) unsigned DEFAULT NULL,
  `equipements_autre` int(10) unsigned DEFAULT NULL,
  `equipements_autre_content` text,
  `reactifs_consommables_reception` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_delais` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_reactifs` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_rupture` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_destockage` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_tracabilite` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_autre` int(10) unsigned DEFAULT NULL,
  `reactifs_consommables_autre_content` text,
  `locaux_environnement_nettoyage` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_entretien` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_coupure_elec` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_coupure_eau` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_dechets` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_autre` int(10) unsigned DEFAULT NULL,
  `locaux_environnement_autre_content` text,
  `systemes_informatiques_absence` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_erreur` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_panne_reseau` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_panne_systeme` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_panne_materiel` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_autre` int(10) unsigned DEFAULT NULL,
  `systemes_informatiques_autre_content` text,
  `sous_traitance_delai` int(10) unsigned DEFAULT NULL,
  `sous_traitance_erreur` int(10) unsigned DEFAULT NULL,
  `sous_traitance_conservation` int(10) unsigned DEFAULT NULL,
  `sous_traitance_facturation` int(10) unsigned DEFAULT NULL,
  `sous_traitance_autre` int(10) unsigned DEFAULT NULL,
  `sous_traitance_autre_content` text,
  `autre` int(10) unsigned DEFAULT NULL,
  `autre_contenu` text,
  `reclamations_clients_contenu` text,
  `relation_dos_client` int(10) unsigned DEFAULT NULL,
  `no_dos` varchar(255) DEFAULT NULL,
  `description` text,
  `impact_patient` int(10) unsigned DEFAULT NULL,
  `impacts_perso_visit` int(10) unsigned DEFAULT NULL,
  `traitement_quoi` text,
  `traitement_qui_id` int(10) unsigned DEFAULT NULL,
  `traitement_quand` date DEFAULT NULL,
  `traitement_action_corrective` int(10) unsigned DEFAULT NULL,
  `traitement_action_description` text,
  `traitement_date_real` date DEFAULT NULL,
  `traitement_correctif_responsable_id` int(10) unsigned DEFAULT NULL,
  `cloture_commentaire` text,
  `cloture_validateur_id` int(10) unsigned DEFAULT NULL,
  `cloture_date` date DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_non_conformite_deleted`
--

LOCK TABLES `sigl_non_conformite_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_non_conformite_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_non_conformite_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_param_cr_data`
--

DROP TABLE IF EXISTS `sigl_param_cr_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_param_cr_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `entete` int(10) unsigned DEFAULT NULL,
  `commentaire` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_param_cr_data`
--

LOCK TABLES `sigl_param_cr_data` WRITE;
/*!40000 ALTER TABLE `sigl_param_cr_data` DISABLE KEYS */;
INSERT INTO `sigl_param_cr_data` VALUES (1,100,NULL,NULL,NULL,1068,1049);
/*!40000 ALTER TABLE `sigl_param_cr_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_param_cr_data_group`
--

DROP TABLE IF EXISTS `sigl_param_cr_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_param_cr_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_param_cr_data_group`
--

LOCK TABLES `sigl_param_cr_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_param_cr_data_group` DISABLE KEYS */;
INSERT INTO `sigl_param_cr_data_group` VALUES (1,1,1000);
/*!40000 ALTER TABLE `sigl_param_cr_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_param_cr_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_param_cr_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_param_cr_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_param_cr_data_group_mode`
--

LOCK TABLES `sigl_param_cr_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_param_cr_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_param_cr_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_param_cr_deleted`
--

DROP TABLE IF EXISTS `sigl_param_cr_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_param_cr_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `entete` int(10) unsigned DEFAULT NULL,
  `commentaire` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_param_cr_deleted`
--

LOCK TABLES `sigl_param_cr_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_param_cr_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_param_cr_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_param_num_dos_data`
--

DROP TABLE IF EXISTS `sigl_param_num_dos_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_param_num_dos_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `periode` int(10) unsigned DEFAULT NULL,
  `format` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_param_num_dos_data`
--

LOCK TABLES `sigl_param_num_dos_data` WRITE;
/*!40000 ALTER TABLE `sigl_param_num_dos_data` DISABLE KEYS */;
INSERT INTO `sigl_param_num_dos_data` VALUES (1,100,'2017-04-14 15:58:16','2017-04-19 17:12:11',100,1070,1072);
/*!40000 ALTER TABLE `sigl_param_num_dos_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_param_num_dos_data_group`
--

DROP TABLE IF EXISTS `sigl_param_num_dos_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_param_num_dos_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_param_num_dos_data_group`
--

LOCK TABLES `sigl_param_num_dos_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_param_num_dos_data_group` DISABLE KEYS */;
INSERT INTO `sigl_param_num_dos_data_group` VALUES (1,1,1000);
/*!40000 ALTER TABLE `sigl_param_num_dos_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_param_num_dos_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_param_num_dos_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_param_num_dos_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_param_num_dos_data_group_mode`
--

LOCK TABLES `sigl_param_num_dos_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_param_num_dos_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_param_num_dos_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_param_num_dos_deleted`
--

DROP TABLE IF EXISTS `sigl_param_num_dos_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_param_num_dos_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `periode` int(10) unsigned DEFAULT NULL,
  `format` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_param_num_dos_deleted`
--

LOCK TABLES `sigl_param_num_dos_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_param_num_dos_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_param_num_dos_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_auth_flooding`
--

DROP TABLE IF EXISTS `sigl_pj_auth_flooding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_auth_flooding` (
  `id_auth_flooding` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hash` varchar(100) NOT NULL,
  `creation_date` int(11) NOT NULL,
  PRIMARY KEY (`id_auth_flooding`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_auth_flooding`
--

LOCK TABLES `sigl_pj_auth_flooding` WRITE;
/*!40000 ALTER TABLE `sigl_pj_auth_flooding` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_pj_auth_flooding` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_auth_lock`
--

DROP TABLE IF EXISTS `sigl_pj_auth_lock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_auth_lock` (
  `id_auth_lock` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hash` varchar(100) NOT NULL,
  `lock_until` int(11) NOT NULL,
  `creation_date` int(11) NOT NULL,
  PRIMARY KEY (`id_auth_lock`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_auth_lock`
--

LOCK TABLES `sigl_pj_auth_lock` WRITE;
/*!40000 ALTER TABLE `sigl_pj_auth_lock` DISABLE KEYS */;
INSERT INTO `sigl_pj_auth_lock` VALUES (1,'b389b5434cc6dd24196ccd16705cab352af94d87',1583743944,1583743884);
/*!40000 ALTER TABLE `sigl_pj_auth_lock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_axis`
--

DROP TABLE IF EXISTS `sigl_pj_axis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_axis` (
  `id_axis` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `id_group` int(11) NOT NULL,
  PRIMARY KEY (`id_axis`),
  UNIQUE KEY `sigl_pj_axis_name` (`name`),
  UNIQUE KEY `sigl_pj_axis_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_axis`
--

LOCK TABLES `sigl_pj_axis` WRITE;
/*!40000 ALTER TABLE `sigl_pj_axis` DISABLE KEYS */;
INSERT INTO `sigl_pj_axis` VALUES (1,'Laboratoire',1000);
/*!40000 ALTER TABLE `sigl_pj_axis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_group`
--

DROP TABLE IF EXISTS `sigl_pj_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_group` (
  `id_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `id_axis` int(11) DEFAULT NULL,
  `disabled` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=1009 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_group`
--

LOCK TABLES `sigl_pj_group` WRITE;
/*!40000 ALTER TABLE `sigl_pj_group` DISABLE KEYS */;
INSERT INTO `sigl_pj_group` VALUES (100,'root',NULL,0),(1000,'Laboratoire',1,0),(1001,'biologiste',NULL,0),(1002,'technicien',NULL,0),(1003,'techav',NULL,0),(1004,'techq',NULL,0),(1005,'secretaire',NULL,0),(1006,'secrav',NULL,0),(1007,'qualiticien',NULL,0),(1008,'prescripteur',NULL,0);
/*!40000 ALTER TABLE `sigl_pj_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_group_link`
--

DROP TABLE IF EXISTS `sigl_pj_group_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_group_link` (
  `id_group_link` int(11) NOT NULL AUTO_INCREMENT,
  `id_group` int(10) unsigned NOT NULL,
  `id_group_parent` int(11) DEFAULT NULL,
  `id_role` int(10) DEFAULT NULL,
  PRIMARY KEY (`id_group_link`),
  UNIQUE KEY `sigl_pj_group_link_real_key` (`id_group`,`id_group_parent`,`id_role`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_group_link`
--

LOCK TABLES `sigl_pj_group_link` WRITE;
/*!40000 ALTER TABLE `sigl_pj_group_link` DISABLE KEYS */;
INSERT INTO `sigl_pj_group_link` VALUES (1,100,1000,1),(2,1001,1000,2),(3,1002,1000,3),(4,1003,1000,5),(5,1004,1000,6),(6,1005,1000,4),(7,1006,1000,7),(8,1007,1000,8),(9,1008,1000,9);
/*!40000 ALTER TABLE `sigl_pj_group_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_group_mode`
--

DROP TABLE IF EXISTS `sigl_pj_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_group_mode` (
  `id_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_group_link` int(11) NOT NULL,
  `id_varset` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  PRIMARY KEY (`id_group_mode`),
  KEY `id_group_link` (`id_group_link`)
) ENGINE=InnoDB AUTO_INCREMENT=5995 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_group_mode`
--

LOCK TABLES `sigl_pj_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_pj_group_mode` DISABLE KEYS */;
INSERT INTO `sigl_pj_group_mode` VALUES (5940,1,1,448),(5941,1,6,448),(5942,1,7,448),(5943,1,8,448),(5944,1,9,448),(5945,1,12,448),(5946,1,13,448),(5947,1,14,448),(5948,1,16,448),(5949,1,17,448),(5950,1,18,448),(5951,1,19,448),(5952,1,20,448),(5953,1,32,448),(5954,1,33,448),(5955,1,34,448),(5956,1,35,448),(5957,1,37,448),(5958,1,39,448),(5959,1,40,448),(5960,1,41,448),(5961,1,42,448),(5962,1,43,448),(5963,1,45,448),(5964,1,47,448),(5965,1,49,448),(5966,1,51,448),(5967,1,53,448),(5968,1,55,448),(5969,1,57,448),(5970,1,59,448),(5971,1,61,448),(5972,1,63,448),(5973,1,65,448),(5974,1,67,448),(5975,1,69,448),(5976,1,71,448),(5977,1,73,448),(5978,1,75,448),(5979,1,77,448),(5980,1,79,448),(5981,1,81,448),(5982,1,83,448),(5983,1,85,448),(5984,1,87,448),(5985,1,89,448),(5986,1,91,448),(5987,1,93,448),(5988,1,95,448),(5989,1,97,448),(5990,1,98,448),(5991,1,99,448),(5992,1,100,448),(5993,1,101,448),(5994,1,102,448);
/*!40000 ALTER TABLE `sigl_pj_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_group_role`
--

DROP TABLE IF EXISTS `sigl_pj_group_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_group_role` (
  `id_group_role` int(11) NOT NULL AUTO_INCREMENT,
  `id_group` int(10) unsigned NOT NULL,
  `id_role` int(11) NOT NULL,
  PRIMARY KEY (`id_group_role`),
  KEY `id_role` (`id_role`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_group_role`
--

LOCK TABLES `sigl_pj_group_role` WRITE;
/*!40000 ALTER TABLE `sigl_pj_group_role` DISABLE KEYS */;
INSERT INTO `sigl_pj_group_role` VALUES (1,100,1);
/*!40000 ALTER TABLE `sigl_pj_group_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_module`
--

DROP TABLE IF EXISTS `sigl_pj_module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_module` (
  `id_module` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `version` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_module`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_module`
--

LOCK TABLES `sigl_pj_module` WRITE;
/*!40000 ALTER TABLE `sigl_pj_module` DISABLE KEYS */;
INSERT INTO `sigl_pj_module` VALUES (1,'default',NULL),(2,'auth',NULL),(3,'style',NULL),(4,'mainframe',NULL),(5,'form',NULL),(6,'admin',NULL),(7,'result',NULL),(8,'graph',NULL);
/*!40000 ALTER TABLE `sigl_pj_module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_module_acl`
--

DROP TABLE IF EXISTS `sigl_pj_module_acl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_module_acl` (
  `id_module_acl` int(11) NOT NULL AUTO_INCREMENT,
  `id_module` int(11) NOT NULL,
  `code` varchar(45) NOT NULL,
  `label` varchar(50) NOT NULL,
  PRIMARY KEY (`id_module_acl`),
  KEY `id_module` (`id_module`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_module_acl`
--

LOCK TABLES `sigl_pj_module_acl` WRITE;
/*!40000 ALTER TABLE `sigl_pj_module_acl` DISABLE KEYS */;
INSERT INTO `sigl_pj_module_acl` VALUES (1,1,'use','Utiliser le module par défaut'),(2,2,'use','Utiliser le module d\'authentification'),(3,3,'use','Utiliser les feuilles de styles'),(4,4,'use','Utiliser le module d\'affichage de page'),(5,5,'use','Utiliser les formulaires'),(6,6,'use','Utiliser le module d\'administration'),(7,7,'use','Utiliser le module résultat'),(8,7,'enter_results','Saisir des résultats'),(9,7,'technical_validation','Valider techniquement'),(10,7,'biological_validation','Valider biologiquement'),(11,8,'use','Utiliser le module graphe'),(12,4,'100','Saisir un dossier patient externe'),(13,4,'200','Saisir un dossier patient hospitalisé'),(14,4,'300','Gérer les produits pathologiques'),(15,4,'400','Lister les dossiers'),(17,4,'600','Gérer les utilisateurs'),(18,4,'700','Gérer les praticiens (prescripteurs)'),(19,4,'900','Gérer le référentiel des analyses'),(20,4,'1100','Gérer les dictionnaires'),(21,4,'1200','Gérer les préférences'),(22,6,'loadxmlresource','Mettre à jour la base de données'),(23,4,'500','Modifier son propre compte'),(24,4,'800','Créer un patient'),(25,4,'1300','Contrôle qualité');
/*!40000 ALTER TABLE `sigl_pj_module_acl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_monitoring`
--

DROP TABLE IF EXISTS `sigl_pj_monitoring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_monitoring` (
  `id_monitoring` int(11) NOT NULL AUTO_INCREMENT,
  `id_client` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `last_access` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_monitoring`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_monitoring`
--

LOCK TABLES `sigl_pj_monitoring` WRITE;
/*!40000 ALTER TABLE `sigl_pj_monitoring` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_pj_monitoring` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_monitoring_detail`
--

DROP TABLE IF EXISTS `sigl_pj_monitoring_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_monitoring_detail` (
  `id_monitoring_detail` int(11) NOT NULL AUTO_INCREMENT,
  `id_monitoring` int(11) NOT NULL,
  `varset_name` char(50) NOT NULL,
  `id_data` int(11) NOT NULL,
  `id_var` char(50) NOT NULL,
  PRIMARY KEY (`id_monitoring_detail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_monitoring_detail`
--

LOCK TABLES `sigl_pj_monitoring_detail` WRITE;
/*!40000 ALTER TABLE `sigl_pj_monitoring_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_pj_monitoring_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_old_passwords`
--

DROP TABLE IF EXISTS `sigl_pj_old_passwords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_old_passwords` (
  `id_old_password` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id_group` int(11) unsigned NOT NULL,
  `date_renew` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `password` char(81) NOT NULL,
  PRIMARY KEY (`id_old_password`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Gestion des anciens mdp';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_old_passwords`
--

LOCK TABLES `sigl_pj_old_passwords` WRITE;
/*!40000 ALTER TABLE `sigl_pj_old_passwords` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_pj_old_passwords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_query`
--

DROP TABLE IF EXISTS `sigl_pj_query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_query` (
  `id_query` int(11) NOT NULL AUTO_INCREMENT,
  `type_request` int(11) NOT NULL,
  `id_resource` int(11) NOT NULL,
  PRIMARY KEY (`id_query`),
  UNIQUE KEY `sigl_pj_query_resource` (`id_resource`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_query`
--

LOCK TABLES `sigl_pj_query` WRITE;
/*!40000 ALTER TABLE `sigl_pj_query` DISABLE KEYS */;
INSERT INTO `sigl_pj_query` VALUES (1,2,2001),(2,2,2002),(3,2,2003),(5,1,2005),(6,2,2006),(7,1,2007),(8,2,2008),(9,1,2009);
/*!40000 ALTER TABLE `sigl_pj_query` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_query_var`
--

DROP TABLE IF EXISTS `sigl_pj_query_var`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_query_var` (
  `id_query_var` int(11) NOT NULL AUTO_INCREMENT,
  `id_query` int(11) NOT NULL,
  `id_varset` int(11) NOT NULL,
  `id_var` varchar(50) NOT NULL,
  PRIMARY KEY (`id_query_var`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_query_var`
--

LOCK TABLES `sigl_pj_query_var` WRITE;
/*!40000 ALTER TABLE `sigl_pj_query_var` DISABLE KEYS */;
INSERT INTO `sigl_pj_query_var` VALUES (1,1,4,'anonyme'),(2,2,4,'anonyme'),(3,3,7,'profil'),(5,5,9,'formule_unite2'),(6,6,3,'colis'),(7,7,3,'date_prescription'),(8,7,3,'date_dos'),(9,8,4,'ddn_approx'),(10,9,12,'produit_biologique'),(11,9,12,'ref_analyse');
/*!40000 ALTER TABLE `sigl_pj_query_var` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_random`
--

DROP TABLE IF EXISTS `sigl_pj_random`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_random` (
  `id_random` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rid` varchar(32) NOT NULL DEFAULT '',
  `random` varchar(32) NOT NULL,
  PRIMARY KEY (`id_random`),
  UNIQUE KEY `UNIQUE` (`rid`,`random`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_random`
--

LOCK TABLES `sigl_pj_random` WRITE;
/*!40000 ALTER TABLE `sigl_pj_random` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_pj_random` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_resource`
--

DROP TABLE IF EXISTS `sigl_pj_resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_resource` (
  `id_resource` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `type` varchar(20) NOT NULL,
  `content` blob,
  `filename` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id_resource`)
) ENGINE=InnoDB AUTO_INCREMENT=20001 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_resource`
--

LOCK TABLES `sigl_pj_resource` WRITE;
/*!40000 ALTER TABLE `sigl_pj_resource` DISABLE KEYS */;
INSERT INTO `sigl_pj_resource` VALUES (1,'dictionnaire','varset',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<varset name=\"dico\" prefix=\"dico\" type=\"sys\" label=\"Dictionary\">\n  <var uid=\"1\" id=\"dico_name\" type=\"string\" mandatory=\"true\" default_label=\"Dictionary\" default_short_label=\"Dictionary\">\n    <string length=\"100\" regexp=\"^[a-zA-Z0-9_]*$\"/>\n  </var>\n  <var uid=\"2\" id=\"label\" type=\"string\" mandatory=\"true\" default_label=\"Label\" default_short_label=\"Label\">\n    <string length=\"255\"/>\n  </var>\n  <var uid=\"3\" id=\"short_label\" type=\"string\" mandatory=\"false\" default_label=\"Short label\" default_short_label=\"Short label\">\n    <string length=\"30\"/>\n  </var>\n  <var uid=\"4\" id=\"position\" type=\"integer\" mandatory=\"false\" default_label=\"Position\" default_short_label=\"Pos.\">\n  <integer min=\"0\" max=\"99999\"/>\n  </var>\n  <var uid=\"5\" id=\"code\" type=\"string\" mandatory=\"true\" default_label=\"Code\" default_short_label=\"Code\">\n    <string length=\"10\"/>\n  </var>\n  <var uid=\"6\" id=\"dico_id\" type=\"string\" mandatory=\"false\" default_label=\"Dico id\" default_short_label=\"Dico id\">\n<string length=\"40\"/>\n  </var>\n<var uid=\"7\" id=\"dico_value_id\" type=\"string\" mandatory=\"false\" default_label=\"Dico id\" default_short_label=\"Dico id\">\n<string length=\"40\"/>\n  </var><var uid=\"8\" id=\"archived\" type=\"boolean\" mandatory=\"false\" default_label=\"Is archived\" default_short_label=\"Is archived\"/></varset>',NULL),(2,'prelevement','varset',NULL,'/xml/2_varset_prelevement.xml'),(3,'dossier','varset',NULL,'/xml/3_varset_dossier.xml'),(4,'patient','varset',NULL,'/xml/4_varset_patient.xml'),(5,'analyse','varset',NULL,'/xml/5_varset_analyse.xml'),(6,'ref_analyse','varset',NULL,'/xml/6_varset_ref_analyse.xml'),(7,'user','varset',NULL,'/xml/7_varset_user.xml'),(8,'preference','varset',NULL,'/xml/8_varset_preference.xml'),(9,'ref_variable','varset',NULL,'/xml/9_varset_ref_variable.xml'),(10,'resultat','varset',NULL,'/xml/10_varset_resultat.xml'),(12,'praticien','varset',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<varset name=\"praticien\">\r\n	<!-- RSL - 20161229 : MaJ varset avec uid -->\r\n	<var uid=\"1\" id=\"code\" type=\"string\" mandatory=\"false\" default_label=\"Code\" default_short_label=\"Code\">\r\n		<string length=\"7\"/>\r\n	</var>\r\n	<var uid=\"2\" id=\"nom\" type=\"string\" mandatory=\"true\" default_label=\"Nom\" default_short_label=\"Nom\">\r\n		<string length=\"40\"/>\r\n	</var>\r\n	<var uid=\"3\" id=\"prenom\" type=\"string\" mandatory=\"false\" default_label=\"Prénom\" default_short_label=\"Prénom\">\r\n		<string length=\"40\"/>\r\n	</var>\r\n	<var uid=\"4\" id=\"ville\" type=\"string\" mandatory=\"false\" default_label=\"Ville\" default_short_label=\"Ville\">\r\n		<string length=\"50\"/>\r\n	</var>\r\n	<var uid=\"5\" id=\"etablissement\" type=\"string\" mandatory=\"false\" default_label=\"Etablissement\" default_short_label=\"Etablissement\">\r\n		<string length=\"50\"/>\r\n	</var>\r\n	<var uid=\"6\" id=\"specialite\" type=\"fkey_dico\" mandatory=\"false\" default_label=\"Spécialité\" default_short_label=\"Spécialité\">\r\n		<fkey_dico dico_name=\"specialite\"/>\r\n	</var>\r\n	<var uid=\"7\" id=\"tel\" type=\"string\" mandatory=\"false\" default_label=\"Téléphone\" default_short_label=\"Tél.\">\r\n		<string length=\"20\"/>\r\n	</var>\r\n	<var uid=\"8\" id=\"email\" type=\"string\" mandatory=\"false\" default_label=\"Email\" default_short_label=\"Email\">\r\n		<string length=\"50\"/>\r\n	</var>\r\n</varset>\r\n',NULL),(13,'refanalyse_refvariable','varset',NULL,'/xml/13_varset_refanalyse_refvariable.xml'),(14,'analyse_combine_individuelle','varset',NULL,'/xml/14_varset_analyse_combine_individuelle.xml'),(15,'validation','varset',NULL,'/xml/15_varset_validation.xml'),(16,'dos_file','varset',NULL,'/xml/16_varset_dos_file.xml'),(17,'evenements','varset',NULL,'/xml/17_varset_evenements.xml'),(18,'monitoring','varset',NULL,'/xml/18_varset_monitoring.xml'),(19,'query','varset',NULL,'/xml/19_varset_query.xml'),(20,'queryvar','varset',NULL,'/xml/20_varset_queryvar.xml'),(32,'surveillance','varset',NULL,'/xml/32_varset_surveillance.xml'),(33,'indicateur','varset',NULL,'/xml/33_varset_indicateur.xml'),(34,'surveillance_refvariable','varset',NULL,'/xml/34_varset_surveillance_refvariable.xml'),(35,'resource','varset',NULL,'/xml/35_varset_resource.xml'),(100,'demande_externe','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"one\">\n	<frame id=\"main\" url=\"form/frame/displayexternalfile/id/101\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(101,'recherche_patient_externe','form',NULL,'/xml/101_form_recherche_patient_externe.xml'),(103,'dossier_externe','form',NULL,'/xml/103_form_dossier_externe.xml'),(104,'dossier_confirmation_externe','form',NULL,'/xml/104_form_dossier_confirmation_externe.xml'),(105,'dossier_admin','form',NULL,'/xml/105_form_dossier_admin.xml'),(106,'facturation','etat',NULL,'/xml/106_etat_facturation.xml'),(200,'demande_interne','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"one\">\n	<frame id=\"main\" url=\"form/frame/displayinternalfile/id/201\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(201,'recherche_patient_interne','form',NULL,'/xml/201_form_recherche_patient_interne.xml'),(203,'dossier_interne','form',NULL,'/xml/203_form_dossier_interne.xml'),(204,'dossier_confirmation_interne','form',NULL,'/xml/204_form_dossier_confirmation_interne.xml'),(300,'liste_prelevements','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"one\">\n	<frame id=\"main\" url=\"form/frame/display/id/301\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(301,'liste_prelevements','form',NULL,'/xml/301_form_liste_prelevements.xml'),(302,'prelevements','form',NULL,'/xml/302_form_prelevements.xml'),(400,'liste_dossiers','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"one\">\n	<frame id=\"main\" url=\"form/frame/display/id/401\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(401,'liste_dossiers','form',NULL,'/xml/401_form_liste_dossiers.xml'),(500,'account','xml',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"account\">\n	<frame id=\"account\" url=\"form/frame/display/id/501\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(600,'utilisateur','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"admin\">\n	<frame id=\"admin\" url=\"form/frame/display/id/602\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(601,'utilisateur','form',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<form id=\"admin_form\">\n	<config/>\n	<data_structure>\n		<!-- Utilisateur -->\n		<dataquery id=\"utilisateur\" table_name=\"sigl_user_data\" varset_name=\"user\" table_alias=\"user\">\n			<column_simple field_name=\"id_data\" table_name=\"user\"/>\n			<column_simple field_name=\"login\" table_name=\"user\"/>\n			<column_simple field_name=\"password\" table_name=\"user\"/>\n			<column sql=\"NULL\" alias=\"password_confirm\" type=\"string\"/>\n			<column_simple field_name=\"titre\" table_name=\"user\"/>\n			<column_simple field_name=\"lastname\" table_name=\"user\"/>\n			<column_simple field_name=\"firstname\" table_name=\"user\"/>\n			<column_simple field_name=\"profil\" table_name=\"user\"/>\n			<column_simple field_name=\"profil_bis\" table_name=\"user\"/>\n			<column_simple field_name=\"id_owner\" table_name=\"user\"/>\n			<condition sql=\"{id_data}={param_id_data}\">\n				<field field_name=\"id_data\" table_name=\"user\" alias=\"id_data\"/>\n				<variable alias=\"param_id_data\" default=\"NULL\">\n					<entry type=\"param\" name=\"id_data\"/>\n				</variable>\n			</condition>\n		</dataquery>\n	</data_structure>\n	<layout title=\"Utilisateurs\" disabled=\"true\">\n		<group id=\"users-group\" title=\"Utilisateurs\" disabled=\"false\">\n			<group>\n				<label dataset=\"utilisateur\" field=\"login\"/>\n				<value dataset=\"utilisateur\" field=\"login\" mode=\"rw\">\n					<option output=\"html\" option_name=\"focus\" value=\"true\"/>\n				</value>\n				<clear/>\n				<sigl_field_password id=\"password\" dataset=\"utilisateur\" field=\"password\" mode=\"rw\">\n					<option output=\"html\" option_name=\"widget\" value=\"WidgetFieldPassword\"/>\n					<option output=\"html\" option_name=\"password\" value=\"true\"/>\n				</sigl_field_password>\n				<clear/>\n				<sigl_confirm_password dataset=\"utilisateur\" field=\"password_confirm\" mode=\"rw\">\n					<option output=\"html\" option_name=\"widget\" value=\"sigl_confirm_password\"/>\n				</sigl_confirm_password>\n				<clear/>\n				<label dataset=\"utilisateur\" field=\"titre\"/>\n				<value dataset=\"utilisateur\" field=\"titre\" mode=\"rw\">\n					<option output=\"html\" option_name=\"widget\" value=\"WidgetSelect\"/>\n				</value>\n				<clear/>\n				<label dataset=\"utilisateur\" field=\"lastname\"/>\n				<value dataset=\"utilisateur\" field=\"lastname\" mode=\"rw\"/>\n				<clear/>\n				<label dataset=\"utilisateur\" field=\"firstname\"/>\n				<value dataset=\"utilisateur\" field=\"firstname\" mode=\"rw\"/>\n				<clear/>\n				<label dataset=\"utilisateur\" field=\"profil\"/>\n				<value dataset=\"utilisateur\" field=\"profil\" mode=\"rw\">\n					<option output=\"html\" option_name=\"render\" value=\"checkbox\"/>\n				</value>\n			</group>\n			<!-- group query_id=\"3\" id=\"profil\"-->\n				<!-- label dataset=\"utilisateur\" field=\"profil_bis\"/-->\n				<!-- value dataset=\"utilisateur\" field=\"profil_bis\" mode=\"rw\" -->\n					<!-- option output=\"html\" option_name=\"render\" value=\"checkbox\"/-->\n				<!-- /value-->\n			<!-- /group-->\n		</group>\n		<group id=\"button-group\">\n			<sigl_save_utilisateur action=\"save\" id=\"save\" label=\"Enregistrer\">\n				<option output=\"html\" option_name=\"widget\" value=\"sigl_save_utilisateur\"/>\n				<redirection module=\"form\" ctrl=\"frame\" action=\"get\">\n					<params>\n						<value alias=\"id\">602</value>\n					</params>\n				</redirection>\n			</sigl_save_utilisateur>\n			<button action=\"exit\" id=\"exit\" label=\"Quitter\">\n				<redirection module=\"form\" ctrl=\"frame\" action=\"get\">\n					<params>\n						<value alias=\"id\">602</value>\n					</params>\n				</redirection>\n			</button>\n		</group>\n	</layout>\n</form>\n',NULL),(602,'liste_utilisateurs','form',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<form id=\"admin_form\">\n	<config/>\n	<data_structure>\n		<!-- Utilisateur -->\n		<dataquery id=\"utilisateur\" table_name=\"sigl_user_data\" varset_name=\"user\" table_alias=\"user\">\n			<column_simple field_name=\"id_data\" table_name=\"user\"/>\n			<column_simple field_name=\"login\" table_name=\"user\"/>\n			<column_simple field_name=\"titre\" table_name=\"user\"/>\n			<column_simple field_name=\"firstname\" table_name=\"user\"/>\n			<column_simple field_name=\"lastname\" table_name=\"user\"/>\n			<column_simple field_name=\"profil\" table_name=\"user\"/>\n		</dataquery>\n	</data_structure>\n	<layout title=\"Liste des utilisateurs\" disabled=\"false\">\n		<group>\n			<group>\n				<sigl_listing_utilisateurs id=\"listing_utilisateur\" dataset=\"utilisateur\" mode=\"r\">\n					<options>\n						<option output=\"html\" option_name=\"actions_render\" value=\"context_menu_link\"/>\n						<option output=\"html\" option_name=\"edit_form_id\" value=\"601\"/>\n						<option output=\"html\" option_name=\"edit_param_name\" value=\"id_data\"/>\n						<option output=\"html\" option_name=\"edit_param_field\" value=\"id_data\"/>\n					</options>\n					<option output=\"html\" option_name=\"widget\" value=\"sigl_listing_utilisateurs\"/>\n					<columns>\n						<column field=\"login\" title=\"Login\" mode=\"r\"/>\n						<column field=\"titre\" title=\"Titre\" mode=\"r\"/>\n						<column field=\"firstname\" title=\"Prénom\" mode=\"r\"/>\n						<column field=\"lastname\" title=\"Nom\" mode=\"r\"/>\n						<column field=\"profil\" title=\"Profil\" mode=\"r\"/>\n					</columns>\n				</sigl_listing_utilisateurs>\n			</group>\n		</group>\n		<group id=\"button-group\">\n			<button action=\"exit\" id=\"exit\" label=\"Ajouter un nouvel utilisateur\">\n				<redirection module=\"form\" ctrl=\"frame\" action=\"get\">\n					<params>\n						<value alias=\"id\">601</value>\n					</params>\n				</redirection>\n			</button>\n		</group>\n	</layout>\n</form>\n',NULL),(603,'edit_user','xml',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<form id=\"admin_form\">\n	<config/>\n	<data_structure>\n		<!-- Utilisateur -->\n		<dataquery id=\"utilisateur\" table_name=\"sigl_user_data\" varset_name=\"user\" table_alias=\"user\">\n			<column_simple field_name=\"id_data\" table_name=\"user\"/>\n			<column_simple field_name=\"login\" table_name=\"user\"/>\n			<column_simple field_name=\"password\" table_name=\"user\"/>\n			<column_simple field_name=\"titre\" table_name=\"user\"/>\n			<column_simple field_name=\"lastname\" table_name=\"user\"/>\n			<column_simple field_name=\"firstname\" table_name=\"user\"/>\n			<column_simple field_name=\"profil\" table_name=\"user\"/>\n			<column_simple field_name=\"profil_bis\" table_name=\"user\"/>\n			<column_simple field_name=\"id_owner\" table_name=\"user\"/>\n			<condition sql=\"{id_data}={param_id_data}\">\n				<field field_name=\"id_data\" table_name=\"user\" alias=\"id_data\"/>\n				<variable alias=\"param_id_data\" default=\"NULL\">\n					<entry type=\"param\" name=\"id_data\"/>\n				</variable>\n			</condition>\n		</dataquery>\n	</data_structure>\n	<layout title=\"Utilisateurs\" disabled=\"true\">\n		<group id=\"users-group\" title=\"Utilisateurs\" disabled=\"false\">\n			<group>\n				<label dataset=\"utilisateur\" field=\"login\"/>\n				<value dataset=\"utilisateur\" field=\"login\" mode=\"r\">\n					<option output=\"html\" option_name=\"focus\" value=\"true\"/>\n				</value>\n				<clear/>\n				<label dataset=\"utilisateur\" field=\"titre\"/>\n				<value dataset=\"utilisateur\" field=\"titre\" mode=\"rw\">\n					<option output=\"html\" option_name=\"widget\" value=\"WidgetSelect\"/>\n				</value>\n				<clear/>\n				<label dataset=\"utilisateur\" field=\"lastname\"/>\n				<value dataset=\"utilisateur\" field=\"lastname\" mode=\"rw\"/>\n				<clear/>\n				<label dataset=\"utilisateur\" field=\"firstname\"/>\n				<value dataset=\"utilisateur\" field=\"firstname\" mode=\"rw\"/>\n				<clear/>\n				<label dataset=\"utilisateur\" field=\"profil\"/>\n				<value dataset=\"utilisateur\" field=\"profil\" mode=\"rw\">\n					<option output=\"html\" option_name=\"render\" value=\"checkbox\"/>\n				</value>\n			</group>\n			<!-- group query_id=\"3\" id=\"profil\"-->\n				<!-- label dataset=\"utilisateur\" field=\"profil_bis\"/-->\n				<!-- value dataset=\"utilisateur\" field=\"profil_bis\" mode=\"rw\" -->\n					<!-- option output=\"html\" option_name=\"render\" value=\"checkbox\"/-->\n				<!-- /value-->\n			<!-- /group-->\n		</group>\n		<group id=\"button-group\">\n			<sigl_save_utilisateur action=\"save\" id=\"save\" label=\"Enregistrer\">\n				<option output=\"html\" option_name=\"widget\" value=\"sigl_save_utilisateur\"/>\n				<redirection module=\"form\" ctrl=\"frame\" action=\"get\">\n					<params>\n						<value alias=\"id\">602</value>\n					</params>\n				</redirection>\n			</sigl_save_utilisateur>\n			<button action=\"exit\" id=\"exit\" label=\"Quitter\">\n				<redirection module=\"form\" ctrl=\"frame\" action=\"get\">\n					<params>\n						<value alias=\"id\">602</value>\n					</params>\n				</redirection>\n			</button>\n		</group>\n	</layout>\n</form>\n',NULL),(604,'edit_pwd','xml',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<form id=\"admin_form\">\n	<config/>\n	<data_structure>\n		<!-- Utilisateur -->\n		<dataquery id=\"utilisateur\" table_name=\"sigl_user_data\" varset_name=\"user\" table_alias=\"user\">\n			<column_simple field_name=\"id_data\" table_name=\"user\"/>\n			<column_simple field_name=\"login\" table_name=\"user\"/>\n			<column_simple field_name=\"password\" table_name=\"user\"/>\n			<column sql=\"NULL\" alias=\"password_confirm\" type=\"string\"/>\n			<column_simple field_name=\"profil\" table_name=\"user\"/>\n			<column_simple field_name=\"id_owner\" table_name=\"user\"/>\n			<condition sql=\"{id_data}={param_id_data}\">\n				<field field_name=\"id_data\" table_name=\"user\" alias=\"id_data\"/>\n				<variable alias=\"param_id_data\" default=\"NULL\">\n					<entry type=\"param\" name=\"id_data\"/>\n				</variable>\n			</condition>\n		</dataquery>\n	</data_structure>\n	<layout title=\"Utilisateurs\" disabled=\"true\">\n		<group id=\"users-group\" title=\"Utilisateurs\" disabled=\"false\">\n			<group>\n				<sigl_field_password id=\"password\" dataset=\"utilisateur\" field=\"password\" mode=\"rw\">\n					<option output=\"html\" option_name=\"widget\" value=\"WidgetFieldPassword\"/>\n					<option output=\"html\" option_name=\"password\" value=\"true\"/>\n				</sigl_field_password>\n				<clear/>\n				<sigl_confirm_password dataset=\"utilisateur\" field=\"password_confirm\" mode=\"rw\">\n					<option output=\"html\" option_name=\"widget\" value=\"sigl_confirm_password\"/>\n				</sigl_confirm_password>\n				<clear/>\n			</group>\n			<!-- group query_id=\"3\" id=\"profil\"-->\n				<!-- label dataset=\"utilisateur\" field=\"profil_bis\"/-->\n				<!-- value dataset=\"utilisateur\" field=\"profil_bis\" mode=\"rw\" -->\n					<!-- option output=\"html\" option_name=\"render\" value=\"checkbox\"/-->\n				<!-- /value-->\n			<!-- /group-->\n		</group>\n		<group id=\"button-group\">\n			<sigl_save_utilisateur action=\"save\" id=\"save\" label=\"Enregistrer\">\n				<option output=\"html\" option_name=\"widget\" value=\"sigl_save_utilisateur\"/>\n				<redirection module=\"form\" ctrl=\"frame\" action=\"get\">\n					<params>\n						<value alias=\"id\">602</value>\n					</params>\n				</redirection>\n			</sigl_save_utilisateur>\n			<button action=\"exit\" id=\"exit\" label=\"Quitter\">\n				<redirection module=\"form\" ctrl=\"frame\" action=\"get\">\n					<params>\n						<value alias=\"id\">602</value>\n					</params>\n				</redirection>\n			</button>\n		</group>\n	</layout>\n</form>\n',NULL),(700,'liste_praticiens','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"one\">\n	<frame id=\"main\" url=\"form/frame/display/id/701\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(701,'liste_praticiens','form',NULL,NULL),(702,'praticiens','form',NULL,NULL),(900,'ref_analyse','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"admin\">\n	<frame id=\"admin\" url=\"form/frame/display/id/901\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(901,'liste_ref_analyse','form',NULL,'/xml/901_form_liste_ref_analyse.xml'),(902,'ref_analyse','form',NULL,'/xml/902_form_ref_analyse.xml'),(903,'ref_analyse_new','form',NULL,'/xml/903_form_ref_analyse_new.xml'),(1001,'numero_dossier_jour','sequence',NULL,'/xml/1001_sequence_numero_dossier_jour.xml'),(1002,'numero_dossier_an','sequence',NULL,'/xml/1002_sequence_numero_dossier_an.xml'),(1100,'dico','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"admin\">\n	<frame id=\"admin\" url=\"form/frame/display/id/1101\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(1200,'preference','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"admin\">\n  <frame id=\"admin\" url=\"form/frame/display/id/1201\" classname=\"FrameForm\"/>\n</mainframe>\n',NULL),(1201,'liste_preference','form',NULL,'/xml/1201_form_liste_preference.xml'),(1500,'liste_stats','form','','/xml/1500_form_liste_stats.xml'),(1501,'stats','form','','/xml/1501_form_stats.xml'),(2000,'dev','mainframe',_binary '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mainframe layout=\"one\">\n\n	<!-- New patient -->\n	<!-- frame id=\"main\" url=\"form/frame/display/id/202\" classname=\"FrameForm\"/-->\n\n	<!-- Form dossier -->\n	<!--frame id=\"main\" url=\"form/frame/display/id/103/id_patient/6/id_dos/113\" classname=\"FrameForm\"/-->\n	<!--frame id=\"main\" url=\"form/frame/display/id/103/id_patient/6\" classname=\"FrameForm\"/-->\n\n	<!-- Form dossier confirmation -->\n	<!--frame id=\"main\" url=\"form/frame/display/id/204/id_dossier/113\" classname=\"FrameForm\"/-->\n\n	<!-- Form dossier admin -->\n	<frame id=\"main\" url=\"form/frame/display/id/105/id_dossier/113\" classname=\"FrameForm\"/>\n\n	<!-- listing -->\n	<!--frame id=\"main\" url=\"form/frame/display/id/302/id_prel/10/num_dos_an/2012000009\"/-->\n</mainframe>\n',NULL),(2001,'patient_anonyme_(query_1)','query',NULL,'/xml/2001_query_patient_anonyme_(query_1).xml'),(2002,'patient_non_anonyme_(query_2)','query',NULL,'/xml/2002_query_patient_non_anonyme_(query_2).xml'),(2003,'profil_bis_(query_3)','query',NULL,'/xml/2003_query_profil_bis_(query_3).xml'),(2004,'type_prelevement','query',NULL,'/xml/2004_query_type_prelevement.xml'),(2005,'formule_unite2_(query_5)','query',NULL,'/xml/2005_query_formule_unite2_(query_5).xml'),(2006,'colis_(query_6)','query',NULL,'/xml/2006_query_colis_(query_6).xml'),(2007,'dates_dos_(query_7)','query',NULL,'/xml/2007_query_dates_dos_(query_7).xml'),(2008,'ddn_approx_(query_8)','query',NULL,'/xml/2008_query_ddn_approx_(query_8).xml'),(3000,'default','style',NULL,'/xml/3000_style_default.xml'),(10000,'access_control_list','acl',NULL,'/xml/10000_acl_access_control_list.xml'),(20000,'sigl','project','','/xml/20000_project_sigl.xml');
/*!40000 ALTER TABLE `sigl_pj_resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_resource_settings`
--

DROP TABLE IF EXISTS `sigl_pj_resource_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_resource_settings` (
  `id_resource_settings` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_resource` int(10) unsigned NOT NULL,
  `id_user` int(10) unsigned DEFAULT NULL,
  `id_settings` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_resource_settings`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_resource_settings`
--

LOCK TABLES `sigl_pj_resource_settings` WRITE;
/*!40000 ALTER TABLE `sigl_pj_resource_settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_pj_resource_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_role`
--

DROP TABLE IF EXISTS `sigl_pj_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_role` (
  `id_role` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `label` varchar(100) NOT NULL,
  PRIMARY KEY (`id_role`),
  UNIQUE KEY `sigl_pj_role` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_role`
--

LOCK TABLES `sigl_pj_role` WRITE;
/*!40000 ALTER TABLE `sigl_pj_role` DISABLE KEYS */;
INSERT INTO `sigl_pj_role` VALUES (1,'admin','Administrateur'),(2,'biologiste','Biologiste'),(3,'technicien','Technicien'),(4,'secretaire','Secrétaire'),(5,'technicien avance','Technicien avancé'),(6,'technicien qualiticien','Technicien qualiticien'),(7,'secretaire avancee','secrétaire avancée'),(8,'qualiticien','Qualiticien'),(9,'prescripteur','Prescripteur');
/*!40000 ALTER TABLE `sigl_pj_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_role_acl`
--

DROP TABLE IF EXISTS `sigl_pj_role_acl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_role_acl` (
  `id_role_acl` int(11) NOT NULL AUTO_INCREMENT,
  `id_role` int(11) NOT NULL,
  `id_module_acl` int(11) NOT NULL,
  PRIMARY KEY (`id_role_acl`),
  KEY `id_role` (`id_role`),
  KEY `id_module_acl` (`id_module_acl`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_role_acl`
--

LOCK TABLES `sigl_pj_role_acl` WRITE;
/*!40000 ALTER TABLE `sigl_pj_role_acl` DISABLE KEYS */;
INSERT INTO `sigl_pj_role_acl` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(8,1,6),(9,1,7),(10,2,1),(11,2,2),(12,2,3),(13,2,4),(14,2,5),(15,2,6),(16,2,7),(17,3,1),(18,3,2),(19,3,3),(20,3,4),(21,3,5),(22,3,6),(23,3,7),(24,1,8),(25,1,9),(26,1,10),(27,3,8),(28,3,9),(29,4,1),(30,4,2),(31,4,3),(32,4,4),(33,4,5),(34,4,6),(35,4,7),(36,2,8),(37,2,9),(38,2,10),(39,1,11),(40,2,11),(41,3,11),(42,4,11),(43,1,17),(44,1,18),(45,1,19),(46,1,20),(47,1,21),(48,2,12),(49,2,13),(50,2,14),(51,2,15),(53,2,18),(54,2,19),(55,2,20),(56,2,21),(57,3,12),(58,3,13),(59,3,14),(60,3,15),(62,3,18),(63,3,21),(64,4,12),(65,4,13),(66,4,14),(67,4,15),(69,4,18),(70,4,21),(71,1,22),(72,1,23),(73,2,23),(74,3,23),(75,4,23),(76,2,24),(77,3,24),(78,4,24);
/*!40000 ALTER TABLE `sigl_pj_role_acl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_sequence`
--

DROP TABLE IF EXISTS `sigl_pj_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_sequence` (
  `id_sequence` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sid` varchar(32) NOT NULL DEFAULT '',
  `pattern` varchar(45) CHARACTER SET latin1 NOT NULL,
  `num` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_sequence`),
  UNIQUE KEY `UNIQUE` (`sid`,`pattern`,`num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_sequence`
--

LOCK TABLES `sigl_pj_sequence` WRITE;
/*!40000 ALTER TABLE `sigl_pj_sequence` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_pj_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_token`
--

DROP TABLE IF EXISTS `sigl_pj_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_token` (
  `id_token` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `token` varchar(8) NOT NULL,
  `id_group` int(10) unsigned DEFAULT NULL,
  `acl_resources` varchar(255) DEFAULT NULL,
  `group_mode` text,
  `context` text,
  `expire_date` date DEFAULT NULL,
  `session_id` varchar(32) DEFAULT NULL,
  `classname` varchar(40) DEFAULT NULL,
  `otp` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id_token`),
  KEY `idx_id_group` (`id_group`),
  KEY `token` (`token`),
  KEY `otp` (`otp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_token`
--

LOCK TABLES `sigl_pj_token` WRITE;
/*!40000 ALTER TABLE `sigl_pj_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_pj_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_pj_varset`
--

DROP TABLE IF EXISTS `sigl_pj_varset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_pj_varset` (
  `id_varset` int(11) NOT NULL AUTO_INCREMENT,
  `label` char(200) NOT NULL,
  `name` char(50) NOT NULL,
  `varset_table_prefix` char(50) NOT NULL,
  `id_resource` int(11) NOT NULL,
  `type` char(4) NOT NULL DEFAULT 'sys',
  PRIMARY KEY (`id_varset`),
  KEY `idx_varset_resource` (`id_resource`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_pj_varset`
--

LOCK TABLES `sigl_pj_varset` WRITE;
/*!40000 ALTER TABLE `sigl_pj_varset` DISABLE KEYS */;
INSERT INTO `sigl_pj_varset` VALUES (1,'Dictionnaire','dico','dico',1,'sys'),(2,'Prélèvement','prel','01',2,'std'),(3,'Dossier','dos','02',3,'std'),(4,'Patient','pat','03',4,'std'),(5,'Analyse','analyse','04',5,'std'),(6,'Ref Analyse','refanalyse','05',6,'std'),(7,'User','user','user',7,'sys'),(8,'Préférence','preference','06',8,'std'),(9,'Ref Variable','refvariable','07',9,'std'),(10,'Résultat','resultat','09',10,'std'),(12,'Praticien','praticien','08',12,'std'),(13,'Lookup ref analyse - ref variable','refanalyse_refvariable','05_07',13,'join'),(14,'Lookup analyse complexe - analyse individuelle','refanalyse_refanalyse','05_05',14,'join'),(15,'Validation','validation','10',15,'std'),(16,'Fichier attaché au dossier','dos_file','11',16,'std'),(17,'Evenements','evtlog','evtlog',17,'sys'),(18,'Monitoring','monitoring','varsetmonitor',18,'sys'),(19,'Query','query','query',19,'sys'),(20,'Query var','queryvar','queryvar',20,'sys'),(32,'Stats','surveillance','14',32,'std'),(33,'Indicateur','indicateur','15',33,'std'),(34,'Surveillance Refvariable','surveillance_refvariable','16',34,'std'),(35,'Resource','resource','resource',35,'std'),(37,'Dictionary status','dicostatus','dicostatus',20007,'sys'),(39,'varset_n16s','varset_n16s','varset_n16s',20009,'std'),(40,'fournisseurs','fournisseurs','fournisseurs',20011,'std'),(41,'procedures','procedures','procedures',20012,'std'),(42,'reunion','reunion','reunion',20015,'std'),(43,'manuels','manuels','manuels',20017,'std'),(45,'revue','revue','revue',20023,'std'),(47,'reunion_pj Fichiers','reunion_pj__file','reunion_pj__file',20027,'join'),(49,'Uploaded files','file','file',20029,'sys'),(51,'non_conf','non_conf','non_conf',20035,'std'),(53,'manuels_document Fichiers','manuels_document__file','manuels_document__file',20039,'join'),(55,'procedures_document Fichiers','procedures_document__file','procedures_document__file',20041,'join'),(57,'Storage','storage','storage',20045,'sys'),(59,'laboratoire','laboratoire','laboratoire',20053,'std'),(61,'revue_pj Fichiers','revue_pj__file','revue_pj__file',20057,'join'),(63,'qualite_general','qualite_general','qualite_general',20063,'std'),(65,'equipement','equipement','equipement',20067,'std'),(67,'equipement_photo Fichiers','equipement_photo__file','equipement_photo__file',20071,'join'),(69,'equipement_maintenance_preventive Fichiers','equipement_maintenance_preventive__file','equipement_maintenance_preventive__file',20073,'join'),(71,'equipement_certif_etalonnage Fichiers','equipement_certif_etalonnage__file','equipement_certif_etalonnage__file',20075,'join'),(73,'equipement_facture Fichiers','equipement_facture__file','equipement_facture__file',20077,'join'),(75,'equipement_pannes Fichiers','equipement_pannes__file','equipement_pannes__file',20079,'join'),(77,'equipement_contrat_maintenance Fichiers','equipement_contrat_maintenance__file','equipement_contrat_maintenance__file',20081,'join'),(79,'planning_ctrl_int','planning_ctrl_int','planning_ctrl_int',20085,'std'),(81,'controle_interne','controle_interne','controle_interne',20087,'std'),(83,'controle_externe','controle_externe','controle_externe',20095,'std'),(85,'planning_ctrl_ext','planning_ctrl_ext','planning_ctrl_ext',20097,'std'),(87,'controle_externe_ctrl_resultat Fichiers','controle_externe_ctrl_resultat__file','controle_externe_ctrl_resultat__file',20105,'join'),(89,'laboratoire_organigramme Fichiers','laboratoire_organigramme__file','laboratoire_organigramme__file',20107,'join'),(91,'user_cv Fichiers','user_cv__file','user_cv__file',20111,'join'),(93,'user_diplomes Fichiers','user_diplomes__file','user_diplomes__file',20113,'join'),(95,'user_formations Fichiers','user_formations__file','user_formations__file',20115,'join'),(97,'user_evaluation Fichiers','user_evaluation__file','user_evaluation__file',20117,'join'),(98,'dos_valisedoc Fichiers','dos_valisedoc__file','dos_valisedoc__file',20119,'join'),(99,'controle_externe_ctrl_resultat_cr Fichiers','controle_externe_ctrl_resultat_cr__file','controle_externe_ctrl_resultat_cr__file',20121,'join'),(100,'param_cr','param_cr','param_cr',20122,'std'),(101,'param_num_dos','param_num_dos','param_num_dos',20124,'std'),(102,'mgt_qlt','mgt_qlt','mgt_qlt',20126,'std');
/*!40000 ALTER TABLE `sigl_pj_varset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_planning_ctrl_ext_data`
--

DROP TABLE IF EXISTS `sigl_planning_ctrl_ext_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_planning_ctrl_ext_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `parametre` varchar(255) DEFAULT NULL,
  `date_ctrl` date DEFAULT NULL,
  `equipement_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_planning_ctrl_ext_data`
--

LOCK TABLES `sigl_planning_ctrl_ext_data` WRITE;
/*!40000 ALTER TABLE `sigl_planning_ctrl_ext_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_planning_ctrl_ext_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_planning_ctrl_ext_data_group`
--

DROP TABLE IF EXISTS `sigl_planning_ctrl_ext_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_planning_ctrl_ext_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_planning_ctrl_ext_data_group`
--

LOCK TABLES `sigl_planning_ctrl_ext_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_planning_ctrl_ext_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_planning_ctrl_ext_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_planning_ctrl_ext_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_planning_ctrl_ext_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_planning_ctrl_ext_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_planning_ctrl_ext_data_group_mode`
--

LOCK TABLES `sigl_planning_ctrl_ext_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_planning_ctrl_ext_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_planning_ctrl_ext_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_planning_ctrl_ext_deleted`
--

DROP TABLE IF EXISTS `sigl_planning_ctrl_ext_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_planning_ctrl_ext_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `parametre` varchar(255) DEFAULT NULL,
  `date_ctrl` date DEFAULT NULL,
  `equipement_id` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_planning_ctrl_ext_deleted`
--

LOCK TABLES `sigl_planning_ctrl_ext_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_planning_ctrl_ext_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_planning_ctrl_ext_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_planning_ctrl_int_data`
--

DROP TABLE IF EXISTS `sigl_planning_ctrl_int_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_planning_ctrl_int_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `parametre` varchar(255) DEFAULT NULL,
  `equipement_id` int(10) unsigned DEFAULT NULL,
  `periode` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_planning_ctrl_int_data`
--

LOCK TABLES `sigl_planning_ctrl_int_data` WRITE;
/*!40000 ALTER TABLE `sigl_planning_ctrl_int_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_planning_ctrl_int_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_planning_ctrl_int_data_group`
--

DROP TABLE IF EXISTS `sigl_planning_ctrl_int_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_planning_ctrl_int_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_planning_ctrl_int_data_group`
--

LOCK TABLES `sigl_planning_ctrl_int_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_planning_ctrl_int_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_planning_ctrl_int_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_planning_ctrl_int_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_planning_ctrl_int_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_planning_ctrl_int_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_planning_ctrl_int_data_group_mode`
--

LOCK TABLES `sigl_planning_ctrl_int_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_planning_ctrl_int_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_planning_ctrl_int_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_planning_ctrl_int_deleted`
--

DROP TABLE IF EXISTS `sigl_planning_ctrl_int_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_planning_ctrl_int_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `parametre` varchar(255) DEFAULT NULL,
  `equipement_id` int(10) unsigned DEFAULT NULL,
  `periode` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_planning_ctrl_int_deleted`
--

LOCK TABLES `sigl_planning_ctrl_int_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_planning_ctrl_int_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_planning_ctrl_int_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_procedures_data`
--

DROP TABLE IF EXISTS `sigl_procedures_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_procedures_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `reference` varchar(255) DEFAULT NULL,
  `titre` varchar(255) DEFAULT NULL,
  `date_insert` date DEFAULT NULL,
  `date_apply` date DEFAULT NULL,
  `date_update` date DEFAULT NULL,
  `section` int(10) unsigned DEFAULT NULL,
  `redacteur_id` int(10) unsigned DEFAULT NULL,
  `verificateur_id` int(10) unsigned DEFAULT NULL,
  `approbateur_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_procedures_data`
--

LOCK TABLES `sigl_procedures_data` WRITE;
/*!40000 ALTER TABLE `sigl_procedures_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_procedures_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_procedures_data_group`
--

DROP TABLE IF EXISTS `sigl_procedures_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_procedures_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_procedures_data_group`
--

LOCK TABLES `sigl_procedures_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_procedures_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_procedures_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_procedures_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_procedures_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_procedures_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_procedures_data_group_mode`
--

LOCK TABLES `sigl_procedures_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_procedures_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_procedures_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_procedures_deleted`
--

DROP TABLE IF EXISTS `sigl_procedures_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_procedures_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `reference` varchar(255) DEFAULT NULL,
  `titre` varchar(255) DEFAULT NULL,
  `date_insert` date DEFAULT NULL,
  `date_apply` date DEFAULT NULL,
  `date_update` date DEFAULT NULL,
  `section` int(10) unsigned DEFAULT NULL,
  `redacteur_id` int(10) unsigned DEFAULT NULL,
  `verificateur_id` int(10) unsigned DEFAULT NULL,
  `approbateur_id` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_procedures_deleted`
--

LOCK TABLES `sigl_procedures_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_procedures_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_procedures_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_procedures_document__file_data`
--

DROP TABLE IF EXISTS `sigl_procedures_document__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_procedures_document__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_procedures_document__file_data`
--

LOCK TABLES `sigl_procedures_document__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_procedures_document__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_procedures_document__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_procedures_document__file_data_group`
--

DROP TABLE IF EXISTS `sigl_procedures_document__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_procedures_document__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_procedures_document__file_data_group`
--

LOCK TABLES `sigl_procedures_document__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_procedures_document__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_procedures_document__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_procedures_document__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_procedures_document__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_procedures_document__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_procedures_document__file_data_group_mode`
--

LOCK TABLES `sigl_procedures_document__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_procedures_document__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_procedures_document__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_procedures_document__file_deleted`
--

DROP TABLE IF EXISTS `sigl_procedures_document__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_procedures_document__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_procedures_document__file_deleted`
--

LOCK TABLES `sigl_procedures_document__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_procedures_document__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_procedures_document__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_qualite_general_data`
--

DROP TABLE IF EXISTS `sigl_qualite_general_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_qualite_general_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_qualite_general_data`
--

LOCK TABLES `sigl_qualite_general_data` WRITE;
/*!40000 ALTER TABLE `sigl_qualite_general_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_qualite_general_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_qualite_general_data_group`
--

DROP TABLE IF EXISTS `sigl_qualite_general_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_qualite_general_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_qualite_general_data_group`
--

LOCK TABLES `sigl_qualite_general_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_qualite_general_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_qualite_general_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_qualite_general_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_qualite_general_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_qualite_general_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_qualite_general_data_group_mode`
--

LOCK TABLES `sigl_qualite_general_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_qualite_general_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_qualite_general_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_qualite_general_deleted`
--

DROP TABLE IF EXISTS `sigl_qualite_general_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_qualite_general_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_qualite_general_deleted`
--

LOCK TABLES `sigl_qualite_general_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_qualite_general_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_qualite_general_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_query_data`
--

DROP TABLE IF EXISTS `sigl_query_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_query_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type_request` int(1) unsigned DEFAULT NULL,
  `id_resource` int(11) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `request` text,
  `message` varchar(200) DEFAULT NULL,
  `level` int(10) unsigned DEFAULT NULL,
  `runlevel` int(10) unsigned DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `mode_avance` int(10) unsigned DEFAULT NULL,
  `cron_minute` varchar(200) DEFAULT NULL,
  `cron_hour` varchar(200) DEFAULT NULL,
  `cron_day` varchar(200) DEFAULT NULL,
  `cron_month` varchar(200) DEFAULT NULL,
  `cron_by_day` varchar(200) DEFAULT NULL,
  `cron_freq` int(10) unsigned DEFAULT NULL,
  `varset` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  UNIQUE KEY `sigl_pj_query_resource` (`id_resource`),
  KEY `sigl_query_data_owner` (`id_owner`),
  KEY `sigl_query_data_level_dico` (`level`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_query_data`
--

LOCK TABLES `sigl_query_data` WRITE;
/*!40000 ALTER TABLE `sigl_query_data` DISABLE KEYS */;
INSERT INTO `sigl_query_data` VALUES (1,2,2001,100,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,2,2002,100,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,2,2003,100,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,1,2005,100,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6,2,2006,100,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,1,2007,100,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8,2,2008,100,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sigl_query_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_query_data_group`
--

DROP TABLE IF EXISTS `sigl_query_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_query_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(11) NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_query_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_query_data_group`
--

LOCK TABLES `sigl_query_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_query_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_query_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_query_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_query_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_query_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_query_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_query_data_group_mode`
--

LOCK TABLES `sigl_query_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_query_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_query_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_query_deleted`
--

DROP TABLE IF EXISTS `sigl_query_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_query_deleted` (
  `id_data` int(11) NOT NULL,
  `type_request` int(1) unsigned DEFAULT NULL,
  `id_resource` int(11) unsigned DEFAULT NULL,
  `id_owner` int(11) unsigned NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `request` text,
  `message` varchar(200) DEFAULT NULL,
  `level` int(10) unsigned DEFAULT NULL,
  `runlevel` int(10) unsigned DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `mode_avance` int(10) unsigned DEFAULT NULL,
  `cron_minute` varchar(200) DEFAULT NULL,
  `cron_hour` varchar(200) DEFAULT NULL,
  `cron_day` varchar(200) DEFAULT NULL,
  `cron_month` varchar(200) DEFAULT NULL,
  `cron_by_day` varchar(200) DEFAULT NULL,
  `cron_freq` int(10) unsigned DEFAULT NULL,
  `varset` varchar(200) DEFAULT NULL,
  UNIQUE KEY `sigl_pj_query_resource` (`id_resource`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_query_deleted`
--

LOCK TABLES `sigl_query_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_query_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_query_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_query_dico_runlevel_data`
--

DROP TABLE IF EXISTS `sigl_query_dico_runlevel_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_query_dico_runlevel_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `id_query` int(10) unsigned NOT NULL,
  `id_dico` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_query` (`id_query`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_query_dico_runlevel_data`
--

LOCK TABLES `sigl_query_dico_runlevel_data` WRITE;
/*!40000 ALTER TABLE `sigl_query_dico_runlevel_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_query_dico_runlevel_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_queryvar_data`
--

DROP TABLE IF EXISTS `sigl_queryvar_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_queryvar_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_query` int(10) unsigned DEFAULT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_varset` int(10) NOT NULL,
  `id_var` varchar(255) NOT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_queryvar_data_owner` (`id_owner`),
  KEY `sigl_queryvar_data_id_query_query` (`id_query`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_queryvar_data`
--

LOCK TABLES `sigl_queryvar_data` WRITE;
/*!40000 ALTER TABLE `sigl_queryvar_data` DISABLE KEYS */;
INSERT INTO `sigl_queryvar_data` VALUES (1,1,100,4,'anonyme'),(2,2,100,4,'anonyme'),(3,3,100,7,'profil'),(5,5,100,9,'formule_unite2'),(6,6,100,3,'colis'),(7,7,100,3,'date_prescription'),(8,7,100,3,'date_dos'),(9,8,100,4,'ddn_approx');
/*!40000 ALTER TABLE `sigl_queryvar_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_queryvar_data_group`
--

DROP TABLE IF EXISTS `sigl_queryvar_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_queryvar_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(11) NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_queryvar_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_queryvar_data_group`
--

LOCK TABLES `sigl_queryvar_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_queryvar_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_queryvar_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_queryvar_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_queryvar_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_queryvar_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_queryvar_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_queryvar_data_group_mode`
--

LOCK TABLES `sigl_queryvar_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_queryvar_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_queryvar_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_queryvar_deleted`
--

DROP TABLE IF EXISTS `sigl_queryvar_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_queryvar_deleted` (
  `id_data` int(11) NOT NULL,
  `id_query` int(10) unsigned DEFAULT NULL,
  `id_owner` int(11) NOT NULL,
  `id_varset` int(10) NOT NULL,
  `id_var` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_queryvar_deleted`
--

LOCK TABLES `sigl_queryvar_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_queryvar_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_queryvar_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_resource_data`
--

DROP TABLE IF EXISTS `sigl_resource_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_resource_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `name` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `type` int(10) unsigned NOT NULL,
  `content` text COLLATE utf8_unicode_ci,
  `filename` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `resource_id` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_resource_data_owner` (`id_owner`),
  KEY `sigl_resource_data_type_dico` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=20133 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_resource_data`
--

LOCK TABLES `sigl_resource_data` WRITE;
/*!40000 ALTER TABLE `sigl_resource_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_resource_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_resource_data_group`
--

DROP TABLE IF EXISTS `sigl_resource_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_resource_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_resource_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_resource_data_group`
--

LOCK TABLES `sigl_resource_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_resource_data_group` DISABLE KEYS */;
INSERT INTO `sigl_resource_data_group` VALUES (1,20001,100),(2,20004,100),(3,20005,100),(5,20007,100),(7,20021,100),(9,20027,100),(11,20029,100),(13,20031,100),(15,20033,100),(17,20039,100),(19,20041,100),(21,20043,100),(23,20045,100),(25,20047,100),(27,20049,100),(29,20051,100),(31,20057,100),(33,20059,100),(35,20061,100),(37,20071,100),(39,20073,100),(41,20075,100),(43,20077,100),(45,20079,100),(47,20081,100),(49,20083,100),(51,20093,100),(53,20103,100),(55,20105,100),(57,20107,100),(59,20109,100),(61,20111,100),(63,20113,100),(65,20115,100),(67,20117,100),(68,20118,100),(69,20119,100),(70,20120,100),(71,20121,100),(72,20128,100),(73,20129,100),(74,20130,100),(75,20131,100),(76,20132,100);
/*!40000 ALTER TABLE `sigl_resource_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_resource_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_resource_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_resource_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_resource_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_resource_data_group_mode`
--

LOCK TABLES `sigl_resource_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_resource_data_group_mode` DISABLE KEYS */;
INSERT INTO `sigl_resource_data_group_mode` VALUES (1,1,56,NULL),(2,2,56,NULL),(3,3,56,NULL),(5,5,56,NULL),(7,7,56,NULL),(9,9,56,NULL),(11,11,56,NULL),(13,13,56,NULL),(15,15,56,NULL),(17,17,56,NULL),(19,19,56,NULL),(21,21,56,NULL),(23,23,56,NULL),(25,25,56,NULL),(27,27,56,NULL),(29,29,56,NULL),(31,31,56,NULL),(33,33,56,NULL),(35,35,56,NULL),(37,37,56,NULL),(39,39,56,NULL),(41,41,56,NULL),(43,43,56,NULL),(45,45,56,NULL),(47,47,56,NULL),(49,49,56,NULL),(51,51,56,NULL),(53,53,56,NULL),(55,55,56,NULL),(57,57,56,NULL),(59,59,56,NULL),(61,61,56,NULL),(63,63,56,NULL),(65,65,56,NULL),(67,67,56,NULL),(68,68,56,NULL),(69,69,56,NULL),(70,70,56,NULL),(71,71,56,NULL),(72,72,56,NULL),(73,73,56,NULL),(74,74,56,NULL),(75,75,56,NULL),(76,76,56,NULL);
/*!40000 ALTER TABLE `sigl_resource_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_resource_deleted`
--

DROP TABLE IF EXISTS `sigl_resource_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_resource_deleted` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL DEFAULT '100',
  `name` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `type` int(10) unsigned NOT NULL,
  `content` text COLLATE utf8_unicode_ci,
  `filename` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `resource_id` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `sigl_resource_data_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_resource_deleted`
--

LOCK TABLES `sigl_resource_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_resource_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_resource_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_reunion_data`
--

DROP TABLE IF EXISTS `sigl_reunion_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_reunion_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `organisateur_id` int(10) unsigned DEFAULT NULL,
  `type_reu` int(10) unsigned DEFAULT NULL,
  `cr` text,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_reunion_data`
--

LOCK TABLES `sigl_reunion_data` WRITE;
/*!40000 ALTER TABLE `sigl_reunion_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_reunion_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_reunion_data_group`
--

DROP TABLE IF EXISTS `sigl_reunion_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_reunion_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_reunion_data_group`
--

LOCK TABLES `sigl_reunion_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_reunion_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_reunion_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_reunion_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_reunion_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_reunion_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_reunion_data_group_mode`
--

LOCK TABLES `sigl_reunion_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_reunion_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_reunion_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_reunion_deleted`
--

DROP TABLE IF EXISTS `sigl_reunion_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_reunion_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `organisateur_id` int(10) unsigned DEFAULT NULL,
  `type_reu` int(10) unsigned DEFAULT NULL,
  `cr` text,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_reunion_deleted`
--

LOCK TABLES `sigl_reunion_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_reunion_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_reunion_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_reunion_pj__file_data`
--

DROP TABLE IF EXISTS `sigl_reunion_pj__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_reunion_pj__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_reunion_pj__file_data`
--

LOCK TABLES `sigl_reunion_pj__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_reunion_pj__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_reunion_pj__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_reunion_pj__file_data_group`
--

DROP TABLE IF EXISTS `sigl_reunion_pj__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_reunion_pj__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_reunion_pj__file_data_group`
--

LOCK TABLES `sigl_reunion_pj__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_reunion_pj__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_reunion_pj__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_reunion_pj__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_reunion_pj__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_reunion_pj__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_reunion_pj__file_data_group_mode`
--

LOCK TABLES `sigl_reunion_pj__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_reunion_pj__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_reunion_pj__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_reunion_pj__file_deleted`
--

DROP TABLE IF EXISTS `sigl_reunion_pj__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_reunion_pj__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_reunion_pj__file_deleted`
--

LOCK TABLES `sigl_reunion_pj__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_reunion_pj__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_reunion_pj__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_revue_data`
--

DROP TABLE IF EXISTS `sigl_revue_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_revue_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `cr` text,
  `type_reu` int(10) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `organisateur_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_revue_data`
--

LOCK TABLES `sigl_revue_data` WRITE;
/*!40000 ALTER TABLE `sigl_revue_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_revue_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_revue_data_group`
--

DROP TABLE IF EXISTS `sigl_revue_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_revue_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_revue_data_group`
--

LOCK TABLES `sigl_revue_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_revue_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_revue_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_revue_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_revue_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_revue_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_revue_data_group_mode`
--

LOCK TABLES `sigl_revue_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_revue_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_revue_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_revue_deleted`
--

DROP TABLE IF EXISTS `sigl_revue_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_revue_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `cr` text,
  `type_reu` int(10) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `organisateur_id` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_revue_deleted`
--

LOCK TABLES `sigl_revue_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_revue_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_revue_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_revue_pj__file_data`
--

DROP TABLE IF EXISTS `sigl_revue_pj__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_revue_pj__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_revue_pj__file_data`
--

LOCK TABLES `sigl_revue_pj__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_revue_pj__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_revue_pj__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_revue_pj__file_data_group`
--

DROP TABLE IF EXISTS `sigl_revue_pj__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_revue_pj__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_revue_pj__file_data_group`
--

LOCK TABLES `sigl_revue_pj__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_revue_pj__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_revue_pj__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_revue_pj__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_revue_pj__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_revue_pj__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_revue_pj__file_data_group_mode`
--

LOCK TABLES `sigl_revue_pj__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_revue_pj__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_revue_pj__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_revue_pj__file_deleted`
--

DROP TABLE IF EXISTS `sigl_revue_pj__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_revue_pj__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_revue_pj__file_deleted`
--

LOCK TABLES `sigl_revue_pj__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_revue_pj__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_revue_pj__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_storage_data`
--

DROP TABLE IF EXISTS `sigl_storage_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_storage_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_storage_data`
--

LOCK TABLES `sigl_storage_data` WRITE;
/*!40000 ALTER TABLE `sigl_storage_data` DISABLE KEYS */;
INSERT INTO `sigl_storage_data` VALUES (1,100,'2021-03-04 11:20:50','2021-03-04 11:20:50',100,'/space/applisdata/labbook/storage');
/*!40000 ALTER TABLE `sigl_storage_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_storage_data_group`
--

DROP TABLE IF EXISTS `sigl_storage_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_storage_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_storage_data_group`
--

LOCK TABLES `sigl_storage_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_storage_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_storage_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_storage_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_storage_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_storage_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_storage_data_group_mode`
--

LOCK TABLES `sigl_storage_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_storage_data_group_mode` DISABLE KEYS */;
INSERT INTO `sigl_storage_data_group_mode` VALUES (1,1,56,NULL);
/*!40000 ALTER TABLE `sigl_storage_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_storage_deleted`
--

DROP TABLE IF EXISTS `sigl_storage_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_storage_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_storage_deleted`
--

LOCK TABLES `sigl_storage_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_storage_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_storage_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_cv__file_data`
--

DROP TABLE IF EXISTS `sigl_user_cv__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_cv__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_cv__file_data`
--

LOCK TABLES `sigl_user_cv__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_user_cv__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_cv__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_cv__file_data_group`
--

DROP TABLE IF EXISTS `sigl_user_cv__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_cv__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_cv__file_data_group`
--

LOCK TABLES `sigl_user_cv__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_user_cv__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_cv__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_cv__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_user_cv__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_cv__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_cv__file_data_group_mode`
--

LOCK TABLES `sigl_user_cv__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_user_cv__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_cv__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_cv__file_deleted`
--

DROP TABLE IF EXISTS `sigl_user_cv__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_cv__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_cv__file_deleted`
--

LOCK TABLES `sigl_user_cv__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_user_cv__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_cv__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_data`
--

DROP TABLE IF EXISTS `sigl_user_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned NOT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(81) DEFAULT NULL,
  `titre` int(10) unsigned DEFAULT NULL,
  `id_group` int(10) unsigned NOT NULL DEFAULT '100',
  `email` varchar(200) DEFAULT NULL,
  `status` int(10) unsigned NOT NULL DEFAULT '0',
  `creation_date` date NOT NULL DEFAULT '0000-00-00',
  `expire_date` date DEFAULT NULL,
  `cps_id` varchar(30) DEFAULT NULL,
  `oauth_provider_id_user` int(10) unsigned DEFAULT NULL,
  `locale` int(10) unsigned NOT NULL DEFAULT '35',
  `rpps` varchar(11) DEFAULT NULL,
  `otp_phone_number` varchar(20) DEFAULT NULL,
  `initiale` varchar(5) DEFAULT NULL,
  `ddn` date DEFAULT NULL,
  `position` varchar(50) DEFAULT NULL,
  `adresse` text,
  `tel` varchar(20) DEFAULT NULL,
  `darrive` date DEFAULT NULL,
  `cv` text,
  `diplome` text,
  `formation` text,
  `deval` date DEFAULT NULL,
  `section` int(10) unsigned DEFAULT NULL,
  `commentaire` text,
  `side_account` int DEFAULT 0,
  PRIMARY KEY (`id_data`),
  KEY `sigl_user_data_ibfk_2` (`titre`),
  KEY `id_owner` (`id_owner`),
  KEY `sigl_user_data_status_dico` (`status`),
  KEY `sigl_user_data_locale_dico` (`locale`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_data`
--

LOCK TABLES `sigl_user_data` WRITE;
/*!40000 ALTER TABLE `sigl_user_data` DISABLE KEYS */;
INSERT INTO `sigl_user_data` VALUES (1,100,NULL,'root','root','cc17e083ebaf055f7d0a3aefc5f966a013803805:5c5f181ddbfa496b6e84e5f3954be395510f8b26',NULL,100,NULL,29,'2015-12-15',NULL,NULL,0,35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0),(2,100,'Bernard','BIO','biologiste','e87794f2c12892b936731468d5a2d5ff795fb012:4db86987d8f477116f80df0f393cde69fef8a59f',0,1001,'',29,'2021-03-04',NULL,'',NULL,35,'',NULL,'','0000-00-00','','','','0000-00-00','','','','0000-00-00',0,'',0),(3,100,'Thierry','TECH','technicien','6c86c15cffeb53cb192a104bc4c0b7ccc0f6b70b:29a7a241aa4dc67bfa9302b1dfe26e0cbac6bfbf',0,1002,'',29,'2021-03-04',NULL,'',NULL,35,'',NULL,'','0000-00-00','','','','0000-00-00','','','','0000-00-00',0,'',0),(4,100,'Thomas','TECHAVANCE','techav','06c3e0066d7122d8e0d56c4b7f6547fdabced768:8774fcb894ce9a7c18f9b282b6b50da2afde9cc3',0,1003,'',29,'2021-03-04',NULL,'',NULL,35,'',NULL,'','0000-00-00','','','','0000-00-00','','','','0000-00-00',0,'',0),(5,100,'Thibault','TECHQUALIT','techq','c4a59b7a6b523d7b96dec2eff991d1fe5306d2dd:26877721454a9f7f67bbbf84de08fac6db828df8',0,1004,'',29,'2021-03-04',NULL,'',NULL,35,'',NULL,'','0000-00-00','','','','0000-00-00','','','','0000-00-00',0,'',0),(6,100,'Sophie','SECR','secretaire','f167ea8095fd02bdd6e956f51c2fb2403b20ecbe:070c514b5e43f43e476f9b3e82bdb7926ab95257',0,1005,'',29,'2021-03-04',NULL,'',NULL,35,'',NULL,'','0000-00-00','','','','0000-00-00','','','','0000-00-00',0,'',0),(7,100,'Sylvie','SECRAV','secrav','5d771e9825b6f98422d469d6c79a9707b01dd892:014f23212d6e2554c847983936a77504e284451a',0,1006,'',29,'2021-03-04',NULL,'',NULL,35,'',NULL,'','0000-00-00','','','','0000-00-00','','','','0000-00-00',0,'',0),(8,100,'Quentin','QUALIT','qualiticien','7d8bd0cc70e922d9205235b88a836e787ba00c67:23f9fe9d846a9ca02f1cadfb38415fcdc5368d9d',0,1007,'',29,'2021-03-04',NULL,'',NULL,35,'',NULL,'','0000-00-00','','','','0000-00-00','','','','0000-00-00',0,'',0),(9,100,'Patrick','PRESCR','prescripteur','999c88ed65983b80619699068e5708132a482b43:d78d5eeac2eb5c251ccf5b542ab98222d36f5b7b',0,1008,'',29,'2021-03-04',NULL,'',NULL,35,'',NULL,'','0000-00-00','','','','0000-00-00','','','','0000-00-00',0,'',1);
/*!40000 ALTER TABLE `sigl_user_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_data_group`
--

DROP TABLE IF EXISTS `sigl_user_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_user_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_data_group`
--

LOCK TABLES `sigl_user_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_user_data_group` DISABLE KEYS */;
INSERT INTO `sigl_user_data_group` VALUES (1,1,1000);
/*!40000 ALTER TABLE `sigl_user_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_user_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_user_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_data_group_mode`
--

LOCK TABLES `sigl_user_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_user_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_deleted`
--

DROP TABLE IF EXISTS `sigl_user_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned NOT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(81) DEFAULT NULL,
  `titre` int(10) unsigned DEFAULT NULL,
  `id_group` int(10) unsigned NOT NULL DEFAULT '100',
  `email` varchar(200) DEFAULT NULL,
  `status` int(10) unsigned NOT NULL DEFAULT '0',
  `creation_date` date NOT NULL DEFAULT '0000-00-00',
  `expire_date` date DEFAULT NULL,
  `cps_id` varchar(30) DEFAULT NULL,
  `oauth_provider_id_user` int(10) unsigned DEFAULT NULL,
  `locale` int(10) unsigned NOT NULL DEFAULT '35',
  `rpps` varchar(11) DEFAULT NULL,
  `initiale` varchar(5) DEFAULT NULL,
  `ddn` date DEFAULT NULL,
  `position` varchar(50) DEFAULT NULL,
  `adresse` text,
  `tel` varchar(20) DEFAULT NULL,
  `darrive` date DEFAULT NULL,
  `cv` text,
  `diplome` text,
  `formation` text,
  `deval` date DEFAULT NULL,
  `section` int(10) unsigned DEFAULT NULL,
  `commentaire` text,
  KEY `sigl_user_data_ibfk_2` (`titre`),
  KEY `id_owner` (`id_owner`),
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_deleted`
--

LOCK TABLES `sigl_user_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_user_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_dico_profil_bis_data`
--

DROP TABLE IF EXISTS `sigl_user_dico_profil_bis_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_dico_profil_bis_data` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_dico` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_dico_profil_bis_data`
--

LOCK TABLES `sigl_user_dico_profil_bis_data` WRITE;
/*!40000 ALTER TABLE `sigl_user_dico_profil_bis_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_dico_profil_bis_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_dico_profil_bis_deleted`
--

DROP TABLE IF EXISTS `sigl_user_dico_profil_bis_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_dico_profil_bis_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_dico` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_dico_profil_bis_deleted`
--

LOCK TABLES `sigl_user_dico_profil_bis_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_user_dico_profil_bis_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_dico_profil_bis_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_dico_profil_data`
--

DROP TABLE IF EXISTS `sigl_user_dico_profil_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_dico_profil_data` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_dico` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_dico_profil_data`
--

LOCK TABLES `sigl_user_dico_profil_data` WRITE;
/*!40000 ALTER TABLE `sigl_user_dico_profil_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_dico_profil_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_dico_profil_deleted`
--

DROP TABLE IF EXISTS `sigl_user_dico_profil_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_dico_profil_deleted` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `id_owner` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_dico` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_dico_profil_deleted`
--

LOCK TABLES `sigl_user_dico_profil_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_user_dico_profil_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_dico_profil_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_diplomes__file_data`
--

DROP TABLE IF EXISTS `sigl_user_diplomes__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_diplomes__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_diplomes__file_data`
--

LOCK TABLES `sigl_user_diplomes__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_user_diplomes__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_diplomes__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_diplomes__file_data_group`
--

DROP TABLE IF EXISTS `sigl_user_diplomes__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_diplomes__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_diplomes__file_data_group`
--

LOCK TABLES `sigl_user_diplomes__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_user_diplomes__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_diplomes__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_diplomes__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_user_diplomes__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_diplomes__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_diplomes__file_data_group_mode`
--

LOCK TABLES `sigl_user_diplomes__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_user_diplomes__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_diplomes__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_diplomes__file_deleted`
--

DROP TABLE IF EXISTS `sigl_user_diplomes__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_diplomes__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_diplomes__file_deleted`
--

LOCK TABLES `sigl_user_diplomes__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_user_diplomes__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_diplomes__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_evaluation__file_data`
--

DROP TABLE IF EXISTS `sigl_user_evaluation__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_evaluation__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_evaluation__file_data`
--

LOCK TABLES `sigl_user_evaluation__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_user_evaluation__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_evaluation__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_evaluation__file_data_group`
--

DROP TABLE IF EXISTS `sigl_user_evaluation__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_evaluation__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_evaluation__file_data_group`
--

LOCK TABLES `sigl_user_evaluation__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_user_evaluation__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_evaluation__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_evaluation__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_user_evaluation__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_evaluation__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_evaluation__file_data_group_mode`
--

LOCK TABLES `sigl_user_evaluation__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_user_evaluation__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_evaluation__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_evaluation__file_deleted`
--

DROP TABLE IF EXISTS `sigl_user_evaluation__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_evaluation__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_evaluation__file_deleted`
--

LOCK TABLES `sigl_user_evaluation__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_user_evaluation__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_evaluation__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_formations__file_data`
--

DROP TABLE IF EXISTS `sigl_user_formations__file_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_formations__file_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_formations__file_data`
--

LOCK TABLES `sigl_user_formations__file_data` WRITE;
/*!40000 ALTER TABLE `sigl_user_formations__file_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_formations__file_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_formations__file_data_group`
--

DROP TABLE IF EXISTS `sigl_user_formations__file_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_formations__file_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_formations__file_data_group`
--

LOCK TABLES `sigl_user_formations__file_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_user_formations__file_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_formations__file_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_formations__file_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_user_formations__file_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_formations__file_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_formations__file_data_group_mode`
--

LOCK TABLES `sigl_user_formations__file_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_user_formations__file_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_formations__file_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_user_formations__file_deleted`
--

DROP TABLE IF EXISTS `sigl_user_formations__file_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_user_formations__file_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `id_ext` int(10) unsigned DEFAULT NULL,
  `id_file` int(10) unsigned DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_user_formations__file_deleted`
--

LOCK TABLES `sigl_user_formations__file_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_user_formations__file_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_user_formations__file_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_varset_n16s_data`
--

DROP TABLE IF EXISTS `sigl_varset_n16s_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_varset_n16s_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `champ_l9kx` varchar(255) DEFAULT NULL,
  `champ_y5fs` int(11) DEFAULT NULL,
  `champ_x311` int(10) unsigned DEFAULT NULL,
  `champ_dnq8` int(10) unsigned DEFAULT NULL,
  `type` int(10) unsigned DEFAULT NULL,
  `ddn` date DEFAULT NULL,
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_varset_n16s_data`
--

LOCK TABLES `sigl_varset_n16s_data` WRITE;
/*!40000 ALTER TABLE `sigl_varset_n16s_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_varset_n16s_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_varset_n16s_data_group`
--

DROP TABLE IF EXISTS `sigl_varset_n16s_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_varset_n16s_data_group` (
  `id_data_group` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data` int(10) unsigned NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `id_data` (`id_data`,`id_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_varset_n16s_data_group`
--

LOCK TABLES `sigl_varset_n16s_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_varset_n16s_data_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_varset_n16s_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_varset_n16s_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_varset_n16s_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_varset_n16s_data_group_mode` (
  `id_data_group_mode` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_data_group` int(10) unsigned NOT NULL,
  `mode` int(10) unsigned NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `id_data_group` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_varset_n16s_data_group_mode`
--

LOCK TABLES `sigl_varset_n16s_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_varset_n16s_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_varset_n16s_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_varset_n16s_deleted`
--

DROP TABLE IF EXISTS `sigl_varset_n16s_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_varset_n16s_deleted` (
  `id_data` int(10) unsigned NOT NULL,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `sys_creation_date` datetime DEFAULT NULL,
  `sys_last_mod_date` datetime DEFAULT NULL,
  `sys_last_mod_user` int(10) unsigned DEFAULT NULL,
  `champ_l9kx` varchar(255) DEFAULT NULL,
  `champ_y5fs` int(11) DEFAULT NULL,
  `champ_x311` int(10) unsigned DEFAULT NULL,
  `champ_dnq8` int(10) unsigned DEFAULT NULL,
  `type` int(10) unsigned DEFAULT NULL,
  `ddn` date DEFAULT NULL,
  KEY `id_data` (`id_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_varset_n16s_deleted`
--

LOCK TABLES `sigl_varset_n16s_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_varset_n16s_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_varset_n16s_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_varsetmonitor_data`
--

DROP TABLE IF EXISTS `sigl_varsetmonitor_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_varsetmonitor_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `id_evtlog` int(10) unsigned DEFAULT NULL,
  `id_varset` int(10) unsigned DEFAULT NULL,
  `id_data_monitored` int(10) unsigned DEFAULT NULL,
  `var_name` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `id_evtlog` (`id_evtlog`),
  KEY `id_varset` (`id_varset`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB AUTO_INCREMENT=279 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_varsetmonitor_data`
--

LOCK TABLES `sigl_varsetmonitor_data` WRITE;
/*!40000 ALTER TABLE `sigl_varsetmonitor_data` DISABLE KEYS */;
INSERT INTO `sigl_varsetmonitor_data` VALUES (1,100,2,7,1,'locale','34'),(2,100,3,7,1,'locale','35'),(3,100,4,7,1,'locale','75'),(4,100,5,7,1,'locale','142'),(5,100,6,35,20130,'filename','translation\\pt\\sigl.mo'),(6,100,6,35,20130,'name','pt'),(7,100,6,35,20130,'type','58'),(8,100,6,35,20130,'description',''),(9,100,7,7,1,'locale','34'),(10,100,8,8,14,'value','0'),(11,100,9,8,14,'value','1'),(12,100,10,7,1,'locale','142'),(13,100,11,7,1,'locale','35'),(14,100,14,6,57,'nom','Electrophorèse de l\'Hémoglobine sans tracé'),(15,100,15,6,58,'nom','Electrophorèse de l\'Hémoglobine avec quantification par densitométrie'),(16,100,16,6,59,'nom','Electrophorèse de l\'Hémoglobine par HPLC'),(17,100,17,6,77,'nom','5\'Nucléotidase'),(18,100,18,6,123,'nom','Microalbumine (dosage à l\'exclusion des bandelettes)'),(19,100,19,6,135,'nom','Clairance de l\'acide urique'),(20,100,20,6,136,'nom','Clairance de l\'urée'),(21,100,21,6,138,'nom','Epreuve d\'Hyperglycémie Provoquée par voie Orale (HGPO) : = 4 dosages'),(22,100,22,6,140,'nom','Epreuve à l\'insuline : dosage du glucose'),(23,100,23,6,144,'nom','Test à HCG : dosage de l\'estradiol'),(24,100,24,6,162,'nom','Recherche d\'hématies foetales'),(25,100,25,6,202,'nom','Recherche d\'une toxine bactérienne par technique immunologique'),(26,100,26,6,205,'nom','Cryptococcose (recherche d\'antigènes solubles de Cryptococcus néoformans)'),(27,100,27,6,220,'nom','Recherche Ac anti HBs (Hépatite B par automate d\'immunoanalyse)'),(28,100,28,6,221,'nom','Recherche Ag HBe (Hépatite B par automate d\'immunoanalyse)'),(29,100,29,6,222,'nom','Recherche Ac anti HBc (Hépatite B par automate d\'immunoanalyse)'),(30,100,30,6,223,'nom','Recherche Ac anti HBc IgM (Hépatite B par automate d\'immunoanalyse)'),(31,100,31,6,224,'nom','Test de neutralisation de l\'hépatite B'),(32,100,32,6,227,'nom','Recherche des Ac anti VHC (par automate d\'immunoanalyse)'),(33,100,33,6,231,'nom','Recherche des Ac anti-VIH (par automate d\'immunoanalyse)'),(34,100,34,6,232,'nom','Recherche et titrage de l\'antigène P24'),(35,100,35,6,248,'nom','Recherche et titrage de l\'Antigène CarcinoEmbryonnaire (ACE)'),(36,100,36,6,249,'nom','Recherche et titrage de l\'Antigène Prostatique Spécifique (PSA)'),(37,100,37,6,250,'nom','Recherche et titrage de l\'Antigène Prostatique Spécifique  libre (PSA libre)'),(38,100,38,6,251,'nom','Recherche et titrage de 2 microglobuline (dans le sérum ou urine)'),(39,100,39,6,276,'nom','Examen cytobactériologique des liquides d\'épanchements ou de ponction'),(40,100,40,6,277,'nom','Examen direct des liquides d\'épanchements ou de ponction'),(41,100,41,6,219,'nom','Recherche AgHBs (Hépatite B par automate d\'immunoanalyse)'),(42,100,44,13,742,NULL,NULL),(43,100,45,13,741,'position','10'),(44,100,46,1,634,NULL,NULL),(45,100,47,37,1,'id_dico','632'),(46,100,47,37,1,'status','119'),(47,100,47,37,1,'effective_date','2017-12-20 16:37:09'),(48,100,47,37,1,'sys_creation_date','2017-12-20 16:37:09'),(49,100,47,37,1,'sys_last_mod_date','2017-12-20 16:37:09'),(50,100,47,37,1,'sys_last_mod_user','100'),(51,100,48,37,2,'id_dico','633'),(52,100,48,37,2,'status','119'),(53,100,48,37,2,'effective_date','2017-12-20 16:37:10'),(54,100,48,37,2,'sys_creation_date','2017-12-20 16:37:10'),(55,100,48,37,2,'sys_last_mod_date','2017-12-20 16:37:10'),(56,100,48,37,2,'sys_last_mod_user','100'),(57,100,49,37,3,'id_dico','1120'),(58,100,49,37,3,'status','119'),(59,100,49,37,3,'effective_date','2017-12-20 16:37:10'),(60,100,49,37,3,'sys_creation_date','2017-12-20 16:37:10'),(61,100,49,37,3,'sys_last_mod_date','2017-12-20 16:37:10'),(62,100,49,37,3,'sys_last_mod_user','100'),(63,100,50,13,764,NULL,NULL),(64,100,51,13,767,NULL,NULL),(65,100,52,13,765,'position','20'),(66,100,53,13,766,'position','10'),(67,100,54,1,1122,NULL,NULL),(68,100,55,1,640,'code','wb'),(69,100,56,37,4,'id_dico','640'),(70,100,56,37,4,'status','119'),(71,100,56,37,4,'effective_date','2017-12-20 17:04:44'),(72,100,56,37,4,'sys_creation_date','2017-12-20 17:04:44'),(73,100,56,37,4,'sys_last_mod_date','2017-12-20 17:04:44'),(74,100,56,37,4,'sys_last_mod_user','100'),(75,100,57,37,5,'id_dico','641'),(76,100,57,37,5,'status','119'),(77,100,57,37,5,'effective_date','2017-12-20 17:04:44'),(78,100,57,37,5,'sys_creation_date','2017-12-20 17:04:44'),(79,100,57,37,5,'sys_last_mod_date','2017-12-20 17:04:44'),(80,100,57,37,5,'sys_last_mod_user','100'),(81,100,58,13,766,NULL,NULL),(82,100,59,9,715,'libelle','Résultat (filariose)'),(83,100,59,9,715,'description',''),(84,100,59,9,715,'type_resultat','635'),(85,100,59,9,715,'formule',''),(86,100,59,9,715,'unite',''),(87,100,59,9,715,'precision',''),(88,100,59,9,715,'normal_min',''),(89,100,59,9,715,'normal_max',''),(90,100,59,9,715,'unite2',''),(91,100,59,9,715,'formule_unite2',''),(92,100,59,9,715,'precision2',''),(93,100,59,9,715,'commentaire',''),(94,100,60,13,1192,'id_refanalyse','413'),(95,100,60,13,1192,'id_refvariable','715'),(96,100,60,13,1192,'position','10'),(97,100,60,13,1192,'obligatoire','4'),(98,100,60,13,1192,'num_var',''),(99,100,61,13,451,NULL,NULL),(100,100,62,13,455,NULL,NULL),(101,100,63,13,457,NULL,NULL),(102,100,64,13,453,NULL,NULL),(103,100,65,13,456,NULL,NULL),(104,100,66,13,452,NULL,NULL),(105,100,67,13,454,NULL,NULL),(106,100,68,13,438,'position','19'),(107,100,69,13,743,NULL,NULL),(108,100,70,9,716,'libelle','Résultat (fièvre jaune)'),(109,100,70,9,716,'description',''),(110,100,70,9,716,'type_resultat','635'),(111,100,70,9,716,'formule',''),(112,100,70,9,716,'unite',''),(113,100,70,9,716,'precision',''),(114,100,70,9,716,'normal_min',''),(115,100,70,9,716,'normal_max',''),(116,100,70,9,716,'unite2',''),(117,100,70,9,716,'formule_unite2',''),(118,100,70,9,716,'precision2',''),(119,100,70,9,716,'commentaire',''),(120,100,71,13,1193,'id_refanalyse','407'),(121,100,71,13,1193,'id_refvariable','716'),(122,100,71,13,1193,'position','20'),(123,100,71,13,1193,'obligatoire','4'),(124,100,71,13,1193,'num_var',''),(125,100,72,13,432,NULL,NULL),(126,100,73,13,434,NULL,NULL),(127,100,74,13,423,'position','14'),(128,100,75,13,236,NULL,NULL),(129,100,76,13,234,'position','20'),(130,100,77,13,395,NULL,NULL),(131,100,78,13,382,'position','14'),(132,100,79,13,410,NULL,NULL),(133,100,80,13,397,'position','17'),(134,100,81,13,407,NULL,NULL),(135,100,82,13,392,NULL,NULL),(136,100,83,13,758,NULL,NULL),(137,100,84,13,757,'position','2'),(138,100,85,13,759,NULL,NULL),(139,100,86,13,757,'position','10'),(140,100,87,9,717,'libelle','Résuultat (poliomyélite)'),(141,100,87,9,717,'description',''),(142,100,87,9,717,'type_resultat','635'),(143,100,87,9,717,'formule',''),(144,100,87,9,717,'unite',''),(145,100,87,9,717,'precision',''),(146,100,87,9,717,'normal_min',''),(147,100,87,9,717,'normal_max',''),(148,100,87,9,717,'unite2',''),(149,100,87,9,717,'formule_unite2',''),(150,100,87,9,717,'precision2',''),(151,100,87,9,717,'commentaire',''),(152,100,88,13,1194,'id_refanalyse','411'),(153,100,88,13,1194,'id_refvariable','717'),(154,100,88,13,1194,'position','20'),(155,100,88,13,1194,'obligatoire','4'),(156,100,88,13,1194,'num_var',''),(157,100,89,9,717,'libelle','Résultat (poliomyélite)'),(158,100,90,6,238,NULL,NULL),(159,100,91,13,746,NULL,NULL),(160,100,92,13,747,NULL,NULL),(161,100,93,13,744,'position','10'),(162,100,94,13,745,'position','20'),(163,100,95,9,718,'libelle','IgM (rougeole)'),(164,100,95,9,718,'description',''),(165,100,95,9,718,'type_resultat','635'),(166,100,95,9,718,'formule',''),(167,100,95,9,718,'unite',''),(168,100,95,9,718,'precision',''),(169,100,95,9,718,'normal_min',''),(170,100,95,9,718,'normal_max',''),(171,100,95,9,718,'unite2',''),(172,100,95,9,718,'formule_unite2',''),(173,100,95,9,718,'precision2',''),(174,100,95,9,718,'commentaire',''),(175,100,96,13,1195,'id_refanalyse','408'),(176,100,96,13,1195,'id_refvariable','718'),(177,100,96,13,1195,'position','2'),(178,100,96,13,1195,'obligatoire','4'),(179,100,96,13,1195,'num_var',''),(180,100,97,9,719,'libelle','IgG (rougeole)'),(181,100,97,9,719,'description',''),(182,100,97,9,719,'type_resultat','635'),(183,100,97,9,719,'formule',''),(184,100,97,9,719,'unite',''),(185,100,97,9,719,'precision',''),(186,100,97,9,719,'normal_min',''),(187,100,97,9,719,'normal_max',''),(188,100,97,9,719,'unite2',''),(189,100,97,9,719,'formule_unite2',''),(190,100,97,9,719,'precision2',''),(191,100,97,9,719,'commentaire',''),(192,100,98,13,1196,'id_refanalyse','408'),(193,100,98,13,1196,'id_refvariable','719'),(194,100,98,13,1196,'position','3'),(195,100,98,13,1196,'obligatoire','4'),(196,100,98,13,1196,'num_var',''),(197,100,99,13,744,NULL,NULL),(198,100,100,13,745,NULL,NULL),(199,100,101,13,1195,'position','10'),(200,100,102,13,1196,'position','20'),(201,100,103,13,315,NULL,NULL),(202,100,104,13,316,NULL,NULL),(203,100,105,13,314,'position','10'),(204,100,106,9,720,'libelle','IgM (rubéole)'),(205,100,106,9,720,'description',''),(206,100,106,9,720,'type_resultat','635'),(207,100,106,9,720,'formule',''),(208,100,106,9,720,'unite',''),(209,100,106,9,720,'precision',''),(210,100,106,9,720,'normal_min',''),(211,100,106,9,720,'normal_max',''),(212,100,106,9,720,'unite2',''),(213,100,106,9,720,'formule_unite2',''),(214,100,106,9,720,'precision2',''),(215,100,106,9,720,'commentaire',''),(216,100,107,13,1197,'id_refanalyse','239'),(217,100,107,13,1197,'id_refvariable','720'),(218,100,107,13,1197,'position','20'),(219,100,107,13,1197,'obligatoire','4'),(220,100,107,13,1197,'num_var',''),(221,100,108,9,721,'libelle','IgG (rubéole)'),(222,100,108,9,721,'description',''),(223,100,108,9,721,'type_resultat','635'),(224,100,108,9,721,'formule',''),(225,100,108,9,721,'unite',''),(226,100,108,9,721,'precision',''),(227,100,108,9,721,'normal_min',''),(228,100,108,9,721,'normal_max',''),(229,100,108,9,721,'unite2',''),(230,100,108,9,721,'formule_unite2',''),(231,100,108,9,721,'precision2',''),(232,100,108,9,721,'commentaire',''),(233,100,109,13,1198,'id_refanalyse','239'),(234,100,109,13,1198,'id_refvariable','721'),(235,100,109,13,1198,'position','30'),(236,100,109,13,1198,'obligatoire','4'),(237,100,109,13,1198,'num_var',''),(238,100,110,13,751,NULL,NULL),(239,100,111,13,750,NULL,NULL),(240,100,112,13,749,NULL,NULL),(241,100,113,13,748,NULL,NULL),(242,100,114,6,409,NULL,NULL),(243,100,115,13,239,NULL,NULL),(244,100,116,13,774,NULL,NULL),(245,100,117,13,777,NULL,NULL),(246,100,118,13,775,'position','20'),(247,100,119,13,776,'position','10'),(248,100,120,13,760,NULL,NULL),(249,100,121,13,763,NULL,NULL),(250,100,122,13,761,'position','20'),(251,100,123,13,762,'position','10'),(252,100,124,1,1121,NULL,NULL),(253,100,125,37,6,'id_dico','636'),(254,100,125,37,6,'status','119'),(255,100,125,37,6,'effective_date','2017-12-20 22:52:57'),(256,100,125,37,6,'sys_creation_date','2017-12-20 22:52:57'),(257,100,125,37,6,'sys_last_mod_date','2017-12-20 22:52:57'),(258,100,125,37,6,'sys_last_mod_user','100'),(259,100,126,37,7,'id_dico','637'),(260,100,126,37,7,'status','119'),(261,100,126,37,7,'effective_date','2017-12-20 22:52:57'),(262,100,126,37,7,'sys_creation_date','2017-12-20 22:52:57'),(263,100,126,37,7,'sys_last_mod_date','2017-12-20 22:52:57'),(264,100,126,37,7,'sys_last_mod_user','100'),(265,100,127,13,755,NULL,NULL),(266,100,128,13,756,NULL,NULL),(267,NULL,130,35,7,'content','<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<varset name=\"user\" prefix=\"user\" type=\"sys\" label=\"User\">\n	<var uid=\"1\" id=\"id_group\" type=\"integer\" mandatory=\"true\" default_label=\"Groupe\" default_short_label=\"Groupe\">\n		<integer min=\"0\" max=\"4294967295\"/>\n	</var'),(268,NULL,130,35,7,'name','user'),(269,NULL,130,35,7,'description',''),(270,NULL,130,35,7,'resource_id',''),(271,NULL,130,35,7,'sys_last_mod_date','2019-04-02 11:33:42'),(272,NULL,130,35,7,'sys_last_mod_user',''),(273,NULL,131,35,10000,'content','<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<acl_roles>\n	<role id=\"1\" label=\"Administrateur\">\n		<access>\n		<allow name=\"form/frame/get\"/><allow name=\"form/frame/save\"/><allow name=\"form/frame/delete\"/><allow name=\"upload/upload\"/><allow name=\"project/manager\"/'),(274,NULL,131,35,10000,'name','access_control_list'),(275,NULL,131,35,10000,'description',''),(276,NULL,131,35,10000,'resource_id',''),(277,NULL,131,35,10000,'sys_last_mod_date','2019-04-02 11:33:42'),(278,NULL,131,35,10000,'sys_last_mod_user','');
/*!40000 ALTER TABLE `sigl_varsetmonitor_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_varsetmonitor_data_group`
--

DROP TABLE IF EXISTS `sigl_varsetmonitor_data_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_varsetmonitor_data_group` (
  `id_data_group` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(11) NOT NULL,
  `id_group` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_data_group`),
  UNIQUE KEY `sigl_query_data_group_id` (`id_data`,`id_group`),
  KEY `id_group` (`id_group`)
) ENGINE=InnoDB AUTO_INCREMENT=267 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_varsetmonitor_data_group`
--

LOCK TABLES `sigl_varsetmonitor_data_group` WRITE;
/*!40000 ALTER TABLE `sigl_varsetmonitor_data_group` DISABLE KEYS */;
INSERT INTO `sigl_varsetmonitor_data_group` VALUES (1,1,1000),(2,2,1000),(3,3,1000),(4,4,1000),(5,5,1000),(6,6,1000),(7,7,1000),(8,8,1000),(9,9,1000),(10,10,1000),(11,11,1000),(12,12,1000),(13,13,1000),(14,14,1000),(15,15,1000),(16,16,1000),(17,17,1000),(18,18,1000),(19,19,1000),(20,20,1000),(21,21,1000),(22,22,1000),(23,23,1000),(24,24,1000),(25,25,1000),(26,26,1000),(27,27,1000),(28,28,1000),(29,29,1000),(30,30,1000),(31,31,1000),(32,32,1000),(33,33,1000),(34,34,1000),(35,35,1000),(36,36,1000),(37,37,1000),(38,38,1000),(39,39,1000),(40,40,1000),(41,41,1000),(42,42,1000),(43,43,1000),(44,44,1000),(45,45,1000),(46,46,1000),(47,47,1000),(48,48,1000),(49,49,1000),(50,50,1000),(51,51,1000),(52,52,1000),(53,53,1000),(54,54,1000),(55,55,1000),(56,56,1000),(57,57,1000),(58,58,1000),(59,59,1000),(60,60,1000),(61,61,1000),(62,62,1000),(63,63,1000),(64,64,1000),(65,65,1000),(66,66,1000),(67,67,1000),(68,68,1000),(69,69,1000),(70,70,1000),(71,71,1000),(72,72,1000),(73,73,1000),(74,74,1000),(75,75,1000),(76,76,1000),(77,77,1000),(78,78,1000),(79,79,1000),(80,80,1000),(81,81,1000),(82,82,1000),(83,83,1000),(84,84,1000),(85,85,1000),(86,86,1000),(87,87,1000),(88,88,1000),(89,89,1000),(90,90,1000),(91,91,1000),(92,92,1000),(93,93,1000),(94,94,1000),(95,95,1000),(96,96,1000),(97,97,1000),(98,98,1000),(99,99,1000),(100,100,1000),(101,101,1000),(102,102,1000),(103,103,1000),(104,104,1000),(105,105,1000),(106,106,1000),(107,107,1000),(108,108,1000),(109,109,1000),(110,110,1000),(111,111,1000),(112,112,1000),(113,113,1000),(114,114,1000),(115,115,1000),(116,116,1000),(117,117,1000),(118,118,1000),(119,119,1000),(120,120,1000),(121,121,1000),(122,122,1000),(123,123,1000),(124,124,1000),(125,125,1000),(126,126,1000),(127,127,1000),(128,128,1000),(129,129,1000),(130,130,1000),(131,131,1000),(132,132,1000),(133,133,1000),(134,134,1000),(135,135,1000),(136,136,1000),(137,137,1000),(138,138,1000),(139,139,1000),(140,140,1000),(141,141,1000),(142,142,1000),(143,143,1000),(144,144,1000),(145,145,1000),(146,146,1000),(147,147,1000),(148,148,1000),(149,149,1000),(150,150,1000),(151,151,1000),(152,152,1000),(153,153,1000),(154,154,1000),(155,155,1000),(156,156,1000),(157,157,1000),(158,158,1000),(159,159,1000),(160,160,1000),(161,161,1000),(162,162,1000),(163,163,1000),(164,164,1000),(165,165,1000),(166,166,1000),(167,167,1000),(168,168,1000),(169,169,1000),(170,170,1000),(171,171,1000),(172,172,1000),(173,173,1000),(174,174,1000),(175,175,1000),(176,176,1000),(177,177,1000),(178,178,1000),(179,179,1000),(180,180,1000),(181,181,1000),(182,182,1000),(183,183,1000),(184,184,1000),(185,185,1000),(186,186,1000),(187,187,1000),(188,188,1000),(189,189,1000),(190,190,1000),(191,191,1000),(192,192,1000),(193,193,1000),(194,194,1000),(195,195,1000),(196,196,1000),(197,197,1000),(198,198,1000),(199,199,1000),(200,200,1000),(201,201,1000),(202,202,1000),(203,203,1000),(204,204,1000),(205,205,1000),(206,206,1000),(207,207,1000),(208,208,1000),(209,209,1000),(210,210,1000),(211,211,1000),(212,212,1000),(213,213,1000),(214,214,1000),(215,215,1000),(216,216,1000),(217,217,1000),(218,218,1000),(219,219,1000),(220,220,1000),(221,221,1000),(222,222,1000),(223,223,1000),(224,224,1000),(225,225,1000),(226,226,1000),(227,227,1000),(228,228,1000),(229,229,1000),(230,230,1000),(231,231,1000),(232,232,1000),(233,233,1000),(234,234,1000),(235,235,1000),(236,236,1000),(237,237,1000),(238,238,1000),(239,239,1000),(240,240,1000),(241,241,1000),(242,242,1000),(243,243,1000),(244,244,1000),(245,245,1000),(246,246,1000),(247,247,1000),(248,248,1000),(249,249,1000),(250,250,1000),(251,251,1000),(252,252,1000),(253,253,1000),(254,254,1000),(255,255,1000),(256,256,1000),(257,257,1000),(258,258,1000),(259,259,1000),(260,260,1000),(261,261,1000),(262,262,1000),(263,263,1000),(264,264,1000),(265,265,1000),(266,266,1000);
/*!40000 ALTER TABLE `sigl_varsetmonitor_data_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_varsetmonitor_data_group_mode`
--

DROP TABLE IF EXISTS `sigl_varsetmonitor_data_group_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_varsetmonitor_data_group_mode` (
  `id_data_group_mode` int(11) NOT NULL AUTO_INCREMENT,
  `id_data_group` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `date_valid` date DEFAULT NULL,
  PRIMARY KEY (`id_data_group_mode`),
  UNIQUE KEY `sigl_varsetmonitor_data_group_mode_id` (`id_data_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_varsetmonitor_data_group_mode`
--

LOCK TABLES `sigl_varsetmonitor_data_group_mode` WRITE;
/*!40000 ALTER TABLE `sigl_varsetmonitor_data_group_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_varsetmonitor_data_group_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sigl_varsetmonitor_deleted`
--

DROP TABLE IF EXISTS `sigl_varsetmonitor_deleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sigl_varsetmonitor_deleted` (
  `id_data` int(11) NOT NULL,
  `id_owner` int(11) NOT NULL,
  `id_evtlog` int(10) unsigned DEFAULT NULL,
  `id_varset` int(10) unsigned DEFAULT NULL,
  `id_data_monitored` int(10) unsigned DEFAULT NULL,
  `var_name` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  KEY `id_evtlog` (`id_evtlog`),
  KEY `id_varset` (`id_varset`),
  KEY `id_owner` (`id_owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sigl_varsetmonitor_deleted`
--

LOCK TABLES `sigl_varsetmonitor_deleted` WRITE;
/*!40000 ALTER TABLE `sigl_varsetmonitor_deleted` DISABLE KEYS */;
/*!40000 ALTER TABLE `sigl_varsetmonitor_deleted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sticker_setting`
--

DROP TABLE IF EXISTS `sticker_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sticker_setting` (
  `sts_ser` int(11) NOT NULL AUTO_INCREMENT,
  `sts_margin_top` int(11) NOT NULL,
  `sts_margin_bottom` int(11) NOT NULL,
  `sts_margin_left` int(11) NOT NULL,
  `sts_margin_right` int(11) NOT NULL,
  `sts_height` int(11) NOT NULL,
  `sts_width` int(11) NOT NULL,
  PRIMARY KEY (`sts_ser`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sticker_setting`
--

LOCK TABLES `sticker_setting` WRITE;
/*!40000 ALTER TABLE `sticker_setting` DISABLE KEYS */;
INSERT INTO `sticker_setting` VALUES (1,10,10,10,10,15,60);
/*!40000 ALTER TABLE `sticker_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_context`
--

DROP TABLE IF EXISTS `sys_context`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_context` (
  `id_sys_config` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `section` varchar(80) NOT NULL,
  `name` varchar(80) NOT NULL,
  `value` varchar(80) NOT NULL,
  `last_update` datetime NOT NULL,
  PRIMARY KEY (`id_sys_config`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_context`
--

LOCK TABLES `sys_context` WRITE;
/*!40000 ALTER TABLE `sys_context` DISABLE KEYS */;
INSERT INTO `sys_context` VALUES (1,'system','version','2.26','2019-04-02 11:33:43');
/*!40000 ALTER TABLE `sys_context` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_dico_data`
--

DROP TABLE IF EXISTS `sys_dico_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_dico_data` (
  `id_data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_owner` int(10) unsigned DEFAULT NULL,
  `dico_name` char(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `label` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `short_label` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `position` int(11) DEFAULT '0',
  `code` char(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dico_id` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_data`),
  KEY `idx_dico_name` (`dico_name`)
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dico_data`
--

LOCK TABLES `sys_dico_data` WRITE;
/*!40000 ALTER TABLE `sys_dico_data` DISABLE KEYS */;
INSERT INTO `sys_dico_data` VALUES (1,100,'dmcp_modalite','Courrier','DMCP_MMAIL',1,'M',NULL),(2,100,'dmcp_modalite','Téléphonique','DMCP_MTEL',2,'T',NULL),(3,100,'dmcp_modalite','Directe','DMCP_MDIRECT',3,'D',NULL),(4,100,'yorn','oui','oui',1,'o',NULL),(5,100,'yorn','non','non',2,'n',NULL),(6,100,'dmcp_demande','Historique','DMCP_HDEM',3,'H',NULL),(7,100,'dmcp_access_mode','Lecture','DMCP_RACCESS',1,'R',NULL),(8,100,'dmcp_access_mode','Insertion','DMCP_CACCESS',2,'8',NULL),(9,100,'dmcp_access_mode','Modification','DMCP_UACCESS',3,'9',NULL),(10,100,'dmcp','Non soumis','DMCP_NO',1,'0',NULL),(11,100,'dmcp','Accessible','DMCP_ACCESS',2,'1',NULL),(12,100,'dmcp','Nominative','DMCP_NOM',3,'2',NULL),(13,100,'dmcp','Protégée','DMCP_PROTECTED',4,'4',NULL),(14,100,'type_evt','Insertion','VZN_REC_INSERT',1,'8',NULL),(15,100,'type_evt','Modification','VZN_REC_UPDATE',2,'9',NULL),(16,100,'type_evt','Suppression','VZN_REC_DELETE',3,'10',NULL),(17,100,'type_evt','Connexion','VZN_EVT_CONNEXION',4,'11',NULL),(18,100,'type_evt','Connexion CPSx','VZN_EVT_CONNEXIONCPS',5,'12',NULL),(19,100,'type_evt','Connexion oAuth','VZN_EVT_CONNEXION_OAUTH',6,'13',NULL),(20,100,'type_evt','Group merge','VZN_EVT_GRP_MERGE',201,'201',NULL),(21,100,'type_evt','Group rm','VZN_EVT_GRP_RM',202,'202',NULL),(22,100,'type_evt','Group rename','VZN_EVT_GRP_RENAME',203,'203',NULL),(23,100,'type_evt','Group add','VZN_EVT_GRP_ADD',204,'204',NULL),(24,100,'type_evt','Group disable','VZN_EVT_GRP_DISABLE',205,'205',NULL),(25,100,'type_evt','Group enable','VZN_EVT_GRP_ENABLE',206,'206',NULL),(26,100,'type_evt','Group move','VZN_EVT_GRP_MOVE',207,'207',NULL),(27,100,'consistency_test_run','Temps réel','RUNTIME',1,'rtm',NULL),(28,100,'consistency_test_run','Post saisie','BATCH',2,'bch',NULL),(29,100,'user_status','Activé','on',1,'on',NULL),(30,100,'user_status','Désactivé','off',2,'off',NULL),(31,100,'user_status','Supprimé','del',3,'del',NULL),(34,100,'locale','English (UK)','UK',1,'en_GB',NULL),(35,100,'locale','Français (FR)','FR',2,'fr_FR',NULL),(36,100,'type_evt','INFO','INFO',7,'6',NULL),(37,100,'type_evt','DEBUG','DEBUG',8,'7',NULL),(38,100,'type_evt','Connection Webservices','VZN_EVT_CONNEXION_WS',9,'14',NULL),(39,100,'resource_type','Form','form',1,'frm',NULL),(40,100,'resource_type','Project','project',2,'prj',NULL),(41,100,'resource_type','Style','style',3,'stl',NULL),(42,100,'resource_type','Varset','varset',4,'vst',NULL),(43,100,'resource_type','ACL','acl',5,'acl',NULL),(44,100,'resource_type','XML','xml',6,'xml',NULL),(45,100,'resource_type','DataSet','dataset',7,'dst',NULL),(46,100,'resource_type','Data Structure','data_structure',8,'str',NULL),(47,100,'resource_type','DataQuery','dataquery',9,'dqy',NULL),(48,100,'resource_type','Query','query',10,'qry',NULL),(49,100,'resource_type','Group','group',11,'grp',NULL),(50,100,'resource_type','ACL Roles','acl_roles',12,'arl',NULL),(51,100,'resource_type','ACL Resources','acl_resources',13,'ars',NULL),(52,100,'resource_type','PHP','php',14,'php',NULL),(53,100,'resource_type','SQL','sql',15,'sql',NULL),(54,100,'resource_type','TPL','tpl',16,'tpl',NULL),(55,100,'resource_type','XSD','xsd',17,'xsd',NULL),(56,100,'resource_type','XSL','xsl',18,'xsl',NULL),(57,100,'resource_type','PO','po',19,'po',NULL),(58,100,'resource_type','MO','mo',20,'mo',NULL),(59,100,'resource_type','CSV','csv',21,'csv',NULL),(60,100,'resource_type','Fixed length','fixed len',22,'fln',NULL),(61,100,'resource_type','Standard class','stdclass',23,'scl',NULL),(62,100,'resource_type','ODK','odk',24,'odk',NULL),(63,100,'resource_type','Listing','listing',25,'lst',NULL),(64,100,'resource_type','Filter','filter',26,'flt',NULL),(65,100,'resource_type','Homepage','homepage',27,'hmp',NULL),(66,100,'resource_type','Script','script',28,'scr',NULL),(67,100,'resource_type','R','r',29,'r',NULL),(68,100,'resource_type','Mainframe','mainframe',30,'mfr',NULL),(69,100,'resource_type','Sequence','sequece',31,'sqc',NULL),(70,100,'dmcp_demande','Accès aux données','DMCP_ADEM',1,'A',NULL),(71,100,'dmcp_demande','Rectification','DMCP_RDEM',2,'R',NULL),(72,100,'resource_type','Layout','Layout',31,'lyt',NULL),(73,100,'resource_type','My account','My account',32,'mya',NULL),(75,100,'locale','English (US)','US',4,'en_US',NULL),(76,NULL,'consistency_test_lvl','Alerte','Alerte',NULL,'alt',NULL),(77,NULL,'consistency_test_lvl','Notice','Notice',NULL,'ntc',NULL),(78,NULL,'consistency_test_frq','Every month','Every month',1,'0 0 1 * *',NULL),(79,NULL,'consistency_test_frq','Every week','Every week',2,'0 0 * * 0',NULL),(80,NULL,'consistency_test_frq','Every day at midnight','Every day at midnight',3,'0 0 * * *',NULL),(81,NULL,'consistency_test_frq','Every hour','Every hour',4,'0 * * * *',NULL),(82,NULL,'listing_rows_number','20','20',1,'20',NULL),(83,NULL,'listing_rows_number','50','50',2,'50',NULL),(84,NULL,'listing_rows_number','100','100',3,'100',NULL),(85,NULL,'listing_action','View','View',1,'view',NULL),(86,NULL,'listing_action','Edit','Edit',2,'edit',NULL),(87,NULL,'listing_action','Delete','Delete',3,'delete',NULL),(88,NULL,'filter_action','Value','Value',1,'value',NULL),(89,NULL,'filter_action','Enter during use','Enter during use',2,'dynamic',NULL),(90,NULL,'filter_approximation_func_date','Days','Days',1,'days',NULL),(91,NULL,'filter_approximation_func_date','Months','Months',2,'months',NULL),(92,NULL,'filter_approximation_func_date','Years','Years',3,'years',NULL),(93,NULL,'filter_approximation_func_datetime','Hours','Hours',1,'hours',NULL),(94,NULL,'filter_approximation_func_datetime','Days','Days',2,'days',NULL),(95,NULL,'filter_approximation_func_datetime','Months','Months',3,'months',NULL),(96,NULL,'filter_approximation_func_datetime','Years','Years',4,'years',NULL),(97,NULL,'filter_approximation_func_numeric','%','%',1,'%',NULL),(98,NULL,'filter_approximation_func_time','Minutes','Minutes',1,'minutes',NULL),(99,NULL,'filter_approximation_func_time','Hours','Hours',2,'hours',NULL),(100,NULL,'filter_approximation_scope','-','-',1,'-',NULL),(101,NULL,'filter_approximation_scope','+','+',2,'+',NULL),(102,NULL,'filter_comparator_dico','equal to','equal to',1,'=',NULL),(103,NULL,'filter_comparator_dico','different than','different than',2,'!=',NULL),(104,NULL,'filter_comparator_dico','empty','empty',3,'empty',NULL),(105,NULL,'filter_comparator_numeric','greater than','greater than',1,'>',NULL),(106,NULL,'filter_comparator_numeric','greater than or equal to','greater than',2,'>=',NULL),(107,NULL,'filter_comparator_numeric','equal to','equal to',3,'=',NULL),(108,NULL,'filter_comparator_numeric','different than','different than',4,'!=',NULL),(109,NULL,'filter_comparator_numeric','less than','less than',5,'<',NULL),(110,NULL,'filter_comparator_numeric','less than or equal to','less than or equal to',6,'<=',NULL),(111,NULL,'filter_comparator_numeric','empty','empty',7,'empty',NULL),(112,NULL,'filter_comparator_string','equal to','equal to',1,'=',NULL),(113,NULL,'filter_comparator_string','different than','different than',2,'!=',NULL),(114,NULL,'filter_comparator_string','contains','contains',3,'contain',NULL),(115,NULL,'filter_comparator_string','begins with','begins with',4,'begin',NULL),(116,NULL,'filter_comparator_string','ends with','ends with',5,'end',NULL),(117,NULL,'filter_comparator_string','empty','empty',6,'empty',NULL),(118,NULL,'function_date','NOW()','NOW()',1,'now()',NULL),(119,NULL,'dico_value_status','Created','Created',1,'C',NULL),(120,NULL,'dico_value_status','Archived','Archived',2,'A',NULL),(121,NULL,'dico_value_status','Unarchived','Unarchived',3,'UA',NULL),(122,NULL,'type_evt','Dico delete','VZN_EVT_DICO_DELETE',301,'301',NULL),(123,NULL,'type_evt','Dico value delete','VZN_EVT_DICO_DELETE_VALUE',302,'302',NULL),(124,NULL,'type_evt','User add','VZN_EVT_USER_ADD',401,'401',NULL),(125,NULL,'type_evt','User disable','VZN_EVT_USER_DISABLE',402,'402',NULL),(126,NULL,'type_evt','User enable','VZN_EVT_USER_ENABLE',403,'403',NULL),(127,NULL,'type_evt','User delete','VZN_EVT_USER_DELETE',404,'404',NULL),(128,NULL,'resource_type','Text','text',35,'txt',NULL),(129,NULL,'var_type','String','String',1,'string',NULL),(130,NULL,'var_type','Integer','Integer',2,'integer',NULL),(131,NULL,'var_type','Float','Float',3,'float',NULL),(132,NULL,'var_type','Date','Date',4,'date',NULL),(133,NULL,'var_type','Time','Time',5,'time',NULL),(134,NULL,'var_type','Date-time','Date-time',6,'datetime',NULL),(135,NULL,'var_type','Boolean','Boolean',7,'boolean',NULL),(136,NULL,'var_type','Text multiline','Text multiline',8,'text',NULL),(137,NULL,'var_type','Dictionnary','Dictionnary',9,'fkey_dico',NULL),(138,NULL,'epimob_data_storage','Local: data is stored on the mobile device (user can send data to the server at anytime).','local',1,'local',NULL),(139,NULL,'epimob_data_storage','Server: when the user saves the form, data is saved directly on the server.','server',2,'server',NULL),(140,NULL,'epimob_gateway','Default','Default',1,'default',NULL),(141,NULL,'epimob_gateway','Twilio','Twilio',2,'twilio',NULL),(143,1,'resource_type','JSON','json',30,'json',NULL),(144,NULL,'bootstrap_colors','Default','Default',1,'default',NULL),(145,NULL,'bootstrap_colors','Primary','Primary',2,'primary',NULL),(146,NULL,'bootstrap_colors','Success','Success',3,'success',NULL),(147,NULL,'bootstrap_colors','Info','Info',4,'info',NULL),(148,NULL,'bootstrap_colors','Warning','Warning',5,'warning',NULL),(149,NULL,'bootstrap_colors','Danger','Danger',6,'danger',NULL);
/*!40000 ALTER TABLE `sys_dico_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_editor`
--

DROP TABLE IF EXISTS `sys_editor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_editor` (
  `id_sys_editor` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_sys_project` int(11) NOT NULL,
  `id_editor` varchar(23) NOT NULL,
  `last_action_id` varchar(23) NOT NULL,
  `last_action_date` datetime NOT NULL,
  PRIMARY KEY (`id_sys_editor`),
  KEY `id_sys_editor` (`id_sys_editor`),
  KEY `id_editor` (`id_editor`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_editor`
--

LOCK TABLES `sys_editor` WRITE;
/*!40000 ALTER TABLE `sys_editor` DISABLE KEYS */;
INSERT INTO `sys_editor` VALUES (1,1,'jzipcxqhqd1483959677538','djzdilyrxi1497544976651','2017-06-15 18:45:30');
/*!40000 ALTER TABLE `sys_editor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_editor_publication`
--

DROP TABLE IF EXISTS `sys_editor_publication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_editor_publication` (
  `id_sys_editor_publication` int(11) NOT NULL AUTO_INCREMENT,
  `uniq_id` varchar(23) NOT NULL,
  `environment_id` varchar(23) NOT NULL,
  `last_update_timestamp` int(11) NOT NULL,
  `id_sys_editor` int(11) NOT NULL,
  `action_page_uploaded` int(11) NOT NULL,
  `action_page_total` int(11) NOT NULL,
  `action_applied` int(11) NOT NULL,
  `action_total` int(11) NOT NULL,
  `action_file` varchar(255) NOT NULL,
  `backup_path` varchar(255) NOT NULL,
  `sql_dump_size` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id_sys_editor_publication`),
  KEY `publication_id` (`environment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=353 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_editor_publication`
--

LOCK TABLES `sys_editor_publication` WRITE;
/*!40000 ALTER TABLE `sys_editor_publication` DISABLE KEYS */;
INSERT INTO `sys_editor_publication` VALUES (1,'fckvuxwvkf1483960410','0',1483960417,1,0,0,3,3,'','',0,90),(2,'felmmlaaur1483960535','0',1483960537,1,0,0,1,1,'','',0,91),(3,'vcwioxkugx1483966701','0',1483966703,1,0,0,1,1,'','',0,91),(4,'vlfasqdqjr1483966721','0',1483966723,1,0,0,1,1,'','',0,91),(5,'tljhipqalz1483966891','0',1483966893,1,0,0,1,1,'','',0,91),(6,'tigalahsvz1483966954','0',1483966955,1,0,0,1,1,'','',0,91),(7,'bnuhonrqqs1483967031','0',1483967032,1,0,0,1,1,'','',0,91),(8,'tcffoocjwh1483967053','0',1483967055,1,0,0,1,1,'','',0,91),(9,'adnsanyeil1483967207','0',1483967209,1,0,0,1,1,'','',0,91),(10,'zmppvykgjj1483967264','0',1483967271,1,0,0,1,1,'','',0,91),(11,'ktztbyznch1483967377','0',1483967378,1,0,0,1,1,'','',0,91),(12,'wvhsqkxolm1483967392','0',1483967393,1,0,0,1,1,'','',0,91),(13,'husaxzysrt1483967618','0',1483967620,1,0,0,1,1,'','',0,91),(14,'hokfotueee1483967626','0',1483967628,1,0,0,1,1,'','',0,91),(15,'gcmvejjwbk1483967743','0',1483967746,1,0,0,1,1,'','',0,91),(16,'lhfujpqosz1483967752','0',1483967754,1,0,0,1,1,'','',0,91),(17,'acjodsuvak1483967947','0',1483967948,1,0,0,1,1,'','',0,90),(18,'xnmzpcvfbb1485177662','0',1485177731,1,0,0,54,54,'','',0,90),(19,'uudkicsaan1485180823','0',1485180828,1,0,0,12,12,'','',0,90),(20,'xfkfwfuuox1485181779','0',1485181783,1,0,0,2,2,'','',0,90),(21,'fjjnxevryz1485181835','0',1485181839,1,0,0,1,1,'','',0,90),(22,'hjxbylbltg1485182312','0',1485182340,1,0,0,3,3,'','',0,91),(23,'weuhajjhco1485182527','0',1485182558,1,0,0,3,3,'','',0,91),(24,'rlqgzydmum1485182594','0',1485182596,1,0,0,1,3,'','',0,91),(25,'sqgkmdgbso1485183317','0',1485183320,1,0,0,4,4,'','',0,90),(26,'narubtwaji1485184865','0',1485184892,1,0,0,1,1,'','',0,91),(27,'jrjwrudhjm1485184948','0',1485184974,1,0,0,1,1,'','',0,91),(28,'chetdnrzgv1485184997','0',1485185001,1,0,0,2,2,'','',0,90),(29,'nuaawmbvyz1485185474','0',1485185477,1,0,0,2,2,'','',0,90),(30,'xqfusdvamk1485185507','0',1485185509,1,0,0,1,1,'','',0,90),(31,'outyjnkgaj1485185567','0',1485185569,1,0,0,1,1,'','',0,90),(32,'fsecegelyd1485185587','0',1485185589,1,0,0,1,1,'','',0,90),(33,'slxedcudwo1485185632','0',1485185635,1,0,0,1,1,'','',0,90),(34,'eahkujqwrt1485185723','0',1485185725,1,0,0,1,1,'','',0,90),(35,'foedojtkwv1485185915','0',1485185917,1,0,0,2,2,'','',0,90),(36,'hfiyhujmzt1485186180','0',1485186182,1,0,0,1,1,'','',0,90),(37,'tsqrbyyowj1485186821','0',1485186824,1,0,0,1,1,'','',0,90),(38,'ppabvavdhf1485187222','0',1485187224,1,0,0,1,1,'','',0,90),(39,'cznlyphztj1485187623','0',1485187625,1,0,0,1,1,'','',0,90),(40,'awhfvuezwv1485187976','0',1485187981,1,0,0,6,6,'','',0,90),(41,'hcyvorwczw1485188047','0',1485188050,1,0,0,1,1,'','',0,90),(42,'bzaxzvduam1485188821','0',1485188833,1,0,0,16,16,'','',0,90),(43,'vktnfnpspc1485188871','0',1485188874,1,0,0,1,1,'','',0,90),(44,'qvyhaujksk1485188988','0',1485188993,1,0,0,9,9,'','',0,90),(45,'ifdgyrqtxl1485189101','0',1485189106,1,0,0,12,12,'','',0,90),(46,'htrmmnahtx1485189520','0',1485189529,1,0,0,11,11,'','',0,90),(47,'bqnzlwmivt1485192037','146',1485192106,1,0,0,58,58,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_20_39__bqnzlwmivt1485192037/bqnzlwmivt1485192037','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_20_39__bqnzlwmivt1485192037',0,90),(49,'hdhclxnlga1485193174','146',1485193199,1,0,0,17,17,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_39_35__hdhclxnlga1485193174/hdhclxnlga1485193174','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_39_35__hdhclxnlga1485193174',0,90),(51,'kfkygiwfxl1485193363','146',1485193373,1,0,0,2,2,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_42_44__kfkygiwfxl1485193363/kfkygiwfxl1485193363','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_42_44__kfkygiwfxl1485193363',0,90),(53,'gjfxzvkoxh1485193413','146',1485193424,1,0,0,2,2,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_43_35__gjfxzvkoxh1485193413/gjfxzvkoxh1485193413','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_43_35__gjfxzvkoxh1485193413',0,90),(55,'drhcyxqmku1485193686','146',1485193696,1,0,0,2,2,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_48_08__drhcyxqmku1485193686/drhcyxqmku1485193686','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_48_08__drhcyxqmku1485193686',0,90),(57,'mysinmdchs1485194007','146',1485194016,1,0,0,2,2,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_53_28__mysinmdchs1485194007/mysinmdchs1485194007','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_53_28__mysinmdchs1485194007',0,90),(59,'hpvwfeylvh1485194116','146',1485194135,1,0,0,9,9,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_55_18__hpvwfeylvh1485194116/hpvwfeylvh1485194116','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__18_55_18__hpvwfeylvh1485194116',0,90),(61,'ziuxmmwpih1485195063','146',1485195071,1,0,0,1,1,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__19_11_05__ziuxmmwpih1485195063/ziuxmmwpih1485195063','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__19_11_05__ziuxmmwpih1485195063',0,90),(63,'lqxevsjhry1485195184','146',1485195200,1,0,0,7,7,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__19_13_05__lqxevsjhry1485195184/lqxevsjhry1485195184','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__19_13_05__lqxevsjhry1485195184',0,90),(65,'eraeiydsez1485195340','146',1485195350,1,0,0,3,3,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__19_15_42__eraeiydsez1485195340/eraeiydsez1485195340','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__19_15_42__eraeiydsez1485195340',0,90),(67,'guxrceapnr1485195886','146',1485195908,1,0,0,11,11,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__19_24_48__guxrceapnr1485195886/guxrceapnr1485195886','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_23__19_24_48__guxrceapnr1485195886',0,90),(69,'gbqxlpbxsm1485245511','146',1485245521,1,0,0,1,1,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_24__09_11_53__gbqxlpbxsm1485245511/gbqxlpbxsm1485245511','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_24__09_11_53__gbqxlpbxsm1485245511',0,90),(71,'ewpigyllvs1485252805','0',1485252806,1,0,0,0,0,'','',0,90),(73,'cylvvfaelk1485277199','0',1485277204,1,0,0,57,57,'','',0,90),(75,'rnmmlnlryc1485354719','0',1485354726,1,0,0,51,51,'','',0,90),(77,'iqpsnubvfx1485355453','146',1485355463,1,0,0,1,1,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_25__15_44_15__iqpsnubvfx1485355453/iqpsnubvfx1485355453','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_25__15_44_15__iqpsnubvfx1485355453',0,90),(79,'rnymzeqzql1485360595','0',1485360604,1,0,0,78,78,'','',0,91),(81,'owwmdruigk1485360624','0',1485360633,1,0,0,78,78,'','',0,91),(83,'wralprbwmn1485361031','0',1485361041,1,0,0,81,81,'','',0,90),(85,'jazmoycwla1485361451','0',1485361453,1,0,0,11,11,'','',0,90),(87,'knlawxvpzy1485361604','0',1485361606,1,0,0,2,2,'','',0,90),(89,'tgvkymgdnp1485361643','0',1485361645,1,0,0,2,2,'','',0,91),(91,'thlzioicxf1485361698','0',1485361699,1,0,0,4,4,'','',0,90),(93,'xrozcfdjae1485361898','0',1485361899,1,0,0,1,1,'','',0,90),(95,'wazsovrvjp1485361924','0',1485361925,1,0,0,1,1,'','',0,90),(97,'nfuvlvokgs1485361954','0',1485361956,1,0,0,1,1,'','',0,90),(99,'uhisihcauj1485362071','0',1485362073,1,0,0,5,5,'','',0,90),(101,'yeytyjhgof1485362093','0',1485362095,1,0,0,1,1,'','',0,90),(103,'yniouynicj1485362111','0',1485362113,1,0,0,1,1,'','',0,90),(105,'atetbcdhoj1485362389','0',1485362394,1,0,0,78,78,'','',0,90),(107,'guhyzlcutk1485362412','0',1485362414,1,0,0,1,1,'','',0,90),(109,'bmfssyakhk1485362555','0',1485362556,1,0,0,7,7,'','',0,90),(111,'lmapqijzrq1485362834','0',1485362839,1,0,0,74,74,'','',0,90),(113,'kcemmvcchx1485363082','0',1485363086,1,0,0,68,68,'','',0,90),(115,'ewiklxbmpa1485363845','0',1485363851,1,0,0,88,88,'','',0,90),(117,'fnecwhgchv1485364037','0',1485364042,1,0,0,48,48,'','',0,90),(119,'jwtlzjlgnl1485364290','0',1485364294,1,0,0,51,51,'','',0,90),(121,'owodzqcqvs1485364571','0',1485364575,1,0,0,42,42,'','',0,90),(123,'heactbjkxi1485365019','0',1485365025,1,0,0,90,90,'','',0,90),(125,'snfpeoniqb1485365159','0',1485365161,1,0,0,4,4,'','',0,90),(127,'ssnliqhjch1485365273','0',1485365275,1,0,0,8,8,'','',0,90),(129,'aypkwmsgzz1485365380','146',1485365405,1,0,0,21,21,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_25__18_29_40__aypkwmsgzz1485365380/aypkwmsgzz1485365380','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_25__18_29_40__aypkwmsgzz1485365380',0,90),(131,'opoxpyxkun1485365415','146',1485365437,1,0,0,17,17,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_25__18_30_15__opoxpyxkun1485365415/opoxpyxkun1485365415','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_25__18_30_15__opoxpyxkun1485365415',0,90),(133,'emxxgwrqrh1485365640','0',1485365643,1,0,0,52,52,'','',0,90),(135,'rstxccocrs1485365740','0',1485365742,1,0,0,11,11,'','',0,90),(137,'kvihpoqxbl1485365801','0',1485365804,1,0,0,7,7,'','',0,90),(139,'dcudsxvtze1485365925','0',1485365930,1,0,0,16,16,'','',0,90),(141,'gwcgznatci1485366050','0',1485366056,1,0,0,20,20,'','',0,90),(143,'lbfmeixuvv1485366134','0',1485366136,1,0,0,10,10,'','',0,90),(145,'vblghmmsnj1485423343','0',1485423352,1,0,0,48,48,'','',0,91),(147,'ecqrdfjaqa1485423421','0',1485423427,1,0,0,49,49,'','',0,90),(149,'zayhtpdptu1485443473','146',1485443559,1,0,0,68,68,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__16_11_13__zayhtpdptu1485443473/zayhtpdptu1485443473','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__16_11_13__zayhtpdptu1485443473',0,90),(151,'ybuikppemh1485443603','146',1485443613,1,0,0,2,2,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__16_13_23__ybuikppemh1485443603/ybuikppemh1485443603','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__16_13_23__ybuikppemh1485443603',0,90),(153,'nvekfmtklq1485445314','146',1485445344,1,0,0,18,18,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__16_41_54__nvekfmtklq1485445314/nvekfmtklq1485445314','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__16_41_54__nvekfmtklq1485445314',0,90),(155,'bbjyvonojk1485445573','146',1485445593,1,0,0,9,9,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__16_46_13__bbjyvonojk1485445573/bbjyvonojk1485445573','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__16_46_13__bbjyvonojk1485445573',0,90),(157,'ulkixikaxk1485448075','146',1485448084,1,0,0,1,1,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_27_55__ulkixikaxk1485448075/ulkixikaxk1485448075','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_27_55__ulkixikaxk1485448075',0,90),(159,'qrfyfqgafl1485448189','146',1485448205,1,0,0,7,7,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_29_49__qrfyfqgafl1485448189/qrfyfqgafl1485448189','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_29_49__qrfyfqgafl1485448189',0,90),(161,'huvlpgtynj1485448534','146',1485448552,1,0,0,9,9,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_35_34__huvlpgtynj1485448534/huvlpgtynj1485448534','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_35_34__huvlpgtynj1485448534',0,90),(163,'ywwzucjhvd1485448812','146',1485448820,1,0,0,1,1,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_40_12__ywwzucjhvd1485448812/ywwzucjhvd1485448812','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_40_12__ywwzucjhvd1485448812',0,90),(165,'nntdasozie1485449200','146',1485449208,1,0,0,1,1,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_46_40__nntdasozie1485449200/nntdasozie1485449200','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__17_46_40__nntdasozie1485449200',0,90),(167,'qpohibbrjg1485451359','146',1485451373,1,0,0,8,8,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__18_22_39__qpohibbrjg1485451359/qpohibbrjg1485451359','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__18_22_39__qpohibbrjg1485451359',0,90),(169,'mddsqklrmf1485452015','146',1485452039,1,0,0,15,15,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__18_33_35__mddsqklrmf1485452015/mddsqklrmf1485452015','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__18_33_35__mddsqklrmf1485452015',0,90),(171,'uasqfjnezt1485452353','146',1485452361,1,0,0,1,1,'/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__18_39_14__uasqfjnezt1485452353/uasqfjnezt1485452353','/space/applisdata/labbook2-5bis/storage/publication/jzipcxqhqd1483959677538/2017_01_26__18_39_14__uasqfjnezt1485452353',0,90),(173,'ihzrggdgvq1485506739','0',1485506740,1,0,0,0,0,'','',0,90),(175,'jsbunnsyof1485507016','0',1485507018,1,0,0,6,6,'','',0,90),(177,'hsabvumdrr1485524072','0',1485524078,1,0,0,76,76,'','',0,90),(179,'rqdqrmcslf1485532718','0',1485532730,1,0,0,162,162,'','',0,90),(181,'cbivgvnihp1485533252','0',1485533253,1,0,0,1,1,'','',0,90),(183,'fupmtuseep1485533283','0',1485533285,1,0,0,1,1,'','',0,90),(185,'puybgrejej1485533328','0',1485533330,1,0,0,1,1,'','',0,90),(187,'aromuiagqv1485533416','0',1485533418,1,0,0,8,8,'','',0,90),(189,'yznenbamrb1485533430','0',1485533432,1,0,0,1,1,'','',0,90),(191,'fyzkfbmrrh1485533488','0',1485533491,1,0,0,4,4,'','',0,90),(193,'jziivahegy1485534605','0',1485534607,1,0,0,15,15,'','',0,90),(195,'ruomwoyhpp1485534613','0',1485534613,1,0,0,0,0,'','',0,90),(197,'lhxuavrgmc1485534632','0',1485534634,1,0,0,4,4,'','',0,90),(199,'oqrjjpwlmt1485535823','0',1485535824,1,0,0,1,1,'','',0,90),(201,'dbovrxqqkj1485536001','0',1485536001,1,0,0,0,0,'','',0,90),(203,'qdsplfkzpw1485536029','0',1485536029,1,0,0,0,0,'','',0,90),(205,'dbdzvhlvcc1485536044','0',1485536046,1,0,0,1,1,'','',0,90),(207,'pudmflrypd1485538529','0',1485538535,1,0,0,39,39,'','',0,90),(209,'nlvfubxjww1485769906','0',1485769924,1,0,0,81,81,'','',0,90),(211,'oawqrmogzi1485773455','0',1485773464,1,0,0,89,89,'','',0,90),(213,'phgwvnfuul1485773636','0',1485773637,1,0,0,0,0,'','',0,90),(215,'ssqgwmsjwy1485773837','0',1485773839,1,0,0,1,1,'','',0,90),(217,'npykhusssk1485775850','0',1485775854,1,0,0,11,11,'','',0,91),(219,'qagisgekno1485775897','0',1485775900,1,0,0,12,12,'','',0,90),(221,'bfttaqjspj1485783879','0',1485783885,1,0,0,48,48,'','',0,90),(223,'bhsvjzbsai1485784293','0',1485784295,1,0,0,10,10,'','',0,90),(225,'ooartqzpjf1485784901','0',1485784902,1,0,0,1,1,'','',0,90),(227,'osywrcqbpe1485785276','0',1485785277,1,0,0,1,1,'','',0,90),(229,'zmfafwmhqt1485786593','0',1485786597,1,0,0,20,20,'','',0,90),(231,'jrxijavbun1485786647','0',1485786648,1,0,0,1,1,'','',0,90),(233,'pkmrinmsmn1485786792','0',1485786794,1,0,0,2,2,'','',0,90),(235,'cazaipgcrq1485786993','0',1485786995,1,0,0,2,2,'','',0,90),(237,'oiziojrutl1485787053','0',1485787056,1,0,0,1,1,'','',0,90),(239,'jwdnvczdvz1485787079','0',1485787080,1,0,0,1,1,'','',0,90),(241,'zaqkphlgbt1485787102','0',1485787104,1,0,0,1,1,'','',0,90),(243,'xwycutxqel1485787240','0',1485787243,1,0,0,2,2,'','',0,90),(245,'wybnvgdatw1485787303','0',1485787305,1,0,0,1,1,'','',0,90),(247,'dclxiwceyf1485787556','0',1485787558,1,0,0,24,24,'','',0,90),(249,'ppklodrmia1485787690','0',1485787692,1,0,0,4,4,'','',0,90),(251,'xcwqilcayn1485787909','0',1485787911,1,0,0,3,3,'','',0,90),(253,'llbenmxwyi1485787942','0',1485787944,1,0,0,1,1,'','',0,90),(255,'rtoatfhrwy1485788063','0',1485788064,1,0,0,4,4,'','',0,90),(257,'dazncqniuo1485788119','0',1485788120,1,0,0,2,2,'','',0,90),(259,'lkpwnqabvw1485788343','0',1485788347,1,0,0,77,77,'','',0,90),(261,'vbpilhgsku1485788414','0',1485788415,1,0,0,1,1,'','',0,90),(263,'kbabessebp1485792745','0',1485792745,1,0,0,0,0,'','',0,90),(265,'pfhtenrveu1485860328','0',1485860330,1,0,0,1,1,'','',0,90),(266,'zstbsfeueg1489760183','0',1489760192,1,0,0,17,17,'','',0,90),(267,'ntwdscznit1489762235','0',1489762240,1,0,0,2,2,'','',0,90),(268,'xzrtxtxmbt1489763393','0',1489763401,1,0,0,10,10,'','',0,90),(269,'wifziisbej1489763407','0',1489763407,1,0,0,0,0,'','',0,90),(270,'ygagyjcvab1489763612','0',1489763617,1,0,0,4,4,'','',0,90),(271,'xbcozhkuws1489764012','0',1489764019,1,0,0,15,15,'','',0,90),(272,'lestjqvirp1489764080','0',1489764084,1,0,0,1,1,'','',0,90),(273,'mwemlrxeqp1489766028','0',1489766034,1,0,0,12,12,'','',0,90),(274,'ahaotbwlmm1489766187','0',1489766189,1,0,0,1,1,'','',0,90),(275,'wmaomtpade1489766263','0',1489766265,1,0,0,1,1,'','',0,90),(276,'ahuuervxzo1489766383','0',1489766386,1,0,0,2,2,'','',0,90),(277,'fkotccefjl1489766492','0',1489766494,1,0,0,1,1,'','',0,90),(278,'vrjbqxwusu1489766600','0',1489766603,1,0,0,5,5,'','',0,90),(279,'avematvpch1489766632','0',1489766635,1,0,0,1,1,'','',0,90),(280,'ufdguqrman1489766687','0',1489766691,1,0,0,1,1,'','',0,90),(281,'vtvrhnacno1489766736','0',1489766740,1,0,0,2,2,'','',0,90),(282,'rnpinycaae1489767009','0',1489767020,1,0,0,52,52,'','',0,90),(283,'sdzpilqdjf1490005504','0',1490005509,1,0,0,3,3,'','',0,90),(284,'qjlggfulek1490005578','0',1490005581,1,0,0,4,4,'','',0,90),(285,'nyonicuure1490005638','0',1490005641,1,0,0,8,8,'','',0,90),(286,'kcrwfgbyrr1490005668','0',1490005671,1,0,0,1,1,'','',0,90),(287,'frfezrtwkn1490005703','0',1490005707,1,0,0,2,2,'','',0,90),(288,'wsouyhipvz1490005794','0',1490005798,1,0,0,1,1,'','',0,90),(289,'qdqennprbz1490005830','0',1490005832,1,0,0,1,1,'','',0,90),(290,'gnyxqwevot1490005906','0',1490005910,1,0,0,15,15,'','',0,90),(291,'qfwxvirjvb1490005965','0',1490006013,1,0,0,13,13,'','',0,91),(292,'ssohunluhy1490006050','0',1490006100,1,0,0,13,13,'','',0,91),(293,'gwgcvjaigc1490006274','0',1490006325,1,0,0,20,20,'','',0,91),(294,'flhnjqchem1490006906','0',1490006937,1,0,0,22,22,'','',0,90),(295,'fkxxwmqzlj1490006986','0',1490006998,1,0,0,7,7,'','',0,90),(296,'qdcvubbeir1490007023','0',1490007027,1,0,0,1,1,'','',0,90),(297,'fmkcmtancs1490007248','0',1490007251,1,0,0,1,1,'','',0,90),(298,'waumudsrxo1490007521','0',1490007533,1,0,0,14,14,'','',0,90),(299,'bfcgnywgvl1490007693','0',1490007722,1,0,0,32,32,'','',0,90),(300,'hbtuelsskr1490007852','0',1490007875,1,0,0,24,24,'','',0,90),(301,'pfmjdzukst1490016112','0',1490016118,1,0,0,7,7,'','',0,90),(302,'vxgutfiqgc1490016138','0',1490016144,1,0,0,4,4,'','',0,90),(303,'rocczcxivz1490016185','0',1490016206,1,0,0,13,13,'','',0,90),(304,'alteqfkzsj1490016215','0',1490016240,1,0,0,14,14,'','',0,90),(305,'knwjrfklga1490016242','0',1490016273,1,0,0,17,17,'','',0,90),(306,'dgythlqwsu1490016300','0',1490016348,1,0,0,31,31,'','',0,90),(307,'izchqcyrtp1490016360','0',1490016366,1,0,0,18,18,'','',0,90),(308,'vttbalhtlz1490016405','0',1490016414,1,0,0,23,23,'','',0,90),(309,'mbqvjhzfmo1490016476','0',1490016485,1,0,0,32,32,'','',0,90),(310,'gxjghcfujd1490016520','0',1490016525,1,0,0,1,1,'','',0,90),(311,'ngvgotujgk1490016568','0',1490016571,1,0,0,4,4,'','',0,90),(312,'zwopechqwx1490016667','0',1490016672,1,0,0,9,9,'','',0,90),(313,'tbnrdlkkzw1490017849','0',1490017853,1,0,0,1,1,'','',0,90),(314,'vkgbbdvekf1490018037','0',1490018043,1,0,0,3,3,'','',0,90),(315,'dmudlujipp1490024932','0',1490024939,1,0,0,10,10,'','',0,90),(316,'pyymomjhfb1490025156','0',1490025159,1,0,0,1,1,'','',0,90),(317,'swwtoxlisy1490025325','0',1490025328,1,0,0,3,3,'','',0,90),(318,'tctckptkvz1490025630','0',1490025639,1,0,0,7,7,'','',0,90),(319,'dzxsmfyjhu1490025664','0',1490025666,1,0,0,1,1,'','',0,90),(320,'skbjkqvzdd1490025874','0',1490025883,1,0,0,11,11,'','',0,90),(321,'rocsewofpk1490026264','0',1490026268,1,0,0,3,3,'','',0,90),(322,'qlcywycpfv1490026310','0',1490026313,1,0,0,1,1,'','',0,90),(323,'mblymrtgfg1490026361','0',1490026364,1,0,0,2,2,'','',0,90),(324,'aqsmhajqhj1490029238','0',1490029241,1,0,0,1,1,'','',0,90),(325,'ujbmdrnmqm1490089869','0',1490089878,1,0,0,21,21,'','',0,90),(326,'qtnqqwubef1492162194','0',1492162229,1,0,0,42,42,'','',0,90),(327,'ocgqysmamh1492162237','0',1492162239,1,0,0,0,0,'','',0,90),(328,'dzueazwlpr1492162496','0',1492162500,1,0,0,5,5,'','',0,90),(329,'mjqeybeaha1492162680','0',1492162684,1,0,0,2,2,'','',0,90),(330,'rpsxqenduc1492162984','0',1492162988,1,0,0,2,2,'','',0,90),(331,'ywmxsctwsv1492177941','0',1492177960,1,0,0,36,36,'','',0,90),(332,'gldyostrmw1492506353','0',1492506359,1,0,0,24,24,'','',0,90),(333,'vhldnjutxx1492507099','0',1492507102,1,0,0,41,41,'','',0,90),(334,'yavpxdseor1492507455','0',1492507458,1,0,0,14,14,'','',0,90),(335,'mzouczsbif1492507627','0',1492507629,1,0,0,9,9,'','',0,90),(336,'rpkwyblers1492676492','0',1492676505,1,0,0,0,0,'','',0,90),(337,'xkwdomlbic1492676621','0',1492676657,1,0,0,3,3,'','',0,90),(338,'muifykseyt1492676783','0',1492676788,1,0,0,1,1,'','',0,90),(339,'vpkkxmpeod1492677225','0',1492677229,1,0,0,4,4,'','',0,90),(340,'eqrzhgxjya1492677303','0',1492677306,1,0,0,4,4,'','',0,90),(341,'bsuwjwwakz1492677348','0',1492677351,1,0,0,2,2,'','',0,90),(342,'jhejrwgiwk1492678561','0',1492678562,1,0,0,0,0,'','',0,90),(343,'ujllsannpf1492683785','0',1492683791,1,0,0,1,1,'','',0,90),(344,'bovvastdjw1492688672','0',1492688676,1,0,0,1,1,'','',0,90),(345,'eqfdiwxqei1492689261','0',1492689264,1,0,0,1,1,'','',0,90),(346,'uqqmmzlkhq1492769399','0',1492769405,1,0,0,13,13,'','',0,90),(347,'sbiaoywoby1497453220','0',1497453226,1,0,0,0,0,'','',0,90),(348,'aapgmbgzfz1497544018','0',1497544024,1,0,0,1,1,'','',0,91),(349,'lbfqwuwpub1497544596','0',1497544597,1,0,0,0,0,'','',0,90),(350,'ktmuwjzasl1497544869','0',1497544873,1,0,0,5,5,'','',0,90),(351,'uxwuhejwls1497544879','0',1497544881,1,0,0,0,0,'','',0,90),(352,'kyufrtflub1497545127','0',1497545130,1,0,0,1,1,'','',0,90);
/*!40000 ALTER TABLE `sys_editor_publication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_module`
--

DROP TABLE IF EXISTS `sys_module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_module` (
  `id_sys_module` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `version` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_sys_module`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_module`
--

LOCK TABLES `sys_module` WRITE;
/*!40000 ALTER TABLE `sys_module` DISABLE KEYS */;
INSERT INTO `sys_module` VALUES (1,'default',NULL),(2,'auth',NULL),(3,'style',NULL),(4,'mainframe',NULL),(5,'form',NULL);
/*!40000 ALTER TABLE `sys_module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_module_acl`
--

DROP TABLE IF EXISTS `sys_module_acl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_module_acl` (
  `id_sys_module_acl` int(11) NOT NULL AUTO_INCREMENT,
  `id_sys_module` int(11) NOT NULL,
  `code` varchar(45) NOT NULL,
  `label` varchar(50) NOT NULL,
  PRIMARY KEY (`id_sys_module_acl`),
  KEY `id_sys_module` (`id_sys_module`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_module_acl`
--

LOCK TABLES `sys_module_acl` WRITE;
/*!40000 ALTER TABLE `sys_module_acl` DISABLE KEYS */;
INSERT INTO `sys_module_acl` VALUES (1,1,'use','Use'),(2,2,'use','Use'),(3,3,'use','Use'),(4,4,'use','Use'),(5,5,'use','Use');
/*!40000 ALTER TABLE `sys_module_acl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_project`
--

DROP TABLE IF EXISTS `sys_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_project` (
  `id_sys_project` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(200) NOT NULL,
  `name` varchar(20) NOT NULL,
  `tables_prefix` varchar(4) NOT NULL,
  `lang` varchar(10) NOT NULL,
  `id_resource` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_sys_project`),
  UNIQUE KEY `sys_project_tables_prefix` (`tables_prefix`),
  UNIQUE KEY `sys_project_name` (`name`),
  UNIQUE KEY `idx_prefix` (`tables_prefix`),
  KEY `id_resource` (`id_resource`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_project`
--

LOCK TABLES `sys_project` WRITE;
/*!40000 ALTER TABLE `sys_project` DISABLE KEYS */;
INSERT INTO `sys_project` VALUES (1,'RESAOLAB - SIGL','sigl','sigl','fr',20000);
/*!40000 ALTER TABLE `sys_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_project_user`
--

DROP TABLE IF EXISTS `sys_project_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_project_user` (
  `id_sys_project_user` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_sys_user` int(11) NOT NULL,
  `id_sys_project` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  PRIMARY KEY (`id_sys_project_user`),
  KEY `id_sys_user_sys_project` (`id_sys_user`,`id_sys_project`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_project_user`
--

LOCK TABLES `sys_project_user` WRITE;
/*!40000 ALTER TABLE `sys_project_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_project_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_script`
--

DROP TABLE IF EXISTS `sys_script`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_script` (
  `id_script` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `start_date` datetime NOT NULL,
  `end_date` datetime DEFAULT NULL,
  `actions_exec_time` mediumtext,
  `consumer_report` mediumtext,
  `id_user` int(11) DEFAULT NULL,
  `id_sys_project` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_script`)
) ENGINE=InnoDB AUTO_INCREMENT=398 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_script`
--

LOCK TABLES `sys_script` WRITE;
/*!40000 ALTER TABLE `sys_script` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_script` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_script_error`
--

DROP TABLE IF EXISTS `sys_script_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_script_error` (
  `id_script_error` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_script` int(10) unsigned NOT NULL,
  `message` mediumtext NOT NULL,
  `trace` longtext,
  PRIMARY KEY (`id_script_error`),
  KEY `id_script` (`id_script`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_script_error`
--

LOCK TABLES `sys_script_error` WRITE;
/*!40000 ALTER TABLE `sys_script_error` DISABLE KEYS */;
INSERT INTO `sys_script_error` VALUES (1,394,'Unable to create tmp directory to process Compare : C:\\Wamp\\www\\tmp/\\5ca32b41c6e5e','#0 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\library\\Resource\\XML\\ScriptPlayer\\Action\\Migration\\VarsetUpdateDiff.php(153): Core_Library_Resource_XML_VarSet->Compare(Object(Core_Library_Resource_XML_VarSet))\n#1 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\library\\Resource\\XML\\ScriptPlayer\\Action\\Migration\\VarsetUpdateDiff.php(215): Core_Library_Resource_XML_ScriptPlayer_Action_Migration_VarsetUpdateDiff->Test(Array)\n#2 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\library\\Migration\\ScriptPlayer.php(98): Core_Library_Resource_XML_ScriptPlayer_Action_Migration_VarsetUpdateDiff->Exec(true)\n#3 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\library\\Migration\\ScriptPlayer.php(177): Core_Library_Migration_ScriptPlayer->ExecAction(Object(Core_Library_Resource_XML_ScriptPlayer_Action_Migration_VarsetUpdateDiff), true)\n#4 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\tools\\Voo4CliApi.php(1434): Core_Library_Migration_ScriptPlayer->Play(Array)\n#5 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\tools\\CliApi.php(69): Voo4CliApi->migration()\n#6 C:\\Wamp64\\www\\apps\\LABBOOK\\resources\\cron\\voo4_cli.php(89): CliApi->process()\n#7 {main}'),(2,395,'Unable to create tmp directory to process Compare : C:\\Wamp\\www\\tmp/\\5ca32b5637240','#0 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\library\\Resource\\XML\\ScriptPlayer\\Action\\Migration\\VarsetVarUpdate.php(164): Core_Library_Resource_XML_VarSet->Compare(Object(Core_Library_Resource_XML_VarSet))\n#1 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\library\\Resource\\XML\\ScriptPlayer\\Action\\Migration\\VarsetVarUpdate.php(216): Core_Library_Resource_XML_ScriptPlayer_Action_Migration_VarsetVarUpdate->Test(Array)\n#2 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\library\\Migration\\ScriptPlayer.php(98): Core_Library_Resource_XML_ScriptPlayer_Action_Migration_VarsetVarUpdate->Exec(true)\n#3 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\library\\Migration\\ScriptPlayer.php(177): Core_Library_Migration_ScriptPlayer->ExecAction(Object(Core_Library_Resource_XML_ScriptPlayer_Action_Migration_VarsetVarUpdate), true)\n#4 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\tools\\Voo4CliApi.php(1434): Core_Library_Migration_ScriptPlayer->Play(Array)\n#5 C:\\Wamp64\\www\\libs\\voozanoo4\\2.26\\src\\tools\\CliApi.php(69): Voo4CliApi->migration()\n#6 C:\\Wamp64\\www\\apps\\LABBOOK\\resources\\cron\\voo4_cli.php(89): CliApi->process()\n#7 {main}');
/*!40000 ALTER TABLE `sys_script_error` ENABLE KEYS */;
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
INSERT INTO `sys_user` VALUES (1,'editor',NULL,NULL,'c80bc97702842b8276a2c48e336eb23442b191a5:SLjcJuagLBTEIMdFl2-_dW0j03K8VXEl',NULL,NULL,'1team@epiconcept.fr',1,1,'2017-01-23 18:20:22');
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

-- Dump completed on 2021-03-04 12:11:55