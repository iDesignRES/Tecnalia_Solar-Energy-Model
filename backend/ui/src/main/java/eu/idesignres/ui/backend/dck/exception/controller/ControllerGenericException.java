package eu.idesignres.ui.backend.dck.exception.controller;

import eu.idesignres.ui.backend.dck.constants.Exceptions;
import eu.idesignres.ui.backend.dck.exception.GenericException;

/**
 * The controller abstract generic exception.
 * @author Tecnalia
 * @version 1.0
 */
public abstract class ControllerGenericException extends GenericException {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 5229376041758877572L;

	
	/**
	 * Constructor.
	 * @param subcategory The subcategory.
	 * @param message The message.
	 */
	protected ControllerGenericException(final String subcategory, final String message) {
        super(Exceptions.EXC_CATEGORY_CONTROLLER.getConstant(), subcategory, message);
    }
}