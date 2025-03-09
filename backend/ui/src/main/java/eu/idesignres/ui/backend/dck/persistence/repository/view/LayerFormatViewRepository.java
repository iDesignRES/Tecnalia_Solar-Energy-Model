package eu.idesignres.ui.backend.dck.persistence.repository.view;

import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.view.LayerFormatView;


/**
 * JPA repository to manage the LayerFormatView objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface LayerFormatViewRepository extends GenericViewRepository<LayerFormatView, String> {

}
