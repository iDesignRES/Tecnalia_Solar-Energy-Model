package eu.idesignres.ui.backend.dck.validation;

import java.util.Locale;

import eu.idesignres.ui.backend.dck.persistence.model.Process;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * Process object validator.
 * @author Tecnalia
 * @version 1.0
 */
public final class ProcessValidator extends GenericValidator {
	
	/** The instance. */
	private static ProcessValidator instance;
	
	
	/**
	 * Constructs a ProcessValidator.
	 * @param locale The locale.
	 */
	private ProcessValidator(final Locale locale) {
		super(locale);
	}
	
	
	/**
	 * Obtains an instance.
	 * @param locale The locale.
	 * @return ProcessValidator
	 */
	public static ProcessValidator getInstance(final Locale locale) {
        if (instance == null) {
            instance = new ProcessValidator(locale);
        }
        return instance;
    }
	
	
	/**
	 * Validates the object.
	 * @param object The object.
	 * @param checkUuid The checkUuid.
	 * @param remove The remove.
	 * @return String
	 */
	public String validate(final Object object, final Boolean checkUuid, final Boolean remove) {
		// Cast object
		Process process = Process.class.cast(object);
		
		// Check the object
		if (process == null) {
			return messageSource.getMessage("validation.generic.object", null, locale);
		}
		
		process.trimObject();
		
		// Check the Process.uuid
		if (checkUuid && StringUtil.isNullOrEmpty(process.getUuid())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Process.uuid");
		}
				
		// Check the Process.name
		if (StringUtil.isNullOrEmpty(process.getName())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Process.name");
		}
		
		// Check the Process.createdDate
		if (checkUuid && process.getCreatedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Process.createdDate");
		}
		
		// Check the Process.lastModifiedDate
		if (checkUuid && process.getLastModifiedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Process.lastModifiedDate");
		}
		
		return null;
	}
}