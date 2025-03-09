package eu.idesignres.ui.backend.dck.util;

import java.util.regex.Matcher;
import java.util.regex.Pattern;


/**
 * Utilities to manage net issues.
 * @author Tecnalia
 * @version 1.0
 */
public final class NetUtil {

	/**
	 * Validates an email address.
	 * @param email The email.
	 * @return Boolean
	 */
	public static Boolean validateEmailAddress(final String email) {
		final Pattern pattern = Pattern.compile("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,6}$", Pattern.CASE_INSENSITIVE);
		final Matcher matcher = pattern.matcher(email);
		return matcher.find();
	}
}