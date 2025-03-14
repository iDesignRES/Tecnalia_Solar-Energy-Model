import json
import logging
import pytest

from flask import current_app, request
from api.api import app


@pytest.fixture
def client():
    ''' Define the test_client '''

    with app.app_context():
        yield app.test_client()


# Test 03 (a) -> Missing input parameters
def testMissingInputParameters(client, caplog):
    ''' Test 03 (a) -> Missing input parameters. '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)
        
    # Call the API function (POST) to authenticate
    response = client.post('/api/qgis/authenticate',
                           data = json.dumps(authPayload),
                           content_type = 'application/json')

    # Check the authentication status code: 200
    assert response.status_code == 200

    # Check the 'value' property, and define the headers for the process
    assert 'value' in response.get_json() and response.get_json()['value']
    headers = {'Authorization': 'Bearer ' + response.get_json()['value']}
        
    # Load the process payload
    with open('api/tests/payloads/pv_payload.json', 'r') as payloadFile:
        processPayload = json.load(payloadFile)

    # Define the test payloads
    testPayloads = [{key: value} for key, value in processPayload.items()]

    # Call the API function (POST) to execute the process
    for payload in testPayloads:
        response = client.post('/api/qgis/pv-power-plants-process', 
                           data = json.dumps(payload),
                           content_type = 'application/json',
                           headers = headers)

        # Check the status code: 400
        assert response.status_code == 400

        # Check the 'value' property
        assert 'value' in response.get_json() and\
            not response.get_json()['value'] is None and\
            response.get_json()['value'] == False


# Test 03 (b) -> Wrong values in input parameters
def testWrongValuesInInputParameters(client, caplog):
    ''' Test 03 (b) -> Wrong values in input parameters. '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)
           
    # Call the API function (POST) to authenticate
    response = client.post('/api/qgis/authenticate',
                           data = json.dumps(authPayload),
                           content_type = 'application/json')

    # Check the authentication status code: 200
    assert response.status_code == 200

    # Check the 'value' property, and define the headers for the process
    assert 'value' in response.get_json() and response.get_json()['value']
    headers = {'Authorization': 'Bearer ' + response.get_json()['value']}
            
    # Load the process payload
    with open('api/tests/payloads/pv_payload.json', 'r') as payloadFile:
        processPayload = json.load(payloadFile)

    # Define the test payloads
    testPayloads = [processPayload.copy() for _ in range(2)]
    testPayloads[0]['nutsid'] = 'ES70'
    testPayloads[1]['slope_angle'] = 370

    # Call the API function (POST) to execute the process
    for payload in testPayloads:
        response = client.post('/api/qgis/pv-power-plants-process',
                                data = json.dumps(payload),
                                content_type = 'application/json',
                                headers = headers)

        # Check the status code: 400
        assert response.status_code == 400

        # Check the 'value' property
        assert 'value' in response.get_json() and\
            not response.get_json()['value'] is None and\
            response.get_json()['value'] == False


# Test 03 (c) -> Process successful
def testProcessSuccessful(client, caplog):
    ''' Test 03 (c) -> Process successful. '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)
        
    # Call the API function (POST) to authenticate
    response = client.post('/api/qgis/authenticate',
                           data = json.dumps(authPayload),
                           content_type = 'application/json')

    # Check the authentication status code: 200
    assert response.status_code == 200

    # Check the 'value' property, and define the headers for the process
    assert 'value' in response.get_json() and response.get_json()['value']
    headers = {'Authorization': 'Bearer ' + response.get_json()['value']}
        
    # Load the process payload
    with open('api/tests/payloads/pv_payload.json', 'r') as payloadFile:
        processPayload = json.load(payloadFile)

    # Call the API function (POST) to execute the process
    response = client.post('/api/qgis/pv-power-plants-process',
                            data = json.dumps(processPayload),
                            content_type = 'application/json',
                             headers = headers)

    # Check the status code: 200
    assert response.status_code == 200

    # Check the 'value' property
    assert 'value' in response.get_json() and response.get_json()['value']
