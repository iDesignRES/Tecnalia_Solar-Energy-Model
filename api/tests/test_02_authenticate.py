import json
import requests

from api.api import app


TEST_URL = 'http://localhost:5010/api/qgis/authenticate'


# Test 02 (a) -> Missing input parameters
def testMissingInputParameters():
    ''' Test 02 (a) -> Missing input parameters. '''
    
    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)

    # Define the test payloads
    testPayloads = [{key: value} for key, value in authPayload.items()]

    # Call the API function (POST)
    for payload in testPayloads:
        response = requests.post(TEST_URL, json = payload)

        # Check the status code: 400
        assert response.status_code == 400

        # Check the 'value' property
        assert 'value' in response.json() and\
            not response.json()['value'] is None and\
            response.json()['value'] == False


# Test 02 (b) -> Authentication failure
def testtestAuthenticationFailure():
    ''' Test 02 (b) -> Authentication failure. '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)

    # Define the test payloads
    testPayloads = [authPayload.copy() for _ in range(2)]
    testPayloads[0]['username'] = 'wrongusername'
    testPayloads[1]['password'] = 'wrongpassword'

    # Call the API function (POST)
    for payload in testPayloads:
        response = requests.post(TEST_URL, json = payload)

        # Check the status code: 401
        assert response.status_code == 401

        # Check the 'value' property
        assert 'value' in response.json() and\
            not response.json()['value'] is None and\
            response.json()['value'] == False


# Test 02 (c) -> Authentication successful
def testAuthenticationSuccessful():
    ''' Test 02 (c) -> Authentication successful. '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)

    # Call the API function (POST)
    response = requests.post(TEST_URL, json = authPayload)

    # Check the status code: 200
    assert response.status_code == 200

    # Check the 'value' property
    assert 'value' in response.json() and response.json()['value']
