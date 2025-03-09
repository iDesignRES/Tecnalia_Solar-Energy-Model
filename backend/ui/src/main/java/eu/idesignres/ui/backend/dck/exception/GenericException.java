package eu.idesignres.ui.backend.dck.exception;

/**
 * The application generic exception.
 * @author Tecnalia
 * @version 1.0
 */
public abstract class GenericException extends Exception {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = 5410625131433531257L;
	
	/** The category. */
	protected String category;
	
	/** The subcategory. */
	protected String subcategory;

	
	/**
	 * Constructor.
	 * @param category The category.
	 * @param subcategory The subcategory.
	 * @param message The message.
	 */
	protected GenericException(final String category, final String subcategory, final String message) {
        super(message);
        
        this.category = category;
        this.subcategory = subcategory;
    }
	
	
    /**
     * Gets the category.
     * @return String
     */
    public String getCategory() {
        return category;
    }
    
    /**
     * Sets the category.
     * @param category The category.
     */
    public void setCategory(final String category) {
    	this.category = category;
    }
    
    /**
     * Gets the subcategory.
     * @return String
     */
    public String getSubcategory() {
        return subcategory;
    }
    
    /**
     * Sets the subcategory.
     * @param subcategory The subcategory.
     */
    public void setSubcategory(final String subcategory) {
    	this.subcategory = subcategory;
    }
    
    /**
     * Gets the full message.
     * @return String
     */
    public String getFullMessage() {
    	return category + "  ::  " + subcategory + "  ::  " + super.getMessage();
    }
}