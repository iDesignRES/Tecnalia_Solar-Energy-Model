package eu.idesignres.ui.backend.dck.persistence.model;

import java.io.Serializable;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;


/**
 * Model of a User object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "t12_idesignres_users",
	uniqueConstraints = {
			@UniqueConstraint(columnNames = {"username"})})
public class User implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 6359616085795033387L;
	
	/** The username. */
	@Id
	@Size(max = 30)
    @Column(name = "username", length = 30, nullable = false)
    private String username;

	/** The password. */
	@NotNull
	@Size(max = 60)
    @Column(name = "password", length = 60, nullable = false)
    private String password;
	
	/** The email. */
	@NotNull
	@Size(max = 80)
    @Column(name = "email", length = 80, nullable = false)
    private String email;
	
	/** The uuid. */
	@NotNull
	@Size(max = 36)
	@Column(name = "uuid", length = 36, nullable = false)
	private String uuid;
	
	/** The createdDate. */
	@NotNull
    @Column(name = "created_date", nullable = false)
    private Long createdDate;
	
	/** The lastModifiedDate. */
	@NotNull
    @Column(name = "last_modified_date", nullable = false)
    private Long lastModifiedDate;
	
	/** The deletedDate. */
    @Column(name = "deleted_date", nullable = true)
    private Long deletedDate;
	
	
	/** The roles (Many-To-Many relationship). */
	@NotNull
    @ManyToMany(fetch = FetchType.EAGER, cascade = {CascadeType.ALL})
    @JoinTable(name = "t13_idesignres_actors", joinColumns = @JoinColumn(name = "username"), inverseJoinColumns = @JoinColumn(name = "role"))
    private Set<Role> roles = new HashSet<>();
	
	
	/** The role. */
	private transient String role;
	
	/** The repeatPassword. */
	private transient String repeatPassword;
	
	/** The previousUsername. */
	private transient String previousUsername;
	
    
    /**
     * Constructs a User.
     */
    public User() {
    	super();
    }
    
    /**
     * Constructs a User.
     * @param username The username.
     * @param password The password.
     * @param email The email.
     * @param uuid The uuid.
     * @param createdDate The createdDate.
     * @param lastModifiedDate The lastModifiedDate.
     * @param deletedDate The deletedDate.
     */
    public User(final String username, final String password, final String email,
    		final String uuid, final Long createdDate, final Long lastModifiedDate,
    		final Long deletedDate) {
    	super();
    	
    	this.username = username;
        this.password = password;
        this.email = email;
        this.uuid = uuid;
        this.createdDate = createdDate;
    	this.lastModifiedDate = lastModifiedDate;
    	this.deletedDate = deletedDate;
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
     * Gets the createdDate.
     * @return Long
     */
    public Long getCreatedDate() {
        return createdDate;
    }

    /**
     * Sets the createdDate.
     * @param createdDate The createdDate.
     */
    public void setCreatedDate(final Long createdDate) {
        this.createdDate = createdDate;
    }
    
    /**
     * Gets the lastModifiedDate.
     * @return Long
     */
    public Long getLastModifiedDate() {
        return lastModifiedDate;
    }

    /**
     * Sets the lastModifiedDate.
     * @param lastModifiedDate The lastModifiedDate.
     */
    public void setLastModifiedDate(final Long lastModifiedDate) {
        this.lastModifiedDate = lastModifiedDate;
    }
    
    /**
     * Gets the deletedDate.
     * @return Long
     */
    public Long getDeletedDate() {
        return deletedDate;
    }

    /**
     * Sets the deletedDate.
     * @param deletedDate The deletedDate.
     */
    public void setDeletedDate(final Long deletedDate) {
        this.deletedDate = deletedDate;
    }
    
    /**
     * Gets the roles.
     * @return Set<Role>
     */
	public Set<Role> getRoles() {
        return roles;
    }

	/**
     * Sets the roles.
     * @param roles The roles.
     */
    public void setRoles(final Set<Role> roles) {
        this.roles = roles;
    }
    
    /**
     * Gets the repeatPassword.
     * @return String
     */
    public String getRepeatPassword() {
        return repeatPassword;
    }

    /**
     * Sets the repeatPassword.
     * @param repeatPassword The repeatPassword.
     */
    public void setRepeatPassword(final String repeatPassword) {
        this.repeatPassword = repeatPassword;
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
     * Gets the previousUsername.
     * @return String
     */
    public String getPreviousUsername() {
        return previousUsername;
    }

    /**
     * Sets the previousUsername.
     * @param previousUsername The previousUsername.
     */
    public void setPreviousUsername(final String previousUsername) {
        this.previousUsername = previousUsername;
    }
    
    
    /**
	 * Trims the object.
	 */
	public void trimObject() {
		username = username != null ? (username.trim().length() > 30 ? username.trim().substring(0, 30) : username.trim()) : null;
		password = password != null ? (password.trim().length() > 60 ? password.trim().substring(0, 60) : password.trim()) : null;
		email = email != null ? (email.trim().length() > 80 ? email.trim().substring(0, 80) : email.trim()) : null;
		uuid = uuid != null ? (uuid.trim().length() > 36 ? uuid.trim().substring(0, 36) : uuid.trim()) : null;
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

        final User vo = (User) o;
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
    	StringBuffer buffer = new StringBuffer("User {");
    	buffer.append("username=").append(getUsername());
    	buffer.append(", password=").append(getPassword());
    	buffer.append(", email=").append(getEmail());
    	buffer.append(", uuid=").append(getUuid());
    	buffer.append(", createdDate=").append(getCreatedDate());
    	buffer.append(", lastModifiedDate=").append(getLastModifiedDate());
    	buffer.append(", deletedDate=").append(getDeletedDate()).append("}");
    	return buffer.toString();
    }
}
