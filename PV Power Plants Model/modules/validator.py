# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (c) 2025 Tecnalia Research & Innovation

import os
from datetime import datetime


REGIONS = 'AL01,AL02,AL03,AT11,AT12,AT13,AT21,AT22,AT31,AT32,AT33,AT34,' \
          'BE10,BE21,BE22,BE23,BE24,BE25,BE31,BE32,BE33,BE34,BE35,BG31,' \
          'BG32,BG33,BG34,BG41,BG42,CH01,CH02,CH03,CH04,CH05,CH06,CH07,' \
          'CY00,CZ01,CZ02,CZ03,CZ04,CZ05,CZ06,CZ07,CZ08,DE11,DE12,DE13,' \
          'DE14,DE21,DE22,DE23,DE24,DE25,DE26,DE27,DE30,DE40,DE50,DE60,' \
          'DE71,DE72,DE73,DE80,DE91,DE92,DE93,DE94,DEA1,DEA2,DEA3,DEA4,' \
          'DEA5,DEB1,DEB2,DEB3,DEC0,DED2,DED4,DED5,DEE0,DEF0,DEG0,DK01,' \
          'DK02,DK03,DK04,DK05,EE00,EL30,EL41,EL42,EL43,EL51,EL52,EL53,' \
          'EL54,EL61,EL62,EL63,EL64,EL65,ES11,ES12,ES13,ES21,ES22,ES23,' \
          'ES24,ES30,ES41,ES42,ES43,ES51,ES52,ES53,ES61,ES62,ES63,ES64,' \
          'FI19,FI1B,FI1C,FI1D,FI20,FR10,FRB0,FRC1,FRC2,FRD1,FRD2,FRE1,' \
          'FRE2,FRF1,FRF2,FRF3,FRG0,FRH0,FRI1,FRI2,FRI3,FRJ1,FRJ2,FRK1,' \
          'FRK2,FRL0,FRM0,HR02,HR03,HR05,HR06,HU11,HU12,HU21,HU22,HU23,' \
          'HU31,HU32,HU33,IE04,IE05,IE06,IS00,ITC1,ITC2,ITC3,ITC4,ITF1,' \
          'ITF2,ITF3,ITF4,ITF5,ITF6,ITG1,ITG2,ITH1,ITH2,ITH3,ITH4,ITH5,' \
          'ITI1,ITI2,ITI3,ITI4,LI00,LT01,LT02,LU00,LV00,ME00,MK00,MT00,' \
          'NL11,NL12,NL13,NL21,NL22,NL23,NL32,NL34,NL35,NL36,NL41,NL42,' \
          'NO02,NO06,NO07,NO08,NO09,NO0A,NO0B,PL21,PL22,PL41,PL42,PL43,' \
          'PL51,PL52,PL61,PL62,PL63,PL71,PL72,PL81,PL82,PL84,PL91,PL92,' \
          'PT11,PT15,PT19,PT1A,PT1B,PT1C,PT1D,PT20,PT30,RO11,RO12,RO21,' \
          'RO22,RO31,RO32,RO41,RO42,RS11,RS12,RS21,RS22,SE11,SE12,SE21,' \
          'SE22,SE23,SE31,SE32,SE33,SI03,SI04,SK01,SK02,SK03,SK04,TR10,' \
          'TR21,TR22,TR31,TR32,TR33,TR41,TR42,TR51,TR52,TR61,TR62,TR63,' \
          'TR71,TR72,TR81,TR82,TR83,TR90,TRA1,TRA2,TRB1,TRB2,TRC1,TRC2,' \
          'TRC3,UA11,UA12,UA13,UA14,UA21,UA22,UA31,UA32,UA33,UA41,UA42,' \
          'UA43,UA44,UA45,UA51,UA52,UA53,UA61,UA62,UA63,UA71,UA72,UA73,' \
          'UA74,UA81,UA82,UA83,XK00'
REGION_LIST = [region.strip() for region in REGIONS.split(',')]


# Function: Validate the limits of a given value
def validateLimits(value, limitDown, limitUp):
    '''
    Function to check the limits of a given value.
    Input parameters:
        value: number -> The value of the property to be evaluated.
        limitDown: integer -> The lower limit.
        limitUp: integer -> The highest limit.
    '''

    return True if limitDown <= value <= limitUp else False


# Function: Validate the command line parameters
def validateCommandLineParameters(parameters):
    '''
    Funtion to validate the command line parameters.
    Input parameters:
        parameters: list -> The list of command line parameters.
    '''

    # Validate the parameters
    if len(parameters) != 4:
        raise Exception(
            'Validator/>  The number of input parameters is incorrect! (4)')

    # Validate if the payload file exists
    if not os.path.exists(parameters[1].strip()):
        raise Exception(
            'Validator/>  The process input data file does not exist!')

    # Validate the datetime objects
    try:
        datetime.strptime(parameters[2], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise Exception(
            'Validator/>  The third input parameter (start datetime) has an incorrect format (yyyy-MM-ddTHH:mm:ss)')
    try:
        datetime.strptime(parameters[3], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise Exception(
            'Validator/>  The fourth input parameter (end datetime) has an incorrect format (yyyy-MM-ddTHH:mm:ss)')
    if (parameters[3] <= parameters[2]):
        raise Exception(
            'Validator/>  The end time cannot be less than the start time!')


# Function: Validate the process payload
def validateProcessPayload(payload):
    '''
    Funtion to validate the process payload.
    Input parameters:
        payload: dict -> The process payload.
    '''

    # Validate the full object
    if not payload or payload is None:
        raise Exception('Validator/>  Could not load the process payload!')

    # Validate the property: nutsid
    if not 'nutsid' in payload or payload['nutsid'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "nutsid"')
    if payload['nutsid'].strip().upper() not in REGION_LIST:
        raise Exception(
            'Validator/>  The following property has an invalid value: "nutsid"')

    # Validate the property: slope_angle
    if not 'slope_angle' in payload or payload['slope_angle'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "slope_angle"')
    if not validateLimits(payload['slope_angle'], 0, 360):
        print('Validator/>  The following property has an invalid value (0 - 360): "slope_angle"')
        print('Validator/>  Its default value will be applied -> 0')
        payload['slope_angle'] = 0

    # Validate the property: area_total_thermal
    if not 'area_total_thermal' in payload:
        raise Exception(
            'Validator/>  The following property is not present: "area_total_thermal"')
    if payload['area_total_thermal'] is not None and not validateLimits(payload['area_total_thermal'], 0, 10 ** 10):
        print('Validator/>  The following property has an invalid value (0 - 10e10): "area_total_thermal"')
        print('Validator/>  Its default value will be applied -> 0')
        payload['area_total_thermal'] = 0

    # Validate the property: power_thermal
    if not 'power_thermal' in payload:
        raise Exception(
            'Validator/>  The following property is not present: "power_thermal"')
    if payload['power_thermal'] is not None and not validateLimits(payload['power_thermal'], 0, 10 ** 12):
        print('Validator/>  The following property has an invalid value (0 - 10e12): "power_thermal"')
        print('Validator/>  Its default value will be applied -> 0')
        payload['power_thermal'] = 0

    # Validate the property: capex_thermal
    if not 'capex_thermal' in payload:
        raise Exception(
            'Validator/>  The following property is not present: "capex_thermal"')
    if payload['capex_thermal'] is not None and not validateLimits(payload['capex_thermal'], 0, 5 * (10 ** 11)):
        print('Validator/>  The following property has an invalid value (0 - 5 * 10e11): "capex_thermal"')
        print('Validator/>  Its default value will be applied -> 0')
        payload['capex_thermal'] = 0

    # Validate the combination of properties: area_total_thermal, power_thermal and capex_thermal
    if payload['area_total_thermal'] is None and payload['power_thermal'] is None and payload['capex_thermal'] is None:
        payload['area_total_thermal'] = 0
        payload['power_thermal'] = None
        payload['capex_thermal'] = None
        print('Validator/>  The following properties are null: "area_total_thermal", "power_thermal" and "capex_thermal"')
        print(
            'Validator/>  The default value for "area_total_thermal" will be applied -> 0')

    # Validate the property: area_total_pv
    if not 'area_total_pv' in payload:
        raise Exception(
            'Validator/>  The following property is not present: "area_total_pv"')
    if payload['area_total_pv'] is not None and not validateLimits(payload['area_total_pv'], 0, 10 ** 10):
        print('Validator/>  The following property has an invalid value (0 - 10e10): "area_total_pv"')
        print('Validator/>  Its default value will be applied -> 0')
        payload['area_total_pv'] = 0

    # Validate the property: power_pv
    if not 'power_pv' in payload:
        raise Exception(
            'Validator/>  The following property is not present: "power_pv"')
    if payload['power_pv'] is not None and not validateLimits(payload['power_pv'], 0, 10 ** 12):
        print('Validator/>  The following property has an invalid value (0 - 10e12): "power_pv"')
        print('Validator/>  Its default value will be applied -> 0')
        payload['power_pv'] = 0

    # Validate the property: capex_pv
    if not 'capex_pv' in payload:
        raise Exception(
            'Validator/>  The following property is not present: "capex_pv"')
    if payload['capex_pv'] is not None and not validateLimits(payload['capex_pv'], 0, 5 * (10 ** 11)):
        print('Validator/>  The following property has an invalid value (0 - 5 * 10e11): "capex_pv"')
        print('Validator/>  Its default value will be applied -> 0')
        payload['capex_pv'] = 0

    # Validate the combination of properties: area_total_pv, power_pv and capex_pv
    if payload['area_total_pv'] is None and payload['power_pv'] is None and payload['capex_pv'] is None:
        payload['area_total_pv'] = 0
        payload['power_pv'] = None
        payload['capex_pv'] = None
        print('Validator/>  The following properties are null: "area_total_pv", "power_pv" and "capex_pv"')
        print('Validator/>  The default value for "area_total_pv" will be applied -> 0')

    # Validate the property: system_cost_thermal
    if not 'system_cost_thermal' in payload or payload['system_cost_thermal'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "system_cost_thermal"')
    if not validateLimits(payload['system_cost_thermal'], 1, 10):
        print('Validator/>  The following property has an invalid value (1 - 10): "system_cost_thermal"')
        print('Validator/>  Its default value will be applied -> 0')
        payload['system_cost_thermal'] = 0

    # Validate the property: system_cost_pv
    if not 'system_cost_pv' in payload or payload['system_cost_pv'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "system_cost_pv"')
    if not validateLimits(payload['system_cost_pv'], 0.2, 1):
        print('Validator/>  The following property has an invalid value (0.2 - 1): "system_cost_pv"')
        print('Validator/>  Its default value will be applied -> 0.5')
        payload['system_cost_pv'] = 0.5

    # Validate the property: loss
    if not 'loss' in payload or payload['loss'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "loss"')
    if not validateLimits(payload['loss'], 8, 20):
        print('Validator/>  The following property has an invalid value (8 - 20): "loss"')
        print('Validator/>  Its default value will be applied -> 14')
        payload['loss'] = 14

    # Validate the property: efficiency_thermal
    if not 'efficiency_thermal' in payload or payload['efficiency_thermal'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "efficiency_thermal"')
    if not validateLimits(payload['efficiency_thermal'], 25, 65):
        print('Validator/>  The following property has an invalid value (25 - 65): "efficiency_thermal"')
        print('Validator/>  Its default value will be applied -> 45')
        payload['efficiency_thermal'] = 45

    # Validate the property: efficiency_optical
    if not 'efficiency_optical' in payload or payload['efficiency_optical'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "efficiency_optical"')
    if not validateLimits(payload['efficiency_optical'], 45, 85):
        print('Validator/>  The following property has an invalid value (45 - 85): "efficiency_optical"')
        print('Validator/>  Its default value will be applied -> 65')
        payload['efficiency_optical'] = 65

    # Validate the property: aperture
    if not 'aperture' in payload or payload['aperture'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "aperture"')
    if not validateLimits(payload['aperture'], 25, 75):
        print(
            'Validator/>  The following property has an invalid value (25 - 75): "aperture"')
        print('Validator/>  Its default value will be applied -> 50')
        payload['aperture'] = 50

    # Validate the property: tilt
    if not 'tilt' in payload or payload['tilt'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "tilt"')
    if not validateLimits(payload['tilt'], 0, 90):
        print('Validator/>  The following property has an invalid value (0 - 90): "tilt"')
        print('Validator/>  Its default value will be applied -> 30')
        payload['tilt'] = 30

    # Validate the property: azimuth
    if not 'azimuth' in payload or payload['azimuth'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "azimuth"')
    if not validateLimits(payload['azimuth'], 0, 360):
        print(
            'Validator/>  The following property has an invalid value (0 - 360): "azimuth"')
        print('Validator/>  Its default value will be applied -> 180')
        payload['azimuth'] = 180

    # Validate the property: tracking_percentage
    if not 'tracking_percentage' in payload or payload['tracking_percentage'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "tracking_percentage"')
    if not validateLimits(payload['tracking_percentage'], 0, 100):
        print('Validator/>  The following property has an invalid value (0 - 100): "tracking_percentage"')
        print('Validator/>  Its default value will be applied -> 60')
        payload['tracking_percentage'] = 60

    # Validate the property: opex_thermal
    if not 'opex_thermal' in payload or payload['opex_thermal'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "opex_thermal"')
    if not validateLimits(payload['opex_thermal'], 0, 40000):
        print('Validator/>  The following property has an invalid value (0 - 40000): "opex_thermal"')
        print('Validator/>  Its default value will be applied -> 20000')
        payload['opex_thermal'] = 20000

    # Validate the property: opex_pv
    if not 'opex_pv' in payload or payload['opex_pv'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "opex_pv"')
    if not validateLimits(payload['opex_pv'], 0, 30000):
        print('Validator/>  The following property has an invalid value (0 - 30000): "opex_pv"')
        print('Validator/>  Its default value will be applied -> 15000')
        payload['opex_pv'] = 15000

    # Validate the property: min_ghi_thermal
    if not 'min_ghi_thermal' in payload or payload['min_ghi_thermal'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "min_ghi_thermal"')
    if not validateLimits(payload['min_ghi_thermal'], 1500, 2500):
        print('Validator/>  The following property has an invalid value (1500 - 2500): "min_ghi_thermal"')
        print('Validator/>  Its default value will be applied -> 2000')
        payload['min_ghi_thermal'] = 2000

    # Validate the property: min_ghi_pv
    if not 'min_ghi_pv' in payload or payload['min_ghi_pv'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "min_ghi_pv"')
    if not validateLimits(payload['min_ghi_pv'], 500, 2000):
        print('Validator/>  The following property has an invalid value (500 - 2000): "min_ghi_pv"')
        print('Validator/>  Its default value will be applied -> 1000')
        payload['min_ghi_pv'] = 1000

    # Validate the property: land_use_thermal
    if not 'land_use_thermal' in payload or payload['land_use_thermal'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "land_use_thermal"')
    if not validateLimits(payload['land_use_thermal'], 25, 100):
        print('Validator/>  The following property has an invalid value (25 - 100): "land_use_thermal"')
        print('Validator/>  Its default value will be applied -> 50')
        payload['land_use_thermal'] = 50

    # Validate the property: land_use_pv
    if not 'land_use_pv' in payload or payload['land_use_pv'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "land_use_pv"')
    if not validateLimits(payload['land_use_pv'], 50, 200):
        print('Validator/>  The following property has an invalid value (50 - 200): "land_use_pv"')
        print('Validator/>  Its default value will be applied -> 100')
        payload['land_use_pv'] = 100

    # Validate the property: convert_coord
    if not 'convert_coord' in payload or payload['convert_coord'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "convert_coord"')
    if int(payload['convert_coord']) not in [0, 1]:
        raise Exception(
            'Validator/>  The following property has an invalid value (0, 1): "convert_coord"')

    # Validate the property: pvgis_year
    if not 'pvgis_year' in payload or payload['pvgis_year'] is None:
        raise Exception(
            'Validator/>  The following property is not present or has a null value: "pvgis_year"')
    if not validateLimits(int(payload['pvgis_year']), 1900, 2020):
        raise Exception(
            'Validator/>  The following property has an invalid value (1900 - 2020): "pvgis_year"')

    # If no exception occurred, return the modified payload
    return payload
