package eu.idesignres.ui.backend.dck.persistence.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.User;


/**
 * JPA repository to manage the User objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface UserRepository extends JpaRepository<User, String> {
	
	@Query("select u from User u where u.username = ?1")
	public User findUserByUsername(final String username);
	
	@Query("delete from User u where u.uuid = ?1")
	@Modifying
	public void deleteUserByUUID(final String uuid);
	
	@Query("delete from User u where u.username = ?1")
	@Modifying
	public void deleteUserByUsername(final String username);
	
	@Query("select u from User u where u.username = ?1 and u.password = ?2")
	public User authenticate(final String user, final String password);
}
