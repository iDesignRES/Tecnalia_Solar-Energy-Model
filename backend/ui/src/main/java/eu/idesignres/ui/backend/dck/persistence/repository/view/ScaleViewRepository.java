package eu.idesignres.ui.backend.dck.persistence.repository.view;

import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.view.ScaleView;


/**
 * JPA repository to manage the ScaleView objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface ScaleViewRepository extends GenericViewRepository<ScaleView, String> {

}
