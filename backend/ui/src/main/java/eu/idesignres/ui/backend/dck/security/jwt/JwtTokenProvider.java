package eu.idesignres.ui.backend.dck.security.jwt;

import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Component;

import eu.idesignres.ui.backend.dck.constants.Security;
import eu.idesignres.ui.backend.dck.security.dto.CredentialsBuilderDTO;
import eu.idesignres.ui.backend.dck.security.dto.CredentialsDTO;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.MalformedJwtException;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.SignatureException;
import io.jsonwebtoken.UnsupportedJwtException;


/**
 * Component to define the JWT token provider.
 * @author Tecnalia
 * @version 1.0
 */
@Component
public class JwtTokenProvider {

	/** Logger. */
	private final Logger log = LoggerFactory.getLogger(JwtTokenProvider.class);
	
	/** The JWT secret key. */
	@Value("${jwt.secret}")
    private String jwtSecret;

	/** The JWT token expiration value (in ms). */
    @Value("${jwt.expiration}")
    private int jwtExpirationInMs;
    
    
    /**
     * Generates the JWT token.
     * @param authentication The authentication object.
     * @return String
     */
    public String generateJWTToken(final Authentication authentication) {
    	log.info("JwtTokenProvider  ::  generateJWTToken(Authentication) :: obtaining credentials from Authentication object...");
    	final CredentialsBuilderDTO credential = (CredentialsBuilderDTO) authentication.getPrincipal();
    	
    	log.info("JwtTokenProvider  ::  generateJWTToken(Authentication) :: calculating dates...");
        final Date now = new Date();
        final Date expireDate = new Date(now.getTime() + jwtExpirationInMs);

        log.info("JwtTokenProvider  ::  generateJWTToken(Authentication) :: generating and returning JWT token...");
        return Jwts.builder()
                .setSubject(credential.getUsername())
                .setIssuedAt(new Date())
                .setExpiration(expireDate)
                .claim(Security.SEC_JWT_CLAIM_IDENTIFIER.getConstant(), credential.getUuid())
                .claim(Security.SEC_JWT_CLAIM_ROLE.getConstant(), ((GrantedAuthority) credential.getAuthorities().toArray()[0]).getAuthority())
                .claim(Security.SEC_JWT_CLAIM_EMAIL.getConstant(), credential.getEmail())
                .signWith(SignatureAlgorithm.HS512, jwtSecret.getBytes())
                .compact();
    }

    
    /**
     * Extracts the credentials from a JWT token.
     * @param token The JWT token.
     * @return String
     */
    public String getCredentialsFromJWT(final String token) {
    	log.info("JwtTokenProvider  ::  getCredentialFromJWT(String) :: obtaining credentials from the JWT token...");
        Claims claims = Jwts.parser()
                .setSigningKey(Security.SEC_SECRET.getConstant().getBytes())
                .parseClaimsJws(token)
                .getBody();
        return claims.getSubject();
    }
    
    
    /**
     * Extracts the full credentials from a JWT token.
     * @param token The JWT token.
     * @return CredentialsDTO
     */
    public CredentialsDTO getFullCredentialsFromJWT(final String token) {
    	log.info("JwtTokenProvider  ::  getFullCredentialsFromJWT(String) :: Obtaining full credentials from the JWT token...");
        final Claims claims = Jwts.parser()
                .setSigningKey(Security.SEC_SECRET.getConstant().getBytes())
                .parseClaimsJws(token)
                .getBody();
        CredentialsDTO result = new CredentialsDTO();
        result.setUuid((String) claims.get(Security.SEC_JWT_CLAIM_IDENTIFIER.getConstant()));
        result.setUsername(claims.getSubject());
        result.setEmail((String) claims.get(Security.SEC_JWT_CLAIM_EMAIL.getConstant()));
        result.setRole((String) claims.get(Security.SEC_JWT_CLAIM_ROLE.getConstant()));
        return result;
    }

    
    /**
     * Validates a JWT token.
     * @param token The JWT token.
     * @return boolean
     */
    public boolean validateToken(final String token) {
        try {
        	log.info("JwtTokenProvider  ::  validateToken(String) :: validating the JWT token...");
            Jwts.parser().setSigningKey(jwtSecret.getBytes()).parseClaimsJws(token.replace("\"", "").trim());
            return true;
        } catch (SignatureException e) {
        	log.error("JwtTokenProvider  ::  validateToken(String) ::  ERROR  ::  Invalid signature  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
        } catch (MalformedJwtException e) {
        	log.error("JwtTokenProvider  ::  validateToken(String) ::  ERROR  ::  Invalid JWT token  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
        } catch (ExpiredJwtException e) {
        	log.error("JwtTokenProvider  ::  validateToken(String) ::  ERROR  ::  Expired JWT token  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
        } catch (UnsupportedJwtException e) {
        	log.error("JwtTokenProvider  ::  validateToken(String) ::  ERROR  ::  Unsupported JWT token  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
        } catch (IllegalArgumentException e) {
        	log.error("JwtTokenProvider  ::  validateToken(String) ::  ERROR  ::  JWT claims String is empty  ::  " + e.getClass().getName() + "  ::  " + e.getMessage());
        }
        return false;
    }
}
