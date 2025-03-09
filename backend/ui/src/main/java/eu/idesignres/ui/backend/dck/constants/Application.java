package eu.idesignres.ui.backend.dck.constants;


/**
 * Enumeration for Application constants.
 * @author Tecnalia
 * @version 1.0
 */
public enum Application {
	APP_DATETIME_UTC("UTC"),
	APP_EN_DATETIME_MASK("yyyy-MM-dd HH:mm:ss"),
	APP_ES_DATETIME_MASK("dd/MM/yyyy HH:mm:ss"),
	APP_MESSAGES_ENCODING("UTF-8"),
	APP_MESSAGES_BASENAME("messages"),
	APP_LOCALE_ES("es"),
	APP_LOCALE_EN("en");
	

	/** The constant. */
	private String constant;
	
	
	
	/**
     * Constructs an Application.
     * @param constant The constant.
     */
	private Application(final String constant) {
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
