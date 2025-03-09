package eu.idesignres.ui.backend.dck.util;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.SftpException;

import eu.idesignres.ui.backend.dck.constants.Strings;
import eu.idesignres.ui.backend.dck.model.Connection;


/**
 * Utilities to manage SFTP connections.
 * @author Tecnalia
 * @version 1.0
 */
public final class SFTPUtil {
	
	/** Logger. **/
	private static final Logger log = LoggerFactory.getLogger(SFTPUtil.class);
	
	/** The TIMEOUT constant. */
	private static final Integer TIMEOUT = 1000000;
	
	
	/**
	 * Creates a session.
	 * @param connection The connection.
     * @return Session
	 * @throws JSchException
	 */
	private static Session createSession(final Connection connection) throws JSchException {
		JSch jsch = new JSch();
	    Session session = null;
	    
	    // Create the session
        session = jsch.getSession(connection.getUsername(), connection.getHost(), connection.getPort());
        session.setPassword(connection.getPassword());
        session.setTimeout(TIMEOUT);

        // Avoid asking for key confirmation
        session.setConfig("StrictHostKeyChecking", "no");

        // Connect to the SFTP Server
        session.connect();
        log.info("Session connected to the SFTP Server!");
        
        return session;
	}
	
	
	/**
	 * Opens a channel.
	 * @param session The session
     * @return ChannelSftp
	 * @throws JSchException 
	 */
	private static ChannelSftp openChannel(final Session session) throws JSchException {
		// Open the channel
		ChannelSftp channelSftp = (ChannelSftp) session.openChannel("sftp");
        channelSftp.connect();
        log.info("SFTP channel opened!");
        
        return channelSftp;
	}

    
	/**
	 * Creates a remote directory.
     * @param connection The connection.
     * @param directory The directory.
     * @param create The create.
     * @throws JSchException
     * @throws SftpException
     */
	public static void createOrRemoveRemoteDirectory(final Connection connection, final String directory, final boolean create) throws JSchException, SftpException {
       Session session = null;
       ChannelSftp channelSftp = null;
       try {
    	   // Create the session
           session = createSession(connection);
           if (session != null) {
        	   // Open the SFTP channel
        	   channelSftp = openChannel(session); 
        	   if (channelSftp != null) {
        		   if (create) {
                	   // Create the directory and assign permissions
                	   log.info("Create the directory -> " + directory);
                	   channelSftp.mkdir(directory);
                	   log.info("Assign permissions to the directory -> " + directory);
                	   channelSftp.chmod(Integer.parseInt("777", 8), directory);	// Convert octal -> decimal
                   } else {
                	   // Remove all the files in the directory
                	   @SuppressWarnings("unchecked")
                	   Vector<LsEntry> filelist = (Vector<LsEntry>) channelSftp.ls(directory);
                	   for (LsEntry entry : filelist) {
                		   final String fileName = entry.getFilename();
                		   if (!fileName.equals(Strings.STR_DOT.getConstant()) && !fileName.equals(Strings.STR_DOT_DOT.getConstant())) {
                    		   log.info("Remove the file -> " + entry.getFilename());
                    		   channelSftp.rm(directory + Strings.STR_SLASH.getConstant() + entry.getFilename());
                    	   }
                       }
                	   
                	   // Remove the directory
                       log.info("Remove the directory -> " + directory);
                	   channelSftp.rmdir(directory);
                   }
        	   }
           }
       } catch (Exception e) {
           throw e;
       } finally {
    	   // Disconnect all
           if (channelSftp != null) {
               channelSftp.disconnect();
               log.info("SFTP channel closed!");
           }
           if (session != null) {
               session.disconnect();
               log.info("Session disconnected!");
           }
       }
   }
   
   
   /**
    * Uploads a file to a remote directory.
    * @param connection The connection.
    * @param fileFullPath The fileFullPath.
    * @param fileBytes The fileBytes.
    * @throws JSchException
    * @throws SftpException
    * @throws FileNotFoundException
    */
   public static void uploadFileToRemoteDirectory(final Connection connection, final String fileFullPath, final byte[] fileBytes) throws JSchException, SftpException, FileNotFoundException {
       Session session = null;
       ChannelSftp channelSftp = null;
       try {
    	   // Create the session
           session = createSession(connection);
           if (session != null) {
        	   // Open the SFTP channel
        	   channelSftp = openChannel(session); 
        	   if (channelSftp != null) {
        		   // Upload the file
                   log.info("Store the file -> " + fileFullPath);
                   channelSftp.put(new ByteArrayInputStream(fileBytes), fileFullPath);
        	   }
           }
       } catch (Exception e) {
           throw e;
       } finally {
    	   // Disconnect all
           if (channelSftp != null) {
               channelSftp.disconnect();
               log.info("SFTP channel closed!");
           }
           if (session != null) {
               session.disconnect();
               log.info("Session disconnected!");
           }
       }
   }
   
   
   /**
    * Removes a remote file.
    * @param connection The connection.
    * @param fileFullPath The fileFullPath.
    * @throws JSchException
    * @throws SftpException
    */
   public static void removeRemoteFile(final Connection connection, final String fileFullPath) throws JSchException, SftpException {
       Session session = null;
       ChannelSftp channelSftp = null;
       try {
    	   // Create the session
           session = createSession(connection);
           if (session != null) {
        	   // Open the SFTP channel
        	   channelSftp = openChannel(session); 
        	   if (channelSftp != null) {
        		   // Remove the file
                   log.info("Remove the file -> " + fileFullPath);
                   channelSftp.rm(fileFullPath);
        	   }
           }
       } catch (Exception e) {
           throw e;
       } finally {
    	   // Disconnect all
           if (channelSftp != null) {
               channelSftp.disconnect();
               log.info("SFTP channel closed!");
           }
           if (session != null) {
               session.disconnect();
               log.info("Session disconnected!");
           }
       }
   }
   
   
   /**
    * Retrieves the list of files in a directory.
    * @param connection The connection.
    * @param directory The directory.
    * @return List<String>
    * @throws JSchException
    * @throws SftpException
    */
   public static List<String> retrieveListOfFilesInDirectory(final Connection connection, final String directory) throws JSchException, SftpException {
	   List<String> result = new ArrayList<String>();
       Session session = null;
       ChannelSftp channelSftp = null;
       try {
           // Create the session
           session = createSession(connection);
           if (session != null) {
        	   // Open the SFTP channel
        	   channelSftp = openChannel(session); 
        	   if (channelSftp != null) {
        		   // Retrieve all the files in the directory
                   @SuppressWarnings("unchecked")
                   Vector<LsEntry> filelist = (Vector<LsEntry>) channelSftp.ls(directory);
            	   for (LsEntry entry : filelist) {
            		   final String fileName = entry.getFilename();
            		   if (!fileName.equals(Strings.STR_DOT.getConstant()) && !fileName.equals(Strings.STR_DOT_DOT.getConstant())) {
                		   log.info("File -> " + entry.getFilename());
                		   result.add(entry.getFilename());
                	   }
                   }
        	   }
           }
		   
           return result;
       } catch (Exception e) {
           throw e;
       } finally {
    	   // Disconnect all
           if (channelSftp != null) {
               channelSftp.disconnect();
               log.info("SFTP channel closed!");
           }
           if (session != null) {
               session.disconnect();
               log.info("Session disconnected!");
           }
       }
   }
   
   
   /**
    * Retrieves a file as a byte array.
    * @param connection The connection.
    * @param fileFullPath The fileFullPath.
    * @return byte[]
    * @throws JSchException
    * @throws SftpException
 * @throws IOException 
    */
   public static byte[] retrieveFile(final Connection connection, final String fileFullPath) throws JSchException, SftpException, IOException {
	   byte[] result = null;
	   ByteArrayOutputStream out = null;
       Session session = null;
       ChannelSftp channelSftp = null;
       try {
           // Create the session
           session = createSession(connection);
           if (session != null) {
        	   // Open the SFTP channel
        	   channelSftp = openChannel(session); 
        	   if (channelSftp != null) {
        		   // Retrieve the file
        		   log.info("File -> " + fileFullPath);
        		   out = new ByteArrayOutputStream();
        		   channelSftp.get(fileFullPath, out);
        		   result = out.toByteArray();
        		   log.info("Length (bytes) -> " + result.length);
        	   }
           }
		   
           return result;
       } catch (Exception e) {
           throw e;
       } finally {
    	   // Disconnect all
    	   if (out != null) {
    		   out.close();
    	   }
           if (channelSftp != null) {
               channelSftp.disconnect();
               log.info("SFTP channel closed!");
           }
           if (session != null) {
               session.disconnect();
               log.info("Session disconnected!");
           }
       }
   }
}