import logging
import math
import os

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from pyproj import CRS, Transformer
from rasterio.mask import mask
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling
from shapely.geometry import shape

import modules.io as io

from modules.logging_config import logger


####################################################################
############################ Preprocess ############################
####################################################################

# Function: PV Power Plants -> Preprocess -> Step 01 -> Process the layer and retrieve the output files
def pv1Step01(layer, nutsId, config):
    ''' PV Power Plants -> Preprocess -> Step 01 : Process the layer and retrieve the output files. '''

    # Read the layer file and convert it to a dataframe
    layerName = layer['name'] + '.' + layer['format']
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Processing "' + layerName + '"...')
    df = gpd.read_file(io.retrieveBasePath(config) + layer['path'])
    
    # Filter the dataframe rows
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Filtering the rows...')
    dfFiltered = df[(df['NUTS_ID'].str.startswith(nutsId)) & (df['LEVL_CODE'] == 3)]
    
    # Obtain the NUTS name
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Obtaining the NUTS name and aggregating a new column...')
    nutsName = df[(df['NUTS_ID'] == nutsId) & (df['LEVL_CODE'] == 2)]['NUTS_NAME'].values[0]
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> NUTS name -> ' + nutsName)
    dfFiltered['NUTS2_NAME'] = nutsName
                        
    # Change the reference system to CRS 4326
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Changing the reference system to CRS 4326...')
    dfFilteredCrs = dfFiltered.to_crs(epsg=4326)
    dfFilteredCrs54009 = dfFiltered.to_crs('Esri:54009')

    # Save all
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Saving...')
    output = io.buildOutputPathPV1Step01(layer, nutsId, config)
    dfFiltered.to_file(output, driver=layer['format'].upper())
    
    outputCrs = io.buildOutputPathCRSPV1Step01(layer, nutsId, 4326, config)
    dfFilteredCrs.to_file(outputCrs, driver = 'GPKG')
    
    outputCrs54009 = io.buildOutputPathCRSPV1Step01(layer, nutsId, 54009, config)
    dfFilteredCrs54009.to_file(outputCrs54009, driver = 'GPKG')
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> [OK]')
    logger.info('')
    return output, outputCrs


# Function: PV Power Plants -> Preprocess -> Steps 02, 03, 04, 05 -> Apply the mask layer
def pv1Steps02030405(layer, mask, step, config):
    ''' PV Power Plants -> Preprocess -> Steps 02, 03, 04 and 05 : Apply the mask layer. '''
    
    layerName = layer['name'] + '.' + layer['format']
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Processing "' + layerName + '"...')
    
    # Read the vectorial file with Geopandas
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Reading the file...')
    gdFile = gpd.read_file(mask)

    # Extract the geometries from the vectorial file
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Extracting the geometries...')
    geoms = gdFile.geometry.values

    # Transform
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Transforming...')
    with rasterio.open(io.retrieveBasePath(config) + layer['path']) as src:
        outImage, outTransformed = rasterio.mask.mask(src, geoms, crop=True)
        outMeta = src.meta.copy()
        
        # Configure the metadata
        outMeta.update({
            "driver": "GTiff",
            "height": outImage.shape[1],
            "width": outImage.shape[2],
            "transform": outTransformed
        })

        # Save the temporary layer
        logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Saving...')
        output = io.buildOutputPathPV1Steps02030405(layer, config)
        with rasterio.open(output, "w", **outMeta) as dst:
            dst.write(outImage)
    
    # Finish
    if step == 5:
        logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> The layers have been clipped!')
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> [OK]')
    logger.info('')
    return output


# Function: PV Power Plants -> Preprocess -> Step 06 -> Filter the slope raster
def pv1Step06(slopeRasterClippedPath, slopeAngle, config):
    ''' PV Power Plants -> Preprocess -> Step 06 : Filter the slope raster. '''

    # Transform
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 06 -> Transforming...')
    nodataVal = 0
    with rasterio.open(slopeRasterClippedPath) as src:
        imageData = src.read(1)
        outMeta = src.meta.copy()

    # Configure the metadata
    slope_radians = np.radians(slopeAngle)
    umbralDN = 250.0 * np.cos(slope_radians)
    outMeta.update({
        "driver": "GTiff",
        "dtype": rasterio.uint8,
        "nodata": nodataVal
    })

    # Save
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 06 -> Saving...')
    filteredSlopeRasterPath = io.buildOutputPathPV1Steps0607(slopeRasterClippedPath)
    newImage = np.where(imageData > umbralDN, 1, 0)
    with rasterio.open(filteredSlopeRasterPath, "w", **outMeta) as dst:
        dst.write(newImage, 1)

    # Finish    
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 06 -> [OK]')
    logger.info('')
    return filteredSlopeRasterPath


# Function: PV Power Plants -> Preprocess -> Step 07 -> Filter raster by user codes
def pv1Step07(srcPath, config):
    ''' PV Power Plants -> Preprocess -> Step 07 : Filter raster by user codes. '''
    
    # Build "user codes" as a list
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> Building user codes...')
    userCodes = config['IDESIGNRES-PARAMETERS']['idesignres.params.user.codes'].split(',')
    userCodes = [int(x) for x in userCodes]
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> User codes -> ' + str(userCodes))
    
    # Open the raster layer and filter
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> Filtering...')
    nodataVal = 0
    with rasterio.open(srcPath) as src:
        # Open the image
        outImage = src.read(1)

        # Fill the "nodata" values with 0s
        outImage[outImage == src.nodata] = 0

        # Filter the image using the user codes
        # The values of the user codes list become 1s (the rest are 0s)
        newImage = np.isin(outImage, userCodes).astype('uint8')

        # Configure the metadata
        outMeta = src.meta.copy()
        outMeta.update({
            "driver": "GTiff",
            "nodata": nodataVal,
            "dtype": 'uint8'
        })

    # Save    
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> Saving...')
    output = io.buildOutputPath_pv1_steps_06_07(srcPath)
    with rasterio.open(output, "w", **outMeta) as dst:
        dst.write(newImage, 1)

    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> [OK]')
    logger.info('')
    return output


# Function: PV Power Plants -> Preprocess -> Steps 08, 10 -> Change a raster resolution
def pv1Steps0810(srcPath, step, config):
    ''' PV Power Plants -> Preprocess -> Steps 09 and 10 : Change a raster resolution. '''
    
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Changing the resolution...')
    dstCrs = CRS.from_epsg(3035)
    dstResolution = float(config['IDESIGNRES-PARAMETERS']['idesignres.params.dst.resolution'])

    with rasterio.open(srcPath) as src:
        logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Transforming...')
        transformer = Transformer.from_crs(src.crs, dstCrs, always_xy = True)
        left, bottom, right, top = transformer.transform_bounds(*src.bounds)

        left = math.floor(left / dstResolution) * dstResolution
        bottom = math.floor(bottom / dstResolution) * dstResolution
        right = math.ceil(right / dstResolution) * dstResolution
        top = math.ceil(top / dstResolution) * dstResolution

        width = int((right - left) / dstResolution)
        height = int((top - bottom) / dstResolution)

        transform = rasterio.Affine(dstResolution, 0.0, left, 0.0, -dstResolution, top)
        data = src.read()
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': src.crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Save    
        logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Saving...')
        output = io.buildOutputPathPV1Steps0810(srcPath)
        with rasterio.open(output, 'w', **kwargs) as dst:
            dst.write(src.read())

    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> [OK]')
    logger.info('')
    return output


# Function: PV Power Plants -> Preprocess -> Step 09, 11, 13 -> Adjust to the size of the "slope" raster
def pv1Steps091113(srcFile, dstFile, step, config):
    ''' PV Power Plants -> Preprocess -> Steps 09, 11 and 13 : Adjust to the size of the slope raster. '''
    
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Reading the metadata of the source layer...')
    with rasterio.open(srcFile) as src:
        dstResolution = float(config['IDESIGNRES-PARAMETERS']['idesignres.params.dst.resolution'])
        srcTransform = src.transform
        srcWidth = src.width
        srcHeight = src.height
        srcBounds = src.bounds
        srcCrs = src.crs
        srcNodata = src.nodata

    # Adjust the 'dst' layer to fit with 'src' layer bounds
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Transforming...')
    with rasterio.open(dstFile) as dst:
        dstTransform = dst.transform
        dstResolution = dst.res
        dstNodata = dst.nodata if dst.nodata is not None else np.nan
        
        newTransform = from_bounds(srcBounds.left, srcBounds.bottom,
            srcBounds.right, srcBounds.top, srcWidth, srcHeight)

        logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Calculating the new "width" and "height"...')
        newWidth = int((srcBounds.right - srcBounds.left) / dstResolution[0])
        newHeight = int((srcBounds.top - srcBounds.bottom) / dstResolution[1])

        logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Updating metadata for the new layer...')
        outMeta = dst.meta.copy()
        outMeta.update({
            'driver': 'GTiff',
            'height': newHeight,
            'width': newWidth,
            'transform': newTransform,
            'nodata': dstNodata,
            'crs': dst.crs
        })

        # Create an empty array for the result
        result = np.full((dst.count, newHeight, newWidth), dstNodata, dtype = dst.dtypes[0])
        for i in range(1, dst.count + 1):
            dstData = dst.read(i, window = dst.window(*srcBounds),
                boundless = True,
                outShape = (newHeight, newWidth),
                resampling = rasterio.enums.Resampling.nearest)
            result[i - 1, :, :] = dstData

    # Save
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Saving...')
    output = io.buildOutputPathPV1Steps091113(dstFile)
    with rasterio.open(output, 'w', **outMeta) as dstAdjusted:
        dstAdjusted.write(result)

    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> [OK]')
    logger.info('')
    return output


# Function: PV Power Plants -> Preprocess -> Step 12 -> Change a raster resolution and reference system
def pv1Step12(inputPath, config):
    ''' PV Power Plants -> Preprocess -> Step 12 : Change a raster resolution and reference system. '''

    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> Reading the metadata of the source layer...')
    dstCrs = CRS.from_epsg(3035)
    dstResolution = float(config['IDESIGNRES-PARAMETERS']['idesignres.params.dst.resolution'])
    
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> Tansforming...')
    with rasterio.open(inputPath) as src:
        transformer = Transformer.from_crs(src.crs, dstCrs, always_xy = True)

        left, bottom, right, top = transformer.transform_bounds(*src.bounds)
        left = math.floor(left / dstResolution) * dstResolution
        bottom = math.floor(bottom / dstResolution) * dstResolution
        right = math.ceil(right / dstResolution) * dstResolution
        top = math.ceil(top / dstResolution) * dstResolution

        width = int((right - left) / dstResolution)
        height = int((top - bottom) / dstResolution)
        transform = rasterio.Affine(dstResolution, 0.0, left, 0.0, -dstResolution, top)

        logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> Updating metadata for the new layer...')
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dstCrs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Save
        logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> Saving...')
        output = io.buildOutputPathPV1Step12(inputPath)
        with rasterio.open(output, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source = rasterio.band(src, i),
                    destination = rasterio.band(dst, i),
                    srcTransform = src.transform,
                    srcCrs = src.crs,
                    dstTransform = transform,
                    dstCrs = dstCrs,
                    resampling = Resampling.bilinear
                )

        # Finish
        logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> [OK]')
        logger.info('')
        return output


# Function: PV Power Plants -> Preprocess -> Step 14 -> Calculate the multiplication of all the layers
def pv1Step14(GHIAlignedOutput, npaAlignedOutput, landuseAlignedPath, slopeFltPath, config):
    ''' PV Power Plants -> Preprocess -> Step 14 : Calculate the multiplication of all the layers. '''

    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 14 -> Calculating...')
    resultPath = io.retrieveRadiationPotentialAreasPath(config)
    with rasterio.open(GHIAlignedOutput) as src1, \
            rasterio.open(npaAlignedOutput) as src2, \
            rasterio.open(landuseAlignedPath) as src3, \
            rasterio.open(slopeFltPath) as src4:
        ghiThreshold = src1.read(1)
        ghiThreshold[ghiThreshold == src1.nodata] = 0

        filteredLandUse = src2.read(1)
        filteredLandUse[filteredLandUse == src2.nodata] = 0

        slopeThreshold = src3.read(1)
        slopeThreshold[slopeThreshold == src3.nodata] = 0

        nonProtectedAreas = src4.read(1)
        nonProtectedAreas[nonProtectedAreas == src4.nodata] = 0

    newImage = ghiThreshold * filteredLandUse * slopeThreshold * nonProtectedAreas

    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 14 -> Updating metadata for the output raster...')
    meta = src1.meta
    meta.update(dtype = rasterio.float32, count = 1)

    # Save
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 14 -> Saving...')
    with rasterio.open(resultPath, 'w', **meta) as dst:
        dst.write(newImage.astype(rasterio.float32), 1)

    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 14 -> [OK]')
    logger.info('')
    return resultPath



# Function: PV Power Plants -> Preprocess -> Step 15 -> Calculate regions
def pv1Step15(radiationPotentialAreas, nutsOutputPath, process, username, nutsid, config):
    ''' PV Power Plants -> Preprocess -> Step 15 : Calculate regions. '''

    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Loading the files...')
    radiationThresholdStart = int(config['IDESIGNRES-PARAMETERS']['idesignres.params.radiation.threshold.start'])
    
    # Function: Convert to degrees
    def convertToDegrees(x, y):
        transformer = Transformer.from_crs('EPSG:3035', 'EPSG:4326', always_xy = True)
        lon, lat = transformer.transform(x, y)
        return lon, lat

    # Read raster file for the first time just to get maximum value and resolution
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Reading the raster file...')
    with rasterio.open(radiationPotentialAreas) as src:
        rasterData = src.read(1)
        res = src.res

    # Read the vectorial file with Geopandas
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Reading the vectorial file...')
    gdf = gpd.read_file(nutsOutputPath)

    # Define radiation thresholds
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Defining the radiation threshold...')
    radiationThresholds = range(radiationThresholdStart, int(np.max(rasterData)) + 100, 100)

    # Create a DataFrame to store results
    columns = ['Region', 'Centroid_X', 'Centroid_Y', 'Total_Area', 'Max_Radiation', 'Average_Radiation', 'Threshold',
               'Area_m2', 'Median_Radiation', 'Median_Radiation_X', 'Median_Radiation_Y']
    df = pd.DataFrame(columns = columns)

    # For each region
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Transforming...')
    for index, row in gdf.iterrows():
        geom = shape(row['geometry'])

        # Open raster file again
        with rasterio.open(radiationPotentialAreas) as src:
            # Clip the raster to the region
            clippedImage, outTransform = mask(src, [geom], crop=True)
            clippedImage = clippedImage[0]

            # Get the NoData value of the raster
            nodata = src.nodata

            # Exclude NoData values
            outImage = clippedImage[clippedImage != nodata]

            # Obtain the centroid of the region
            centroid = geom.centroid
            centroidLon, centroidLat = convertToDegrees(centroid.x, centroid.y)
            baseData = [row['NUTS_ID'], centroidLon, centroidLat, geom.area, outImage.max(), outImage.mean()]

            for i, threshold in enumerate(radiationThresholds):
                nextThreshold = radiationThresholds[i + 1] if i + 1 < len(radiationThresholds) else float('inf')

                # Start the data for this threshold level
                thresholdData = list(baseData)
                thresholdData.append(threshold)

                # Calculate area for this radiation range
                areaM2 = ((outImage >= threshold) & (outImage < nextThreshold)).sum() * res[0] * res[1]
                thresholdData.append(areaM2)

                # Handle the radiant calculations if the area is not null
                thresholdImage2d = np.copy(clippedImage)
                thresholdImage2d[(thresholdImage2d < threshold) |
                    (thresholdImage2d >= nextThreshold) | (thresholdImage2d == nodata)] = np.nan
                thresholdMask2d = ~np.isnan(thresholdImage2d)

                if areaM2 > 0:
                    thresholdImage1d = thresholdImage2d[thresholdMask2d]

                    # Calculate the median radiation value for the current threshold
                    medianThreshold = np.median(thresholdImage1d)
                    thresholdData.append(medianThreshold)

                    # Construct an array where each pixel's value is the distance from the median
                    distancesToMedian = np.abs(thresholdImage2d - medianThreshold)
                    
                    # Set distances outside of the mask to an arbitrary large number for correct pixel selection later
                    distancesToMedian[~thresholdMask2d] = np.inf

                    # Get indices of the pixel with value closest to the median
                    closestPixelYIindex, closestPixelXIndex = np.unravel_index(
                        np.argmin(distancesToMedian),
                        thresholdImage2d.shape)

                    # The coordinates of the pixel center
                    closestPixelX, closestPixelY = outTransform * (
                        closestPixelXIndex + 0.5, closestPixelYIindex + 0.5)
                    closestPixelLon, closestPixelLat = convertToDegrees(closestPixelX, closestPixelY)

                    thresholdData.extend([closestPixelLon, closestPixelLat])
                else:
                    thresholdData.extend([np.nan, np.nan, np.nan])

                # Append the results for this threshold to the DataFrame
                df.loc[len(df)] = thresholdData

    # Save the DataFrame as a CSV file
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Saving...')
    csvName = io.retrieveOutputTmpPathConcatFile(True, process, username, nutsid, config)
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Temp. output file -> ' + csvName)
    df.to_csv(csvName, index = False, sep = ',')
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Saved!!')
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> [OK]')
    logger.info('')
    return csvName

