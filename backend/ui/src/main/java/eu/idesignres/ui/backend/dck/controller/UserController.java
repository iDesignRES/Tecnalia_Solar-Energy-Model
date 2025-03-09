package eu.idesignres.ui.backend.dck.controller;

import java.util.List;
import java.util.Locale;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.MessageSource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import eu.idesignres.ui.backend.dck.constants.Exceptions;
import eu.idesignres.ui.backend.dck.exception.controller.ControllerGenericException;
import eu.idesignres.ui.backend.dck.exception.controller.database.InsertDataException;
import eu.idesignres.ui.backend.dck.exception.controller.database.RetrieveDataException;
import eu.idesignres.ui.backend.dck.exception.controller.validation.ValidationException;
import eu.idesignres.ui.backend.dck.model.Connection;
import eu.idesignres.ui.backend.dck.persistence.model.Actor;
import eu.idesignres.ui.backend.dck.persistence.model.User;
import eu.idesignres.ui.backend.dck.persistence.model.view.RoleView;
import eu.idesignres.ui.backend.dck.persistence.model.view.UserView;
import eu.idesignres.ui.backend.dck.persistence.service.RoleService;
import eu.idesignres.ui.backend.dck.persistence.service.UserService;
import eu.idesignres.ui.backend.dck.util.CollectionUtil;
import eu.idesignres.ui.backend.dck.util.DateUtil;
import eu.idesignres.ui.backend.dck.util.SFTPUtil;
import eu.idesignres.ui.backend.dck.util.StringUtil;
import eu.idesignres.ui.backend.dck.validation.UserValidator;


/**
 * Controller to manage the operations about users.
 * @author Tecnalia
 * @version 1.0
 */
@RestController
@RequestMapping("/api/qgis-ui")
public class UserController {
	
	/** Logger. **/
	private final Logger log = LoggerFactory.getLogger(UserController.class);
	
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
	
	/** The sftpBaseOutputDirectory. */
	@Value("${sftp.base.output.directory}")
	private String sftpBaseOutputDirectory;
	
	/** Service to access the data of the User objects. */
	@Autowired
	UserService userService;
	
	/** Service to access the data of the Role objects. */
	@Autowired
	RoleService roleService;
	
	/** Password encoder. */
	@Autowired
	private PasswordEncoder passwordEncoder;
	
	/** Messages manager. */
	@Autowired
	MessageSource messageSource;
	
	
	// ********** API METHODS ********** //
	
	
	/**
	 * Retrieves all the users.
	 * Call example: https://localhost/api/qgis-ui/users
	 * @param locale The locale object.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/users")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveUsers(@RequestHeader(name = "Accept-Language", required = false) Locale locale) {
		try {
			// Retrieve the list of users
			log.info("UserController  ::  retrieveUsers(Locale) :: Retrieving the Users...");
			List<UserView> result = userService.retrieveUsers();
			log.info("UserController  ::  retrieveUsers(Locale) :: The Users were retrieved successfully!");
			
			// Return response
			return ResponseEntity.status(HttpStatus.OK).body(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("UserController  ::  retrieveUsers(Locale) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("UserController  ::  retrieveUsers(Locale) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Retrieves the user which UUID corresponds to the given parameter.
	 * Call example: http://localhost/api/qgis-ui/users/uuid/{uuid}
	 * @param locale The locale.
	 * @param uuid The uuid.
	 * @return ResponseEntity<Object>
	 */
	@GetMapping("/users/uuid/{uuid}")
	@Secured({ "ROLE_ADMINISTRATOR" })
    public ResponseEntity<Object> retrieveUserByUUID(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @PathVariable String uuid) {
		try {
			// Validate the parameter
			log.info("UserController  ::  retrieveUserByUUID(Locale, String) :: Validating the UUID...");
			if (StringUtil.isNullOrEmpty(uuid)) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_USER.getConstant(), messageSource.getMessage("rest.user.retrieve.400", null, locale));
			}
			log.info("UserController  ::  retrieveUserByUUID(Locale, String) :: Validation completed!");
			
			// Retrieve the full list of roles
			log.info("UserController  ::  retrieveUserByUUID(Locale, String) :: Retrieving the full list of workgroups...");
			final List<RoleView> roleList = roleService.retrieveRoles();
			if (CollectionUtil.isNullOrEmpty(roleList)) {
				throw new RetrieveDataException(Exceptions.EXC_SUBCATEGORY_USER.getConstant(), messageSource.getMessage("rest.user.retrieve.role.list.400", null, locale));
			}
			log.info("UserController  ::  retrieveUserByUUID(Locale, String) :: The full list of workgroups was retrieved successfully!");
			
			// Retrieve the user
			log.info("UserController  ::  retrieveUserByUUID(Locale, String) :: Retrieving the user [" + uuid.trim() + "]...");
			UserView result = userService.retrieveUserByUUID(uuid.trim());
			log.info("UserController  ::  retrieveUserByUUID(Locale, String) :: The user was retrieved successfully!");
			
			if (result != null) {
				// Format the dates
				log.info("UserController  ::  retrieveUserByUUID(Locale, String) :: Formatting the dates...");
				result.setFormattedCreatedDate(DateUtil.buildFormattedDateFromTimestamp(result.getCreatedDate() * 1000L, locale));
				result.setFormattedLastModifiedDate(DateUtil.buildFormattedDateFromTimestamp(result.getLastModifiedDate() * 1000L, locale));
				if (result.getDeletedDate() != null) {
					result.setFormattedDeletedDate(DateUtil.buildFormattedDateFromTimestamp(result.getDeletedDate() * 1000L, locale));
				}
				log.info("UserController  ::  retrieveUserByUUID(Locale, String) :: The dates were formatted successfully!");
			} else {
				result = new UserView();
			}
			result.setRoleList(roleList);
			
			// Return response
			return ResponseEntity.ok(result);
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("UserController  ::  retrieveUserByUUID(Locale, String) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("UserController  ::  retrieveUserByUUID(Locale, String) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Adds a new User in the database.
	 * Call example: https://localhost/api/qgis-ui/users/add
	 * @param locale The locale object.
	 * @param user The user object.
	 * @return ResponseEntity<Object>
	 */
	@PostMapping("/users/add")
	@Secured({ "ROLE_ADMINISTRATOR" })
	@Transactional
    public ResponseEntity<Object> addUser(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @RequestBody User user) {
		try {
			// Validate the User object
			log.info("UserController  ::  addUser(Locale, User) :: Validating the User object...");
			final String validation = UserValidator.getInstance(locale).validate(user, false, false);
			if (validation != null) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_USER.getConstant(), validation);
			}
			user.trimObject();
			if (userService.retrieveUserByUsername(user.getUsername()) != null) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_USER.getConstant(), messageSource.getMessage("rest.user.add.name.400", null, locale));
			}
			log.info("UserController  ::  addUser(Locale, User) :: Validation completed!");
			
			// Set the encrypted password and the UUID
			log.info("UserController  ::  addUser(Locale, User) :: Setting the encrypted password and the UUID...");
			user.setPassword(passwordEncoder.encode(user.getPassword()));
			user.setUuid(UUID.randomUUID().toString());
			log.info("UserController  ::  addUser(Locale, User) :: Encrypted password and UUID susccefully established!");
			
			// Establish the dates
			log.info("UserController  ::  addUser(Locale, User) :: Establishing the dates...");
			final Long now = DateUtil.getCurrentShortTimestamp();
			user.setCreatedDate(now);
			user.setLastModifiedDate(now);
			log.info("UserController  ::  addUser(Locale, User) :: Dates established!");
			
			// Create the user's directory in the SFTP Server
			log.info("UserController  ::  addUser(Locale, User) :: Creating the user's directory in the SFTP Server...");
			SFTPUtil.createOrRemoveRemoteDirectory(new Connection(sftpHost, Integer.valueOf(sftpPort), sftpUsername, sftpPassword),
					sftpBaseOutputDirectory + user.getUsername(), true);
			log.info("UserController  ::  addUser(Locale, User) :: The remote user's directory was susccefully created!");
			
			// Add the User and the Actor objects
			log.info("UserController  ::  addUser(Locale, User) :: Adding the User and Actor objects...");
			if (userService.addUser(user) == null) {
				throw new InsertDataException(Exceptions.EXC_SUBCATEGORY_USER.getConstant(), messageSource.getMessage("rest.user.add.user.400", null, locale));
			}
			if (userService.addActor(new Actor(user.getUsername(), user.getRole())) == null) {
				throw new InsertDataException(Exceptions.EXC_SUBCATEGORY_USER.getConstant(), messageSource.getMessage("rest.user.add.actor.400", null, locale));
			}
			log.info("UserController  ::  addUser(Locale, User) :: The User and Actor objects were added succesfully!");
			
			// Return response
			return ResponseEntity.ok(messageSource.getMessage("rest.user.add.200", null, locale));
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("UserController  ::  addUser(Locale, User) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("UserController  ::  addUser(Locale, User) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
	
	
	/**
	 * Deletes a User.
	 * Call example: https://localhost/api/qgis-ui/users/delete
	 * @param locale The locale object.
	 * @param user The user.
	 * @return ResponseEntity<String>
	 */
	@PostMapping("/users/delete")
	@Secured({ "ROLE_ADMINISTRATOR" })
	@Transactional
    public ResponseEntity<String> deleteUser(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @RequestBody User user) {
		try {
			// Validate the User object
			log.info("UserController  ::  deleteUser(Locale, User) :: Validating the User object...");
			final String validation = UserValidator.getInstance(locale).validate(user, true, true);
			if (validation != null) {
				throw new ValidationException(Exceptions.EXC_SUBCATEGORY_USER.getConstant(), validation);
			}
			user.trimObject();
			log.info("UserController  ::  deleteUser(Locale, User) :: Validation completed!");
			
			// Create the user's directory in the SFTP Server
			log.info("UserController  ::  addUser(Locale, User) :: Removing the user's directory in the SFTP Server...");
			SFTPUtil.createOrRemoveRemoteDirectory(new Connection(sftpHost, Integer.valueOf(sftpPort), sftpUsername, sftpPassword),
					sftpBaseOutputDirectory + user.getUsername(), false);
			log.info("UserController  ::  addUser(Locale, User) :: The remote user's directory was susccefully removed!");
			
			// Delete the User object (and Actor object in cascade)
			log.info("UserController  ::  deleteUser(Locale, User) :: Deleting the User object...");
			userService.deleteUserByUsername(user.getUsername());
			log.info("UserController  ::  deleteUser(Locale, User) :: The User object was deleted succesfully!");
			
			// Return response
			return ResponseEntity.ok(messageSource.getMessage("rest.user.delete.200", null, locale));
		} catch (ControllerGenericException cge) {
			// Error: 400: Bad request
			log.error("UserController  ::  deleteUser(Locale, User) ::  ERROR  ::  " + cge.getClass().getName() + "  ::  " + cge.getMessage());
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(cge.getMessage());
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("UserController  ::  deleteUser(Locale, User) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
}