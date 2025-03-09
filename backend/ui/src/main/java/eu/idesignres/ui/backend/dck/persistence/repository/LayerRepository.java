package eu.idesignres.ui.backend.dck.persistence.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import eu.idesignres.ui.backend.dck.persistence.model.Layer;


/**
 * JPA repository to manage the Layer objects.
 * @author Tecnalia
 * @version 1.0
 */
@Repository
public interface LayerRepository extends JpaRepository<Layer, String> {

	@Query("select l from Layer l where l.uuid = ?1")
	public Layer findLayerByUUID(final String uuid);
	
	@Query("select l from Layer l where l.name = ?1")
	public Layer findLayerByName(final String name);
	
	@Query("select l from Layer l where l.scale = ?1 order by l.name")
	public List<Layer> findLayersByScale(final String scale);
	
	@Query("select l from Layer l where l.layerFormat = ?1 order by l.name")
	public List<Layer> findLayersByFormat(final String format);
	
	@Query("delete from Layer l where l.uuid = ?1")
	@Modifying
	public void deleteLayerByUUID(final String uuid);
}
