package eu.idesignres.ui.backend.dck.persistence.repository.view;

import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.view.LayerSimpleView;


/**
 * JPA repository to manage the LayerSimpleView objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface LayerSimpleViewRepository extends GenericViewRepository<LayerSimpleView, String> {

}
