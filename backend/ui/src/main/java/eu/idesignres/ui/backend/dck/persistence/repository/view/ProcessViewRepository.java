package eu.idesignres.ui.backend.dck.persistence.repository.view;

import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.view.ProcessView;


/**
 * JPA repository to manage the ProcessView objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface ProcessViewRepository extends GenericViewRepository<ProcessView, String> {

}
