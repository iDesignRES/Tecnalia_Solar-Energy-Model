package eu.idesignres.ui.backend.dck.security.dto;

import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import eu.idesignres.ui.backend.dck.persistence.model.User;


/**
 * DTO to build and store the information obtained from a CredentialDTO object.
 * @author Tecnalia
 * @version 1.0
 */
public final class CredentialsBuilderDTO implements UserDetails {

	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 178546742993250299L;
	
	/** Logger. **/
	private static final Logger log = LoggerFactory.getLogger(CredentialsBuilderDTO.class);
	
	/** The username. */
    private String username;
    
    /** The password. */
    private String password;
    
    /** The email. */
    private String email;
    
    /** The uuid. */
    private String uuid;
    
    /** The authorities (roles). */
    private Collection<? extends GrantedAuthority> authorities;
    

    /**
     * Constructs a CredentialsBuilderDTO.
     */
    public CredentialsBuilderDTO() {}
    
    /**
     * Constructs a CredentialsBuilderDTO.
     * @param username The username.
     * @param password The password.
     * @param email The email.
     * @param uuid The uuid.
     * @param authorities The authorities (roles).
     */
    public CredentialsBuilderDTO(final String username, final String password, final String email,
    		final String uuid, final Collection<? extends GrantedAuthority> authorities) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.uuid = uuid;
        this.authorities = authorities;
    }
    

    /*
     * (non-Javadoc)
     * @see org.springframework.security.core.userdetails.UserDetails#getUsername()
     */
    @Override
    public String getUsername() {
        return username;
    }    

    /*
     * (non-Javadoc)
     * @see org.springframework.security.core.userdetails.UserDetails#getPassword()
     */
    @Override
    public String getPassword() {
        return password;
    }
    
    /**
     * Gets the email.
     * @return String
     */
    public String getEmail() {
        return email;
    }
    
    /**
     * Gets the uuid.
     * @return String
     */
    public String getUuid() {
        return uuid;
    }
    
    /*
     * (non-Javadoc)
     * @see org.springframework.security.core.userdetails.UserDetails#getAuthorities()
     */
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }

    /*
     * (non-Javadoc)
     * @see org.springframework.security.core.userdetails.UserDetails#isAccountNonExpired()
     */
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    /*
     * (non-Javadoc)
     * @see org.springframework.security.core.userdetails.UserDetails#isAccountNonLocked()
     */
    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    /*
     * (non-Javadoc)
     * @see org.springframework.security.core.userdetails.UserDetails#isCredentialsNonExpired()
     */
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    /*
     * (non-Javadoc)
     * @see org.springframework.security.core.userdetails.UserDetails#isEnabled()
     */
    @Override
    public boolean isEnabled() {
        return true;
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

        final CredentialsBuilderDTO dto = (CredentialsBuilderDTO) o;
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
    	StringBuffer buffer = new StringBuffer("CredentialsBuilderDTO {");
    	buffer.append("username=").append(getUsername());
    	buffer.append(", password=").append(getPassword());
    	buffer.append(", email=").append(getEmail());
    	buffer.append(", uuid=").append(getUuid()).append("}");
    	return buffer.toString();
    }
    
    
    /**
     * Builds a CredentialsBuilderDTO from a CredentialsDTO object.
     * @param user The user.
     * @return CredentialsBuilderDTO
     */
    public static CredentialsBuilderDTO build(final User user){
    	log.info("CredentialsBuilderDTO  ::  build(User) :: extracting authorities (roles)...");
        List<GrantedAuthority> authorities =
        		user.getRoles().stream().map(
        				role -> new SimpleGrantedAuthority(role.getName())).collect(Collectors.toList());
                
        log.info("CredentialsBuilderDTO  ::  build(User) :: building and returning the CredentialsDTO object...");
        return new CredentialsBuilderDTO(
        		user.getUsername(),
        		user.getPassword(),
        		user.getEmail(),
        		user.getUuid(),
        		authorities);
    }
}
