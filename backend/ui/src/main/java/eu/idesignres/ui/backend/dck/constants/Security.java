package eu.idesignres.ui.backend.dck.constants;


/**
 * Enumeration for Security constants.
 * @author Tecnalia
 * @version 1.0
 */
public enum Security {
	SEC_URL_RESOURCES("/resources/**"),
	SEC_URL_FAVICON("/favicon.ico"),
	SEC_URL_HELLO("/api/qgis-ui/hello/**"),
	SEC_URL_ROLES("/api/qgis-ui/roles/**"),
	SEC_URL_USERS("/api/qgis-ui/users/**"),
	SEC_URL_SCALES("/api/qgis-ui/scales/**"),
	SEC_URL_PROCESSES("/api/qgis-ui/processes/**"),
	SEC_URL_LAYER_FORMATS("/api/qgis-ui/layer-formats/**"),
	SEC_URL_LAYERS("/api/qgis-ui/layers/**"),
	SEC_AUTHORIZATION("Authorization"),
	SEC_BEARER("Bearer "),
	SEC_JWT("JWT"),
	SEC_JWT_CLAIM_IDENTIFIER("identifier"),
	SEC_JWT_CLAIM_ROLE("role"),
	SEC_JWT_CLAIM_EMAIL("email"),
	SEC_SECRET("837cecf276fc4195a7c69d4436fc8552"),
	SEC_SECURE_APP("secure-app"),
	SEC_SECURE_API("secure-api"),
	SEC_EXPIRE("345600000L"),
	SEC_ROLE_ADMINISTRATOR("ROLE_ADMINISTRATOR"),
	SEC_ROLE_OPERATOR("ROLE_OPERATOR");
	
	
	/** The constant. */
	private String constant;
	
	
	
	/**
     * Constructs a Security.
     * @param constant The constant.
     */
	private Security(final String constant) {
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
