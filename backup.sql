-- MySQL dump 10.13  Distrib 5.7.40, for Win64 (x86_64)
--
-- Host: localhost    Database: club
-- ------------------------------------------------------
-- Server version	5.7.40

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
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity` (
  `activity_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` longtext,
  `location` varchar(200) DEFAULT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `max_participants` int(11) DEFAULT NULL,
  `current_participants` int(11) NOT NULL,
  `status` smallint(6) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `club_id` bigint(20) DEFAULT NULL,
  `organizer_id` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`activity_id`),
  KEY `活动表_club_id_104cf791_fk_社团表_club_id` (`club_id`),
  KEY `活动表_organizer_id_b7276623_fk_成员表_member_id` (`organizer_id`),
  CONSTRAINT `活动表_club_id_104cf791_fk_社团表_club_id` FOREIGN KEY (`club_id`) REFERENCES `club` (`club_id`),
  CONSTRAINT `活动表_organizer_id_b7276623_fk_成员表_member_id` FOREIGN KEY (`organizer_id`) REFERENCES `member` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES (14,'英语角晨读（书法社）','活动说明：英语角晨读（书法社）的详细安排与注意事项。','线上会议','2025-12-03 08:12:55.731999','2025-12-03 12:12:55.731999',30,3,3,'2025-11-27 08:12:55.731999',13,'2021010'),(15,'摄影外拍（英语角）','活动说明：摄影外拍（英语角）的详细安排与注意事项。','校门口集合','2026-03-04 08:12:55.731999','2026-03-04 11:12:55.731999',50,2,3,'2026-03-01 08:12:55.731999',16,'2021031'),(16,'招新宣讲会（英语角）','活动说明：招新宣讲会（英语角）的详细安排与注意事项。','操场','2026-02-14 08:12:55.731999','2026-02-14 13:12:55.731999',80,0,3,'2026-02-10 08:12:55.731999',16,'2021031'),(17,'作品展览（书法社）','活动说明：作品展览（书法社）的详细安排与注意事项。','线上会议','2026-01-30 08:12:55.731999','2026-01-30 11:12:55.731999',80,1,3,'2026-01-12 08:12:55.731999',13,'2021007'),(18,'英语角晨读（书法社）','活动说明：英语角晨读（书法社）的详细安排与注意事项。','体育馆','2026-02-13 08:12:55.731999','2026-02-13 12:12:55.731999',50,5,3,'2026-01-28 08:12:55.731999',13,'2021008'),(19,'换届大会（篮球社）','活动说明：换届大会（篮球社）的详细安排与注意事项。','线上会议','2026-01-10 08:12:55.731999','2026-01-10 10:12:55.731999',30,4,3,'2026-01-09 08:12:55.731999',14,'2021014'),(20,'迎新晚会（科技创新协会）','活动说明：迎新晚会（科技创新协会）的详细安排与注意事项。','图书馆报告厅','2026-02-10 08:12:55.731999','2026-02-10 12:12:55.731999',50,2,1,'2026-01-27 08:12:55.731999',12,'2021001'),(21,'线上竞赛（科技创新协会）','活动说明：线上竞赛（科技创新协会）的详细安排与注意事项。','校门口集合','2026-02-28 08:12:55.731999','2026-02-28 11:12:55.731999',80,0,2,'2026-02-11 08:12:55.731999',12,'2021002'),(22,'周末训练（摄影协会）','活动说明：周末训练（摄影协会）的详细安排与注意事项。','教学楼A101','2025-12-10 08:12:55.731999','2025-12-10 10:12:55.731999',80,4,2,'2025-11-27 08:12:55.731999',15,'2021019'),(23,'线上竞赛（摄影协会）','活动说明：线上竞赛（摄影协会）的详细安排与注意事项。','体育馆','2025-12-17 08:12:55.731999','2025-12-17 10:12:55.731999',100,7,1,'2025-12-16 08:12:55.731999',15,'2021022'),(24,'作品展览（书法社）','活动说明：作品展览（书法社）的详细安排与注意事项。','体育馆','2026-02-27 08:12:55.731999','2026-02-27 10:12:55.731999',100,2,3,'2026-02-24 08:12:55.731999',13,'2021008'),(25,'主题讲座（篮球社）','活动说明：主题讲座（篮球社）的详细安排与注意事项。','操场','2025-12-13 08:12:55.731999','2025-12-13 13:12:55.731999',50,2,3,'2025-12-04 08:12:55.731999',14,'2021013');
/*!40000 ALTER TABLE `activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_comment`
--

DROP TABLE IF EXISTS `activity_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity_comment` (
  `comment_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `activity_id` bigint(20) NOT NULL,
  `member_id` varchar(30) NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `activity_comment_activity_id_899d176d_fk_activity_activity_id` (`activity_id`),
  KEY `activity_comment_member_id_cc87f890_fk_member_member_id` (`member_id`),
  CONSTRAINT `activity_comment_activity_id_899d176d_fk_activity_activity_id` FOREIGN KEY (`activity_id`) REFERENCES `activity` (`activity_id`),
  CONSTRAINT `activity_comment_member_id_cc87f890_fk_member_member_id` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_comment`
--

LOCK TABLES `activity_comment` WRITE;
/*!40000 ALTER TABLE `activity_comment` DISABLE KEYS */;
INSERT INTO `activity_comment` VALUES (1,'有点东西啊 好玩','2026-04-05 22:48:42.098777',20,'2021002');
/*!40000 ALTER TABLE `activity_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_like`
--

DROP TABLE IF EXISTS `activity_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity_like` (
  `like_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `like_time` datetime(6) DEFAULT NULL,
  `activity_id` bigint(20) NOT NULL,
  `member_id` varchar(30) NOT NULL,
  PRIMARY KEY (`like_id`),
  UNIQUE KEY `activity_like_activity_id_member_id_cdd7ce50_uniq` (`activity_id`,`member_id`),
  KEY `activity_like_member_id_4236cffc_fk_member_member_id` (`member_id`),
  CONSTRAINT `activity_like_activity_id_4879b024_fk_activity_activity_id` FOREIGN KEY (`activity_id`) REFERENCES `activity` (`activity_id`),
  CONSTRAINT `activity_like_member_id_4236cffc_fk_member_member_id` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_like`
--

LOCK TABLES `activity_like` WRITE;
/*!40000 ALTER TABLE `activity_like` DISABLE KEYS */;
INSERT INTO `activity_like` VALUES (1,'2026-04-05 22:48:32.450393',20,'2021002');
/*!40000 ALTER TABLE `activity_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_photo`
--

DROP TABLE IF EXISTS `activity_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity_photo` (
  `photo_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `photo` varchar(100) NOT NULL,
  `description` longtext,
  `upload_time` datetime(6) DEFAULT NULL,
  `activity_id` bigint(20) NOT NULL,
  `member_id` varchar(30) NOT NULL,
  PRIMARY KEY (`photo_id`),
  KEY `activity_photo_activity_id_fe0a0421_fk_activity_activity_id` (`activity_id`),
  KEY `activity_photo_member_id_e1c99402_fk_member_member_id` (`member_id`),
  CONSTRAINT `activity_photo_activity_id_fe0a0421_fk_activity_activity_id` FOREIGN KEY (`activity_id`) REFERENCES `activity` (`activity_id`),
  CONSTRAINT `activity_photo_member_id_e1c99402_fk_member_member_id` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_photo`
--

LOCK TABLES `activity_photo` WRITE;
/*!40000 ALTER TABLE `activity_photo` DISABLE KEYS */;
INSERT INTO `activity_photo` VALUES (1,'activity_photos/屏幕截图_2026-01-13_235231.png','六百六十六','2026-04-05 22:49:03.376295',20,'2021002');
/*!40000 ALTER TABLE `activity_photo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_registration`
--

DROP TABLE IF EXISTS `activity_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity_registration` (
  `registration_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `register_time` datetime(6) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `remark` longtext,
  `activity_id` bigint(20) NOT NULL,
  `member_id` varchar(30) NOT NULL,
  PRIMARY KEY (`registration_id`),
  UNIQUE KEY `活动报名表_activity_id_member_id_a1c626a0_uniq` (`activity_id`,`member_id`),
  KEY `活动报名表_member_id_3810ed22_fk_成员表_member_id` (`member_id`),
  CONSTRAINT `活动报名表_activity_id_765b9f7b_fk_活动表_activity_id` FOREIGN KEY (`activity_id`) REFERENCES `activity` (`activity_id`),
  CONSTRAINT `活动报名表_member_id_3810ed22_fk_成员表_member_id` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_registration`
--

LOCK TABLES `activity_registration` WRITE;
/*!40000 ALTER TABLE `activity_registration` DISABLE KEYS */;
INSERT INTO `activity_registration` VALUES (38,'2026-03-15 16:12:55.753124',4,NULL,14,'2021008'),(39,'2026-03-15 16:12:55.755702',1,NULL,14,'2021009'),(40,'2026-03-15 16:12:55.758042',3,NULL,14,'2021011'),(41,'2026-03-15 16:12:55.759476',1,NULL,14,'2021010'),(42,'2026-03-15 16:12:55.761675',4,NULL,14,'2021006'),(43,'2026-03-15 16:12:55.762837',2,NULL,14,'2021007'),(44,'2026-03-15 16:12:55.766058',2,NULL,15,'2021033'),(45,'2026-03-15 16:12:55.767307',1,NULL,15,'2021035'),(46,'2026-03-15 16:12:55.769688',3,NULL,15,'2021032'),(47,'2026-03-15 16:12:55.771195',3,NULL,16,'2021033'),(48,'2026-03-15 16:12:55.772264',1,NULL,17,'2021006'),(49,'2026-03-15 16:12:55.774296',2,NULL,18,'2021010'),(50,'2026-03-15 16:12:55.775804',1,NULL,18,'2021009'),(51,'2026-03-15 16:12:55.777929',1,NULL,18,'2021008'),(52,'2026-03-15 16:12:55.778970',2,NULL,18,'2021006'),(53,'2026-03-15 16:12:55.781447',4,NULL,18,'2021011'),(54,'2026-03-15 16:12:55.783556',1,NULL,18,'2021007'),(55,'2026-03-15 16:12:55.785694',1,NULL,19,'2021012'),(56,'2026-03-15 16:12:55.786981',4,NULL,19,'2021013'),(57,'2026-03-15 16:12:55.788257',2,NULL,19,'2021016'),(58,'2026-03-15 16:12:55.790324',1,NULL,19,'2021018'),(59,'2026-03-15 16:12:55.791513',2,NULL,19,'2021017'),(60,'2026-03-15 16:12:55.793747',2,NULL,20,'2021002'),(61,'2026-03-15 16:12:55.795779',1,NULL,20,'2021003'),(62,'2026-03-15 16:12:55.797512',2,NULL,22,'2021027'),(63,'2026-03-15 16:12:55.799634',3,NULL,22,'2021022'),(64,'2026-03-15 16:12:55.800773',2,NULL,22,'2021025'),(65,'2026-03-15 16:12:55.802819',2,NULL,22,'2021030'),(66,'2026-03-15 16:12:55.804865',1,NULL,22,'2021024'),(67,'2026-03-15 16:12:55.806226',2,NULL,23,'2021027'),(68,'2026-03-15 16:12:55.808454',4,NULL,23,'2021025'),(69,'2026-03-15 16:12:55.810476',4,NULL,23,'2021029'),(70,'2026-03-15 16:12:55.811621',2,NULL,23,'2021021'),(71,'2026-03-15 16:12:55.813699',3,NULL,23,'2021028'),(72,'2026-03-15 16:12:55.814989',2,NULL,23,'2021023'),(73,'2026-03-15 16:12:55.817015',2,NULL,23,'2021022'),(74,'2026-03-15 16:12:55.819208',1,NULL,23,'2021020'),(75,'2026-03-15 16:12:55.820294',3,NULL,23,'2021024'),(76,'2026-03-15 16:12:55.822328',2,NULL,23,'2021026'),(77,'2026-03-15 16:12:55.823497',1,NULL,23,'2021030'),(78,'2026-03-15 16:12:55.826070',4,NULL,23,'2021019'),(79,'2026-03-15 16:12:55.828152',2,NULL,24,'2021006'),(80,'2026-03-15 16:12:55.830361',2,NULL,24,'2021008'),(81,'2026-03-15 16:12:55.832386',3,NULL,25,'2021013'),(82,'2026-03-15 16:12:55.833531',3,NULL,25,'2021012'),(83,'2026-03-15 16:12:55.834901',1,NULL,25,'2021018'),(84,'2026-03-15 16:12:55.837069',2,NULL,25,'2021017');
/*!40000 ALTER TABLE `activity_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcement`
--

DROP TABLE IF EXISTS `announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `announcement` (
  `announcement_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `publish_time` datetime(6) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `is_top` tinyint(1) NOT NULL,
  `publisher_id` varchar(32) DEFAULT NULL,
  `club_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`announcement_id`),
  KEY `announcement_publisher_id_8af3cd4c_fk_myadmin_id` (`publisher_id`),
  KEY `announcement_club_id_39d9f373_fk_club_club_id` (`club_id`),
  CONSTRAINT `announcement_club_id_39d9f373_fk_club_club_id` FOREIGN KEY (`club_id`) REFERENCES `club` (`club_id`),
  CONSTRAINT `announcement_publisher_id_8af3cd4c_fk_myadmin_id` FOREIGN KEY (`publisher_id`) REFERENCES `myadmin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcement`
--

LOCK TABLES `announcement` WRITE;
/*!40000 ALTER TABLE `announcement` DISABLE KEYS */;
INSERT INTO `announcement` VALUES (1,'欢迎新同学加入社团大家庭','亲爱的同学们：\n\n欢迎大家加入我们的社团！在这里，你将有机会参与各种有趣的活动，结识志同道合的朋友，提升自己的综合素质。\n\n请大家积极参与社团活动，遵守社团规章制度，共同营造良好的社团氛围。\n\n祝大家在社团生活中收获满满！','2026-03-15 16:12:55.855739',1,1,'gyz',NULL),(2,'关于2026年春季招新活动的通知','各社团负责人：\r\n\r\n2026年春季招新活动即将开始，请各社团做好招新准备工作，包括制定招新计划、准备宣传材料、安排面试等。\r\n\r\n招新时间：4月1日-4月15日\r\n招新要求：热爱社团工作，有责任心，积极向上\r\n\r\n请于3月25日前将招新计划报送至学生处。','2026-03-15 16:12:55.856810',1,0,'gyz',NULL),(3,'社团活动安全须知','为了确保社团活动的顺利开展和同学们的安全，请大家务必遵守以下规定：\n\n1. 参加活动前请确认身体状况，如有不适及时告知负责人\n2. 活动过程中服从指挥，听从安排\n3. 注意个人财物安全\n4. 活动结束后及时返校，不得在外逗留\n\n安全第一，祝大家玩得开心！','2026-03-15 16:12:55.859297',1,0,'gyz',NULL),(4,'社团经费使用管理办法','为规范社团经费使用，提高资金使用效益，特制定本办法：\n\n1. 经费使用必须符合社团发展需要和学校相关规定\n2. 大额支出须经社长审批，重大活动经费使用须报学生处备案\n3. 所有发票须妥善保管，作为报销凭证\n4. 定期公布经费使用情况，接受成员监督\n\n请大家共同维护社团利益。','2026-03-15 16:12:55.861328',1,0,'gyz',NULL),(6,'11111','22222','2026-03-15 16:37:45.562633',1,0,'gyz',NULL),(7,'111111231','22222','2026-03-15 16:39:41.226699',1,1,NULL,12);
/*!40000 ALTER TABLE `announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add 社团',7,'add_club'),(26,'Can change 社团',7,'change_club'),(27,'Can delete 社团',7,'delete_club'),(28,'Can view 社团',7,'view_club'),(29,'Can add 部门',8,'add_department'),(30,'Can change 部门',8,'change_department'),(31,'Can delete 部门',8,'delete_department'),(32,'Can view 部门',8,'view_department'),(33,'Can add 管理员',9,'add_myadmin'),(34,'Can change 管理员',9,'change_myadmin'),(35,'Can delete 管理员',9,'delete_myadmin'),(36,'Can view 管理员',9,'view_myadmin'),(37,'Can add 角色',10,'add_role'),(38,'Can change 角色',10,'change_role'),(39,'Can delete 角色',10,'delete_role'),(40,'Can view 角色',10,'view_role'),(41,'Can add 成员',11,'add_member'),(42,'Can change 成员',11,'change_member'),(43,'Can delete 成员',11,'delete_member'),(44,'Can view 成员',11,'view_member'),(45,'Can add 活动',12,'add_activity'),(46,'Can change 活动',12,'change_activity'),(47,'Can delete 活动',12,'delete_activity'),(48,'Can view 活动',12,'view_activity'),(49,'Can add 活动报名',13,'add_activityregistration'),(50,'Can change 活动报名',13,'change_activityregistration'),(51,'Can delete 活动报名',13,'delete_activityregistration'),(52,'Can view 活动报名',13,'view_activityregistration'),(53,'Can add 招新批次',14,'add_recruitment'),(54,'Can change 招新批次',14,'change_recruitment'),(55,'Can delete 招新批次',14,'delete_recruitment'),(56,'Can view 招新批次',14,'view_recruitment'),(57,'Can add 招新报名',15,'add_recruitmentapplication'),(58,'Can change 招新报名',15,'change_recruitmentapplication'),(59,'Can delete 招新报名',15,'delete_recruitmentapplication'),(60,'Can view 招新报名',15,'view_recruitmentapplication'),(61,'Can add 公告',16,'add_announcement'),(62,'Can change 公告',16,'change_announcement'),(63,'Can delete 公告',16,'delete_announcement'),(64,'Can view 公告',16,'view_announcement'),(65,'Can add 关注',17,'add_follow'),(66,'Can change 关注',17,'change_follow'),(67,'Can delete 关注',17,'delete_follow'),(68,'Can view 关注',17,'view_follow'),(69,'Can add 活动点赞',18,'add_activitylike'),(70,'Can change 活动点赞',18,'change_activitylike'),(71,'Can delete 活动点赞',18,'delete_activitylike'),(72,'Can view 活动点赞',18,'view_activitylike'),(73,'Can add 活动评论',19,'add_activitycomment'),(74,'Can change 活动评论',19,'change_activitycomment'),(75,'Can delete 活动评论',19,'delete_activitycomment'),(76,'Can view 活动评论',19,'view_activitycomment'),(77,'Can add 活动照片',20,'add_activityphoto'),(78,'Can change 活动照片',20,'change_activityphoto'),(79,'Can delete 活动照片',20,'delete_activityphoto'),(80,'Can view 活动照片',20,'view_activityphoto');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `club`
--

DROP TABLE IF EXISTS `club`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `club` (
  `club_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `established_date` date DEFAULT NULL,
  `president` varchar(30) DEFAULT NULL,
  `contact_phone` varchar(11) DEFAULT NULL,
  `contact_email` varchar(254) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`club_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `club`
--

LOCK TABLES `club` WRITE;
/*!40000 ALTER TABLE `club` DISABLE KEYS */;
INSERT INTO `club` VALUES (12,'科技创新协会','开展编程、竞赛、项目实践等活动。','2025-08-10','张伟','13800001001','tech@club.edu.cn',1,'2026-03-15 16:12:55.646555'),(13,'书法社','传承书法艺术，定期练笔与展览。','2025-05-17','李芳','13800001002','calligraphy@club.edu.cn',1,'2026-03-15 16:12:55.659160'),(14,'篮球社','组织训练与院系篮球赛。','2025-08-10','王强','13800001003','basketball@club.edu.cn',1,'2026-03-15 16:12:55.660348'),(15,'摄影协会','外拍、讲座、作品分享。','2024-05-26','刘洋','13800001004','photo@club.edu.cn',1,'2026-03-15 16:12:55.662568'),(16,'英语角','口语练习、观影、四六级互助。','2024-04-22','陈敏','13800001005','english@club.edu.cn',1,'2026-03-15 16:12:55.664762');
/*!40000 ALTER TABLE `club` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `department` (
  `department_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `create_time` datetime(6) DEFAULT NULL,
  `club_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`department_id`),
  KEY `部门表_club_id_acc5781e_fk_社团表_club_id` (`club_id`),
  CONSTRAINT `部门表_club_id_acc5781e_fk_社团表_club_id` FOREIGN KEY (`club_id`) REFERENCES `club` (`club_id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (42,'科技策划部','策划部日常事务','2026-03-15 08:12:55.665764',12),(43,'科技宣传部','宣传部日常事务','2026-03-15 08:12:55.667353',12),(44,'科技办公室','办公室日常事务','2026-03-15 08:12:55.668353',12),(45,'科技技术部','技术部日常事务','2026-03-15 08:12:55.669407',12),(46,'书法策划部','策划部日常事务','2026-03-15 08:12:55.673160',13),(47,'书法技术部','技术部日常事务','2026-03-15 08:12:55.674573',13),(48,'书法宣传部','宣传部日常事务','2026-03-15 08:12:55.676079',13),(49,'书法办公室','办公室日常事务','2026-03-15 08:12:55.677120',13),(50,'篮球外联部','外联部日常事务','2026-03-15 08:12:55.679613',14),(51,'篮球宣传部','宣传部日常事务','2026-03-15 08:12:55.681164',14),(52,'篮球技术部','技术部日常事务','2026-03-15 08:12:55.682170',14),(53,'篮球策划部','策划部日常事务','2026-03-15 08:12:55.684190',14),(54,'摄影策划部','策划部日常事务','2026-03-15 08:12:55.685698',15),(55,'摄影办公室','办公室日常事务','2026-03-15 08:12:55.687995',15),(56,'摄影宣传部','宣传部日常事务','2026-03-15 08:12:55.688998',15),(57,'摄影外联部','外联部日常事务','2026-03-15 08:12:55.690002',15),(58,'英语办公室','办公室日常事务','2026-03-15 08:12:55.692487',16),(59,'英语外联部','外联部日常事务','2026-03-15 08:12:55.694394',16);
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(12,'app01','activity'),(19,'app01','activitycomment'),(18,'app01','activitylike'),(20,'app01','activityphoto'),(13,'app01','activityregistration'),(16,'app01','announcement'),(7,'app01','club'),(8,'app01','department'),(17,'app01','follow'),(11,'app01','member'),(9,'app01','myadmin'),(14,'app01','recruitment'),(15,'app01','recruitmentapplication'),(10,'app01','role'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-17 13:30:53.063970'),(2,'auth','0001_initial','2025-12-17 13:30:53.377089'),(3,'admin','0001_initial','2025-12-17 13:30:53.448234'),(4,'admin','0002_logentry_remove_auto_add','2025-12-17 13:30:53.454040'),(5,'admin','0003_logentry_add_action_flag_choices','2025-12-17 13:30:53.459996'),(6,'app01','0001_initial','2025-12-17 13:30:53.772687'),(7,'contenttypes','0002_remove_content_type_name','2025-12-17 13:30:53.828026'),(8,'auth','0002_alter_permission_name_max_length','2025-12-17 13:30:53.863070'),(9,'auth','0003_alter_user_email_max_length','2025-12-17 13:30:53.896449'),(10,'auth','0004_alter_user_username_opts','2025-12-17 13:30:53.903769'),(11,'auth','0005_alter_user_last_login_null','2025-12-17 13:30:53.943708'),(12,'auth','0006_require_contenttypes_0002','2025-12-17 13:30:53.946735'),(13,'auth','0007_alter_validators_add_error_messages','2025-12-17 13:30:53.954482'),(14,'auth','0008_alter_user_username_max_length','2025-12-17 13:30:53.986411'),(15,'auth','0009_alter_user_last_name_max_length','2025-12-17 13:30:54.019750'),(16,'auth','0010_alter_group_name_max_length','2025-12-17 13:30:54.054797'),(17,'auth','0011_update_proxy_permissions','2025-12-17 13:30:54.063929'),(18,'auth','0012_alter_user_first_name_max_length','2025-12-17 13:30:54.097845'),(19,'sessions','0001_initial','2025-12-17 13:30:54.127981'),(20,'app01','0002_add_password','2026-03-15 07:48:24.111371'),(21,'app01','0003_alter_activity_table_and_more','2026-03-15 08:10:21.738524'),(22,'app01','0004_create_announcement','2026-03-15 08:12:14.412332'),(23,'app01','0005_announcement_club','2026-03-15 08:25:04.872767'),(24,'app01','0006_member_avatar_member_nickname_follow','2026-04-05 13:26:30.431125'),(25,'app01','0007_activityphoto_activitycomment_activitylike','2026-04-05 14:44:25.847635');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('abe3gj4svgp8ehsd4z4kgi525j2lyi2b','eyJpbmZvIjp7InR5cGUiOiJhZG1pbiIsImlkIjoiZ3l6IiwibmFtZSI6Imd5eiJ9fQ:1w2OoG:Ke6Bwy3ThxTI16tuq2mvtEPOcYVJRdrmNQTcw4UkdJ8','2026-03-31 07:25:48.165214'),('cuh91fnbjdkgw3v7j9a1ukg9vnjh6dp3','eyJpbmZvIjp7InR5cGUiOiJhZG1pbiIsImlkIjoiZ3l6IiwibmFtZSI6Imd5eiJ9fQ:1w9NRp:P7VlhAe5aKAV8DY-HtpF_WfN3aEoBdn9l6my9paTuBs','2026-04-19 13:23:29.118256'),('e3xryjl7r6ibg7n9alavi1lg9kuzs2o1','.eJwVikkKgCAUhu_yr1s40IBnESTrCYJaSAYh3j1dfkOFT-6Cqni-m6AQKVrKmODPToIJztjaMe1xZF0Wx2ddNmFlt0co1oyTywn5CmQCvRSgRGs_1pYbRQ:1w1h1x:e82LPalRtBfvoGr0bVUrzOdNJZ0w4Ni9VvlpkWM-4t0','2026-03-29 08:41:01.176980'),('npc7bmt2hj5ae3ef2sjzfvlhc7iil1ka','.eJwljU0KgzAQhe8yMDutmaSKulOwpxBCUsciJCpWhSLevbHdve_98A4Yxn6C8oD1MzOU4NlbXiCCoQskhSQhZMDR-Ctut8zatN3uPfXBfbrN6qtJMoJlcqwd7-ygDGh2s5olbBLP3WCSP78TbFKsCfPHTxRYpNhkmOdYVZdT1Fg3OhxnsaCYlJZKkVK3eXzBeX4BzxUxRg:1w9OO3:5eHTVkc8swG07DaCmWmDGqvfv36zkjo_8JlYC5otihQ','2026-04-19 14:23:39.585162'),('ouluctm3ca15aspcnkixqkwvh4svmm3f','eyJpbmZvIjp7ImlkIjoiZ3l6IiwibmFtZSI6Imd5eiJ9fQ:1vVrfY:faWtAl9MIctYaHkWgsdG4zjLJmFVPNeF5lPO8yleo0U','2025-12-31 13:34:20.758504');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follow`
--

DROP TABLE IF EXISTS `follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow` (
  `follow_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `follow_time` datetime(6) DEFAULT NULL,
  `followed_id` varchar(30) NOT NULL,
  `follower_id` varchar(30) NOT NULL,
  PRIMARY KEY (`follow_id`),
  UNIQUE KEY `follow_follower_id_followed_id_600fe32b_uniq` (`follower_id`,`followed_id`),
  KEY `follow_followed_id_90ed3317_fk_member_member_id` (`followed_id`),
  CONSTRAINT `follow_followed_id_90ed3317_fk_member_member_id` FOREIGN KEY (`followed_id`) REFERENCES `member` (`member_id`),
  CONSTRAINT `follow_follower_id_839f26a2_fk_member_member_id` FOREIGN KEY (`follower_id`) REFERENCES `member` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follow`
--

LOCK TABLES `follow` WRITE;
/*!40000 ALTER TABLE `follow` DISABLE KEYS */;
INSERT INTO `follow` VALUES (1,NULL,'2021003','2021002'),(2,NULL,'2021004','2021002'),(3,NULL,'2021005','2021002');
/*!40000 ALTER TABLE `follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member` (
  `member_id` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `gender` smallint(6) DEFAULT NULL,
  `grade` smallint(6) DEFAULT NULL,
  `major` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `join_time` datetime(6) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `remark` longtext,
  `club_id` bigint(20) DEFAULT NULL,
  `department_id` bigint(20) DEFAULT NULL,
  `role_id` bigint(20) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `nickname` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`member_id`),
  KEY `成员表_club_id_eee6abb0_fk_社团表_club_id` (`club_id`),
  KEY `成员表_department_id_4baa0894_fk_部门表_department_id` (`department_id`),
  KEY `成员表_role_id_d43fd2e9_fk_角色表_role_id` (`role_id`),
  CONSTRAINT `成员表_club_id_eee6abb0_fk_社团表_club_id` FOREIGN KEY (`club_id`) REFERENCES `club` (`club_id`),
  CONSTRAINT `成员表_department_id_4baa0894_fk_部门表_department_id` FOREIGN KEY (`department_id`) REFERENCES `department` (`department_id`),
  CONSTRAINT `成员表_role_id_d43fd2e9_fk_角色表_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES ('2021001','白涛',NULL,NULL,NULL,NULL,NULL,'2025-09-08 08:12:55.697962',1,'',NULL,NULL,NULL,'9b7bdac3cbd4af86551d5f27d64a5291','avatars/test.jpg',NULL),('2021002','段伟',2,5,'工商管理','13854620192','2021002@student.edu.cn','2025-10-28 08:12:55.697962',1,'',12,43,NULL,'4f798c24a8c2c93a9384f5a3abdce6dc','avatars/屏幕截图_2026-01-13_233133.png',NULL),('2021003','范磊',1,1,'软件工程','13809327060','2021003@student.edu.cn','2025-07-13 08:12:55.699026',1,NULL,12,44,2,NULL,NULL,NULL),('2021004','贺鑫',2,2,'法学','13841291820','2021004@student.edu.cn','2025-07-30 08:12:55.700040',1,NULL,12,45,2,NULL,NULL,NULL),('2021005','唐芳',1,2,'软件工程','13875722267','2021005@student.edu.cn','2025-10-23 08:12:55.701165',1,NULL,12,44,2,NULL,NULL,NULL),('2021006','陈芳',2,2,'金融学','13893176828','2021006@student.edu.cn','2025-12-28 08:12:55.704403',1,NULL,13,46,1,NULL,NULL,NULL),('2021007','漕芳',2,1,'工商管理','13830778654','2021007@student.edu.cn','2025-10-11 08:12:55.705914',1,NULL,13,47,2,'9b7bdac3cbd4af86551d5f27d64a5291',NULL,NULL),('2021008','蒋超',1,3,'计算机科学与技术','13859566535','2021008@student.edu.cn','2025-05-05 08:12:55.707035',1,NULL,13,49,2,NULL,NULL,NULL),('2021009','吕磊',1,4,'机械工程','13836774792','2021009@student.edu.cn','2025-06-29 08:12:55.707035',1,NULL,13,46,2,NULL,NULL,NULL),('2021010','刘伟',1,2,'电子信息','13851417146','2021010@student.edu.cn','2025-09-12 08:12:55.708206',1,NULL,13,46,2,NULL,NULL,NULL),('2021011','高勇',2,2,'软件工程','13829600282','2021011@student.edu.cn','2025-11-04 08:12:55.709240',1,NULL,13,47,2,NULL,NULL,NULL),('2021012','黎杰',1,4,'电子信息','13854602925','2021012@student.edu.cn','2025-12-16 08:12:55.710243',1,NULL,14,52,1,NULL,NULL,NULL),('2021013','邓伟',2,2,'工商管理','13828397191','2021013@student.edu.cn','2025-07-28 08:12:55.711560',1,NULL,14,52,2,NULL,NULL,NULL),('2021014','郝芳',2,3,'汉语言文学','13879422768','2021014@student.edu.cn','2025-09-06 08:12:55.712565',1,NULL,14,50,2,NULL,NULL,NULL),('2021015','黄杰',2,5,'计算机科学与技术','13800853100','2021015@student.edu.cn','2025-06-25 08:12:55.713598',1,NULL,14,52,2,NULL,NULL,NULL),('2021016','任强',2,5,'法学','13827122340','2021016@student.edu.cn','2025-10-30 08:12:55.714776',1,NULL,14,51,2,NULL,NULL,NULL),('2021017','钟超',2,4,'数学与应用数学','13886447507','2021017@student.edu.cn','2025-07-16 08:12:55.714776',1,NULL,14,50,2,NULL,NULL,NULL),('2021018','文军',1,1,'计算机科学与技术','13844334215','2021018@student.edu.cn','2025-02-28 08:12:55.715778',1,NULL,14,53,2,NULL,NULL,NULL),('2021019','孔飞',2,4,'汉语言文学','13882361098','2021019@student.edu.cn','2025-03-30 08:12:55.718284',1,NULL,15,55,1,NULL,NULL,NULL),('2021020','尹鑫',1,2,'工商管理','13818815973','2021020@student.edu.cn','2026-02-02 08:12:55.719335',1,NULL,15,54,2,NULL,NULL,NULL),('2021021','潘飞',1,4,'软件工程','13892930195','2021021@student.edu.cn','2025-06-30 08:12:55.720498',1,NULL,15,56,2,NULL,NULL,NULL),('2021022','卢勇',1,1,'英语','13899833935','2021022@student.edu.cn','2025-11-28 08:12:55.720498',1,NULL,15,55,2,NULL,NULL,NULL),('2021023','阎明',2,5,'金融学','13815345288','2021023@student.edu.cn','2025-11-08 08:12:55.721522',1,NULL,15,56,2,NULL,NULL,NULL),('2021024','顾丽',2,5,'数学与应用数学','13832023574','2021024@student.edu.cn','2025-02-23 08:12:55.722697',1,NULL,15,57,2,NULL,NULL,NULL),('2021025','林飞',2,2,'法学','13851986229','2021025@student.edu.cn','2025-04-28 08:12:55.722697',1,NULL,15,54,2,NULL,NULL,NULL),('2021026','邵鹏',2,3,'机械工程','13875200975','2021026@student.edu.cn','2026-01-08 08:12:55.723964',1,NULL,15,54,2,NULL,NULL,NULL),('2021027','侯伟',2,1,'法学','13872661832','2021027@student.edu.cn','2025-08-23 08:12:55.723964',1,NULL,15,57,2,NULL,NULL,NULL),('2021028','秦芳',1,5,'金融学','13874490360','2021028@student.edu.cn','2025-12-06 08:12:55.725300',1,NULL,15,56,2,NULL,NULL,NULL),('2021029','余芳',1,5,'软件工程','13871116242','2021029@student.edu.cn','2025-02-28 08:12:55.725699',1,NULL,15,54,2,NULL,NULL,NULL),('2021030','段敏',2,3,'英语','13806365288','2021030@student.edu.cn','2025-06-23 08:12:55.726698',1,NULL,15,54,2,NULL,NULL,NULL),('2021031','任静',1,1,'机械工程','13800822387','2021031@student.edu.cn','2026-01-19 08:12:55.728482',1,NULL,16,59,1,NULL,NULL,NULL),('2021032','顾玲',1,4,'计算机科学与技术','13836866296','2021032@student.edu.cn','2025-10-26 08:12:55.728482',1,NULL,16,58,2,NULL,NULL,NULL),('2021033','方伟',2,3,'计算机科学与技术','13838491441','2021033@student.edu.cn','2025-10-23 08:12:55.729991',1,NULL,16,58,2,NULL,NULL,NULL),('2021034','吴明',2,1,'计算机科学与技术','13847508004','2021034@student.edu.cn','2025-11-07 08:12:55.730996',1,NULL,16,58,2,NULL,NULL,NULL),('2021035','孔艳',2,3,'机械工程','13893354225','2021035@student.edu.cn','2025-07-16 08:12:55.730996',1,NULL,16,59,2,NULL,NULL,NULL);
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myadmin`
--

DROP TABLE IF EXISTS `myadmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `myadmin` (
  `id` varchar(32) NOT NULL,
  `user_name` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myadmin`
--

LOCK TABLES `myadmin` WRITE;
/*!40000 ALTER TABLE `myadmin` DISABLE KEYS */;
INSERT INTO `myadmin` VALUES ('fwb','fwb','9b7bdac3cbd4af86551d5f27d64a5291'),('gyz','gyz','9b7bdac3cbd4af86551d5f27d64a5291');
/*!40000 ALTER TABLE `myadmin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recruitment`
--

DROP TABLE IF EXISTS `recruitment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recruitment` (
  `recruitment_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status` smallint(6) DEFAULT '1',
  `create_time` datetime DEFAULT NULL,
  `club_id` bigint(20) NOT NULL,
  PRIMARY KEY (`recruitment_id`),
  KEY `club_id` (`club_id`),
  CONSTRAINT `recruitment_ibfk_1` FOREIGN KEY (`club_id`) REFERENCES `club` (`club_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recruitment`
--

LOCK TABLES `recruitment` WRITE;
/*!40000 ALTER TABLE `recruitment` DISABLE KEYS */;
/*!40000 ALTER TABLE `recruitment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recruitment_application`
--

DROP TABLE IF EXISTS `recruitment_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recruitment_application` (
  `application_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `recruitment_id` bigint(20) NOT NULL,
  `student_id` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `gender` smallint(6) DEFAULT NULL,
  `grade` smallint(6) DEFAULT NULL,
  `major` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `apply_department_id` bigint(20) DEFAULT NULL,
  `status` smallint(6) DEFAULT '1',
  `apply_time` datetime DEFAULT NULL,
  `remark` longtext,
  PRIMARY KEY (`application_id`),
  UNIQUE KEY `recruitment_student_id` (`recruitment_id`,`student_id`),
  KEY `apply_department_id` (`apply_department_id`),
  CONSTRAINT `recruitment_application_ibfk_1` FOREIGN KEY (`recruitment_id`) REFERENCES `recruitment` (`recruitment_id`),
  CONSTRAINT `recruitment_application_ibfk_2` FOREIGN KEY (`apply_department_id`) REFERENCES `department` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recruitment_application`
--

LOCK TABLES `recruitment_application` WRITE;
/*!40000 ALTER TABLE `recruitment_application` DISABLE KEYS */;
/*!40000 ALTER TABLE `recruitment_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `role_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `level` smallint(6) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'社长',1,'社团负责人'),(2,'普通成员',2,'成员');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-07 18:17:04
