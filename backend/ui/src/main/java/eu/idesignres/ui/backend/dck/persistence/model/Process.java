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

import eu.idesignres.ui.backend.dck.persistence.model.view.LayerComplexView;


/**
 * Model of a Process object.
 * @author Tecnalia
 * @version 1.0
 */
@Entity
@Table(name = "t03_idesignres_processes",
	uniqueConstraints = {
			@UniqueConstraint(columnNames = {"name"})})
public class Process implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 8757455177529502203L;

	
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
	
	/** The description. */
	@Size(max = 150)
    @Column(name = "description", length = 150, nullable = true)
    private String description;
	
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
	private transient List<LayerComplexView> layers;
	
	/** The results. */
	private transient List<String> results;
    
    
    /**
     * Constructs a Process.
     */
    public Process() {
    	super();
    	
    	layers = new ArrayList<LayerComplexView>();
    	results = new ArrayList<String>();
    }
    
    /**
     * Constructs a Process.
     * @param uuid The uuid.
     * @param name The name.
     */
    public Process(final String uuid, final String name) {
    	super();
    	
    	this.uuid = uuid;
    	this.name = name;
    	
    	layers = new ArrayList<LayerComplexView>();
    	results = new ArrayList<String>();
    }
    
    /**
     * Constructs a Process.
     * @param uuid The uuid.
     * @param name The name.
     * @param description The description.
     * @param createdDate The createdDate.
     * @param lastModifiedDate The lastModifiedDate.
     * @param deletedDate The deletedDate.
     */
    public Process(final String uuid, final String name, final String description,
    		final Long createdDate, final Long lastModifiedDate, final Long deletedDate) {
    	super();
    	
    	this.uuid = uuid;
    	this.name = name;
    	this.description = description;
        this.createdDate = createdDate;
    	this.lastModifiedDate = lastModifiedDate;
    	this.deletedDate = deletedDate;
    	
    	layers = new ArrayList<LayerComplexView>();
    	results = new ArrayList<String>();
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
     * @return List<LayerComplexView>
     */
    public List<LayerComplexView> getLayers() {
        return layers != null ? layers : new ArrayList<LayerComplexView>();
    }

    /**
     * Sets the layers.
     * @param layers The layers.
     */
    public void setLayers(final List<LayerComplexView> layers) {
        this.layers = layers != null ? layers : new ArrayList<LayerComplexView>();
    }
    
    /**
     * Gets the results.
     * @return List<String>
     */
    public List<String> getResults() {
        return results != null ? results : new ArrayList<String>();
    }

    /**
     * Sets the results.
     * @param results The results.
     */
    public void setResults(final List<String> results) {
        this.results = results != null ? results : new ArrayList<String>();
    }
    
    
    /**
	 * Trims the object.
	 */
	public void trimObject() {
		uuid = uuid != null ? (uuid.trim().length() > 36 ? uuid.trim().substring(0, 36) : uuid.trim()) : null;
		name = name != null ? (name.trim().length() > 30 ? name.trim().substring(0, 30) : name.trim()) : null;
		description = description != null ? (description.trim().length() > 150 ? description.trim().substring(0, 150) : description.trim()) : null;
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

        final Process vo = (Process) o;
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
    	StringBuffer buffer = new StringBuffer("Process {");
    	buffer.append("uuid=").append(getUuid());
    	buffer.append(", name=").append(getName());
    	buffer.append(", description=").append(getDescription());
    	buffer.append(", createdDate=").append(getCreatedDate());
    	buffer.append(", lastModifiedDate=").append(getLastModifiedDate());
    	buffer.append(", deletedDate=").append(getDeletedDate());
    	buffer.append(", layers=").append(getLayers().size());
    	buffer.append(", results=").append(getResults().size()).append("}");
    	return buffer.toString();
    }
}
