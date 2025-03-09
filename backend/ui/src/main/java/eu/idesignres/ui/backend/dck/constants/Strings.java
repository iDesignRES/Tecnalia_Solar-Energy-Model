package eu.idesignres.ui.backend.dck.constants;


/**
 * Enumeration for Strings constants.
 * @author Tecnalia
 * @version 1.0
 */
public enum Strings {
	STR_OK("OK"),
	STR_NOOK("NOOK"),
	STR_NULL("NULL"),
	STR_JDBC("JDBC"),
	STR_SSL("SSL"),
	STR_NONE("None"),
	STR_VALUE("value"),
	STR_TRUE("true"),
	STR_FALSE("false"),
	STR_BLANK(""),
	STR_WHITESPACE(" "),
	STR_DOT("."),
	STR_DOT_DOT(".."),
	STR_UNDERSCORE("_"),
	STR_SLASH("/"),
	STR_SEMICOLON(";"),
	STR_REPLACE_WILDCARD("{1}"),
	STR_SEPARATOR("::S::"),
	STR_FORBIDDEN("|%&*{}\\<>?\"'"),
	STR_OK_CODE("0"),
	STR_ENTER_KEY("n");
	
	
	/** The constant. */
	private String constant;
	
	
	
	/**
     * Constructs a Strings.
     * @param constant The constant.
     */
	private Strings(final String constant) {
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
