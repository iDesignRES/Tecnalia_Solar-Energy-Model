package eu.idesignres.ui.backend.dck.exception.controller.database;

import eu.idesignres.ui.backend.dck.exception.controller.ControllerGenericException;

/**
 * The controller insert data exception.
 * @author Tecnalia
 * @version 1.0
 */
public final class InsertDataException extends ControllerGenericException {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 8261294652941786564L;
	

	/**
	 * Constructor.
	 * @param subcategory The subcategory.
	 * @param message The message.
	 */
	public InsertDataException(final String subcategory, final String message) {
        super(subcategory, message);
    }
}