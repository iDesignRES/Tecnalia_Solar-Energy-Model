# General imports
import configparser
import json
import logging
import math
import requests
import resource
import time
import zipfile
from datetime import timedelta

# Flask imports
from flask import Flask
from flask import request

# Flask JWT Extended imports
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

# JSON validation imports
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import schemas.json_schemas as json_schema

# Modules imports
import modules.database as db
import modules.io as io
import modules.qgis as qgis
import modules.qgis_pv_preprocess as qgis_pv1
import modules.qgis_pv_process as qgis_pv2
import modules.qgis_bp_preprocess as qgis_bp1
import modules.qgis_bp_process as qgis_bp2
import modules.rest as rest
import modules.sftp as sftp

import pandas as pd


# Init API
app = Flask(__name__)

# Create the config objects and read .ini and .properties files
config = configparser.ConfigParser()
config.read('/home/qgis/api/config/config.ini')
properties = configparser.ConfigParser()
properties.read('/home/qgis/api/properties/api.properties')

# Configure JWT
app.config['JWT_SECRET_KEY'] = '837cecf276fc4195a7c69d4436fc8552'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours = 96)
jwt = JWTManager(app)

# Init logging
logging.basicConfig(level = logging.INFO)

# Configure Pandas
pd.options.mode.chained_assignment = None


# Function: Set memory limit (in bytes)
def setMemoryLimit():
    # Limit memory to 16 GB
    limit = 16 * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))


@app.before_first_request
def before_first_request():
    setMemoryLimit()


# Function: Verify as online
@app.route('/api/qgis/hello', methods = ['GET'])
def hello():
    # Show info logs
    logging.info('')
    logging.info('****************************************************************************************')
    logging.info('****************************  IDESIGNRES :: Version ' + config['IDESIGNRES']['idesignres.version'])
    logging.info('****************************  FUNCTION   :: Hello!')
    logging.info('****************************************************************************************')
    
    # Show the QGIS Server version
    logging.info('')
    logging.info('  QGIS Server/> Running')
    logging.info('  QGIS Server/> Version : ' + qgis.getVersion())
    logging.info('')

    # Show the request response
    logging.info('  Response/>    [' + properties['IDESIGNRES-REST']['idesignres.rest.ok.code'] + ']')
    logging.info('')
    logging.info('****************************************************************************************')
    logging.info('')

    # Create and return the OK response
    return rest.buildResponse200(True, config, properties)


# Function: Authenticate
@app.route('/api/qgis/authenticate', methods = ['POST'])
def authenticate():
    # Show info logs
    logging.info('')
    logging.info('****************************************************************************************')
    logging.info('****************************  IDESIGNRES :: Version ' + config['IDESIGNRES']['idesignres.version'])
    logging.info('****************************  FUNCTION   :: Authenticate')
    logging.info('****************************************************************************************')
    
    body = request.get_json()
    try:
        # Validate if the input corresponds to the schema
        validate(instance = body, schema = json_schema.authenticate_schema)
        if not body['username'].strip() or not body['password'].strip():
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.json.empty.property'])

        # Show the request body
        logging.info('')
        logging.info('  QGIS Server/> Request body :')
        logging.info(json.dumps(body, indent = 4))
        logging.info('')
        
        # Call to UI-Backend to authenticate and create the token
        auth_response = requests.post(
            config['IDESIGNRES-UIBACKEND']['idesignres.uibackend.url.authenticate'].replace(
                '{1}', config['IDESIGNRES-UIBACKEND']['idesignres.uibackend.host']),
            data=json.dumps(
                {'username': str(body['username']).strip(),
                'password': str(body['password']).strip()}),
                headers={properties['IDESIGNRES-REST']['idesignres.rest.content.type.header']:
                    properties['IDESIGNRES-REST']['idesignres.rest.content.type.value']},
            verify=False)
        token = None
        if auth_response and auth_response.status_code == 200:
            token = create_access_token(identity = str(body['username']).strip())
        else:
            raise ConnectionRefusedError('')

        # Create the OK response
        response = rest.buildResponse200Value(token, properties)
    except ValueError as valueError:
        # Create a Bad Request response
        response = rest.buildResponse400(str(valueError), properties)
    except ValidationError as validationError:
        # Create a Bad Request response
        response = rest.buildResponse400(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.json.format'], properties)
    except ConnectionRefusedError as cre:
        # Create an Unauthorized response
        response = rest.buildResponse401(properties)
    except Exception as error:
        # Create a Bad Request response
        response = rest.buildResponse400(str(error), properties)

    # Return the response
    return response


# Function: Execute solar preprocess
def executeSolarPreprocess(process, nutsid, slope_angle, user):
    out_csv_file = None
    try:
        # Retrieve the layers from the database
        logging.info('')
        layerList = db.retrieveAllLayersByProcess(process, config)
        if layerList and len(layerList) > 0:
            # Load the layers from the SFTP Server
            logging.info('')
            logging.info('  QGIS Server/> Retrieving the layers from the SFTP Server (if needed)...')
            logging.info('')
            success = sftp.retrieveLayerFiles(layerList, config)
            logging.info('')
        
            # Process the layer
            if success:
                # Step 01 -> Process the base layer and retrieve the output file
                nuts_out, nuts_out_CRS = qgis_pv1.pv1_step_01(layerList[0], nutsid, config)
                    
                # Step 02 -> "slope" raster
                slo_clip_path = qgis_pv1.pv1_steps_02_03_04_05(layerList[1], nuts_out, '02', config)
                
                # Step 03 -> "GHI" raster
                ghi_clip_path = qgis_pv1.pv1_steps_02_03_04_05(layerList[2], nuts_out_CRS, '03', config)
                    
                # Step 04 -> "land use" raster
                lan_clip_path = qgis_pv1.pv1_steps_02_03_04_05(layerList[3], nuts_out, '04', config)
                     
                # Step 05 -> "non protected areas" raster
                npa_clip_path = qgis_pv1.pv1_steps_02_03_04_05(layerList[4], nuts_out, '05', config)
                    
                # Step 06 -> Filter the "slope" raster
                slo_flt_path = qgis_pv1.pv1_step_06(slo_clip_path, slope_angle, config)
                    
                # Step 07 -> Filter "land use" raster by codes
                lan_flt_path = qgis_pv1.pv1_step_07(lan_clip_path, config)
                    
                # Step 08 -> Change the resolution of the "land use" raster
                lan_res_path = qgis_pv1.pv1_steps_08_10(lan_flt_path, '08', config)
                    
                # Step 09 -> Adjust the "land use" raster to the size of the "slope" raster
                lan_align_path = qgis_pv1.pv1_steps_09_11_13(slo_flt_path, lan_res_path, '09', config)
                    
                # Step 10 -> Change the resolution of the "non protected areas" raster
                npa_res_path = qgis_pv1.pv1_steps_08_10(npa_clip_path, '10', config)
                    
                # Step 11 -> Adjust the "non protected areas" raster to the size of the "slope" raster
                npa_align_path = qgis_pv1.pv1_steps_09_11_13(slo_flt_path, npa_res_path, '11', config)
                    
                # Step 12 -> Change the resolution and the reference system of the "GHI" raster
                ghi_repres_path = qgis_pv1.pv1_step_12(ghi_clip_path, config)
                  
                # Step 13 -> Adjust the "GHI" raster to the size of the "slope" raster
                ghi_align_path = qgis_pv1.pv1_steps_09_11_13(slo_flt_path, ghi_repres_path, '13', config)
                   
                # Step 14 -> Calculate the multiplication of all the layers
                rd_areas = qgis_pv1.pv1_step_14(ghi_align_path, npa_align_path, lan_align_path, slo_flt_path, config)
                    
                # Step 15 -> Calculate regions
                out_csv_file = qgis_pv1.pv1_step_15(rd_areas, nuts_out, process, user, nutsid, config)
                
                # Upload the output file to the SFTP Server
                if out_csv_file:
                    logging.info('  QGIS Server/> Uploading the result file...')
                    logging.info('')
                    rem_output = io.retrieveOutputTmpPath(False, config) + out_csv_file[out_csv_file.rfind('/') + 1:]
                    rem_output = rem_output.replace('{1}', user)
                    sftp.uploadOutputFile(out_csv_file, rem_output, config)
                
        result = out_csv_file
    except ValueError as valueError:
        result = None
    except ValidationError as validationError:
        result = None
    except Exception as error:
        result = None
    finally:
        # Remove all the temporary layer files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.layers.tmp']) != 1:
            logging.info('  QGIS Server/> Removing al the temporary layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersTmpPath(config))
        
        # Remove all the temporary files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.files.tmp']) != 1:
            logging.info('  QGIS Server/> Removing al the temporary files...')
            io.removeFilesFromDirectory(io.retrieveFilesTmpPath(config))

    # Return the result
    logging.info('')
    return result


# Function: Execute building preprocess
def executeBuildingPreprocess(process, nutsid, user):
    out_csv_file = None
    try:
        # Retrieve the layers from the database
        logging.info('')
        layerList = db.retrieveAllLayersByProcess(process, config)
        if layerList and len(layerList) > 0:
            # Load the layers from the SFTP Server
            logging.info('')
            logging.info('  QGIS Server/> Retrieving the layers from the SFTP Server (if needed)...')
            logging.info('')
            
            success = sftp.retrieveLayerFiles(layerList, config)
            if success:
                # Retrieve the files from the database
                logging.info('')
                fileList = db.retrieveAllFilesByProcess(process, config)
                if fileList and len(fileList) > 0:
                    # Load the files from the SFTP Server
                    logging.info('')
                    logging.info('  QGIS Server/> Retrieving the files from the SFTP Server (if needed)...')
                    logging.info('')
                    success = sftp.retrieveDataFiles(fileList, config)
                    if success:
                        # Retrieve the resources from the database
                        logging.info('')
                        resourceList = db.retrieveAllResources(process, config)
                        logging.info('')

                        # Step 01 -> Download and unzip
                        destination_dir = qgis_bp1.bp1_step_01(nutsid, fileList, resourceList, config, properties)
                            
                        # Step 02 -> Export the selected NUTS
                        nuts_flt_crs, out_nuts_54009 = qgis_bp1.bp1_step_02(layerList[0], nutsid, config, properties)
                            
                        # Step 03 -> Clip and save the vector layers
                        clipped_layers = qgis_bp1.bp1_step_03(destination_dir, nuts_flt_crs)
                            
                        # Step 04 -> Load the buildings layer
                        buildings_layer = qgis_bp1.bp1_step_04(clipped_layers, True, config)
                            
                        # Step 05 -> Load the NUTS layer
                        nuts_layer = qgis_bp1.bp1_step_05(out_nuts_54009)
                            
                        # Step 06 -> Load the land use layer
                        land_use_layer = qgis_bp1.bp1_step_06(clipped_layers)
                            
                        # Step 07 -> Load the Raster Use layer
                        raster_use_layer = qgis_bp1.bp1_step_07(layerList[2], config)
                            
                        # Step 08 -> Load the Raster Height layer
                        raster_height_layer = qgis_bp1.bp1_step_08(layerList[6], config)
                            
                        ##### Start the building preprocessing #####
                          
                        # Step 09 -> Assign NUTS
                        qgis_bp1.bp1_step_09(buildings_layer, nuts_layer, nutsid)
                            
                        # Step 10 -> Calculate height volumes
                        qgis_bp1.bp1_step_10(buildings_layer, raster_height_layer)
                            
                        # Step 11 -> Calculate statistics and mapping
                        qgis_bp1.bp1_step_11(buildings_layer, raster_use_layer, land_use_layer, fileList[1], config)
                        
                        # Step 12 -> Adjoin facade calculations
                        buildings = qgis_bp1.bp1_step_12(True, config)
                            
                        # Step 13 -> Mask raster layers
                        clipped_rasters = qgis_bp1.bp1_step_13(layerList, config)
                            
                        # Step 14 -> Process clipped layers
                        layers_dict = qgis_bp1.bp1_step_14(nutsid, clipped_rasters, fileList[2], destination_dir, config)
                        
                        # Step 15 -> Assign year info
                        buildings = qgis_bp1.bp1_step_15(nutsid, buildings, layers_dict, fileList[2], config)
                        
                        # Step 16 -> Calculate additional info
                        buildings = qgis_bp1.bp1_step_16(buildings)
                        
                        # Step 17 -> Prepare clustering ([n_clusters_AB , n_clusters_SFH, n_clusters_SS])
                        clusters = [4, 3, 1]
                        AB_df, SFH_df, SS_df = qgis_bp1.bp1_step_17(buildings)
                        
                        # Step 18 -> Perform clustering (AB)
                        df_clusters_AB = qgis_bp1.bp1_step_18(AB_df, clusters[0])
                        
                        # Step 19 -> Perform clustering (SFH)
                        df_clusters_SFH = qgis_bp1.bp1_step_19(SFH_df, clusters[1])
                        
                        # Step 20 -> Perform clustering (SS)
                        df_clusters_SS = qgis_bp1.bp1_step_20(SS_df, clusters[2])
                        
                        # Step 21 -> Create the final Dataframe
                        final_df, out_csv_file = qgis_bp1.bp1_step_21(df_clusters_AB, df_clusters_SFH, df_clusters_SS, process, user, nutsid)
                        
                        # Upload the output file to the SFTP Server
                        if out_csv_file:
                            logging.info('  QGIS Server/> Uploading the result file...')
                            logging.info('')
                            rem_output = io.retrieveOutputTmpPath(False, config) + out_csv_file[out_csv_file.rfind('/') + 1:]
                            rem_output = rem_output.replace('{1}', user)
                            sftp.uploadOutputFile(out_csv_file, rem_output, config)

        result = output_csv_file
    except ValueError as valueError:
        raise
    except ValidationError as validationError:
        raise
    except Exception as error:
        raise
    finally:
        # Remove all the temporary layer files
        if int(config['IDESIGNRES']['idesignres.persistence.layers.tmp']) != 1:
            logging.info('  QGIS Server/> Removing al the temporary layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersTmpPath(config))
        
        # Remove all the layer files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.layers']) != 1:
            logging.info('  QGIS Server/> Removing al the layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersBasePath(config))

    # Return the result
    logging.info('')
    return result


# Function: Execute PV Power Plants process
@app.route('/api/qgis/pv-power-plants-process', methods = ['POST'])
@jwt_required()
def executePVPowerPlantsProcess():
    # Show info logs
    logging.info('')
    logging.info('****************************************************************************************')
    logging.info('****************************  IDESIGNRES :: Version ' + config['IDESIGNRES']['idesignres.version'])
    logging.info('****************************  FUNCTION   :: PV Power Plants process')
    logging.info('****************************************************************************************')

    # Extract the current user from the JWT token
    user = get_jwt_identity()
    
    # Extract the body from the request
    body = request.get_json()

    try:
        # Validate if the input corresponds to the schema
        validate(instance = body, schema = json_schema.pv_power_plants_process_schema)
        if not body['nutsid'].strip() or not body['slope_angle'] or not user.strip():
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.json.empty.property'])
        
        # Perform other validations (Valid NUTSID)
        nutsids = [nutsid.strip() for nutsid in config['IDESIGNRES-PARAMETERS']['idesignres.params.nutsids'].split(',')]
        if body['nutsid'].strip().upper() not in nutsids:
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.nutsid.not.valid'])

        # Show the request body
        logging.info('')
        logging.info('  QGIS Server/> Request body :')
        logging.info(json.dumps(body, indent = 4))
        logging.info('')
        
        # Check if the user has his/her own output directory
        if not sftp.checkUserDirectory(user, config):
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.output'])
        logging.info('')
        
        # Retrieve the processess from the database
        processList = db.retrieveAllProcesses(config)
        if processList and len(processList) > 0 and processList[0]:
            # Check if the result already exists
            if int(config['IDESIGNRES']['idesignres.check.previous.results']) == 1:
                rem_file = config['IDESIGNRES-PATH']['idesignres.path.output.zip.name'].replace('{1}',
                    processList[0]['uuid']).replace('{2}', body['nutsid'].strip())
                file_exists = sftp.fileExists(config['IDESIGNRES-PATH']['idesignres.path.output'] + user + '/' + rem_file, config)
                if file_exists:
                    logging.info('')
                    logging.info('  SFTP Server/> ' + properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.result.exists'])
                    logging.info('')
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.result.exists'])
        
            # Init QGIS
            logging.info('')
            qgisApp = qgis.init()

            # Create QGIS project
            logging.info('')
            logging.info('  QGIS Server/> Creating project...')
            qgis.createProject(io.retrieveProjectsBasePathConcatProjectName(config),
                io.retrieveDefaultProjectName(config),
                properties)

            # Execute the preprocess
            result = None
            if int(config['IDESIGNRES']['idesignres.preprocess.pv']) == 1:
                result = executeSolarPreprocess(processList[0]['uuid'], body['nutsid'].strip(), body['slope_angle'], user.strip())
                if not result or not io.fileExists(result):
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.no.input.data.preprocess'])
            
            # Step 01 -> Load the specific configuration
            list_parameters_th, list_parameters_pv, system_cost, land_use_th, land_use_pv, min_ghi_th, min_ghi_pv,\
            eff_th, eff_op, aperture, t_coord, year, tilt, azimuth, tracking, loss, opex_th, opex_pv =\
                qgis_pv2.pv2_step_01(config)
            
            # Step 02 -> Download the result of the Solar preprocess and load the data
            scada_th, scada_pv = qgis_pv2.pv2_step_02(user, body['nutsid'].strip(), processList[0]['uuid'], config)
            if scada_th is None or scada_th.empty or scada_pv is None or scada_pv.empty:
                raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.no.input.data.preprocess'])
                
            # Step 03 -> Calculate the available thermal area
            area_th, power_th, capex_th = qgis_pv2.pv2_step_03(list_parameters_th, system_cost, land_use_th)
                
            # Step 04 -> Calculate the available PV area
            area_pv, power_pv, capex_pv = qgis_pv2.pv2_step_04(list_parameters_pv, system_cost, land_use_pv)
                
            # Step 05 -> Thermal production
            nuts2_th, rows_th, pot_dist_th, df_th = qgis_pv2.pv2_step_05(scada_th, area_th, min_ghi_th,
                land_use_th, eff_th, eff_op, aperture, t_coord, year)
                
            # Step 06 -> PV production
            name_nuts2, nuts2_pv, pot_dist_pv, df_pv = qgis_pv2.pv2_step_06(rows_th, scada_pv,
                area_pv, min_ghi_pv, land_use_pv, tilt, azimuth, tracking, loss, t_coord, year)
              
            # Step 07 -> Calculate the aggregated production
            prod_aggregated = qgis_pv2.pv2_step_07(df_th, df_pv, name_nuts2)
                
            # Step 08 -> Calculate the distribution production
            nuts2_distrib = qgis_pv2.pv2_step_08(nuts2_th, nuts2_pv)
            
            # Step 09 -> Save the results
            outputs = qgis_pv2.pv2_step_09(prod_aggregated, nuts2_distrib, name_nuts2, pot_dist_th,
                pot_dist_pv, opex_th, opex_pv, config)
                        
            # Compress and upload the output files to the SFTP Server
            if outputs and len(outputs) > 0:
                logging.info('  QGIS Server/> Compressing the result files...')
                logging.info('')
                fil = io.retrieveOutputBasePath(True, config) + processList[0]['uuid'] + '_' + body['nutsid'].strip() + '.zip' 
                with zipfile.ZipFile(fil, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for loc_output in outputs:
                        zipf.write(loc_output, loc_output[loc_output.rfind('/') + 1:])
            rem_output = io.retrieveOutputBasePath(False, config) + fil[fil.rfind('/') + 1:]
            rem_output = rem_output.replace('{1}', user)
            sftp.uploadOutputFile(fil, rem_output, config)

        # Create the OK response
        response = rest.buildResponse200Value(properties['IDESIGNRES-REST']['idesignres.rest.result.download'], properties)
    except ValueError as valueError:
        # Create a Bad Request response
        response = rest.buildResponse400(str(valueError), properties)
    except ValidationError as validationError:
        # Create a Bad Request response
        response = rest.buildResponse400(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.json.format'], properties)
    except Exception as error:
        # Create a Bad Request response
        response = rest.buildResponse400(str(error), properties)
    finally:
        # Remove all the output files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.output']) != 1:
            logging.info('  QGIS Server/> Removing al the local output files...')
            io.removeFilesFromDirectory(io.retrieveOutputBasePath(True, config))
        
        # Remove the project file
        logging.info('  QGIS Server/> Removing the project...')
        qgis.removeProject(io.retrieveProjectsBasePathConcatProjectName(config))

    # Return the response
    logging.info('')
    return response
    

# Function: Execute building energy simulation process
@app.route('/api/qgis/building-energy-simulation-process', methods = ['POST'])
@jwt_required()
def executeBuildingEnergySimulationProcess():
    # Show info logs
    logging.info('')
    logging.info('****************************************************************************************')
    logging.info('****************************  IDESIGNRES :: Version ' + config['IDESIGNRES']['idesignres.version'])
    logging.info('****************************  FUNCTION   :: Building energy simulation process')
    logging.info('****************************************************************************************')

    # Extract the current user from the JWT token
    user = get_jwt_identity()
    
    # Extract the body from the request
    body = request.get_json()

    try:
        # Validate if the input corresponds to the schema
        validate(instance = body, schema = json_schema.building_energy_simulation_process_schema)
        if not body['nutsid'].strip() or not user.strip():
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.json.empty.property'])
        
        # Perform other validations (Valid NUTSID)
        nutsids = [nutsid.strip() for nutsid in config['IDESIGNRES-PARAMETERS']['idesignres.params.nutsids'].split(',')]
        if body['nutsid'].strip().upper() not in nutsids:
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.nutsid.not.valid'])
        
        # Perform other validations (Active measures)
        archetypes = [arch.strip() for arch in config['IDESIGNRES-PARAMETERS']['idesignres.params.archetypes'].split(',')]
        for measure in body['scenario']['active_measures']:
            if measure['building_use'].strip() not in archetypes:
                raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.archetypes'])
            if bool(measure['user_defined_data']):
                # Space heating
                if (math.floor((float(measure['space_heating']['solids']) +\
                    float(measure['space_heating']['lpg'])  +\
                    float(measure['space_heating']['diesel_oil']) +\
                    float(measure['space_heating']['gas_heat_pumps']) +\
                    float(measure['space_heating']['natural_gas']) +\
                    float(measure['space_heating']['biomass']) +\
                    float(measure['space_heating']['geothermal']) +\
                    float(measure['space_heating']['distributed_heat']) +\
                    float(measure['space_heating']['advanced_electric_heating']) +\
                    float(measure['space_heating']['conventional_electric_heating']) +\
                    float(measure['space_heating']['bio_oil']) +\
                    float(measure['space_heating']['bio_gas']) +\
                    float(measure['space_heating']['hydrogen'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Space heating'))
                # Space cooling  
                if (math.floor((float(measure['space_cooling']['gas_heat_pumps']) +\
                    float(measure['space_cooling']['electric_space_cooling'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Space cooling'))
                # Water heating
                if (math.floor((float(measure['water_heating']['solids']) +\
                    float(measure['water_heating']['lpg']) +\
                    float(measure['water_heating']['diesel_oil']) +\
                    float(measure['water_heating']['natural_gas']) +\
                    float(measure['water_heating']['biomass']) +\
                    float(measure['water_heating']['geothermal']) +\
                    float(measure['water_heating']['distributed_heat']) +\
                    float(measure['water_heating']['advanced_electric_heating']) +\
                    float(measure['water_heating']['bio_oil']) +\
                    float(measure['water_heating']['bio_gas']) +\
                    float(measure['water_heating']['hydrogen']) +\
                    float(measure['water_heating']['solar']) +\
                    float(measure['water_heating']['electricity'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Water heating'))
                # Cooking
                if (math.floor((float(measure['cooking']['solids']) +\
                    float(measure['cooking']['lpg']) +\
                    float(measure['cooking']['natural_gas']) +\
                    float(measure['cooking']['biomass']) +\
                    float(measure['cooking']['electricity'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Cooking'))
                # Lighting
                if (math.floor((float(measure['lighting']['electricity'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Lighting'))
                #Appliances
                if (math.floor((float(measure['appliances']['electricity'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Appliances'))
            
        # Perform other validations (Active measures baseline)
        for measure in body['scenario']['active_measures_baseline']:
            if measure['building_use'].strip() not in archetypes:
                raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.baseline.archetypes'])
            if bool(measure['user_defined_data']):
                # Space heating
                if (math.floor((float(measure['space_heating']['solids']) +\
                    float(measure['space_heating']['lpg'])  +\
                    float(measure['space_heating']['diesel_oil']) +\
                    float(measure['space_heating']['gas_heat_pumps']) +\
                    float(measure['space_heating']['natural_gas']) +\
                    float(measure['space_heating']['biomass']) +\
                    float(measure['space_heating']['geothermal']) +\
                    float(measure['space_heating']['distributed_heat']) +\
                    float(measure['space_heating']['advanced_electric_heating']) +\
                    float(measure['space_heating']['conventional_electric_heating']) +\
                    float(measure['space_heating']['bio_oil']) +\
                    float(measure['space_heating']['bio_gas']) +\
                    float(measure['space_heating']['hydrogen'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.baseline.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Space heating'))
                # Space cooling  
                if (math.floor((float(measure['space_cooling']['gas_heat_pumps']) +\
                    float(measure['space_cooling']['electric_space_cooling'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.baseline.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Space cooling'))
                # Water heating
                if (math.floor((float(measure['water_heating']['solids']) +\
                    float(measure['water_heating']['lpg']) +\
                    float(measure['water_heating']['diesel_oil']) +\
                    float(measure['water_heating']['natural_gas']) +\
                    float(measure['water_heating']['biomass']) +\
                    float(measure['water_heating']['geothermal']) +\
                    float(measure['water_heating']['distributed_heat']) +\
                    float(measure['water_heating']['advanced_electric_heating']) +\
                    float(measure['water_heating']['bio_oil']) +\
                    float(measure['water_heating']['bio_gas']) +\
                    float(measure['water_heating']['hydrogen']) +\
                    float(measure['water_heating']['solar']) +\
                    float(measure['water_heating']['electricity'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.baseline.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Water heating'))
                # Cooking
                if (math.floor((float(measure['cooking']['solids']) +\
                    float(measure['cooking']['lpg']) +\
                    float(measure['cooking']['natural_gas']) +\
                    float(measure['cooking']['biomass']) +\
                    float(measure['cooking']['electricity'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.baseline.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Cooking'))
                # Lighting
                if (math.floor((float(measure['lighting']['electricity'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.baseline.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Lighting'))
                #Appliances
                if (math.floor((float(measure['appliances']['electricity'])) * 10000) / 10000) != 1:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.active.measures.baseline.not.100']\
                        .replace('{1}', measure['building_use']).replace('{2}', 'Appliances'))
                        
        # Perform other validations (Passive measures)
        ref_levels = [lvl.strip() for lvl in config['IDESIGNRES-PARAMETERS']['idesignres.params.ref.levels'].split(',')]
        for measure in body['scenario']['passive_measures']:
            if measure['building_use'].strip() not in archetypes:
                raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.passive.measures.archetypes'])
            if measure['ref_level'].strip().lower() not in ref_levels:
                raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.passive.measures.ref.level'])

        # Check if the user has his/her own output directory
        if not sftp.checkUserDirectory(user, config):
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.output'])
        logging.info('')
        
        # Adapt the input data
        for i in range(len(body['scenario']['active_measures'])):
            body['scenario']['active_measures'][i]['building_use'] =\
                body['scenario']['active_measures'][i]['building_use'].strip()
        for i in range(len(body['scenario']['active_measures_baseline'])):
            body['scenario']['active_measures'][i]['building_use'] =\
                body['scenario']['active_measures'][i]['building_use'].strip()
        for i in range(len(body['scenario']['passive_measures'])):
            body['scenario']['passive_measures'][i]['building_use'] =\
                body['scenario']['passive_measures'][i]['building_use'].strip()
            body['scenario']['passive_measures'][i]['ref_level'] =\
                body['scenario']['passive_measures'][i]['ref_level'].strip().capitalize()

        # Retrieve the processess from the database
        processList = db.retrieveAllProcesses(config)
        if processList and len(processList) > 0 and processList[1]:
            # Check if the result already exists
            if int(config['IDESIGNRES']['idesignres.check.previous.results']) == 1:
                rem_file = config['IDESIGNRES-PATH']['idesignres.path.output.zip.name'].replace('{1}',
                    processList[1]['uuid']).replace('{2}', body['nutsid'].strip())
                file_exists = sftp.fileExists(config['IDESIGNRES-PATH']['idesignres.path.output'] + user + '/' + rem_file, config)
                if file_exists:
                    logging.info('')
                    logging.info('  SFTP Server/> ' + properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.result.exists'])
                    logging.info('')
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.result.exists'])
        
            # Retrieve the dbase files from the SFTP Server
            logging.info('')
            logging.info('  QGIS Server/> Retrieving the dbase files from the SFTP Server...')
            logging.info('')
            dbaseFileList = sftp.retrieveDbaseFiles(config)
            logging.info('')
            if dbaseFileList and len(dbaseFileList) > 0:
                # Init QGIS
                qgisApp = qgis.init()

                # Create QGIS project
                logging.info('')
                logging.info('  QGIS Server/> Creating project...')
                logging.info('')
                qgis.createProject(io.retrieveProjectsBasePathConcatProjectName(config),
                    io.retrieveDefaultProjectName(config),
                    properties)
                
                # Execute the preprocess
                result = None
                if int(config['IDESIGNRES']['idesignres.preprocess.bp']) == 1:
                    result = executeBuildingPreprocess(processList[1]['uuid'], body['nutsid'].strip(), user.strip())
                    if not result or not io.fileExists(result):
                        raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.no.input.data.preprocess'])

                # Step 01 -> Download the result of the Buildings preprocess
                df_csv = qgis_bp2.bp2_step_01(user, body['nutsid'].strip(), processList[1]['uuid'], config)
                if df_csv is None or df_csv.empty:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.no.input.data.preprocess'])

                # Step 02 -> Retrieve temperatures
                temps_path = qgis_bp2.bp2_step_02(body['nutsid'].strip(), body['year'], dbaseFileList[6], config, properties)
                        
                # Step 03 -> Retrieve radiation values
                rad_path = qgis_bp2.bp2_step_03(body['nutsid'].strip(), body['year'], dbaseFileList[5], config, properties)
                if not temps_path or not rad_path:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.no.rad.temp'])
               
                # Step 04 -> Load the database
                df_dhw, df_years, df_sectors, df_seasons, df_temperatures, df_schedule, df_res_hh_tes, df_ser_hh_tes,\
                df_uvalues, df_retro_uvalues, df_ach, df_base_temperatures, df_calendar, df_bes_capex, df_bes_opex,\
                df_res, df_bes_capacity, df_retro_cost, df_solar_office, df_solar_noffice, df_dwellings, df_r_t_hh_eff =\
                    qgis_bp2.bp2_step_04(dbaseFileList, body)
                            
                # Step 05 -> Add new columns to the input dataframe
                df_input = qgis_bp2.bp2_step_05(df_csv)
                            
                # Step 06 -> Add the input data
                df_input = qgis_bp2.bp2_step_06(df_csv, df_dhw, df_years, df_sectors, df_dwellings, body, properties)
                del df_years, df_sectors, df_dwellings
                            
                # Step 07 -> Add the active measures
                df_input = qgis_bp2.bp2_step_07(df_csv, df_res_hh_tes, df_ser_hh_tes, df_r_t_hh_eff, config, body)
                del df_res_hh_tes, df_ser_hh_tes, df_r_t_hh_eff
                            
                # Step 08 -> Add the passive measures
                df_input = qgis_bp2.bp2_step_08(df_csv, body)
                            
                # Step 09 -> Add the U-Values and the Internal Gains dataframes
                df_input = qgis_bp2.bp2_step_09(df_csv, df_dhw, df_uvalues, df_retro_uvalues, df_ach, body)
                del df_dhw, df_uvalues, df_retro_uvalues, df_ach
                            
                # Step 10 -> Add the CAPEX dataframe
                df_input = qgis_bp2.bp2_step_10(df_input, df_bes_capex)
                del df_bes_capex
                            
                # Step 11 -> Add the OPEX dataframe
                df_input = qgis_bp2.bp2_step_11(df_input, df_bes_opex)
                del df_bes_opex
                            
                # Step 12 -> Add the Retroffiting Cost dataframe
                df_input = qgis_bp2.bp2_step_12(df_input, df_retro_cost)
                del df_retro_cost
                            
                # Step 13 -> Add the Renewable Energy Systems dataframe
                df_input = qgis_bp2.bp2_step_13(df_input, df_res)
                del df_res
                            
                # Step 14 -> Add the Capacity dataframe
                df_input = qgis_bp2.bp2_step_14(df_input, df_bes_capacity, config)
                del df_bes_capacity
                            
                # Step 15 -> Add the Equivalent Power dataframe
                df_input = qgis_bp2.bp2_step_15(df_input)
                            
                # Step 16 -> Calculate the costs
                df_input = qgis_bp2.bp2_step_16(df_input)
                        
                # Step 17 -> Calculate the General Schedule
                dict_schedule = qgis_bp2.bp2_step_17(df_input, df_schedule, df_temperatures, df_base_temperatures,
                    df_solar_office, df_solar_noffice, body)
                del df_temperatures, df_base_temperatures, df_solar_office, df_solar_noffice
                            
                # Step 18 -> Calculate the Scenario
                dict_schedule = qgis_bp2.bp2_step_18(df_input, dict_schedule, config, body)
                            
                # Step 19 -> Calculate the Anual Results
                df_anual_res = qgis_bp2.bp2_step_19(df_input, dict_schedule)
                            
                # Step 20 -> Calculate the Consolidate
                dictConsolidated = {}
                for arch in archetypes:
                    dictConsolidated[arch] = qgis_bp2.bp2_step_20(df_input, dict_schedule, arch)
                            
                # Step 21 -> Calculate the Hourly Results
                dictHourlyResults = {}
                for arch in archetypes:
                    dictHourlyResults[arch] = qgis_bp2.bp2_step_21(df_input, dict_schedule, arch)
                del dict_schedule
                           
                # Step 22 -> Save the final result
                output = qgis_bp2.bp2_step_22(df_input, df_anual_res, dictConsolidated, dictHourlyResults, config)
                del df_input, df_anual_res, dictConsolidated, dictHourlyResults
                            
                # Compress and upload the output file to the SFTP Server
                if output:
                    logging.info('  QGIS Server/> Compressing the result file...')
                    logging.info('')
                    fil = io.retrieveOutputBasePath(True, config) + processList[1]['uuid'] + '_' + body['nutsid'].strip() + '.zip' 
                    with zipfile.ZipFile(fil, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write(output, output[output.rfind('/') + 1:])
                    rem_output = io.retrieveOutputBasePath(False, config) + fil[fil.rfind('/') + 1:]
                    rem_output = rem_output.replace('{1}', user)
                    sftp.uploadOutputFile(fil, rem_output, config)

        # Create the OK response
        response = rest.buildResponse200Value(properties['IDESIGNRES-REST']['idesignres.rest.result.download'], properties)
    except ValueError as valueError:
        # Create a Bad Request response
        response = rest.buildResponse400(str(valueError), properties)
    except ValidationError as validationError:
        # Create a Bad Request response
        response = rest.buildResponse400(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.json.format'], properties)
    except Exception as error:
        # Create a Bad Request response
        response = rest.buildResponse400(str(error), properties)
    finally:
        # Remove all the temporary files
        if int(config['IDESIGNRES']['idesignres.persistence.layers.tmp']) != 1:
            logging.info('  QGIS Server/> Removing al the temporary layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersTmpPath(config))
        
        # Remove all the layer files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.layers']) != 1:
            logging.info('  QGIS Server/> Removing al the layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersBasePath(config))
        
        # Remove all the temporary files
        if int(config['IDESIGNRES']['idesignres.persistence.files.tmp']) != 1:
            logging.info('  QGIS Server/> Removing al the temporary files...')
            io.removeFilesFromDirectory(io.retrieveFilesTmpPath(config))
        
        # Remove all the output files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.output']) != 1:
            logging.info('  QGIS Server/> Removing al the local output files...')
            io.removeFilesFromDirectory(io.retrieveOutputBasePath(True, config))
        
        # Remove the project file
        logging.info('  QGIS Server/> Removing the project...')
        qgis.removeProject(io.retrieveProjectsBasePathConcatProjectName(config))

    # Return the response
    logging.info('')
    return response



# Run app
if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 5010)
