package eu.idesignres.ui.backend.dck.util;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import eu.idesignres.ui.backend.dck.constants.Application;


/**
 * Utilities to manage dates.
 * @author Tecnalia
 * @version 1.0
 */
public final class DateUtil {

	/**
	 * Obtains the current timestamp.
	 * @return Long
	 */
	public static Long getCurrentTimestamp() {
		return new Date().getTime();
	}
	
	
	/**
	 * Obtains the current timestamp (short format).
	 * @return Long
	 */
	public static Long getCurrentShortTimestamp() {
		return (new Date().getTime()) / 1000L;
	}
	
	
	/**
	 * Builds a formatted date from timestamp.
	 * @param timestamp The timestamp.
	 * @param locale The locale.
	 * @return String
	 */
	public static String buildFormattedDateFromTimestamp(final Long timestamp, final Locale locale) {
		if (timestamp != null && locale != null) {
			SimpleDateFormat formatter = null;
			if (locale.toLanguageTag().equals(Application.APP_LOCALE_ES.getConstant())) {
				formatter = new SimpleDateFormat(Application.APP_ES_DATETIME_MASK.getConstant());
				return formatter.format(new Date(timestamp.longValue()));
			} else if (locale.toLanguageTag().equals(Application.APP_LOCALE_EN.getConstant())) {
				formatter = new SimpleDateFormat(Application.APP_EN_DATETIME_MASK.getConstant());
				return formatter.format(new Date(timestamp.longValue()));
			}
		}
		return null;
	}
}