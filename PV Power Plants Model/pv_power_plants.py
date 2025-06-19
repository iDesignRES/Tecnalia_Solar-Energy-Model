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
import pandas as pd
import sys

from datetime import datetime
from modules import model
from modules import validator


VERSION = 'v0.9.1'


# Function: Execute the Model
def executeModel(modelPayload: dict):
    '''
    Function to execute the PV Power Plants Model.
    Input parameters:
        modelPayload: dict -> The dictionary with the Model input payload.
    '''

    print('Main/>  Executing the PV Power Plants Model (please wait)...')
    print('')
    listParametersTH, listParametersPV, systemCostTH, systemCostPV, \
        landUseTH, landUsePV, minGhiTH, minGhiPV, effTH, effOp, aperture, \
        convertCoord, year, tilt, azimuth, tracking, loss, opexTH, opexPV = model.executeModelStep01(
            modelPayload)
    print('')
    scadaTH, scadaPV = model.executeModelStep02(modelPayload['nutsid'])
    print('')
    areaTH, powerTH, capexTH = model.executeModelStep03(
        listParametersTH, systemCostTH, landUseTH)
    print('')
    areaPV, powerPV, capexPV = model.executeModelStep04(
        listParametersPV, systemCostPV, landUsePV)
    print('')
    nuts2TH, rowsTH, potDistTH, dfTH, scadaPV = model.executeModelStep05(scadaTH, scadaPV, areaTH, minGhiTH, landUseTH,
                                                                         effTH, effOp, aperture, convertCoord, year)
    print('')
    nameNuts2, nuts2PV, potDistPV, dfPV = model.executeModelStep06(scadaPV, areaPV, minGhiPV, landUsePV, tilt,
                                                                   azimuth, tracking, loss, convertCoord, year)
    print('')
    prodAggregated = model.executeModelStep07(dfTH, dfPV, nameNuts2)
    print('')
    nuts2Distrib = model.executeModelStep08(dfTH, nuts2TH, nuts2PV)
    print('')
    output = model.executeModelStep09(prodAggregated, nuts2Distrib, dfTH,
                                      potDistTH, potDistPV, opexTH, opexPV)
    print('')
    print('Main/>  [OK]')
    return output


# Function: Execute the PV Power Plants process
def executePVPowerPlantsProcess(processPayload: dict, startTime: str, endTime: str):
    '''
    Function to execute the PV Power Plants process.
    Input parameters:
        processPayload: dict -> The dictionary with the process input payload.
        startTime: str -> The start datetime.
        endTime: str -> The end datetime.
    '''

    try:
        # Execute the Model
        print(
            'Main/>  *** PV Power Plants process [version ' + VERSION + '] ***')
        output = executeModel(processPayload)

        # Return the result (filtered)
        result = output[0]
        result['time(UTC)'] = pd.to_datetime(result['time(UTC)'])
        start = pd.to_datetime(datetime.strptime(
            startTime, '%Y-%m-%dT%H:%M:%S'))
        end = pd.to_datetime(datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S'))
        resultFiltered = result[(result['time(UTC)'] >= start) & (
            result['time(UTC)'] <= end)].copy()
        resultFiltered['Ppv'] = resultFiltered['Ppv'].apply(
            lambda x: float(str(x).replace(',', '.')))
        resultFiltered['Pthermal'] = resultFiltered['Pthermal'].apply(
            lambda x: float(str(x).replace(',', '.')))
        return resultFiltered.to_dict(orient='list')
    except Exception as error:
        print('Main/>  An error occurred executing the PV Power Plants process!')
        print(error)


# Function: Main
def main():
    '''
    Main function.
    Input parameters:
        sys.argv[0]: str -> The current file name.
        sys.argv[1]: str -> The process input data file path.
        sys.argv[2]: str -> The start datetime.
        sys.argv[3]: str -> The end datetime.
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
        executePVPowerPlantsProcess(processPayload, sys.argv[2], sys.argv[3])
    except Exception as exception:
        print(f'{exception}')


if __name__ == "__main__":
    main()
