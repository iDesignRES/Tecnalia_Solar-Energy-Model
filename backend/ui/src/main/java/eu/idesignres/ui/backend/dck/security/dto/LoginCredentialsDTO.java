package eu.idesignres.ui.backend.dck.security.dto;

import java.io.Serializable;
import java.util.Objects;

import javax.validation.constraints.NotNull;


/**
 * DTO to store the information obtained in a login action.
 * @author Tecnalia
 * @version 1.0
 */
public class LoginCredentialsDTO implements Serializable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = -2158507235254739599L;

	/** The username. */
	@NotNull
    private String username;

	/** The password. */
	@NotNull
    private String password;
    
    
    /**
     * Constructs a LoginCredentialsDTO.
     */
    public LoginCredentialsDTO() {}
    
    /**
     * Constructs a LoginCredentialsDTO.
     * @param username The username.
     * @param password The password.
     */
    public LoginCredentialsDTO(final String username, final String password) {
        this.username = username;
        this.password = password;
    }
    

    /**
     * Gets the username.
     * @return String
     */
    public String getUsername() {
        return username;
    }

    /**
     * Sets the username.
     * @param username The username.
     */
    public void setUsername(final String username) {
        this.username = username;
    }

    /**
     * Gets the password.
     * @return String
     */
    public String getPassword() {
        return password;
    }

    /**
     * Sets the password.
     * @param password The password.
     */
    public void setPassword(final String password) {
        this.password = password;
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

        final LoginCredentialsDTO dto = (LoginCredentialsDTO) o;
        if (dto.getUsername() == null || getUsername() == null) {
            return false;
        }
        
        return Objects.equals(getUsername(), dto.getUsername());
    }
    
    
    /*
     * (non-Javadoc)
     * @see java.lang.Object#hashCode()
     */
    @Override
    public int hashCode() {
        return Objects.hashCode(getUsername());
    }
    
    
    /*
     * (non-Javadoc)
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
    	StringBuffer buffer = new StringBuffer("LoginCredentialsDTO {");
    	buffer.append("username=").append(getUsername());
    	buffer.append(", password=").append(getPassword()).append("}");
    	return buffer.toString();
    }
}
