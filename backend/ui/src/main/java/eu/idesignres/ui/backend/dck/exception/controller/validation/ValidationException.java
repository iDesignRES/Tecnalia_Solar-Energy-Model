package eu.idesignres.ui.backend.dck.exception.controller.validation;

import eu.idesignres.ui.backend.dck.exception.controller.ControllerGenericException;

/**
 * The controller validation exception.
 * @author Tecnalia
 * @version 1.0
 */
public final class ValidationException extends ControllerGenericException {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = -5267197127964384581L;

	
	/**
	 * Constructor.
	 * @param subcategory The subcategory.
	 * @param message The message.
	 */
	public ValidationException(final String subcategory, final String message) {
        super(subcategory, message);
    }
}