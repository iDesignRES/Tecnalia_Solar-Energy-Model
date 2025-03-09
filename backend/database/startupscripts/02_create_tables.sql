/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
-- -----------------------------------
-- Database: `dbidesignres`
-- -----------------------------------
USE `dbidesignres`;

-- -----------------------------------
-- Create table: `t01_idesignres_scales`
-- -----------------------------------
DROP TABLE IF EXISTS `t01_idesignres_scales`;
CREATE TABLE IF NOT EXISTS `t01_idesignres_scales` (
  `uuid` varchar(36) NOT NULL,
  `name` varchar(60) NOT NULL,
  `description` varchar(240),
  `created_date` bigint unsigned NOT NULL,
  `last_modified_date` bigint unsigned NOT NULL,
  `deleted_date` bigint unsigned,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t02_idesignres_layer_formats`
-- -----------------------------------
DROP TABLE IF EXISTS `t02_idesignres_layer_formats`;
CREATE TABLE IF NOT EXISTS `t02_idesignres_layer_formats` (
  `uuid` varchar(36) NOT NULL,
  `name` varchar(30) NOT NULL,
  `extension` varchar(5) NOT NULL,
  `created_date` bigint unsigned NOT NULL,
  `last_modified_date` bigint unsigned NOT NULL,
  `deleted_date` bigint unsigned,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t03_idesignres_processes`
-- -----------------------------------
DROP TABLE IF EXISTS `t03_idesignres_processes`;
CREATE TABLE IF NOT EXISTS `t03_idesignres_processes` (
  `uuid` varchar(36) NOT NULL,
  `name` varchar(40) NOT NULL,
  `description` varchar(150),
  `created_date` bigint unsigned NOT NULL,
  `last_modified_date` bigint unsigned NOT NULL,
  `deleted_date` bigint unsigned,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t11_idesignres_roles`
-- -----------------------------------
DROP TABLE IF EXISTS `t11_idesignres_roles`;
CREATE TABLE IF NOT EXISTS `t11_idesignres_roles` (
  `name` varchar(25) NOT NULL,
  `description` varchar(150) NOT NULL,
  `uuid` varchar(36) NOT NULL,
  `created_date` bigint unsigned NOT NULL,
  `last_modified_date` bigint unsigned NOT NULL,
  `deleted_date` bigint unsigned,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t12_idesignres_users`
-- -----------------------------------
DROP TABLE IF EXISTS `t12_idesignres_users`;
CREATE TABLE IF NOT EXISTS `t12_idesignres_users` (
  `username` varchar(30) NOT NULL,
  `password` varchar(60) NOT NULL,
  `email` varchar(80) NOT NULL,
  `uuid` varchar(36) NOT NULL,
  `created_date` bigint unsigned NOT NULL,
  `last_modified_date` bigint unsigned NOT NULL,
  `deleted_date` bigint unsigned,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t13_idesignres_actors`
-- -----------------------------------
DROP TABLE IF EXISTS `t13_idesignres_actors`;
CREATE TABLE IF NOT EXISTS `t13_idesignres_actors` (
  `username` varchar(30) NOT NULL,
  `role` varchar(25) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t21_idesignres_layers`
-- -----------------------------------
DROP TABLE IF EXISTS `t21_idesignres_layers`;
CREATE TABLE IF NOT EXISTS `t21_idesignres_layers` (
  `uuid` varchar(36) NOT NULL,
  `name` varchar(80) NOT NULL,
  `full_path` varchar(240) NOT NULL,
  `scale_fk` varchar(36) NOT NULL,
  `format_fk` varchar(36) NOT NULL,
  `created_date` bigint unsigned NOT NULL,
  `last_modified_date` bigint unsigned NOT NULL,
  `deleted_date` bigint unsigned,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t22_idesignres_files`
-- -----------------------------------
DROP TABLE IF EXISTS `t22_idesignres_files`;
CREATE TABLE IF NOT EXISTS `t22_idesignres_files` (
  `uuid` varchar(36) NOT NULL,
  `name` varchar(80) NOT NULL,
  `full_path` varchar(240) NOT NULL,
  `created_date` bigint unsigned NOT NULL,
  `last_modified_date` bigint unsigned NOT NULL,
  `deleted_date` bigint unsigned,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t23_idesignres_resources`
-- -----------------------------------
DROP TABLE IF EXISTS `t23_idesignres_resources`;
CREATE TABLE IF NOT EXISTS `t23_idesignres_resources` (
  `uuid` varchar(36) NOT NULL,
  `name` varchar(80) NOT NULL,
  `web_path` varchar(150) NOT NULL,
  `sftp_path` varchar(150) NOT NULL,
  `created_date` bigint unsigned NOT NULL,
  `last_modified_date` bigint unsigned NOT NULL,
  `deleted_date` bigint unsigned,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t31_idesignres_processes_layers`
-- -----------------------------------
DROP TABLE IF EXISTS `t31_idesignres_processes_layers`;
CREATE TABLE `t31_idesignres_processes_layers` (
  `process_fk` varchar(36) NOT NULL,
  `layer_fk` varchar(36) NOT NULL,
  PRIMARY KEY (`process_fk`, `layer_fk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t32_idesignres_processes_files`
-- -----------------------------------
DROP TABLE IF EXISTS `t32_idesignres_processes_files`;
CREATE TABLE `t32_idesignres_processes_files` (
  `process_fk` varchar(36) NOT NULL,
  `file_fk` varchar(36) NOT NULL,
  PRIMARY KEY (`process_fk`, `file_fk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Create table: `t33_idesignres_processes_resources`
-- -----------------------------------
DROP TABLE IF EXISTS `t33_idesignres_processes_resources`;
CREATE TABLE `t33_idesignres_processes_resources` (
  `process_fk` varchar(36) NOT NULL,
  `resource_fk` varchar(36) NOT NULL,
  PRIMARY KEY (`process_fk`, `resource_fk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- -----------------------------------
-- Add constraints
-- -----------------------------------
ALTER TABLE `t01_idesignres_scales`
    ADD CONSTRAINT `uq_scale_uuid` UNIQUE (`name`);

ALTER TABLE `t02_idesignres_layer_formats`
    ADD CONSTRAINT `uq_layer_format_uuid` UNIQUE (`name`);

ALTER TABLE `t03_idesignres_processes`
    ADD CONSTRAINT `uq_process_uuid` UNIQUE (`name`);
	
ALTER TABLE `t11_idesignres_roles`
    ADD CONSTRAINT `uq_role_uuid` UNIQUE (`uuid`);

ALTER TABLE `t12_idesignres_users`
    ADD CONSTRAINT `uq_user_uuid` UNIQUE (`uuid`);

ALTER TABLE `t21_idesignres_layers`
    ADD CONSTRAINT `uq_layer_name` UNIQUE (`name`);
ALTER TABLE `t21_idesignres_layers`
    ADD CONSTRAINT `fk_layer__scale_uuid` 
    FOREIGN KEY (`scale_fk`) REFERENCES `t01_idesignres_scales` (`uuid`);
ALTER TABLE `t21_idesignres_layers`
    ADD KEY `fk_layer__scale_uuid` (`scale_fk`);
ALTER TABLE `t21_idesignres_layers`
    ADD CONSTRAINT `fk_layer__format_uuid` 
    FOREIGN KEY (`format_fk`) REFERENCES `t02_idesignres_layer_formats` (`uuid`);
ALTER TABLE `t21_idesignres_layers`
    ADD KEY `fk_layer__format_uuid` (`format_fk`);

ALTER TABLE `t22_idesignres_files`
    ADD CONSTRAINT `uq_file_name` UNIQUE (`name`);

ALTER TABLE `t23_idesignres_resources`
    ADD CONSTRAINT `uq_resource_name` UNIQUE (`name`);
    
ALTER TABLE `t31_idesignres_processes_layers`
    ADD CONSTRAINT `fk_rel__process_uuid` 
    FOREIGN KEY (`process_fk`) REFERENCES `t03_idesignres_processes` (`uuid`) ON DELETE CASCADE;
ALTER TABLE `t31_idesignres_processes_layers`
    ADD KEY `fk_rel__process_uuid` (`process_fk`);
ALTER TABLE `t31_idesignres_processes_layers`
    ADD CONSTRAINT `fk_rel__layer_uuid` 
    FOREIGN KEY (`layer_fk`) REFERENCES `t21_idesignres_layers` (`uuid`) ON DELETE CASCADE;
ALTER TABLE `t31_idesignres_processes_layers`
    ADD KEY `fk_rel__layer_uuid` (`layer_fk`);

ALTER TABLE `t32_idesignres_processes_files`
    ADD CONSTRAINT `fk_rel__process_file_uuid` 
    FOREIGN KEY (`process_fk`) REFERENCES `t03_idesignres_processes` (`uuid`) ON DELETE CASCADE;
ALTER TABLE `t32_idesignres_processes_files`
    ADD KEY `fk_rel__process_file_uuid` (`process_fk`);
ALTER TABLE `t32_idesignres_processes_files`
    ADD CONSTRAINT `fk_rel__file_uuid` 
    FOREIGN KEY (`file_fk`) REFERENCES `t22_idesignres_files` (`uuid`) ON DELETE CASCADE;
ALTER TABLE `t32_idesignres_processes_files`
    ADD KEY `fk_rel__file_uuid` (`file_fk`);

ALTER TABLE `t33_idesignres_processes_resources`
    ADD CONSTRAINT `fk_rel__process_resource_uuid` 
    FOREIGN KEY (`process_fk`) REFERENCES `t03_idesignres_processes` (`uuid`) ON DELETE CASCADE;
ALTER TABLE `t33_idesignres_processes_resources`
    ADD KEY `fk_rel__process_resource_uuid` (`process_fk`);
ALTER TABLE `t33_idesignres_processes_resources`
    ADD CONSTRAINT `fk_rel__resource_uuid` 
    FOREIGN KEY (`resource_fk`) REFERENCES `t23_idesignres_resources` (`uuid`) ON DELETE CASCADE;
ALTER TABLE `t33_idesignres_processes_resources`
    ADD KEY `fk_rel__resource_uuid` (`resource_fk`);

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
