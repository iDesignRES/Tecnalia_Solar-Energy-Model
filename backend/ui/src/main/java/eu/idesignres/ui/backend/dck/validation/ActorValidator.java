package eu.idesignres.ui.backend.dck.validation;

import java.util.Locale;

import eu.idesignres.ui.backend.dck.persistence.model.Actor;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * Actor object validator.
 * @author Tecnalia
 * @version 1.0
 */
public final class ActorValidator extends GenericValidator {
	
	/** The instance. */
	private static ActorValidator instance;
	
	
	/**
	 * Constructs an ActorValidator.
	 * @param locale The locale.
	 */
	private ActorValidator(final Locale locale) {
		super(locale);
	}
	
	
	/**
	 * Obtains an instance.
	 * @param locale The locale.
	 * @return ActorValidator
	 */
	public static ActorValidator getInstance(final Locale locale) {
        if (instance == null) {
            instance = new ActorValidator(locale);
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
		Actor actor = Actor.class.cast(object);
		
		// Check the object
		if (actor == null) {
			return messageSource.getMessage("validation.generic.object", null, locale);
		}
		
		actor.trimObject();
		
		// Check the Actor.username
		if (StringUtil.isNullOrEmpty(actor.getUsername())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Actor.username");
		}
		
		// Check the Actor.role attribute
		if (StringUtil.isNullOrEmpty(actor.getRole())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Actor.role");
		}
		
		return null;
	}
}