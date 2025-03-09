package eu.idesignres.ui.backend.dck.persistence.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;


/**
 * JPA repository to manage the Process objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface ProcessRepository extends JpaRepository<eu.idesignres.ui.backend.dck.persistence.model.Process, String> {

	@Query("select p from Process p where p.uuid = ?1")
	public eu.idesignres.ui.backend.dck.persistence.model.Process findProcessByUUID(final String uuid);
}
