package eu.idesignres.ui.backend.dck.persistence.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.Actor;


/**
 * JPA repository to manage the Actor objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface ActorRepository extends JpaRepository<Actor, String> {

	@Query("update Actor a set a.username = ?2, a.role = ?3 where a.username = ?1")
	@Modifying
	public void updateActor(final String previuosUsername, final String newUsername, final String role);
}
