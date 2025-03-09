package eu.idesignres.ui.backend.dck.persistence.model.view;

import java.io.Serializable;
import java.util.Objects;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;


/**
 * Model of a LayerSimpleView object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "v21A_idesignres_layers_simple")
public class LayerSimpleView implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 3255360187634805155L;
	
	
	/** The uuid. */
	@Id
	@Column(name = "uuid")
	private String uuid;
	
	/** The name. */
    @Column(name = "name")
    private String name;

	/** The fullPath. */
    @Column(name = "fullPath")
    private String fullPath;
	
	/** The createdDate. */
    @Column(name = "created_date")
    private Long createdDate;
	
	/** The lastModifiedDate. */
    @Column(name = "last_modified_date")
    private Long lastModifiedDate;
	
	/** The deletedDate. */
    @Column(name = "deleted_date")
    private Long deletedDate;
    
    /** The scaleName. */
    @Column(name = "scale_name")
    private String scaleName;
	
	/** The layerFormatName. */
    @Column(name = "layer_format_name")
    private String layerFormatName;
    
    /** The processes. */
    @Column(name = "processes")
    private Integer processes;
    
    
    /**
     * Constructs a LayerComplexView.
     */
    public LayerSimpleView() {
    	super();
    }
    
    /**
     * Constructs a LayerComplexView.
     * @param uuid The uuid.
     * @param name The name.
     * @param fullPath The fullPath.
     * @param createdDate The createdDate.
     * @param lastModifiedDate The lastModifiedDate.
     * @param deletedDate The deletedDate.
     * @param scaleName The scaleName.
     * @param layerFormatName The layerFormatName.
     * @param processes The processes.
     */
    public LayerSimpleView(final String uuid, final String name, final String fullPath,
    		final Long createdDate, final Long lastModifiedDate, final Long deletedDate,
    		final String scaleName, final String layerFormatName, final Integer processes) {
    	super();
    	
    	this.uuid = uuid;
    	this.name = name;
    	this.fullPath = fullPath;
        this.createdDate = createdDate;
    	this.lastModifiedDate = lastModifiedDate;
    	this.deletedDate = deletedDate;
    	this.scaleName = scaleName;
    	this.layerFormatName = layerFormatName;
    	this.processes = processes == null || processes < 0 ? 0 : processes;
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
     * Gets the fullPath.
     * @return String
     */
    public String getFullPath() {
        return fullPath;
    }

    /**
     * Sets the fullPath.
     * @param fullPath The fullPath.
     */
    public void setFullPath(final String fullPath) {
        this.fullPath = fullPath;
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
     * Gets the scaleName.
     * @return String
     */
    public String getScaleName() {
        return scaleName;
    }

    /**
     * Sets the scaleName.
     * @param scaleName The scaleName.
     */
    public void setScaleName(final String scaleName) {
        this.scaleName = scaleName;
    }
    
    /**
     * Gets the layerFormatName.
     * @return String
     */
    public String getLayerFormatName() {
        return layerFormatName;
    }

    /**
     * Sets the layerFormatName.
     * @param layerFormatName The layerFormatName.
     */
    public void setLayerFormatName(final String layerFormatName) {
        this.layerFormatName = layerFormatName;
    }
    
    /**
     * Gets the processes.
     * @return Integer
     */
    public Integer getProcesses() {
    	return processes == null || processes < 0 ? 0 : processes;
    }

    /**
     * Sets the processes.
     * @param processes The processes.
     */
    public void setProcesses(final Integer processes) {
    	this.processes = processes == null || processes < 0 ? 0 : processes;
    }
    
    
    /**
	 * Trims the object.
	 */
	public void trimObject() {
		uuid = uuid != null ? (uuid.trim().length() > 36 ? uuid.trim().substring(0, 36) : uuid.trim()) : null;
		name = name != null ? (name.trim().length() > 30 ? name.trim().substring(0, 30) : name.trim()) : null;
		fullPath = fullPath != null ? (fullPath.trim().length() > 240 ? fullPath.trim().substring(0, 240) : fullPath.trim()) : null;
		scaleName = scaleName != null ? (scaleName.trim().length() > 60 ? scaleName.trim().substring(0, 60) : scaleName.trim()) : null;
		layerFormatName = layerFormatName != null ? (layerFormatName.trim().length() > 30 ? layerFormatName.trim().substring(0, 30) : layerFormatName.trim()) : null;
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

        final LayerSimpleView vo = (LayerSimpleView) o;
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
    	StringBuffer buffer = new StringBuffer("LayerSimpleView {");
    	buffer.append("uuid=").append(getUuid());
    	buffer.append(", name=").append(getName());
    	buffer.append(", fullPath=").append(getFullPath());
    	buffer.append(", createdDate=").append(getCreatedDate());
    	buffer.append(", lastModifiedDate=").append(getLastModifiedDate());
    	buffer.append(", deletedDate=").append(getDeletedDate());
    	buffer.append(", scaleName=").append(getScaleName());
    	buffer.append(", layerFormatName=").append(getLayerFormatName());
    	buffer.append(", processes=").append(getProcesses()).append("}");
    	return buffer.toString();
    }
}
