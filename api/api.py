# General imports
import configparser
import json
import logging
import math
import requests
import resource
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
import schemas.json_schemas as jsonSchema

# Modules imports
import modules.database as db
import modules.io as io
import modules.qgis as qgis
import modules.qgis_pv_preprocess as qgisPV1
import modules.qgis_pv_process as qgisPV2
import modules.qgis_bp_preprocess as qgisBP1
import modules.qgis_bp_process as qgisBP2
import modules.rest as rest
import modules.sftp as sftp
from modules.logging_config import logger

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

# Configure Pandas
pd.options.mode.chained_assignment = None


# Function: Set memory limit (in bytes)
def setMemoryLimit(limitConfig):
    ''' Function to limit the memory. '''
    
    limit = limitConfig * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))


@app.before_first_request
def before_first_request():
    ''' Function to set the memory limit before the first request. '''
    
    setMemoryLimit(int(config['IDESIGNRES']['idesignres.memory.limit.gb']))


# Function: Verify as online
@app.route('/api/qgis/hello', methods = ['GET'])
def hello():
    ''' API function to check if the API is online. '''
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************************************')
    logger.info('****************************  IDESIGNRES :: Version ' + config['IDESIGNRES']['idesignres.version'])
    logger.info('****************************  FUNCTION   :: Hello!')
    logger.info('****************************************************************************************')
    
    # Show the QGIS Server version
    logger.info('')
    logger.info('  QGIS Server/> Running')
    logger.info('  QGIS Server/> Version : ' + qgis.getVersion())
    logger.info('')

    # Show the request response
    logger.info('  Response/>    [' + properties['IDESIGNRES-REST']['idesignres.rest.ok.code'] + ']')
    logger.info('')
    logger.info('****************************************************************************************')
    logger.info('')

    # Create and return the OK response
    return rest.buildResponse200(True, config, properties)


# Function: Authenticate
@app.route('/api/qgis/authenticate', methods = ['POST'])
def authenticate():
    ''' Function to check if a user is authenticated. '''
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************************************')
    logger.info('****************************  IDESIGNRES :: Version ' + config['IDESIGNRES']['idesignres.version'])
    logger.info('****************************  FUNCTION   :: Authenticate')
    logger.info('****************************************************************************************')
    
    body = request.get_json()
    try:
        # Validate if the input corresponds to the schema
        validate(instance = body, schema = jsonSchema.authenticateSchema)
        if not body['username'].strip() or not body['password'].strip():
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.json.empty.property'])

        # Call to UI-Backend to authenticate and create the token
        authResponse = requests.post(
            config['IDESIGNRES-UIBACKEND']['idesignres.uibackend.url.authenticate'].replace(
                '{1}', config['IDESIGNRES-UIBACKEND']['idesignres.uibackend.host']),
                data = json.dumps(
                    {'username': str(body['username']).strip(),
                    'password': str(body['password']).strip()}),
                headers = {properties['IDESIGNRES-REST']['idesignres.rest.content.type.header']:
                    properties['IDESIGNRES-REST']['idesignres.rest.content.type.value']},
                verify = False)
        token = None
        if authResponse and authResponse.status_code == 200:
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
        response = rest.buildResponse400(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.json.format'],
            properties)
    except ConnectionRefusedError as cre:
        # Create an Unauthorized response
        response = rest.buildResponse401(properties)
    except Exception as error:
        # Create a Bad Request response
        response = rest.buildResponse400(str(error), properties)

    # Return the response
    return response


# Function: Execute solar preprocess
def executeSolarPreprocess(process, nutsid, slopeAngle, user):
    ''' API function to execute the solar preprocess. '''
    
    outCsvFile = None
    try:
        # Retrieve the layers from the database
        logger.info('')
        layerList = db.retrieveAllLayersByProcess(process, config)
        if layerList and len(layerList) > 0:
            # Load the layers from the SFTP Server
            logger.info('')
            logger.info('  QGIS Server/> Retrieving the layers from the SFTP Server (if needed)...')
            logger.info('')
            success = sftp.retrieveLayerFiles(layerList, config)
            logger.info('')
        
            # Process the layer
            if success:
                # Step 01 -> Process the base layer and retrieve the output file
                nutsOut, nutsOutCrs = qgisPV1.pv1Step01(layerList[0], nutsid, config)
                    
                # Step 02 -> "slope" raster
                slopeClipPath = qgisPV1.pv1Steps02030405(layerList[1], nutsOut, '02', config)
                
                # Step 03 -> "GHI" raster
                ghiClipPath = qgisPV1.pv1Steps02030405(layerList[2], nutsOutCrs, '03', config)
                    
                # Step 04 -> "land use" raster
                lanClipPath = qgisPV1.pv1Steps02030405(layerList[3], nutsOut, '04', config)
                     
                # Step 05 -> "non protected areas" raster
                npaClipPath = qgisPV1.pv1Steps02030405(layerList[4], nutsOut, '05', config)
                    
                # Step 06 -> Filter the "slope" raster
                slopeFltPath = qgisPV1.pv1Step06(slopeClipPath, slopeAngle, config)
                    
                # Step 07 -> Filter "land use" raster by codes
                lanFltPath = qgisPV1.pv1Step07(lanClipPath, config)
                    
                # Step 08 -> Change the resolution of the "land use" raster
                lanResPath = qgisPV1.pv1Steps0810(lanFltPath, '08', config)
                    
                # Step 09 -> Adjust the "land use" raster to the size of the "slope" raster
                lanAlignPath = qgisPV1.pv1Steps091113(slopeFltPath, lanResPath, '09', config)
                    
                # Step 10 -> Change the resolution of the "non protected areas" raster
                npaResPath = qgisPV1.pv1Steps0810(npaClipPath, '10', config)
                    
                # Step 11 -> Adjust the "non protected areas" raster to the size of the "slope" raster
                npaAlignPath = qgisPV1.pv1Steps091113(slopeFltPath, npaResPath, '11', config)
                    
                # Step 12 -> Change the resolution and the reference system of the "GHI" raster
                ghiRepresPath = qgisPV1.pv1Step12(ghiClipPath, config)
                  
                # Step 13 -> Adjust the "GHI" raster to the size of the "slope" raster
                ghiAlignPath = qgisPV1.pv1Steps091113(slopeFltPath, ghiRepresPath, '13', config)
                   
                # Step 14 -> Calculate the multiplication of all the layers
                rdAreas = qgisPV1.pv1Step14(ghiAlignPath, npaAlignPath, lanAlignPath, slopeFltPath, config)
                    
                # Step 15 -> Calculate regions
                outCsvFile = qgisPV1.pv1Step15(rdAreas, nutsOut, process, user, nutsid, config)
                
                # Upload the output file to the SFTP Server
                if outCsvFile:
                    logger.info('  QGIS Server/> Uploading the result file...')
                    logger.info('')
                    remOutput = io.retrieveOutputTmpPath(False, config) +\
                        outCsvFile[outCsvFile.rfind('/') + 1:]
                    remOutput = remOutput.replace('{1}', user)
                    sftp.uploadOutputFile(outCsvFile, remOutput, config)
                
        result = outCsvFile
    except ValueError as valueError:
        result = None
    except ValidationError as validationError:
        result = None
    except Exception as error:
        result = None
    finally:
        # Remove all the temporary layer files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.layers.tmp']) != 1:
            logger.info('  QGIS Server/> Removing al the temporary layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersTmpPath(config))
        
        # Remove all the temporary files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.files.tmp']) != 1:
            logger.info('  QGIS Server/> Removing al the temporary files...')
            io.removeFilesFromDirectory(io.retrieveFilesTmpPath(config))

    # Return the result
    logger.info('')
    return result


# Function: Execute building preprocess
def executeBuildingPreprocess(process, nutsid, user):
    ''' API function to execute the buildings preprocess. '''
    
    outCsvFile = None
    try:
        # Retrieve the layers from the database
        logger.info('')
        layerList = db.retrieveAllLayersByProcess(process, config)
        if layerList and len(layerList) > 0:
            # Load the layers from the SFTP Server
            logger.info('')
            logger.info('  QGIS Server/> Retrieving the layers from the SFTP Server (if needed)...')
            logger.info('')
            
            success = sftp.retrieveLayerFiles(layerList, config)
            if success:
                # Retrieve the files from the database
                logger.info('')
                fileList = db.retrieveAllFilesByProcess(process, config)
                if fileList and len(fileList) > 0:
                    # Load the files from the SFTP Server
                    logger.info('')
                    logger.info('  QGIS Server/> Retrieving the files from the SFTP Server (if needed)...')
                    logger.info('')
                    success = sftp.retrieveDataFiles(fileList, config)
                    if success:
                        # Retrieve the resources from the database
                        logger.info('')
                        resourceList = db.retrieveAllResources(process, config)
                        logger.info('')

                        # Step 01 -> Download and unzip
                        destinationDir = qgisBP1.bp1Step01(nutsid, fileList, resourceList, config, properties)
                            
                        # Step 02 -> Export the selected NUTS
                        nutsFltCrs, outNuts54009 = qgisBP1.bp1Step02(layerList[0], nutsid, config, properties)
                            
                        # Step 03 -> Clip and save the vector layers
                        clippedLayers = qgisBP1.bp1Step03(destinationDir, nutsFltCrs)
                            
                        # Step 04 -> Load the buildings layer
                        buildingsLayer = qgisBP1.bp1Step04(clippedLayers, True, config)
                            
                        # Step 05 -> Load the NUTS layer
                        nutsLayer = qgisBP1.bp1Step05(outNuts54009)
                            
                        # Step 06 -> Load the land use layer
                        landUseLayer = qgisBP1.bp1Step06(clippedLayers)
                            
                        # Step 07 -> Load the Raster Use layer
                        rasterUseLayer = qgisBP1.bp1Step07(layerList[2], config)
                            
                        # Step 08 -> Load the Raster Height layer
                        rasterHeightLayer = qgisBP1.bp1Step08(layerList[6], config)
                            
                        ##### Start the building preprocessing #####
                          
                        # Step 09 -> Assign NUTS
                        qgisBP1.bp1Step09(buildingsLayer, nutsLayer, nutsid)
                            
                        # Step 10 -> Calculate height volumes
                        qgisBP1.bp1Step10(buildingsLayer, rasterHeightLayer)
                            
                        # Step 11 -> Calculate statistics and mapping
                        qgisBP1.bp1Step11(buildingsLayer, rasterUseLayer, landUseLayer, fileList[1], config)
                        
                        # Step 12 -> Adjoin facade calculations
                        buildings = qgisBP1.bp1Step12(True, config)
                            
                        # Step 13 -> Mask raster layers
                        clippedRasters = qgisBP1.bp1Step13(layerList, config)
                            
                        # Step 14 -> Process clipped layers
                        layers_dict = qgisBP1.bp1Step14(nutsid, clippedRasters,
                            fileList[2], destinationDir, config)
                        
                        # Step 15 -> Assign year info
                        buildings = qgisBP1.bp1Step15(nutsid, buildings, layers_dict, fileList[2], config)
                        
                        # Step 16 -> Calculate additional info
                        buildings = qgisBP1.bp1Step16(buildings)
                        
                        # Step 17 -> Prepare clustering ([n_clusters_AB , n_clusters_SFH, n_clusters_SS])
                        clusters = [4, 3, 1]
                        dfAB, dfSFH, dfSS = qgisBP1.bp1Step17(buildings)
                        
                        # Step 18 -> Perform clustering (AB)
                        dfClustersAB = qgisBP1.bp1Step18(dfAB, clusters[0])
                        
                        # Step 19 -> Perform clustering (SFH)
                        dfClustersSFH = qgisBP1.bp1Step19(dfSFH, clusters[1])
                        
                        # Step 20 -> Perform clustering (SS)
                        dfClustersSS = qgisBP1.bp1Step20(dfSS, clusters[2])
                        
                        # Step 21 -> Create the final Dataframe
                        dfFinal, outCsvFile = qgisBP1.bp1Step21(dfClustersAB, dfClustersSFH,
                            dfClustersSS, process, user, nutsid)
                        
                        # Upload the output file to the SFTP Server
                        if outCsvFile:
                            logger.info('  QGIS Server/> Uploading the result file...')
                            logger.info('')
                            remOutput = io.retrieveOutputTmpPath(False, config) +\
                                outCsvFile[outCsvFile.rfind('/') + 1:]
                            remOutput = remOutput.replace('{1}', user)
                            sftp.uploadOutputFile(outCsvFile, remOutput, config)

        result = outCsvFile
    except ValueError as valueError:
        raise
    except ValidationError as validationError:
        raise
    except Exception as error:
        raise
    finally:
        # Remove all the temporary layer files
        if int(config['IDESIGNRES']['idesignres.persistence.layers.tmp']) != 1:
            logger.info('  QGIS Server/> Removing al the temporary layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersTmpPath(config))
        
        # Remove all the layer files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.layers']) != 1:
            logger.info('  QGIS Server/> Removing al the layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersBasePath(config))

    # Return the result
    logger.info('')
    return result


# Function: Execute PV Power Plants process
@app.route('/api/qgis/pv-power-plants-process', methods = ['POST'])
@jwt_required()
def executePVPowerPlantsProcess():
    ''' API function to execute the PV Power Plants process. '''
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************************************')
    logger.info('****************************  IDESIGNRES :: Version ' + config['IDESIGNRES']['idesignres.version'])
    logger.info('****************************  FUNCTION   :: PV Power Plants process')
    logger.info('****************************************************************************************')

    # Extract the current user from the JWT token
    user = get_jwt_identity()
    
    # Extract the body from the request
    body = request.get_json()

    try:
        # Validate if the input corresponds to the schema
        validate(instance = body, schema = jsonSchema.pvPowerPlantsProcessSchema)
        if not body['nutsid'].strip() or not body['slope_angle'] or not user.strip():
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.json.empty.property'])
        
        # Perform other validations (Valid NUTSID)
        nutsids = [nutsid.strip() for nutsid in config['IDESIGNRES-PARAMETERS']['idesignres.params.nutsids'].split(',')]
        if body['nutsid'].strip().upper() not in nutsids:
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.nutsid.not.valid'])

        # Check if the user has his/her own output directory
        if not sftp.checkUserDirectory(user, config):
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.output'])
        logger.info('')
        
        # Retrieve the processess from the database
        processList = db.retrieveAllProcesses(config)
        if processList and len(processList) > 0 and processList[0]:
            # Check if the result already exists
            if int(config['IDESIGNRES']['idesignres.check.previous.results']) == 1:
                remFile = config['IDESIGNRES-PATH']['idesignres.path.output.zip.name'].replace('{1}',
                    processList[0]['uuid']).replace('{2}', body['nutsid'].strip())
                fileExists = sftp.fileExists(config['IDESIGNRES-PATH']['idesignres.path.output'] +\
                    user + '/' + remFile, config)
                if fileExists:
                    logger.info('')
                    logger.info('  SFTP Server/> ' +\
                        properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.result.exists'])
                    logger.info('')
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.result.exists'])
        
            # Init QGIS
            logger.info('')
            qgisApp = qgis.init()

            # Create QGIS project
            logger.info('')
            logger.info('  QGIS Server/> Creating project...')
            qgis.createProject(io.retrieveProjectsBasePathConcatProjectName(config),
                io.retrieveDefaultProjectName(config),
                properties)

            # Execute the preprocess
            result = None
            if int(config['IDESIGNRES']['idesignres.preprocess.pv']) == 1:
                result = executeSolarPreprocess(processList[0]['uuid'], body['nutsid'].strip(),
                    body['slope_angle'], user.strip())
                if not result or not io.fileExists(result):
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.no.input.data.preprocess'])
            
            # Step 01 -> Load the specific configuration
            listParametersTH, listParametersPV, systemCost, landUseTH, landUsePV, minGhiTH, minGhiPV,\
            effTH, effOp, aperture, tCoord, year, tilt, azimuth, tracking, loss, opexTH, opexPV =\
                qgisPV2.pv2Step01(config)
            
            # Step 02 -> Download the result of the Solar preprocess and load the data
            scadaTH, scadaPV = qgisPV2.pv2Step02(user, body['nutsid'].strip(), processList[0]['uuid'], config)
            if scadaTH is None or scadaTH.empty or scadaPV is None or scadaPV.empty:
                raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.no.input.data.preprocess'])
                
            # Step 03 -> Calculate the available thermal area
            areaTH, powerTH, capexTH = qgisPV2.pv2Step03(listParametersTH, systemCost, landUseTH)
                
            # Step 04 -> Calculate the available PV area
            areaPV, powerPV, capexPV = qgisPV2.pv2Step04(listParametersPV, systemCost, landUsePV)
                
            # Step 05 -> Thermal production
            nuts2TH, rowsTH, potDistTH, dfTH = qgisPV2.pv2Step05(scadaTH, areaTH, minGhiTH,
                landUseTH, effTH, effOp, aperture, tCoord, year)
                
            # Step 06 -> PV production
            nameNuts2, nuts2PV, potDistPV, dfPV = qgisPV2.pv2Step06(rowsTH, scadaPV,
                areaPV, minGhiPV, landUsePV, tilt, azimuth, tracking, loss, tCoord, year)
              
            # Step 07 -> Calculate the aggregated production
            prodAggregated = qgisPV2.pv2Step07(dfTH, dfPV, nameNuts2)
                
            # Step 08 -> Calculate the distribution production
            nuts2Distrib = qgisPV2.pv2Step08(nuts2TH, nuts2PV)
            
            # Step 09 -> Save the results
            outputs = qgisPV2.pv2Step09(prodAggregated, nuts2Distrib, nameNuts2, potDistTH,
                potDistPV, opexTH, opexPV, config)
                        
            # Compress and upload the output files to the SFTP Server
            if outputs and len(outputs) > 0:
                logger.info('  QGIS Server/> Compressing the result files...')
                logger.info('')
                fil = io.retrieveOutputBasePath(True, config) + processList[0]['uuid'] + '_' +\
                    body['nutsid'].strip() + '.zip' 
                with zipfile.ZipFile(fil, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for locOutput in outputs:
                        zipf.write(locOutput, locOutput[locOutput.rfind('/') + 1:])
            remOutput = io.retrieveOutputBasePath(False, config) + fil[fil.rfind('/') + 1:]
            remOutput = remOutput.replace('{1}', user)
            sftp.uploadOutputFile(fil, remOutput, config)

        # Create the OK response
        response = rest.buildResponse200Value(properties['IDESIGNRES-REST']['idesignres.rest.result.download'], properties)
        if not request.headers.get('X-Julia') is None and bool(request.headers.get('X-Julia')):
            response = rest.buildResponse200TimeSeries(io.buildDictionaryFromPVOutputFile(outputs[0]), properties)
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
            logger.info('  QGIS Server/> Removing al the local output files...')
            io.removeFilesFromDirectory(io.retrieveOutputBasePath(True, config))
        
        # Remove the project file
        logger.info('  QGIS Server/> Removing the project...')
        qgis.removeProject(io.retrieveProjectsBasePathConcatProjectName(config))

    # Return the response
    logger.info('')
    return response
    

# Function: Execute building energy simulation process
@app.route('/api/qgis/building-energy-simulation-process', methods = ['POST'])
@jwt_required()
def executeBuildingEnergySimulationProcess():
    ''' API function to execute the Building Energy Simulationprocess. '''
    
    # Show info logs
    logger.info('')
    logger.info('****************************************************************************************')
    logger.info('****************************  IDESIGNRES :: Version ' + config['IDESIGNRES']['idesignres.version'])
    logger.info('****************************  FUNCTION   :: Building energy simulation process')
    logger.info('****************************************************************************************')

    # Extract the current user from the JWT token
    user = get_jwt_identity()
    
    # Extract the body from the request
    body = request.get_json()

    try:
        # Validate if the input corresponds to the schema
        validate(instance = body, schema = jsonSchema.buildingEnergySimulationProcessSchema)
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
        refLevels = [lvl.strip() for lvl in config['IDESIGNRES-PARAMETERS']['idesignres.params.ref.levels'].split(',')]
        for measure in body['scenario']['passive_measures']:
            if measure['building_use'].strip() not in archetypes:
                raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.passive.measures.archetypes'])
            if measure['ref_level'].strip().lower() not in refLevels:
                raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.passive.measures.ref.level'])

        # Check if the user has his/her own output directory
        if not sftp.checkUserDirectory(user, config):
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.output'])
        logger.info('')
        
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
                remFile = config['IDESIGNRES-PATH']['idesignres.path.output.zip.name'].replace('{1}',
                    processList[1]['uuid']).replace('{2}', body['nutsid'].strip())
                fileExists = sftp.fileExists(config['IDESIGNRES-PATH']['idesignres.path.output'] +\
                    user + '/' + remFile, config)
                if fileExists:
                    logger.info('')
                    logger.info('  SFTP Server/> ' +\
                        properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.result.exists'])
                    logger.info('')
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.result.exists'])
        
            # Retrieve the dbase files from the SFTP Server
            logger.info('')
            logger.info('  QGIS Server/> Retrieving the dbase files from the SFTP Server...')
            logger.info('')
            dbaseFileList = sftp.retrieveDbaseFiles(config)
            logger.info('')
            if dbaseFileList and len(dbaseFileList) > 0:
                # Init QGIS
                qgisApp = qgis.init()

                # Create QGIS project
                logger.info('')
                logger.info('  QGIS Server/> Creating project...')
                logger.info('')
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
                dfCsv = qgisBP2.bp2Step01(user, body['nutsid'].strip(), processList[1]['uuid'], config)
                if dfCsv is None or dfCsv.empty:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.no.input.data.preprocess'])

                # Step 02 -> Retrieve temperatures
                tempsPath = qgisBP2.bp2Step02(body['nutsid'].strip(), body['year'], dbaseFileList[6], config, properties)
                        
                # Step 03 -> Retrieve radiation values
                radPath = qgisBP2.bp2Step03(body['nutsid'].strip(), body['year'], dbaseFileList[5], config, properties)
                if not tempsPath or not radPath:
                    raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.validation.no.rad.temp'])
               
                # Step 04 -> Load the database
                dfDHW, dfYears, dfSectors, dfSeasons, dfTemperatures, dfSchedule, dfResHHTes, dfSerHHTes,\
                dfUvalues, dfRetroUvalues, dfACH, dfBaseTemperatures, dfCalendar, dfBesCapex, dfBesOpex,\
                dfRes, dfBesCapacity, dfRetroCost, dfSolarOffice, dfSolarNoffice, dfDwellings, dfRTHHEff =\
                    qgisBP2.bp2Step04(dbaseFileList, body)
                            
                # Step 05 -> Add new columns to the input dataframe
                dfInput = qgisBP2.bp2Step05(dfCsv)
                            
                # Step 06 -> Add the input data
                dfInput = qgisBP2.bp2Step06(dfCsv, dfDHW, dfYears, dfSectors, dfDwellings, body, properties)
                del dfYears, dfSectors, dfDwellings
                            
                # Step 07 -> Add the active measures
                dfInput = qgisBP2.bp2Step07(dfCsv, dfResHHTes, dfSerHHTes, dfRTHHEff, config, body)
                del dfResHHTes, dfSerHHTes, dfRTHHEff
                            
                # Step 08 -> Add the passive measures
                dfInput = qgisBP2.bp2Step08(dfCsv, body)
                            
                # Step 09 -> Add the U-Values and the Internal Gains dataframes
                dfInput = qgisBP2.bp2Step09(dfCsv, dfDHW, dfUvalues, dfRetroUvalues, dfACH, body)
                del dfDHW, dfUvalues, dfRetroUvalues, dfACH
                            
                # Step 10 -> Add the CAPEX dataframe
                dfInput = qgisBP2.bp2Step10(dfInput, dfBesCapex)
                del dfBesCapex
                            
                # Step 11 -> Add the OPEX dataframe
                dfInput = qgisBP2.bp2Step11(dfInput, dfBesOpex)
                del dfBesOpex
                            
                # Step 12 -> Add the Retroffiting Cost dataframe
                dfInput = qgisBP2.bp2Step12(dfInput, dfRetroCost)
                del dfRetroCost
                            
                # Step 13 -> Add the Renewable Energy Systems dataframe
                dfInput = qgisBP2.bp2Step13(dfInput, dfRes)
                del dfRes
                            
                # Step 14 -> Add the Capacity dataframe
                dfInput = qgisBP2.bp2Step14(dfInput, dfBesCapacity, config)
                del dfBesCapacity
                            
                # Step 15 -> Add the Equivalent Power dataframe
                dfInput = qgisBP2.bp2Step15(dfInput)
                            
                # Step 16 -> Calculate the costs
                dfInput = qgisBP2.bp2Step16(dfInput)
                        
                # Step 17 -> Calculate the General Schedule
                dictSchedule = qgisBP2.bp2Step17(dfInput, dfSchedule, dfTemperatures, dfBaseTemperatures,
                    dfSolarOffice, dfSolarNoffice, body)
                del dfTemperatures, dfBaseTemperatures, dfSolarOffice, dfSolarNoffice
                            
                # Step 18 -> Calculate the Scenario
                dictSchedule = qgisBP2.bp2Step18(dfInput, dictSchedule, config, body)
                            
                # Step 19 -> Calculate the Anual Results
                dfAnualResults = qgisBP2.bp2Step19(dfInput, dictSchedule)
                            
                # Step 20 -> Calculate the Consolidate
                dictConsolidated = {}
                for arch in archetypes:
                    dictConsolidated[arch] = qgisBP2.bp2Step20(dfInput, dictSchedule, arch)
                            
                # Step 21 -> Calculate the Hourly Results
                dictHourlyResults = {}
                for arch in archetypes:
                    dictHourlyResults[arch] = qgisBP2.bp2Step21(dfInput, dictSchedule, arch)
                del dictSchedule
                           
                # Step 22 -> Save the final result
                output = qgisBP2.bp2Step22(dfInput, dfAnualResults, dictConsolidated, dictHourlyResults, config)
                del dfInput, dfAnualResults, dictConsolidated, dictHourlyResults
                            
                # Compress and upload the output file to the SFTP Server
                if output:
                    logger.info('  QGIS Server/> Compressing the result file...')
                    logger.info('')
                    fil = io.retrieveOutputBasePath(True, config) + processList[1]['uuid'] + '_' + body['nutsid'].strip() + '.zip' 
                    with zipfile.ZipFile(fil, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write(output, output[output.rfind('/') + 1:])
                    remOutput = io.retrieveOutputBasePath(False, config) + fil[fil.rfind('/') + 1:]
                    remOutput = remOutput.replace('{1}', user)
                    sftp.uploadOutputFile(fil, remOutput, config)

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
            logger.info('  QGIS Server/> Removing al the temporary layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersTmpPath(config))
        
        # Remove all the layer files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.layers']) != 1:
            logger.info('  QGIS Server/> Removing al the layer files...')
            io.removeFilesFromDirectory(io.retrieveLayersBasePath(config))
        
        # Remove all the temporary files
        if int(config['IDESIGNRES']['idesignres.persistence.files.tmp']) != 1:
            logger.info('  QGIS Server/> Removing al the temporary files...')
            io.removeFilesFromDirectory(io.retrieveFilesTmpPath(config))
        
        # Remove all the output files if it is allowed
        if int(config['IDESIGNRES']['idesignres.persistence.output']) != 1:
            logger.info('  QGIS Server/> Removing al the local output files...')
            io.removeFilesFromDirectory(io.retrieveOutputBasePath(True, config))
        
        # Remove the project file
        logger.info('  QGIS Server/> Removing the project...')
        qgis.removeProject(io.retrieveProjectsBasePathConcatProjectName(config))

    # Return the response
    logger.info('')
    return response



# Run app
if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 5010)
