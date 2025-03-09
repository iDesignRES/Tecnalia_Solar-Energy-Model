package eu.idesignres.ui.backend.dck.controller;

import java.util.Locale;

import javax.validation.Valid;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.MessageSource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import eu.idesignres.ui.backend.dck.constants.Exceptions;
import eu.idesignres.ui.backend.dck.constants.Strings;
import eu.idesignres.ui.backend.dck.exception.controller.validation.ValidationException;
import eu.idesignres.ui.backend.dck.security.dto.CredentialsBuilderDTO;
import eu.idesignres.ui.backend.dck.security.dto.JwtDTO;
import eu.idesignres.ui.backend.dck.security.dto.LoginCredentialsDTO;
import eu.idesignres.ui.backend.dck.security.jwt.JwtTokenProvider;
import eu.idesignres.ui.backend.dck.util.CollectionUtil;


/**
 * Controller to check if the application is online.
 * @author Tecnalia
 * @version 1.0
 */
@RestController
@RequestMapping("/api/qgis-ui")
public class HelloController {
	
	/** Logger. **/
	private final Logger log = LoggerFactory.getLogger(HelloController.class);
	
	/** JWT provider. */
	@Autowired
    JwtTokenProvider jwtProvider;
	
	/** Authentication manager. */
	@Autowired
    AuthenticationManager authenticationManager;
	
	/** Messages manager. */
	@Autowired
	MessageSource messageSource;
	
	
	// ********** API METHODS ********** //
	
	
	/**
	 * Returns online information.
	 * Call example: https://localhost/api/qgis-ui/hello
	 * @param locale The locale.
	 * @return ResponseEntity<String>
	 */
	@GetMapping("/hello")
    public ResponseEntity<String> hello(@RequestHeader(name = "Accept-Language", required = false) Locale locale) {
		log.info("HelloController  ::  hello(Locale) ::  Tekzone Backend online!");
		return ResponseEntity.ok(messageSource.getMessage("rest.hello.200", null, locale));
    }
	
	
	/**
	 * Do the authentication.
	 * Call example: https://localhost/api/qgis-ui/hello/authenticate
	 * @param locale The locale.
	 * @param credentials The credentials.
	 * @param bindingResult The bindingResult.
	 * @return ResponseEntity<Object>
	 */
	@PostMapping("/hello/authenticate")
    public ResponseEntity<Object> authenticate(@RequestHeader(name = "Accept-Language", required = false) Locale locale, @Valid @RequestBody LoginCredentialsDTO credentials, final BindingResult bindingResult) {
		try {
			// Do the authentication
			log.info("HelloController  ::  authenticate(Locale, LoginCredentialsDTO, BindingResult) :: Authenticating...");
			Authentication authentication = authenticationManager.authenticate(
	                new UsernamePasswordAuthenticationToken(credentials.getUsername(), credentials.getPassword()));
			log.info("HelloController  ::  authenticate(Locale, LoginCredentialsDTO, BindingResult) :: Authenticated!");
			
			// Place the authentication object to Security Context
			log.info("HelloController  ::  authenticate(Locale, LoginCredentialsDTO, BindingResult) :: Placing the authentication object to Security context...");
	        SecurityContextHolder.getContext().setAuthentication(authentication);
	        log.info("HelloController  ::  authenticate(Locale, LoginCredentialsDTO, BindingResult) :: Placed!");
	        
	        // Check if the credentials are acceptable
	        log.info("HelloController  ::  authenticate(Locale, LoginCredentialsDTO, BindingResult) :: Generating JWT token...");
	        final CredentialsBuilderDTO userDetails = (CredentialsBuilderDTO) authentication.getPrincipal();
	        if (userDetails != null && CollectionUtil.isNullOrEmpty(userDetails.getAuthorities())) {
	        	throw new ValidationException(Exceptions.EXC_SUBCATEGORY_USER.getConstant(), messageSource.getMessage("rest.hello.authenticate.406", null, locale));
	        }
	        
	        // Create the JWT token
	        return new ResponseEntity<Object>(
	        		new JwtDTO(jwtProvider.generateJWTToken(authentication)),
		        		HttpStatus.OK);
		} catch (ValidationException ve) {
			// Error: 406: Not acceptable request
			log.error("HelloController  ::  authenticate(Locale, LoginCredentialsDTO, BindingResult) ::  ERROR  ::  " + ve.getClass().getName() + "  ::  " + ve.getMessage());
			return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE).body(ve.getMessage());
		} catch (AuthenticationException ae) {
			// Error 403: Forbidden ; Error 503: Service unavailable
			log.error("HelloController  ::  authenticate(Locale, LoginCredentialsDTO, BindingResult) ::  ERROR  ::  " + ae.getClass().getName() + "  ::  " + ae.getMessage());
			if (ae.getMessage().indexOf(Strings.STR_JDBC.getConstant()) != -1) {
				return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(messageSource.getMessage("rest.generic.503", null, locale));
			}
			return ResponseEntity.status(HttpStatus.FORBIDDEN).body(messageSource.getMessage("rest.hello.authenticate.403", null, locale));
		} catch (Exception e) {
			// Error 500: Internal server error
			log.error("HelloController  ::  authenticate(Locale, LoginCredentialsDTO, BindingResult) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(messageSource.getMessage("rest.generic.500", null, locale));
		}
    }
}