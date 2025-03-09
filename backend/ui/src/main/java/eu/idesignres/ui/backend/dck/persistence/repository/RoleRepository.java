package eu.idesignres.ui.backend.dck.persistence.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.Role;


/**
 * JPA repository to manage the Role objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface RoleRepository extends JpaRepository<Role, String> {

	@Query("select r from Role r where r.uuid = ?1")
	public Role findRoleByUUID(final String uuid);
}
