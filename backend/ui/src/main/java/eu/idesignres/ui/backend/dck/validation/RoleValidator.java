package eu.idesignres.ui.backend.dck.validation;

import java.util.Locale;

import eu.idesignres.ui.backend.dck.persistence.model.Role;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * Role object validator.
 * @author Tecnalia
 * @version 1.0
 */
public final class RoleValidator extends GenericValidator {
	
	/** The instance. */
	private static RoleValidator instance;
	
	
	/**
	 * Constructs a RoleValidator.
	 * @param locale The locale.
	 */
	private RoleValidator(final Locale locale) {
		super(locale);
	}
	
	
	/**
	 * Obtains an instance.
	 * @param locale The locale.
	 * @return RoleValidator
	 */
	public static RoleValidator getInstance(final Locale locale) {
        if (instance == null) {
            instance = new RoleValidator(locale);
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
		Role role = Role.class.cast(object);
		
		// Check the object
		if (role == null) {
			return messageSource.getMessage("validation.generic.object", null, locale);
		}
		
		role.trimObject();
		
		// Check the Role.name
		if (StringUtil.isNullOrEmpty(role.getName())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Role.name");
		}
		
		// Check the Role.description attribute
		if (StringUtil.isNullOrEmpty(role.getDescription())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Role.description");
		}
		
		// Check the Role.uuid
		if (checkUuid && StringUtil.isNullOrEmpty(role.getUuid())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Role.uuid");
		}
		
		// Check the Role.createdDate
		if (checkUuid && role.getCreatedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Role.createdDate");
		}
		
		// Check the Role.lastModifiedDate
		if (checkUuid && role.getLastModifiedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "Role.lastModifiedDate");
		}
		
		return null;
	}
}