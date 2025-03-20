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
    testPayloads = [processPayload.copy() for _ in range(25)]
    del testPayloads[0]['nutsid']
    del testPayloads[1]['slope_angle']
    del testPayloads[2]['area_total_thermal']
    del testPayloads[3]['area_total_pv']
    del testPayloads[4]['power_thermal']
    del testPayloads[5]['power_pv']
    del testPayloads[6]['capex_thermal']
    del testPayloads[7]['capex_pv']
    del testPayloads[8]['tilt']
    del testPayloads[9]['azimuth']
    del testPayloads[10]['loss']
    del testPayloads[11]['tracking_percentage']
    del testPayloads[12]['efficiency_thermal']
    del testPayloads[13]['efficiency_optical']
    del testPayloads[14]['aperture']
    del testPayloads[15]['system_cost_thermal']
    del testPayloads[16]['system_cost_pv']
    del testPayloads[17]['opex_thermal']
    del testPayloads[18]['opex_pv']
    del testPayloads[19]['min_ghi_thermal']
    del testPayloads[20]['min_ghi_pv']
    del testPayloads[21]['land_use_thermal']
    del testPayloads[22]['land_use_pv']
    del testPayloads[23]['convert_coord']
    del testPayloads[24]['pvgis_year']

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
    testPayloads = [processPayload.copy() for _ in range(25)]
    testPayloads[0]['nutsid'] = 'ES70'
    testPayloads[1]['slope_angle'] = 370
    testPayloads[2]['area_total_thermal'] = -1
    testPayloads[3]['area_total_pv'] = -1
    testPayloads[4]['power_thermal'] = -1
    testPayloads[5]['power_pv'] = -1
    testPayloads[6]['capex_thermal'] = -1
    testPayloads[7]['capex_pv'] = -1
    testPayloads[8]['tilt'] = 100
    testPayloads[9]['azimuth'] = 400
    testPayloads[10]['loss'] = 4
    testPayloads[11]['tracking_percentage'] = 200
    testPayloads[12]['efficiency_thermal'] = 20
    testPayloads[13]['efficiency_optical'] = 40
    testPayloads[14]['aperture'] = 10
    testPayloads[15]['system_cost_thermal'] = 20
    testPayloads[16]['system_cost_pv'] = 4
    testPayloads[17]['opex_thermal'] = -1
    testPayloads[18]['opex_pv'] = -1
    testPayloads[19]['min_ghi_thermal'] = 3000
    testPayloads[20]['min_ghi_pv'] = 4000
    testPayloads[21]['land_use_thermal'] = 10
    testPayloads[22]['land_use_pv'] = 10
    testPayloads[23]['convert_coord'] = -1
    testPayloads[24]['pvgis_year'] = 1700

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
