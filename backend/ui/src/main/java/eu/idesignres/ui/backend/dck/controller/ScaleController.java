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
import eu.idesignres.ui.backend.dck.persistence.model.Scale;
import eu.idesignres.ui.backend.dck.persistence.model.view.ScaleView;
import eu.idesignres.ui.backend.dck.persistence.service.LayerService;
import eu.idesignres.ui.backend.dck.persistence.service.ScaleService;
import eu.idesignres.ui.backend.dck.util.CollectionUtil;
import eu.idesignres.ui.backend.dck.util.DateUtil;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * Controller to manage the operations about scales.
 * @author Tecnalia
 * @version 1.0
 */
@RestController
@RequestMapping("/api/qgis-ui")
public class ScaleController {
	
	/** Logger. **/
	private final Logger log = LoggerFactory.getLogger(ScaleController.class);
	
	/** Service to access the data of the Scale objects. */
	@Autowired
	ScaleService scaleService;
	
	/** Service to access the data of the Layer objects. */
	@Autowired
	LayerService layerService;
	
	/** Messages manager. */
	@Autowired
	MessageSource messageSource;
	
	
	// ********** API METHODS ********** //
	
	/**
	 * Retrieves all the layer formats.
	 * Call example: https://localhost/api/qgis-ui/scales
	 * @param locale The locale object.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/scales")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveScales(@RequestHeader(name = "Accept-Language", required = false) Locale locale) {
		try {
			// Retrieve the list of scales
			log.info("ScaleController  ::  retrieveScales(Locale) :: Retrieving all the scales...");
			final List<ScaleView> result = scaleService.retrieveScales();
			if (CollectionUtil.isNullOrEmpty(result)) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_SCALE.getConstant(), messageSource.getMessage("rest.layer.format.retrieve.400", null, locale));
			}
			log.info("ScaleController  ::  retrieveScales(Locale) :: The scales were retrieved successfully!");
			
			// Return response
			return ResponseEntity.status(HttpStatus.OK).body(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("ScaleController  ::  retrieveScales(Locale) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("ScaleController  ::  retrieveScales(Locale) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Retrieves the scale which UUID corresponds to the given parameter.
	 * Call example: http://localhost/api/qgis-ui/scales/uuid/{uuid}
	 * @param locale The locale.
	 * @param uuid The uuid.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/scales/uuid/{uuid}")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveScaleByUUID(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @PathVariable String uuid) {
		try {
			// Validate the parameter
			log.info("ScaleController  ::  retrieveScaleByUUID(Locale, String) :: Validating the UUID...");
			if (StringUtil.isNullOrEmpty(uuid)) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_SCALE.getConstant(), messageSource.getMessage("rest.layer.format.retrieve.uuid.400", null, locale));
			}
			log.info("ScaleController  ::  retrieveScaleByUUID(Locale, String) :: Validation completed!");
			
			// Retrieve the Scale
			log.info("ScaleController  ::  retrieveScaleByUUID(Locale, String) :: Retrieving the Scale [" + uuid.trim() + "]...");
			Scale result = scaleService.retrieveScaleByUUID(uuid.trim());
			if (result == null) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_SCALE.getConstant(), messageSource.getMessage("rest.layer.format.retrieve.role.400", null, locale));
			}
			log.info("ScaleController  ::  retrieveScaleByUUID(Locale, String) :: The Scale was retrieved successfully!");
			
			// Retrieve the associated layers
			log.info("ScaleController  ::  retrieveScaleByUUID(Locale, String) :: Retrieving the associated Layers...");
			result.setLayers(layerService.retrieveLayersByScale(result.getUuid()));
			log.info("ScaleController  ::  retrieveScaleByUUID(Locale, String) :: The associated Layers were retrieved successfully!");
			
			// Format the dates
			log.info("ScaleController  ::  retrieveScaleByUUID(Locale, String) :: Formatting the dates...");
			result.setFormattedCreatedDate(DateUtil.buildFormattedDateFromTimestamp(result.getCreatedDate() * 1000L, locale));
			result.setFormattedLastModifiedDate(DateUtil.buildFormattedDateFromTimestamp(result.getLastModifiedDate() * 1000L, locale));
			if (result.getDeletedDate() != null) {
				result.setFormattedDeletedDate(DateUtil.buildFormattedDateFromTimestamp(result.getDeletedDate() * 1000L, locale));
			}
			log.info("ScaleController  ::  retrieveScaleByUUID(Locale, String) :: The dates were formatted successfully!");
			
			// Return response
			return ResponseEntity.ok(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("ScaleController  ::  retrieveScaleByUUID(Locale, String) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("ScaleController  ::  retrieveScaleByUUID(Locale, String) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
}