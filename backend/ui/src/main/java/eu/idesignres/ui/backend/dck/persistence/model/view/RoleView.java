package eu.idesignres.ui.backend.dck.persistence.model.view;

import java.io.Serializable;
import java.util.Objects;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;


/**
 * Model of an RoleView object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "v11_idesignres_roles")
public class RoleView implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = -1383404267500670544L;
	
	
	/** The name. */
	@Id
    @Column(name = "name")
    private String name;

	/** The description. */
    @Column(name = "description")
    private String description;
	
	/** The uuid. */
	@Column(name = "uuid")
	private String uuid;
	
	/** The createdDate. */
    @Column(name = "created_date")
    private Long createdDate;
	
	/** The lastModifiedDate. */
    @Column(name = "last_modified_date")
    private Long lastModifiedDate;
	
	/** The deletedDate. */
    @Column(name = "deleted_date")
    private Long deletedDate;
	
    /** The users. */
    @Column(name = "users")
    private Integer users;
    
    
    /**
     * Constructs a RoleView.
     */
    public RoleView() {
    	super();
    	
    	users = 0;
    }
    
    /**
     * Constructs a RoleView.
     * @param name The name.
     * @param description The description.
     * @param uuid The uuid.
     * @param createdDate The createdDate.
     * @param lastModifiedDate The lastModifiedDate.
     * @param deletedDate The deletedDate.
     * @param users The users.
     */
    public RoleView(final String name, final String description, final String uuid,
    		final Long createdDate, final Long lastModifiedDate, final Long deletedDate,
    		final Integer users) {
    	super();
    	
    	this.name = name;
        this.description = description;
        this.uuid = uuid;
        this.createdDate = createdDate;
    	this.lastModifiedDate = lastModifiedDate;
    	this.deletedDate = deletedDate;
    	this.users = users == null || users < 0 ? 0 : users;
    }
    

    /**
     * Gets the name.
     * @return String
     */
    public String getName() {
        return name;
    }

    /**
     * Sets the name.
     * @param name The name.
     */
    public void setName(final String name) {
        this.name = name;
    }
    
    /**
     * Gets the description.
     * @return String
     */
    public String getDescription() {
        return description;
    }

    /**
     * Sets the description.
     * @param description The description.
     */
    public void setDescription(final String description) {
        this.description = description;
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
     * Gets the users.
     * @return Integer
     */
    public Integer getUsers() {
    	return users == null || users < 0 ? 0 : users;
    }

    /**
     * Sets the users.
     * @param users The users.
     */
    public void setUsers(final Integer users) {
    	this.users = users == null || users < 0 ? 0 : users;
    }
    
    
    /**
	 * Trims the object.
	 */
	public void trimObject() {
		name = name != null ? (name.trim().length() > 25 ? name.trim().substring(0, 25) : name.trim()) : null;
		description = description != null ? (description.trim().length() > 150 ? description.trim().substring(0, 150) : description.trim()) : null;
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

        final RoleView vo = (RoleView) o;
        if (vo.getName() == null || getName() == null) {
            return false;
        }
        
        return Objects.equals(getName(), vo.getName());
    }
    
    
    /*
     * (non-Javadoc)
     * @see java.lang.Object#hashCode()
     */
    @Override
    public int hashCode() {
        return Objects.hashCode(getName());
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
    	StringBuffer buffer = new StringBuffer("RoleView {");
    	buffer.append("name=").append(getName());
    	buffer.append(", description=").append(getDescription());
    	buffer.append(", uuid=").append(getUuid());
    	buffer.append(", createdDate=").append(getCreatedDate());
    	buffer.append(", lastModifiedDate=").append(getLastModifiedDate());
    	buffer.append(", deletedDate=").append(getDeletedDate());
    	buffer.append(", users=").append(getUsers()).append("}");
    	return buffer.toString();
    }
}
