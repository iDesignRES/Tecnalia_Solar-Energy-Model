package eu.idesignres.ui.backend.dck.persistence.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import eu.idesignres.ui.backend.dck.persistence.model.Actor;
import eu.idesignres.ui.backend.dck.persistence.model.User;
import eu.idesignres.ui.backend.dck.persistence.model.view.UserView;
import eu.idesignres.ui.backend.dck.persistence.repository.ActorRepository;
import eu.idesignres.ui.backend.dck.persistence.repository.UserRepository;
import eu.idesignres.ui.backend.dck.persistence.repository.view.UserViewRepository;


/**
 * Service to implement the operations on User objects.
 * @author Tecnalia
 * @version 1.0
 */
@Service
@Transactional
public class UserService {
	
	/** The JPA repository to manage the existing User objects. */
	@Autowired
	UserRepository userRepository;
	
	@Autowired
	UserViewRepository userViewRepository;
	
	/** The JPA repository to manage the existing Actor objects. */
	@Autowired
	ActorRepository actorRepository;
	
	
	/**
	 * Retrieves all the UserView objects existing in the database.
	 * @return List<UserView>
	 * @throws Exception
	 */
    public List<UserView> retrieveUsers() throws Exception {
    	return userViewRepository.findAll();
    }
    
    
    /**
	 * Retrieves the UserView object which UUID corresponds to the given parameter.
	 * @param uuid The uuid.
	 * @return UserView
	 * @throws Exception
	 */
    public UserView retrieveUserByUUID(final String uuid) throws Exception {
   		return userViewRepository.findUserByUUIDFromView(uuid);
    }
    
    
    /**
	 * Retrieves the User object which username corresponds to the given parameter.
	 * @param username The username.
	 * @return User
	 * @throws Exception
	 */
    public User retrieveUserByUsername(final String username) throws Exception {
   		return userRepository.findUserByUsername(username);
    }
    
    
    /**
	 * Retrieves the UserView object which username corresponds to the given parameter.
	 * @param username The username.
	 * @return UserView
	 * @throws Exception
	 */
    public UserView retrieveUserByUsernameFromView(final String username) throws Exception {
   		return userViewRepository.findUserByUsernameFromView(username);
    }
    
    
    /**
	 * Retrieves the UserView object which username corresponds to the given parameter.
	 * @param username The username.
	 * @param uuid The uuid.
	 * @return UserView
	 * @throws Exception
	 */
    public UserView retrieveUserByUsername(final String username, final String uuid) throws Exception {
   		return userViewRepository.findUserByUsernameFromView(username, uuid);
    }
    
    
    /**
	 * Adds a User.
	 * @param user The user.
	 * @return User
	 * @throws Exception
	 */
    public User addUser(final User user) throws Exception {
    	return userRepository.saveAndFlush(user);
    }
    
    
    /**
	 * Adds an Actor.
	 * @param actor The actor.
	 * @return Actor
	 * @throws Exception
	 */
    public Actor addActor(final Actor actor) throws Exception {
    	return actorRepository.saveAndFlush(actor);
    }
    
    
    /**
	 * Deletes a User by uuid.
	 * @param uuid The uuid.
	 * @throws Exception
	 */
    public void deleteUserByUUID(final String uuid) throws Exception {
    	userRepository.deleteUserByUUID(uuid);
    }
    
    
    /**
	 * Deletes a User by username.
	 * @param username The username.
	 * @throws Exception
	 */
    public void deleteUserByUsername(final String username) throws Exception {
    	userRepository.deleteUserByUsername(username);
    }
}