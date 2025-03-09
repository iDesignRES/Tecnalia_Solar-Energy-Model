package eu.idesignres.ui.backend.dck.security.dto;

import java.io.Serializable;
import java.util.Objects;


/**
 * DTO to store the information obtained from a CredentialDTO object.
 * @author Tecnalia
 * @version 1.0
 */
public final class CredentialsDTO implements Serializable {

	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 8917296454091368051L;
	
	/** The username. */
    private String username;
    
    /** The password. */
    private String password;
    
    /** The email. */
    private String email;
    
    /** The uuid. */
    private String uuid;
    
    /** The role. */
    private String role;
	
	
    /**
     * Constructs a CredentialsDTO.
     */
	public CredentialsDTO() {}
	
	/**
     * Constructs a CredentialsDTO.
     * @param username The username.
     * @param password The password.
     * @param email The email.
     * @param uuid The uuid.
     * @param role The role.
     */
	public CredentialsDTO(final String username, final String password, final String email,
			final String uuid, final String role) {
		this.username = username;
		this.password = password;
		this.email = email;
		this.uuid = uuid;
		this.role = role;
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

	/**
     * Gets the email.
     * @return String
     */
	public String getEmail() {
		return email;
	}

	/**
     * Sets the email.
     * @param email The email.
     */
	public void setEmail(final String email) {
		this.email = email;
	}
    
    /**
     * Gets the uuid.
     * @return String
     */
    public String getUuid() {
        return uuid;
    }

    /**
     * Sets the uuid.
     * @param uuid The uuid.
     */
    public void setUuid(final String uuid) {
        this.uuid = uuid;
    }
    
    /**
     * Gets the role.
     * @return String
     */
	public String getRole() {
		return role;
	}

	/**
     * Sets the role.
     * @param role The role.
     */
	public void setRole(final String role) {
		this.role = role;
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

        final CredentialsDTO dto = (CredentialsDTO) o;
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
    	StringBuffer buffer = new StringBuffer("CredentialsDTO {");
    	buffer.append("username=").append(getUsername());
    	buffer.append(", password=").append(getPassword());
    	buffer.append(", email=").append(getEmail());
    	buffer.append(", uuid=").append(getUuid());
    	buffer.append(", role=").append(getRole()).append("}");
    	return buffer.toString();
    }
}
