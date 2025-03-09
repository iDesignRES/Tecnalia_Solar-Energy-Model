package eu.idesignres.ui.backend.dck.persistence.repository.view;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.NoRepositoryBean;


/**
 * JPA repository to manage all the View objects.
 * @author Tecnalia
 * @version 1.0
 */
@NoRepositoryBean
public interface GenericViewRepository<T, ID> extends JpaRepository<T, ID> {

	List<T> findAll();
}
