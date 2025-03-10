import configparser
import json
import requests

# Create the config objects and read .ini and .properties files
config = configparser.ConfigParser()
config.read('config/config.ini')


# Function: Execute the PV Power Plants process
def executePVPowerPlantsProcess():
    ''' Function to execute the PV Power Plants process. '''

    try:
        # Load the authentication payload
        with open('payloads/auth_payload.json', 'r') as payloadFile:
            authPayload = json.load(payloadFile)
        if not authPayload or authPayload is None:
            raise Exception('Process/>  Could not load the authentication payload!')
        
        # Authenticate
        print('Process/>  Authenticating...')
        response = requests.post(config['URL']['url.auth'], json = authPayload)
        if response.status_code != 200:
            raise Exception('Process/>  Authentication error!')
        print('Process/>  Authentication [OK]')

        # Obtain the security token from the response
        token = response.json()['value']
        if token:
            # Load the process headers
            with open('headers/pv_headers.json', 'r') as headersFile:
                headers = json.load(headersFile)
            if not headers or headers is None or not headers['Authorization'] or headers['Authorization'] is None:
                raise Exception('Process/>  Could not load the process headers!')
            headers['Authorization'] = headers['Authorization'].replace('{1}', token)

            # Load the process payload
            with open('payloads/pv_payload.json', 'r') as payloadFile:
                processPayload = json.load(payloadFile)
            if not processPayload or processPayload is None:
                raise Exception('Process/>  Could not load the process payload!')

            # Execute the process
            print('Process/>  Executing the PV Power Plants process (please wait)...')
            response = requests.post(config['URL']['url.pv'], json = processPayload, headers = headers)
            if response.status_code != 200:
                raise Exception('Process/>  An error occurred executing the PV Power Plants process!')
            print('Process/>  [Process OK]')
    except Exception as error:
        print(error)
    

# Function: Main
def main():
    ''' Main function '''

    executePVPowerPlantsProcess()


if __name__ == "__main__":
    main()
