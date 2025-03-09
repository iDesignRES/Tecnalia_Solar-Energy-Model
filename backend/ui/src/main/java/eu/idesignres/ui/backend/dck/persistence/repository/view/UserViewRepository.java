package eu.idesignres.ui.backend.dck.persistence.repository.view;

import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.view.UserView;


/**
 * JPA repository to manage the UserView objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface UserViewRepository extends GenericViewRepository<UserView, String> {

	@Query("select u from UserView u where u.uuid = ?1")
	public UserView findUserByUUIDFromView(final String uuid);
	
	@Query("select u from UserView u where u.username = ?1")
	public UserView findUserByUsernameFromView(final String username);
	
	@Query("select u from UserView u where u.username = ?1 and u.uuid != ?2")
	public UserView findUserByUsernameFromView(final String username, final String uuid);
}
