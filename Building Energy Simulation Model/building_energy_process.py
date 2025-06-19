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

import json
import sys
import pandas as pd

from datetime import datetime
from modules import model
from modules import validator
from pathlib import Path


VERSION = 'v0.9.1'
BUILDING_USES = ['Apartment Block',
                 'Single family- Terraced houses',
                 'Hotels and Restaurants',
                 'Health',
                 'Education',
                 'Offices',
                 'Trade',
                 'Other non-residential buildings',
                 'Sport']


# Function: Format the Hourly results
def formatHourlyResults(dictHourlyResults, archetypes):
    '''
    Function to format the Hourly results.
    Input parameters:
        dictHourlyResults: dict -> The dictionary corresponding to he Hourly results.
        archetypes: list -> The list of building uses.
    '''

    formattedOutput = {}
    for arch in archetypes:
        formattedOutput[arch] = []
        df = dictHourlyResults[arch]
        for index, row in df.iterrows():
            datetimeConverted = datetime.strptime(
                row['Datetime'], '%d/%m/%Y %H:%M')
            dictConverted = {
                'Datetime': datetimeConverted.strftime('%Y-%m-%d %H:%M'),
                'Solids|Coal': row['Solids|Coal'],
                'Liquids|Gas': row['Liquids|Gas'],
                'Liquids|Oil': row['Liquids|Oil'],
                'Gases|Gas': row['Gases|Gas'],
                'Solids|Biomass': row['Solids|Biomass'],
                'Electricity': row['Electricity'],
                'Heat': row['Heat'],
                'Liquids|Biomass': row['Liquids|Biomass'],
                'Gases|Biomass': row['Gases|Biomass'],
                'Hydrogen': row['Hydrogen'],
                'Heat|Solar': row['Heat|Solar'],
                'Variable cost [€/KWh]': row['Variable cost [€/KWh]'],
                'Emissions [KgCO2/KWh]': row['Emissions [kgCO2/KWh]']
            }
            formattedOutput[arch].append(dictConverted)
    return formattedOutput


# Function: Execute the Model
def executeModel(modelPayload: dict):
    '''
    Function to execute the Buildings Stock Energy Model.
    Input parameters:
        modelPayload: dict -> The dictionary with the Model input payload.
    '''

    print('Main/>  Executing the Buildings Stock Energy Model (please wait)...')
    print('')
    dfCsv = model.executeModelStep01(modelPayload['nutsid'].strip())
    print('')
    tempsPath = model.executeModelStep02(
        modelPayload['nutsid'].strip(), modelPayload['year'])
    print('')
    radPath = model.executeModelStep03(
        modelPayload['nutsid'].strip(), modelPayload['year'])
    print('')
    if tempsPath is None or radPath is None:
        raise ValueError(
            'Main/>  There is no data on radiation and/or temperatures!')
    dfDHW, dfYears, dfSectors, dfSeasons, \
        dfTemperatures, dfSchedule, dfResHHTes, \
        dfSerHHTes, dfUvalues, dfRetroUvalues, \
        dfACH, dfBaseTemperatures, dfCalendar, \
        dfBesCapex, dfBesOpex, dfRes, dfBesCapacity, \
        dfRetroCost, dfSolarOffice, dfSolarNoffice, \
        dfDwellings, dfRTHHEff = model.executeModelStep04(modelPayload['nutsid'].strip(),
                                                          modelPayload['scenario']['hdd_reduction'],
                                                          modelPayload['scenario']['cdd_reduction'])
    print('')
    dfInput = model.executeModelStep05(dfCsv)
    print('')
    dfInput = model.executeModelStep06(dfCsv,
                                       dfDHW,
                                       dfYears,
                                       dfSectors,
                                       dfDwellings,
                                       modelPayload['nutsid'].strip(),
                                       modelPayload['scenario']['increase_residential_built_area'],
                                       modelPayload['scenario']['increase_service_built_area'])
    del dfYears, dfSectors, dfDwellings
    print('')
    dfInput = model.executeModelStep07(dfCsv,
                                       dfResHHTes,
                                       dfSerHHTes,
                                       dfRTHHEff,
                                       modelPayload['nutsid'].strip(),
                                       modelPayload['scenario']['active_measures'],
                                       modelPayload['scenario']['active_measures_baseline'],
                                       BUILDING_USES)
    del dfResHHTes, dfSerHHTes, dfRTHHEff
    print('')
    dfInput = model.executeModelStep08(
        dfCsv, modelPayload['scenario']['passive_measures'])
    print('')
    dfInput = model.executeModelStep09(dfCsv,
                                       dfDHW,
                                       dfUvalues,
                                       dfRetroUvalues,
                                       dfACH,
                                       modelPayload['nutsid'].strip())
    del dfDHW, dfUvalues, dfRetroUvalues, dfACH
    print('')
    dfInput = model.executeModelStep10(dfInput, dfBesCapex)
    del dfBesCapex
    print('')
    dfInput = model.executeModelStep11(dfInput, dfBesOpex)
    del dfBesOpex
    print('')
    dfInput = model.executeModelStep12(dfInput, dfRetroCost)
    del dfRetroCost
    print('')
    dfInput = model.executeModelStep13(dfInput, dfRes)
    del dfRes
    print('')
    dfInput = model.executeModelStep14(dfInput, dfBesCapacity, BUILDING_USES)
    del dfBesCapacity
    print('')
    dfInput = model.executeModelStep15(dfInput)
    print('')
    dfInput = model.executeModelStep16(dfInput)
    print('')
    dictSchedule = model.executeModelStep17(dfInput,
                                            dfSchedule,
                                            dfTemperatures,
                                            dfBaseTemperatures,
                                            dfSolarOffice,
                                            dfSolarNoffice,
                                            modelPayload['nutsid'].strip())
    del dfTemperatures, dfBaseTemperatures, dfSolarOffice, dfSolarNoffice
    print('')
    dictSchedule = model.executeModelStep18(dfInput, dictSchedule)
    print('')
    dfAnualResults = model.executeModelStep19(dfInput, dictSchedule)
    print('')
    dictConsolidated = {}
    for arch in BUILDING_USES:
        dictConsolidated[arch] = model.executeModelStep20(dictSchedule, arch)
    print('')
    dictHourlyResults = {}
    for arch in BUILDING_USES:
        dictHourlyResults[arch] = model.executeModelStep21(
            dfInput, dictSchedule, arch)
    del dictSchedule
    print('')
    return formatHourlyResults(dictHourlyResults, BUILDING_USES)


# Function: Execute the Building Energy Simulation process
def executeBuildingEnergySimulationProcess(processPayload: dict, startTime: str, endTime: str, buildingUse: str):
    '''
    Function to execute the Building Energy Simulation process.
    Input parameters:
        processPayload: dict -> The dictionary with the process input payload.
        startTime: text -> The start datetime.
        endTime: text -> The end datetime.
        buildingUse: text -> The archetype (building use).
    '''

    try:
        # Execute the Model
        print(
            'Main/>  *** Building Energy Simulation process [version ' + VERSION + '] ***')
        output = executeModel(processPayload)

        # Remove all the temporary files
        print('Main/>  Removing all the temporary files...')
        directory = Path(__file__).parent / 'temporary'
        for fileInDirectory in directory.iterdir():
            if fileInDirectory.is_file():
                fileInDirectory.unlink()

        # Return the result (filtered)
        result = pd.DataFrame(output[buildingUse])
        result['Datetime'] = pd.to_datetime(result['Datetime'])
        start = pd.to_datetime(datetime.strptime(
            startTime, '%Y-%m-%dT%H:%M:%S'))
        end = pd.to_datetime(datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S'))
        resultFiltered = result[(result['Datetime'] >= start) & (
            result['Datetime'] <= end)]
        print('Main/>  [OK]')
        return resultFiltered.to_dict(orient='list')
    except Exception as error:
        print('Main/>  An error occurred executing the Building Energy Simulation process!')
        print(error)


# Function: Main
def main():
    '''
    Main function.
    Input parameters:
        sys.argv[0]: text -> The current file name.
        sys.argv[1]: text -> The process input data file path.
        sys.argv[2]: text -> The start datetime.
        sys.argv[3]: text -> The end datetime.
        sys.argv[4]: text -> The archetype (building use).
    '''

    try:
        # Validate the command line parameters
        validator.validateCommandLineParameters(sys.argv)

        # Load the process payload
        print('Main/>  Loading the process payload...')
        with open(sys.argv[1].strip(), 'r') as payloadFile:
            processPayload = json.load(payloadFile)

        # Validate the process payload
        processPayload = validator.validateProcessPayload(processPayload)
        print('Main/>  Input data validation OK!...')

        # Execute the process
        print('Main/>  Loading the Model...')
        executeBuildingEnergySimulationProcess(
            processPayload, sys.argv[2], sys.argv[3], sys.argv[4])
    except Exception as exception:
        print(f'{exception}')


if __name__ == "__main__":
    main()
