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


####################################################################
############################ Preprocess ############################
####################################################################

# Function: PV Power Plants -> Preprocess -> Step 01 -> Process the layer and retrieve the output files
def pv1_step_01(layer, nuts_id, config):
    # Read the layer file and convert it to a dataframe
    layer_name = layer['name'] + '.' + layer['format']
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Processing "' + layer_name + '"...')
    df = gpd.read_file(io.retrieveBasePath(config) + layer['path'])
    
    # Filter the dataframe rows
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Filtering the rows...')
    df_filtered = df[(df['NUTS_ID'].str.startswith(nuts_id)) & (df['LEVL_CODE'] == 3)]
    
    # Obtain the NUTS name
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Obtaining the NUTS name and aggregating a new column...')
    nuts_name = df[(df['NUTS_ID'] == nuts_id) & (df['LEVL_CODE'] == 2)]['NUTS_NAME'].values[0]
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> NUTS name -> ' + nuts_name)
    df_filtered['NUTS2_NAME'] = nuts_name
                        
    # Change the reference system to CRS 4326
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Changing the reference system to CRS 4326...')
    df_filtered_crs = df_filtered.to_crs(epsg=4326)
    df_filtered_crs54009 = df_filtered.to_crs('Esri:54009')

    # Save all
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> Saving...')
    output = io.buildOutputPath_pv1_step_01(layer, nuts_id, config)
    df_filtered.to_file(output, driver=layer['format'].upper())
    
    output_crs = io.buildOutputPathCRS_pv1_step_01(layer, nuts_id, 4326, config)
    df_filtered_crs.to_file(output_crs, driver='GPKG')
    
    output_crs54009 = io.buildOutputPathCRS_pv1_step_01(layer, nuts_id, 54009, config)
    df_filtered_crs54009.to_file(output_crs54009, driver='GPKG')
    
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 01 -> [OK]')
    logging.info('')
    return output, output_crs


# Function: PV Power Plants -> Preprocess -> Steps 02, 03, 04, 05 -> Apply the mask layer
def pv1_steps_02_03_04_05(layer, mask, step, config):
    layer_name = layer['name'] + '.' + layer['format']
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Processing "' + layer_name + '"...')
    
    # Read the vectorial file with Geopandas
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Reading the file...')
    gd_file = gpd.read_file(mask)

    # Extract the geometries from the vectorial file
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Extracting the geometries...')
    geoms = gd_file.geometry.values

    # Transform
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Transforming...')
    with rasterio.open(io.retrieveBasePath(config) + layer['path']) as src:
        out_image, out_transformed = rasterio.mask.mask(src, geoms, crop=True)
        out_meta = src.meta.copy()
        
        # Configure the metadata
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transformed
        })

        # Save the temporary layer
        logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Saving...')
        output = io.buildOutputPath_pv1_steps_02_03_04_05(layer, config)
        with rasterio.open(output, "w", **out_meta) as dst:
            dst.write(out_image)
    
    # Finish
    if step == 5:
        logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> The layers have been clipped!')
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> [OK]')
    logging.info('')
    return output


# Function: PV Power Plants -> Preprocess -> Step 06 -> Filter the slope raster
def pv1_step_06(slope_raster_clipped_path, slope_angle, config):
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 06 -> Processing...')

    # Transform
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 06 -> Transforming...')
    nodata_val = 0
    with rasterio.open(slope_raster_clipped_path) as src:
        image_data = src.read(1)
        out_meta = src.meta.copy()

    # Configure the metadata
    slope_radians = np.radians(slope_angle)
    DN_umbral = 250.0 * np.cos(slope_radians)
    out_meta.update({
        "driver": "GTiff",
        "dtype": rasterio.uint8,
        "nodata": nodata_val
    })

    # Save
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 06 -> Saving...')
    filtered_slope_raster_path = io.buildOutputPath_pv1_steps_06_07(slope_raster_clipped_path)
    new_image = np.where(image_data > DN_umbral, 1, 0)
    with rasterio.open(filtered_slope_raster_path, "w", **out_meta) as dst:
        dst.write(new_image, 1)

    # Finish    
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 06 -> [OK]')
    logging.info('')
    return filtered_slope_raster_path


# Function: PV Power Plants -> Preprocess -> Step 07 -> Filter raster by user codes
def pv1_step_07(src_path, config):
    # Build "user codes" as a list
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> Building user codes...')
    user_codes = config['IDESIGNRES-PARAMETERS']['idesignres.params.user.codes'].split(',')
    user_codes = [int(x) for x in user_codes]
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> User codes -> ' + str(user_codes))
    
    # Open the raster layer and filter
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> Filtering...')
    nodata_val = 0
    with rasterio.open(src_path) as src:
        # Open the image
        out_image = src.read(1)

        # Fill the "nodata" values with 0s
        out_image[out_image == src.nodata] = 0

        # Filter the image using the user codes
        # The values of the user codes list become 1s (the rest are 0s)
        new_image = np.isin(out_image, user_codes).astype('uint8')

        # Configure the metadata
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "nodata": nodata_val,
            "dtype": 'uint8'
        })

    # Save    
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> Saving...')
    output = io.buildOutputPath_pv1_steps_06_07(src_path)
    with rasterio.open(output, "w", **out_meta) as dst:
        dst.write(new_image, 1)

    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 07 -> [OK]')
    logging.info('')
    return output


# Function: PV Power Plants -> Preprocess -> Steps 08, 10 -> Change a raster resolution
def pv1_steps_08_10(src_path, step, config):
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Changing the resolution...')
    dst_crs = CRS.from_epsg(3035)
    dst_resolution = float(config['IDESIGNRES-PARAMETERS']['idesignres.params.dst.resolution'])

    with rasterio.open(src_path) as src:
        logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Transforming...')
        transformer = Transformer.from_crs(src.crs, dst_crs, always_xy = True)
        left, bottom, right, top = transformer.transform_bounds(*src.bounds)

        left = math.floor(left / dst_resolution) * dst_resolution
        bottom = math.floor(bottom / dst_resolution) * dst_resolution
        right = math.ceil(right / dst_resolution) * dst_resolution
        top = math.ceil(top / dst_resolution) * dst_resolution

        width = int((right - left) / dst_resolution)
        height = int((top - bottom) / dst_resolution)

        transform = rasterio.Affine(dst_resolution, 0.0, left, 0.0, -dst_resolution, top)
        data = src.read()
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': src.crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Save    
        logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Saving...')
        output = io.buildOutputPath_pv1_steps_08_10(src_path)
        with rasterio.open(output, 'w', **kwargs) as dst:
            dst.write(src.read())

    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> [OK]')
    logging.info('')
    return output


# Function: PV Power Plants -> Preprocess -> Step 09, 11, 13 -> Adjust to the size of the "slope" raster
def pv1_steps_09_11_13(src_file, dst_file, step, config):
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Reading the metadata of the source layer...')
    with rasterio.open(src_file) as src:
        dst_resolution = float(config['IDESIGNRES-PARAMETERS']['idesignres.params.dst.resolution'])
        src_transform = src.transform
        src_width = src.width
        src_height = src.height
        src_bounds = src.bounds
        src_crs = src.crs
        src_nodata = src.nodata

    # Adjust the 'dst' layer to fit with 'src' layer bounds
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Transforming...')
    with rasterio.open(dst_file) as dst:
        dst_transform = dst.transform
        dst_resolution = dst.res
        dst_nodata = dst.nodata if dst.nodata is not None else np.nan
        
        new_transform = from_bounds(src_bounds.left,
            src_bounds.bottom,
            src_bounds.right,
            src_bounds.top,
            src_width,
            src_height)

        logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Calculating the new "width" and "height"...')
        new_width = int((src_bounds.right - src_bounds.left) / dst_resolution[0])
        new_height = int((src_bounds.top - src_bounds.bottom) / dst_resolution[1])

        logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Updating metadata for the new layer...')
        out_meta = dst.meta.copy()
        out_meta.update({
            'driver': 'GTiff',
            'height': new_height,
            'width': new_width,
            'transform': new_transform,
            'nodata': dst_nodata,
            'crs': dst.crs
        })

        # Create an empty array for the result
        result = np.full((dst.count, new_height, new_width), dst_nodata, dtype=dst.dtypes[0])
        for i in range(1, dst.count + 1):
            dst_data = dst.read(i, window=dst.window(*src_bounds),
                boundless=True,
                out_shape=(new_height, new_width),
                resampling=rasterio.enums.Resampling.nearest)
            result[i - 1, :, :] = dst_data

    # Save
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> Saving...')
    output = io.buildOutputPath_pv1_steps_09_11_13(dst_file)
    with rasterio.open(output, 'w', **out_meta) as dst_adjusted:
        dst_adjusted.write(result)

    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step ' + step + ' -> [OK]')
    logging.info('')
    return output


# Function: PV Power Plants -> Preprocess -> Step 12 -> Change a raster resolution and reference system
def pv1_step_12(input_path, config):
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> Reading the metadata of the source layer...')
    dst_crs = CRS.from_epsg(3035)
    dst_resolution = float(config['IDESIGNRES-PARAMETERS']['idesignres.params.dst.resolution'])
    
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> Tansforming...')
    with rasterio.open(input_path) as src:
        transformer = Transformer.from_crs(src.crs, dst_crs, always_xy = True)

        left, bottom, right, top = transformer.transform_bounds(*src.bounds)
        left = math.floor(left / dst_resolution) * dst_resolution
        bottom = math.floor(bottom / dst_resolution) * dst_resolution
        right = math.ceil(right / dst_resolution) * dst_resolution
        top = math.ceil(top / dst_resolution) * dst_resolution

        width = int((right - left) / dst_resolution)
        height = int((top - bottom) / dst_resolution)
        transform = rasterio.Affine(dst_resolution, 0.0, left, 0.0, -dst_resolution, top)

        logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> Updating metadata for the new layer...')
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Save
        logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> Saving...')
        output = io.buildOutputPath_pv1_step_12(input_path)
        with rasterio.open(output, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source = rasterio.band(src, i),
                    destination = rasterio.band(dst, i),
                    src_transform = src.transform,
                    src_crs = src.crs,
                    dst_transform = transform,
                    dst_crs = dst_crs,
                    resampling = Resampling.bilinear
                )

        # Finish
        logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 12 -> [OK]')
        logging.info('')
        return output


# Function: PV Power Plants -> Preprocess -> Step 14 -> Calculate the multiplication of all the layers
def pv1_step_14(GHI_aligned_output, npa_aligned_output, landuse_aligned_path, slope_flt_path, config):
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 14 -> Calculating...')
    result_path = io.retrieveRadiationPotentialAreasPath(config)
    with rasterio.open(GHI_aligned_output) as src1, \
            rasterio.open(npa_aligned_output) as src2, \
            rasterio.open(landuse_aligned_path) as src3, \
            rasterio.open(slope_flt_path) as src4:
        ghi_threshold = src1.read(1)
        ghi_threshold[ghi_threshold == src1.nodata] = 0

        filtered_land_use = src2.read(1)
        filtered_land_use[filtered_land_use == src2.nodata] = 0

        slope_threshold = src3.read(1)
        slope_threshold[slope_threshold == src3.nodata] = 0

        non_protected_areas = src4.read(1)
        non_protected_areas[non_protected_areas == src4.nodata] = 0

    new_image = ghi_threshold * filtered_land_use * slope_threshold * non_protected_areas

    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 14 -> Updating metadata for the output raster...')
    meta = src1.meta
    meta.update(dtype=rasterio.float32, count=1)

    # Save
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 14 -> Saving...')
    with rasterio.open(result_path, 'w', **meta) as dst:
        dst.write(new_image.astype(rasterio.float32), 1)

    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 14 -> [OK]')
    logging.info('')
    return result_path



# Function: PV Power Plants -> Preprocess -> Step 15 -> Calculate regions
def pv1_step_15(radiationPotentialAreas, nuts_output_path, process, username, nutsid, config):
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Loading the files...')
    radiation_threshold_start = int(config['IDESIGNRES-PARAMETERS']['idesignres.params.radiation.threshold.start'])
    
    # Function: Convert to degrees
    def convertToDegrees(x, y):
        transformer = Transformer.from_crs('EPSG:3035', 'EPSG:4326', always_xy = True)
        lon, lat = transformer.transform(x, y)
        return lon, lat

    # Read raster file for the first time just to get maximum value and resolution
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Reading the raster file...')
    with rasterio.open(radiationPotentialAreas) as src:
        raster_data = src.read(1)
        res = src.res

    # Read the vectorial file with Geopandas
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Reading the vectorial file...')
    gdf = gpd.read_file(nuts_output_path)

    # Define radiation thresholds
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Defining the radiation threshold...')
    radiation_thresholds = range(radiation_threshold_start, int(np.max(raster_data)) + 100, 100)

    # Create a DataFrame to store results
    columns = ['Region', 'Centroid_X', 'Centroid_Y', 'Total_Area', 'Max_Radiation', 'Average_Radiation', 'Threshold',
               'Area_m2', 'Median_Radiation', 'Median_Radiation_X', 'Median_Radiation_Y']
    df = pd.DataFrame(columns=columns)

    # For each region
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Transforming...')
    for index, row in gdf.iterrows():
        geom = shape(row['geometry'])

        # Open raster file again
        with rasterio.open(radiationPotentialAreas) as src:
            # Clip the raster to the region
            clipped_image, out_transform = mask(src, [geom], crop=True)
            clipped_image = clipped_image[0]

            # Get the NoData value of the raster
            nodata = src.nodata

            # Exclude NoData values
            out_image = clipped_image[clipped_image != nodata]

            # Obtain the centroid of the region
            centroid = geom.centroid
            centroid_lon, centroid_lat = convertToDegrees(centroid.x, centroid.y)

            base_data = [row['NUTS_ID'], centroid_lon, centroid_lat, geom.area, out_image.max(), out_image.mean()]

            for i, threshold in enumerate(radiation_thresholds):
                next_threshold = radiation_thresholds[i + 1] if i + 1 < len(radiation_thresholds) else float('inf')

                # Start the data for this threshold level
                threshold_data = list(base_data)
                threshold_data.append(threshold)

                # Calculate area for this radiation range
                area_m2 = ((out_image >= threshold) & (out_image < next_threshold)).sum() * res[0] * res[1]
                threshold_data.append(area_m2)

                # Handle the radiant calculations if the area is not null
                threshold_image_2d = np.copy(clipped_image)
                threshold_image_2d[(threshold_image_2d < threshold) |
                                   (threshold_image_2d >= next_threshold) |
                                   (threshold_image_2d == nodata)] = np.nan

                threshold_mask_2d = ~np.isnan(threshold_image_2d)

                if area_m2 > 0:
                    threshold_image_1d = threshold_image_2d[threshold_mask_2d]

                    # Calculate the median radiation value for the current threshold
                    median_threshold = np.median(threshold_image_1d)
                    threshold_data.append(median_threshold)

                    # Construct an array where each pixel's value is the distance from the median
                    distances_to_median = np.abs(threshold_image_2d - median_threshold)
                    
                    # Set distances outside of the mask to an arbitrary large number for correct pixel selection later
                    distances_to_median[~threshold_mask_2d] = np.inf

                    # Get indices of the pixel with value closest to the median
                    closest_pixel_y_index, closest_pixel_x_index = np.unravel_index(
                        np.argmin(distances_to_median),
                        threshold_image_2d.shape)

                    # The coordinates of the pixel center
                    closest_pixel_x, closest_pixel_y = out_transform * (
                        closest_pixel_x_index + 0.5, closest_pixel_y_index + 0.5)
                    closest_pixel_lon, closest_pixel_lat = convertToDegrees(closest_pixel_x, closest_pixel_y)

                    threshold_data.extend([closest_pixel_lon, closest_pixel_lat])
                else:
                    threshold_data.extend([np.nan, np.nan, np.nan])

                # Append the results for this threshold to the DataFrame
                df.loc[len(df)] = threshold_data

    # Save the DataFrame as a CSV file
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Saving...')
    csv_name = io.retrieveOutputTmpPathConcatFile(True, process, username, nutsid, config)
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Temp. output file -> ' + csv_name)
    df.to_csv(csv_name, index = False, sep = ',')
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> Saved!!')
    
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Preprocess -> Step 15 -> [OK]')
    logging.info('')
    return csv_name

