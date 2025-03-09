import logging
import json
import pvlib

import pandas as pd

from pathlib import Path
from pyproj import Transformer
from typing import Union

import modules.sftp as sftp
import modules.io as mio


#####################################################################
############################## Process ##############################
#####################################################################


# Function: PV Power Plants -> Process -> Step 01 -> Load the specific configuration
def pv2_step_01(config):
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 01 -> Loading the specific configuration...')
    with open(config['IDESIGNRES-PATH']['idesignres.path.pv.config'], 'r') as config_file:
        configuration = json.load(config_file)
        if not configuration:
            raise ValueError(properties['IDESIGNRES-EXCEPTIONS']['idesignres.exception.configuration.not.loaded'])
            
        list_parameters_th = [configuration['system']['area_total_thermal'],
            configuration['system']['power_thermal'],
            configuration['system']['capex_thermal']]
        list_parameters_pv = [configuration['system']['area_total_pv'],
            configuration['system']['power_pv'],
            configuration['system']['capex_pv']]
        system_cost = int(configuration['system']['system_cost']) # in €
        land_use_th = int(configuration['system']['land_use_thermal'])  # in W/m2
        land_use_pv = int(configuration['system']['land_use_pv'])  # in W/m2
        min_ghi_th = int(configuration['system']['min_ghi_thermal'])  # in W/m2
        min_ghi_pv = int(configuration['system']['min_ghi_pv'])  # in W/m2
        eff_th = float(configuration['system']['efficiency_thermal'] / 100)
        eff_op = float(configuration['system']['efficiency_optical'] / 100)
        aperture = float(configuration['system']['aperture'] / 100)
        t_coord = True if int(configuration['system']['type_coord']) == 1 else False
        year = int(configuration['system']['pvgis_year'])
        tilt = int(configuration['system']['tilt'])
        azimuth = int(configuration['system']['azimuth'])
        tracking = int(configuration['system']['tracking'])
        loss = float(configuration['system']['loss'])  # in %
        opex_th = int(configuration['system']['opex_thermal'])  # in €/W
        opex_pv = int(configuration['system']['opex_pv'])  # in €/W
    
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 01 -> [OK]')
    logging.info('')
    return list_parameters_th, list_parameters_pv, system_cost, land_use_th, land_use_pv,\
        min_ghi_th, min_ghi_pv, eff_th, eff_op, aperture, t_coord, year, tilt, azimuth,\
        tracking, loss, opex_th, opex_pv


# Function: PV Power Plants -> Process -> Step 02 -> Download the previous result
def pv2_step_02(currentUser, nutsId, processId, config):
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 02 -> Downloading the result file of the Solar preprocess...')
    logging.info('')
    df_scada_th, df_scada_pv = None, None
    file_path = config['IDESIGNRES-PATH']['idesignres.path.output.tmp'] + currentUser + '/'
    file_name = config['IDESIGNRES-PATH']['idesignres.path.output.default.name'].replace('{1}', processId).replace('{2}', nutsId)
    download = sftp.retrieveSingleFile(file_path, file_name, config)
    logging.info('')
    if download:
        logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 02 -> Loading the thermal data...')
        df_scada_th = pd.read_csv(mio.retrieveFilesTmpPath(config) + '/' + file_name, header = 0, encoding = "ISO-8859-1",
            delimiter = ",", decimal = ".").sort_values(by = 'Median_Radiation', ascending = False)

        logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 02 -> Loading the photovoltaic data...')
        df_scada_pv = pd.read_csv(mio.retrieveFilesTmpPath(config) + '/' + file_name, header = 0, encoding = "ISO-8859-1",
            delimiter = ",", decimal = ".").sort_values(by = 'Median_Radiation', ascending = False)

    # Finish    
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 02 -> [OK]')
    logging.info('')
    return df_scada_th, df_scada_pv


# Function: PV Power Plants -> Process -> Step 03 -> Calculate the available thermal area
def pv2_step_03(list_parameters_th, system_cost, land_use_th):
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Calculating the available thermal area...')
    area_th, power_th, capex_th = get_available_area(
    	parameters = list_parameters_th,
    	cost = system_cost,
    	land_use = land_use_th)
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Area -> ' + str(area_th))
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Power -> ' + str(power_th))
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> Capex -> ' + str(capex_th))
    
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 03 -> [OK]')
    logging.info('')
    return area_th, power_th, capex_th


# Function: PV Power Plants -> Process -> Step 04 -> Calculate the available PV area
def pv2_step_04(list_parameters_pv, system_cost, land_use_pv):
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Calculating the available PV area...')
    area_pv, power_pv, capex_pv = get_available_area(
    	parameters = list_parameters_pv,
    	cost = system_cost,
    	land_use = land_use_pv)
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Area -> ' + str(area_pv))
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Power -> ' + str(power_pv))
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> Capex -> ' + str(capex_pv))
    
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 04 -> [OK]')
    logging.info('')
    return area_pv, power_pv, capex_pv


# Function: PV Power Plants -> Process -> Step 05 -> Thermal production
def pv2_step_05(scada_th, area_th, min_ghi_th, land_use_th, eff_th, eff_op, aperture, t_coord, year):
    # Get the regions
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Obtaining the regions...')
    rows_th, name_nuts2 = get_regions(scada = scada_th, area = area_th, min_ghi = min_ghi_th)
    #logging.info(rows_th)
    
    # Get the thermal production
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Obtaining the thermal production...')
    prod_th = get_thermal_production(rows = rows_th, land_use = land_use_th, eff_th = eff_th,
        eff_op = eff_op, aperture = area_th * aperture, t_coord = t_coord, year = year)
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Saving the thermal production in a DataFrame...')
    df_th = (pd.DataFrame(prod_th).sum(axis = 0))
    
    # Get the distribution
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> Obtaining the distribution...')
    nuts2_th, pot_dist_th, areas_dist_th = get_distribution(rows = rows_th, label = 'thermal_power')
    
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 05 -> [OK]')
    logging.info('')
    return nuts2_th, rows_th, pot_dist_th, df_th


# Function: PV Power Plants -> Process -> Step 06 -> PV production
def pv2_step_06(rows_th, scada_pv, area_pv, min_ghi_pv, land_use_pv, tilt, azimuth, tracking, loss, t_coord, year):
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Removing areas used with thermal power...')
    for region in rows_th:
        df = scada_pv.loc[(scada_pv['Region'] == region['Region']) & (scada_pv['Threshold'] == region['Threshold'])]
        df['Area_m2'] -= region['Area_m2']
        scada_pv.loc[(scada_pv['Region'] == region['Region']) & (scada_pv['Threshold'] == region['Threshold'])] = df
    
    # Get the regions
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Obtaining the regions...')
    rows_pv, name_nuts2 = get_regions(scada = scada_pv, area = area_pv, min_ghi = min_ghi_pv)
    
    # Get the PV production
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Obtaining the PV production...')
    prod_pv = get_pv_production(rows = rows_pv, land_use = land_use_pv, tilt = tilt, azimuth = azimuth,
        tracking = tracking, loss = loss, t_coord = t_coord, year = year)
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Saving the PV production in a DataFrame...')
    df_pv = (pd.DataFrame(prod_pv).sum(axis = 0))
    
    # Get the distribution
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> Obtaining the distribution...')
    nuts2_pv, pot_dist_pv, areas_dist_pv = get_distribution(rows = rows_pv, label = 'pv_power')
    
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 06 -> [OK]')
    logging.info('')
    return name_nuts2, nuts2_pv, pot_dist_pv, df_pv


# Function: PV Power Plants -> Process -> Step 07 -> Calculate the aggregated production
def pv2_step_07(df_th, df_pv, name_nuts2):
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 07 -> Calculating the aggregated production...')
    prod_agreggated = pd.concat([df_th.reset_index(), df_pv.reset_index()], ignore_index = False, axis = 1)
    prod_agreggated = prod_agreggated.drop(columns = ['time'])
    prod_agreggated = prod_agreggated.set_index('time(UTC)')
    prod_agreggated.columns = ['Pthermal_' + str(name_nuts2), 'Ppv_' + str(name_nuts2)]
    prod_agreggated.index = prod_agreggated.index.strftime('%Y-%m-%d %H:%M:%S')
    
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 07 -> [OK]')
    logging.info('')
    return prod_agreggated


# Function: PV Power Plants -> Process -> Step 08 -> Calculate the distribution production
def pv2_step_08(nuts2_th, nuts2_pv):
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 08 -> Calculating the distribution production...')
    nuts2_th = nuts2_th.add_suffix('_Pthermal')
    nuts2_pv = nuts2_pv.add_suffix('_Ppv')
    nuts2_dist = pd.concat([nuts2_th.reset_index(), nuts2_pv.reset_index()], ignore_index = False, axis = 1)
    nuts2_dist = nuts2_dist.drop(columns = ['time'])
    nuts2_dist = nuts2_dist.set_index('time(UTC)')
    
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 08 -> [OK]')
    logging.info('')
    return nuts2_dist


# Function: PV Power Plants -> Process -> Step 09 -> Save the results
def pv2_step_09(prod_agreggated, nuts2_dist, name_nuts2, pot_dist_th, pot_dist_pv, opex_th, opex_pv, config):
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 09 -> Saving the results...')
    outputs = [mio.retrieveOutputBasePath(True, config) + name_nuts2 + '.csv']
    to_csv(prod_agreggated.reset_index(), outputs[0])
    
    names_nuts3 = list(
        dict.fromkeys([nuts2_dist.columns[col].rsplit('_')[0] for col in range(len(nuts2_dist.columns))]))
    
    for i in range(len(names_nuts3)):
        df_nuts3 = pd.DataFrame()
        nuts3_cols = [x for x in nuts2_dist if (x.startswith(names_nuts3[i]))]
        new_nuts3_cols = [item.rsplit('_')[1] for item in nuts3_cols]
        df_nuts3[new_nuts3_cols] = nuts2_dist[nuts3_cols]
        output = mio.retrieveOutputBasePath(True, config) + names_nuts3[i] + '.csv'
        outputs.append(output)
        to_csv(df_nuts3.reset_index(), output)
      
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 09 -> Combining the dictionaries...')
    pot_th = {f'{k}_thermal': v for k, v in pot_dist_th.items()}
    pot_pv = {f'{k}_pv': v for k, v in pot_dist_pv.items()}
    combined_dict = {**pot_th, **pot_pv}
    opex_tot_th, opex_tot_pv = opex_calc(dict_data = combined_dict, opex_th = opex_th, opex_pv = opex_pv)
    combined_dict['opex_thermal'] = opex_tot_th  # In €
    combined_dict['opex_pv'] = opex_tot_pv  # In €
    
    output = mio.retrieveOutputBasePath(True, config) + name_nuts2 + '.json'
    outputs.append(output)
    dict_to_json(combined_dict, Path(output), replace = True)
     
    # Finish
    logging.info('  QGIS Server/> PV Power Plants -> Process -> Step 09 -> [OK]')
    logging.info('')
    return outputs



#####################################################################
######################## Auxiliary functions ########################
#####################################################################


# Auxiliary function: Get coord
def get_coord(df: pd.DataFrame) -> tuple:
    sample_x = df['Median_Radiation_X']
    sample_y = df['Median_Radiation_Y']

    transformer = Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy = True)
    xy = transformer.transform(sample_x, sample_y)
    return xy[0], xy[1]


# Auxiliary function: To CSV
def to_csv(df, filename):
    df.to_csv(filename, index = False, decimal = ',', sep = ';')


# Auxiliary function: Dict to JSON
def dict_to_json(d: Union[dict, list], path: Path, replace: bool = False):
    path = path.with_suffix(".json")
    if replace or not path.is_file():
        with open(path, "w", encoding = "utf-8") as f:
            json.dump(d, f, sort_keys = False, indent = 4)


# Auxiliary function: Thermal model
def thermal_model(radiation: pd.DataFrame, eff_th: float, eff_op: float, aperture: float) -> list:
    return radiation * aperture * eff_th * eff_op / 1000000  # in  MWh


# Auxiliary function: Get available area
def get_available_area(parameters: list, cost: float, land_use: float) -> tuple:
    index = next((i for i, value in enumerate(parameters) if value is not None), -1)
    if index == 2:
        capex = parameters[index]
        power = parameters[index] / (cost * 1000000)  # in MW
        area = power * 1000000 / land_use  # in m2
    elif index == 1:
        area = parameters[index] * 1000000 / land_use  # in m2
        power = parameters[index]
        capex = power * cost * 1000000
    else:
        area = parameters[0]  # en m2
        power = (area * land_use) / 1000000  # in MW
        capex = power * cost * 1000000

    return area, power, capex
    

# Auxiliary function: Get regions
def get_regions(scada: dict, area: float, min_ghi: float) -> tuple:
    current_sum = 0
    name_nuts2 = None
    rows = []
    for index, row in scada.iterrows():
        if name_nuts2 is None:
            name_nuts2 = row['Region'][:-1]
        if row['Area_m2'] > 0 and row['Region'] != name_nuts2 and row['Threshold'] >= min_ghi:
            if current_sum + row['Area_m2'] > area:
                row['Area_m2'] = area - current_sum
                current_sum += row['Area_m2']
                rows.append(row)
                break
            current_sum += row['Area_m2']
            rows.append(row)

    return rows, name_nuts2


# Auxiliary function: Get thermal production
def get_thermal_production(rows: list, land_use: float,
    eff_th: float, eff_op: float, aperture: float, t_coord: bool, year: int) -> list:
    production = []
    for region in rows:
        lon, lat = region['Median_Radiation_X'], region['Median_Radiation_Y']
        if t_coord:
            lon, lat = get_coord(region)

        factor = 1
        data, moths, inputs, metadata = pvlib.iotools.get_pvgis_tmy(
            latitude = lat, longitude = lon, outputformat = 'json',
            usehorizon = True, userhorizon = None, startyear = None,
            endyear = None, map_variables = True,
            timeout = 15)
        
        data.index = data.index.map(lambda x: x.replace(year = year))
        region['radiation'] = data['dni']
        region['temperature'] = data['temp_air']
        pot_MW = (region['Area_m2'] * land_use) / 1000000
        region['power_installed(kW)'] = pot_MW

        region['thermal_power'] = thermal_model(
            radiation = data['dni'], eff_th = eff_th, eff_op = eff_op, aperture = aperture) * factor
        production.append(region['thermal_power'])  # in MWh
    return production


# Auxiliary function: Get PV production
def get_pv_production(rows: list, land_use: float, tilt: float, azimuth: float,
    tracking: int, loss: float, t_coord: bool, year: int) -> list:
    production = []
    for region in rows:
        lon, lat = region['Median_Radiation_X'], region['Median_Radiation_Y']
        if t_coord:
            lon, lat = get_coord(region)

        pot_MW = (region['Area_m2'] * land_use) / 1000000
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
def get_distribution(rows: list, label: str) -> tuple:
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
def opex_calc(dict_data: dict, opex_th: float, opex_pv: float) -> tuple:
    total_th = 0
    total_pv = 0
    for d_key, d_value in dict_data.items():
        if 'pv' in d_key:
            total_pv += d_value
        elif 'thermal' in d_key:
            total_th += d_value
    return total_th * opex_th, total_pv * opex_pv

