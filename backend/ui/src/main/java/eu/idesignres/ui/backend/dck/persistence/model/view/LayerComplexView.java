package eu.idesignres.ui.backend.dck.persistence.model.view;

import java.io.Serializable;
import java.util.Objects;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;


/**
 * Model of a LayerComplexView object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "v21B_idesignres_layers_complex")
public class LayerComplexView implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = -426080594155501950L;
	
	
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
    
    /** The scaleUuid. */
	@Column(name = "scale_uuid")
	private String scaleUuid;
	
	/** The scaleName. */
    @Column(name = "scale_name")
    private String scaleName;
    
    /** The layerFormatUuid. */
	@Column(name = "layer_format_uuid")
	private String layerFormatUuid;
	
	/** The layerFormatName. */
    @Column(name = "layer_format_name")
    private String layerFormatName;
    
    /** The processUuid. */
	@Column(name = "process_uuid")
	private String processUuid;
	
	/** The processName. */
    @Column(name = "process_name")
    private String processName;
    
    /** The processDescription. */
    @Column(name = "process_description")
    private String processDescription;
    
    
    /**
     * Constructs a LayerComplexView.
     */
    public LayerComplexView() {
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
     * @param scaleUuid The scaleUuid.
     * @param scaleName The scaleName.
     * @param layerFormatUuid The layerFormatUuid.
     * @param layerFormatName The layerFormatName.
     * @param processUuid The processUuid.
     * @param processName The processName.
     * @param processDescription The processDescription.
     */
    public LayerComplexView(final String uuid, final String name, final String fullPath,
    		final Long createdDate, final Long lastModifiedDate, final Long deletedDate,
    		final String scaleUuid, final String scaleName, final String layerFormatUuid,
    		final String layerFormatName, final String processUuid, final String processName,
    		final String processDescription) {
    	super();
    	
    	this.uuid = uuid;
    	this.name = name;
    	this.fullPath = fullPath;
        this.createdDate = createdDate;
    	this.lastModifiedDate = lastModifiedDate;
    	this.deletedDate = deletedDate;
    	this.scaleUuid = scaleUuid;
    	this.scaleName = scaleName;
    	this.layerFormatUuid = layerFormatUuid;
    	this.layerFormatName = layerFormatName;
    	this.processUuid = processUuid;
    	this.processName = processName;
    	this.processDescription = processDescription;
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
     * Gets the scaleUuid.
     * @return String
     */
    public String getScaleUuid() {
        return scaleUuid;
    }

    /**
     * Sets the scaleUuid.
     * @param scaleUuid The scaleUuid.
     */
    public void setScaleUuid(final String scaleUuid) {
        this.scaleUuid = scaleUuid;
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
     * Gets the layerFormatUuid.
     * @return String
     */
    public String getLayerFormatUuid() {
        return layerFormatUuid;
    }

    /**
     * Sets the layerFormatUuid.
     * @param layerFormatUuid The layerFormatUuid.
     */
    public void setLayerFormatUuid(final String layerFormatUuid) {
        this.layerFormatUuid = layerFormatUuid;
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
     * Gets the processUuid.
     * @return String
     */
    public String getProcessUuid() {
        return processUuid;
    }

    /**
     * Sets the processUuid.
     * @param processUuid The processUuid.
     */
    public void setProcessUuid(final String processUuid) {
        this.processUuid = processUuid;
    }
    
    /**
     * Gets the processName.
     * @return String
     */
    public String getProcessName() {
        return processName;
    }

    /**
     * Sets the processName.
     * @param processName The processName.
     */
    public void setProcessName(final String processName) {
        this.processName = processName;
    }
    
    /**
     * Gets the processDescription.
     * @return String
     */
    public String getProcessDescription() {
        return processDescription;
    }

    /**
     * Sets the processDescription.
     * @param processDescription The processDescription.
     */
    public void setProcessDescription(final String processDescription) {
        this.processDescription = processDescription;
    }
    
    
    /**
	 * Trims the object.
	 */
	public void trimObject() {
		uuid = uuid != null ? (uuid.trim().length() > 36 ? uuid.trim().substring(0, 36) : uuid.trim()) : null;
		name = name != null ? (name.trim().length() > 30 ? name.trim().substring(0, 30) : name.trim()) : null;
		fullPath = fullPath != null ? (fullPath.trim().length() > 240 ? fullPath.trim().substring(0, 240) : fullPath.trim()) : null;
		scaleUuid = scaleUuid != null ? (scaleUuid.trim().length() > 36 ? scaleUuid.trim().substring(0, 36) : scaleUuid.trim()) : null;
		scaleName = scaleName != null ? (scaleName.trim().length() > 60 ? scaleName.trim().substring(0, 60) : scaleName.trim()) : null;
		layerFormatUuid = layerFormatUuid != null ? (layerFormatUuid.trim().length() > 36 ? layerFormatUuid.trim().substring(0, 36) : layerFormatUuid.trim()) : null;
		layerFormatName = layerFormatName != null ? (layerFormatName.trim().length() > 30 ? layerFormatName.trim().substring(0, 30) : layerFormatName.trim()) : null;
		processUuid = processUuid != null ? (processUuid.trim().length() > 36 ? processUuid.trim().substring(0, 36) : processUuid.trim()) : null;
		processName = processName != null ? (processName.trim().length() > 30 ? processName.trim().substring(0, 30) : processName.trim()) : null;
		processDescription = processDescription != null ? (processDescription.trim().length() > 150 ? processDescription.trim().substring(0, 150) : processDescription.trim()) : null;
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

        final LayerComplexView vo = (LayerComplexView) o;
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
    	StringBuffer buffer = new StringBuffer("LayerComplexView {");
    	buffer.append("uuid=").append(getUuid());
    	buffer.append(", name=").append(getName());
    	buffer.append(", fullPath=").append(getFullPath());
    	buffer.append(", createdDate=").append(getCreatedDate());
    	buffer.append(", lastModifiedDate=").append(getLastModifiedDate());
    	buffer.append(", deletedDate=").append(getDeletedDate());
    	buffer.append(", scaleUuid=").append(getScaleUuid());
    	buffer.append(", scaleName=").append(getScaleName());
    	buffer.append(", layerFormatUuid=").append(getLayerFormatUuid());
    	buffer.append(", layerFormatName=").append(getLayerFormatName());
    	buffer.append(", processUuid=").append(getProcessUuid());
    	buffer.append(", processName=").append(getProcessName());
    	buffer.append(", processDescription=").append(getProcessDescription()).append("}");
    	return buffer.toString();
    }
}
