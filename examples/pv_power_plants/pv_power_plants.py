import json
import os
import requests
import sys


URL_AUTH = 'https://idesignres.digital.tecnalia.dev/api/qgis/authenticate'
URL_PROCESS  = 'https://idesignres.digital.tecnalia.dev/api/qgis/pv-power-plants-process'


# Function: Execute the PV Power Plants process
def executePVPowerPlantsProcess(processPayloadFilePath):
    ''' Function to execute the PV Power Plants process. '''

    try:
        # Load the authentication payload
        with open('auth.json', 'r') as payloadFile:
            authPayload = json.load(payloadFile)
        if not authPayload or authPayload is None:
            raise Exception('Process/>  Could not load the authentication payload!')
        
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

            # Load the process payload
            with open(processPayloadFilePath, 'r') as payloadFile:
                processPayload = json.load(payloadFile)
            if not processPayload or processPayload is None:
                raise Exception('Process/>  Could not load the process payload!')

            # Execute the process
            print('Process/>  Executing the PV Power Plants process (please wait)...')
            response = requests.post(URL_PROCESS, json = processPayload, headers = headers)
            if response.status_code != 200:
                raise Exception('Process/>  An error occurred executing the PV Power Plants process!')
            print('Process/>  [Process OK]')
            print(response.text)
    except Exception as error:
        print('Process/>  An error occurred executing the PV Power Plants process!')
        print(error)
    

# Function: Main
def main():
    ''' Main function '''

    # Read input parameters:
    # [0]: file name
    # [1]: input data file path
    if len(sys.argv) > 1:
        if not os.path.exists(sys.argv[1].strip()):
            print('Process/>  The input data file does not exist!')
        else:
            executePVPowerPlantsProcess(sys.argv[1].strip())
    else:
        print('Process/>  No input parameters were provided!')


if __name__ == "__main__":
    main()
