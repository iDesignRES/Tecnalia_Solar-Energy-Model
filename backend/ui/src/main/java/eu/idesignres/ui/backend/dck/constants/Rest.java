package eu.idesignres.ui.backend.dck.constants;


/**
 * Enumeration for REST constants.
 * @author Tecnalia
 * @version 1.0
 */
public enum Rest {
	REST_TIMEOUT("4000"),
	REST_LONG_TIMEOUT("20000"),
	REST_VERY_LONG_TIMEOUT("35000");
	

	/** The constant. */
	private String constant;
	
	
	
	/**
     * Constructs an Application.
     * @param constant The constant.
     */
	private Rest(final String constant) {
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
