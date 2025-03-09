package eu.idesignres.ui.backend.dck.persistence.model.view;

import java.io.Serializable;
import java.util.Objects;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;


/**
 * Model of a LayerFormatView object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "v02_idesignres_layer_formats")
public class LayerFormatView implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 2803879608098807448L;
	
	
	/** The uuid. */
	@Id
	@Column(name = "uuid")
	private String uuid;
	
	/** The name. */
    @Column(name = "name")
    private String name;

	/** The extension. */
    @Column(name = "extension")
    private String extension;
	
	/** The createdDate. */
    @Column(name = "created_date")
    private Long createdDate;
	
	/** The lastModifiedDate. */
    @Column(name = "last_modified_date")
    private Long lastModifiedDate;
	
	/** The deletedDate. */
    @Column(name = "deleted_date")
    private Long deletedDate;
    
    /** The layers. */
    @Column(name = "layers")
    private Integer layers;
    
    
    /**
     * Constructs a LayerFormatView.
     */
    public LayerFormatView() {
    	super();
    	
    	layers = 0;
    }
    
    /**
     * Constructs a LayerFormatView.
     * @param uuid The uuid.
     * @param name The name.
     * @param extension The extension.
     * @param createdDate The createdDate.
     * @param lastModifiedDate The lastModifiedDate.
     * @param deletedDate The deletedDate.
     */
    public LayerFormatView(final String uuid, final String name, final String extension,
    		final Long createdDate, final Long lastModifiedDate, final Long deletedDate) {
    	super();
    	
    	this.uuid = uuid;
    	this.name = name;
        this.extension = extension;
        
        this.createdDate = createdDate;
    	this.lastModifiedDate = lastModifiedDate;
    	this.deletedDate = deletedDate;
    	
    	layers = 0;
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
     * Gets the layers.
     * @return Integer
     */
    public Integer getLayers() {
        return layers != null ? layers : 0;
    }

    /**
     * Sets the layers.
     * @param layers The layers.
     */
    public void setLayers(final Integer layers) {
        this.layers = layers != null ? layers : 0;
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

        final LayerFormatView vo = (LayerFormatView) o;
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
    	StringBuffer buffer = new StringBuffer("LayerFormatView {");
    	buffer.append("uuid=").append(getUuid());
    	buffer.append(", name=").append(getName());
    	buffer.append(", extension=").append(getExtension());
    	buffer.append(", createdDate=").append(getCreatedDate());
    	buffer.append(", lastModifiedDate=").append(getLastModifiedDate());
    	buffer.append(", deletedDate=").append(getDeletedDate());
    	buffer.append(", layers=").append(getLayers()).append("}");
    	return buffer.toString();
    }
}
