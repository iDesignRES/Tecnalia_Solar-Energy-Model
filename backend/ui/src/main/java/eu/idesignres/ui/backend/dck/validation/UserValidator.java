package eu.idesignres.ui.backend.dck.validation;

import java.util.Locale;

import eu.idesignres.ui.backend.dck.constants.Strings;
import eu.idesignres.ui.backend.dck.persistence.model.User;
import eu.idesignres.ui.backend.dck.util.NetUtil;
import eu.idesignres.ui.backend.dck.util.StringUtil;


/**
 * User object validator.
 * @author Tecnalia
 * @version 1.0
 */
public final class UserValidator extends GenericValidator {
	
	/** The instance. */
	private static UserValidator instance;
	
	
	/**
	 * Constructs an UserValidator.
	 * @param locale The locale.
	 */
	private UserValidator(final Locale locale) {
		super(locale);
	}
	
	
	/**
	 * Obtains an instance.
	 * @param locale The locale.
	 * @return UserValidator
	 */
	public static UserValidator getInstance(final Locale locale) {
        if (instance == null) {
            instance = new UserValidator(locale);
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
		User user = User.class.cast(object);
		
		// Check the object
		if (user == null) {
			return messageSource.getMessage("validation.generic.object", null, locale);
		}
		
		user.trimObject();
		
		// Check the User.uuid
		if (checkUuid && StringUtil.isNullOrEmpty(user.getUuid())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "User.uuid");
		}
		
		// Check the User.username
		if (StringUtil.isNullOrEmpty(user.getUsername())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "User.username");
		}
		for (int i = 0;i < user.getUsername().length();i++) {
			if (Strings.STR_FORBIDDEN.getConstant().indexOf(user.getUsername().charAt(i)) != -1) {
				return messageSource.getMessage("validation.generic.forbidden.characters", null, locale)
						.replace("{1}", Strings.STR_FORBIDDEN.getConstant());
			}
		}
		
		// Check the User.password
		if (!checkUuid && !remove) {
			if (StringUtil.isNullOrEmpty(user.getPassword())) {
				return messageSource.getMessage("validation.generic.attribute", null, locale)
						.replace("{1}", "User.password");
			}
			for (int i = 0;i < user.getPassword().length();i++) {
				if (Strings.STR_FORBIDDEN.getConstant().indexOf(user.getPassword().charAt(i)) != -1) {
					return messageSource.getMessage("validation.generic.forbidden.characters", null, locale)
							.replace("{1}", Strings.STR_FORBIDDEN.getConstant());
				}
			}
		}
		
		// Check the User.repeatPassword
		if (!checkUuid && !remove && StringUtil.isNullOrEmpty(user.getRepeatPassword())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "User.repeatPassword");
		}
		if (!checkUuid &&!remove && !user.getPassword().equals(user.getRepeatPassword())) {
			return messageSource.getMessage("rest.user.add.update.different.passwords.400", null, locale);
		}
		
		// Check the User.email
		if (StringUtil.isNullOrEmpty(user.getEmail())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "User.email");
		}
		if (!NetUtil.validateEmailAddress(user.getEmail())) {
			return messageSource.getMessage("validation.generic.invalid", null, locale)
					.replace("{1}", "User.email")
					.replace("{2}", user.getEmail());
		}
		
		// Check the User.role
		if (!remove && StringUtil.isNullOrEmpty(user.getRole())) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "User.role");
		}
		
		// Check the User.createdDate
		if (checkUuid && user.getCreatedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "User.createdDate");
		}
		
		// Check the User.lastModifiedDate
		if (checkUuid && user.getLastModifiedDate() == null) {
			return messageSource.getMessage("validation.generic.attribute", null, locale)
					.replace("{1}", "User.lastModifiedDate");
		}
		
		return null;
	}
}