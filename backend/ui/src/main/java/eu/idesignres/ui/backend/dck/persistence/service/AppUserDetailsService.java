package eu.idesignres.ui.backend.dck.persistence.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import eu.idesignres.ui.backend.dck.persistence.repository.UserRepository;
import eu.idesignres.ui.backend.dck.security.dto.CredentialsBuilderDTO;


/**
 * Service to implement the Spring Security "UserDetailsService" interface.
 * @author Tecnalia
 * @version 1.0
 */
@Service
public class AppUserDetailsService implements UserDetailsService {
	
	/** Logger. */
	private final Logger log = LoggerFactory.getLogger(UserDetailsService.class);
	
	/** The service to manage the existing credentials. */
	@Autowired
	UserRepository userRepository;

    
	/*
	 * (non-Javadoc)
	 * @see org.springframework.security.core.userdetails.UserDetailsService#loadUserByUsername(java.lang.String)
	 */
	@Override
    @Transactional
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
		try {
			log.info("AppUserDetailsService  ::  loadUserByUsername(String) :: calling service to fetch credentials by username...");
			return CredentialsBuilderDTO.build(userRepository.findUserByUsername(username));
		} catch (Exception e) {
			log.error("AppUserDetailsService  ::  loadUserByUsername(String) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
		}
        return null;
    }
}