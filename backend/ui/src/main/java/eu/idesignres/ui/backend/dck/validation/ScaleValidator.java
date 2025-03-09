package eu.idesignres.ui.backend.dck.validation;

import java.util.Locale;

import eu.idesignres.ui.backend.dck.persistence.model.Scale;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * Scale object validator.
 * @author Tecnalia
 * @version 1.0
 */
public final class ScaleValidator extends GenericValidator {
	
	/** The instance. */
	private static ScaleValidator instance;
	
	
	/**
	 * Constructs a ScaleValidator.
	 * @param locale The locale.
	 */
	private ScaleValidator(final Locale locale) {
		super(locale);
	}
	
	
	/**
	 * Obtains an instance.
	 * @param locale The locale.
	 * @return LayerFormatValidator
	 */
	public static ScaleValidator getInstance(final Locale locale) {
        if (instance == null) {
            instance = new ScaleValidator(locale);
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
		Scale scale = Scale.class.cast(object);
		
		// Check the object
		if (scale == null) {
			return messageSource.getMessage("validation.generic.object", null, locale);
		}
		
		scale.trimObject();
		
		// Check the Scale.uuid
		if (checkUuid && StringUtil.isNullOrEmpty(scale.getUuid())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Scale.uuid");
		}
				
		// Check the Scale.name
		if (StringUtil.isNullOrEmpty(scale.getName())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Scale.name");
		}
		
		// Check the Scale.createdDate
		if (checkUuid && scale.getCreatedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Scale.createdDate");
		}
		
		// Check the Scale.lastModifiedDate
		if (checkUuid && scale.getLastModifiedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Scale.lastModifiedDate");
		}
		
		return null;
	}
}