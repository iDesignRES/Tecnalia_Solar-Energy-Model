package eu.idesignres.ui.backend.dck.security.jwt;

import java.io.IOException;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import eu.idesignres.ui.backend.dck.constants.Security;
import eu.idesignres.ui.backend.dck.constants.Strings;
import eu.idesignres.ui.backend.dck.persistence.service.AppUserDetailsService;


/**
 * Filter to intercept the required authentication.
 * @author Tecnalia
 * @version 1.0
 */
public class JwtAuthenticationFilter extends OncePerRequestFilter {

	/** Logger. */
	private final Logger log = LoggerFactory.getLogger(JwtAuthenticationFilter.class);
	
	/** The "token provider" component. */
	@Autowired
    private JwtTokenProvider tokenProvider;

	/** The service which implements the Spring Security "UserDetailsService" interface. */
    @Autowired
    private AppUserDetailsService userDetailsService;
    
    
    /*
     * (non-Javadoc)
     * @see org.springframework.web.filter.OncePerRequestFilter#doFilterInternal(javax.servlet.http.HttpServletRequest, javax.servlet.http.HttpServletResponse, javax.servlet.FilterChain)
     */
    @Override
    protected void doFilterInternal(final HttpServletRequest request, final HttpServletResponse response,
    		final FilterChain filterChain) throws ServletException, IOException {
        try {
        	log.info("JwtAuthenticationFilter  ::  doFilterInternal(HttpServletRequest, HttpServletResponse, FilterChain) :: getting the JWT token...");
            final String token = getToken(request);
            
            if (StringUtils.hasText(token) && tokenProvider.validateToken(token)) {
            	log.info("JwtAuthenticationFilter  ::  doFilterInternal(HttpServletRequest, HttpServletResponse, FilterChain) :: the JWT token is validated!");
            	
                final UserDetails userDetails = userDetailsService.loadUserByUsername(tokenProvider.getCredentialsFromJWT(token));
                log.info("JwtAuthenticationFilter  ::  doFilterInternal(HttpServletRequest, HttpServletResponse, FilterChain) :: user details loaded!");
                
                UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        } catch (Exception e) {
        	log.error("JwtAuthenticationFilter  ::  doFilterInternal(HttpServletRequest, HttpServletResponse, FilterChain) ::  ERROR  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
        }
        
        log.info("JwtAuthenticationFilter  ::  doFilterInternal(HttpServletRequest, HttpServletResponse, FilterChain) :: filtering...");
        filterChain.doFilter(request, response);
    }

    
    /**
     * Gets the JWT token.
     * @param request The request.
     * @return String
     */
    private String getToken(final HttpServletRequest request) {
        final String bearerToken = request.getHeader(Security.SEC_AUTHORIZATION.getConstant());
        if (bearerToken != null && bearerToken.startsWith(Security.SEC_BEARER.getConstant())) {
            return bearerToken.replace(Security.SEC_BEARER.getConstant(), Strings.STR_BLANK.getConstant());
        }
        return null;
    }
}
