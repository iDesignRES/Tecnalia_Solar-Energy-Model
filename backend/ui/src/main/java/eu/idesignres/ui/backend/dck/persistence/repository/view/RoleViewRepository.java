package eu.idesignres.ui.backend.dck.persistence.repository.view;

import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.view.RoleView;


/**
 * JPA repository to manage the RoleView objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface RoleViewRepository extends GenericViewRepository<RoleView, String> {

}
