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
def bp1_step_01(nuts_id, file_list, resource_list, config, properties):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Preparing the data...')
    if not (4 <= len(nuts_id) <= 5 and nuts_id[:2].isalpha()):
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> NUTS_ID not valid! [NUTS2/NUTS3]!')
        return
    
    # Read the Excel file
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Reading the Excel file...')
    df = pd.read_excel(io.retrieveBasePath(config) + file_list[0]['path'])
    url = df.loc[df['NUTS_ID'] == nuts_id, 'Link'].values
    if not url or len(url) == 0:
        raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.nuts.id.not.found'])

    # Search the resource from the url, and download it
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Obtaining the ZIP file...')
    destination_dir = io.retrieveFilesTmpPath(config)
    resource_obj = None
    for resource in resource_list:
        if resource['web'] == url:
            resource_obj = resource
            break
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Unzipping...')
    logging.info('')
    if resource_obj:
        resource_obj['local'] = sftp.downloadResource(resource_obj, config)
        if resource_obj['local'] and zipfile.is_zipfile(resource_obj['local']):
            with zipfile.ZipFile(resource_obj['local'], 'r') as zip_ref:
                zip_ref.extractall(io.retrieveFilesTmpPath(config))
        else:
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.not.zip.file'])
    
    # Delete all the not necessary files
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> Removing the not necessary files...')
    exclude_files = ['README', 'gis_osm_landuse_a_free_1', 'gis_osm_buildings_a_free_1']
    for fil in os.listdir(destination_dir):
        filename_without_extension = os.path.splitext(fil)[0]
        if not any(fnmatch.fnmatch(filename_without_extension, pattern) for pattern in exclude_files):
            os.remove(os.path.join(destination_dir, fil))

    # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 01 -> [OK]')
    logging.info('')
    return destination_dir


# Function: Build. Energy Sim. -> Preprocess -> Step 02 -> Export the selected NUTS
def bp1_step_02(layer, nuts_id, config, properties):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> Exporting the selected NUTS...')
    
    # Read the layer file
    data = gpd.read_file(io.retrieveBasePath(config) + layer['path'])
    
    # Filter data according to length of NUTS_ID and select the name of the NUTS
    if len(nuts_id) == 5:
        nuts_filtered = data[data['NUTS_ID'] == nuts_id]
        nuts_name_values = data[(data['NUTS_ID'] == nuts_id) & (data['LEVL_CODE'] == 3)]['NUTS_NAME'].values
    else:
        nuts_filtered = data[(data['NUTS_ID'].str.startswith(nuts_id)) & (data['LEVL_CODE'] == 3)]
        nuts_name_values = data[(data['NUTS_ID'] == nuts_id) & (data['LEVL_CODE'] == 2)]['NUTS_NAME'].values
    
    # Ensure that values exist for NUTS_NAME
    if len(nuts_name_values) > 0:
        nuts_name = nuts_name_values[0]
        nuts_filtered['NUTS2_NAME'] = nuts_name
    else:
        raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.nuts.name.for_nuts.id'].replace('{1}', nuts_id))
    
    # Convert GeoDataFrame to 4326 and 54009 Mollewide coordinate systems
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> Converting GeoDataFrame to 4326 cooordinate system...')
    nuts_filtered_crs = nuts_filtered.to_crs(epsg = 4326)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> Converting GeoDataFrame to 54009 Mollewide cooordinate system...')
    nuts_filtered_moll54009 = nuts_filtered.to_crs('Esri:54009')
    
    # Save
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> Saving...')
    output_nuts_path, output_nuts_path_moll54009 = io.buildOutputPaths_BP_Step_02(layer, nuts_id, config, properties)
    nuts_filtered_crs.to_file(output_nuts_path, driver=layer['format'].upper())
    nuts_filtered_moll54009.to_file(output_nuts_path_moll54009, driver = layer['format'].upper())
    
    # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 02 -> [OK]')
    logging.info('')
    return nuts_filtered_crs, output_nuts_path_moll54009


# Function: Build. Energy Sim. -> Preprocess -> Step 03 -> Clip and save the vector layers
def bp1_step_03(destination_dir, nuts_filtered_crs):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> Clipping the layer(s) (can take quite a while)...')
    
    # Use the NUTS layer at 4326 for cutting. Reproject and save layers in 54009 and gpkg
    clipped_layers = []
    for fil in os.listdir(destination_dir):
        if fil.endswith('shp'):
            file_path = os.path.join(destination_dir, fil)
            logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> File -> ' + file_path)
            gdf = gpd.read_file(file_path)
            gdf_clipped = gpd.clip(gdf, nuts_filtered_crs)
            gdf_clipped = gdf_clipped.to_crs('Esri:54009'.upper())
            
            # Only save if the file is not empty
            if not gdf_clipped.empty:
                output = destination_dir + '/' + str(fil.rsplit('.', 1)[0]) + '_repro54009.gpkg'
                logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> Save -> ' + output)
                gdf_clipped.to_file(output, driver = 'GPKG')
                clipped_layers.append(output)
            else:
                logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> The file is empty, so it is not saved!')
    
    # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 03 -> [OK]')
    logging.info('')
    return clipped_layers


# Function: Build. Energy Sim. -> Preprocess -> Step 04 -> Load the buildings layer
def bp1_step_04(clipped_layers, isTest, config):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 04 -> Loading the buildings layer...')
    buildings_path = config['IDESIGNRES-PATH']['idesignres.path.bp.test']\
        if isTest else [path for path in clipped_layers if 'buildings' in path][0]
    layer = qgis.loadVectorLayer(buildings_path, 'Buildings', 'ogr')
    
    # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 04 -> [OK]')
    logging.info('')
    return layer
    
    
# Function: Build. Energy Sim. -> Preprocess -> Step 05 -> Load the NUTS layer
def bp1_step_05(nuts_path_moll54009):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 05 -> Loading the NUTS layer...')
    layer = qgis.loadVectorLayer(nuts_path_moll54009, 'NUTS', 'ogr')
    
     # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 05 -> [OK]')
    logging.info('')
    return layer


# Function: Build. Energy Sim. -> Preprocess -> Step 06 -> Load the land use layer
def bp1_step_06(clipped_layers):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 06 -> loading the land use layer...')
    layer = qgis.loadVectorLayer([path for path in clipped_layers if 'landuse' in path][0], 'Land Use', 'ogr')
    
     # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 06 -> [OK]')
    logging.info('')
    return layer


# Function: Build. Energy Sim. -> Preprocess -> Step 07 -> Load the Raster Use layer
def bp1_step_07(layer_obj, config):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 07 -> Loading the Raster Use layer...')
    layer = qgis.loadRasterLayerWithProvider(io.retrieveLayersBasePath(config) + '/' +\
        layer_obj['name'] + '.' + layer_obj['format'], 'Raster Use', 'gdal')
    
     # Finish    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 07 -> [OK]')
    logging.info('')
    return layer


# Function: Build. Energy Sim. -> Preprocess -> Step 08 -> Load the Raster Height layer
def bp1_step_08(layer_obj, config):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 08 -> Loading the Raster Height layer...')
    layer = qgis.loadRasterLayerWithProvider(io.retrieveLayersBasePath(config) + '/' +\
        layer_obj['name'] + '.' + layer_obj['format'], 'Raster Height', 'gdal')
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 08 -> [OK]')
    logging.info('')
    return layer


# Function: Build. Energy Sim. -> Preprocess -> Step 09 -> Assign NUTS
def bp1_step_09(buildings_layer, nuts_layer, nuts_id):
    """
    This function assigns NUTS3, NUTS2 and BuildingFP_area to each building in a given layer (buildings_layer).
    If the building's area is less than 30 m², the building is removed from the layer.
    If a building does not have a 'NUTS3' value, it is also removed.
    """

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> ##### Start building preprocessing #####')
    logging.info('')
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Assigning NUTS...')
    
    # Verify if "NUTS3", "NUTS2" and "AREA" fields exist. If not, it creates them
    if buildings_layer.fields().indexFromName('NUTS3') == -1:
        buildings_layer.dataProvider().addAttributes([QgsField('NUTS3', QVariant.String)])
        buildings_layer.updateFields()

    if buildings_layer.fields().indexFromName('NUTS2') == -1:
        buildings_layer.dataProvider().addAttributes([QgsField('NUTS2', QVariant.String)])
        buildings_layer.updateFields()

    if buildings_layer.fields().indexFromName('BuildingFP_area') == -1:
        buildings_layer.dataProvider().addAttributes([QgsField('BuildingFP_area', QVariant.Double)])
        buildings_layer.updateFields()

    # Extract the indexes
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Extracting the indexes...')
    index_NUTS3 = buildings_layer.fields().indexFromName('NUTS3')
    index_NUTS2 = buildings_layer.fields().indexFromName('NUTS2')
    index_AREA = buildings_layer.fields().indexFromName('BuildingFP_area')
    
    # Update the features
    buildings_layer_index = QgsSpatialIndex(buildings_layer.getFeatures())
    features_to_update, n_processed = [], 0
    for nuts_feat in nuts_layer.getFeatures():
        if nuts_feat['LEVL_CODE'] != 3:
            continue

        nuts3_id = nuts_feat['NUTS_ID']
        intersecting_ids = buildings_layer_index.intersects(nuts_feat.geometry().boundingBox())
        intersecting_features = buildings_layer.getFeatures(QgsFeatureRequest().setFilterFids(intersecting_ids))
        for building_feat in intersecting_features:
            if nuts_feat.geometry().intersects(building_feat.geometry()):
                # Assign NUTS3
                building_feat['NUTS3'] = nuts3_id
                # Assign NUTS2
                building_feat['NUTS2'] = nuts_id[:4]
                # Calculate the AREA
                building_feat['BuildingFP_area'] = building_feat.geometry().area()
                features_to_update.append(building_feat)

            if len(features_to_update) >= 2000:
                changes = {feature.id(): {
                    index_NUTS3: feature['NUTS3'],
                    index_NUTS2: feature['NUTS2'],
                    index_AREA: feature['BuildingFP_area']} for feature in features_to_update
                }
                dataProvider = buildings_layer.dataProvider()
                dataProvider.changeAttributeValues(changes)
                features_to_update = []
                n_processed += 5000
    
    if features_to_update:
        changes = {feature.id(): {
            index_NUTS3: feature['NUTS3'],
            index_NUTS2: feature['NUTS2'],
            index_AREA: feature['BuildingFP_area']} for feature in features_to_update
        }
        dataProvider = buildings_layer.dataProvider()
        dataProvider.changeAttributeValues(changes)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> ' + str(n_processed) + ' buildings processed')
    
    # Eliminate all geometries with an area of less than 30m².
    expression = QgsExpression(' "BuildingFP_area" < 30 ')
    ids = [f.id() for f in buildings_layer.getFeatures(QgsFeatureRequest(expression))]
    buildings_layer.dataProvider().deleteFeatures(ids)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Deleted ' + str(len(ids)) + ' buildings (area of less than 30m²)')
    
    # Get a list of entity IDs that have the field ‘NUTS3’ as NULL
    expression = QgsExpression(' "NUTS3" is NULL ')
    ids = [f.id() for f in buildings_layer.getFeatures(QgsFeatureRequest(expression))]
    buildings_layer.dataProvider().deleteFeatures(ids)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Removed ' + str(len(ids)) + ' features out of boundary')
    
    # Commit changes
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> Commiting changes...')
    buildings_layer.commitChanges()
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 09 -> [OK]')
    logging.info('')


# Function: Build. Energy Sim. -> Preprocess -> Step 10 -> Calculate height volumes
def bp1_step_10(buildings_layer, raster_height_layer):
    """
    This function calculates the number of floors, GFA and volume of each building in the 'buildings'
    layer based on the'GHS_Heightmean' attribute.
    If a building doesn't have 'GHS_Heightmean' (height), the value is calculated from a raster
    layer with height data ('raster_height').
    """

    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> Calculating heights and volumes...')
    buildings_layer.startEditing()
    if 'GHS_Heightmean' in [field.name() for field in buildings_layer.fields()]:
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> The field "GHS_Heightmean" already exists!')
    else:
        prefix = 'GHS_Height'
        stats_to_calculate = QgsZonalStatistics.Mean
        zonal_stats = QgsZonalStatistics(buildings_layer, raster_height_layer, 'GHS_Height', 1, stats_to_calculate)
        zonal_stats.calculateStatistics(None)
    
    # Define the list of fields to be added
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> Defining the list of fields to be added...')
    fields_to_add = ['N_Floors', 'Building_GFA', 'Volume']

    # Create the fields (if they do not exist)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> Creating the fields (can take quite a while)...')
    if not all(field in [field.name() for field in buildings_layer.fields()] for field in fields_to_add):
        buildings_layer.dataProvider().addAttributes([QgsField(field, QVariant.Double) for field in fields_to_add])
        buildings_layer.updateFields()
    else:
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> All the fields already exist!')
    
    # Calculate 'N_Floors' as a function of 'GHS_Heightmean' and GFA with N_floors
    counter = 0
    for feature in buildings_layer.getFeatures():
        counter += 1
        GHS_Heightmean = feature['GHS_Heightmean']
        if not GHS_Heightmean or GHS_Heightmean == 0:
            GHS_Heightmean = 3.5
        elif 0 <= GHS_Heightmean < 2.5:
            GHS_Heightmean = 2.5
            
        # Updating GHS_Heightmean on the feature
        feature['GHS_Heightmean'] = GHS_Heightmean
        
        # Calculate and update 'N_Floors'
        feature['N_Floors'] = round(GHS_Heightmean / 3)
        
        # Calculate building GFA and update
        feature['Building_GFA'] = feature['N_Floors'] * feature['BuildingFP_area']
        feature['Volume'] = feature['GHS_Heightmean'] * feature['BuildingFP_area']
        buildings_layer.updateFeature(feature)

    # Commit changes
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> Commiting changes...')
    buildings_layer.commitChanges()

    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 10 -> [OK]')
    logging.info('')


# Function: Build. Energy Sim. -> Preprocess -> Step 11 -> Calculate statistics and mapping
def bp1_step_11(buildings_layer, raster_use_layer, land_use_layer, mapping_csv_obj, config):
    """
    This function calculates the majority use for each building from a raster layer ('raster_use') and
    a vector layer with classified land use data ('land_use').
    The function also maps the use to defined groups, sub-sectors, and sectors according to a mapping
    table stored in a CSV file ('MappingCsvPath').
    """
    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> Calculating statistics and mapping...')
    csv_path = io.retrieveBasePath(config) + mapping_csv_obj['path']
    
    # Calculate zone statistics with majority value
    if 'GHS_Majority' in [field.name() for field in buildings_layer.fields()]:
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> The field "GHS_Majority" anready exists!')
    else:
        zonal_stats = QgsZonalStatistics(buildings_layer, raster_use_layer, 'GHS_', stats = QgsZonalStatistics.Majority)
        zonal_stats.calculateStatistics(None)

    # Create spatial index for the Land Use layer
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> Creating spatial index for the Land Use layer...')
    index = QgsSpatialIndex(land_use_layer.getFeatures())
    
    # Create a dictionary from the CSV file
    mapping_dict = {}
    with open(csv_path, mode='r') as fil:
        reader = csv.reader(fil, delimiter=';')
        next(reader)  # To skip the headers
        for row in reader:
            mapping_dict[row[0]] = row[1:]

    # Create new columns in the buildings layer
    fields = ['Group', 'Sub_sector', 'Sector', 'Combined_Use']
    for field in fields:
        buildings_layer.dataProvider().addAttributes([QgsField(field, QVariant.String)])
    buildings_layer.updateFields()

    total_features = buildings_layer.featureCount()
    percentage_increment = total_features // 10
    
    buildings_layer.startEditing()
    
    # Allocation of uses and mapping
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> Starting use allocation/mapping (can take quite a while)...')
    for feature in buildings_layer.getFeatures():
        type_value = str(feature['type'])
        
        # Check if the 'type' field exists and is not empty
        if not type_value or type_value.isspace() or type_value in ['NULL', 'None', 'none', '']:
            final_use = 'unknown'
            land_use_value = None
            
            geom = feature.geometry()
            intersects = index.intersects(geom.boundingBox())
            for i in intersects:
                land_use_feat = land_use_layer.getFeature(i)
                if land_use_feat.geometry().intersects(geom):
                    land_use_value = land_use_feat['fclass']
                    break

            ghs_majority = feature['GHS_Majority']
            if land_use_value in ('industrial', 'retail', 'military', 'commercial'):
                final_use = land_use_value
            elif ghs_majority == 0 or ghs_majority == 1:
                final_use = 'residential'
            elif ghs_majority == 2:
                final_use = 'other non-residential'
            feature['Combined_Use'] = final_use
        else:
            feature['Combined_Use'] = type_value

        combined_use = feature['Combined_Use']
        if combined_use not in mapping_dict:
            combined_use = 'other non-residential'.capitalize()

        if combined_use in mapping_dict:
            feature['Group'] = mapping_dict[combined_use][0]
            feature['Sub_sector'] = mapping_dict[combined_use][1]
            feature['Sector'] = mapping_dict[combined_use][2]
            if feature['Sub_sector'] == 'Apartment blocks' and feature['N_floors'] < 3:
                feature['Sub_sector'] = 'Single family- Terraced houses'
            elif feature['Sub_sector'] == 'Single family- Terraced houses' and feature['N_floors'] > 3:
                feature['Sub_sector'] = 'Apartment blocks'

        buildings_layer.updateFeature(feature)
        
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> Use allocation and mapping completed!')
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 11 -> [OK]')
    logging.info('')


# Function: Build. Energy Sim. -> Preprocess -> Step 12 -> Adjoin facade calculations
def bp1_step_12(isTest, config):
    """
    This function calculates the length of the adjoining perimeter (facade) and the ratio of this length to the total
    perimeter of each building. Buildings with a ratio equal to or above 1 are removed, and the calculations are performed
    again for the buildings affected by these removals. The results are stored in a new GeoDataFrame returned by the function.
    """
    
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Adjoining facade calculations...')
    
    # Load the building layer from the GPKG file
    buildings_path = config['IDESIGNRES-PATH']['idesignres.path.bp.test'] if isTest else config['IDESIGNRES-PATH']['idesignres.path.bp.test']
    buildings = gpd.read_file(buildings_path)
    
    # Ensure that the geometry is of type Polygon or Multipolygon.
    buildings = buildings[buildings.geometry.type.isin(['Polygon', 'MultiPolygon'])]
    buildings['adjoining_perimeter'] = 0.0
    
    # Create a spatial index (R-tree) for buildings
    sindex = buildings.sindex
    
    #####
    
    # Funtion (internal): Calculate adjoining
    def calculate_adjoining(current_buildings, sindex, all_buildings):
        # Iterate on each building to calculate its dividing façade
        for idx, building in current_buildings.iterrows():
            adjoining_perimeter = 0.0

            # Get the perimeter of the current building as a line (LineString)
            building_perimeter = building.geometry.boundary

            # Obtain the length of the perimeter
            perimeter = building_perimeter.length

            # Obtain the bounding box of the current building
            bbox = building.geometry.bounds

            # Find possible intersections with the spatial index
            possible_intersections = list(sindex.intersection(bbox))

            # Iterate on buildings selected by the spatial index
            for idx_others in possible_intersections:
                if idx_others == idx:
                    continue  # Ignore the same building

                bbox_buildings = all_buildings.iloc[idx_others]

                # Calculate the intersection between the perimeter of the building and the other building
                intersection = building_perimeter.intersection(bbox_buildings.geometry)

                # If the intersection is of type LineString or MultiLineString, add length
                if isinstance(intersection, LineString):
                    adjoining_perimeter += intersection.length
                elif intersection.geom_type == 'MultiLineString':
                    adjoining_perimeter += sum(line.length for line in intersection.geoms)

                # Save the length of the party wall and the perimeter in the column
                current_buildings.at[idx, 'adjoining_perimeter'] = adjoining_perimeter

            current_buildings.at[idx, 'perimeter'] = perimeter
        
            # Calculate the ratio adj_facade / perimeter
            current_buildings.at[idx, 'Ratio'] = adjoining_perimeter / perimeter if perimeter > 0 else 0
    
    #####
    
    # Funtion (internal): Find adjacents
    def find_adjacents(current_buildings, sindex):
        # Iterate over each building to look for adjacent buildings
        adjacents = set()
        for idx, building in current_buildings.iterrows():
            # Get the bounding box of the current building
            bbox = building.geometry.bounds

            # Find possible intersections with the spatial index
            possible_intersections = list(sindex.intersection(bbox))

            # Update
            adjacents.update(possible_intersections)

        # Return a DataFrame with adjacent buildings
        return buildings.iloc[list(adjacents)].copy()

    #####
    
    # Calculate adjoining for all buildings
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Calculate adjoining for all buildings...')
    calculate_adjoining(buildings, sindex, buildings)
    
    # Filter buildings where Ratio is >= 1
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Filtering buildings where Ratio >= 1...')
    to_remove = buildings[buildings['Ratio'] >= 1].copy()

    # Obtain adjacencies for buildings to be removed
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Finding adjancencies for buildings to be removed...')
    to_recalculate = find_adjacents(to_remove, sindex)
    
    # Remove buildings with Ratio >= 1
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Removing buildings where Ratio >= 1...')
    buildings = buildings[buildings['Ratio'] < 1]

    # Recalculating adjoining buildings
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Recalculating adjoining buildings...')
    calculate_adjoining(to_recalculate, sindex, buildings)

    # Merge recalculated buildings again
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Merging recalculated buildings...')
    buildings.update(to_recalculate)
    
    # Save the result in a new GPKG file
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> Saving to a new GeoPackage file...')
    buildings.to_file(buildings_path, driver = 'GPKG')

    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 12 -> [OK]')
    logging.info('')
    return buildings


# Function: Build. Energy Sim. -> Preprocess -> Step 13 -> Mask raster layers
def bp1_step_13(layer_list, config):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 13 -> Masking raster layers (can take quite a while)...')
    
    # Retrieve the necessary paths
    clipped_rasters_paths = []
    layers = [{'name': layer_list[8]['name'], 'path': io.retrieveBasePath(config) + layer_list[8]['path'], 'format': layer_list[8]['format']},
              {'name': layer_list[5]['name'], 'path': io.retrieveBasePath(config) + layer_list[8]['path'], 'format': layer_list[8]['format']},
              {'name': layer_list[4]['name'], 'path': io.retrieveBasePath(config) + layer_list[8]['path'], 'format': layer_list[8]['format']},
              {'name': layer_list[3]['name'], 'path': io.retrieveBasePath(config) + layer_list[8]['path'], 'format': layer_list[8]['format']},
              {'name': layer_list[7]['name'], 'path': io.retrieveBasePath(config) + layer_list[8]['path'], 'format': layer_list[8]['format']}]
    nuts_layer_path = io.retrieveBasePath(config) + layer_list[0]['path']
    
    for layer in layers:
        gdf = gpd.read_file(nuts_layer_path)
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
        output = io.buildOutputPath_BP_Step_13(layer['name'], layer['format'], config)
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 13 -> Saving: ' + output + '...')
        with rasterio.open(output, "w", **out_meta) as dst:
            dst.write(out_image)
        clipped_rasters_paths.append(output)
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 13 -> [OK]')
    logging.info('')
    return clipped_rasters_paths


# Function: Build. Energy Sim. -> Preprocess -> Step 14 -> Process clipped layers
def bp1_step_14(nuts_id, clipped, excel_file, download_folder, config):
    # CSV file with the percentages per country and year
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Loading the Excel file to calculate the percentages...')
    share_years_df = pd.read_excel(io.retrieveBasePath(config) + excel_file['path'])
    
    # Dictionary that will contain the 'layer' data
    layers_dict = {}
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Calculating the percentages...')
    country_percentage_before_1945 = share_years_df.loc[share_years_df['NUTS_ID'] == nuts_id[:2], 'Before 1945'].values[0]
    country_percentage_1945_1969 = share_years_df.loc[share_years_df['NUTS_ID'] == nuts_id[:2], '1945 - 1969'].values[0]
    country_percentage_1970_1979 = share_years_df.loc[share_years_df['NUTS_ID'] == nuts_id[:2], '1970 - 1979'].values[0]
    country_percentage_1980_1989 = share_years_df.loc[share_years_df['NUTS_ID'] == nuts_id[:2], '1980 - 1989'].values[0]
    
    total_mem, used_mem, free_mem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (1) -> ' +\
        str(round((used_mem / total_mem) * 100, 2)) + '%')
    
    chunk_size = int(config['IDESIGNRES-PARAMETERS']['idesignres.params.chunk.size'])
    with rasterio.open(clipped[4]) as src_2020, rasterio.open(clipped[0]) as src_1975:
        ratio = np.zeros((src_1975.height, src_1975.width), dtype = np.float16)
        for row_off in range(0, src_1975.height, chunk_size):
            for col_off in range(0, src_1975.width, chunk_size):
                window = rasterio.windows.Window(col_off, row_off, chunk_size, chunk_size)
                c_ratio = np.divide(
                    src_1975.read(1, window = window).astype(np.float16),
                    src_2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src_1975.read(1, window = window).astype(np.float16)),
                    where = (src_2020.read(1, window = window).astype(np.float16) != 0))
                ratio[row_off:row_off + chunk_size, col_off:col_off + chunk_size] = c_ratio
        layers_dict["Before1945"] = (ratio * country_percentage_before_1945, src_1975.profile)
        layers_dict["1945to1969"] = (ratio * country_percentage_1945_1969, src_1975.profile)
        del c_ratio, ratio
        gc.collect()

    total_mem, used_mem, free_mem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (2) -> ' +\
        str(round((used_mem / total_mem) * 100, 2)) + '%')
    
    with rasterio.open(clipped[4]) as src_2020, rasterio.open(clipped[0]) as src_1975, rasterio.open(clipped[1]) as src_1990:
        diff = np.zeros((src_1975.height, src_1975.width), dtype = np.float16)
        for row_off in range(0, src_1975.height, chunk_size):
            for col_off in range(0, src_1975.width, chunk_size):
                window = rasterio.windows.Window(col_off, row_off, chunk_size, chunk_size)
                c_diff = np.divide(src_1990.read(1, window = window).astype(np.float16) - src_1975.read(1, window = window).astype(np.float16),
                    src_2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src_1975.read(1, window = window).astype(np.float16)),
                    where = (src_2020.read(1, window = window).astype(np.float16) != 0))
                diff[row_off:row_off + chunk_size, col_off:col_off + chunk_size] = c_diff
        layers_dict["1970to1979"] = (diff * country_percentage_1970_1979, src_1975.profile)
        layers_dict["1980to1989"] = (diff * country_percentage_1980_1989, src_1975.profile)
        del c_diff, diff
        gc.collect()

    total_mem, used_mem, free_mem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (3) -> ' +\
        str(round((used_mem / total_mem) * 100, 2)) + '%')

    with rasterio.open(clipped[4]) as src_2020, rasterio.open(clipped[1]) as src_1990, rasterio.open(clipped[2]) as src_2000:
        diff = np.zeros((src_2020.height, src_2020.width), dtype = np.float16)
        for row_off in range(0, src_2020.height, chunk_size):
            for col_off in range(0, src_2020.width, chunk_size):
                window = rasterio.windows.Window(col_off, row_off, chunk_size, chunk_size)
                c_diff = np.divide(src_2000.read(1, window = window).astype(np.float16) - src_1990.read(1, window = window).astype(np.float16),
                    src_2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src_1990.read(1, window = window).astype(np.float16)),
                    where = (src_2020.read(1, window = window).astype(np.float16) != 0))
                diff[row_off:row_off + chunk_size, col_off:col_off + chunk_size] = c_diff
        layers_dict["1990to2000"] = (diff, src_1990.profile)
        del c_diff, diff
        gc.collect()
    
    total_mem, used_mem, free_mem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (4) -> ' +\
        str(round((used_mem / total_mem) * 100, 2)) + '%')

    with rasterio.open(clipped[4]) as src_2020, rasterio.open(clipped[2]) as src_2000, rasterio.open(clipped[3]) as src_2010:
        diff = np.zeros((src_2020.height, src_2020.width), dtype=np.float16)
        for row_off in range(0, src_2020.height, chunk_size):
            for col_off in range(0, src_2020.width, chunk_size):
                window = rasterio.windows.Window(col_off, row_off, chunk_size, chunk_size)
                c_diff = np.divide(src_2010.read(1, window = window).astype(np.float16) - src_2000.read(1, window = window).astype(np.float16),
                    src_2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src_2000.read(1, window = window).astype(np.float16)),
                    where = (src_2020.read(1, window = window).astype(np.float16) != 0))
                diff[row_off:row_off + chunk_size, col_off:col_off + chunk_size] = c_diff
        layers_dict["2000to2010"] = (diff, src_1990.profile)
        del c_diff, diff
        gc.collect()

    total_mem, used_mem, free_mem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (5) -> ' +\
        str(round((used_mem / total_mem) * 100, 2)) + '%')
    
    with rasterio.open(clipped[4]) as src_2020, rasterio.open(clipped[3]) as src_2010:
        diff = np.zeros((src_2020.height, src_2020.width), dtype=np.float16)
        for row_off in range(0, src_2020.height, chunk_size):
            for col_off in range(0, src_2020.width, chunk_size):
                window = rasterio.windows.Window(col_off, row_off, chunk_size, chunk_size)
                c_diff = np.divide(src_2020.read(1, window = window).astype(np.float16) - src_2010.read(1, window = window).astype(np.float16),
                    src_2020.read(1, window = window).astype(np.float16),
                    out = np.zeros_like(src_2010.read(1, window = window).astype(np.float16)),
                    where = (src_2020.read(1, window = window).astype(np.float16) != 0))
                diff[row_off:row_off + chunk_size, col_off:col_off + chunk_size] = c_diff
        layers_dict["Post2010"] = (diff, src_1990.profile)
        del c_diff, diff
        gc.collect()
    
    total_mem, used_mem, free_mem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> Current mem usage (6) -> ' +\
        str(round((used_mem / total_mem) * 100, 2)) + '%')
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 14 -> [OK]')
    logging.info('')
    return layers_dict


# Function: Build. Energy Sim. -> Preprocess -> Step 15 -> Assign year info
def bp1_step_15(nuts_id, buildings, layers_dict, excel_file, config):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 15 -> Assigning year info...')
    for raster_name, (raster_data, transform) in layers_dict.items():
        buildings[raster_name] = buildings.geometry.centroid.apply(\
            lambda point: getPixelValue(point.x, point.y, raster_data, transform))
            
    # Assign value = 1 to the field with the highest % of built-up area in all those records where there is no year information
    columns_to_check = ['Before1945', '1945to1969', '1970to1979', '1980to1989', '1990to2000', '2000to2010', 'Post2010']

    # Get the 'MostCommon' column for this particular 'country_code'.
    share_years_df = pd.read_excel(io.retrieveBasePath(config) + excel_file['path'])
    most_common_column = share_years_df.loc[share_years_df['NUTS_ID'].str[:2] == nuts_id[:2], 'MostCommon'].values[0]

    # Check if all values in the columns are 0 (which means no data available)
    condition = (buildings[columns_to_check] == 0).all(axis = 1)

    # Assign 1 to the corresponding column in the rows where all values are 0
    buildings.loc[condition, most_common_column] = 1
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 15 -> [OK]')
    logging.info('')
    return buildings


# Function: Build. Energy Sim. -> Preprocess -> Step 16 -> Calculate additional info
def bp1_step_16(buildings):
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
    
    #buildings.to_file(driver='GPKG', filename=buildings_path)
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 16 -> [OK]')
    logging.info('')
    return buildings


# Function: Build. Energy Sim. -> Preprocess -> Step 17 -> Prepare clustering
def bp1_step_17(buildings):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 17 -> Preparing clustering...')
    
    # Filter the dataframe to keep only those in the Sub_sector field that are 'Apartment block'
    apartment_block = buildings[buildings['Sub_sector'] == 'Apartment blocks']

    # Check if there are no buildings in the Sub_sector 'Apartment block'
    if apartment_block.empty:
        logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 17 -> No empty buildings for "Apartment block" Subsector!')
        return pd.DataFrame()

    # The years / periods we are going to use
    periods = ['Before1945', '1945to1969', '1970to1979', '1980to1989', '1990to2000', '2000to2010', 'Post2010']

    # Duplicate rows for each period
    def expand_row(row):
        period_data = []
        for period in periods:
            new_row = row.copy()
            new_row['Period'] = period
            new_row['BuiltArea_ShareYears'] = row['Building_GFA'] * row[period]
            period_data.append(new_row.to_dict())
        return period_data

    # Duplicate rows 7 times and apply expand_row to each row
    expanded_data = apartment_block.apply(expand_row, axis = 1)

    # Concatenate all dictionaries returned by expand_row into a single dataframe
    AB_df = pd.DataFrame([item for sublist in expanded_data for item in sublist])
    
    # Filter the dataframe to keep only those in the Sub_sector field that are ‘Single family- Terraced houses’.
    SFH_df = buildings[buildings['Sub_sector'] == 'Single family- Terraced houses']
    
    # Filter the dataframe to keep only those in the Sector field that are 'Service sector'
    SS_df = buildings[buildings['Sector'] == 'Service sector']
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 17 -> [OK]')
    logging.info('')
    return AB_df, SFH_df, SS_df


# Function: Build. Energy Sim. -> Preprocess -> Step 18 -> Perform clustering (AB)
def bp1_step_18(AB_df, n_clusters_AB):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 18 -> Performing clustering (AB)...')

    df_all_years = pd.DataFrame()
    df_clusters_AB = pd.DataFrame(
        columns = ['Sub_sector', 'Cluster', 'Centroid_GHS_Heightmean', 'Centroid_ExtFachade', 'Centroid_ShapeFactor'])

    def calculate_distance(row, centroid):
        return np.sqrt(
            (row['%ExtFachade'] - centroid['%ExtFachade']) ** 2
            + (row['ShapeFactor'] - centroid['ShapeFactor']) ** 2
            + (row['GHS_Heightmean'] - centroid['GHS_Heightmean']) ** 2)

    period_to_year = {
        'Before1945': 1900,
        '1945to1969': 1955,
        '1970to1979': 1975,
        '1980to1989': 1985,
        '1990to2000': 1995,
        '2000to2010': 2005,
        'Post2010': 2020
    }

    for period in AB_df['Period'].unique():
        df_period = AB_df.loc[AB_df['Period'] == period].copy()
        df_period['Year'] = period_to_year[period]
        df_period['NormalizedBuiltArea'] = df_period['BuiltArea_ShareYears'] / df_period['BuiltArea_ShareYears'].sum()
        weights = df_period['NormalizedBuiltArea'].values

        df_clustering = df_period[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']]
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_clustering)

        # Adjust the KMeans model
        km = KMeans(n_clusters=n_clusters_AB, max_iter = 8000)
        df_period['cluster'] = km.fit_predict(df_scaled, sample_weight = weights)
        df_period['cluster'] = df_period['cluster'].apply(lambda x: f"{x}_{period}")
        centroids = df_period.groupby('cluster')[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']].mean()
        
        # Calculate the distance from each entity to the centroid
        df_period['distance'] = df_period.apply(lambda row: calculate_distance(row, centroids.loc[row['cluster']]), axis = 1)
        df_period_centroid_osmids = df_period.loc[df_period.groupby('cluster')['distance'].idxmin()]
        df_centroid_osm_ids = df_period_centroid_osmids.set_index('cluster')['osm_id']
        df_period['centroid_osm_id'] = df_period['cluster'].apply(lambda x: 1 if df_centroid_osm_ids[x] in df_period['osm_id'].values else 0)
        sum_GFArea = df_period.groupby('cluster')['BuiltArea_ShareYears'].sum()
        df_all_years = pd.concat([df_all_years, df_period])

        # Stores the information in df_clusters and then prints the centroids and nearest entities for each cluster
        for cluster in df_period['cluster'].unique():
            centroid = centroids.loc[cluster]
            closest_entity = df_period[df_period['osm_id'] == df_centroid_osm_ids[cluster]]
            new_df = pd.DataFrame([{'Period': period,
                'Cluster': cluster, 'Centroid_GHS_Heightmean': centroid['GHS_Heightmean'], 'Centroid_ExtFachade': centroid['%ExtFachade'],
                'Centroid_ShapeFactor': centroid['ShapeFactor'], 'Closest_Entity_OSM_ID': closest_entity['osm_id'].values[0],
                'Closest_Entity_FootprintArea': closest_entity['BuildingFP_area'].values[0],
                'Closest_Entity_GFA': closest_entity['Building_GFA'].values[0],
                'Closest_Entity_Height': closest_entity['GHS_Heightmean'].values[0],
                'Closest_Entity_N_floors': closest_entity['N_Floors'].values[0], 'Closest_Entity_Volume': closest_entity['Volume'].values[0],
                'Closest_Entity_TotalPerimeter': closest_entity['perimeter'].values[0],
                'Closest_Entity_%ExtFachade': closest_entity['%ExtFachade'].values[0],
                'Closest_Entity_R_WalltoGFA': closest_entity['R_WalltoGFA'].values[0],
                'Closest_Entity_ShapeFactor': closest_entity['ShapeFactor'].values[0],
                'Year': df_period['Year'].iloc[0], 'Area': sum_GFArea[cluster]}])

            new_df = new_df.dropna(how='all', axis = 1)
            new_df = new_df.dropna(how='all', axis = 0)
            df_clusters_AB = df_clusters_AB.dropna(how = 'all', axis=1)
            df_clusters_AB = df_clusters_AB.dropna(how = 'all', axis=0)
            df_clusters_AB = pd.concat([df_clusters_AB, new_df]).reset_index(drop=True)

    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 18 -> [OK]')
    logging.info('')
    return df_clusters_AB


# Function: Build. Energy Sim. -> Preprocess -> Step 19 -> Perform clustering (SFH)
def bp1_step_19(SFH_df, n_clusters_SFH):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 19 -> Performing clustering (SFH)...')
    
    df_all_Sub_sector = pd.DataFrame()
    df_clusters_SFH = pd.DataFrame(
        columns = ['Sub_sector', 'Cluster', 'Centroid_GHS_Heightmean', 'Centroid_ExtFachade', 'Centroid_ShapeFactor'])

    def calculate_distance(row, centroid):
        return np.sqrt(
            (row['%ExtFachade'] - centroid['%ExtFachade']) ** 2
            + (row['ShapeFactor'] - centroid['ShapeFactor']) ** 2
            + (row['GHS_Heightmean'] - centroid['GHS_Heightmean']) ** 2)

    # Iterating over each unique Sub_sector in the dataset
    for Sub_sector in SFH_df['Sub_sector'].unique():
        # Selecting the rows for specific Sub_sector
        df_subsector = SFH_df.loc[SFH_df['Sub_sector'] == Sub_sector].copy()
        df_subsector['NormalizedBuiltArea'] = df_subsector['Building_GFA'] / df_subsector['Building_GFA'].sum()
        weights = df_subsector['NormalizedBuiltArea'].values
        df_clustering = df_subsector[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']]
        
        # Scaling the features to have zero mean and unit variance using StandardScaler for optimal performance
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_clustering)

        # Applying KMeans clustering algorithm
        km = KMeans(n_clusters=n_clusters_SFH, max_iter = 8000)
        df_subsector['cluster'] = km.fit_predict(df_scaled, sample_weight = weights)

        # Assign a unique cluster identifier for each Sub_sector
        df_subsector['cluster'] = df_subsector['cluster'].apply(lambda x: f"{x}_{Sub_sector}")

        # Compute the centroids of each cluster
        centroids = df_subsector.groupby('cluster')[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']].mean()
        df_subsector['distance'] = df_subsector.apply(lambda row: calculate_distance(row, centroids.loc[row['cluster']]), axis=1)
        df_subsector_centroid_osmids = df_subsector.loc[df_subsector.groupby('cluster')['distance'].idxmin()]
        df_centroid_osm_ids = df_subsector_centroid_osmids.set_index('cluster')['osm_id']
        df_subsector['centroid_osm_id'] = df_subsector['cluster'].apply(
            lambda x: 1 if df_centroid_osm_ids[x] in df_subsector['osm_id'].values else 0)
        sum_GFArea = df_subsector.groupby('cluster')['Building_GFA'].sum()

        df_all_Sub_sector = pd.concat([df_all_Sub_sector, df_subsector])
        for cluster in df_subsector['cluster'].unique():
            centroid = centroids.loc[cluster]
            closest_entity = df_subsector[df_subsector['osm_id'] == df_centroid_osm_ids[cluster]]
            new_df = pd.DataFrame([{'Sub_sector': Sub_sector,
                'Cluster': cluster, 'Centroid_GHS_Heightmean': centroid['GHS_Heightmean'],
                'Centroid_ExtFachade': centroid['%ExtFachade'], 'Centroid_ShapeFactor': centroid['ShapeFactor'],
                'Closest_Entity_OSM_ID': closest_entity['osm_id'].values[0],
                'Closest_Entity_FootprintArea': closest_entity['BuildingFP_area'].values[0],
                'Closest_Entity_GFA': closest_entity['Building_GFA'].values[0],
                'Closest_Entity_Height': closest_entity['GHS_Heightmean'].values[0],
                'Closest_Entity_N_floors': closest_entity['N_Floors'].values[0],
                'Closest_Entity_Volume': closest_entity['Volume'].values[0],
                'Closest_Entity_TotalPerimeter': closest_entity['perimeter'].values[0],
                'Closest_Entity_%ExtFachade': closest_entity['%ExtFachade'].values[0],
                'Closest_Entity_R_WalltoGFA': closest_entity['R_WalltoGFA'].values[0],
                'Closest_Entity_ShapeFactor': closest_entity['ShapeFactor'].values[0], 'Sum_GFArea': sum_GFArea[cluster]}])

            new_df = new_df.dropna(how = 'all', axis = 1)
            new_df = new_df.dropna(how = 'all', axis = 0)
            df_clusters_SFH = df_clusters_SFH.dropna(how = 'all', axis = 1)
            df_clusters_SFH = df_clusters_SFH.dropna(how = 'all', axis = 0)
            df_clusters_SFH = pd.concat([df_clusters_SFH, new_df]).reset_index(drop=True)

    # Conversion of 'Period' to 'Year' through a dictionary mapping
    period_to_year = {
        'Before1945': 1900,
        '1945to1969': 1955,
        '1970to1979': 1975,
        '1980to1989': 1985,
        '1990to2000': 1995,
        '2000to2010': 2005,
        'Post2010': 2020
    }

    # Iterate over each row in df_clusters_SFH
    new_rows = []
    for _, row in df_clusters_SFH.iterrows():
        for period, year in period_to_year.items():
            new_row = row.copy()
            new_row['Period'] = period
            new_row['Year'] = year
            new_rows.append(new_row)
    df_expanded = pd.DataFrame(new_rows)

    # Reset the index of the expanded DataFrame
    df_expanded.reset_index(drop=True, inplace=True)

    # First, 'melt' df_all_Sub_sector to get a row for each cluster and period
    df_area = df_all_Sub_sector.melt(id_vars=['cluster'],
                                     value_vars=[c for c in df_all_Sub_sector.columns if c.endswith('_A')],
                                     var_name='Period',
                                     value_name='Area')

    # Remove the '_A' from the end of the period
    df_area['Period'] = df_area['Period'].str.rstrip('_A')

    # Sum the area values by cluster and period
    df_area = df_area.groupby(['cluster', 'Period'])['Area'].sum().reset_index()

    # Create a combined index column for df_area
    df_area['merge_index'] = df_area['cluster'] + df_area['Period']

    # Create a combined index column for df_expanded
    df_expanded['merge_index'] = df_expanded['Cluster'] + df_expanded['Period']

    # Sort df_area by this combined index
    df_area.sort_values('merge_index', inplace = True)

    # Create a new df that merges on 'merge_index'
    df_merged_SFH = df_expanded.merge(df_area, how = 'left', on = 'merge_index')

    # Now we no longer need the 'merge_index' column
    df_merged_SFH.drop(columns = 'merge_index', inplace = True)
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 19 -> [OK]')
    logging.info('')
    return df_merged_SFH


# Function: Build. Energy Sim. -> Preprocess -> Step 20 -> Perform clustering (SS)
def bp1_step_20(SS_df, n_clusters_SS):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 20 -> Performing clustering (SS)...')
    
    df_all_Sub_sector = pd.DataFrame()
    df_clusters_SS = pd.DataFrame(
        columns = ['Sub_sector', 'Cluster', 'Centroid_GHS_Heightmean', 'Centroid_ExtFachade', 'Centroid_ShapeFactor'])

    def calculate_distance(row, centroid):
        return np.sqrt(
            (row['%ExtFachade'] - centroid['%ExtFachade']) ** 2
            + (row['ShapeFactor'] - centroid['ShapeFactor']) ** 2
            + (row['GHS_Heightmean'] - centroid['GHS_Heightmean']) ** 2)

    for Sub_sector in SS_df['Sub_sector'].unique():
        df_subsector = SS_df.loc[SS_df['Sub_sector'] == Sub_sector].copy()
        df_subsector['NormalizedBuiltArea'] = df_subsector['Building_GFA'] / df_subsector['Building_GFA'].sum()
        weights = df_subsector['NormalizedBuiltArea'].values
        df_clustering = df_subsector[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']]

        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_clustering)

        km = KMeans(n_clusters=n_clusters_SS, max_iter=8000)
        df_subsector['cluster'] = km.fit_predict(df_scaled, sample_weight=weights)
        df_subsector['cluster'] = df_subsector['cluster'].apply(lambda x: f"{x}_{Sub_sector}")

        centroids = df_subsector.groupby('cluster')[['GHS_Heightmean', '%ExtFachade', 'ShapeFactor']].mean()
        df_subsector['distance'] = df_subsector.apply(lambda row: calculate_distance(row, centroids.loc[row['cluster']]), axis = 1)

        df_subsector_centroid_osmids = df_subsector.loc[df_subsector.groupby('cluster')['distance'].idxmin()]
        df_centroid_osm_ids = df_subsector_centroid_osmids.set_index('cluster')['osm_id']
        df_subsector['centroid_osm_id'] = df_subsector['cluster'].apply(
            lambda x: 1 if df_centroid_osm_ids[x] in df_subsector['osm_id'].values else 0)
        sum_GFArea = df_subsector.groupby('cluster')['Building_GFA'].sum()

        df_all_Sub_sector = pd.concat([df_all_Sub_sector, df_subsector])
        for cluster in df_subsector['cluster'].unique():
            centroid = centroids.loc[cluster]
            closest_entity = df_subsector[df_subsector['osm_id'] == df_centroid_osm_ids[cluster]]
            new_df = pd.DataFrame([{'Sub_sector': Sub_sector,
                'Cluster': cluster, 'Centroid_GHS_Heightmean': centroid['GHS_Heightmean'],
                'Centroid_ExtFachade': centroid['%ExtFachade'], 'Centroid_ShapeFactor': centroid['ShapeFactor'],
                'Closest_Entity_OSM_ID': closest_entity['osm_id'].values[0],
                'Closest_Entity_FootprintArea': closest_entity['BuildingFP_area'].values[0],
                'Closest_Entity_GFA': closest_entity['Building_GFA'].values[0],
                'Closest_Entity_Height': closest_entity['GHS_Heightmean'].values[0],
                'Closest_Entity_N_floors': closest_entity['N_Floors'].values[0],
                'Closest_Entity_Volume': closest_entity['Volume'].values[0],
                'Closest_Entity_TotalPerimeter': closest_entity['perimeter'].values[0],
                'Closest_Entity_%ExtFachade': closest_entity['%ExtFachade'].values[0],
                'Closest_Entity_R_WalltoGFA': closest_entity['R_WalltoGFA'].values[0],
                'Closest_Entity_ShapeFactor': closest_entity['ShapeFactor'].values[0], 'Sum_GFArea': sum_GFArea[cluster]}])

            new_df = new_df.dropna(how = 'all', axis = 1)
            new_df = new_df.dropna(how = 'all', axis = 0)
            df_clusters_SS = df_clusters_SS.dropna(how = 'all', axis = 1)
            df_clusters_SS = df_clusters_SS.dropna(how = 'all', axis = 0)
            df_clusters_SS = pd.concat([df_clusters_SS, new_df]).reset_index(drop = True)

        period_to_year = {
            'Before1945': 1900,
            '1945to1969': 1955,
            '1970to1979': 1975,
            '1980to1989': 1985,
            '1990to2000': 1995,
            '2000to2010': 2005,
            'Post2010': 2020
        }

        # Iterate over each row in df_clusters_SS
        new_rows = []
        for _, row in df_clusters_SS.iterrows():
            for period, year in period_to_year.items():
                new_row = row.copy()
                new_row['Period'] = period
                new_row['Year'] = year
                new_rows.append(new_row)

        df_expanded = pd.DataFrame(new_rows)

        # Reset the new dataframe index
        df_expanded.reset_index(drop = True, inplace = True)

        # First, we melt df_all_Sub_sector to get one row for each cluster and period.
        df_area = df_all_Sub_sector.melt(id_vars=['cluster'],
            value_vars = [c for c in df_all_Sub_sector.columns if c.endswith('_A')], var_name = 'Period', value_name = 'Area')

        # We remove the '_A' from the end of the period
        df_area['Period'] = df_area['Period'].str.rstrip('_A')

        # add the values of area per cluster and period
        df_area = df_area.groupby(['cluster', 'Period'])['Area'].sum().reset_index()

        # We create a combined index column for df_area
        df_area['merge_index'] = df_area['cluster'] + df_area['Period']

        # Create a combined index column for df_expanded
        df_expanded['merge_index'] = df_expanded['Cluster'] + df_expanded['Period']

        # We sort df_area by this combined index
        df_area.sort_values('merge_index', inplace = True)

        # We create a new df that is merge on merge_index
        df_mergedSS = df_expanded.merge(df_area, how = 'left', on = 'merge_index')

        # Then we no longer need the merge_index column
        df_mergedSS.drop(columns = 'merge_index', inplace = True)
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 20 -> [OK]')
    logging.info('')
    return df_mergedSS


# Function: Build. Energy Sim. -> Preprocess -> Step 21 -> Create the final Dataframe
def bp1_step_21(df_clusters_AB, df_clusters_SFH, df_clusters_Ss, process, username, nutsid):
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> Creating the final Dataframe...')
    
    # Create an empty DataFrame with the required columns
    final_df = pd.DataFrame(columns = ['Building ID', 'Use', 'Age', 'Footprint Area', 'Number of floors', 'Volume', 'Gross floor area',
        'Total External Facade area', 'Opaque Facade area', 'Window area', 'Height'])

    # Define the auxiliary function for calculating the required fields
    def calculate_fields(df, use, building_id_format):
        df_new = pd.DataFrame()
        if building_id_format == 'AB_Format':
            df_new['Building ID'] = 'Apartment Block' + '_' + df['Cluster'].astype(str)
        else:
            df_new['Building ID'] = df['Cluster'].astype(str) + '_' + df['Year'].astype(str)
        df_new['Use'] = df[use] if use != 'Apartment Block' else use
        df_new['Age'] = df['Year']
        df_new['Footprint Area'] = df['Area'] / df['Closest_Entity_N_floors']
        df_new['Number of floors'] = df['Closest_Entity_N_floors']
        df_new['Volume'] = (df['Area'] / df['Closest_Entity_N_floors']) * df['Closest_Entity_Height']
        df_new['Gross floor area'] = df['Area']
        df_new['Total External Facade area'] = (df['Closest_Entity_R_WalltoGFA'] * df['Area'] * df['Closest_Entity_%ExtFachade'])
        df_new['Height'] = df['Closest_Entity_Height']
        return df_new

    # Apply the auxiliary function to calculate the fields and add them to the final DataFrame
    frames = [calculate_fields(df_clusters_AB, use = 'Apartment Block', building_id_format = 'AB_Format'),
              calculate_fields(df_clusters_SFH, use = 'Sub_sector', building_id_format = 'SS_Format'),
              calculate_fields(df_clusters_SS, use = 'Sub_sector', building_id_format = 'SS_Format')]
    final_df = pd.concat(frames)
    
    # Save the DataFrame as a CSV file
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> Saving...')
    csv_name = io.retrieveOutputTmpPathConcatFile(True, process, username, nutsid, config)
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> Temp. output file -> ' + csv_name)
    final_df.to_csv(csv_name, index = False, sep = ',')
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> Saved!!')
    
    # Finish
    logging.info('  QGIS Server/> Build. Energy Sim. -> Preprocess -> Step 21 -> [OK]')
    logging.info('')
    return final_df, csv_name
    
    

#####################################################################
######################## Auxiliary functions ########################
#####################################################################



# Auxiliary function: Get pixel value
def getPixelValue(centroid_x, centroid_y, raster_data, transform):
    pixel_x, pixel_y = ~transform['transform'] * (centroid_x, centroid_y)
    pixel_x, pixel_y = int(pixel_x), int(pixel_y)
    pixel_value = raster_data[pixel_y, pixel_x]
    return pixel_value

