package eu.idesignres.ui.backend.dck.persistence.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import eu.idesignres.ui.backend.dck.persistence.model.Scale;
import eu.idesignres.ui.backend.dck.persistence.model.view.ScaleView;
import eu.idesignres.ui.backend.dck.persistence.repository.ScaleRepository;
import eu.idesignres.ui.backend.dck.persistence.repository.view.ScaleViewRepository;


/**
 * Service to implement the operations on Scale objects.
 * @author Tecnalia
 * @version 1.0
 */
@Service
@Transactional
public class ScaleService {
	
	/** The JPA repository to manage the existing Scale objects. */
	@Autowired
	ScaleRepository scaleRepository;
	
	/** The JPA repository to manage the existing ScaleView objects. */
	@Autowired
	ScaleViewRepository scaleViewRepository;
	
	
	/**
	 * Retrieves all the scales existing in the database.
	 * @return List<ScaleView>
	 * @throws Exception
	 */
    public List<ScaleView> retrieveScales() throws Exception {
    	return scaleViewRepository.findAll();
    }
    
    
    /**
	 * Retrieves the Scale which uuid corresponds to the given parameter.
	 * @param uuid The uuid.
	 * @return Scale
	 * @throws Exception
	 */
    public Scale retrieveScaleByUUID(final String uuid) throws Exception {
		return scaleRepository.findScaleByUUID(uuid);
    }
}