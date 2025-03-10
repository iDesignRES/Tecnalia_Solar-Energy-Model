import csv
import fnmatch
import gc
import logging
import os
import zipfile

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask

import modules.io as io
import modules.qgis as qgis
import modules.sftp as sftp

from qgis.core import QgsField
from qgis.core import QgsSpatialIndex
from qgis.core import (
    QgsField, QgsSpatialIndex, QgsFeatureRequest,
    QgsExpression
)
from qgis.analysis import QgsZonalStatistics
from PyQt5.QtCore import QVariant
from shapely.geometry import LineString
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# Function: Build. Energy Sim. -> Preprocess -> Step 01 -> Obtain the ZIP file
def bp1Step01(nutsId, fileList, resourceList, config, properties):
    ''' Build. Energy Sim. -> Preprocess -> Step 01 : Obtain the ZIP file. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Preparing the data...')
    if not (4 <= len(nutsId) <= 5 and nutsId[:2].isalpha()):
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> NUTS_ID not valid! [NUTS2/NUTS3]!')
        return
    
    # Read the Excel file
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Reading the Excel file...')
    df = pd.read_excel(io.retrieveBasePath(config) + fileList[0]['path'])
    url = df.loc[df['NUTS_ID'] == nutsId, 'Link'].values
    if not url or len(url) == 0:
        raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.nuts.id.not.found'])

    # Search the resource from the url, and download it
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Obtaining the ZIP file...')
    destinationDir = io.retrieveFilesTmpPath(config)
    resourceObj = None
    for resource in resourceList:
        if resource['web'] == url:
            resourceObj = resource
            break
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Unzipping...')
    logging.info('')
    if resourceObj:
        resourceObj['local'] = sftp.downloadResource(resourceObj, config)
        if resourceObj['local'] and zipfile.is_zipfile(resourceObj['local']):
            with zipfile.ZipFile(resourceObj['local'], 'r') as zipRef:
                zipRef.extractall(io.retrieveFilesTmpPath(config))
        else:
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.not.zip.file'])
    
    # Delete all the not necessary files
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Removing the not necessary files...')
    excludeFiles = ['README', 'gis_osm_landuse_a_free_1', 'gis_osm_buildings_a_free_1']
    for fil in os.listdir(destinationDir):
        filenameWithoutExt = os.path.splitext(fil)[0]
        if not any(fnmatch.fnmatch(filenameWithoutExt, pattern) for pattern in excludeFiles):
            os.remove(os.path.join(destinationDir, fil))

    # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> [OK]')
    logging.info('')
    return destinationDir


# Function: Build. Energy Sim. -> Preprocess -> Step 02 -> Export the selected NUTS
def bp1Step02(layer, nutsId, config, properties):
    ''' Build. Energy Sim. -> Preprocess -> Step 02 : Export the selected NUTS. '''
    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> Exporting the selected NUTS...')
    
    # Read the layer file
    data = gpd.read_file(io.retrieveBasePath(config) + layer['path'])
    
    # Filter data according to length of NUTS_ID and select the name of the NUTS
    if len(nutsId) == 5:
        nutsFiltered = data[data['NUTS_ID'] == nutsId]
        nutsNameValues = data[(data['NUTS_ID'] == nutsId) & (data['LEVL_CODE'] == 3)]['NUTS_NAME'].values
    else:
        nutsFiltered = data[(data['NUTS_ID'].str.startswith(nutsId)) & (data['LEVL_CODE'] == 3)]
        nutsNameValues = data[(data['NUTS_ID'] == nutsId) & (data['LEVL_CODE'] == 2)]['NUTS_NAME'].values
    
    # Ensure that values exist for NUTS_NAME
    if len(nutsNameValues) > 0:
        nuts_name = nutsNameValues[0]
        nutsFiltered['NUTS2_NAME'] = nuts_name
    else:
        raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.nuts.name.for_nuts.id'].replace('{1}', nutsId))
    
    # Convert GeoDataFrame to 4326 and 54009 Mollewide coordinate systems
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> Converting GeoDataFrame to 4326 cooordinate system...')
    nutsFilteredCrs = nutsFiltered.to_crs(epsg = 4326)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> Converting GeoDataFrame to 54009 Mollewide cooordinate system...')
    nutsFilteredMoll54009 = nutsFiltered.to_crs('Esri:54009')
    
    # Save
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> Saving...')
    outputNutsPath, outputNutsPathMoll54009 = io.buildOutputPathsBPStep02(layer, nutsId, config, properties)
    nutsFilteredCrs.to_file(outputNutsPath, driver = layer['format'].upper())
    nutsFilteredMoll54009.to_file(outputNutsPathMoll54009, driver = layer['format'].upper())
    
    # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> [OK]')
    logging.info('')
    return nutsFilteredCrs, outputNutsPathMoll54009


# Function: Build. Energy Sim. -> Preprocess -> Step 03 -> Clip and save the vector layers
def bp1Step03(destinationDir, nutsFilteredCrs):
    ''' Build. Energy Sim. -> Preprocess -> Step 03 : Clip and save the vector layers. '''
    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> Clipping the layer(s) (can take quite a while)...')
    
    # Use the NUTS layer at 4326 for cutting. Reproject and save layers in 54009 and gpkg
    clippedLayers = []
    for fil in os.listdir(destinationDir):
        if fil.endswith('shp'):
            filepath = os.path.join(destinationDir, fil)
            logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> File -> ' + filepath)
            gdf = gpd.read_file(filepath)
            gdfClipped = gpd.clip(gdf, nutsFilteredCrs)
            gdfClipped = gdfClipped.to_crs('Esri:54009'.upper())
            
            # Only save if the file is not empty
            if not gdfClipped.empty:
                output = destinationDir + '/' + str(fil.rsplit('.', 1)[0]) + '_repro54009.gpkg'
                logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> Save -> ' + output)
                gdfClipped.to_file(output, driver = 'GPKG')
                clippedLayers.append(output)
            else:
                logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> The file is empty, so it is not saved!')
    
    # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> [OK]')
    logging.info('')
    return clippedLayers


# Function: Build. Energy Sim. -> Preprocess -> Step 04 -> Load the buildings layer
def bp1Step04(clippedLayers, isTest, config):
    ''' Build. Energy Sim. -> Preprocess -> Step 04 : Load the buildings layer. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 04 -> Loading the buildings layer...')
    buildingsPath = config['IDESIGNRES-PATH']['idesignres.path.bp.test']\
        if isTest else [path for path in clippedLayers if 'buildings' in path][0]
    layer = qgis.loadVectorLayer(buildingsPath, 'Buildings', 'ogr')
    
    # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 04 -> [OK]')
    logging.info('')
    return layer
    
    
# Function: Build. Energy Sim. -> Preprocess -> Step 05 -> Load the NUTS layer
def bp1Step05(nutsPathMoll54009):
    ''' Build. Energy Sim. -> Preprocess -> Step 05 : Load the NUTS layer. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 05 -> Loading the NUTS layer...')
    layer = qgis.loadVectorLayer(nutsPathMoll54009, 'NUTS', 'ogr')
    
     # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 05 -> [OK]')
    logging.info('')
    return layer


# Function: Build. Energy Sim. -> Preprocess -> Step 06 -> Load the land use layer
def bp1Step06(clippedLayers):
    ''' Build. Energy Sim. -> Preprocess -> Step 06 : Load the land use layer. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 06 -> loading the land use layer...')
    layer = qgis.loadVectorLayer([path for path in clippedLayers if 'landuse' in path][0], 'Land Use', 'ogr')
    
     # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 06 -> [OK]')
    logging.info('')
    return layer


# Function: Build. Energy Sim. -> Preprocess -> Step 07 -> Load the Raster Use layer
def bp1Step07(layerObj, config):
    ''' Build. Energy Sim. -> Preprocess -> Step 07 : Load the raster use layer. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 07 -> Loading the Raster Use layer...')
    layer = qgis.loadRasterLayerWithProvider(io.retrieveLayersBasePath(config) + '/' +\
        layerObj['name'] + '.' + layerObj['format'], 'Raster Use', 'gdal')
    
     # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 07 -> [OK]')
    logging.info('')
    return layer


# Function: Build. Energy Sim. -> Preprocess -> Step 08 -> Load the Raster Height layer
def bp1Step08(layerObj, config):
    ''' Build. Energy Sim. -> Preprocess -> Step 08 : Load the raster height layer. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 08 -> Loading the Raster Height layer...')
    layer = qgis.loadRasterLayerWithProvider(io.retrieveLayersBasePath(config) + '/' +\
        layerObj['name'] + '.' + layerObj['format'], 'Raster Height', 'gdal')
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 08 -> [OK]')
    logging.info('')
    return layer


# Function: Build. Energy Sim. -> Preprocess -> Step 09 -> Assign NUTS
def bp1Step09(buildingsLayer, nutsLayer, nutsId):
    '''
    Build. Energy Sim. -> Preprocess -> Step 09 : Assign NUTS.
    This function assigns NUTS3, NUTS2 and BuildingFP_area to each building in a given layer (buildingsLayer).
    If the building's area is less than 30 m², the building is removed from the layer.
    If a building does not have a 'NUTS3' value, it is also removed.
    '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> ##### Start building preprocessing #####')
    logging.info('')
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Assigning NUTS...')
    
    # Verify if "NUTS3", "NUTS2" and "AREA" fields exist. If not, it creates them
    if buildingsLayer.fields().indexFromName('NUTS3') == -1:
        buildingsLayer.dataProvider().addAttributes([QgsField('NUTS3', QVariant.String)])
        buildingsLayer.updateFields()

    if buildingsLayer.fields().indexFromName('NUTS2') == -1:
        buildingsLayer.dataProvider().addAttributes([QgsField('NUTS2', QVariant.String)])
        buildingsLayer.updateFields()

    if buildingsLayer.fields().indexFromName('BuildingFP_area') == -1:
        buildingsLayer.dataProvider().addAttributes([QgsField('BuildingFP_area', QVariant.Double)])
        buildingsLayer.updateFields()

    # Extract the indexes
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Extracting the indexes...')
    indexNUTS3 = buildingsLayer.fields().indexFromName('NUTS3')
    indexNUTS2 = buildingsLayer.fields().indexFromName('NUTS2')
    indexAREA = buildingsLayer.fields().indexFromName('BuildingFP_area')
    
    # Update the features
    buildingsLayerIndex = QgsSpatialIndex(buildingsLayer.getFeatures())
    featuresToUpdate, nProcessed = [], 0
    for nutsFeat in nutsLayer.getFeatures():
        if nutsFeat['LEVL_CODE'] != 3:
            continue

        nuts3Id = nutsFeat['NUTS_ID']
        intersectingIds = buildingsLayerIndex.intersects(nutsFeat.geometry().boundingBox())
        intersectingFeatures = buildingsLayer.getFeatures(QgsFeatureRequest().setFilterFids(intersectingIds))
        for buildingFeat in intersectingFeatures:
            if nutsFeat.geometry().intersects(buildingFeat.geometry()):
                # Assign NUTS3
                buildingFeat['NUTS3'] = nuts3Id
                # Assign NUTS2
                buildingFeat['NUTS2'] = nutsId[:4]
                # Calculate the AREA
                buildingFeat['BuildingFP_area'] = buildingFeat.geometry().area()
                featuresToUpdate.append(buildingFeat)

            if len(featuresToUpdate) >= 2000:
                changes = {feature.id(): {
                    indexNUTS3: feature['NUTS3'],
                    indexNUTS2: feature['NUTS2'],
                    indexAREA: feature['BuildingFP_area']} for feature in featuresToUpdate
                }
                dataProvider = buildingsLayer.dataProvider()
                dataProvider.changeAttributeValues(changes)
                featuresToUpdate = []
                nProcessed += 5000
    
    if featuresToUpdate:
        changes = {feature.id(): {
            indexNUTS3: feature['NUTS3'],
            indexNUTS2: feature['NUTS2'],
            indexAREA: feature['BuildingFP_area']} for feature in featuresToUpdate
        }
        dataProvider = buildingsLayer.dataProvider()
        dataProvider.changeAttributeValues(changes)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> ' +\
        str(nProcessed) + ' buildings processed')
    
    # Eliminate all geometries with an area of less than 30m².
    expression = QgsExpression(' "BuildingFP_area" < 30 ')
    ids = [f.id() for f in buildingsLayer.getFeatures(QgsFeatureRequest(expression))]
    buildingsLayer.dataProvider().deleteFeatures(ids)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Deleted ' + str(len(ids)) + ' buildings (area of less than 30m²)')
    
    # Get a list of entity IDs that have the field ‘NUTS3’ as NULL
    expression = QgsExpression(' "NUTS3" is NULL ')
    ids = [f.id() for f in buildingsLayer.getFeatures(QgsFeatureRequest(expression))]
    buildingsLayer.dataProvider().deleteFeatures(ids)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Removed ' + str(len(ids)) + ' features out of boundary')
    
    # Commit changes
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Commiting changes...')
    buildingsLayer.commitChanges()
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> [OK]')
    logging.info('')


# Function: Build. Energy Sim. -> Preprocess -> Step 10 -> Calculate height volumes
def bp1Step10(buildingsLayer, rasterHeightLayer):
    '''
    Build. Energy Sim. -> Preprocess -> Step 10 : Calculate height volumes.
    This function calculates the number of floors, GFA and volume of each building in the 'buildings'
    layer based on the'GHS_Heightmean' attribute.
    If a building doesn't have 'GHS_Heightmean' (height), the value is calculated from a raster
    layer with height data ('raster_height').
    '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> Calculating heights and volumes...')
    buildingsLayer.startEditing()
    if 'GHS_Heightmean' in [field.name() for field in buildingsLayer.fields()]:
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> The field "GHS_Heightmean" already exists!')
    else:
        prefix = 'GHS_Height'
        statsToCalculate = QgsZonalStatistics.Mean
        zonalStats = QgsZonalStatistics(buildingsLayer, rasterHeightLayer, 'GHS_Height', 1, statsToCalculate)
        zonalStats.calculateStatistics(None)
    
    # Define the list of fields to be added
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> Defining the list of fields to be added...')
    fieldsToAdd = ['N_Floors', 'Building_GFA', 'Volume']

    # Create the fields (if they do not exist)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> Creating the fields (can take quite a while)...')
    if not all(field in [field.name() for field in buildingsLayer.fields()] for field in fieldsToAdd):
        buildingsLayer.dataProvider().addAttributes([QgsField(field, QVariant.Double) for field in fieldsToAdd])
        buildingsLayer.updateFields()
    else:
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> All the fields already exist!')
    
    # Calculate 'N_Floors' as a function of 'GHS_Heightmean' and GFA with N_floors
    counter = 0
    for feature in buildingsLayer.getFeatures():
        counter += 1
        GHSHeightmean = feature['GHS_Heightmean']
        if not GHSHeightmean or GHSHeightmean == 0:
            GHSHeightmean = 3.5
        elif 0 <= GHSHeightmean < 2.5:
            GHSHeightmean = 2.5
            
        # Updating GHS_Heightmean on the feature
        feature['GHS_Heightmean'] = GHSHeightmean
        
        # Calculate and update 'N_Floors'
        feature['N_Floors'] = round(GHSHeightmean / 3)
        
        # Calculate building GFA and update
        feature['Building_GFA'] = feature['N_Floors'] * feature['BuildingFP_area']
        feature['Volume'] = feature['GHS_Heightmean'] * feature['BuildingFP_area']
        buildingsLayer.updateFeature(feature)

    # Commit changes
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> Commiting changes...')
    buildingsLayer.commitChanges()

    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> [OK]')
    logging.info('')


# Function: Build. Energy Sim. -> Preprocess -> Step 11 -> Calculate statistics and mapping
def bp1Step11(buildingsLayer, rasterUseLayer, landUseLayer, mappingCsvObj, config):
    '''
    Build. Energy Sim. -> Preprocess -> Step 11 : Calculate statistics and mapping.
    This function calculates the majority use for each building from a raster layer ('rasterUseLayer') and
    a vector layer with classified land use data ('land_use').
    The function also maps the use to defined groups, sub-sectors, and sectors according to a mapping
    table stored in a CSV file ('MappingCsvPath').
    '''
    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> Calculating statistics and mapping...')
    csvPath = io.retrieveBasePath(config) + mappingCsvObj['path']
    
    # Calculate zone statistics with majority value
    if 'GHS_Majority' in [field.name() for field in buildingsLayer.fields()]:
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> The field "GHS_Majority" anready exists!')
    else:
        zonalStats = QgsZonalStatistics(buildingsLayer, rasterUseLayer, 'GHS_', stats = QgsZonalStatistics.Majority)
        zonalStats.calculateStatistics(None)

    # Create spatial index for the Land Use layer
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> Creating spatial index for the Land Use layer...')
    index = QgsSpatialIndex(landUseLayer.getFeatures())
    
    # Create a dictionary from the CSV file
    mappingDict = {}
    with open(csvPath, mode = 'r') as fil:
        reader = csv.reader(fil, delimiter = ';')
        next(reader)  # To skip the headers
        for row in reader:
            mappingDict[row[0]] = row[1:]

    # Create new columns in the buildings layer
    fields = ['Group', 'Sub_sector', 'Sector', 'Combined_Use']
    for field in fields:
        buildingsLayer.dataProvider().addAttributes([QgsField(field, QVariant.String)])
    buildingsLayer.updateFields()

    totalFeatures = buildingsLayer.featureCount()
    percentageIncrement = totalFeatures // 10
    
    buildingsLayer.startEditing()
    
    # Allocation of uses and mapping
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> Starting use allocation/mapping (can take quite a while)...')
    for feature in buildingsLayer.getFeatures():
        typeValue = str(feature['type'])
        
        # Check if the 'type' field exists and is not empty
        if not typeValue or typeValue.isspace() or typeValue in ['NULL', 'None', 'none', '']:
            finalUse = 'unknown'
            landUseValue = None
            geom = feature.geometry()
            intersects = index.intersects(geom.boundingBox())
            for i in intersects:
                landUseFeat = landUseLayer.getFeature(i)
                if landUseFeat.geometry().intersects(geom):
                    landUseValue = landUseFeat['fclass']
                    break

            ghsMajority = feature['GHS_Majority']
            if landUseValue in ('industrial', 'retail', 'military', 'commercial'):
                finalUse = landUseValue
            elif ghsMajority == 0 or ghsMajority == 1:
                finalUse = 'residential'
            elif ghsMajority == 2:
                finalUse = 'other non-residential'
            feature['Combined_Use'] = finalUse
        else:
            feature['Combined_Use'] = typeValue

        combinedUse = feature['Combined_Use']
        if combinedUse not in mappingDict:
            combinedUse = 'other non-residential'.capitalize()

        if combinedUse in mappingDict:
            feature['Group'] = mappingDict[combinedUse][0]
            feature['Sub_sector'] = mappingDict[combinedUse][1]
            feature['Sector'] = mappingDict[combinedUse][2]
            if feature['Sub_sector'] == 'Apartment blocks' and feature['N_floors'] < 3:
                feature['Sub_sector'] = 'Single family- Terraced houses'
            elif feature['Sub_sector'] == 'Single family- Terraced houses' and feature['N_floors'] > 3:
                feature['Sub_sector'] = 'Apartment blocks'

        buildingsLayer.updateFeature(feature)
        
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> Use allocation and mapping completed!')
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> [OK]')
    logging.info('')


# Function: Build. Energy Sim. -> Preprocess -> Step 12 -> Adjoin facade calculations
def bp1Step12(isTest, config):
    '''
    Build. Energy Sim. -> Preprocess -> Step 12 : Adjoin facade calculations.
    This function calculates the length of the adjoining perimeter (facade) and the ratio of this length to the total
    perimeter of each building. Buildings with a ratio equal to or above 1 are removed, and the calculations are performed
    again for the buildings affected by these removals. The results are stored in a new GeoDataFrame returned by the function.
    '''
    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Adjoining facade calculations...')
    
    # Load the building layer from the GPKG file
    buildingsPath = config['IDESIGNRES-PATH']['idesignres.path.bp.test']\
        if isTest else config['IDESIGNRES-PATH']['idesignres.path.bp.test']
    buildings = gpd.read_file(buildingsPath)
    
    # Ensure that the geometry is of type Polygon or Multipolygon.
    buildings = buildings[buildings.geometry.type.isin(['Polygon', 'MultiPolygon'])]
    buildings['adjoining_perimeter'] = 0.0
    
    # Create a spatial index (R-tree) for buildings
    sindex = buildings.sindex
    
    #####
    
    # Funtion (internal): Calculate adjoining
    def calculateAdjoining(currentBuildings, sindex, allBuildings):
        # Iterate on each building to calculate its dividing façade
        for idx, building in currentBuildings.iterrows():
            adjoiningPerimeter = 0.0

            # Get the perimeter of the current building as a line (LineString)
            buildingPerimeter = building.geometry.boundary

            # Obtain the length of the perimeter
            perimeter = buildingPerimeter.length

            # Obtain the bounding box of the current building
            bbox = building.geometry.bounds

            # Find possible intersections with the spatial index
            possibleIntersections = list(sindex.intersection(bbox))

            # Iterate on buildings selected by the spatial index
            for idxOthers in possibleIntersections:
                if idxOthers == idx:
                    continue  # Ignore the same building

                bboxBuildings = allBuildings.iloc[idxOthers]

                # Calculate the intersection between the perimeter of the building and the other building
                intersection = buildingPerimeter.intersection(bboxBuildings.geometry)

                # If the intersection is of type LineString or MultiLineString, add length
                if isinstance(intersection, LineString):
                    adjoiningPerimeter += intersection.length
                elif intersection.geom_type == 'MultiLineString':
                    adjoiningPerimeter += sum(line.length for line in intersection.geoms)

                # Save the length of the party wall and the perimeter in the column
                currentBuildings.at[idx, 'adjoining_perimeter'] = adjoiningPerimeter

            currentBuildings.at[idx, 'perimeter'] = perimeter
        
            # Calculate the ratio adj_facade / perimeter
            currentBuildings.at[idx, 'Ratio'] = adjoiningPerimeter / perimeter if perimeter > 0 else 0
    
    #####
    
    # Funtion (internal): Find adjacents
    def findAdjacents(currentBuildings, sindex):
        # Iterate over each building to look for adjacent buildings
        adjacents = set()
        for idx, building in currentBuildings.iterrows():
            # Get the bounding box of the current building
            bbox = building.geometry.bounds

            # Find possible intersections with the spatial index
            possibleIntersections = list(sindex.intersection(bbox))

            # Update
            adjacents.update(possibleIntersections)

        # Return a DataFrame with adjacent buildings
        return buildings.iloc[list(adjacents)].copy()

    #####
    
    # Calculate adjoining for all buildings
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Calculate adjoining for all buildings...')
    calculateAdjoining(buildings, sindex, buildings)
    
    # Filter buildings where Ratio is >= 1
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Filtering buildings where Ratio >= 1...')
    toRemove = buildings[buildings['Ratio'] >= 1].copy()

    # Obtain adjacencies for buildings to be removed
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Finding adjancencies for buildings to be removed...')
    toRecalculate = findAdjacents(toRemove, sindex)
    
    # Remove buildings with Ratio >= 1
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Removing buildings where Ratio >= 1...')
    buildings = buildings[buildings['Ratio'] < 1]

    # Recalculating adjoining buildings
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Recalculating adjoining buildings...')
    calculateAdjoining(toRecalculate, sindex, buildings)

    # Merge recalculated buildings again
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Merging recalculated buildings...')
    buildings.update(toRecalculate)
    
    # Save the result in a new GPKG file
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Saving to a new GeoPackage file...')
    buildings.to_file(buildingsPath, driver = 'GPKG')

    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> [OK]')
    logging.info('')
    return buildings


# Function: Build. Energy Sim. -> Preprocess -> Step 13 -> Mask raster layers
def bp1Step13(layerList, config):
    ''' Build. Energy Sim. -> Preprocess -> Step 13 : Mask raster layers. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 13 -> Masking raster layers (can take quite a while)...')
    
    # Retrieve the necessary paths
    clippedRastersPaths = []
    layers = [{'name': layerList[8]['name'], 'path': io.retrieveBasePath(config) +\
        layerList[8]['path'], 'format': layerList[8]['format']},
            {'name': layerList[5]['name'], 'path': io.retrieveBasePath(config) +\
        layerList[8]['path'], 'format': layerList[8]['format']},
            {'name': layerList[4]['name'], 'path': io.retrieveBasePath(config) +\
        layerList[8]['path'], 'format': layerList[8]['format']},
            {'name': layerList[3]['name'], 'path': io.retrieveBasePath(config) +\
        layerList[8]['path'], 'format': layerList[8]['format']},
            {'name': layerList[7]['name'], 'path': io.retrieveBasePath(config) +\
        layerList[8]['path'], 'format': layerList[8]['format']}]
    nutsLayerPath = io.retrieveBasePath(config) + layerList[0]['path']
    
    for layer in layers:
        gdf = gpd.read_file(nutsLayerPath)
        geoms = gdf.geometry.values

        with rasterio.open(layer['path']) as src:
            out_image, out_transform = mask(src, geoms, crop=True)
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
                "compress": 'lzw'
            })
        
        # Save the temporary layer
        output = io.buildOutputPathBPStep13(layer['name'], layer['format'], config)
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 13 -> Saving: ' + output + '...')
        with rasterio.open(output, "w", **out_meta) as dst:
            dst.write(out_image)
        clippedRastersPaths.append(output)
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 13 -> [OK]')
    logging.info('')
    return clippedRastersPaths


# Function: Build. Energy Sim. -> Preprocess -> Step 14 -> Process clipped layers
def bp1Step14(nutsId, clipped, excelFile, downloadFolder, config):
    ''' Build. Energy Sim. -> Preprocess -> Step 14 : Process clipped layers. '''

    # CSV file with the percentages per country and year
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Loading the Excel file to calculate the percentages...')
    dfShareYears = pd.read_excel(io.retrieveBasePath(config) + excelFile['path'])
    
    # Dictionary that will contain the 'layer' data
    layersDict = {}
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Calculating the percentages...')
    countryPctBefore1945 = dfShareYears.loc[dfShareYears['NUTS_ID'] == nutsId[:2], 'Before 1945'].values[0]
    countryPct19451969 = dfShareYears.loc[dfShareYears['NUTS_ID'] == nutsId[:2], '1945 - 1969'].values[0]
    countryPct19701979 = dfShareYears.loc[dfShareYears['NUTS_ID'] == nutsId[:2], '1970 - 1979'].values[0]
    countryPct19801989 = dfShareYears.loc[dfShareYears['NUTS_ID'] == nutsId[:2], '1980 - 1989'].values[0]
    
    totalMem, usedMem, freeMem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (1) -> ' +\
        str(round((usedMem / totalMem) * 100, 2)) + '%')
    
    chunkSize = int(config['IDESIGNRES-PARAMETERS']['idesignres.params.chunk.size'])
    with rasterio.open(clipped[4]) as src2020, rasterio.open(clipped[0]) as src1975:
        ratio = np.zeros((src1975.height, src1975.width), dtype = np.float16)
        for rowOff in range(0, src1975.height, chunkSize):
            for colOff in range(0, src1975.width, chunkSize):
                window = rasterio.windows.Window(colOff, rowOff, chunkSize, chunkSize)
                cRatio = np.divide(
                    src1975.read(1, window = window).astype(np.float16),
                    src2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src1975.read(1, window = window).astype(np.float16)),
                    where = (src2020.read(1, window = window).astype(np.float16) != 0))
                ratio[rowOff:rowOff + chunkSize, colOff:colOff + chunkSize] = cRatio
        layersDict["Before1945"] = (ratio * countryPctBefore1945, src1975.profile)
        layersDict["1945to1969"] = (ratio * countryPct19451969, src1975.profile)
        del cRatio, ratio
        gc.collect()

    totalMem, usedMem, freeMem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (2) -> ' +\
        str(round((usedMem / totalMem) * 100, 2)) + '%')
    
    with rasterio.open(clipped[4]) as src2020, rasterio.open(clipped[0]) as src1975, rasterio.open(clipped[1]) as src_1990:
        diff = np.zeros((src1975.height, src1975.width), dtype = np.float16)
        for rowOff in range(0, src1975.height, chunkSize):
            for colOff in range(0, src1975.width, chunkSize):
                window = rasterio.windows.Window(colOff, rowOff, chunkSize, chunkSize)
                cDiff = np.divide(src_1990.read(1, window = window).astype(np.float16) -\
                    src1975.read(1, window = window).astype(np.float16),
                    src2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src1975.read(1, window = window).astype(np.float16)),
                    where = (src2020.read(1, window = window).astype(np.float16) != 0))
                diff[rowOff:rowOff + chunkSize, colOff:colOff + chunkSize] = cDiff
        layersDict["1970to1979"] = (diff * countryPct19701979, src1975.profile)
        layersDict["1980to1989"] = (diff * countryPct19801989, src1975.profile)
        del cDiff, diff
        gc.collect()

    totalMem, usedMem, freeMem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (3) -> ' +\
        str(round((usedMem / totalMem) * 100, 2)) + '%')

    with rasterio.open(clipped[4]) as src2020, rasterio.open(clipped[1]) as src_1990, rasterio.open(clipped[2]) as src_2000:
        diff = np.zeros((src2020.height, src2020.width), dtype = np.float16)
        for rowOff in range(0, src2020.height, chunkSize):
            for colOff in range(0, src2020.width, chunkSize):
                window = rasterio.windows.Window(colOff, rowOff, chunkSize, chunkSize)
                cDiff = np.divide(src_2000.read(1, window = window).astype(np.float16) -\
                    src_1990.read(1, window = window).astype(np.float16),
                    src2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src_1990.read(1, window = window).astype(np.float16)),
                    where = (src2020.read(1, window = window).astype(np.float16) != 0))
                diff[rowOff:rowOff + chunkSize, colOff:colOff + chunkSize] = cDiff
        layersDict["1990to2000"] = (diff, src_1990.profile)
        del cDiff, diff
        gc.collect()
    
    totalMem, usedMem, freeMem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (4) -> ' +\
        str(round((usedMem / totalMem) * 100, 2)) + '%')

    with rasterio.open(clipped[4]) as src2020, rasterio.open(clipped[2]) as src_2000, rasterio.open(clipped[3]) as src_2010:
        diff = np.zeros((src2020.height, src2020.width), dtype = np.float16)
        for rowOff in range(0, src2020.height, chunkSize):
            for colOff in range(0, src2020.width, chunkSize):
                window = rasterio.windows.Window(colOff, rowOff, chunkSize, chunkSize)
                cDiff = np.divide(src_2010.read(1, window = window).astype(np.float16) -\
                    src_2000.read(1, window = window).astype(np.float16),
                    src2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src_2000.read(1, window = window).astype(np.float16)),
                    where = (src2020.read(1, window = window).astype(np.float16) != 0))
                diff[rowOff:rowOff + chunkSize, colOff:colOff + chunkSize] = cDiff
        layersDict["2000to2010"] = (diff, src_1990.profile)
        del cDiff, diff
        gc.collect()

    totalMem, usedMem, freeMem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (5) -> ' +\
        str(round((usedMem / totalMem) * 100, 2)) + '%')
    
    with rasterio.open(clipped[4]) as src2020, rasterio.open(clipped[3]) as src_2010:
        diff = np.zeros((src2020.height, src2020.width), dtype = np.float16)
        for rowOff in range(0, src2020.height, chunkSize):
            for colOff in range(0, src2020.width, chunkSize):
                window = rasterio.windows.Window(colOff, rowOff, chunkSize, chunkSize)
                cDiff = np.divide(src2020.read(1, window = window).astype(np.float16) -\
                    src_2010.read(1, window = window).astype(np.float16),
                    src2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src_2010.read(1, window = window).astype(np.float16)),
                    where = (src2020.read(1, window = window).astype(np.float16) != 0))
                diff[rowOff:rowOff + chunkSize, colOff:colOff + chunkSize] = cDiff
        layersDict["Post2010"] = (diff, src_1990.profile)
        del cDiff, diff
        gc.collect()
    
    totalMem, usedMem, freeMem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (6) -> ' +\
        str(round((usedMem / totalMem) * 100, 2)) + '%')
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> [OK]')
    logging.info('')
    return layersDict


# Function: Build. Energy Sim. -> Preprocess -> Step 15 -> Assign year info
def bp1Step15(nutsId, buildings, layersDict, excelFile, config):
    ''' Build. Energy Sim. -> Preprocess -> Step 15 : Assign year info. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 15 -> Assigning year info...')
    for rasterName, (rasterData, transform) in layersDict.items():
        buildings[rasterName] = buildings.geometry.centroid.apply(\
            lambda point: getPixelValue(point.x, point.y, rasterData, transform))
            
    # Assign value = 1 to the field with the highest % of built-up area in all those records where there is no year information
    columnsToCheck = ['Before1945', '1945to1969', '1970to1979', '1980to1989', '1990to2000', '2000to2010', 'Post2010']

    # Get the 'MostCommon' column for this particular 'country_code'.
    dfShareYears = pd.read_excel(io.retrieveBasePath(config) + excelFile['path'])
    mostCommonColumn = dfShareYears.loc[dfShareYears['NUTS_ID'].str[:2] == nutsId[:2], 'MostCommon'].values[0]

    # Check if all values in the columns are 0 (which means no data available)
    condition = (buildings[columnsToCheck] == 0).all(axis = 1)

    # Assign 1 to the corresponding column in the rows where all values are 0
    buildings.loc[condition, mostCommonColumn] = 1
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 15 -> [OK]')
    logging.info('')
    return buildings


# Function: Build. Energy Sim. -> Preprocess -> Step 16 -> Calculate additional info
def bp1Step16(buildings):
    ''' Build. Energy Sim. -> Preprocess -> Step 16 : Calculate additional info. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 16 -> Calculating additional info...')
    
    # Calculation of built-up area per year from share data
    buildings['Before1945_A'] = buildings['Before1945'] * buildings['Building_GFA']
    buildings['1945to1969_A'] = buildings['1945to1969'] * buildings['Building_GFA']
    buildings['1970to1979_A'] = buildings['1970to1979'] * buildings['Building_GFA']
    buildings['1980to1989_A'] = buildings['1980to1989'] * buildings['Building_GFA']
    buildings['1990to2000_A'] = buildings['1990to2000'] * buildings['Building_GFA']
    buildings['2000to2010_A'] = buildings['2000to2010'] * buildings['Building_GFA']
    buildings['Post2010_A'] = buildings['Post2010'] * buildings['Building_GFA']

    # Calculation of additional parameters
    buildings['ExtFachadeArea'] = (buildings['perimeter'] - buildings['adjoining_perimeter']) * buildings['GHS_Heightmean']
    buildings['%ExtFachade'] = 1 - (buildings['adjoining_perimeter'] / buildings['perimeter'])
    buildings.loc[buildings['%ExtFachade'] < 0, '%ExtFachade'] = 0
    buildings['ShapeFactor'] = ((buildings['perimeter'] * buildings['GHS_Heightmean'] +\
        buildings['BuildingFP_area'] * 2)) / buildings['Volume']
    buildings['R_WalltoGFA'] = (buildings['perimeter'] * buildings['GHS_Heightmean']) / buildings['Building_GFA']
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 16 -> [OK]')
    logging.info('')
    return buildings


# Function: Build. Energy Sim. -> Preprocess -> Step 17 -> Prepare clustering
def bp1Step17(buildings):
    ''' Build. Energy Sim. -> Preprocess -> Step 17 : Prepare clustering. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 17 -> Preparing clustering...')
    
    # Filter the dataframe to keep only those in the Sub_sector field that are 'Apartment block'
    apartmentBlock = buildings[buildings['Sub_sector'] == 'Apartment blocks']

    # Check if there are no buildings in the Sub_sector 'Apartment block'
    if apartmentBlock.empty:
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 17 -> No empty buildings for "Apartment block" Subsector!')
        return pd.DataFrame()

    # The years / periods we are going to use
    periods = ['Before1945', '1945to1969', '1970to1979', '1980to1989', '1990to2000', '2000to2010', 'Post2010']

    # Duplicate rows for each period
    def expandRow(row):
        periodData = []
        for period in periods:
            newRow = row.copy()
            newRow['Period'] = period
            newRow['BuiltArea_ShareYears'] = row['Building_GFA'] * row[period]
            periodData.append(newRow.to_dict())
        return periodData

    # Duplicate rows 7 times and apply 'expandRow' to each row
    expandedData = apartmentBlock.apply(expandRow, axis = 1)

    # Concatenate all dictionaries returned by 'expandRow' into a single dataframe
    dfAB = pd.DataFrame([item for sublist in expandedData for item in sublist])
    
    # Filter the dataframe to keep only those in the Sub_sector field that are 'Single family- Terraced houses'.
    dfSFH = buildings[buildings['Sub_sector'] == 'Single family- Terraced houses']
    
    # Filter the dataframe to keep only those in the Sector field that are 'Service sector'
    dfSS = buildings[buildings['Sector'] == 'Service sector']
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 17 -> [OK]')
    logging.info('')
    return dfAB, dfSFH, dfSS


# Function: Build. Energy Sim. -> Preprocess -> Step 18 -> Perform clustering (AB)
def bp1Step18(dfAB, nClustersAB):
    ''' Build. Energy Sim. -> Preprocess -> Step 09 : Perform clustering (AB). '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 18 -> Performing clustering (AB)...')

    dfAllYears = pd.DataFrame()
    dfClustersAB = pd.DataFrame(
        columns = ['Sub_sector', 'Cluster', 'Centroid_GHS_Heightmean', 'Centroid_ExtFachade', 'Centroid_ShapeFactor'])

    def calculateDistance(row, centroid):
        return np.sqrt(
            (row['%ExtFachade'] - centroid['%ExtFachade']) ** 2
            + (row['ShapeFactor'] - centroid['ShapeFactor']) ** 2
            + (row['GHS_Heightmean'] - centroid['GHS_Heightmean']) ** 2)

    periodToYear = {
        'Before1945': 1900,
        '1945to1969': 1955,
        '1970to1979': 1975,
        '1980to1989': 1985,
        '1990to2000': 1995,
        '2000to2010': 2005,
        'Post2010': 2020
    }

    for period in dfAB['Period'].unique():
        dfPeriod = dfAB.loc[dfAB['Period'] == period].copy()
        dfPeriod['Year'] = periodToYear[period]
        dfPeriod['NormalizedBuiltArea'] = dfPeriod['BuiltArea_ShareYears'] / dfPeriod['BuiltArea_ShareYears'].sum()
        weights = dfPeriod['NormalizedBuiltArea'].values

        dfClustering = dfPeriod[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']]
        scaler = StandardScaler()
        dfScaled = scaler.fit_transform(dfClustering)

        # Adjust the KMeans model
        km = KMeans(n_clusters = nClustersAB, max_iter = 8000)
        dfPeriod['cluster'] = km.fit_predict(dfScaled, sample_weight = weights)
        dfPeriod['cluster'] = dfPeriod['cluster'].apply(lambda x: f"{x}_{period}")
        centroids = dfPeriod.groupby('cluster')[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']].mean()
        
        # Calculate the distance from each entity to the centroid
        dfPeriod['distance'] = dfPeriod.apply(lambda row: calculateDistance(row, centroids.loc[row['cluster']]), axis = 1)
        dfPeriodCentroidOsmIds = dfPeriod.loc[dfPeriod.groupby('cluster')['distance'].idxmin()]
        dfCentroidOsmIds = dfPeriodCentroidOsmIds.set_index('cluster')['osm_id']
        dfPeriod['centroid_osm_id'] = dfPeriod['cluster'].apply(lambda x: 1\
            if dfCentroidOsmIds[x] in dfPeriod['osm_id'].values else 0)
        sumGFArea = dfPeriod.groupby('cluster')['BuiltArea_ShareYears'].sum()
        dfAllYears = pd.concat([dfAllYears, dfPeriod])

        # Stores the information in df_clusters and then prints the centroids and nearest entities for each cluster
        for cluster in dfPeriod['cluster'].unique():
            centroid = centroids.loc[cluster]
            closestEntity = dfPeriod[dfPeriod['osm_id'] == dfCentroidOsmIds[cluster]]
            dfNew = pd.DataFrame([{'Period': period,
                'Cluster': cluster, 'Centroid_GHS_Heightmean': centroid['GHS_Heightmean'],
                'Centroid_ExtFachade': centroid['%ExtFachade'],
                'Centroid_ShapeFactor': centroid['ShapeFactor'],
                'Closest_Entity_OSM_ID': closestEntity['osm_id'].values[0],
                'Closest_Entity_FootprintArea': closestEntity['BuildingFP_area'].values[0],
                'Closest_Entity_GFA': closestEntity['Building_GFA'].values[0],
                'Closest_Entity_Height': closestEntity['GHS_Heightmean'].values[0],
                'Closest_Entity_N_floors': closestEntity['N_Floors'].values[0],
                'Closest_Entity_Volume': closestEntity['Volume'].values[0],
                'Closest_Entity_TotalPerimeter': closestEntity['perimeter'].values[0],
                'Closest_Entity_%ExtFachade': closestEntity['%ExtFachade'].values[0],
                'Closest_Entity_R_WalltoGFA': closestEntity['R_WalltoGFA'].values[0],
                'Closest_Entity_ShapeFactor': closestEntity['ShapeFactor'].values[0],
                'Year': dfPeriod['Year'].iloc[0], 'Area': sumGFArea[cluster]}])

            dfNew = dfNew.dropna(how='all', axis = 1)
            dfNew = dfNew.dropna(how='all', axis = 0)
            dfClustersAB = dfClustersAB.dropna(how = 'all', axis = 1)
            dfClustersAB = dfClustersAB.dropna(how = 'all', axis = 0)
            dfClustersAB = pd.concat([dfClustersAB, dfNew]).reset_index(drop = True)

    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 18 -> [OK]')
    logging.info('')
    return dfClustersAB


# Function: Build. Energy Sim. -> Preprocess -> Step 19 -> Perform clustering (SFH)
def bp1Step19(dfSFH, nClustersSFH):
    ''' Build. Energy Sim. -> Preprocess -> Step 19 : Perform clustering (SFH). '''
   
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 19 -> Performing clustering (SFH)...')
    
    dfAllSubSector = pd.DataFrame()
    dfClustersSFH = pd.DataFrame(
        columns = ['Sub_sector', 'Cluster', 'Centroid_GHS_Heightmean', 'Centroid_ExtFachade', 'Centroid_ShapeFactor'])

    def calculateDistance(row, centroid):
        return np.sqrt(
            (row['%ExtFachade'] - centroid['%ExtFachade']) ** 2
            + (row['ShapeFactor'] - centroid['ShapeFactor']) ** 2
            + (row['GHS_Heightmean'] - centroid['GHS_Heightmean']) ** 2)

    # Iterating over each unique Sub_sector in the dataset
    for Sub_sector in dfSFH['Sub_sector'].unique():
        # Selecting the rows for specific Sub_sector
        dfSubsector = dfSFH.loc[dfSFH['Sub_sector'] == Sub_sector].copy()
        dfSubsector['NormalizedBuiltArea'] = dfSubsector['Building_GFA'] / dfSubsector['Building_GFA'].sum()
        weights = dfSubsector['NormalizedBuiltArea'].values
        dfClustering = dfSubsector[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']]
        
        # Scaling the features to have zero mean and unit variance using StandardScaler for optimal performance
        scaler = StandardScaler()
        dfScaled = scaler.fit_transform(dfClustering)

        # Applying KMeans clustering algorithm
        km = KMeans(n_clusters = nClustersSFH, max_iter = 8000)
        dfSubsector['cluster'] = km.fit_predict(dfScaled, sample_weight = weights)

        # Assign a unique cluster identifier for each Sub_sector
        dfSubsector['cluster'] = dfSubsector['cluster'].apply(lambda x: f"{x}_{Sub_sector}")

        # Compute the centroids of each cluster
        centroids = dfSubsector.groupby('cluster')[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']].mean()
        dfSubsector['distance'] = dfSubsector.apply(lambda row: calculateDistance(row, centroids.loc[row['cluster']]), axis = 1)
        dfSubsectorCentroidOsmIds = dfSubsector.loc[dfSubsector.groupby('cluster')['distance'].idxmin()]
        dfCentroidOsmIds = dfSubsectorCentroidOsmIds.set_index('cluster')['osm_id']
        dfSubsector['centroid_osm_id'] = dfSubsector['cluster'].apply(
            lambda x: 1 if dfCentroidOsmIds[x] in dfSubsector['osm_id'].values else 0)
        sumGFArea = dfSubsector.groupby('cluster')['Building_GFA'].sum()

        dfAllSubSector = pd.concat([dfAllSubSector, dfSubsector])
        for cluster in dfSubsector['cluster'].unique():
            centroid = centroids.loc[cluster]
            closestEntity = dfSubsector[dfSubsector['osm_id'] == dfCentroidOsmIds[cluster]]
            dfNew = pd.DataFrame([{'Sub_sector': Sub_sector,
                'Cluster': cluster, 'Centroid_GHS_Heightmean': centroid['GHS_Heightmean'],
                'Centroid_ExtFachade': centroid['%ExtFachade'],
                'Centroid_ShapeFactor': centroid['ShapeFactor'],
                'Closest_Entity_OSM_ID': closestEntity['osm_id'].values[0],
                'Closest_Entity_FootprintArea': closestEntity['BuildingFP_area'].values[0],
                'Closest_Entity_GFA': closestEntity['Building_GFA'].values[0],
                'Closest_Entity_Height': closestEntity['GHS_Heightmean'].values[0],
                'Closest_Entity_N_floors': closestEntity['N_Floors'].values[0],
                'Closest_Entity_Volume': closestEntity['Volume'].values[0],
                'Closest_Entity_TotalPerimeter': closestEntity['perimeter'].values[0],
                'Closest_Entity_%ExtFachade': closestEntity['%ExtFachade'].values[0],
                'Closest_Entity_R_WalltoGFA': closestEntity['R_WalltoGFA'].values[0],
                'Closest_Entity_ShapeFactor': closestEntity['ShapeFactor'].values[0],
                'Sum_GFArea': sumGFArea[cluster]}])

            dfNew = dfNew.dropna(how = 'all', axis = 1)
            dfNew = dfNew.dropna(how = 'all', axis = 0)
            dfClustersSFH = dfClustersSFH.dropna(how = 'all', axis = 1)
            dfClustersSFH = dfClustersSFH.dropna(how = 'all', axis = 0)
            dfClustersSFH = pd.concat([dfClustersSFH, dfNew]).reset_index(drop = True)

    # Conversion of 'Period' to 'Year' through a dictionary mapping
    periodToYear = {
        'Before1945': 1900,
        '1945to1969': 1955,
        '1970to1979': 1975,
        '1980to1989': 1985,
        '1990to2000': 1995,
        '2000to2010': 2005,
        'Post2010': 2020
    }

    # Iterate over each row in dfClustersSFH
    newRows = []
    for _, row in dfClustersSFH.iterrows():
        for period, year in periodToYear.items():
            newRow = row.copy()
            newRow['Period'] = period
            newRow['Year'] = year
            newRows.append(newRow)
    dfExpanded = pd.DataFrame(newRows)

    # Reset the index of the expanded DataFrame
    dfExpanded.reset_index(drop = True, inplace = True)

    # First, 'melt' dfAllSubSector to get a row for each cluster and period
    dfArea = dfAllSubSector.melt(id_vars = ['cluster'],
        value_vars = [c for c in dfAllSubSector.columns if c.endswith('_A')],
        var_name = 'Period',
        value_name = 'Area')

    # Remove the '_A' from the end of the period
    dfArea['Period'] = dfArea['Period'].str.rstrip('_A')

    # Sum the area values by cluster and period
    dfArea = dfArea.groupby(['cluster', 'Period'])['Area'].sum().reset_index()

    # Create a combined index column for dfArea
    dfArea['merge_index'] = dfArea['cluster'] + dfArea['Period']

    # Create a combined index column for dfExpanded
    dfExpanded['merge_index'] = dfExpanded['Cluster'] + dfExpanded['Period']

    # Sort dfArea by this combined index
    dfArea.sort_values('merge_index', inplace = True)

    # Create a new df that merges on 'merge_index'
    dfMergedSFH = dfExpanded.merge(dfArea, how = 'left', on = 'merge_index')

    # Now we no longer need the 'merge_index' column
    dfMergedSFH.drop(columns = 'merge_index', inplace = True)
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 19 -> [OK]')
    logging.info('')
    return dfMergedSFH


# Function: Build. Energy Sim. -> Preprocess -> Step 20 -> Perform clustering (SS)
def bp1Step20(dfSS, nClustersSS):
    ''' Build. Energy Sim. -> Preprocess -> Step 20 : Perform clustering (SS). '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 20 -> Performing clustering (SS)...')
    
    dfAllSubSector = pd.DataFrame()
    dfClustersSS = pd.DataFrame(
        columns = ['Sub_sector', 'Cluster', 'Centroid_GHS_Heightmean', 'Centroid_ExtFachade', 'Centroid_ShapeFactor'])

    def calculateDistance(row, centroid):
        return np.sqrt(
            (row['%ExtFachade'] - centroid['%ExtFachade']) ** 2
            + (row['ShapeFactor'] - centroid['ShapeFactor']) ** 2
            + (row['GHS_Heightmean'] - centroid['GHS_Heightmean']) ** 2)

    for sub_sector in dfSS['Sub_sector'].unique():
        dfSubsector = dfSS.loc[dfSS['Sub_sector'] == sub_sector].copy()
        dfSubsector['NormalizedBuiltArea'] = dfSubsector['Building_GFA'] / dfSubsector['Building_GFA'].sum()
        weights = dfSubsector['NormalizedBuiltArea'].values
        dfClustering = dfSubsector[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']]

        scaler = StandardScaler()
        dfScaled = scaler.fit_transform(dfClustering)

        km = KMeans(n_clusters = nClustersSS, max_iter = 8000)
        dfSubsector['cluster'] = km.fit_predict(dfScaled, sample_weight = weights)
        dfSubsector['cluster'] = dfSubsector['cluster'].apply(lambda x: f"{x}_{Sub_sector}")

        centroids = dfSubsector.groupby('cluster')[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']].mean()
        dfSubsector['distance'] = dfSubsector.apply(lambda row: calculateDistance(row, centroids.loc[row['cluster']]), axis = 1)

        dfSubsectorCentroidOsmIds = dfSubsector.loc[dfSubsector.groupby('cluster')['distance'].idxmin()]
        dfCentroidOsmIds = dfSubsectorCentroidOsmIds.set_index('cluster')['osm_id']
        dfSubsector['centroid_osm_id'] = dfSubsector['cluster'].apply(
            lambda x: 1 if dfCentroidOsmIds[x] in dfSubsector['osm_id'].values else 0)
        sumGFArea = dfSubsector.groupby('cluster')['Building_GFA'].sum()

        dfAllSubSector = pd.concat([dfAllSubSector, dfSubsector])
        for cluster in dfSubsector['cluster'].unique():
            centroid = centroids.loc[cluster]
            closestEntity = dfSubsector[dfSubsector['osm_id'] == dfCentroidOsmIds[cluster]]
            dfNew = pd.DataFrame([{'Sub_sector': sub_sector,
                'Cluster': cluster, 'Centroid_GHS_Heightmean': centroid['GHS_Heightmean'],
                'Centroid_ExtFachade': centroid['%ExtFachade'], 'Centroid_ShapeFactor': centroid['ShapeFactor'],
                'Closest_Entity_OSM_ID': closestEntity['osm_id'].values[0],
                'Closest_Entity_FootprintArea': closestEntity['BuildingFP_area'].values[0],
                'Closest_Entity_GFA': closestEntity['Building_GFA'].values[0],
                'Closest_Entity_Height': closestEntity['GHS_Heightmean'].values[0],
                'Closest_Entity_N_floors': closestEntity['N_Floors'].values[0],
                'Closest_Entity_Volume': closestEntity['Volume'].values[0],
                'Closest_Entity_TotalPerimeter': closestEntity['perimeter'].values[0],
                'Closest_Entity_%ExtFachade': closestEntity['%ExtFachade'].values[0],
                'Closest_Entity_R_WalltoGFA': closestEntity['R_WalltoGFA'].values[0],
                'Closest_Entity_ShapeFactor': closestEntity['ShapeFactor'].values[0],
                'Sum_GFArea': sumGFArea[cluster]}])

            dfNew = dfNew.dropna(how = 'all', axis = 1)
            dfNew = dfNew.dropna(how = 'all', axis = 0)
            dfClustersSS = dfClustersSS.dropna(how = 'all', axis = 1)
            dfClustersSS = dfClustersSS.dropna(how = 'all', axis = 0)
            dfClustersSS = pd.concat([dfClustersSS, dfNew]).reset_index(drop = True)

        periodToYear = {
            'Before1945': 1900,
            '1945to1969': 1955,
            '1970to1979': 1975,
            '1980to1989': 1985,
            '1990to2000': 1995,
            '2000to2010': 2005,
            'Post2010': 2020
        }

        # Iterate over each row in dfClustersSS
        newRows = []
        for _, row in dfClustersSS.iterrows():
            for period, year in periodToYear.items():
                newRow = row.copy()
                newRow['Period'] = period
                newRow['Year'] = year
                newRows.append(newRow)

        dfExpanded = pd.DataFrame(newRows)

        # Reset the new dataframe index
        dfExpanded.reset_index(drop = True, inplace = True)

        # First, we melt dfAllSubSector to get one row for each cluster and period.
        dfArea = dfAllSubSector.melt(id_vars = ['cluster'],
            value_vars = [c for c in dfAllSubSector.columns if c.endswith('_A')],
            var_name = 'Period', value_name = 'Area')

        # We remove the '_A' from the end of the period
        dfArea['Period'] = dfArea['Period'].str.rstrip('_A')

        # add the values of area per cluster and period
        dfArea = dfArea.groupby(['cluster', 'Period'])['Area'].sum().reset_index()

        # We create a combined index column for dfArea
        dfArea['merge_index'] = dfArea['cluster'] + dfArea['Period']

        # Create a combined index column for dfExpanded
        dfExpanded['merge_index'] = dfExpanded['Cluster'] + dfExpanded['Period']

        # We sort dfArea by this combined index
        dfArea.sort_values('merge_index', inplace = True)

        # We create a new df that is merge on merge_index
        dfMergedSS = dfExpanded.merge(dfArea, how = 'left', on = 'merge_index')

        # Then we no longer need the merge_index column
        dfMergedSS.drop(columns = 'merge_index', inplace = True)
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 20 -> [OK]')
    logging.info('')
    return dfMergedSS


# Function: Build. Energy Sim. -> Preprocess -> Step 21 -> Create the final Dataframe
def bp1Step21(dfClustersAB, dfClustersSFH, dfClustersSS, process, username, nutsid):
    ''' Build. Energy Sim. -> Preprocess -> Step 21 : Create the final dataframe. '''

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> Creating the final Dataframe...')
    
    # Create an empty DataFrame with the required columns
    dfFinal = pd.DataFrame(columns = ['Building ID', 'Use', 'Age', 'Footprint Area', 'Number of floors', 'Volume',
        'Gross floor area', 'Total External Facade area', 'Opaque Facade area', 'Window area', 'Height'])

    # Define the auxiliary function for calculating the required fields
    def calculateFields(df, use, buildingIdFormat):
        dfNew = pd.DataFrame()
        if buildingIdFormat == 'AB_Format':
            dfNew['Building ID'] = 'Apartment Block' + '_' + df['Cluster'].astype(str)
        else:
            dfNew['Building ID'] = df['Cluster'].astype(str) + '_' + df['Year'].astype(str)
        dfNew['Use'] = df[use] if use != 'Apartment Block' else use
        dfNew['Age'] = df['Year']
        dfNew['Footprint Area'] = df['Area'] / df['Closest_Entity_N_floors']
        dfNew['Number of floors'] = df['Closest_Entity_N_floors']
        dfNew['Volume'] = (df['Area'] / df['Closest_Entity_N_floors']) * df['Closest_Entity_Height']
        dfNew['Gross floor area'] = df['Area']
        dfNew['Total External Facade area'] = (df['Closest_Entity_R_WalltoGFA'] *\
            df['Area'] * df['Closest_Entity_%ExtFachade'])
        dfNew['Height'] = df['Closest_Entity_Height']
        return dfNew

    # Apply the auxiliary function to calculate the fields and add them to the final DataFrame
    frames = [calculateFields(dfClustersAB, use = 'Apartment Block', buildingIdFormat = 'AB_Format'),
              calculateFields(dfClustersSFH, use = 'Sub_sector', buildingIdFormat = 'SS_Format'),
              calculateFields(dfClustersSS, use = 'Sub_sector', buildingIdFormat = 'SS_Format')]
    dfFinal = pd.concat(frames)
    
    # Save the DataFrame as a CSV file
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> Saving...')
    csvName = io.retrieveOutputTmpPathConcatFile(True, process, username, nutsid, config)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> Temp. output file -> ' + csvName)
    dfFinal.to_csv(csvName, index = False, sep = ',')
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> Saved!!')
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> [OK]')
    logging.info('')
    return dfFinal, csvName
    
    

#####################################################################
######################## Auxiliary functions ########################
#####################################################################



# Auxiliary function: Get pixel value
def getPixelValue(centroidX, centroidY, rasterData, transform):
    ''' Function to get a pixel value. '''

    pixelX, pixelY = ~transform['transform'] * (centroidX, centroidY)
    pixelX, pixelY = int(pixelX), int(pixelY)
    pixelValue = rasterData[pixelY, pixelX]
    return pixelValue

