package eu.idesignres.ui.backend.dck.validation;

import java.util.Locale;

import eu.idesignres.ui.backend.dck.persistence.model.LayerFormat;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * LayerFormat object validator.
 * @author Tecnalia
 * @version 1.0
 */
public final class LayerFormatValidator extends GenericValidator {
	
	/** The instance. */
	private static LayerFormatValidator instance;
	
	
	/**
	 * Constructs a LayerFormatValidator.
	 * @param locale The locale.
	 */
	private LayerFormatValidator(final Locale locale) {
		super(locale);
	}
	
	
	/**
	 * Obtains an instance.
	 * @param locale The locale.
	 * @return LayerFormatValidator
	 */
	public static LayerFormatValidator getInstance(final Locale locale) {
        if (instance == null) {
            instance = new LayerFormatValidator(locale);
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
		LayerFormat layerFormat = LayerFormat.class.cast(object);
		
		// Check the object
		if (layerFormat == null) {
			return messageSource.getMessage("validation.generic.object", null, locale);
		}
		
		layerFormat.trimObject();
		
		// Check the LayerFormat.uuid
		if (checkUuid && StringUtil.isNullOrEmpty(layerFormat.getUuid())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "LayerFormat.uuid");
		}
				
		// Check the LayerFormat.name
		if (StringUtil.isNullOrEmpty(layerFormat.getName())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "LayerFormat.name");
		}
		
		// Check the LayerFormat.extension attribute
		if (StringUtil.isNullOrEmpty(layerFormat.getExtension())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "LayerFormat.extension");
		}
		
		// Check the LayerFormat.createdDate
		if (checkUuid && layerFormat.getCreatedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "LayerFormat.createdDate");
		}
		
		// Check the LayerFormat.lastModifiedDate
		if (checkUuid && layerFormat.getLastModifiedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "LayerFormat.lastModifiedDate");
		}
		
		return null;
	}
}