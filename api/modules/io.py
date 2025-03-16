import logging
import os
import requests

from modules.logging_config import logger

from pathlib import Path

import pandas as pd


########## Path functions ##########


# Function: Built the tree path
def buildTreePath(config):
    ''' Function to build the tree path. '''

    obj = {   'base': {
                  'key': config['IDESIGNRES-PATH']['idesignres.path.base'],
                  'children': {
                      'projects': {
                          'key': config['IDESIGNRES-PATH']['idesignres.path.projects']
                      },
                      'dbase': {
                          'key': config['IDESIGNRES-PATH']['idesignres.path.dbase']
                      },
                      'files': {
                          'key': config['IDESIGNRES-PATH']['idesignres.path.files'],
                          'children': {
                              'tmp': {
                                  'key': config['IDESIGNRES-PATH']['idesignres.path.tmp']
                              }
                          }
                      },
                      'layers': {
                          'key': config['IDESIGNRES-PATH']['idesignres.path.layers'],
                          'children': {
                              'tmp': {
                                  'key': config['IDESIGNRES-PATH']['idesignres.path.tmp']
                              }
                          }
                      },
                      'output': {
                          'key': config['IDESIGNRES-PATH']['idesignres.path.output']
                      },
                      'output-tmp': {
                          'key': config['IDESIGNRES-PATH']['idesignres.path.output.tmp']
                      }
                  }
              }
          }
    return obj


# Function: Retrieve the base path
def retrieveBasePath(config):
    ''' Function to retrieve the base path. '''
    
    obj = buildTreePath(config)
    return obj['base']['key']


# Function: Retrieve the projects base path
def retrieveProjectsBasePath(config):
    ''' Function to retrieve the projects base path. '''

    obj = buildTreePath(config)
    return obj['base']['key'] + obj['base']['children']['projects']['key']


# Function: Retrieve the dbase files base path
def retrieveDbaseBasePath(config):
    ''' Function to retrieve the dbase base path. '''

    obj = buildTreePath(config)
    return obj['base']['key'] + obj['base']['children']['dbase']['key']


# Function: Retrieve the projects base path + the default project name
def retrieveProjectsBasePathConcatProjectName(config):
    ''' Function to retrieve the projects base path, concatening the default project name. '''

    obj = buildTreePath(config)
    return obj['base']['key'] + obj['base']['children']['projects']['key'] + config['IDESIGNRES-PATH']['idesignres.path.projects.default.name']


# Function: Retrieve the layers base path
def retrieveLayersBasePath(config):
    ''' Function to retrieve the layers base path. '''

    obj = buildTreePath(config)
    return obj['base']['key'] + obj['base']['children']['layers']['key']


# Function: Retrieve the layers temporary base path
def retrieveLayersTmpPath(config):
    ''' Function to retrieve the layers temporary path. '''

    obj = buildTreePath(config)
    return obj['base']['key'] + obj['base']['children']['layers']['key'] + obj['base']['children']['layers']['children']['tmp']['key']


# Function: Retrieve the files base path
def retrieveFilesBasePath(config):
    ''' Function to retrieve the files base path. '''

    obj = buildTreePath(config)
    return obj['base']['key'] + obj['base']['children']['files']['key']


# Function: Retrieve the files temporary base path
def retrieveFilesTmpPath(config):
    ''' Function to retrieve the temporary base path. '''

    obj = buildTreePath(config)
    return obj['base']['key'] + obj['base']['children']['files']['key'] + obj['base']['children']['files']['children']['tmp']['key']


# Function: Retrieve the output base path
def retrieveOutputBasePath(local, config):
    ''' Function to retrieve the output base path. '''

    obj = buildTreePath(config)
    if local:
        return obj['base']['key'] + obj['base']['children']['output']['key']
    return config['IDESIGNRES-SFTP']['idesignres.sftp.path.output']


# Function: Retrieve the output temporary path
def retrieveOutputTmpPath(local, config):
    ''' Function to retrieve the output temporary path. '''

    obj = buildTreePath(config)
    if local:
        return obj['base']['key'] + obj['base']['children']['output-tmp']['key']
    return config['IDESIGNRES-SFTP']['idesignres.sftp.path.output.tmp']


# Function: Retrieve the output base path + the default output file name
def retrieveOutputBasePathConcatFile(local, process, username, nutsid, config):
    ''' Function to retrieve the output base path, concatening the default output file name. '''

    fileName = config['IDESIGNRES-PATH']['idesignres.path.output.default.name'].replace('{1}', process).replace('{2}', nutsid)
    if local:
        return retrieveOutputBasePath(True, config) + '/' + fileName
    return retrieveOutputBasePath(False, config).replace('{1}', username) + fileName


# Function: Retrieve the output temporary path + the default output file name
def retrieveOutputTmpPathConcatFile(local, process, username, nutsid, config):
    ''' Function to retrieve the output temporaty path, concatening the default output file name. '''

    fileName = config['IDESIGNRES-PATH']['idesignres.path.output.default.name'].replace('{1}', process).replace('{2}', nutsid)
    if local:
        return retrieveOutputTmpPath(True, config) + fileName
    return retrieveOutputTmpPath(False, config).replace('{1}', username) + fileName


# Function: Retrieve the "Radiation Potential Areas" file path
def retrieveRadiationPotentialAreasPath(config):
    ''' Function to retrieve the Radiation Potential Areas file path. '''

    return retrieveLayersTmpPath(config) + '/Radiation_PotentialAreas.tif'


# Function: Retrieve the default QGIS project name a file
def retrieveDefaultProjectName(config):
    ''' Function to retrieve the default project name. '''

    return config['IDESIGNRES-PATH']['idesignres.path.projects.default.name']


########## PV Power Plants path functions ##########


# Function: Build the PV Power Plants -> Preprocess -> Step 01 output path
def buildOutputPathPV1Step01(layer, nuts_id, config):
    ''' Function to retrieve the PV preprocess - Step 01 output path. '''

    return retrieveLayersTmpPath(config) + '/' + layer['name'] + '_' + nuts_id + '.' + layer['format']


# Function: Build the PV Power Plants -> Preprocess -> Step 01 output path with CRS
def buildOutputPathCRSPV1Step01(layer, nuts_id, reference_system, config):
    ''' Function to retrieve the PV preprocess - Step 01 output path (with CRS). '''

    return retrieveLayersTmpPath(config) + '/' + layer['name'] + '_' + nuts_id + '_' + str(reference_system) + '.' + layer['format']


# Function: Build the output path (clipped) for PV Power Plants -> Preprocess -> Steps 02, 03, 04 and 05
def buildOutputPathPV1Steps02030405(layer, config):
    ''' Function to retrieve the PV preprocess - Steps 02, 03, 04 and 05 output path. '''

    return retrieveLayersTmpPath(config) + '/' + layer['name'] + '_Clipped.' + layer['format']


# Function: Build the PV Power Plants -> Preprocess -> Step 06 and 07 output path
def buildOutputPathPV1Steps0607(src_path):
    ''' Function to retrieve the PV preprocess - Steps 06 and 07 output path. '''

    name, extension = os.path.splitext(src_path)
    return name + '_Filtered' + extension


# Function: Build the PV Power Plants -> Preprocess -> Step 08 and 10 output path
def buildOutputPathPV1Steps0810(src_path):
    ''' Function to retrieve the PV preprocess - Steps 08 and 10 output path. '''

    name, extension = os.path.splitext(src_path)
    return name + '_Res25' + extension


# Function: Build the PV Power Plants -> Preprocess -> Step 09, 11 and 13 output path
def buildOutputPathPV1Steps091113(src_path):
    ''' Function to retrieve the PV preprocess - Steps 09, 11 and 13 output path. '''

    name, extension = os.path.splitext(src_path)
    return name + '_Aligned' + extension


# Function: Build the PV Power Plants -> Preprocess -> Step 12 output path
def buildOutputPathPV1Step12(src_path):
    ''' Function to retrieve the PV preprocess - Step 12 output path. '''

    name, extension = os.path.splitext(src_path)
    return name + '_ReproResized' + extension


########## Building process path functions ##########


# Function: Build the Buildings preprocess -> Step 02 output paths
def buildOutputPathsBPStep02(layer, nuts_id, config, properties):
    ''' Function to retrieve the Buildings preprocess - Step 02 output path. '''

    path01 = retrieveLayersTmpPath(config) + '/' + layer['name'] + '_' + nuts_id + '.' + layer['format']
    path02 = retrieveLayersTmpPath(config) + '/' + layer['name'] + '_' + nuts_id +\
        '_repro54009.' + layer['format']
    return path01, path02


# Function: Build the output path (clipped) for Buildings preprocess -> Step 13
def buildOutputPathBPStep13(layer_name, layer_format, config):
    ''' Function to retrieve the Buildings preprocess - Step 13 output path. '''

    return retrieveLayersTmpPath(config) + '/' + layer_name + '_Clipped.' + layer_format


########## Strict I/O functions ##########


# Function: Check if a file exists
def fileExists(fileFullPath):
    ''' Function to check if a file exists. '''

    fileToCheck = Path(fileFullPath)
    return fileToCheck.is_file()


# Function: Remove a file
def removeFile(fileFullPath):
    ''' Function to remove a file. '''
    os.remove(fileFullPath)


# Function: Remove all the files in a directory
def removeFilesFromDirectory(directory):
    ''' Function to remove files from a directory. '''

    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))


########## Remote I/O functions ##########


# Function: Download a remote file
def downloadRemoteFile(remote_url, local_file_path, chunk_size, timeout, properties):
    ''' Function to download a remote file. '''

    try:
        logger.info(remote_url)
        with requests.get(remote_url, stream=True, timeout=timeout) as response:
            response.raise_for_status()
            total_size = int(response.headers.get(properties['IDESIGNRES-REST']['idesignres.rest.content.length.header'], 0))
            with open(local_file_path, 'wb') as f:
                downloaded_size = 0
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size:
                            percent_downloaded = (downloaded_size / total_size) * 100
                            logger.info(f'{percent_downloaded:.2f}% ({downloaded_size}/{total_size} bytes)')
    except Exception as error:
        raise


########## Other I/O functions ##########
# Function: Build a dictionary from PV output file
def buildDictionaryFromPVOutputFile(filePath):
    dictResult = []
    with open(filePath, 'r') as fil:
        dfResult = pd.read_csv(filePath, sep = ';')
        for index, row in dfResult.iterrows():
            dictResult.append({'time(UTC)': row[0], 'Pthermal': row[1], 'Ppv': row[2]})
    return dictResult