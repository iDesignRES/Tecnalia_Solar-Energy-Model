package eu.idesignres.ui.backend.dck.persistence.repository.view;

import java.util.List;

import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.view.LayerComplexView;


/**
 * JPA repository to manage the LayerComplexView objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface LayerComplexViewRepository extends GenericViewRepository<LayerComplexView, String> {

	@Query("select l from LayerComplexView l where l.processUuid = ?1")
	public List<LayerComplexView> findLayersByProcess(final String process);
}
