package eu.idesignres.ui.backend.dck.model;

import java.io.Serializable;


/**
 * Model of a Connection object.
 * @author Tecnalia
 * @version 1.0
 */
public class Connection implements Serializable, Cloneable {
	
	/* The "serialVersionUID" constant */
	private static final long serialVersionUID = -2482801590010695733L;
	
	
	/** The host. */
	private String host;
	
	/** The port. */
    private Integer port;

	/** The username. */
    private String username;
	
	/** The password. */
    private String password;
    
    
    /**
     * Constructs a Connection.
     */
    public Connection() {
    	super();
    }
    
    /**
     * Constructs a Connection.
     * @param host The host.
     * @param port The port.
     * @param username The username.
     * @param password The password.
     */
    public Connection(final String host, final Integer port, final String username,
    		final String password) {
    	super();
    	
    	this.host = host;
    	this.port = port;
    	this.username = username;
        this.password = password;
    }
    

    /**
     * Gets the host.
     * @return String
     */
    public String getHost() {
        return host;
    }

    /**
     * Sets the host.
     * @param host The host.
     */
    public void setHost(final String host) {
        this.host = host;
    }
    
    /**
     * Gets the port.
     * @return Integer
     */
    public Integer getPort() {
        return port;
    }

    /**
     * Sets the port.
     * @param port The port.
     */
    public void setPort(final Integer port) {
        this.port = port;
    }
    
    /**
     * Gets the username.
     * @return String
     */
    public String getUsername() {
        return username;
    }

    /**
     * Sets the username.
     * @param username The username.
     */
    public void setUsername(final String username) {
        this.username = username;
    }
    
    /**
     * Gets the password.
     * @return String
     */
    public String getPassword() {
        return password;
    }

    /**
     * Sets the password.
     * @param password The password.
     */
    public void setPassword(final String password) {
        this.password = password;
    }
    
    
    /*
     * (non-Javadoc)
     * @see java.lang.Object#clone()
     */
    @Override
	public Object clone() throws CloneNotSupportedException {
    	return super.clone();
	}
    
    
    /*
     * (non-Javadoc)
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
    	StringBuffer buffer = new StringBuffer("Connection {");
    	buffer.append("host=").append(getHost());
    	buffer.append(", port=").append(getPort());
    	buffer.append(", username=").append(getUsername());
    	buffer.append(", password=").append(getPassword()).append("}");
    	return buffer.toString();
    }
}
