-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: basculax
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `movimiento`
--

DROP TABLE IF EXISTS `movimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimiento` (
  `idmovimiento` int NOT NULL AUTO_INCREMENT,
  `idproveedor` int DEFAULT NULL,
  `idconductor` int DEFAULT NULL,
  `idvehiculo` int DEFAULT NULL,
  `idproducto` int DEFAULT NULL,
  `idorigen` int DEFAULT NULL,
  `iddestino` int DEFAULT NULL,
  `observaciones` varchar(255) DEFAULT NULL,
  `fechaentrada` date DEFAULT NULL,
  `horaentrada` time DEFAULT NULL,
  `fechasalida` date DEFAULT NULL,
  `horasalida` time DEFAULT NULL,
  `pesoentrada` int DEFAULT NULL,
  `pesosalida` int DEFAULT NULL,
  `pesoneto` int DEFAULT NULL,
  `idoperario` int DEFAULT NULL,
  `idbascula` int DEFAULT NULL,
  `idbodega` int DEFAULT NULL,
  `idusuario` int DEFAULT NULL,
  `tipomovimiento` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`idmovimiento`),
  KEY `idproveedor` (`idproveedor`),
  KEY `idconductor` (`idconductor`),
  KEY `idvehiculo` (`idvehiculo`),
  KEY `idproducto` (`idproducto`),
  KEY `idorigen` (`idorigen`),
  KEY `iddestino` (`iddestino`),
  KEY `idoperario` (`idoperario`),
  KEY `idbascula` (`idbascula`),
  KEY `idbodega` (`idbodega`),
  KEY `idusuario` (`idusuario`),
  CONSTRAINT `movimiento_ibfk_1` FOREIGN KEY (`idproveedor`) REFERENCES `proveedores` (`id`),
  CONSTRAINT `movimiento_ibfk_10` FOREIGN KEY (`idusuario`) REFERENCES `user` (`id`),
  CONSTRAINT `movimiento_ibfk_2` FOREIGN KEY (`idconductor`) REFERENCES `conductores` (`id`),
  CONSTRAINT `movimiento_ibfk_3` FOREIGN KEY (`idvehiculo`) REFERENCES `vehiculo` (`id`),
  CONSTRAINT `movimiento_ibfk_4` FOREIGN KEY (`idproducto`) REFERENCES `productos` (`IDproducto`),
  CONSTRAINT `movimiento_ibfk_5` FOREIGN KEY (`idorigen`) REFERENCES `origenes` (`idorigen`),
  CONSTRAINT `movimiento_ibfk_6` FOREIGN KEY (`iddestino`) REFERENCES `destinos` (`iddestino`),
  CONSTRAINT `movimiento_ibfk_7` FOREIGN KEY (`idoperario`) REFERENCES `operarios` (`idoperario`),
  CONSTRAINT `movimiento_ibfk_8` FOREIGN KEY (`idbascula`) REFERENCES `basculas` (`Idbascula`),
  CONSTRAINT `movimiento_ibfk_9` FOREIGN KEY (`idbodega`) REFERENCES `bodegas` (`idBodega`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimiento`
--

LOCK TABLES `movimiento` WRITE;
/*!40000 ALTER TABLE `movimiento` DISABLE KEYS */;
INSERT INTO `movimiento` VALUES (1,6,6,11,1,1,1,'Ninguna','2024-03-22','18:18:47','2024-03-23','11:38:58',73,59,14,NULL,NULL,NULL,NULL,'E'),(2,1,1,12,2,2,2,'No hay observaciones','2024-03-22','18:19:32','2024-03-23','11:59:39',93,5,88,NULL,NULL,NULL,NULL,'E'),(3,1,1,13,3,3,3,'Ninguna','2024-03-23','11:38:29','2024-03-23','11:52:56',94,16,78,NULL,NULL,NULL,NULL,'E'),(4,1,1,14,4,4,4,'no','2024-03-23','11:55:57',NULL,NULL,88,NULL,NULL,NULL,NULL,NULL,NULL,'E'),(5,1,1,15,5,5,5,'No hay','2024-03-23','11:58:57',NULL,NULL,18,NULL,NULL,NULL,NULL,NULL,NULL,'E'),(6,1,1,11,5,1,1,'No hay observaciones','2024-03-26','12:19:06','2024-03-26','12:19:50',98,58,40,NULL,NULL,NULL,NULL,'E'),(7,3,4,13,7,7,7,'Ninguna','2024-04-02','18:02:25','2024-04-06','12:14:54',94,17,77,NULL,NULL,NULL,NULL,'E'),(8,5,1,18,8,8,8,'No hay Observaciones','2024-04-02','18:17:46','2024-04-06','11:02:09',82,20,61,NULL,NULL,NULL,NULL,'E'),(9,5,5,7,7,7,7,'No hay','2024-04-06','12:04:51','2024-04-06','12:55:37',73,8,65,NULL,NULL,NULL,NULL,'S'),(10,3,4,14,1,1,2,'No hay observaciones','2024-04-06','12:53:10','2024-04-06','12:56:34',91,81,10,NULL,NULL,NULL,NULL,'E'),(11,4,4,19,2,2,4,'No','2024-04-06','13:04:44','2024-04-06','13:05:02',73,99,26,NULL,NULL,NULL,NULL,'S'),(12,3,6,11,2,3,4,'No hay','2024-04-08','17:49:46','2024-04-08','17:54:34',22,91,1,NULL,NULL,NULL,NULL,'E'),(13,1,1,14,1,4,4,'No','2024-04-08','18:02:19','2024-04-08','18:02:48',99,82,17,NULL,NULL,NULL,NULL,'E'),(14,6,6,11,1,1,1,'No','2024-04-08','18:04:15','2024-04-08','18:04:55',65,52,13,NULL,NULL,NULL,NULL,'S'),(15,1,1,12,1,2,1,'No','2024-04-08','18:05:52','2024-04-08','18:07:21',20,99,79,NULL,NULL,NULL,NULL,'S'),(16,6,6,11,1,1,1,'No','2024-04-09','10:13:52','2024-04-09','10:15:52',94,92,2,NULL,NULL,NULL,NULL,'E'),(17,6,6,12,3,2,1,'No','2024-04-09','10:25:05','2024-04-12','08:16:14',99,85,14,NULL,NULL,NULL,NULL,'E'),(18,6,6,11,1,1,1,'No','2024-04-12','08:17:39',NULL,NULL,90,NULL,NULL,NULL,NULL,NULL,NULL,'S'),(19,13,12,11,12,13,13,'Traslado','2024-04-12','09:31:38','2024-04-12','09:32:20',89,17,72,NULL,NULL,NULL,NULL,'E'),(20,6,6,11,1,1,1,'No hay','2024-04-20','13:33:53',NULL,NULL,37,NULL,NULL,NULL,NULL,NULL,NULL,'E'),(21,4,4,12,2,2,2,'Ninguna','2024-04-20','13:40:37','2024-04-20','13:43:03',44,21,23,NULL,NULL,NULL,NULL,'E'),(22,8,4,13,3,3,3,'Ninguna','2024-04-20','13:46:03','2024-04-20','13:47:26',99,90,9,NULL,NULL,NULL,NULL,'E'),(23,1,1,11,3,1,1,'No hay','2024-04-25','17:54:53',NULL,NULL,90,NULL,NULL,NULL,NULL,NULL,NULL,'E');
/*!40000 ALTER TABLE `movimiento` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-27 19:36:48
