package eu.idesignres.ui.backend.dck.security.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import eu.idesignres.ui.backend.dck.constants.Security;
import eu.idesignres.ui.backend.dck.persistence.service.AppUserDetailsService;
import eu.idesignres.ui.backend.dck.security.jwt.JwtAuthenticationEntryPoint;
import eu.idesignres.ui.backend.dck.security.jwt.JwtAuthenticationFilter;


/**
 * Definition of the application security configuration.
 * @author Tecnalia
 * @version 1.0
 */
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class SecurityConfiguration extends WebSecurityConfigurerAdapter {
	
	/** Logger. **/
	private final Logger log = LoggerFactory.getLogger(SecurityConfiguration.class);
	
	/** The service which implements the Spring Security "UserDetailsService" interface. */
	@Autowired
    private AppUserDetailsService userDetailsService;
	
	/** The component to manage the authentication entry point. */
	@Autowired
    JwtAuthenticationEntryPoint jwtEntryPoint;
	
	
	/**
	 * Constructs the filter object bean.
	 * @return MedeaJwtAuthenticationFilter
	 */
	@Bean
    public JwtAuthenticationFilter jwtTokenFilter() {
        return new JwtAuthenticationFilter();
    }
	
	
	/**
	 * Constructs the BCrypt password encoder bean.
	 * @return PasswordEncoder
	 */
	@Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
	
	
	/*
	 * (non-Javadoc)
	 * @see org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter#authenticationManager()
	 */
	@Override
    protected AuthenticationManager authenticationManager() throws Exception {
        return super.authenticationManager();
    }
	
	
	/*
	 * (non-Javadoc)
	 * @see org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter#authenticationManagerBean()
	 */
	@Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }
	
	
	/**
	 * Constructs the CORS configuration source bean.
	 * @return CorsConfigurationSource
	 */
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        final UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", new CorsConfiguration().applyPermitDefaultValues());
        return source;
    }
    
    
    /*
     * (non-Javadoc)
     * @see org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter#configure(org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder)
     */
    @Override
    public void configure(AuthenticationManagerBuilder auth) throws Exception {
    	auth.userDetailsService(userDetailsService).passwordEncoder(passwordEncoder());
    }
    
    
    /*
     * (non-Javadoc)
     * @see org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter#configure(org.springframework.security.config.annotation.web.builders.HttpSecurity)
     */
    @Override
    protected void configure(HttpSecurity http) throws Exception {
    	log.info("SecurityConfig  ::  configure(HttpSecurity) :: Configuring the application security...");
    	
    	http.cors().and().csrf().disable()													// Disable CORS configuration and CSRF filter
    		.authorizeRequests()
    		.antMatchers(Security.SEC_URL_HELLO.getConstant()).permitAll()					// Allow access to /api/qgis-ui/hello/**
    		.antMatchers(Security.SEC_URL_ROLES.getConstant()).authenticated()				// Allow access to /api/qgis-ui/roles/**
    		.antMatchers(Security.SEC_URL_USERS.getConstant()).authenticated()				// Allow access to /api/qgis-ui/users/**
    		.antMatchers(Security.SEC_URL_SCALES.getConstant()).authenticated()				// Allow access to /api/qgis-ui/scales/**
    		.antMatchers(Security.SEC_URL_PROCESSES.getConstant()).authenticated()			// Allow access to /api/qgis-ui/processes/**
    		.antMatchers(Security.SEC_URL_LAYER_FORMATS.getConstant()).authenticated()		// Allow access to /api/qgis-ui/layer-formats/**
    		.antMatchers(Security.SEC_URL_LAYERS.getConstant()).authenticated()				// Allow access to /api/qgis-ui/layers/**
    		.antMatchers(Security.SEC_URL_RESOURCES.getConstant()).permitAll()				// Allow access to /resources/**
	        .antMatchers(Security.SEC_URL_FAVICON.getConstant()).permitAll()				// Allow access to /favicon.ico
	        .and()
	        .exceptionHandling().authenticationEntryPoint(jwtEntryPoint)
	        .and()
	        .addFilterBefore(jwtTokenFilter(), UsernamePasswordAuthenticationFilter.class)	// Add authentication filter
	        .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);	// Disable cookies
    }
}
