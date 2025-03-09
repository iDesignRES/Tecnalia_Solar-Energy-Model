package eu.idesignres.ui.backend.dck.persistence.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;


/**
 * Model of a LayerFormat object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "t02_idesignres_layer_formats",
	uniqueConstraints = {
			@UniqueConstraint(columnNames = {"name"})})
public class LayerFormat implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = -5451938623897806642L;

	
	/** The uuid. */
	@Id
	@Size(max = 36)
	@Column(name = "uuid", length = 36, unique = true)
	private String uuid;
	
	/** The name. */
	@NotNull
	@Size(max = 30)
    @Column(name = "name", length = 30, nullable = false)
    private String name;

	/** The extension. */
	@NotNull
	@Size(max = 5)
    @Column(name = "extension", length = 5, nullable = false)
    private String extension;
	
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
    
	
	/** The formattedCreatedDate. */
	private transient String formattedCreatedDate;
	
	/** The formattedLastModifiedDate. */
	private transient String formattedLastModifiedDate;
	
	/** The formattedDeletedDate. */
	private transient String formattedDeletedDate;
	
	/** The layers. */
	private transient List<Layer> layers;
    
    
    /**
     * Constructs a LayerFormat.
     */
    public LayerFormat() {
    	super();
    	
    	layers = new ArrayList<Layer>();
    }
    
    /**
     * Constructs a LayerFormat.
     * @param uuid The uuid.
     * @param name The name.
     * @param extension The extension.
     * @param createdDate The createdDate.
     * @param lastModifiedDate The lastModifiedDate.
     * @param deletedDate The deletedDate.
     */
    public LayerFormat(final String uuid, final String name, final String extension,
    		final Long createdDate, final Long lastModifiedDate, final Long deletedDate) {
    	super();
    	
    	this.uuid = uuid;
    	this.name = name;
        this.extension = extension;
        
        this.createdDate = createdDate;
    	this.lastModifiedDate = lastModifiedDate;
    	this.deletedDate = deletedDate;
    	
    	layers = new ArrayList<Layer>();
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
     * Gets the extension.
     * @return String
     */
    public String getExtension() {
        return extension;
    }

    /**
     * Sets the extension.
     * @param extension The extension.
     */
    public void setExtension(final String extension) {
        this.extension = extension;
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
     * Gets the layers.
     * @return List<Layer>
     */
    public List<Layer> getLayers() {
        return layers != null ? layers : new ArrayList<Layer>();
    }

    /**
     * Sets the layers.
     * @param layers The layers.
     */
    public void setLayers(final List<Layer> layers) {
        this.layers = layers != null ? layers : new ArrayList<Layer>();;
    }
    
    
    /**
	 * Trims the object.
	 */
	public void trimObject() {
		uuid = uuid != null ? (uuid.trim().length() > 36 ? uuid.trim().substring(0, 36) : uuid.trim()) : null;
		name = name != null ? (name.trim().length() > 30 ? name.trim().substring(0, 30) : name.trim()) : null;
		extension = extension != null ? (extension.trim().length() > 5 ? extension.trim().substring(0, 5) : extension.trim()) : null;
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

        final LayerFormat vo = (LayerFormat) o;
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
    	StringBuffer buffer = new StringBuffer("LayerFormat {");
    	buffer.append("uuid=").append(getUuid());
    	buffer.append(", name=").append(getName());
    	buffer.append(", extension=").append(getExtension());
    	buffer.append(", createdDate=").append(getCreatedDate());
    	buffer.append(", lastModifiedDate=").append(getLastModifiedDate());
    	buffer.append(", deletedDate=").append(getDeletedDate());
    	buffer.append(", layers=").append(getLayers().size()).append("}");
    	return buffer.toString();
    }
}
