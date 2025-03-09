package eu.idesignres.ui.backend.dck.constants;


/**
 * Enumeration for Entities constants.
 * @author Tecnalia
 * @version 1.0
 */
public enum Entities {
	ENT_GENERAL_DEFAULT_UUID("00000000-0000-0000-0000-000000000000"),
	ENT_GENERAL_SECONDARY_UUID("11111111-1111-1111-1111-111111111111"),
	ENT_GENERAL_MAX_UUID("99999999-9999-9999-9999-999999999999");
	

	/** The constant. */
	private String constant;
	
	
	
	/**
     * Constructs an Entities.
     * @param constant The constant.
     */
	private Entities(final String constant) {
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
