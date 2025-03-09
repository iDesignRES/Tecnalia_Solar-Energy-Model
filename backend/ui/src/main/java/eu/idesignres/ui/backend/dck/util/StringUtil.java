package eu.idesignres.ui.backend.dck.util;

import java.util.Date;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import eu.idesignres.ui.backend.dck.constants.Strings;


/**
 * Utilities to manage strings.
 * @author Tecnalia
 * @version 1.0
 */
public final class StringUtil {

	/**
	 * Generates a random UUID.
	 * @return String
	 */
	public static String generateUuid() {
		return UUID.randomUUID().toString();
	}
	
	
	/**
	 * Checks if a String is null or empty.
	 * @param sourceString The source string.
	 * @return boolean
	 */
	public static boolean isNullOrEmpty(final String sourceString) {
		return sourceString == null || sourceString.trim().length() == 0 || sourceString.trim().equalsIgnoreCase(Strings.STR_NULL.getConstant());
	}
	
	
	/**
	 * Extracts the String between double quotes.
	 * @param sourceString The source string.
	 * @return String
	 */
	public static String extractStringBetweenDoubleQuotes(final String sourceString) {
		if (!isNullOrEmpty(sourceString)) {
			final Pattern pattern = Pattern.compile("\"([^\"]*)\"");
			final Matcher matcher = pattern.matcher(sourceString);
			StringBuffer result = new StringBuffer("");
			while (matcher.find()) {
				result.append(matcher.group(0).replace("\"", "").trim()).append(",");
			}
			return result.toString().substring(0, result.toString().length() - 1);
		}
		return null;
	}
	
	
	/**
	 * Creates an Instance name.
	 * @param honeypotCode The honeypotCode
	 * @return String
	 */
	public static String createInstanceName(final String honeypotCode) {
		return honeypotCode + Strings.STR_UNDERSCORE.getConstant() + new Date().getTime();
	}
}