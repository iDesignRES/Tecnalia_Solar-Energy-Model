package eu.idesignres.ui.backend.dck.exception.controller.database;

import eu.idesignres.ui.backend.dck.exception.controller.ControllerGenericException;

/**
 * The controller update data exception.
 * @author Tecnalia
 * @version 1.0
 */
public final class UpdateDataException extends ControllerGenericException {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 7086492104860827983L;
	

	/**
	 * Constructor.
	 * @param subcategory The subcategory.
	 * @param message The message.
	 */
	public UpdateDataException(final String subcategory, final String message) {
        super(subcategory, message);
    }
}