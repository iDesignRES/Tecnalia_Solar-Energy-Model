package eu.idesignres.ui.backend.dck.persistence.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

import org.hibernate.annotations.GenericGenerator;

import eu.idesignres.ui.backend.dck.persistence.model.view.LayerFormatView;
import eu.idesignres.ui.backend.dck.persistence.model.view.ScaleView;


/**
 * Model of a Layer object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "t21_idesignres_layers",
	uniqueConstraints = {
			@UniqueConstraint(columnNames = {"name"})})
public class Layer implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 823806271002299032L;

	
	/** The uuid. */
	@Id
	@GeneratedValue(generator = "UUID")
	@GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
	@Size(max = 36)
	@Column(name = "uuid", length = 36, unique = true, updatable = false, nullable = false)
	private String uuid;
	
	/** The name. */
	@NotNull
	@Size(max = 80)
    @Column(name = "name", length = 80, nullable = false)
    private String name;
	
	/** The fullPath. */
	@NotNull
	@Size(max = 240)
	@Column(name = "full_path", length = 240, unique = true)
	private String fullPath;
	
	/** The scale. */
	@NotNull
	@Size(max = 36)
	@Column(name = "scale_fk", length = 36, unique = true)
	private String scale;
	
	/** The layerFormat. */
	@NotNull
	@Size(max = 36)
	@Column(name = "format_fk", length = 36, unique = true)
	private String layerFormat;
	
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
	
	/** The scales. */
	private transient List<ScaleView> scales;
	
	/** The formats. */
	private transient List<LayerFormatView> formats;
	
	/** The processes. */
	private transient List<Process> processes;
    
    
    /**
     * Constructs a Layer.
     */
    public Layer() {
    	super();
    }
    
    /**
     * Constructs a Layer.
     * @param uuid The uuid.
     * @param name The name.
     * @param fullPath The fullPath.
     * @param scale The scale.
     * @param layerFormat The layerFormat.
     * @param createdDate The createdDate.
     * @param lastModifiedDate The lastModifiedDate.
     * @param deletedDate The deletedDate.
     */
    public Layer(final String uuid, final String name, final String fullPath,
    		final String scale, final String layerFormat, final Long createdDate,
    		final Long lastModifiedDate, final Long deletedDate) {
    	super();
    	
    	this.uuid = uuid;
    	this.name = name;
    	this.fullPath = fullPath;
        this.scale = scale;
        this.layerFormat = layerFormat;
        this.createdDate = createdDate;
    	this.lastModifiedDate = lastModifiedDate;
    	this.deletedDate = deletedDate;
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
     * Gets the scale.
     * @return String
     */
    public String getScale() {
        return scale;
    }

    /**
     * Sets the scale.
     * @param scale The scale.
     */
    public void setScale(final String scale) {
        this.scale = scale;
    }
    
    /**
     * Gets the layerFormat.
     * @return String
     */
    public String getLayerFormat() {
        return layerFormat;
    }

    /**
     * Sets the layerFormat.
     * @param layerFormat The layerFormat.
     */
    public void setLayerFormat(final String layerFormat) {
        this.layerFormat = layerFormat;
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
     * Gets the scales.
     * @return List<ScaleView>
     */
    public List<ScaleView> getScales() {
        return scales != null ? scales : new ArrayList<ScaleView>();
    }

    /**
     * Sets the scales.
     * @param scales The scales.
     */
    public void setScales(final List<ScaleView> scales) {
        this.scales = scales != null ? scales : new ArrayList<ScaleView>();
    }
    
    /**
     * Gets the formats.
     * @return List<LayerFormatView>
     */
    public List<LayerFormatView> getFormats() {
        return formats != null ? formats : new ArrayList<LayerFormatView>();
    }

    /**
     * Sets the formats.
     * @param formats The formats.
     */
    public void setFormats(final List<LayerFormatView> formats) {
        this.formats = formats != null ? formats : new ArrayList<LayerFormatView>();
    }
    
    /**
     * Gets the processes.
     * @return List<Process>
     */
    public List<Process> getProcesses() {
        return processes != null ? processes : new ArrayList<Process>();
    }

    /**
     * Sets the processes.
     * @param processes The processes.
     */
    public void setProcesses(final List<Process> processes) {
        this.processes = processes != null ? processes : new ArrayList<Process>();
    }
    
    
    /**
	 * Trims the object.
	 */
	public void trimObject() {
		uuid = uuid != null ? (uuid.trim().length() > 36 ? uuid.trim().substring(0, 36) : uuid.trim()) : null;
		name = name != null ? (name.trim().length() > 80 ? name.trim().substring(0, 80) : name.trim()) : null;
		fullPath = fullPath != null ? (fullPath.trim().length() > 240 ? fullPath.trim().substring(0, 240) : fullPath.trim()) : null;
		scale = scale != null ? (scale.trim().length() > 36 ? scale.trim().substring(0, 36) : scale.trim()) : null;
		layerFormat = layerFormat != null ? (layerFormat.trim().length() > 36 ? layerFormat.trim().substring(0, 36) : layerFormat.trim()) : null;
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

        final Layer vo = (Layer) o;
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
    	StringBuffer buffer = new StringBuffer("Layer {");
    	buffer.append("uuid=").append(getUuid());
    	buffer.append(", name=").append(getName());
    	buffer.append(", fullPath=").append(getFullPath());
    	buffer.append(", scale=").append(getScale());
    	buffer.append(", layerFormat=").append(getScale());
    	buffer.append(", createdDate=").append(getCreatedDate());
    	buffer.append(", lastModifiedDate=").append(getLastModifiedDate());
    	buffer.append(", deletedDate=").append(getDeletedDate());
    	buffer.append(", processes=").append(getProcesses().size()).append("}");
    	return buffer.toString();
    }
}
