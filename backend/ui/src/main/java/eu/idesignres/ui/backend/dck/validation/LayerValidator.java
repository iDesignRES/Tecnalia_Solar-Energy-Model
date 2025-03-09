package eu.idesignres.ui.backend.dck.validation;

import java.util.Locale;

import eu.idesignres.ui.backend.dck.persistence.model.Layer;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * Layer object validator.
 * @author Tecnalia
 * @version 1.0
 */
public final class LayerValidator extends GenericValidator {
	
	/** The instance. */
	private static LayerValidator instance;
	
	
	/**
	 * Constructs a LayerValidator.
	 * @param locale The locale.
	 */
	private LayerValidator(final Locale locale) {
		super(locale);
	}
	
	
	/**
	 * Obtains an instance.
	 * @param locale The locale.
	 * @return LayerValidator
	 */
	public static LayerValidator getInstance(final Locale locale) {
        if (instance == null) {
            instance = new LayerValidator(locale);
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
		Layer layer = Layer.class.cast(object);
		
		// Check the object
		if (layer == null) {
			return messageSource.getMessage("validation.generic.object", null, locale);
		}
		
		layer.trimObject();
		
		// Check the Layer.uuid
		if (checkUuid && StringUtil.isNullOrEmpty(layer.getUuid())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Layer.uuid");
		}
				
		// Check the Layer.name
		if (StringUtil.isNullOrEmpty(layer.getName())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Layer.name");
		}
		
		// Check the Layer.scale
		if (!checkUuid && StringUtil.isNullOrEmpty(layer.getScale())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Layer.scale");
		}
		
		// Check the Layer.layerFormat
		if (!checkUuid && StringUtil.isNullOrEmpty(layer.getLayerFormat())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Layer.layerFormat");
		}
		
		// Check the Layer.createdDate
		if (checkUuid && layer.getCreatedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Layer.createdDate");
		}
		
		return null;
	}
}