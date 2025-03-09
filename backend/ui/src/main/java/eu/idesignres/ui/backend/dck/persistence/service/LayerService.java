package eu.idesignres.ui.backend.dck.persistence.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import eu.idesignres.ui.backend.dck.persistence.model.Layer;
import eu.idesignres.ui.backend.dck.persistence.model.view.LayerComplexView;
import eu.idesignres.ui.backend.dck.persistence.model.view.LayerSimpleView;
import eu.idesignres.ui.backend.dck.persistence.repository.LayerRepository;
import eu.idesignres.ui.backend.dck.persistence.repository.view.LayerComplexViewRepository;
import eu.idesignres.ui.backend.dck.persistence.repository.view.LayerSimpleViewRepository;


/**
 * Service to implement the operations on Layer objects.
 * @author Tecnalia
 * @version 1.0
 */
@Service
@Transactional
public class LayerService {
	
	/** The JPA repository to manage the existing Layer objects. */
	@Autowired
	LayerRepository layerRepository;
	
	/** The JPA repository to manage the existing LayerSimpleView objects. */
	@Autowired
	LayerSimpleViewRepository layerSimpleViewRepository;
	
	/** The JPA repository to manage the existing LayerComplexView objects. */
	@Autowired
	LayerComplexViewRepository layerComplexViewRepository;
	
	
	/**
	 * Retrieves all the simple layers existing in the database.
	 * @return List<LayerSimpleView>
	 * @throws Exception
	 */
    public List<LayerSimpleView> retrieveSimpleLayers() throws Exception {
    	return layerSimpleViewRepository.findAll();
    }
    
    
    /**
	 * Retrieves all the complex layers existing in the database.
	 * @return List<LayerComplexView>
	 * @throws Exception
	 */
    public List<LayerComplexView> retrieveComplexLayers() throws Exception {
    	return layerComplexViewRepository.findAll();
    }
    
    
    /**
	 * Retrieves the Layer which uuid corresponds to the given parameter.
	 * @param uuid The uuid.
	 * @return Layer
	 * @throws Exception
	 */
    public Layer retrieveLayerByUUID(final String uuid) throws Exception {
		return layerRepository.findLayerByUUID(uuid);
    }
    
    
    /**
	 * Retrieves the Layer which name corresponds to the given parameter.
	 * @param name The name.
	 * @return Layer
	 * @throws Exception
	 */
    public Layer retrieveLayerByName(final String name) throws Exception {
		return layerRepository.findLayerByName(name);
    }
    
    
    /**
	 * Retrieves the Layer which scale corresponds to the given parameter.
	 * @param scale The scale.
	 * @return List<Layer>
	 * @throws Exception
	 */
    public List<Layer> retrieveLayersByScale(final String scale) throws Exception {
		return layerRepository.findLayersByScale(scale);
    }
    
    
    /**
	 * Retrieves the Layers which format corresponds to the given parameter.
	 * @param scale The scale.
	 * @return List<Layer>
	 * @throws Exception
	 */
    public List<Layer> retrieveLayersByFormat(final String format) throws Exception {
		return layerRepository.findLayersByFormat(format);
    }
    
    
    /**
	 * Retrieves the Layers which process corresponds to the given parameter.
	 * @param process The process.
	 * @return List<LayerComplexView>
	 * @throws Exception
	 */
    public List<LayerComplexView> retrieveLayersByProcess(final String process) throws Exception {
		return layerComplexViewRepository.findLayersByProcess(process);
    }
    
    
    /**
	 * Adds a Layer.
	 * @param layer The layer.
	 * @return Layer
	 * @throws Exception
	 */
    public Layer addLayer(final Layer layer) throws Exception {
    	return layerRepository.saveAndFlush(layer);
    }
    
    
    /**
	 * Deletes a Layer by UUID.
	 * @param uuid The uuid.
	 * @throws Exception
	 */
    public void deleteLayerByUUID(final String uuid) throws Exception {
    	layerRepository.deleteLayerByUUID(uuid);
    }
}