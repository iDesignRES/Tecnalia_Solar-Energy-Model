package eu.idesignres.ui.backend.dck.controller;

import java.util.List;
import java.util.Locale;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.MessageSource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import eu.idesignres.ui.backend.dck.constants.Exceptions;
import eu.idesignres.ui.backend.dck.exception.controller.ControllerGenericException;
import eu.idesignres.ui.backend.dck.exception.controller.database.RetrieveDataException;
import eu.idesignres.ui.backend.dck.exception.controller.validation.ValidationException;
import eu.idesignres.ui.backend.dck.persistence.model.LayerFormat;
import eu.idesignres.ui.backend.dck.persistence.model.view.LayerFormatView;
import eu.idesignres.ui.backend.dck.persistence.service.LayerFormatService;
import eu.idesignres.ui.backend.dck.persistence.service.LayerService;
import eu.idesignres.ui.backend.dck.util.CollectionUtil;
import eu.idesignres.ui.backend.dck.util.DateUtil;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * Controller to manage the operations about layer formats.
 * @author Tecnalia
 * @version 1.0
 */
@RestController
@RequestMapping("/api/qgis-ui")
public class LayerFormatController {
	
	/** Logger. **/
	private final Logger log = LoggerFactory.getLogger(LayerFormatController.class);
	
	/** Service to access the data of the LayerFormat objects. */
	@Autowired
	LayerFormatService layerFormatService;
	
	/** Service to access the data of the Layer objects. */
	@Autowired
	LayerService layerService;
	
	/** Messages manager. */
	@Autowired
	MessageSource messageSource;
	
	
	// ********** API METHODS ********** //
	
	/**
	 * Retrieves all the layer formats.
	 * Call example: https://localhost/api/qgis-ui/layer-formats
	 * @param locale The locale object.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/layer-formats")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveLayerFormats(@RequestHeader(name = "Accept-Language", required = false) Locale locale) {
		try {
			// Retrieve the list of layer formats
			log.info("LayerFormatController  ::  retrieveLayerFormats(Locale) :: Retrieving all the layer formats...");
			List<LayerFormatView> result = layerFormatService.retrieveLayerFormats();
			if (CollectionUtil.isNullOrEmpty(result)) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_LAYER_FORMAT.getConstant(), messageSource.getMessage("rest.layer.format.retrieve.400", null, locale));
			}
			log.info("LayerFormatController  ::  retrieveLayerFormats(Locale) :: The layer formats were retrieved successfully!");
			
			// Adjust the extensions
			log.info("LayerFormatController  ::  retrieveLayerFormats(Locale) :: Adjusting the extensions...");
			for (LayerFormatView layerFormat : result) {
				layerFormat.setExtension(layerFormat.getExtension().toUpperCase());
			}
			log.info("LayerFormatController  ::  retrieveLayerFormats(Locale) :: The extensions were adjusted successfully!");
			
			// Return response
			return ResponseEntity.status(HttpStatus.OK).body(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("LayerFormatController  ::  retrieveLayerFormats(Locale) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("LayerFormatController  ::  retrieveLayerFormats(Locale) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Retrieves the layer format which UUID corresponds to the given parameter.
	 * Call example: http://localhost/api/qgis-ui/layer-formats/uuid/{uuid}
	 * @param locale The locale.
	 * @param uuid The uuid.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/layer-formats/uuid/{uuid}")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveLayerFormatByUUID(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @PathVariable String uuid) {
		try {
			// Validate the parameter
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: Validating the UUID...");
			if (StringUtil.isNullOrEmpty(uuid)) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_LAYER_FORMAT.getConstant(), messageSource.getMessage("rest.layer.format.retrieve.uuid.400", null, locale));
			}
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: Validation completed!");
			
			// Retrieve the Layer Format
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: Retrieving the Layer Format [" + uuid.trim() + "]...");
			LayerFormat result = layerFormatService.retrieveLayerFormatByUUID(uuid.trim());
			if (result == null) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_LAYER_FORMAT.getConstant(), messageSource.getMessage("rest.layer.format.retrieve.role.400", null, locale));
			}
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: The Layer Format was retrieved successfully!");
			
			// Adjust the extension
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: Adjusting the extension...");
			result.setExtension(result.getExtension().toUpperCase());
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: The extension was adjusted successfully!");
			
			// Retrieve the associated layers
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: Retrieving the associated Layers...");
			result.setLayers(layerService.retrieveLayersByFormat(result.getUuid()));
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: The associated Layers were retrieved successfully!");
						
			// Format the dates
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: Formatting the dates...");
			result.setFormattedCreatedDate(DateUtil.buildFormattedDateFromTimestamp(result.getCreatedDate() * 1000L, locale));
			result.setFormattedLastModifiedDate(DateUtil.buildFormattedDateFromTimestamp(result.getLastModifiedDate() * 1000L, locale));
			if (result.getDeletedDate() != null) {
				result.setFormattedDeletedDate(DateUtil.buildFormattedDateFromTimestamp(result.getDeletedDate() * 1000L, locale));
			}
			log.info("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) :: The dates were formatted successfully!");
			
			// Return response
			return ResponseEntity.ok(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("LayerFormatController  ::  retrieveLayerFormatByUUID(Locale, String) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
}