import json
import requests

from api.api import app


TEST_URL_AUTH = 'http://localhost:5010/api/qgis/authenticate'
TEST_URL_PROCESS = 'http://localhost:5010/api/qgis/pv-power-plants-process'


# Test 03 (a) -> Missing input parameters
def testMissingInputParameters():
    ''' Test 03 (a) -> Missing input parameters. '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)
    
    # Call the API function (POST) to authenticate
    response = requests.post(TEST_URL_AUTH, json = authPayload)

    # Check the authentication status code: 200
    assert response.status_code == 200

    # Check the 'value' property, and define the headers for the process
    assert 'value' in response.json() and response.json()['value']
    headers = {'Authorization': 'Bearer ' + response.json()['value'],
               'Content-Type': 'application/json' }
    
    # Load the process payload
    with open('api/tests/payloads/pv_payload.json', 'r') as payloadFile:
        processPayload = json.load(payloadFile)

    # Define the test payloads
    testPayloads = [{key: value} for key, value in processPayload.items()]

    # Call the API function (POST) to execute the process
    for payload in testPayloads:
        response = requests.post(TEST_URL_PROCESS, json = payload, headers = headers)

        # Check the status code: 400
        assert response.status_code == 400

        # Check the 'value' property
        assert 'value' in response.json() and\
            not response.json()['value'] is None and\
            response.json()['value'] == False


# Test 03 (b) -> Wrong values in input parameters
def testWrongValuesInInputParameters():
    ''' Test 03 (b) -> Wrong values in input parameters. '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)
    
    # Call the API function (POST) to authenticate
    response = requests.post(TEST_URL_AUTH, json = authPayload)

    # Check the authentication status code: 200
    assert response.status_code == 200

    # Check the 'value' property, and define the headers for the process
    assert 'value' in response.json() and response.json()['value']
    headers = {'Authorization': 'Bearer ' + response.json()['value'],
               'Content-Type': 'application/json' }
    
    # Load the process payload
    with open('api/tests/payloads/pv_payload.json', 'r') as payloadFile:
        processPayload = json.load(payloadFile)

    # Define the test payloads
    testPayloads = [processPayload.copy() for _ in range(2)]
    testPayloads[0]['nutsid'] = 'ES70'
    testPayloads[1]['slope_angle'] = 370

    # Call the API function (POST) to execute the process
    for payload in testPayloads:
        response = requests.post(TEST_URL_PROCESS, json = payload, headers = headers)

        # Check the status code: 400
        assert response.status_code == 400

        # Check the 'value' property
        assert 'value' in response.json() and\
            not response.json()['value'] is None and\
            response.json()['value'] == False


# Test 03 (c) -> Process successful
def testProcessSuccessful():
    ''' Test 03 (c) -> Process successful. '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)
    
    # Call the API function (POST) to authenticate
    response = requests.post(TEST_URL_AUTH, json = authPayload)

    # Check the authentication status code: 200
    assert response.status_code == 200

    # Check the 'value' property, and define the headers for the process
    assert 'value' in response.json() and response.json()['value']
    headers = {'Authorization': 'Bearer ' + response.json()['value'],
               'Content-Type': 'application/json' }
    
    # Load the process payload
    with open('api/tests/payloads/pv_payload.json', 'r') as payloadFile:
        processPayload = json.load(payloadFile)

    # Call the API function (POST) to execute the process
    response = requests.post(TEST_URL_PROCESS, json = processPayload, headers = headers)

    # Check the status code: 200
    assert response.status_code == 200

    # Check the 'value' property
    assert 'value' in response.json() and response.json()['value']
