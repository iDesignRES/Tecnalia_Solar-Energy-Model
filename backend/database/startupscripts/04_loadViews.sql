--
-- Database: `dbidesignres`    ’
--
USE `dbidesignres`;
SET FOREIGN_KEY_CHECKS=0;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- -------------------------------------
-- View: `v01_idesignres_scales`
-- -------------------------------------
CREATE VIEW v01_idesignres_scales AS
SELECT
	scl.uuid AS uuid,
	scl.name AS name,
	scl.description AS description,
	scl.created_date AS created_date,
	scl.last_modified_date AS last_modified_date,
	scl.deleted_date AS deleted_date,
	COUNT(lay.uuid) AS layers
FROM
	t01_idesignres_scales scl
LEFT OUTER JOIN
	t21_idesignres_layers lay ON
		scl.uuid = lay.scale_fk
GROUP BY
	scl.uuid
ORDER BY
	scl.name;

-- -------------------------------------
-- View: `v02_idesignres_layer_formats`
-- -------------------------------------
CREATE VIEW v02_idesignres_layer_formats AS
SELECT
	laf.uuid AS uuid,
	laf.name AS name,
	laf.extension AS extension,
	laf.created_date AS created_date,
	laf.last_modified_date AS last_modified_date,
	laf.deleted_date AS deleted_date,
	COUNT(lay.uuid) AS layers
FROM
	t02_idesignres_layer_formats laf
LEFT OUTER JOIN
	t21_idesignres_layers lay ON
		laf.uuid = lay.format_fk
GROUP BY
	laf.uuid
ORDER BY
	laf.name;

-- -------------------------------------
-- View: `v03_idesignres_processes`
-- -------------------------------------
CREATE VIEW v03_idesignres_processes AS
SELECT
	prc.uuid AS uuid,
	prc.name AS name,
	prc.description AS description,
	prc.created_date AS created_date,
	prc.last_modified_date AS last_modified_date,
	prc.deleted_date AS deleted_date,
	COUNT(prl.layer_fk) AS layers
FROM
	t03_idesignres_processes prc
LEFT OUTER JOIN
	t31_idesignres_processes_layers prl ON
		prc.uuid = prl.process_fk
GROUP BY
	prc.uuid
ORDER BY
	prc.uuid;
	
-- -------------------------------------
-- View: `v11_idesignres_roles`
-- -------------------------------------
CREATE VIEW v11_idesignres_roles AS
SELECT
	rol.uuid AS uuid,
	rol.name AS name,
	rol.description AS description,
	rol.created_date AS created_date,
	rol.last_modified_date AS last_modified_date,
	rol.deleted_date AS deleted_date,
	(
	SELECT
		COUNT(role)
	FROM
		t13_idesignres_actors
	WHERE
		 role = rol.name
	) AS users
FROM
	t11_idesignres_roles rol
GROUP BY
	rol.uuid
ORDER BY
	rol.uuid;

-- -------------------------------------
-- View: `v12_idesignres_users`
-- -------------------------------------
CREATE VIEW v12_idesignres_users AS
SELECT
	usr.uuid AS uuid,
	usr.username AS username,
	usr.password AS password,
	usr.email AS email,
	usr.created_date AS created_date,
	usr.last_modified_date AS last_modified_date,
	usr.deleted_date AS deleted_date,
	act.role AS role
FROM
	t12_idesignres_users usr
JOIN
	t13_idesignres_actors act ON
		usr.username = act.username
GROUP BY
	usr.uuid
ORDER BY
	usr.username;
	
-- -------------------------------------
-- View: `v21A_idesignres_layers_simple`
-- -------------------------------------
CREATE VIEW v21A_idesignres_layers_simple AS
SELECT
	lay.uuid AS uuid,
	lay.name AS name,
	lay.full_path AS full_path,
	lay.created_date AS created_date,
	lay.last_modified_date AS last_modified_date,
	lay.deleted_date AS deleted_date,
	scl.name AS scale_name,
	frm.name AS layer_format_name,
	(
	SELECT
		COUNT(process_fk)
	FROM
		t31_idesignres_processes_layers
	WHERE
		 layer_fk = lay.uuid
	) AS processes
FROM
	t21_idesignres_layers lay
JOIN
	t01_idesignres_scales scl ON
		lay.scale_fk = scl.uuid
JOIN
	t02_idesignres_layer_formats frm ON
		lay.format_fk = frm.uuid
ORDER BY
	lay.name;

-- -------------------------------------
-- View: `v21B_idesignres_layers_complex`
-- -------------------------------------
CREATE VIEW v21B_idesignres_layers_complex AS
SELECT
	lay.uuid AS uuid,
	lay.name AS name,
	lay.full_path AS full_path,
	lay.created_date AS created_date,
	lay.last_modified_date AS last_modified_date,
	lay.deleted_date AS deleted_date,
	scl.uuid AS scale_uuid,
	scl.name AS scale_name,
	frm.uuid AS layer_format_uuid,
	frm.name AS layer_format_name,
	prc.uuid AS process_uuid,
	prc.name AS process_name,
	prc.description AS process_description
FROM
	t21_idesignres_layers lay
JOIN
	t01_idesignres_scales scl ON
		lay.scale_fk = scl.uuid
JOIN
	t02_idesignres_layer_formats frm ON
		lay.format_fk = frm.uuid
LEFT OUTER JOIN
	t31_idesignres_processes_layers prl ON
		lay.uuid = prl.layer_fk
LEFT OUTER JOIN
	t03_idesignres_processes prc ON
		prl.process_fk = prc.uuid
ORDER BY
	lay.name;

-- -------------------------------------
-- View: `v22_idesignres_files`
-- -------------------------------------
CREATE VIEW v22_idesignres_files AS
SELECT
	fil.uuid AS uuid,
	fil.name AS name,
	fil.full_path AS full_path,
	fil.created_date AS created_date,
	fil.last_modified_date AS last_modified_date,
	fil.deleted_date AS deleted_date,
	(
	SELECT
		COUNT(process_fk)
	FROM
		t32_idesignres_processes_files
	WHERE
		 file_fk = fil.uuid
	) AS processes
FROM
	t22_idesignres_files fil
ORDER BY
	fil.name;

-- -------------------------------------
-- View: `v23_idesignres_resources`
-- -------------------------------------
CREATE VIEW v23_idesignres_resources AS
SELECT
	rsc.uuid AS uuid,
	rsc.name AS name,
	rsc.web_path AS web_path,
	rsc.sftp_path AS sftp_path,
	rsc.created_date AS created_date,
	rsc.last_modified_date AS last_modified_date,
	rsc.deleted_date AS deleted_date,
	(
	SELECT
		COUNT(process_fk)
	FROM
		t33_idesignres_processes_resources
	WHERE
		 resource_fk = rsc.uuid
	) AS processes
FROM
	t23_idesignres_resources rsc
ORDER BY
	rsc.name;

-- -------------------------------------
-- View: `v31_idesignres_processes_layers`
-- -------------------------------------
CREATE VIEW v31_idesignres_processes_layers AS
SELECT
	prc.uuid AS process_uuid,
	prc.name AS process_name,
	prc.description AS process_description,
	lay.uuid AS layer_uuid,
	lay.name AS layer_name,
	lay.full_path AS layer_full_path,
	lay.scale_fk AS layer_scale_uuid,
	scl.name AS layer_scale_name,
	lay.format_fk AS layer_format_uuid,
	frm.name AS layer_format_name,
	frm.extension AS layer_format_extension
FROM
	t03_idesignres_processes prc
JOIN
	t31_idesignres_processes_layers prl ON
		prc.uuid = prl.process_fk
JOIN
	t21_idesignres_layers lay ON
		prl.layer_fk = lay.uuid
JOIN
	t01_idesignres_scales scl ON
		lay.scale_fk = scl.uuid
JOIN
	t02_idesignres_layer_formats frm ON
		lay.format_fk = frm.uuid
ORDER BY
	prc.name, lay.name;

-- -------------------------------------
-- View: `v32_idesignres_processes_files`
-- -------------------------------------
CREATE VIEW v32_idesignres_processes_files AS
SELECT
	prc.uuid AS process_uuid,
	prc.name AS process_name,
	prc.description AS process_description,
	fil.uuid AS file_uuid,
	fil.name AS file_name,
	fil.full_path AS file_full_path
FROM
	t03_idesignres_processes prc
JOIN
	t32_idesignres_processes_files prl ON
		prc.uuid = prl.process_fk
JOIN
	t22_idesignres_files fil ON
		prl.file_fk = fil.uuid
ORDER BY
	prc.name, fil.name;

-- -------------------------------------
-- View: `v33_idesignres_processes_resources`
-- -------------------------------------
CREATE VIEW v33_idesignres_processes_resources AS
SELECT
	prc.uuid AS process_uuid,
	prc.name AS process_name,
	prc.description AS process_description,
	rsc.uuid AS resource_uuid,
	rsc.name AS resource_name,
	rsc.web_path AS resource_web_path,
	rsc.sftp_path AS resource_sftp_path
FROM
	t03_idesignres_processes prc
JOIN
	t33_idesignres_processes_resources prl ON
		prc.uuid = prl.process_fk
JOIN
	t23_idesignres_resources rsc ON
		prl.resource_fk = rsc.uuid
ORDER BY
	prc.name, rsc.name;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
