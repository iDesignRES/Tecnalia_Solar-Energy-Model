import logging
import paramiko

import modules.io as io


########## SFTP functions ##########


# Function: Build the connection parameters
def buildConnectionParameters(config):
    obj = { 'hostname': config['IDESIGNRES-SFTP']['idesignres.sftp.host'],
            'port': int(config['IDESIGNRES-SFTP']['idesignres.sftp.port']),
            'username': config['IDESIGNRES-SFTP']['idesignres.sftp.username'],
            'password': config['IDESIGNRES-SFTP']['idesignres.sftp.password'],
            'timeout': int(config['IDESIGNRES-SFTP']['idesignres.sftp.timeout'])
          }
    return obj


# Function: Checks a user directory
def checkUserDirectory(username, config):
    try:
        # Build the path
        userDirectoryPath = io.retrieveOutputBasePath(False, config).replace('{1}', username)
        logging.info('  SFTP Server/> Checking if the user is authorized to execute the process...')
        logging.info('')
            
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)
            
        # Open the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname = conn['hostname'],
            port = conn['port'],
            username = conn['username'],
            password = conn['password'],
            timeout = conn['timeout'])
        
        # Open the SFTP channel
        sftp = client.open_sftp()

        # Check the directory
        sftp.stat(userDirectoryPath)
        logging.info('')
        logging.info('  SFTP Server/> Authorized!')
        return True
    except FileNotFoundError as fnfError:
        logging.info('')
        logging.info('  SFTP Server/> Not authorized!')
        return False
    except IOError as ioError:
        logging.info('')
        logging.info('  SFTP Server/> Not authorized!')
        return False
    except Exception as error:
        raise


# Function: Retrieve the layer files stored in the SFTP Server
def retrieveLayerFiles(layerList, config):
    try:
        if layerList and len(layerList) > 0:
            # Retrieve the base path
            basePath = io.retrieveBasePath(config)
            
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Retrieve the files
            logging.info('')
            for layer in layerList:
                if io.fileExists(basePath + layer['path']):
                    logging.info('  SFTP Server/> The file "' + layer['name'] + '" is already locally stored.')
                else:
                    logging.info('  SFTP Server/> Downloading the file "' + layer['name'] + '"...')
                    sftp.get(layer['path'], basePath + layer['path'])
            logging.info('')
        
            # Close the SSH client and return
            client.close()
            return True
        return False
    except Exception as error:
        raise


# Function: Retrieve the data files stored in the SFTP Server
def retrieveDataFiles(fileList, config):
    try:
        if fileList and len(fileList) > 0:
            # Retrieve the base path
            basePath = io.retrieveBasePath(config)
            
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Retrieve the files
            logging.info('')
            for fil in fileList:
                if io.fileExists(basePath + fil['path']):
                    logging.info('  SFTP Server/> The file "' + fil['name'] + '" is already locally stored.')
                else:
                    logging.info('  SFTP Server/> Downloading the file "' + fil['name'] + '"...')
                    sftp.get(fil['path'], basePath + fil['path'])
            logging.info('')
        
            # Close the SSH client and return
            client.close()
            return True
        return False
    except Exception as error:
        raise


# Function: Retrieve the dbase files stored in the SFTP Server
def retrieveDbaseFiles(config):
    try:
        # Retrieve the base path
        basePath = io.retrieveBasePath(config)
            
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)
            
        # Open the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname = conn['hostname'],
            port = conn['port'],
            username = conn['username'],
            password = conn['password'],
            timeout = conn['timeout'])
        
        # Open the SFTP channel
        sftp = client.open_sftp()
        
        # List all files in the remote folder
        logging.info('')
        fileList = sftp.listdir(config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'])
        fileList.sort()
        result = []
        for fil in fileList:
            if io.fileExists(basePath + config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil):
                logging.info('  SFTP Server/> The file "' + fil + '" is already locally stored.')
            else:
                logging.info('  SFTP Server/> Downloading the file "' + (config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil) + '"...')
                sftp.get(config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil,
                    basePath + config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil)
            result.append({'name': fil, 'path': basePath + config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil})
        
        # Close the SSH client and return
        client.close()
        return result
    except Exception as error:
        raise


# Function: Retrieve a single file stored in the SFTP Server
def retrieveSingleFile(filePath, fileName, config):
    try:
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)
            
        # Open the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname = conn['hostname'],
            port = conn['port'],
            username = conn['username'],
            password = conn['password'],
            timeout = conn['timeout'])
        
        # Open the SFTP channel
        sftp = client.open_sftp()
        
        # Download the file
        logging.info('')
        logging.info('  SFTP Server/> Downloading the file "' + (filePath + fileName) + '"...')
        sftp.get(filePath + fileName, io.retrieveFilesTmpPath(config) + '/' + fileName)
        
        # Close the SSH client and return
        client.close()
        return True
    except Exception as error:
        return False


# Function: Downloads a resource stored in the SFTP Server
def downloadResource(resource, config):
    try:
        if resource:
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Retrieve the files
            logging.info('')
            logging.info('  SFTP Server/> Downloading the file "' + resource['name'] + '"...')
            local_path = io.retrieveFilesTmpPath(config) + '/' + resource['name']
            sftp.get(resource['sftp'], local_path)
            logging.info('')
        
            # Close the SSH client and return
            client.close()
            return local_path
        return None
    except Exception as error:
        raise


# Function: Checks if a file exists in the SFTP Server
def fileExists(remoteFilePath, config):
    try:
        if remoteFilePath:
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Check if the file exists
            sftp.stat(remoteFilePath)
        
            # Close the SSH client and return
            client.close()
            return True
        return False
    except FileNotFoundError as fnfError:
        logging.error(str(fnfError))
        return False
    except IOError as ioError:
        logging.error(str(ioError))
        return False
    except Exception as error:
        logging.error(str(error))
        raise
 
 
 # Function: Upload an output file to the SFTP Server
def uploadOutputFile(localFilePath, remoteFilePath, config):
    try:
        if localFilePath and remoteFilePath:
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Upload the file
            logging.info('')
            if io.fileExists(localFilePath):
                logging.info('  SFTP Server/> Uploading the output file...')
                sftp.put(localFilePath, remoteFilePath)
            logging.info('')
        
            # Close the SSH client and return
            client.close()
            return True
        return False
    except Exception as error:
        logging.error(str(error))
        raise


