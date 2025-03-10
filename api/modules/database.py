import logging
import pymysql


########## Database functions ##########


# Function: Build the connection parameters
def buildConnectionParameters(config):
    ''' Function to define the database connection parameters. '''

    obj = { 'host': config['IDESIGNRES-DB']['idesignres.db.host'],
            'user': config['IDESIGNRES-DB']['idesignres.db.username'],
            'pwd': config['IDESIGNRES-DB']['idesignres.db.password'],
            'db': config['IDESIGNRES-DB']['idesignres.db.database']
          }
    return obj


# Function: Retrieve all the processes in the database
def retrieveAllProcesses(config):
    ''' Function to retrieve from the database all the available processes. '''

    result = []
    conn = None
    try:
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)

        # Connect to the database
        logging.info('  DATA Server/> Connecting to the database...')
        conn = pymysql.connect(host = conn['host'], user = conn['user'], password = conn['pwd'], db = conn['db'])

        # Declare the custom cursor
        cursor = conn.cursor()
        
        # Declare and execute the query
        logging.info('  DATA Server/> Executing the query to retrieve the processes...')
        query = """
            SELECT
                uuid,
                name
            FROM
                t03_idesignres_processes
            ORDER BY uuid
        """
        cursor.execute(query)
        processes = cursor.fetchall()
        if processes and len(processes) > 0:
            for process in processes:
                logging.info('  DATA Server/> ' + process[0] + ' -> ' + process[1])
                result.append({ 'uuid': process[0], 'name': process[1] })
        return result
    except Exception as error:
        raise
    finally:
        # Close the connection
        if conn:
            conn.close()


# Function: Retrieve all the layers in the database
def retrieveAllLayersByProcess(process, config):
    ''' Function to retrieve from the database all the layers associated to a process. '''

    result = []
    conn = None
    try:
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)

        # Connect to the database
        logging.info('  DATA Server/> Connecting to the database...')
        conn = pymysql.connect(host = conn['host'], user = conn['user'], password = conn['pwd'], db = conn['db'])

        # Declare the custom cursor
        cursor = conn.cursor()
        
        # Declare and execute the query
        logging.info('  DATA Server/> Executing the query to retrieve the layers...')
        query = """
            SELECT
                layer_uuid,
                layer_name,
                layer_full_path,
                layer_format_extension
            FROM
                v31_idesignres_processes_layers
            WHERE process_uuid = '%s'
            ORDER BY layer_uuid
        """
        cursor.execute(query % (process))
        layers = cursor.fetchall()
        if layers and len(layers) > 0:
            for layer in layers:
                logging.info('  DATA Server/> ' + layer[0] + ' -> ' + layer[1])
                result.append({ 'uuid': layer[0], 'name': layer[1], 'path': layer[2], 'format': layer[3] })
        return result
    except Exception as error:
        raise
    finally:
        # Close the connection
        if conn:
            conn.close()


# Function: Retrieve all the files in the database
def retrieveAllFilesByProcess(process, config):
    ''' Function to retrieve from the database all the files associated to a process. '''

    result = []
    conn = None
    try:
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)

        # Connect to the database
        logging.info('  DATA Server/> Connecting to the database...')
        conn = pymysql.connect(host = conn['host'], user = conn['user'], password = conn['pwd'], db = conn['db'])

        # Declare the custom cursor
        cursor = conn.cursor()
        
        # Declare and execute the query
        logging.info('  DATA Server/> Executing the query to retrieve the files...')
        query = """
            SELECT
                file_uuid,
                file_name,
                file_full_path
            FROM
                v32_idesignres_processes_files
            WHERE process_uuid = '%s'
            ORDER BY file_uuid
        """
        cursor.execute(query % (process))
        files = cursor.fetchall()
        if files and len(files) > 0:
            for fil in files:
                logging.info('  DATA Server/> ' + fil[0] + ' -> ' + fil[1])
                result.append({ 'uuid': fil[0], 'name': fil[1], 'path': fil[2] })
        return result
    except Exception as error:
        raise
    finally:
        # Close the connection
        if conn:
            conn.close()


# Function: Retrieve all the resources in the database
def retrieveAllResources(process, config):
    ''' Function to retrieve from the database all the resources. '''

    result = []
    conn = None
    try:
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)

        # Connect to the database
        logging.info('  DATA Server/> Connecting to the database...')
        conn = pymysql.connect(host = conn['host'], user = conn['user'], password = conn['pwd'], db = conn['db'])

        # Declare the custom cursor
        cursor = conn.cursor()
        
        # Declare and execute the query
        logging.info('  DATA Server/> Executing the query to retrieve the resources...')
        query = """
            SELECT
                resource_uuid,
                resource_name,
                resource_web_path,
                resource_sftp_path
            FROM
                v33_idesignres_processes_resources
            WHERE process_uuid = '%s'
            ORDER BY resource_uuid
        """
        cursor.execute(query % (process))
        resources = cursor.fetchall()
        if resources and len(resources) > 0:
            for resource in resources:
                logging.info('  DATA Server/> ' + resource[1])
                result.append({ 'uuid': resource[0], 'name': resource[1], 'web': resource[2], 'sftp': resource[3], 'local': None })
        return result
    except Exception as error:
        raise
    finally:
        # Close the connection
        if conn:
            conn.close()

