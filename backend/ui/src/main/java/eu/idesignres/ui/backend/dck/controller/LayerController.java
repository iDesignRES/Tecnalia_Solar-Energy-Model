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
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import eu.idesignres.ui.backend.dck.constants.Exceptions;
import eu.idesignres.ui.backend.dck.constants.Strings;
import eu.idesignres.ui.backend.dck.exception.controller.ControllerGenericException;
import eu.idesignres.ui.backend.dck.exception.controller.database.InsertDataException;
import eu.idesignres.ui.backend.dck.exception.controller.database.RetrieveDataException;
import eu.idesignres.ui.backend.dck.exception.controller.validation.ValidationException;
import eu.idesignres.ui.backend.dck.model.Connection;
import eu.idesignres.ui.backend.dck.persistence.model.Layer;
import eu.idesignres.ui.backend.dck.persistence.model.LayerFormat;
import eu.idesignres.ui.backend.dck.persistence.model.view.LayerComplexView;
import eu.idesignres.ui.backend.dck.persistence.model.view.LayerSimpleView;
import eu.idesignres.ui.backend.dck.persistence.service.LayerFormatService;
import eu.idesignres.ui.backend.dck.persistence.service.LayerService;
import eu.idesignres.ui.backend.dck.persistence.service.ScaleService;
import eu.idesignres.ui.backend.dck.util.CollectionUtil;
import eu.idesignres.ui.backend.dck.util.DateUtil;
import eu.idesignres.ui.backend.dck.util.SFTPUtil;
import eu.idesignres.ui.backend.dck.util.StringUtil;
import eu.idesignres.ui.backend.dck.validation.LayerValidator;


/**
 * Controller to manage the operations about layers.
 * @author Tecnalia
 * @version 1.0
 */
@RestController
@RequestMapping("/api/qgis-ui")
public class LayerController {
	
	/** Logger. **/
	private final Logger log = LoggerFactory.getLogger(LayerController.class);
	
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
	
	/** The sftpBaseLayersDirectory. */
	@Value("${sftp.base.layers.directory}")
	private String sftpBaseLayersDirectory;
	
	/** Service to access the data of the Layer objects. */
	@Autowired
	LayerService layerService;
	
	/** Service to access the data of the Scale objects. */
	@Autowired
	ScaleService scaleService;
	
	/** Service to access the data of the LayerFormat objects. */
	@Autowired
	LayerFormatService layerFormatService;
	
	/** Messages manager. */
	@Autowired
	MessageSource messageSource;
	
	
	// ********** API METHODS ********** //
	
	/**
	 * Retrieves all the layers.
	 * Call example: https://localhost/api/qgis-ui/layers
	 * @param locale The locale object.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/layers")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveLayers(@RequestHeader(name = "Accept-Language", required = false) Locale locale) {
		try {
			// Retrieve the list of layers
			log.info("LayerController  ::  retrieveLayers(Locale) :: Retrieving all the layers...");
			final List<LayerSimpleView> result = layerService.retrieveSimpleLayers();
			if (CollectionUtil.isNullOrEmpty(result)) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_LAYER.getConstant(), messageSource.getMessage("rest.process.retrieve.400", null, locale));
			}
			log.info("LayerController  ::  retrieveLayers(Locale) :: The layers were retrieved successfully!");
			
			// Return response
			return ResponseEntity.status(HttpStatus.OK).body(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("LayerController  ::  retrieveLayers(Locale) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("LayerController  ::  retrieveLayers(Locale) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Retrieves the layer which UUID corresponds to the given parameter.
	 * Call example: http://localhost/api/qgis-ui/layers/uuid/{uuid}
	 * @param locale The locale.
	 * @param uuid The uuid.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/layers/uuid/{uuid}")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveLayerByUUID(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @PathVariable String uuid) {
		try {
			// Validate the parameter
			log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: Validating the UUID...");
			if (StringUtil.isNullOrEmpty(uuid)) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_LAYER.getConstant(), messageSource.getMessage("rest.process.retrieve.uuid.400", null, locale));
			}
			log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: Validation completed!");
			
			// Retrieve the Layer
			log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: Retrieving the Layer [" + uuid.trim() + "]...");
			Layer result = layerService.retrieveLayerByUUID(uuid.trim());
			log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: The Layer was retrieved successfully!");
			
			if (result != null) {
				// Retrieve the associated processes
				log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: Retrieving the associated Processes...");
				final List<LayerComplexView> layerComplexList = layerService.retrieveComplexLayers();
				if (!CollectionUtil.isNullOrEmpty(layerComplexList)) {
					List<eu.idesignres.ui.backend.dck.persistence.model.Process> processesList =
							new ArrayList<eu.idesignres.ui.backend.dck.persistence.model.Process>();
					for (LayerComplexView layerComplex : layerComplexList) {
						if (result.getUuid().equals(layerComplex.getUuid()) && layerComplex.getProcessUuid() != null) {
							processesList.add(new eu.idesignres.ui.backend.dck.persistence.model.Process(
									layerComplex.getProcessUuid(), layerComplex.getProcessName()));
							break;
						}
					}
					result.setProcesses(processesList);
				}
				log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: The associated Processes were retrieved successfully!");
						
				// Format the dates
				log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: Formatting the dates...");
				result.setFormattedCreatedDate(DateUtil.buildFormattedDateFromTimestamp(result.getCreatedDate() * 1000L, locale));
				result.setFormattedLastModifiedDate(DateUtil.buildFormattedDateFromTimestamp(result.getLastModifiedDate() * 1000L, locale));
				if (result.getDeletedDate() != null) {
					result.setFormattedDeletedDate(DateUtil.buildFormattedDateFromTimestamp(result.getDeletedDate() * 1000L, locale));
				}
				log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: The dates were formatted successfully!");
			} else {
				// Build a new layer
				result = new Layer();
				
				// Assign the list of scales
				log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: Retrieving and assigning the list of scales...");
				result.setScales(scaleService.retrieveScales());
				log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: The list of scales was retrieved and assigned successfully!");
				
				// Assign the list of layer formats
				log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: Retrieving and assigning the list of layer formats...");
				result.setFormats(layerFormatService.retrieveLayerFormats());
				log.info("LayerController  ::  retrieveLayerByUUID(Locale, String) :: The list of layer formats was retrieved and assigned successfully!");
			}
			
			// Return response
			return ResponseEntity.ok(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("ProcessController  ::  retrieveLayerByUUID(Locale, String) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("LayerController  ::  retrieveLayerByUUID(Locale, String) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Adds a new Layer to the database.
	 * Call example: http://localhost/api/qgis-ui/layers/add
	 * @param locale The locale object.
	 * @param file The file object.
	 * @param layer The layer object.
	 * @return ResponseEntity<Object>
	 */
	@PostMapping("/layers/add")
	@Secured({ "ROLE_ADMINISTRATOR" })
	@Transactional
    public ResponseEntity<Object> addLayer(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @RequestPart("file") MultipartFile file, @RequestPart("layer") Layer layer) {
		try {
			// Validate the Layer object
			log.info("LayerController  ::  addLayer(Locale, Layer) :: Validating the Layer object...");
			final String validation = LayerValidator.getInstance(locale).validate(layer, false, false);
			if (validation != null) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_LAYER.getConstant(), validation);
			}
			layer.trimObject();
			if (layerService.retrieveLayerByName(layer.getName()) != null) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_LAYER.getConstant(), messageSource.getMessage("rest.layer.add.name.400", null, locale));
			}
			log.info("LayerController  ::  addLayer(Locale, Layer) :: Validation completed!");
			
			// Establish the dates
			log.info("LayerController  ::  addLayer(Locale, Layer) :: Establishing the dates...");
			final Long now = DateUtil.getCurrentShortTimestamp();
			layer.setCreatedDate(now);
			layer.setLastModifiedDate(now);
			log.info("LayerController  ::  addLayer(Locale, Layer) :: Dates established!");
			
			// Retrieve the full layer format
			final LayerFormat layerFormat = layerFormatService.retrieveLayerFormatByUUID(layer.getLayerFormat());
			if (layerFormat == null) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_LAYER.getConstant(), messageSource.getMessage("rest.layer.add.format.400", null, locale));
			}
			
			// Add the Layer object
			log.info("LayerController  ::  addLayer(Locale, Layer) :: Adding the Layer object...");
			layer.setFullPath(sftpBaseLayersDirectory + layer.getName() + Strings.STR_DOT.getConstant() + layerFormat.getExtension());
			if (layerService.addLayer(layer) == null) {
				throw new InsertDataException(Exceptions.EXC_SUBCATEGORY_LAYER.getConstant(), messageSource.getMessage("rest.layer.add.400", null, locale));
			}
			log.info("LayerController  ::  addLayer(Locale, Layer) :: The Layer object was added succesfully!");
			
			// Upload the file to the SFTP Server
			log.info("LayerController  ::  addLayer(Locale, Layer) :: Uploading the file to the SFTP Server...");
			SFTPUtil.uploadFileToRemoteDirectory(new Connection(sftpHost, Integer.valueOf(sftpPort), sftpUsername, sftpPassword),
					layer.getFullPath(), file.getBytes());
            log.info("LayerController  ::  addLayer(Locale, Layer) :: The file was uploaded successfully!");
			
			// Return response
			return ResponseEntity.ok(messageSource.getMessage("rest.layer.add.200", null, locale));
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("LayerController  ::  addLayer(Locale, Layer) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		}  catch (Exception e) {
			// Error 500: Internal server error
			log.error("LayerController  ::  addLayer(Locale, Layer) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Deletes a Layer.
	 * Call example: https://localhost/api/qgis-ui/layers/delete
	 * @param locale The locale object.
	 * @param layer The layer.
	 * @return ResponseEntity<String>
	 */
	@PostMapping("/layers/delete")
	@Secured({ "ROLE_ADMINISTRATOR" })
	@Transactional
    public ResponseEntity<String> deleteLayer(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @RequestBody Layer layer) {
		try {
			// Validate the Layer object
			log.info("LayerController  ::  deleteLayer(Locale, Layer) :: Validating the Layer object...");
			final String validation = LayerValidator.getInstance(locale).validate(layer, true, true);
			if (validation != null) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_USER.getConstant(), validation);
			}
			layer.trimObject();
			log.info("LayerController  ::  deleteLayer(Locale, Layer) :: Validation completed!");
			
			// Remove the layer from the SFTP Server
			log.info("LayerController  ::  deleteLayer(Locale, Layer) :: Removing the Layer from the SFTP Server...");
			SFTPUtil.removeRemoteFile(new Connection(sftpHost, Integer.valueOf(sftpPort), sftpUsername, sftpPassword), layer.getFullPath());
			log.info("LayerController  ::  deleteLayer(Locale, Layer) :: The Layer was susccefully removed!");
			
			// Delete the Layer object
			log.info("LayerController  ::  deleteLayer(Locale, Layer) :: Deleting the Layer object...");
			layerService.deleteLayerByUUID(layer.getUuid());
			log.info("LayerController  ::  deleteLayer(Locale, Layer) :: The Layer object was deleted succesfully!");
			
			// Return response
			return ResponseEntity.ok(messageSource.getMessage("rest.layer.delete.200", null, locale));
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("LayerController  ::  deleteLayer(Locale, Layer) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("LayerController  ::  deleteLayer(Locale, Layer) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
}