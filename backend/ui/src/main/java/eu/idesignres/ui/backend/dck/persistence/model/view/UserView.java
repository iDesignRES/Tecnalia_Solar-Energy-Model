package eu.idesignres.ui.backend.dck.persistence.model.view;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

import org.springframework.data.annotation.Immutable;


/**
 * Model of a UserView object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "v12_idesignres_users")
@Immutable
public class UserView implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 458441298955825423L;

	
	/** The uuid. */
	@Id
	@Column(name = "uuid")
	private String uuid;
	
	/** The username. */
    @Column(name = "username")
    private String username;
    
    /** The password. */
    @Column(name = "password")
    private String password;
    
    /** The email. */
    @Column(name = "email")
    private String email;
	
	/** The createdDate. */
    @Column(name = "created_date")
    private Long createdDate;
	
	/** The lastModifiedDate. */
    @Column(name = "last_modified_date")
    private Long lastModifiedDate;
	
	/** The deletedDate. */
    @Column(name = "deleted_date")
    private Long deletedDate;
    
    /** The role. */
    @Column(name = "role")
    private String role;
    
    
  	/** The roleList. */
	private transient List<RoleView> roleList;
	
	/** The formattedCreatedDate. */
	private transient String formattedCreatedDate;
	
	/** The formattedLastModifiedDate. */
	private transient String formattedLastModifiedDate;
	
	/** The formattedDeletedDate. */
	private transient String formattedDeletedDate;
    
    
    /**
     * Constructs a UserView.
     */
    public UserView() {
    	super();
    	
    	roleList = new ArrayList<RoleView>();
    }
    
    /**
     * Constructs a UserView.
     * @param uuid The uuid.
     * @param username The username.
     * @param password The password.
     * @param email The email.
     * @param createdDate The createdDate.
     * @param lastModifiedDate The lastModifiedDate.
     * @param deletedDate The deletedDate.
     * @param role The role.
     */
    public UserView(final String uuid, final String username, final String password,
    		final String email, final Long createdDate, final Long lastModifiedDate,
    		final Long deletedDate, final String role) {
    	super();
    	
    	this.uuid = uuid;
    	this.username = username;
    	this.password = password;
    	this.email = email;
    	this.createdDate = createdDate;
    	this.lastModifiedDate = lastModifiedDate;
    	this.deletedDate = deletedDate;
    	this.role = role;
    	
    	roleList = new ArrayList<RoleView>();
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
     * Gets the roleList.
     * @return List<RoleView>
     */
    public List<RoleView> getRoleList() {
        return roleList == null ? new ArrayList<RoleView>() : roleList;
    }

    /**
     * Sets the roleList.
     * @param roleList The roleList.
     */
    public void setRoleList(final List<RoleView> roleList) {
        this.roleList = roleList == null ? new ArrayList<RoleView>() : roleList;
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
     * Gets the formattedCreatedDate.
     * @return String
     */
    public String getFormattedCreatedDate() {
        return formattedCreatedDate;
    }

    /**
     * Sets the formattedCreatedDate.
     * @param formattedCreatedDate The formattedCreatedDate.
     */
    public void setFormattedCreatedDate(final String formattedCreatedDate) {
        this.formattedCreatedDate = formattedCreatedDate;
    }
    
    /**
     * Gets the formattedLastModifiedDate.
     * @return String
     */
    public String getFormattedLastModifiedDate() {
        return formattedLastModifiedDate;
    }

    /**
     * Sets the formattedLastModifiedDate.
     * @param formattedLastModifiedDate The formattedLastModifiedDate.
     */
    public void setFormattedLastModifiedDate(final String formattedLastModifiedDate) {
        this.formattedLastModifiedDate = formattedLastModifiedDate;
    }
    
    /**
     * Gets the formattedDeletedDate.
     * @return String
     */
    public String getFormattedDeletedDate() {
        return formattedDeletedDate;
    }

    /**
     * Sets the formattedDeletedDate.
     * @param formattedDeletedDate The formattedDeletedDate.
     */
    public void setFormattedDeletedDate(final String formattedDeletedDate) {
        this.formattedDeletedDate = formattedDeletedDate;
    }
    
    
    /**
	 * Trims the object.
	 */
	public void trimObject() {
		uuid = uuid != null ? (uuid.trim().length() > 36 ? uuid.trim().substring(0, 36) : uuid.trim()) : null;
		username = username != null ? (username.trim().length() > 30 ? username.trim().substring(0, 30) : username.trim()) : null;
		password = password != null ? (password.trim().length() > 60 ? password.trim().substring(0, 60) : password.trim()) : null;
		email = email != null ? (email.trim().length() > 80 ? email.trim().substring(0, 80) : email.trim()) : null;
		role = role != null ? (role.trim().length() > 20 ? role.trim().substring(0, 20) : role.trim()) : null;
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

        final UserView vo = (UserView) o;
        if (vo.getUuid() == null || getUuid() == null) {
            return false;
        }
        
        return Objects.equals(getUuid(), vo.getUuid());
    }
    
    
    /*
     * (non-Javadoc)
     * @see java.lang.Object#hashCode()
     */
    @Override
    public int hashCode() {
        return Objects.hashCode(getUuid());
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
    	StringBuffer buffer = new StringBuffer("UserView {");
    	buffer.append("uuid=").append(getUuid());
    	buffer.append(", username=").append(getUsername());
    	buffer.append(", password=").append(getPassword());
    	buffer.append(", email=").append(getEmail());
    	buffer.append(", createdDate=").append(getCreatedDate());
    	buffer.append(", lastModifiedDate=").append(getLastModifiedDate());
    	buffer.append(", deletedDate=").append(getDeletedDate());
    	buffer.append(", role=").append(getRole());
    	buffer.append(", role=").append(getRole()).append("}");
    	return buffer.toString();
    }
}
