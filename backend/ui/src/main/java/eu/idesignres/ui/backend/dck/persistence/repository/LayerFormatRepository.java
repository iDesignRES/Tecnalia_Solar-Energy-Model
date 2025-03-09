package eu.idesignres.ui.backend.dck.persistence.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.LayerFormat;


/**
 * JPA repository to manage the LayerFormat objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface LayerFormatRepository extends JpaRepository<LayerFormat, String> {

	@Query("select l from LayerFormat l where l.uuid = ?1")
	public LayerFormat findLayerFormatByUUID(final String uuid);
}
