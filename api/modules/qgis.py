import logging
import os

import modules.io as io

from modules.logging_config import logger

from qgis.core import *
from qgis.server import *


# Function: Init QGIS
def init():
    '''
    Function to init QGIS.
    Input parameters:
        None.
    '''

    QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
    qgisapp = QgsApplication([], False)
    qgisapp.initQgis()
    qgisserver = QgsServer()
    return qgisapp


# Function: Retrieve QGIS version
def getVersion():
    '''
    Function to retrieve the QGIS version.
    Input parameters:
        None.
    '''

    return str(Qgis.QGIS_VERSION)


# Function: Create a QGIS project
def createProject(projectFullPath, projectName, properties):
    '''
    Function to create a QGIS project.
    Input parameters:
        projectFullPath: text -> The full path where the project is stored.
        projectName: text -> The name of the project.
        properties: ConfigParser -> The data in the properties file.
    '''

    if io.fileExists(projectFullPath):
        raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.project.exists'].replace('{1}', projectName))
    QgsProject.instance().setFileName(projectFullPath)


# Function: Write the QGIS project
def writeProject():
    '''
    Function to write the QGIS project.
    Input parameters:
        None.
    '''

    QgsProject.instance().write()


# Function: Remove the QGIS project
def removeProject(projectFullPathAndName):
    '''
    Function to remove a QGIS project.
    Input parameters:
        projectFullPathAndName: text -> The full path of the project to be removed.
    '''

    QgsProject.instance().clear()
    if io.fileExists(projectFullPathAndName):
        io.removeFile(projectFullPathAndName)


# Function: Load a vector layer
def loadVectorLayer(layerPath, layerName, dataProvider):
    '''
    Function to load a vector layer.
    Input parameters:
        layerPath: text -> The path of the layer file.
        layerName: text -> The name of the layer.
        dataProvider: text -> The data provider.
    '''

    layer = QgsVectorLayer(layerPath, layerName, dataProvider)
    return layer


# Function: Load a raster layer
def loadRasterLayer(layerPath, layerName):
    '''
    Function to load a raster layer.
    Input parameters:
        layerPath: text -> The path of the layer file.
        layerName: text -> The name of the layer.
    '''

    layer = QgsRasterLayer(layerPath, layerName)
    return layer


# Function: Load a raster layer with provider
def loadRasterLayerWithProvider(layerPath, layerName, dataProvider):
    '''
    Function to load a raster layer with provider.
    Input parameters:
        layerPath: text -> The path of the layer file.
        layerName: text -> The name of the layer.
        dataProvider: text -> The data provider.
    '''

    layer = QgsRasterLayer(layerPath, layerName, dataProvider)
    return layer


# Function: Add a layer to the QGIS project
def addLayerToProject(layer):
    '''
    Function to add a layer to a QGIS project.
    Input parameters:
        layer: object -> The layer to be added.
    '''

    QgsProject.instance().addMapLayer(layer)

