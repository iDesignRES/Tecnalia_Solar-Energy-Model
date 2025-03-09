package eu.idesignres.ui.backend.dck.persistence.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import eu.idesignres.ui.backend.dck.persistence.model.view.ProcessView;
import eu.idesignres.ui.backend.dck.persistence.repository.ProcessRepository;
import eu.idesignres.ui.backend.dck.persistence.repository.view.ProcessViewRepository;


/**
 * Service to implement the operations on Process objects.
 * @author Tecnalia
 * @version 1.0
 */
@Service
@Transactional
public class ProcessService {
	
	/** The JPA repository to manage the existing Process objects. */
	@Autowired
	ProcessRepository processRepository;
	
	/** The JPA repository to manage the existing ProcessView objects. */
	@Autowired
	ProcessViewRepository processViewRepository;
	
	
	/**
	 * Retrieves all the processes existing in the database.
	 * @return List<ProcessView>
	 * @throws Exception
	 */
    public List<ProcessView> retrieveProcesses() throws Exception {
    	return processViewRepository.findAll();
    }
    
    
    /**
	 * Retrieves the Process which uuid corresponds to the given parameter.
	 * @param uuid The uuid.
	 * @return Process
	 * @throws Exception
	 */
    public eu.idesignres.ui.backend.dck.persistence.model.Process retrieveProcessByUUID(final String uuid) throws Exception {
		return processRepository.findProcessByUUID(uuid);
    }
}