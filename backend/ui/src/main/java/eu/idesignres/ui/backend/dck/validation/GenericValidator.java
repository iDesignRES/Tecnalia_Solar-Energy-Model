package eu.idesignres.ui.backend.dck.validation;

import java.util.Locale;

import org.springframework.context.support.ResourceBundleMessageSource;

import eu.idesignres.ui.backend.dck.constants.Application;


/**
 * Generic validator.
 * @author Tecnalia
 * @version 1.0
 */
public abstract class GenericValidator {
	
	/** The locale. */
	protected Locale locale;
	
	/** The messageSource. */
	protected ResourceBundleMessageSource messageSource;
	
	
	/**
	 * Constructs a GenericValidator.
	 * @param locale The locale.
	 */
	protected GenericValidator(final Locale locale) {
		this.locale = locale;
		
		messageSource = new ResourceBundleMessageSource();
		messageSource.setDefaultEncoding(Application.APP_MESSAGES_ENCODING.getConstant());
		messageSource.setBasename(Application.APP_MESSAGES_BASENAME.getConstant());
	}
	
	
	/**
	 * Validates an object.
	 * @param object The object.
	 * @param checkUuid The checkUuid.
	 * @param remove The remove.
	 * @return String
	 */
	protected abstract String validate(final Object object, final Boolean checkUuid, final Boolean remove);
}