package eu.idesignres.ui.backend.dck.persistence.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import eu.idesignres.ui.backend.dck.persistence.model.Role;
import eu.idesignres.ui.backend.dck.persistence.model.view.RoleView;
import eu.idesignres.ui.backend.dck.persistence.repository.RoleRepository;
import eu.idesignres.ui.backend.dck.persistence.repository.view.RoleViewRepository;


/**
 * Service to implement the operations on Role objects.
 * @author Tecnalia
 * @version 1.0
 */
@Service
@Transactional
public class RoleService {
	
	/** The JPA repository to manage the existing Role objects. */
	@Autowired
	RoleRepository roleRepository;
	
	/** The JPA repository to manage the existing RoleView objects. */
	@Autowired
	RoleViewRepository roleViewRepository;
	
	
	/**
	 * Retrieves all the roles existing in the database.
	 * @return List<RoleView>
	 * @throws Exception
	 */
    public List<RoleView> retrieveRoles() throws Exception {
    	return roleViewRepository.findAll();
    }
    
    
    /**
	 * Retrieves the Role which uuid corresponds to the given parameter.
	 * @param uuid The uuid.
	 * @return Role
	 * @throws Exception
	 */
    public Role retrieveRoleByUUID(final String uuid) throws Exception {
		return roleRepository.findRoleByUUID(uuid);
    }
}