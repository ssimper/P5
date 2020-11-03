-- MySQL dump 10.13  Distrib 8.0.21, for Linux (x86_64)
--
-- Host: localhost    Database: off_2
-- ------------------------------------------------------
-- Server version	8.0.21-0ubuntu0.20.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8mb4' COLLATE 'utf8mb4_unicode_ci';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nutriscore`
--

DROP TABLE IF EXISTS `nutriscore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nutriscore` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(1) UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nutriscore`
--

LOCK TABLES `nutriscore` WRITE;
/*!40000 ALTER TABLE `nutriscore` DISABLE KEYS */;
/*!40000 ALTER TABLE `nutriscore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `bar_code` bigint NOT NULL,
  `name` varchar(150) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `nutriscore_id` smallint unsigned NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`bar_code`),
  KEY `nutriscore_id` (`nutriscore_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`nutriscore_id`) REFERENCES `nutriscore` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stored_products`
--

DROP TABLE IF EXISTS `stored_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stored_product` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `original_bar_code` bigint NOT NULL,
  `substitution_bar_code` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_original_bar_code` (`original_bar_code`),
  KEY `fk_substitution_bar_code` (`substitution_bar_code`), 
  CONSTRAINT `fk_original_bar_code` FOREIGN KEY (`original_bar_code`) REFERENCES `product` (`bar_code`),
  CONSTRAINT `fk_substitution_bar_code` FOREIGN KEY (`substitution_bar_code`) REFERENCES `product` (`bar_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stored_product`
--

LOCK TABLES `stored_product` WRITE;
/*!40000 ALTER TABLE `stored_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `stored_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_category`
--

DROP TABLE IF EXISTS `product_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_category` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `product_bar_code` bigint NOT NULL,
  `category_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_product_bar_code` (`product_bar_code`),
  KEY `fk_category_id` (`category_id`),
  CONSTRAINT `fk_category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `fk_product_bar_code` FOREIGN KEY (`product_bar_code`) REFERENCES `product` (`bar_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_category`
--

LOCK TABLES `product_category` WRITE;
/*!40000 ALTER TABLE `product_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_store`
--

DROP TABLE IF EXISTS `product_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_store` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `product_bar_code` bigint NOT NULL,
  `store_id` smallint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_bar_code` (`product_bar_code`),
  KEY `store_id` (`store_id`),
  CONSTRAINT `product_store_ibfk_1` FOREIGN KEY (`product_bar_code`) REFERENCES `product` (`bar_code`),
  CONSTRAINT `product_store_ibfk_2` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_store`
--

LOCK TABLES `product_store` WRITE;
/*!40000 ALTER TABLE `product_store` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(150) UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8mb4' COLLATE 'utf8mb4_unicode_ci';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store`
--

LOCK TABLES `store` WRITE;
/*!40000 ALTER TABLE `store` DISABLE KEYS */;
/*!40000 ALTER TABLE `store` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-13 22:25:33
