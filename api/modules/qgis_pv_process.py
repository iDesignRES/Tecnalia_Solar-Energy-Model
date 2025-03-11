import logging
import json
import pvlib

import pandas as pd

from pathlib import Path
from pyproj import Transformer
from typing import Union

import modules.sftp as sftp
import modules.io as mio

from modules.logging_config import logger


#####################################################################
############################## Process ##############################
#####################################################################


# Function: PV Power Plants -> Process -> Step 01 -> Load the specific configuration
def pv2Step01(config):
    ''' PV Power Plants -> Process -> Step 01 : Load the specific configuration. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 01 -> Loading the specific configuration...')
    with open(config['IDESIGNRES-PATH']['idesignres.path.pv.config'], 'r') as configFile:
        configuration = json.load(configFile)
        if not configuration:
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.configuration.not.loaded'])
            
        listParametersTH = [configuration['system']['area_total_thermal'],
            configuration['system']['power_thermal'],
            configuration['system']['capex_thermal']]
        listParametersPV = [configuration['system']['area_total_pv'],
            configuration['system']['power_pv'],
            configuration['system']['capex_pv']]
        systemCost = int(configuration['system']['system_cost']) # in €
        landUseTH = int(configuration['system']['land_use_thermal'])  # in W/m2
        landUsePV = int(configuration['system']['land_use_pv'])  # in W/m2
        minGhiTH = int(configuration['system']['min_ghi_thermal'])  # in W/m2
        minGhiPV = int(configuration['system']['min_ghi_pv'])  # in W/m2
        effTH = float(configuration['system']['efficiency_thermal'] / 100)
        effOp = float(configuration['system']['efficiency_optical'] / 100)
        aperture = float(configuration['system']['aperture'] / 100)
        tCoord = True if int(configuration['system']['type_coord']) == 1 else False
        year = int(configuration['system']['pvgis_year'])
        tilt = int(configuration['system']['tilt'])
        azimuth = int(configuration['system']['azimuth'])
        tracking = int(configuration['system']['tracking'])
        loss = float(configuration['system']['loss'])  # in %
        opexTH = int(configuration['system']['opex_thermal'])  # in €/W
        opexPV = int(configuration['system']['opex_pv'])  # in €/W
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 01 -> [OK]')
    logger.info('')
    return listParametersTH, listParametersPV, systemCost, landUseTH, landUsePV,\
        minGhiTH, minGhiPV, effTH, effOp, aperture, tCoord, year, tilt, azimuth,\
        tracking, loss, opexTH, opexPV


# Function: PV Power Plants -> Process -> Step 02 -> Download the previous result
def pv2Step02(currentUser, nutsId, processId, config):
    ''' PV Power Plants -> Process -> Step 02 : Download the previous result. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 02 -> Downloading the result file of the Solar preprocess...')
    logger.info('')
    dfScadaTH, dfScadaPV = None, None
    filePath = config['IDESIGNRES-PATH']['idesignres.path.output.tmp'] + currentUser + '/'
    fileName = config['IDESIGNRES-PATH']['idesignres.path.output.default.name'].replace('{1}', processId).replace('{2}', nutsId)
    download = sftp.retrieveSingleFile(filePath, fileName, config)
    logger.info('')
    if download:
        logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 02 -> Loading the thermal data...')
        dfScadaTH = pd.read_csv(mio.retrieveFilesTmpPath(config) + '/' + fileName, header = 0, encoding = "ISO-8859-1",
            delimiter = ",", decimal = ".").sort_values(by = 'Median_Radiation', ascending = False)

        logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 02 -> Loading the photovoltaic data...')
        dfScadaPV = pd.read_csv(mio.retrieveFilesTmpPath(config) + '/' + fileName, header = 0, encoding = "ISO-8859-1",
            delimiter = ",", decimal = ".").sort_values(by = 'Median_Radiation', ascending = False)

    # Finish    
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 02 -> [OK]')
    logger.info('')
    return dfScadaTH, dfScadaPV


# Function: PV Power Plants -> Process -> Step 03 -> Calculate the available thermal area
def pv2Step03(listParametersTH, systemCost, landUseTH):
    ''' PV Power Plants -> Process -> Step 03 : Calculate the available thermal area. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Calculating the available thermal area...')
    areaTH, powerTH, capexTH = getAvailableArea(
    	parameters = listParametersTH, cost = systemCost, landUse = landUseTH)

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Area -> ' + str(areaTH))
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Power -> ' + str(powerTH))
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Capex -> ' + str(capexTH))
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> [OK]')
    logger.info('')
    return areaTH, powerTH, capexTH


# Function: PV Power Plants -> Process -> Step 04 -> Calculate the available PV area
def pv2Step04(listParametersPV, systemCost, landUsePV):
    ''' PV Power Plants -> Process -> Step 04 : Calculate the available PV area. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Calculating the available PV area...')
    areaPV, powerPV, capexPV = getAvailableArea(
    	parameters = listParametersPV, cost = systemCost, landUse = landUsePV)

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Area -> ' + str(areaPV))
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Power -> ' + str(powerPV))
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Capex -> ' + str(capexPV))
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> [OK]')
    logger.info('')
    return areaPV, powerPV, capexPV


# Function: PV Power Plants -> Process -> Step 05 -> Thermal production
def pv2Step05(scadaTH, areaTH, minGhiTH, landUseTH, effTH, effOp, aperture, tCoord, year):
    ''' PV Power Plants -> Process -> Step 03 : Calculate the thermal production. '''

    # Get the regions
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Obtaining the regions...')
    rowsTH, nameNuts2 = getRegions(scada = scadaTH, area = areaTH, minGHI = minGhiTH)
    
    # Get the thermal production
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Obtaining the thermal production...')
    prodTH = getThermalProduction(rows = rowsTH, landUse = landUseTH, effTH = effTH,
        effOp = effOp, aperture = areaTH * aperture, tCoord = tCoord, year = year)
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Saving the thermal production in a DataFrame...')
    dfTH = (pd.DataFrame(prodTH).sum(axis = 0))
    
    # Get the distribution
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Obtaining the distribution...')
    nuts2TH, potDistTH, areasDistTH = getDistribution(rows = rowsTH, label = 'thermal_power')
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> [OK]')
    logger.info('')
    return nuts2TH, rowsTH, potDistTH, dfTH


# Function: PV Power Plants -> Process -> Step 06 -> PV production
def pv2Step06(rowsTH, scadaPV, areaPV, minGhiPV, landUsePV, tilt, azimuth, tracking, loss, tCoord, year):
    ''' PV Power Plants -> Process -> Step 06 : Calculate the PV production. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Removing areas used with thermal power...')
    for region in rowsTH:
        df = scadaPV.loc[(scadaPV['Region'] == region['Region']) & (scadaPV['Threshold'] == region['Threshold'])]
        df['Area_m2'] -= region['Area_m2']
        scadaPV.loc[(scadaPV['Region'] == region['Region']) & (scadaPV['Threshold'] == region['Threshold'])] = df
    
    # Get the regions
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Obtaining the regions...')
    rowsPV, nameNuts2 = getRegions(scada = scadaPV, area = areaPV, minGHI = minGhiPV)
    
    # Get the PV production
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Obtaining the PV production...')
    prodPV = getPVProduction(rows = rowsPV, landUse = landUsePV, tilt = tilt, azimuth = azimuth,
        tracking = tracking, loss = loss, tCoord = tCoord, year = year)
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Saving the PV production in a DataFrame...')
    dfPV = (pd.DataFrame(prodPV).sum(axis = 0))
    
    # Get the distribution
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Obtaining the distribution...')
    nuts2PV, potDistPV, areasDistPV = getDistribution(rows = rowsPV, label = 'pv_power')
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> [OK]')
    logger.info('')
    return nameNuts2, nuts2PV, potDistPV, dfPV


# Function: PV Power Plants -> Process -> Step 07 -> Calculate the aggregated production
def pv2Step07(dfTH, dfPV, nameNuts2):
    ''' PV Power Plants -> Process -> Step 07 : Calculate the aggregated production. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 07 -> Calculating the aggregated production...')
    prodAgreggated = pd.concat([dfTH.reset_index(), dfPV.reset_index()], ignore_index = False, axis = 1)
    prodAgreggated = prodAgreggated.drop(columns = ['time'])
    prodAgreggated = prodAgreggated.set_index('time(UTC)')
    prodAgreggated.columns = ['Pthermal_' + str(nameNuts2), 'Ppv_' + str(nameNuts2)]
    prodAgreggated.index = prodAgreggated.index.strftime('%Y-%m-%d %H:%M:%S')
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 07 -> [OK]')
    logger.info('')
    return prodAgreggated


# Function: PV Power Plants -> Process -> Step 08 -> Calculate the distribution production
def pv2Step08(nuts2TH, nuts2PV):
    ''' PV Power Plants -> Process -> Step 08 : Calculate the distribution production. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 08 -> Calculating the distribution production...')
    nuts2TH = nuts2TH.add_suffix('_Pthermal')
    nuts2PV = nuts2PV.add_suffix('_Ppv')
    nuts2Dist = pd.concat([nuts2TH.reset_index(), nuts2PV.reset_index()], ignore_index = False, axis = 1)
    nuts2Dist = nuts2Dist.drop(columns = ['time'])
    nuts2Dist = nuts2Dist.set_index('time(UTC)')
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 08 -> [OK]')
    logger.info('')
    return nuts2Dist


# Function: PV Power Plants -> Process -> Step 09 -> Save the results
def pv2Step09(prodAgreggated, nuts2Dist, nameNuts2, potDistTH, potDistPV, opexTH, opexPV, config):
    ''' PV Power Plants -> Process -> Step 09 : Save the results. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 09 -> Saving the results...')
    outputs = [mio.retrieveOutputBasePath(True, config) + nameNuts2 + '.csv']
    toCsv(prodAgreggated.reset_index(), outputs[0])
    
    namesNuts3 = list(
        dict.fromkeys([nuts2Dist.columns[col].rsplit('_')[0] for col in range(len(nuts2Dist.columns))]))
    
    for i in range(len(namesNuts3)):
        dfNuts3 = pd.DataFrame()
        nuts3Cols = [x for x in nuts2Dist if (x.startswith(namesNuts3[i]))]
        newNuts3Cols = [item.rsplit('_')[1] for item in nuts3Cols]
        dfNuts3[newNuts3Cols] = nuts2Dist[nuts3Cols]
        output = mio.retrieveOutputBasePath(True, config) + namesNuts3[i] + '.csv'
        outputs.append(output)
        toCsv(dfNuts3.reset_index(), output)
      
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 09 -> Combining the dictionaries...')
    potTH = {f'{k}_thermal': v for k, v in potDistTH.items()}
    potPV = {f'{k}_pv': v for k, v in potDistPV.items()}
    combinedDict = {**potTH, **potPV}
    opexTotTH, opexTotPV = opexCalc(dictData = combinedDict, opexTH = opexTH, opexPV = opexPV)
    combinedDict['opex_thermal'] = opexTotTH  # In €
    combinedDict['opex_pv'] = opexTotPV  # In €
    
    output = mio.retrieveOutputBasePath(True, config) + nameNuts2 + '.json'
    outputs.append(output)
    dictToJson(combinedDict, Path(output), replace = True)
     
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 09 -> [OK]')
    logger.info('')
    return outputs



#####################################################################
######################## Auxiliary functions ########################
#####################################################################


# Auxiliary function: Get coord
def getCoord(df: pd.DataFrame) -> tuple:
    ''' Function to get the coordinates. '''

    sample_x = df['Median_Radiation_X']
    sample_y = df['Median_Radiation_Y']

    transformer = Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy = True)
    xy = transformer.transform(sample_x, sample_y)
    return xy[0], xy[1]


# Auxiliary function: To CSV
def toCsv(df, filename):
    ''' Function to transform a dataframe to CSV. '''

    df.to_csv(filename, index = False, decimal = ',', sep = ';')


# Auxiliary function: Dict to JSON
def dictToJson(d: Union[dict, list], path: Path, replace: bool = False):
    ''' Function to transform a dictionary to JSON. '''

    path = path.with_suffix(".json")
    if replace or not path.is_file():
        with open(path, "w", encoding = "utf-8") as f:
            json.dump(d, f, sort_keys = False, indent = 4)


# Auxiliary function: Thermal model
def thermalModel(radiation: pd.DataFrame, effTH: float, effOp: float, aperture: float) -> list:
    ''' Function to get the thermal model. '''

    return radiation * aperture * effTH * effOp / 1000000  # in  MWh


# Auxiliary function: Get available area
def getAvailableArea(parameters: list, cost: float, landUse: float) -> tuple:
    ''' Function to obtain the available area. '''

    index = next((i for i, value in enumerate(parameters) if value is not None), -1)
    if index == 2:
        capex = parameters[index]
        power = parameters[index] / (cost * 1000000)  # in MW
        area = power * 1000000 / landUse  # in m2
    elif index == 1:
        area = parameters[index] * 1000000 / landUse  # in m2
        power = parameters[index]
        capex = power * cost * 1000000
    else:
        area = parameters[0]  # en m2
        power = (area * landUse) / 1000000  # in MW
        capex = power * cost * 1000000

    return area, power, capex
    

# Auxiliary function: Get regions
def getRegions(scada: dict, area: float, minGHI: float) -> tuple:
    ''' Function to get the regions. '''

    current_sum = 0
    nameNuts2 = None
    rows = []
    for index, row in scada.iterrows():
        if nameNuts2 is None:
            nameNuts2 = row['Region'][:-1]
        if row['Area_m2'] > 0 and row['Region'] != nameNuts2 and row['Threshold'] >= minGHI:
            if current_sum + row['Area_m2'] > area:
                row['Area_m2'] = area - current_sum
                current_sum += row['Area_m2']
                rows.append(row)
                break
            current_sum += row['Area_m2']
            rows.append(row)

    return rows, nameNuts2


# Auxiliary function: Get thermal production
def getThermalProduction(rows: list, landUse: float,
    effTH: float, effOp: float, aperture: float, tCoord: bool, year: int) -> list:
    ''' Function to get the thermal production. '''

    production = []
    for region in rows:
        lon, lat = region['Median_Radiation_X'], region['Median_Radiation_Y']
        if tCoord:
            lon, lat = getCoord(region)

        factor = 1
        data, moths, inputs, metadata = pvlib.iotools.get_pvgis_tmy(
            latitude = lat, longitude = lon, outputformat = 'json',
            usehorizon = True, userhorizon = None, startyear = None,
            endyear = None, map_variables = True,
            timeout = 15)
        
        data.index = data.index.map(lambda x: x.replace(year = year))
        region['radiation'] = data['dni']
        region['temperature'] = data['temp_air']
        pot_MW = (region['Area_m2'] * landUse) / 1000000
        region['power_installed(kW)'] = pot_MW

        region['thermal_power'] = thermalModel(
            radiation = data['dni'], effTH = effTH, effOp = effOp, aperture = aperture) * factor
        production.append(region['thermal_power'])  # in MWh
    return production


# Auxiliary function: Get PV production
def getPVProduction(rows: list, landUse: float, tilt: float, azimuth: float,
    tracking: int, loss: float, tCoord: bool, year: int) -> list:
    ''' Function to get the PV production. '''

    production = []
    for region in rows:
        lon, lat = region['Median_Radiation_X'], region['Median_Radiation_Y']
        if tCoord:
            lon, lat = getCoord(region)

        pot_MW = (region['Area_m2'] * landUse) / 1000000
        region['power_installed(kW)'] = pot_MW
        factor = 1
        
        # pvgis is limited in peakpower to 100000000
        if pot_MW * 1000 > 100000000:
            pot_MW = pot_MW / 1000
            factor = 1000

        prod = []
        df, params, meta = pvlib.iotools.get_pvgis_hourly(
            latitude = lat, longitude = lon, start = year, end = year,
            raddatabase='PVGIS-SARAH3', surface_tilt = tilt, surface_azimuth = azimuth,
            pvcalculation = True, peakpower = pot_MW * 1000,
            trackingtype = tracking,
            loss = loss, components = False)
        prod.append(df['P'])  # in Wh
        region['pv_power'] = (pd.DataFrame(prod).sum(axis = 0)) * factor / 1000000  # to MW
        production.append((pd.DataFrame(prod).sum(axis = 0) * factor / 1000000))  # to MkW
    return production


# Auxiliary function: Get distribution
def getDistribution(rows: list, label: str) -> tuple:
    ''' Function to obtain the distribution. '''

    res = []
    for i in rows:
        if i['Region'] not in res:
            res.append(i['Region'])

    df = pd.DataFrame(rows)
    suma_nuts = []
    suma_areas = []
    suma_pots = []
    for i in res:
        nuts = df.loc[i == df['Region']][label]
        df_nuts = pd.DataFrame(nuts.tolist())
        suma_nuts.append(df_nuts.sum())
        areas_nuts3 = df.loc[i == df['Region']]['Area_m2']
        pot_nuts3 = df.loc[i == df['Region']]['power_installed(kW)']
        suma_areas.append(pd.DataFrame(areas_nuts3.tolist()).sum())
        suma_pots.append(pd.DataFrame(pot_nuts3.tolist()).sum())

    areas = dict(zip(res, [x[0] for x in suma_areas]))
    pots = dict(zip(res, [x[0] for x in suma_pots]))

    nuts2 = pd.DataFrame(suma_nuts, index = res).transpose()
    nuts2 = nuts2.dropna(axis = 1)
    nuts2.index = nuts2.index.strftime('%Y-%m-%d %H:%M:%S')
    return nuts2, pots, areas


# Auxiliary function: Opex calc
def opexCalc(dictData: dict, opexTH: float, opexPV: float) -> tuple:
    ''' Function to calculate the OPEX. '''

    total_th = 0
    total_pv = 0
    for d_key, d_value in dictData.items():
        if 'pv' in d_key:
            total_pv += d_value
        elif 'thermal' in d_key:
            total_th += d_value
    return total_th * opexTH, total_pv * opexPV

