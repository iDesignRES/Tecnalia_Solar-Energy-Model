package eu.idesignres.ui.backend.dck.persistence.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.Scale;


/**
 * JPA repository to manage the Scale objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface ScaleRepository extends JpaRepository<Scale, String> {

	@Query("select s from Scale s where s.uuid = ?1")
	public Scale findScaleByUUID(final String uuid);
}
