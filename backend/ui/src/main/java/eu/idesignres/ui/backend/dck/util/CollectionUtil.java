package eu.idesignres.ui.backend.dck.util;

import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Set;

import eu.idesignres.ui.backend.dck.constants.Strings;


/**
 * Utilities to manage collections.
 * @author Tecnalia
 * @version 1.0
 */
public final class CollectionUtil {

	/**
	 * Checks if an array is null or empty.
	 * @param sourceArray The source array.
	 * @return boolean
	 */
	public static boolean isNullOrEmpty(final Object[] sourceArray) {
		return sourceArray == null || sourceArray.length == 0;
	}
	
	
	/**
	 * Checks if a List is null or empty.
	 * @param sourceList The source list.
	 * @return boolean
	 */
	public static boolean isNullOrEmpty(final List<?> sourceList) {
		return sourceList == null || sourceList.isEmpty();
	}
	
	
	/**
	 * Checks if a Map is null or empty.
	 * @param sourceMap The source map.
	 * @return boolean
	 */
	public static boolean isNullOrEmpty(final Map<?, ?> sourceMap) {
		return sourceMap == null || sourceMap.isEmpty();
	}
	
	
	/**
	 * Checks if a Set is null or empty.
	 * @param sourceSet The source set.
	 * @return boolean
	 */
	public static boolean isNullOrEmpty(final Set<?> sourceSet) {
		return sourceSet == null || sourceSet.isEmpty();
	}
	
	
	/**
	 * Checks if a Collection is null or empty.
	 * @param sourceSet The source set.
	 * @return boolean
	 */
	public static boolean isNullOrEmpty(final Collection<?> sourceCollection) {
		return sourceCollection == null || sourceCollection.isEmpty();
	}
	
	
	/**
	 * Converts a string list to an unique string.
	 * @param sourceList The sourceList.
	 * @param separator The separator.
	 * @return String
	 */
	public static String convertStringListToString(final List<String> sourceList, final String separator) {
		StringBuffer result = new StringBuffer(Strings.STR_BLANK.getConstant());
		if (!CollectionUtil.isNullOrEmpty(sourceList)) {
			final int len = sourceList.size();
			for (int i = 0;i < len;i++) {
				if (i > 0) {
					result.append(separator);
				}
				result.append(sourceList.get(i));
			}
		}
		return result.toString();
	}
}