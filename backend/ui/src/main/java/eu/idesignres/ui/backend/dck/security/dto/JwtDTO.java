package eu.idesignres.ui.backend.dck.security.dto;

import java.io.Serializable;
import java.util.Objects;


/**
 * DTO to store the information obtained from JWT.
 * @author Tecnalia
 * @version 1.0
 */
public final class JwtDTO implements Serializable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = -6121788317588290774L;
	
	/** The token. **/
	private String token;

    
    /**
     * Constructs a JwtDTO.
     */
    public JwtDTO() {}
    
    /**
     * Constructs a JwtDTO.
     * @param token The token.
     */
    public JwtDTO(final String token) {
        this.token = token;
    }
    

    /**
     * Gets the token.
     * @return String
     */
    public String getToken() {
        return token;
    }

    /**
     * Sets the token.
     * @param token The token.
     */
    public void setToken(final String token) {
        this.token = token;
    }
    
    
    /*
     * (non-Javadoc)
     * @see java.lang.Object#equals(java.lang.Object)
     */
    @Override
    public boolean equals(final Object o) {
        if (this == o) {
            return true;
        }
        
        if (o == null || getClass() != o.getClass()) {
            return false;
        }

        final JwtDTO dto = (JwtDTO) o;
        if (dto.getToken() == null || getToken() == null) {
            return false;
        }
        
        return Objects.equals(getToken(), dto.getToken());
    }
	

    /*
     * (non-Javadoc)
     * @see java.lang.Object#hashCode()
     */
    @Override
    public int hashCode() {
        return Objects.hashCode(getToken());
    }
    

    /*
     * (non-Javadoc)
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
    	StringBuffer buffer = new StringBuffer("JwtDTO {");
    	buffer.append("token=").append(getToken()).append("}");
    	return buffer.toString();
    }
}
