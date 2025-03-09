package eu.idesignres.ui.backend.dck.persistence.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import eu.idesignres.ui.backend.dck.persistence.model.LayerFormat;
import eu.idesignres.ui.backend.dck.persistence.model.view.LayerFormatView;
import eu.idesignres.ui.backend.dck.persistence.repository.LayerFormatRepository;
import eu.idesignres.ui.backend.dck.persistence.repository.view.LayerFormatViewRepository;


/**
 * Service to implement the operations on LayerFormat objects.
 * @author Tecnalia
 * @version 1.0
 */
@Service
@Transactional
public class LayerFormatService {
	
	/** The JPA repository to manage the existing LayerFormat objects. */
	@Autowired
	LayerFormatRepository layerFormatRepository;
	
	/** The JPA repository to manage the existing LayerFormatView objects. */
	@Autowired
	LayerFormatViewRepository layerFormatViewRepository;
	
	
	/**
	 * Retrieves all the layer formats existing in the database.
	 * @return List<LayerFormatView>
	 * @throws Exception
	 */
    public List<LayerFormatView> retrieveLayerFormats() throws Exception {
    	return layerFormatViewRepository.findAll();
    }
    
    
    /**
	 * Retrieves the LayerFormat which uuid corresponds to the given parameter.
	 * @param uuid The uuid.
	 * @return LayerFormat
	 * @throws Exception
	 */
    public LayerFormat retrieveLayerFormatByUUID(final String uuid) throws Exception {
		return layerFormatRepository.findLayerFormatByUUID(uuid);
    }
}