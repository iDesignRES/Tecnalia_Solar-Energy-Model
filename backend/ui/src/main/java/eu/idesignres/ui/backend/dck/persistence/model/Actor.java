package eu.idesignres.ui.backend.dck.persistence.model;

import java.io.Serializable;
import java.util.Objects;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;


/**
 * Model of an Actor object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "t13_idesignres_actors")
public class Actor implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = -1594497436428320802L;
	
	/** The username. */
	@Id
	@Size(max = 30)
    @Column(name = "username", length = 30, unique = true, updatable = false, nullable = false)
    private String username;
	
	/** The role. */
	@NotNull
	@Size(max = 25)
    @Column(name = "role", length = 25, nullable = false)
    private String role;
    
    
    /**
     * Constructs an Actor.
     */
    public Actor() {
    	super();
    }
    
    /**
     * Constructs an Actor.
     * @param username The username.
     * @param role The role.
     */
    public Actor(final String username, final String role) {
    	super();
    	
    	this.username = username;
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
    
    
    /**
	 * Trims the object.
	 */
	public void trimObject() {
		username = username != null ? (username.trim().length() > 30 ? username.trim().substring(0, 30) : username.trim()) : null;
		role = role != null ? (role.trim().length() > 25 ? role.trim().substring(0, 25) : role.trim()) : null;
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

        final Actor vo = (Actor) o;
        if (vo.getUsername() == null || getUsername() == null) {
            return false;
        }
        
        return Objects.equals(getUsername(), vo.getUsername());
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
     * @see java.lang.Object#clone()
     */
    @Override
	public Object clone() throws CloneNotSupportedException {
    	return super.clone();
	}
    
    
    /*
     * (non-Javadoc)
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
    	StringBuffer buffer = new StringBuffer("Actor {");
    	buffer.append("username=").append(getUsername());
    	buffer.append(", role=").append(getRole()).append("}");
    	return buffer.toString();
    }
}
