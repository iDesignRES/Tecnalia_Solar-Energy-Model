package eu.idesignres.ui.backend.dck.controller;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.MessageSource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import eu.idesignres.ui.backend.dck.constants.Exceptions;
import eu.idesignres.ui.backend.dck.constants.Strings;
import eu.idesignres.ui.backend.dck.exception.controller.ControllerGenericException;
import eu.idesignres.ui.backend.dck.exception.controller.database.RetrieveDataException;
import eu.idesignres.ui.backend.dck.exception.controller.validation.ValidationException;
import eu.idesignres.ui.backend.dck.model.Connection;
import eu.idesignres.ui.backend.dck.persistence.model.Process;
import eu.idesignres.ui.backend.dck.persistence.model.view.ProcessView;
import eu.idesignres.ui.backend.dck.persistence.service.LayerService;
import eu.idesignres.ui.backend.dck.persistence.service.ProcessService;
import eu.idesignres.ui.backend.dck.security.dto.CredentialsDTO;
import eu.idesignres.ui.backend.dck.security.jwt.JwtTokenProvider;
import eu.idesignres.ui.backend.dck.util.CollectionUtil;
import eu.idesignres.ui.backend.dck.util.DateUtil;
import eu.idesignres.ui.backend.dck.util.SFTPUtil;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * Controller to manage the operations about processes.
 * @author Tecnalia
 * @version 1.0
 */
@RestController
@RequestMapping("/api/qgis-ui")
public class ProcessController {
	
	/** Logger. **/
	private final Logger log = LoggerFactory.getLogger(ProcessController.class);
	
	/** The sftpHost. */
	@Value("${sftp.host}")
	private String sftpHost;
	
	/** The sftpPort. */
	@Value("${sftp.port}")
	private String sftpPort;
	
	/** The sftpUsername. */
	@Value("${sftp.username}")
	private String sftpUsername;
	
	/** The sftpPassword. */
	@Value("${sftp.password}")
	private String sftpPassword;
	
	/** The sftpPassword. */
	@Value("${sftp.base.output.directory}")
	private String sftpBaseOutputDirectory;
	
	/** Service to access the data of the Process objects. */
	@Autowired
	ProcessService processService;
	
	/** Service to access the data of the Layer objects. */
	@Autowired
	LayerService layerService;
	
	/** Messages manager. */
	@Autowired
	MessageSource messageSource;
	
	
	// ********** API METHODS ********** //
	
	/**
	 * Retrieves all the processes.
	 * Call example: https://localhost/api/qgis-ui/processes
	 * @param locale The locale object.
	 * @param token The token.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/processes")
	@Secured({ "ROLE_ADMINISTRATOR", "ROLE_OPERATOR" })
    public ResponseEntity<Object> retrieveProcesses(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @RequestHeader(name = "Authorization") String token) {
		try {
			// Retrieve the list of processes
			log.info("ProcessController  ::  retrieveProcesses(Locale, String) :: Retrieving all the processes...");
			List<ProcessView> result = processService.retrieveProcesses();
			if (CollectionUtil.isNullOrEmpty(result)) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_PROCESS.getConstant(), messageSource.getMessage("rest.process.retrieve.400", null, locale));
			}
			log.info("ProcessController  ::  retrieveProcesses(Locale, String) :: The processes were retrieved successfully!");
			
			// Extract the credentials from the security token
			log.info("ProcessController  ::  retrieveProcesses(Locale, String) :: Extracting the credentials from the security token...");
			final CredentialsDTO credentials = new JwtTokenProvider().getFullCredentialsFromJWT(token.split(Strings.STR_WHITESPACE.getConstant())[1]);
			log.info("ProcessController  ::  retrieveProcesses(Locale, String) :: The credentials were extracted successfully!");
			
			// Retrieve the results
			log.info("ProcessController  ::  retrieveProcesses(Locale, String) :: Retrieving the results...");
			final List<String> fileList = SFTPUtil.retrieveListOfFilesInDirectory(
					new Connection(sftpHost, Integer.valueOf(sftpPort), sftpUsername, sftpPassword),
					sftpBaseOutputDirectory + credentials.getUsername());
			if (!CollectionUtil.isNullOrEmpty(fileList)) {
				for (ProcessView process : result) {
					for (String fileName : fileList) {
						if (fileName.startsWith(process.getUuid())) {
							process.setResults(process.getResults() + 1);
						}
					}
				}
			}
			log.info("ProcessController  ::  retrieveProcesses(Locale, String) :: The results were retrieved successfully!");
						
			// Return response
			return ResponseEntity.status(HttpStatus.OK).body(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("ProcessController  ::  retrieveProcesses(Locale, String) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("ProcessController  ::  retrieveProcesses(Locale, String) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Retrieves the process which UUID corresponds to the given parameter.
	 * Call example: http://localhost/api/qgis-ui/processes/uuid/{uuid}
	 * @param locale The locale.
	 * @param token The token.
	 * @param uuid The uuid.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/processes/uuid/{uuid}")
	@Secured({ "ROLE_ADMINISTRATOR", "ROLE_OPERATOR" })
    public ResponseEntity<Object> retrieveProcessByUUID(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @RequestHeader(name = "Authorization") String token, @PathVariable String uuid) {
		try {
			// Validate the parameter
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: Validating the UUID...");
			if (StringUtil.isNullOrEmpty(uuid)) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_PROCESS.getConstant(), messageSource.getMessage("rest.process.retrieve.uuid.400", null, locale));
			}
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: Validation completed!");
			
			// Retrieve the Process
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: Retrieving the Process [" + uuid.trim() + "]...");
			Process result = processService.retrieveProcessByUUID(uuid.trim());
			if (result == null) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_PROCESS.getConstant(), messageSource.getMessage("rest.process.retrieve.role.400", null, locale));
			}
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: The Process was retrieved successfully!");
			
			// Retrieve the associated layers
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: Retrieving the associated Layers...");
			result.setLayers(layerService.retrieveLayersByProcess(result.getUuid()));
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: The associated Layers were retrieved successfully!");
						
			// Extract the credentials from the security token
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: Extracting the credentials from the security token...");
			final CredentialsDTO credentials = new JwtTokenProvider().getFullCredentialsFromJWT(token.split(Strings.STR_WHITESPACE.getConstant())[1]);
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: The credentials were extracted successfully!");
			
			// Retrieve the results
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: Retrieving the results...");
			final List<String> fileList = SFTPUtil.retrieveListOfFilesInDirectory(
					new Connection(sftpHost, Integer.valueOf(sftpPort), sftpUsername, sftpPassword),
					sftpBaseOutputDirectory + credentials.getUsername());
			if (!CollectionUtil.isNullOrEmpty(fileList)) {
				List<String> resultList = new ArrayList<String>();
				for (String fileName : fileList) {
					if (fileName.startsWith(result.getUuid())) {
						resultList.add(fileName.substring(result.getUuid().length() + 1));
					}
				}
				result.setResults(resultList);
			}
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: The results were retrieved successfully!");
						
			// Format the dates
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: Formatting the dates...");
			result.setFormattedCreatedDate(DateUtil.buildFormattedDateFromTimestamp(result.getCreatedDate() * 1000L, locale));
			result.setFormattedLastModifiedDate(DateUtil.buildFormattedDateFromTimestamp(result.getLastModifiedDate() * 1000L, locale));
			if (result.getDeletedDate() != null) {
				result.setFormattedDeletedDate(DateUtil.buildFormattedDateFromTimestamp(result.getDeletedDate() * 1000L, locale));
			}
			log.info("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) :: The dates were formatted successfully!");
			
			// Return response
			return ResponseEntity.ok(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("ProcessController  ::  retrieveProcessByUUID(Locale, String, String) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Downloads a result file.
	 * Call example: http://localhost/api/qgis-ui/processes/download
	 * @param locale The locale.
	 * @param token The token.
	 * @param fileName The fileName;
	 * @return ResponseEntity<Object>
	 */
	@PostMapping("/processes/download")
	@Secured({ "ROLE_ADMINISTRATOR", "ROLE_OPERATOR" })
    public ResponseEntity<Object> downloadResult(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @RequestHeader(name = "Authorization") String token, @RequestBody String fileName) {
		try {
			// Validate the parameter
			log.info("ProcessController  ::  downloadResult(Locale, String, String) :: Validating the UUID...");
			if (StringUtil.isNullOrEmpty(fileName)) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_PROCESS.getConstant(), messageSource.getMessage("rest.process.retrieve.uuid.400", null, locale));
			}
			log.info("ProcessController  ::  downloadResult(Locale, String, String) :: Validation completed!");
			
			// Extract the credentials from the security token
			log.info("ProcessController  ::  downloadResult(Locale, String, String) :: Extracting the credentials from the security token...");
			final CredentialsDTO credentials = new JwtTokenProvider().getFullCredentialsFromJWT(token.split(Strings.STR_WHITESPACE.getConstant())[1]);
			log.info("ProcessController  ::  downloadResult(Locale, String, String) :: The credentials were extracted successfully!");
			
			// Retrieve the file as a byte array
			log.info("ProcessController  ::  downloadResult(Locale, String, String) :: Retrieving the results...");
			byte[] result = SFTPUtil.retrieveFile(
					new Connection(sftpHost, Integer.valueOf(sftpPort), sftpUsername, sftpPassword),
					sftpBaseOutputDirectory + credentials.getUsername() + Strings.STR_SLASH.getConstant() + fileName);
			log.info("ProcessController  ::  downloadResult(Locale, String, String) :: The results were retrieved successfully!");

			// Return response
			return ResponseEntity.ok(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("ProcessController  ::  downloadResult(Locale, String, String) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("ProcessController  ::  downloadResult(Locale, String, String) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
}