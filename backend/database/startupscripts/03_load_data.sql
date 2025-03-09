USE `dbidesignres`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

/*!40000 ALTER TABLE `t01_idesignres_scales` DISABLE KEYS */;
INSERT INTO `t01_idesignres_scales` (`uuid`, `name`, `description`, `created_date`, `last_modified_date`, `deleted_date`) VALUES
	('00000000-0000-0000-0000-000000000000', 'Europe', 'Scale: Europe', 1709888175, 1709888175, NULL),
	('11111111-1111-1111-1111-111111111111', 'America', 'Scale: America', 1709888175, 1709888175, NULL),
	('22222222-2222-2222-2222-222222222222', 'Asia', 'Scale: Asia', 1709888175, 1709888175, NULL);
/*!40000 ALTER TABLE `t01_idesignres_scales` ENABLE KEYS */;

/*!40000 ALTER TABLE `t02_idesignres_layer_formats` DISABLE KEYS */;
INSERT INTO `t02_idesignres_layer_formats` (`uuid`, `name`, `extension`, `created_date`, `last_modified_date`, `deleted_date`) VALUES
	('00000000-0000-0000-0000-000000000000', 'GeoPackage', 'gpkg', 1709888175, 1709888175, NULL),
	('11111111-1111-1111-1111-111111111111', 'Raster Layer', 'tif', 1709888175, 1709888175, NULL),
	('22222222-2222-2222-2222-222222222222', 'Shape', 'shp', 1709888175, 1709888175, NULL);
/*!40000 ALTER TABLE `t02_idesignres_layer_formats` ENABLE KEYS */;

/*!40000 ALTER TABLE `t03_idesignres_processes` DISABLE KEYS */;
INSERT INTO `t03_idesignres_processes` (`uuid`, `name`, `description`, `created_date`, `last_modified_date`, `deleted_date`) VALUES
	('00000000-0000-0000-0000-000000000000', 'PV Power Plants process', NULL, 1709888175, 1709888175, NULL),
	('11111111-1111-1111-1111-111111111111', 'Building energy simulation process', NULL, 1709888175, 1709888175, NULL);
/*!40000 ALTER TABLE `t03_idesignres_processes` ENABLE KEYS */;

/*!40000 ALTER TABLE `t11_idesignres_roles` DISABLE KEYS */;
INSERT INTO `t11_idesignres_roles` (`name`, `description`, `uuid`, `created_date`, `last_modified_date`, `deleted_date`) VALUES
	('ROLE_ADMINISTRATOR', 'Application Administrator', '00000000-0000-0000-0000-000000000000', 1709888175, 1709888175, NULL),
	('ROLE_OPERATOR', 'Application Operator', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL);
/*!40000 ALTER TABLE `t11_idesignres_roles` ENABLE KEYS */;

/*!40000 ALTER TABLE `t12_idesignres_users` DISABLE KEYS */;
-- Default password ('admin'): PWDadmin#2024
-- Default password ('operator'): PWDoperator#2024
INSERT INTO `t12_idesignres_users` (`username`, `password`, `email`, `uuid`, `created_date`, `last_modified_date`, `deleted_date`) VALUES
	('admin', '$2a$10$f4DkTQrcilEreod3q0W61OMBogaOj5MY2ZWOyZBHhpJ3PghFgIFvy', 'alberto.molinuevo@tecnalia.com', '00000000-0000-0000-0000-000000000000', 1709888175, 1709888175, NULL),
	('operator', '$2a$10$51uaMCSq8qrqYwbvolyb3e9/Lc9ZuY5xWLFcN1lj19CZauIM77GEi', 'alberto.molinuevo@tecnalia.com', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL);
/*!40000 ALTER TABLE `t12_idesignres_users` ENABLE KEYS */;

/*!40000 ALTER TABLE `t13_idesignres_actors` DISABLE KEYS */;
INSERT INTO `t13_idesignres_actors` (`username`, `role`) VALUES
	('admin', 'ROLE_ADMINISTRATOR'),
	('operator', 'ROLE_OPERATOR');
/*!40000 ALTER TABLE `t13_idesignres_actors` ENABLE KEYS */;

/*!40000 ALTER TABLE `t21_idesignres_layers` DISABLE KEYS */;
INSERT INTO `t21_idesignres_layers` (`uuid`, `name`, `full_path`, `scale_fk`, `format_fk`, `created_date`, `last_modified_date`, `deleted_date`) VALUES
	('0304ac37-9315-4b31-b321-1644978b25e0', 'NUTS_RG_01M_2024_3035', '/layers/NUTS_RG_01M_2024_3035.gpkg', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000',  1709888175, 1709888175, NULL),
	('0a63f21a-a683-4b33-bd7e-84d8905689ed', 'eudem_slop_3035_europe', '/layers/eudem_slop_3035_europe.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('a0fec53d-e587-46eb-93a5-49b3494ba01e', 'GHI_Annual_Europe', '/layers/GHI_Annual_Europe.tif','00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('c6b50a42-db65-4266-ae9a-6be1d05ec102', 'LUISA_basemap_020321_50m', '/layers/LUISA_basemap_020321_50m.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('fd3f1fef-fc6b-4716-bd2d-5d72a971bd2a', 'NonProtectedAreas250ConvertedCompressed', '/layers/NonProtectedAreas250ConvertedCompressed.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('81e91f45-6a56-46b3-8137-fe1d270b88f5', 'GHS_BUILT_C_FUN_E2018_Europe_R2023A_54009_10', '/layers/GHS_BUILT_C_FUN_E2018_Europe_R2023A_54009_10.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('de07e7fa-1467-42ed-a5c5-028bc57ed4cb', 'GHS_BUILT_H_ANBH_E2018_Europe_R2023A_54009_100', '/layers/GHS_BUILT_H_ANBH_E2018_Europe_R2023A_54009_100.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('ee4872d2-088c-4c9e-9f66-6f2144e999af', 'GHS_BUILT_S_E1975_GLOBE_R2023A_54009_100_EU_C', '/layers/GHS_BUILT_S_E1975_GLOBE_R2023A_54009_100_EU_C.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('dbde4513-448a-4535-9244-bf43ca6265de', 'GHS_BUILT_S_E1990_GLOBE_R2023A_54009_100_EU_C', '/layers/GHS_BUILT_S_E1990_GLOBE_R2023A_54009_100_EU_C.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('ac57259c-1ef0-48fc-a295-c2e74bc3caf4', 'GHS_BUILT_S_E2000_GLOBE_R2023A_54009_100_EU_C', '/layers/GHS_BUILT_S_E2000_GLOBE_R2023A_54009_100_EU_C.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('8b851c93-ba51-4744-a4cf-38d257e8f7cd', 'GHS_BUILT_S_E2010_GLOBE_R2023A_54009_100_EU_C', '/layers/GHS_BUILT_S_E2010_GLOBE_R2023A_54009_100_EU_C.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('e84e8c53-7669-4175-a8c9-fce405910ac3', 'GHS_BUILT_S_E2020_GLOBE_R2023A_54009_100_EU_C', '/layers/GHS_BUILT_S_E2020_GLOBE_R2023A_54009_100_EU_C.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL),
	('2114111c-7dcd-4419-9fcd-b8491500a76b', 'ES21_REC', '/layers/ES21_REC.gpkg', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', 1709888175, 1709888175, NULL),
	('0c133c8f-cae9-4a46-a86a-b1afc24f8c35', 'DatosSE1', '/layers/DatosSE1.gpkg', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', 1709888175, 1709888175, NULL),
	('fe524c33-15c0-40f8-b42b-0d4b73641464', 'Total_heating_demand', '/layers/Total_heating_demand.tif', '00000000-0000-0000-0000-000000000000', '11111111-1111-1111-1111-111111111111', 1709888175, 1709888175, NULL);
/*!40000 ALTER TABLE `t21_idesignres_layers` ENABLE KEYS */;

/*!40000 ALTER TABLE `t22_idesignres_files` DISABLE KEYS */;
INSERT INTO `t22_idesignres_files` (`uuid`, `name`, `full_path`, `created_date`, `last_modified_date`, `deleted_date`) VALUES
	('2565e3ed-20b8-45cf-bf03-f4c703f3a287', 'NutsRegionsBuildingLayer_DownloadLinksNUTS2_3', '/files/NutsRegionsBuildingLayer_DownloadLinksNUTS2_3.xlsx', 1709888175, 1709888175, NULL),
	('569ff7ff-5551-4183-b9f9-fe183995370b', 'UsosMapeados', '/files/UsosMapeados.csv', 1709888175, 1709888175, NULL),
	('a8650b54-2e28-4328-9326-77c0e22b26e3', 'ShareYearsBSO', '/files/ShareYearsBSO.xlsx', 1709888175, 1709888175, NULL);
/*!40000 ALTER TABLE `t22_idesignres_files` ENABLE KEYS */;

/*!40000 ALTER TABLE `t23_idesignres_resources` DISABLE KEYS */;
INSERT INTO `t23_idesignres_resources` (`uuid`, `name`, `web_path`, `sftp_path`, `created_date`, `last_modified_date`, `deleted_date`) VALUES
	('7dbc7f3f-1cdf-4b66-a684-e1eea5dfbd5c', 'andalucia-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/andalucia-latest-free.shp.zip', '/resources/andalucia-latest-free.shp.zip', 1709888175, 1709888175, NULL),
	('e19a8509-4bb4-4b53-81d4-b2f03e3e66a6', 'aragon-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/aragon-latest-free.shp.zip', '/resources/aragon-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('2f1b1fc4-0443-480d-b469-dbc5fecf7dc7', 'asturias-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/asturias-latest-free.shp.zip', '/resources/asturias-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('0b66ab54-f434-4225-955f-5e690b953e9f', 'cantabria-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/cantabria-latest-free.shp.zip', '/resources/cantabria-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('5ad7a2e4-1a26-462d-b53a-b494921df9e1', 'castilla-la-mancha-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/castilla-la-mancha-latest-free.shp.zip', '/resources/castilla-la-mancha-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('ccc60a02-0201-47e7-b5ff-1fffcc275e9d', 'castilla-y-leon-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/castilla-y-leon-latest-free.shp.zip', '/resources/castilla-y-leon-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('f3372440-fbec-4309-bf63-0ae3de43bd2c', 'cataluna-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/cataluna-latest-free.shp.zip', '/resources/cataluna-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('5dff6c5a-a4c7-49af-86ba-faeff9188010', 'ceuta-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/ceuta-latest-free.shp.zip', '/resources/ceuta-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('f5f8406c-d271-4a76-a867-4dadf567d68f', 'extremadura-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/extremadura-latest-free.shp.zip', '/resources/extremadura-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('d86b9fdc-5cc0-4772-aa65-17babc97b2c1', 'galicia-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/galicia-latest-free.shp.zip', '/resources/galicia-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('d1040b78-7c98-4c8b-ad04-8d620826e485', 'islas-baleares-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/islas-baleares-latest-free.shp.zip', '/resources/islas-baleares-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('f20cd616-00ec-449a-9900-fa857222cc42', 'la-rioja-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/la-rioja-latest-free.shp.zip', '/resources/la-rioja-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('01066a67-0797-4d0b-920a-a7d94ad4ab8d', 'madrid-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/madrid-latest-free.shp.zip', '/resources/madrid-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('be6dbbb1-0c50-4877-9276-a4a02b001bad', 'melilla-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/melilla-latest-free.shp.zip', '/resources/melilla-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('1641cf0d-70fc-4f91-8b20-0a79d20ae736', 'murcia-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/murcia-latest-free.shp.zip', '/resources/murcia-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('47b6b15d-6075-4315-a7fc-2e1ad1656e38', 'navarra-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/navarra-latest-free.shp.zip', '/resources/navarra-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('21bfbb21-bced-4101-bc6a-05c11f37973b', 'pais-vasco-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/pais-vasco-latest-free.shp.zip', '/resources/pais-vasco-latest-free.shp.zip', 1709888175, 1709888175, NULL),
        ('b6f7b308-b74d-4c94-b6f7-94999fd723d8', 'valencia-latest-free.shp.zip', 'https://download.geofabrik.de/europe/spain/valencia-latest-free.shp.zip', '/resources/valencia-latest-free.shp.zip', 1709888175, 1709888175, NULL);
/*!40000 ALTER TABLE `t23_idesignres_resources` ENABLE KEYS */;

/*!40000 ALTER TABLE `t31_idesignres_processes_layers` DISABLE KEYS */;
INSERT INTO `t31_idesignres_processes_layers` (`process_fk`, `layer_fk`) VALUES
	('00000000-0000-0000-0000-000000000000', '0304ac37-9315-4b31-b321-1644978b25e0'),
	('00000000-0000-0000-0000-000000000000', '0a63f21a-a683-4b33-bd7e-84d8905689ed'),
	('00000000-0000-0000-0000-000000000000', 'a0fec53d-e587-46eb-93a5-49b3494ba01e'),
	('00000000-0000-0000-0000-000000000000', 'c6b50a42-db65-4266-ae9a-6be1d05ec102'),
	('00000000-0000-0000-0000-000000000000', 'fd3f1fef-fc6b-4716-bd2d-5d72a971bd2a'),
	('11111111-1111-1111-1111-111111111111', '0304ac37-9315-4b31-b321-1644978b25e0'),
	('11111111-1111-1111-1111-111111111111', '81e91f45-6a56-46b3-8137-fe1d270b88f5'),
	('11111111-1111-1111-1111-111111111111', 'de07e7fa-1467-42ed-a5c5-028bc57ed4cb'),
	('11111111-1111-1111-1111-111111111111', 'ee4872d2-088c-4c9e-9f66-6f2144e999af'),
	('11111111-1111-1111-1111-111111111111', 'dbde4513-448a-4535-9244-bf43ca6265de'),
	('11111111-1111-1111-1111-111111111111', 'ac57259c-1ef0-48fc-a295-c2e74bc3caf4'),
	('11111111-1111-1111-1111-111111111111', '8b851c93-ba51-4744-a4cf-38d257e8f7cd'),
	('11111111-1111-1111-1111-111111111111', 'e84e8c53-7669-4175-a8c9-fce405910ac3'),
	('11111111-1111-1111-1111-111111111111', '2114111c-7dcd-4419-9fcd-b8491500a76b');
/*!40000 ALTER TABLE `t31_idesignres_processes_layers` ENABLE KEYS */;

/*!40000 ALTER TABLE `t32_idesignres_processes_files` DISABLE KEYS */;
INSERT INTO `t32_idesignres_processes_files` (`process_fk`, `file_fk`) VALUES
	('11111111-1111-1111-1111-111111111111', '2565e3ed-20b8-45cf-bf03-f4c703f3a287'),
	('11111111-1111-1111-1111-111111111111', 'a8650b54-2e28-4328-9326-77c0e22b26e3'),
	('11111111-1111-1111-1111-111111111111', '569ff7ff-5551-4183-b9f9-fe183995370b');
/*!40000 ALTER TABLE `t32_idesignres_processes_files` ENABLE KEYS */;

/*!40000 ALTER TABLE `t33_idesignres_processes_resources` DISABLE KEYS */;
INSERT INTO `t33_idesignres_processes_resources` (`process_fk`, `resource_fk`) VALUES
	('11111111-1111-1111-1111-111111111111', '7dbc7f3f-1cdf-4b66-a684-e1eea5dfbd5c'),
	('11111111-1111-1111-1111-111111111111', 'e19a8509-4bb4-4b53-81d4-b2f03e3e66a6'),
	('11111111-1111-1111-1111-111111111111', '2f1b1fc4-0443-480d-b469-dbc5fecf7dc7'),
	('11111111-1111-1111-1111-111111111111', '0b66ab54-f434-4225-955f-5e690b953e9f'),
	('11111111-1111-1111-1111-111111111111', '5ad7a2e4-1a26-462d-b53a-b494921df9e1'),
	('11111111-1111-1111-1111-111111111111', 'ccc60a02-0201-47e7-b5ff-1fffcc275e9d'),
	('11111111-1111-1111-1111-111111111111', 'f3372440-fbec-4309-bf63-0ae3de43bd2c'),
	('11111111-1111-1111-1111-111111111111', '5dff6c5a-a4c7-49af-86ba-faeff9188010'),
	('11111111-1111-1111-1111-111111111111', 'f5f8406c-d271-4a76-a867-4dadf567d68f'),
	('11111111-1111-1111-1111-111111111111', 'd86b9fdc-5cc0-4772-aa65-17babc97b2c1'),
	('11111111-1111-1111-1111-111111111111', 'd1040b78-7c98-4c8b-ad04-8d620826e485'),
	('11111111-1111-1111-1111-111111111111', 'f20cd616-00ec-449a-9900-fa857222cc42'),
	('11111111-1111-1111-1111-111111111111', '01066a67-0797-4d0b-920a-a7d94ad4ab8d'),
	('11111111-1111-1111-1111-111111111111', 'be6dbbb1-0c50-4877-9276-a4a02b001bad'),
	('11111111-1111-1111-1111-111111111111', '1641cf0d-70fc-4f91-8b20-0a79d20ae736'),
	('11111111-1111-1111-1111-111111111111', '47b6b15d-6075-4315-a7fc-2e1ad1656e38'),
	('11111111-1111-1111-1111-111111111111', '21bfbb21-bced-4101-bc6a-05c11f37973b'),
	('11111111-1111-1111-1111-111111111111', 'b6f7b308-b74d-4c94-b6f7-94999fd723d8');
/*!40000 ALTER TABLE `t33_idesignres_processes_resources` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
