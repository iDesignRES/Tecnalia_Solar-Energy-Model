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
def pv2Step01(body, config):
    ''' PV Power Plants -> Process -> Step 01 : Load the specific configuration. '''
    
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 01 -> Building the specific configuration...')
    areaAvailableTH = checkLimits(body, 'area_total_thermal', 0, 10 ** 10, 0) if 'area_total_thermal' in body else None
    powerTH = checkLimits(body, 'power_thermal', 0, 10 ** 12, 0) if 'power_thermal' in body else None
    capexTH = checkLimits(body, 'capex_thermal', 0, 5 * 10 ** 11, 0) if 'capex_thermal' in body else None
    if areaAvailableTH is None and powerTH is None and capexTH is None:
        areaAvailableTH = 0
        powerTH, capexTH = None, None
        logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 01 -> Default value area TH is ' + str(areaAvailableTH))
    areaAvailablePV = checkLimits(body, 'area_total_pv', 0, 10 ** 10, 0) if 'area_total_pv' in body else None
    powerPV = checkLimits(body, 'power_pv', 0, 10 ** 12, 0) if 'power_pv' in body else None
    capexPV = checkLimits(body, 'capex_pv', 0, 5 * 10 ** 11, 0) if 'capex_pv' in body else None
    if areaAvailablePV is None and powerPV is None and capexPV is None:
        areaAvailablePV = 0
        powerPV, capexPV = None, None
        logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 01 -> Default value area PV is ' + str(areaAvailablePV))
    
    listParametersTH = [areaAvailableTH, powerTH, capexTH]
    listParametersPV = [areaAvailablePV, powerPV, capexPV]
    systemCostTH = checkLimits(body, 'system_cost_thermal', 1, 10, 5)  # in €
    systemCostPV = checkLimits(body, 'system_cost_pv', 0.2, 1, 0.5)    # in €
    loss = checkLimits(body, 'loss', 8, 20, 14)  # in %
    effTH = checkLimits(body, 'efficiency_thermal', 25, 65, 45) / 100
    effOp = checkLimits(body, 'efficiency_optical', 45, 85, 65) / 100
    aperture = checkLimits(body, 'aperture', 25, 75, 50) / 100
    tilt = checkLimits(body, 'tilt', 0, 90, 30)
    azimuth = checkLimits(body, 'azimuth', 0, 360, 180)
    tracking = checkLimits(body, 'tracking_percentage', 0, 100, 60) / 100
    opexTH = checkLimits(body, 'opex_thermal', 0, 40000, 20000)  # in €/W
    opexPV = checkLimits(body, 'opex_pv', 0, 30000, 15000)       # in €/W
    minGhiTH = checkLimits(body, 'min_ghi_thermal', 1500, 2500, 2000)  # in W/m2
    minGhiPV = checkLimits(body, 'min_ghi_pv', 500, 2000, 1000)        # in W/m2
    landUseTH = checkLimits(body, 'land_use_thermal', 25, 100, 50)  # in W/m2
    landUsePV = checkLimits(body, 'land_use_pv', 50, 200, 100)      # in W/m2
    convertCoord = True if int(body['convert_coord']) == 1 else False
    year = int(body['pvgis_year'])
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 01 -> [OK]')
    logger.info('')
    return listParametersTH, listParametersPV, systemCostTH, systemCostPV, landUseTH, landUsePV,\
        minGhiTH, minGhiPV, effTH, effOp, aperture, convertCoord, year, tilt, azimuth,\
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
def pv2Step03(listParametersTH, systemCostTH, landUseTH):
    ''' PV Power Plants -> Process -> Step 03 : Calculate the available thermal area. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Calculating the available thermal area...')
    areaTH, powerTH, capexTH = getAvailableArea(
    	parameters = listParametersTH, cost = systemCostTH, landUse = landUseTH)

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Area -> ' + str(areaTH))
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Power -> ' + str(powerTH))
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Capex -> ' + str(capexTH))
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> [OK]')
    logger.info('')
    return areaTH, powerTH, capexTH


# Function: PV Power Plants -> Process -> Step 04 -> Calculate the available PV area
def pv2Step04(listParametersPV, systemCostPV, landUsePV):
    ''' PV Power Plants -> Process -> Step 04 : Calculate the available PV area. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Calculating the available PV area...')
    areaPV, powerPV, capexPV = getAvailableArea(
    	parameters = listParametersPV, cost = systemCostPV, landUse = landUsePV)

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Area -> ' + str(areaPV))
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Power -> ' + str(powerPV))
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Capex -> ' + str(capexPV))
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> [OK]')
    logger.info('')
    return areaPV, powerPV, capexPV


# Function: PV Power Plants -> Process -> Step 05 -> Thermal production
def pv2Step05(scadaTH, scadaPV, areaTH, minGhiTH, landUseTH, effTH, effOp, aperture, convertCoord, year):
    ''' PV Power Plants -> Process -> Step 03 : Calculate the thermal production. '''

    # Get the regions
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Obtaining the regions...')
    rowsTH, nameNuts2 = getRegions(scada = scadaTH, area = areaTH, minGHI = minGhiTH)
    
    # Get the thermal production and save it to a dataframe
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Obtaining the thermal production...')
    prodTH = getThermalProduction(rows = rowsTH, landUse = landUseTH, effTH = effTH,
        effOp = effOp, aperture = areaTH * aperture, convertCoord = convertCoord, year = year)
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Saving the thermal production in a DataFrame...')
    dfTH = (pd.DataFrame(prodTH).sum(axis = 0))
    
    # Get the distribution
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Obtaining the distribution...')
    if not dfTH.empty:
        nuts2TH, potDistTH, areasDistTH = getDistribution(rows = rowsTH, label = 'thermal_power')

        # Remove areas used with TH
        logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Removing areas used with thermal power...')
        for region in rowsTH:
            df = scadaPV.loc[(scadaPV['Region'] == region['Region']) & (scadaPV['Threshold'] == region['Threshold'])]
            df['Area_m2'] -= region['Area_m2']
            scadaPV.loc[(scadaPV['Region'] == region['Region']) & (scadaPV['Threshold'] == region['Threshold'])] = df
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> [OK]')
    logger.info('')
    return nuts2TH, rowsTH, potDistTH, dfTH, scadaPV


# Function: PV Power Plants -> Process -> Step 06 -> PV production
def pv2Step06(rowsTH, scadaPV, areaPV, minGhiPV, landUsePV, tilt, azimuth, tracking, loss, convertCoord, year):
    ''' PV Power Plants -> Process -> Step 06 : Calculate the PV production. '''

    # Get the regions
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Obtaining the regions...')
    rowsPV, nameNuts2 = getRegions(scada = scadaPV, area = areaPV, minGHI = minGhiPV)
    
    # Get the PV production
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Obtaining the PV production...')
    prodPVTracking = getPVProduction(rows = rowsPV, landUse = landUsePV, tilt = tilt, azimuth = azimuth,
        tracking = 1, loss = loss, convertCoord = convertCoord, year = year)
    prodPVFixed = getPVProduction(rows = rowsPV, landUse = landUsePV, tilt = tilt, azimuth = azimuth,
        tracking = 0, loss = loss, convertCoord = convertCoord, year = year)
    prodPV = list(map(sum, zip(map(lambda x: x * tracking, prodPVTracking), map(lambda x: x * (1 - tracking), prodPVFixed))))
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
    if not dfTH.empty:
        prodAgreggated = pd.concat([dfTH.reset_index(), dfPV.reset_index()], ignore_index = False, axis = 1)
        prodAgreggated = prodAgreggated.drop(columns = ['time'])
        prodAgreggated = prodAgreggated.set_index('time(UTC)')
        prodAgreggated.columns = ['Pthermal_' + str(nameNuts2), 'Ppv_' + str(nameNuts2)]
        prodAgreggated.index = pd.to_datetime(prodAgreggated.index, format = '%Y-%m-%d %H:%M:%S').round('H').strftime('%Y-%m-%d %H:%M:%S')
    else:
        prodAgreggated = pd.DataFrame(dfPV, columns = ['Ppv_' + str(nameNuts2)])
        prodAgreggated.index = pd.to_datetime(prodAgreggated.index).round('H').strftime('%Y-%m-%d %H:%M:%S')
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 07 -> [OK]')
    logger.info('')
    return prodAgreggated


# Function: PV Power Plants -> Process -> Step 08 -> Calculate the distributed production
def pv2Step08(dfTH, nuts2TH, nuts2PV):
    ''' PV Power Plants -> Process -> Step 08 : Calculate the distributed production. '''

    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 08 -> Calculating the distributed production...')
    if not dfTH.empty:
        nuts2TH = nuts2TH.add_suffix('_Pthermal')
        nuts2PV = nuts2PV.add_suffix('_Ppv')
        nuts2Dist = pd.concat([nuts2TH.reset_index(), nuts2PV.reset_index()], ignore_index = False, axis = 1)
        nuts2Dist = nuts2Dist.drop(columns = ['time'])
        nuts2Dist = nuts2Dist.set_index('time(UTC)')
    else:
        nuts2PV = nuts2PV.add_suffix('_Ppv')
        nuts2Dist = nuts2PV
        nuts2Dist = nuts2Dist.rename_axis('time(UTC)')
    
    # Finish
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 08 -> [OK]')
    logger.info('')
    return nuts2Dist


# Function: PV Power Plants -> Process -> Step 09 -> Save the results
def pv2Step09(prodAgreggated, nuts2Dist, nameNuts2, dfTH, potDistTH, potDistPV, opexTH, opexPV, config):
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
    potPV = {f'{k}_pv': v for k, v in potDistPV.items()}
    if not dfTH.empty:
        potTH = {f'{k}_thermal': v for k, v in potDistTH.items()}
        combinedDict = {**potTH, **potPV}
    else:
        combinedDict = {**potPV}
    
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 09 -> Calculating the OPEX...')
    opexTotTH, opexTotPV = opexCalc(dictData = combinedDict, opexTH = opexTH, opexPV = opexPV)
    combinedDict['opex_thermal'] = opexTotTH  # In €
    combinedDict['opex_pv'] = opexTotPV  # In €
    
    logger.info('  QGIS Server/> PV Power Plants -> Process -> Step 09 -> Saving...')
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


# Auxiliary function: Check limits
def checkLimits(dictToEvaluate, name, limitDown, limitUp, defaultValue):
    if name in dictToEvaluate:
        value = dictToEvaluate[name]
        if value is not None:
            if limitDown <= value <= limitUp:
                return value
            return defaultValue
        return value
    return defaultValue


# Auxiliary function: Get coord
def getCoord(df: pd.DataFrame) -> tuple:
    ''' Function to get the coordinates. '''

    sampleX = df['Median_Radiation_X']
    sampleY = df['Median_Radiation_Y']

    transformer = Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy = True)
    xy = transformer.transform(sampleX, sampleY)
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

    currentSum = 0
    nameNuts2 = None
    rows = []
    for index, row in scada.iterrows():
        if nameNuts2 is None:
            nameNuts2 = row['Region'][:-1]
        if row['Area_m2'] > 0 and row['Region'] != nameNuts2 and row['Threshold'] >= minGHI:
            if currentSum + row['Area_m2'] > area:
                row['Area_m2'] = area - currentSum
                currentSum += row['Area_m2']
                rows.append(row)
                break
            currentSum += row['Area_m2']
            rows.append(row)

    return rows, nameNuts2


# Auxiliary function: Get thermal production
def getThermalProduction(rows: list, landUse: float,
    effTH: float, effOp: float, aperture: float, convertCoord: bool, year: int) -> list:
    ''' Function to get the thermal production. '''

    production = []
    for region in rows:
        lon, lat = region['Median_Radiation_X'], region['Median_Radiation_Y']
        if convertCoord or lat > 180:
            lon, lat = getCoord(region)

        factor = 1
        data, moths, inputs, metadata = pvlib.iotools.get_pvgis_tmy(
            latitude = lat, longitude = lon, outputformat = 'json',
            usehorizon = True, userhorizon = None, startyear = None,
            endyear = None, map_variables = True,
            timeout = 30)
        
        data.index = data.index.map(lambda x: x.replace(year = year))
        region['radiation'] = data['dni']
        region['temperature'] = data['temp_air']
        region['power_installed(kW)'] = (region['Area_m2'] * landUse) / 1000000

        region['thermal_power'] = thermalModel(
            radiation = data['dni'], effTH = effTH, effOp = effOp, aperture = aperture) * factor
        production.append(region['thermal_power'])  # in MWh
    return production


# Auxiliary function: Get PV production
def getPVProduction(rows: list, landUse: float, tilt: float, azimuth: float,
    tracking: int, loss: float, convertCoord: bool, year: int) -> list:
    ''' Function to get the PV production. '''

    production = []
    for region in rows:
        lon, lat = region['Median_Radiation_X'], region['Median_Radiation_Y']
        if convertCoord:
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
    sumNuts = []
    sumAreas = []
    sumPots = []
    for i in res:
        nuts = df.loc[i == df['Region']][label]
        dfNuts = pd.DataFrame(nuts.tolist())
        sumNuts.append(dfNuts.sum())
        areasNuts3 = df.loc[i == df['Region']]['Area_m2']
        potNuts3 = df.loc[i == df['Region']]['power_installed(kW)']
        sumAreas.append(pd.DataFrame(areasNuts3.tolist()).sum())
        sumPots.append(pd.DataFrame(potNuts3.tolist()).sum())

    areas = dict(zip(res, [x[0] for x in sumAreas]))
    pots = dict(zip(res, [x[0] for x in sumPots]))

    nuts2 = pd.DataFrame(sumNuts, index = res).transpose()
    nuts2 = nuts2.dropna(axis = 1)
    nuts2.index = nuts2.index.strftime('%Y-%m-%d %H:%M:%S')
    return nuts2, pots, areas


# Auxiliary function: Opex calc
def opexCalc(dictData: dict, opexTH: float, opexPV: float) -> tuple:
    ''' Function to calculate the OPEX. '''

    totalTH = 0
    totalPV = 0
    for dKey, dValue in dictData.items():
        if 'thermal' in dKey:
            totalTH += dValue
        elif 'pv' in dKey:
            totalPV += dValue
    return totalTH * opexTH, totalPV * opexPV

