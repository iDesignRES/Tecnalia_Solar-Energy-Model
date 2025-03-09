package eu.idesignres.ui.backend.dck.exception.controller.database;

import eu.idesignres.ui.backend.dck.exception.controller.ControllerGenericException;

/**
 * The controller retrieve data exception.
 * @author Tecnalia
 * @version 1.0
 */
public final class RetrieveDataException extends ControllerGenericException {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 6957387756844767300L;

	
	/**
	 * Constructor.
	 * @param subcategory The subcategory.
	 * @param message The message.
	 */
	public RetrieveDataException(final String subcategory, final String message) {
        super(subcategory, message);
    }
}