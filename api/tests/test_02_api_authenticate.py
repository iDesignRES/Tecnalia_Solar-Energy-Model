import json
import logging
import pytest

from flask import current_app, request
from api.api import app


@pytest.fixture
def client():
    '''
    Define the test_client.
    Input parameters:
        None.
    '''

    with app.app_context():
        yield app.test_client()


# Test 02 (a) -> Missing input parameters
def testMissingInputParameters(client, caplog):
    '''
    Test 02 (a) -> Missing input parameters.
    Input parameters:
        client: object -> The PyTest client object.
        caplog: object -> The PyTest object to capture the logs.
    '''
    
    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)

    # Define the test payloads
    testPayloads = [{key: value} for key, value in authPayload.items()]

    # Call the API function (POST)
    for payload in testPayloads:
        response = client.post('/api/qgis/authenticate',
                               data = json.dumps(payload),
                               content_type = 'application/json')

        # Check the status code: 400
        assert response.status_code == 400

        # Check the 'value' property
        assert 'value' in response.get_json() and\
            not response.get_json()['value'] is None and\
            response.get_json()['value'] == False


# Test 02 (b) -> Authentication failure
def testAuthenticationFailure(client, caplog):
    '''
    Test 02 (b) -> Authentication failure.
    Input parameters:
        client: object -> The PyTest client object.
        caplog: object -> The PyTest object to capture the logs.
    '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)

    # Define the test payloads
    testPayloads = [authPayload.copy() for _ in range(2)]
    testPayloads[0]['username'] = 'wrongusername'
    testPayloads[1]['password'] = 'wrongpassword'

    # Call the API function (POST)
    for payload in testPayloads:
        response = client.post('/api/qgis/authenticate',
                               data = json.dumps(payload),
                               content_type = 'application/json')

        # Check the status code: 401
        assert response.status_code == 401

        # Check the 'value' property
        assert 'value' in response.get_json() and\
            not response.get_json()['value'] is None and\
            response.get_json()['value'] == False


# Test 02 (c) -> Authentication successful
def testAuthenticationSuccessful(client, caplog):
    '''
    Test 02 (c) -> Authentication successful.
    Input parameters:
        client: object -> The PyTest client object.
        caplog: object -> The PyTest object to capture the logs.
    '''

    # Load the authentication payload
    with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
        authPayload = json.load(payloadFile)

    # Call the API function (POST)
    response = client.post('/api/qgis/authenticate',
                           data = json.dumps(authPayload),
                           content_type = 'application/json')

    # Check the status code: 200
    assert response.status_code == 200

    # Check the 'value' property
    assert 'value' in response.get_json() and response.get_json()['value']
