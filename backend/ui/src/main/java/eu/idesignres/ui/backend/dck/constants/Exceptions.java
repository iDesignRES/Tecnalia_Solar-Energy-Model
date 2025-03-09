package eu.idesignres.ui.backend.dck.constants;


/**
 * Enumeration for Exceptions constants.
 * @author Tecnalia
 * @version 1.0
 */
public enum Exceptions {
	EXC_CATEGORY_CONTROLLER("CONTROLLER"),
	EXC_SUBCATEGORY_USER("USER"),
	EXC_SUBCATEGORY_ROLE("ROLE"),
	EXC_SUBCATEGORY_SCALE("SCALE"),
	EXC_SUBCATEGORY_PROCESS("PROCESS"),
	EXC_SUBCATEGORY_LAYER_FORMAT("LAYER_FORMAT"),
	EXC_SUBCATEGORY_LAYER("LAYER"),
	EXC_SUBCATEGORY_NETWORK("NETWORK");
	
	
	/** The constant. */
	private String constant;
	
	
	
	/**
     * Constructs a Exceptions.
     * @param constant The constant.
     */
	private Exceptions(final String constant) {
		this.constant = constant;
	}
	
	
	
	/**
     * Gets the constant.
     * @return String
     */
	public String getConstant() {
		return constant;
	}
}
