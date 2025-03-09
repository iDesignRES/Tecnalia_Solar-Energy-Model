import logging
import os

import modules.io as io

from qgis.core import *
from qgis.server import *


# Function: Init QGIS
def init():
    QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
    qgisapp = QgsApplication([], False)
    qgisapp.initQgis()
    qgisserver = QgsServer()
    return qgisapp


# Function: Retrieve QGIS version
def getVersion():
    return str(Qgis.QGIS_VERSION)


# Function: Create a QGIS project
def createProject(projectFullPath, projectName, properties):
    if io.fileExists(projectFullPath):
        raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.project.exists'].replace('{1}', projectName))
    QgsProject.instance().setFileName(projectFullPath)


# Function: Write the QGIS project
def writeProject():
    QgsProject.instance().write()


# Function: Remove the QGIS project
def removeProject(projectFullPathAndName):
    QgsProject.instance().clear()
    if io.fileExists(projectFullPathAndName):
        io.removeFile(projectFullPathAndName)


# Function: Load a vector layer
def loadVectorLayer(layerPath, layerName, dataProvider):
    layer = QgsVectorLayer(layerPath, layerName, dataProvider)
    return layer


# Function: Load a raster layer
def loadRasterLayer(layerPath, layerName):
    layer = QgsRasterLayer(layerPath, layerName)
    return layer


# Function: Load a raster layer with provider
def loadRasterLayerWithProvider(layerPath, layerName, dataProvider):
    layer = QgsRasterLayer(layerPath, layerName, dataProvider)
    return layer


# Function: Add a layer to the QGIS project
def addLayerToProject(layer):
    QgsProject.instance().addMapLayer(layer)

