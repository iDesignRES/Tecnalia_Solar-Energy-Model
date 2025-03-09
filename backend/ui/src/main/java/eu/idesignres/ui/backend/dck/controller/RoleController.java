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
import eu.idesignres.ui.backend.dck.persistence.model.Role;
import eu.idesignres.ui.backend.dck.persistence.model.view.RoleView;
import eu.idesignres.ui.backend.dck.persistence.service.RoleService;
import eu.idesignres.ui.backend.dck.persistence.service.UserService;
import eu.idesignres.ui.backend.dck.util.CollectionUtil;
import eu.idesignres.ui.backend.dck.util.DateUtil;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * Controller to manage the operations about roles.
 * @author Tecnalia
 * @version 1.0
 */
@RestController
@RequestMapping("/api/qgis-ui")
public class RoleController {
	
	/** Logger. **/
	private final Logger log = LoggerFactory.getLogger(RoleController.class);
	
	/** Service to access the data of the Role objects. */
	@Autowired
	RoleService roleService;
	
	/** Service to access the data of the User objects. */
	@Autowired
	UserService userService;
	
	/** Messages manager. */
	@Autowired
	MessageSource messageSource;
	
	
	// ********** API METHODS ********** //
	
	/**
	 * Retrieves all the roles.
	 * Call example: https://localhost/api/qgis-ui/roles
	 * @param locale The locale object.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/roles")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveRoles(@RequestHeader(name = "Accept-Language", required = false) Locale locale) {
		try {
			// Retrieve the list of roles
			log.info("RoleController  ::  retrieveRoles(Locale) :: Retrieving all the roles...");
			final List<RoleView> result = roleService.retrieveRoles();
			if (CollectionUtil.isNullOrEmpty(result)) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_ROLE.getConstant(), messageSource.getMessage("rest.role.retrieve.400", null, locale));
			}
			log.info("RoleController  ::  retrieveRoles(Locale) :: The roles were retrieved successfully!");
			
			// Return response
			return ResponseEntity.status(HttpStatus.OK).body(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("RoleController  ::  retrieveRoles(Locale) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("RoleController  ::  retrieveRoles(Locale) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Retrieves the role which UUID corresponds to the given parameter.
	 * Call example: http://localhost/api/qgis-ui/roles/uuid/{uuid}
	 * @param locale The locale.
	 * @param uuid The uuid.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/roles/uuid/{uuid}")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveRoleByUUID(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @PathVariable String uuid) {
		try {
			// Validate the parameter
			log.info("RoleController  ::  retrieveRoleByUUID(Locale, String) :: Validating the UUID...");
			if (StringUtil.isNullOrEmpty(uuid)) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_ROLE.getConstant(), messageSource.getMessage("rest.role.retrieve.uuid.400", null, locale));
			}
			log.info("RoleController  ::  retrieveRoleByUUID(Locale, String) :: Validation completed!");
			
			// Retrieve the Role
			log.info("RoleController  ::  retrieveRoleByUUID(Locale, String) :: Retrieving the Role [" + uuid.trim() + "]...");
			Role result = roleService.retrieveRoleByUUID(uuid.trim());
			if (result == null) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_ROLE.getConstant(), messageSource.getMessage("rest.role.retrieve.role.400", null, locale));
			}
			log.info("RoleController  ::  retrieveRoleByUUID(Locale, String) :: The Role was retrieved successfully!");
			
			// Format the dates
			log.info("RoleController  ::  retrieveRoleByUUID(Locale, String) :: Formatting the dates...");
			result.setFormattedCreatedDate(DateUtil.buildFormattedDateFromTimestamp(result.getCreatedDate() * 1000L, locale));
			result.setFormattedLastModifiedDate(DateUtil.buildFormattedDateFromTimestamp(result.getLastModifiedDate() * 1000L, locale));
			if (result.getDeletedDate() != null) {
				result.setFormattedDeletedDate(DateUtil.buildFormattedDateFromTimestamp(result.getDeletedDate() * 1000L, locale));
			}
			log.info("RoleController  ::  retrieveRoleByUUID(Locale, String) :: The dates were formatted successfully!");
			
			// Return response
			return ResponseEntity.ok(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("RoleController  ::  retrieveRoleByUUID(Locale, String) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("RoleController  ::  retrieveRoleByUUID(Locale, String) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
}