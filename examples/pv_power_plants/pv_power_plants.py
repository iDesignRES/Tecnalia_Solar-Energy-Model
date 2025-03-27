import json
import os
import requests
import sys

import pandas as pd
import numpy as np

from datetime import datetime


URL_AUTH = 'https://idesignres.digital.tecnalia.dev/api/qgis/authenticate'
URL_PROCESS  = 'https://idesignres.digital.tecnalia.dev/api/qgis/pv-power-plants-process'


# Function: Execute the PV Power Plants process
def executePVPowerPlantsProcess(authPayload: dict, processPayload: dict, startTime: str, endTime: str):
    '''
    Function to execute the PV Power Plants process.
    Input parameters:
        authPayload: dict -> The dictionary with the authorization payload.
        processPayload: dict -> The dictionary with the process input payload.
        startTime: text -> The start datetime.
        endTime: text -> The end datetime.
    '''

    try:
        # Authenticate
        print('Process/>  Authenticating...')
        response = requests.post(URL_AUTH, json = authPayload)
        if response.status_code != 200:
            raise Exception('Process/>  Authentication error!')
        print('Process/>  Authentication [OK]')

        # Obtain the security token from the response
        token = response.json()['value']
        if token:
            headers = {'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json',
                        'X-Julia': 'True'
            }

            # Execute the process
            print('Process/>  Executing the PV Power Plants process (please wait)...')
            response = requests.post(URL_PROCESS, json = processPayload, headers = headers)
            if response.status_code != 200:
                raise Exception()
            print('Process/>  [Process OK]')

            # Return the result (filtered)
            data = pd.DataFrame(response.json())
            data['time(UTC)'] = pd.to_datetime(data['time(UTC)'])
            start = pd.to_datetime(datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S'))
            end = pd.to_datetime(datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S'))
            dataFiltered = data[(data['time(UTC)'] >= start) & (data['time(UTC)'] <= end)].copy()
            dataFiltered['Ppv'] = dataFiltered['Ppv'].apply(lambda x: float(x.replace(',', '.')))
            dataFiltered['Pthermal'] = dataFiltered['Pthermal'].apply(lambda x: float(x.replace(',', '.')))
            return dataFiltered.to_dict(orient = 'list')
    except Exception as error:
        print('Process/>  An error occurred executing the PV Power Plants process!')
        print(error)
    

# Function: Main
def main():
    '''
    Main function.
    Input parameters:
        sys.argv[0]: text -> The client file name.
        sys.argv[1]: text -> The authorization file path.
        sys.argv[2]: text -> The process input data file path.
        sys.argv[3]: text -> The start datetime.
        sys.argv[4]: text -> The end datetime.
    '''

    try:
        # Read input parameters:
        if len(sys.argv) < 5:
            raise Exception('The number of input parameters is incorrect! (5)')
        if not os.path.exists(sys.argv[1].strip()):
            raise Exception('The authorization file does not exist!')
        if not os.path.exists(sys.argv[2].strip()):
            raise Exception('The input data file does not exist!')
        
        # Load the authorization payload
        with open(sys.argv[1].strip(), 'r') as authPayloadFile:
            authPayload = json.load(authPayloadFile)
        if not authPayload or authPayload is None:
            raise Exception('Could not load the authorization payload!')

        # Load the process payload
        with open(sys.argv[2].strip(), 'r') as payloadFile:
            processPayload = json.load(payloadFile)
        if not processPayload or processPayload is None:
            raise Exception('Could not load the process payload!')
        
        # Validate the datetime objects
        try:
            startTime = datetime.strptime(sys.argv[3], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise Exception('The third input parameter (start datetime) has an incorrect format (yyyy-MM-ddTHH:mm:ss)')
        try:
            endTime = datetime.strptime(sys.argv[4], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise Exception('The fourth input parameter (end datetime) has an incorrect format (yyyy-MM-ddTHH:mm:ss)')
        if (endTime <= startTime):
            raise Exception('The end time cannot be less than the start time!')

        # Execute the processs
        executePVPowerPlantsProcess(authPayload, processPayload, sys.argv[3], sys.argv[4])
    except Exception as exception:
        print(f'Process/>  {exception}') 
    
    

if __name__ == "__main__":
    main()
