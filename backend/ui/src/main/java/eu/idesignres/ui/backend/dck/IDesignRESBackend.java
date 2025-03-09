package eu.idesignres.ui.backend.dck;

import java.util.Locale;
import java.util.TimeZone;

import javax.annotation.PostConstruct;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.support.ResourceBundleMessageSource;
import org.springframework.web.servlet.LocaleResolver;
import org.springframework.web.servlet.i18n.SessionLocaleResolver;

import eu.idesignres.ui.backend.dck.constants.Application;


/**
 * Application starter.
 * @author Tecnalia
 * @version 1.0
 */
@SpringBootApplication
public class IDesignRESBackend {
	
	/** The default localeTag. */
	@Value( "${app.default.locale.tag}" )
	private String localeTag;
	
	/** Logger. */
	private static final Logger log = LoggerFactory.getLogger(IDesignRESBackend.class);
	
	
	/**
	 * Inits the time zone.
	 */
	@PostConstruct
	void init() {
		TimeZone.setDefault(TimeZone.getTimeZone(Application.APP_DATETIME_UTC.getConstant()));
	}
	
	
	/**
	 * Creates the LocaleResolver object.
	 * @return LocaleResolver
	 */
	@Bean  
	public LocaleResolver localeResolver() {
		SessionLocaleResolver localeResolver = new SessionLocaleResolver();
		localeResolver.setDefaultLocale(Locale.forLanguageTag(localeTag));
		return localeResolver;
	}
	

	/**
	 * Configures the ResourceBundle.
	 * @return ResourceBundleMessageSource
	 */
	@Bean
	public ResourceBundleMessageSource bundleMessageSource() {
		ResourceBundleMessageSource messageSource = new ResourceBundleMessageSource();
		messageSource.setDefaultEncoding(Application.APP_MESSAGES_ENCODING.getConstant());
		messageSource.setBasename(Application.APP_MESSAGES_BASENAME.getConstant());
		return messageSource;
	}
	
	
	/*
	 * Main method (start).
	 */
	public static void main(String[] args) {
		SpringApplication.run(IDesignRESBackend.class, args);
		log.info("IDesignRES UI-Backend started!");
	}
}
