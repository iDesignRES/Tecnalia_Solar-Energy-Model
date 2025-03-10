import logging
import os

import modules.io as io

from qgis.core import *
from qgis.server import *


# Function: Init QGIS
def init():
    ''' Function to init QGIS. '''

    QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
    qgisapp = QgsApplication([], False)
    qgisapp.initQgis()
    qgisserver = QgsServer()
    return qgisapp


# Function: Retrieve QGIS version
def getVersion():
    ''' Function to retrieve the QGIS version. '''

    return str(Qgis.QGIS_VERSION)


# Function: Create a QGIS project
def createProject(projectFullPath, projectName, properties):
    ''' Function to create a QGIS project. '''

    if io.fileExists(projectFullPath):
        raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.project.exists'].replace('{1}', projectName))
    QgsProject.instance().setFileName(projectFullPath)


# Function: Write the QGIS project
def writeProject():
    ''' Function to write the QGIS project. '''

    QgsProject.instance().write()


# Function: Remove the QGIS project
def removeProject(projectFullPathAndName):
    ''' Function to remove a QGIS project. '''

    QgsProject.instance().clear()
    if io.fileExists(projectFullPathAndName):
        io.removeFile(projectFullPathAndName)


# Function: Load a vector layer
def loadVectorLayer(layerPath, layerName, dataProvider):
    ''' Function to load a vector layer. '''

    layer = QgsVectorLayer(layerPath, layerName, dataProvider)
    return layer


# Function: Load a raster layer
def loadRasterLayer(layerPath, layerName):
    ''' Function to load a raster layer. '''

    layer = QgsRasterLayer(layerPath, layerName)
    return layer


# Function: Load a raster layer with provider
def loadRasterLayerWithProvider(layerPath, layerName, dataProvider):
    ''' Function to load a raster layer with provider. '''

    layer = QgsRasterLayer(layerPath, layerName, dataProvider)
    return layer


# Function: Add a layer to the QGIS project
def addLayerToProject(layer):
    ''' Function to add a layer to a QGIS project. '''

    QgsProject.instance().addMapLayer(layer)

