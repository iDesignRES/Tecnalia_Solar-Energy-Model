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


# Test 04 (a) -> Missing input parameters
def testMissingInputParameters(client, caplog):
    '''
    Test 04 (a) -> Missing input parameters.
    Input parameters:
        client: object -> The PyTest client object.
        caplog: object -> The PyTest object to capture the logs.
    '''

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
    with open('api/tests/payloads/bes_payload.json', 'r') as payloadFile:
        processPayload = json.load(payloadFile)

    # Define the test payloads
    testPayloads = [processPayload.copy() for _ in range(997)]
    del testPayloads[0]['nutsid']
    del testPayloads[1]['year']
    del testPayloads[2]['scenario']['increase_residential_built_area']
    del testPayloads[3]['scenario']['increase_service_built_area']
    del testPayloads[4]['scenario']['hdd_reduction']
    del testPayloads[5]['scenario']['cdd_reduction']
    index = 6
    for i in range(9):
        del testPayloads[index]['scenario']['passive_measures'][i]['building_use']
        del testPayloads[index + 1]['scenario']['passive_measures'][i]['ref_level']
        del testPayloads[index + 2]['scenario']['passive_measures'][i]['percentages_by_periods']['Pre-1945']
        del testPayloads[index + 3]['scenario']['passive_measures'][i]['percentages_by_periods']['1945-1969']
        del testPayloads[index + 4]['scenario']['passive_measures'][i]['percentages_by_periods']['1970-1979']
        del testPayloads[index + 5]['scenario']['passive_measures'][i]['percentages_by_periods']['1980-1989']
        del testPayloads[index + 6]['scenario']['passive_measures'][i]['percentages_by_periods']['1990-1999']
        del testPayloads[index + 7]['scenario']['passive_measures'][i]['percentages_by_periods']['2000-2010']
        del testPayloads[index + 8]['scenario']['passive_measures'][i]['percentages_by_periods']['Post-2010']
        del testPayloads[index + 9]['scenario']['passive_measures'][i]['percentages_by_periods']
        index += 10
    # index = 6 + (9 * 10) = 96
    for i in range(9):
        del testPayloads[index]['scenario']['active_measures'][i]['building_use']
        del testPayloads[index + 1]['scenario']['active_measures'][i]['user_defined_data']
        del testPayloads[index + 2]['scenario']['active_measures'][i]['space_heating']['pct_build_equipped']
        del testPayloads[index + 3]['scenario']['active_measures'][i]['space_heating']['solids']
        del testPayloads[index + 4]['scenario']['active_measures'][i]['space_heating']['lpg']
        del testPayloads[index + 5]['scenario']['active_measures'][i]['space_heating']['diesel_oil']
        del testPayloads[index + 6]['scenario']['active_measures'][i]['space_heating']['gas_heat_pumps']
        del testPayloads[index + 7]['scenario']['active_measures'][i]['space_heating']['natural_gas']
        del testPayloads[index + 8]['scenario']['active_measures'][i]['space_heating']['biomass']
        del testPayloads[index + 9]['scenario']['active_measures'][i]['space_heating']['geothermal']
        del testPayloads[index + 10]['scenario']['active_measures'][i]['space_heating']['distributed_heat']
        del testPayloads[index + 11]['scenario']['active_measures'][i]['space_heating']['advanced_electric_heating']
        del testPayloads[index + 12]['scenario']['active_measures'][i]['space_heating']['conventional_electric_heating']
        del testPayloads[index + 13]['scenario']['active_measures'][i]['space_heating']['bio_oil']
        del testPayloads[index + 14]['scenario']['active_measures'][i]['space_heating']['bio_gas']
        del testPayloads[index + 15]['scenario']['active_measures'][i]['space_heating']['hydrogen']
        del testPayloads[index + 16]['scenario']['active_measures'][i]['space_heating']['electricity_in_circulation']
        del testPayloads[index + 17]['scenario']['active_measures'][i]['space_cooling']['pct_build_equipped']
        del testPayloads[index + 18]['scenario']['active_measures'][i]['space_cooling']['gas_heat_pumps']
        del testPayloads[index + 19]['scenario']['active_measures'][i]['space_cooling']['electric_space_cooling']
        del testPayloads[index + 20]['scenario']['active_measures'][i]['water_heating']['pct_build_equipped']
        del testPayloads[index + 21]['scenario']['active_measures'][i]['water_heating']['solids']
        del testPayloads[index + 22]['scenario']['active_measures'][i]['water_heating']['lpg']
        del testPayloads[index + 23]['scenario']['active_measures'][i]['water_heating']['diesel_oil']
        del testPayloads[index + 24]['scenario']['active_measures'][i]['water_heating']['natural_gas']
        del testPayloads[index + 25]['scenario']['active_measures'][i]['water_heating']['biomass']
        del testPayloads[index + 26]['scenario']['active_measures'][i]['water_heating']['geothermal']
        del testPayloads[index + 27]['scenario']['active_measures'][i]['water_heating']['distributed_heat']
        del testPayloads[index + 28]['scenario']['active_measures'][i]['water_heating']['advanced_electric_heating']
        del testPayloads[index + 29]['scenario']['active_measures'][i]['water_heating']['bio_oil']
        del testPayloads[index + 30]['scenario']['active_measures'][i]['water_heating']['bio_gas']
        del testPayloads[index + 31]['scenario']['active_measures'][i]['water_heating']['hydrogen']
        del testPayloads[index + 32]['scenario']['active_measures'][i]['water_heating']['solar']
        del testPayloads[index + 33]['scenario']['active_measures'][i]['water_heating']['electricity']
        del testPayloads[index + 34]['scenario']['active_measures'][i]['cooking']['pct_build_equipped']
        del testPayloads[index + 35]['scenario']['active_measures'][i]['cooking']['solids']
        del testPayloads[index + 36]['scenario']['active_measures'][i]['cooking']['lpg']
        del testPayloads[index + 37]['scenario']['active_measures'][i]['cooking']['natural_gas']
        del testPayloads[index + 39]['scenario']['active_measures'][i]['cooking']['biomass']
        del testPayloads[index + 40]['scenario']['active_measures'][i]['cooking']['electricity']
        del testPayloads[index + 41]['scenario']['active_measures'][i]['lighting']['pct_build_equipped']
        del testPayloads[index + 42]['scenario']['active_measures'][i]['lighting']['electricity']
        del testPayloads[index + 43]['scenario']['active_measures'][i]['appliances']['pct_build_equipped']
        del testPayloads[index + 44]['scenario']['active_measures'][i]['appliances']['electricity']
        del testPayloads[index + 45]['scenario']['active_measures'][i]['space_heating']
        del testPayloads[index + 46]['scenario']['active_measures'][i]['space_cooling']
        del testPayloads[index + 47]['scenario']['active_measures'][i]['water_heating']
        del testPayloads[index + 48]['scenario']['active_measures'][i]['cooking']
        del testPayloads[index + 49]['scenario']['active_measures'][i]['lighting']
        del testPayloads[index + 50]['scenario']['active_measures'][i]['appliances']
        index += 50
    # index = 96 + (9 * 50) = 546
    for i in range(9):
        del testPayloads[index]['scenario']['active_measures_baseline'][i]['building_use']
        del testPayloads[index + 1]['scenario']['active_measures_baseline'][i]['user_defined_data']
        del testPayloads[index + 2]['scenario']['active_measures_baseline'][i]['space_heating']['pct_build_equipped']
        del testPayloads[index + 3]['scenario']['active_measures_baseline'][i]['space_heating']['solids']
        del testPayloads[index + 4]['scenario']['active_measures_baseline'][i]['space_heating']['lpg']
        del testPayloads[index + 5]['scenario']['active_measures_baseline'][i]['space_heating']['diesel_oil']
        del testPayloads[index + 6]['scenario']['active_measures_baseline'][i]['space_heating']['gas_heat_pumps']
        del testPayloads[index + 7]['scenario']['active_measures_baseline'][i]['space_heating']['natural_gas']
        del testPayloads[index + 8]['scenario']['active_measures_baseline'][i]['space_heating']['biomass']
        del testPayloads[index + 9]['scenario']['active_measures_baseline'][i]['space_heating']['geothermal']
        del testPayloads[index + 10]['scenario']['active_measures_baseline'][i]['space_heating']['distributed_heat']
        del testPayloads[index + 11]['scenario']['active_measures_baseline'][i]['space_heating']['advanced_electric_heating']
        del testPayloads[index + 12]['scenario']['active_measures_baseline'][i]['space_heating']['conventional_electric_heating']
        del testPayloads[index + 13]['scenario']['active_measures_baseline'][i]['space_heating']['bio_oil']
        del testPayloads[index + 14]['scenario']['active_measures_baseline'][i]['space_heating']['bio_gas']
        del testPayloads[index + 15]['scenario']['active_measures_baseline'][i]['space_heating']['hydrogen']
        del testPayloads[index + 16]['scenario']['active_measures_baseline'][i]['space_heating']['electricity_in_circulation']
        del testPayloads[index + 17]['scenario']['active_measures_baseline'][i]['space_cooling']['pct_build_equipped']
        del testPayloads[index + 18]['scenario']['active_measures_baseline'][i]['space_cooling']['gas_heat_pumps']
        del testPayloads[index + 19]['scenario']['active_measures_baseline'][i]['space_cooling']['electric_space_cooling']
        del testPayloads[index + 20]['scenario']['active_measures_baseline'][i]['water_heating']['pct_build_equipped']
        del testPayloads[index + 21]['scenario']['active_measures_baseline'][i]['water_heating']['solids']
        del testPayloads[index + 22]['scenario']['active_measures_baseline'][i]['water_heating']['lpg']
        del testPayloads[index + 23]['scenario']['active_measures_baseline'][i]['water_heating']['diesel_oil']
        del testPayloads[index + 24]['scenario']['active_measures_baseline'][i]['water_heating']['natural_gas']
        del testPayloads[index + 25]['scenario']['active_measures_baseline'][i]['water_heating']['biomass']
        del testPayloads[index + 26]['scenario']['active_measures_baseline'][i]['water_heating']['geothermal']
        del testPayloads[index + 27]['scenario']['active_measures_baseline'][i]['water_heating']['distributed_heat']
        del testPayloads[index + 28]['scenario']['active_measures_baseline'][i]['water_heating']['advanced_electric_heating']
        del testPayloads[index + 29]['scenario']['active_measures_baseline'][i]['water_heating']['bio_oil']
        del testPayloads[index + 30]['scenario']['active_measures_baseline'][i]['water_heating']['bio_gas']
        del testPayloads[index + 31]['scenario']['active_measures_baseline'][i]['water_heating']['hydrogen']
        del testPayloads[index + 32]['scenario']['active_measures_baseline'][i]['water_heating']['solar']
        del testPayloads[index + 33]['scenario']['active_measures_baseline'][i]['water_heating']['electricity']
        del testPayloads[index + 34]['scenario']['active_measures_baseline'][i]['cooking']['pct_build_equipped']
        del testPayloads[index + 35]['scenario']['active_measures_baseline'][i]['cooking']['solids']
        del testPayloads[index + 36]['scenario']['active_measures_baseline'][i]['cooking']['lpg']
        del testPayloads[index + 37]['scenario']['active_measures_baseline'][i]['cooking']['natural_gas']
        del testPayloads[index + 39]['scenario']['active_measures_baseline'][i]['cooking']['biomass']
        del testPayloads[index + 40]['scenario']['active_measures_baseline'][i]['cooking']['electricity']
        del testPayloads[index + 41]['scenario']['active_measures_baseline'][i]['lighting']['pct_build_equipped']
        del testPayloads[index + 42]['scenario']['active_measures_baseline'][i]['lighting']['electricity']
        del testPayloads[index + 43]['scenario']['active_measures_baseline'][i]['appliances']['pct_build_equipped']
        del testPayloads[index + 44]['scenario']['active_measures_baseline'][i]['appliances']['electricity']
        del testPayloads[index + 45]['scenario']['active_measures_baseline'][i]['space_heating']
        del testPayloads[index + 46]['scenario']['active_measures_baseline'][i]['space_cooling']
        del testPayloads[index + 47]['scenario']['active_measures_baseline'][i]['water_heating']
        del testPayloads[index + 48]['scenario']['active_measures_baseline'][i]['cooking']
        del testPayloads[index + 49]['scenario']['active_measures_baseline'][i]['lighting']
        del testPayloads[index + 50]['scenario']['active_measures_baseline'][i]['appliances']
        index += 50
    # index = 546 + (9 * 50) = 996

    # Call the API function (POST) to execute the process
    for payload in testPayloads:
        response = client.post('/api/qgis/building-energy-simulation-process', 
                                data = json.dumps(payload),
                                content_type = 'application/json',
                                headers = headers)

        # Check the status code: 400
        assert response.status_code == 400

        # Check the 'value' property
        assert 'value' in response.get_json() and\
            not response.get_json()['value'] is None and\
            response.get_json()['value'] == False


# Test 04 (b) -> Wrong values in input parameters
def testWrongValuesInInputParameters(client, caplog):
    '''
    Test 04 (b) -> Wrong values in input parameters.
    Input parameters:
        client: object -> The PyTest client object.
        caplog: object -> The PyTest object to capture the logs.
    '''

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
    with open('api/tests/payloads/bes_payload.json', 'r') as payloadFile:
        processPayload = json.load(payloadFile)

    testPayloads = [processPayload.copy() for _ in range(997)]
    testPayloads[0]['nutsid'] = 'ES70'
    testPayloads[1]['year'] = 1970
    testPayloads[2]['scenario']['increase_residential_built_area'] = -0.4
    testPayloads[3]['scenario']['increase_service_built_area'] = 1.16
    testPayloads[4]['scenario']['hdd_reduction'] = -1
    testPayloads[5]['scenario']['cdd_reduction'] = 1.3
    index = 6
    for i in range(9):
        testPayloads[index]['scenario']['passive_measures'][i]['building_use'] = 'XXX'
        testPayloads[index + 1]['scenario']['passive_measures'][i]['ref_level'] = 'Avg'
        testPayloads[index + 2]['scenario']['passive_measures'][i]['percentages_by_periods']['Pre-1945'] = -1
        testPayloads[index + 3]['scenario']['passive_measures'][i]['percentages_by_periods']['1945-1969'] = 1.5
        testPayloads[index + 4]['scenario']['passive_measures'][i]['percentages_by_periods']['1970-1979'] = 1.5
        testPayloads[index + 5]['scenario']['passive_measures'][i]['percentages_by_periods']['1980-1989'] = 1.5
        testPayloads[index + 6]['scenario']['passive_measures'][i]['percentages_by_periods']['1990-1999'] = 1.5
        testPayloads[index + 7]['scenario']['passive_measures'][i]['percentages_by_periods']['2000-2010'] = 1.5
        testPayloads[index + 8]['scenario']['passive_measures'][i]['percentages_by_periods']['Post-2010'] = 1.5
        testPayloads[index + 9]['scenario']['passive_measures'][i]['percentages_by_periods'] = 1.5
        index += 10
    # index = 6 + (9 * 10) = 96
    for i in range(9):
        testPayloads[index]['scenario']['active_measures'][i]['building_use'] = 'XXX'
        testPayloads[index + 1]['scenario']['active_measures'][i]['user_defined_data'] = None
        testPayloads[index + 2]['scenario']['active_measures'][i]['space_heating']['pct_build_equipped'] = 1.4
        testPayloads[index + 3]['scenario']['active_measures'][i]['space_heating']['solids'] = 1.4
        testPayloads[index + 4]['scenario']['active_measures'][i]['space_heating']['lpg'] = 1.4
        testPayloads[index + 5]['scenario']['active_measures'][i]['space_heating']['diesel_oil'] = 1.4
        testPayloads[index + 6]['scenario']['active_measures'][i]['space_heating']['gas_heat_pumps'] = 1.4
        testPayloads[index + 7]['scenario']['active_measures'][i]['space_heating']['natural_gas'] = 1.4
        testPayloads[index + 8]['scenario']['active_measures'][i]['space_heating']['biomass'] = 1.4
        testPayloads[index + 9]['scenario']['active_measures'][i]['space_heating']['geothermal'] = 1.4
        testPayloads[index + 10]['scenario']['active_measures'][i]['space_heating']['distributed_heat'] = 1.4
        testPayloads[index + 11]['scenario']['active_measures'][i]['space_heating']['advanced_electric_heating'] = 1.4
        testPayloads[index + 12]['scenario']['active_measures'][i]['space_heating']['conventional_electric_heating'] = 1.4
        testPayloads[index + 13]['scenario']['active_measures'][i]['space_heating']['bio_oil'] = 1.4
        testPayloads[index + 14]['scenario']['active_measures'][i]['space_heating']['bio_gas'] = 1.4
        testPayloads[index + 15]['scenario']['active_measures'][i]['space_heating']['hydrogen'] = 1.4
        testPayloads[index + 16]['scenario']['active_measures'][i]['space_heating']['electricity_in_circulation'] = 1.4
        testPayloads[index + 17]['scenario']['active_measures'][i]['space_cooling']['pct_build_equipped'] = 1.4
        testPayloads[index + 18]['scenario']['active_measures'][i]['space_cooling']['gas_heat_pumps'] = 1.4
        testPayloads[index + 19]['scenario']['active_measures'][i]['space_cooling']['electric_space_cooling'] = 1.4
        testPayloads[index + 20]['scenario']['active_measures'][i]['water_heating']['pct_build_equipped'] = 1.4
        testPayloads[index + 21]['scenario']['active_measures'][i]['water_heating']['solids'] = 1.4
        testPayloads[index + 22]['scenario']['active_measures'][i]['water_heating']['lpg'] = 1.4
        testPayloads[index + 23]['scenario']['active_measures'][i]['water_heating']['diesel_oil'] = 1.4
        testPayloads[index + 24]['scenario']['active_measures'][i]['water_heating']['natural_gas'] = 1.4
        testPayloads[index + 25]['scenario']['active_measures'][i]['water_heating']['biomass']
        testPayloads[index + 26]['scenario']['active_measures'][i]['water_heating']['geothermal'] = 1.4
        testPayloads[index + 27]['scenario']['active_measures'][i]['water_heating']['distributed_heat'] = 1.4
        testPayloads[index + 28]['scenario']['active_measures'][i]['water_heating']['advanced_electric_heating'] = 1.4
        testPayloads[index + 29]['scenario']['active_measures'][i]['water_heating']['bio_oil'] = 1.4
        testPayloads[index + 30]['scenario']['active_measures'][i]['water_heating']['bio_gas'] = 1.4
        testPayloads[index + 31]['scenario']['active_measures'][i]['water_heating']['hydrogen'] = 1.4
        testPayloads[index + 32]['scenario']['active_measures'][i]['water_heating']['solar'] = 1.4
        testPayloads[index + 33]['scenario']['active_measures'][i]['water_heating']['electricity'] = 1.4
        testPayloads[index + 34]['scenario']['active_measures'][i]['cooking']['pct_build_equipped'] = 1.4
        testPayloads[index + 35]['scenario']['active_measures'][i]['cooking']['solids'] = 1.4
        testPayloads[index + 36]['scenario']['active_measures'][i]['cooking']['lpg'] = 1.4
        testPayloads[index + 37]['scenario']['active_measures'][i]['cooking']['natural_gas'] = 1.4
        testPayloads[index + 39]['scenario']['active_measures'][i]['cooking']['biomass'] = 1.4
        testPayloads[index + 40]['scenario']['active_measures'][i]['cooking']['electricity'] = 1.4
        testPayloads[index + 41]['scenario']['active_measures'][i]['lighting']['pct_build_equipped'] = 1.4
        testPayloads[index + 42]['scenario']['active_measures'][i]['lighting']['electricity'] = 1.4
        testPayloads[index + 43]['scenario']['active_measures'][i]['appliances']['pct_build_equipped'] = 1.4
        testPayloads[index + 44]['scenario']['active_measures'][i]['appliances']['electricity'] = 1.4
        testPayloads[index + 45]['scenario']['active_measures'][i]['space_heating'] = 1.4
        testPayloads[index + 46]['scenario']['active_measures'][i]['space_cooling'] = 1.4
        testPayloads[index + 47]['scenario']['active_measures'][i]['water_heating'] = 1.4
        testPayloads[index + 48]['scenario']['active_measures'][i]['cooking'] = 1.4
        testPayloads[index + 49]['scenario']['active_measures'][i]['lighting'] = 1.4
        testPayloads[index + 50]['scenario']['active_measures'][i]['appliances'] = 1.4
        index += 50
    # index = 96 + (9 * 50) = 546
    for i in range(9):
        testPayloads[index]['scenario']['active_measures_baseline'][i]['building_use'] = 'XXX'
        testPayloads[index + 1]['scenario']['active_measures_baseline'][i]['user_defined_data'] = None
        testPayloads[index + 2]['scenario']['active_measures_baseline'][i]['space_heating']['pct_build_equipped'] = 1.4
        testPayloads[index + 3]['scenario']['active_measures_baseline'][i]['space_heating']['solids'] = 1.4
        testPayloads[index + 4]['scenario']['active_measures_baseline'][i]['space_heating']['lpg'] = 1.4
        testPayloads[index + 5]['scenario']['active_measures_baseline'][i]['space_heating']['diesel_oil'] = 1.4
        testPayloads[index + 6]['scenario']['active_measures_baseline'][i]['space_heating']['gas_heat_pumps'] = 1.4
        testPayloads[index + 7]['scenario']['active_measures_baseline'][i]['space_heating']['natural_gas'] = 1.4
        testPayloads[index + 8]['scenario']['active_measures_baseline'][i]['space_heating']['biomass'] = 1.4
        testPayloads[index + 9]['scenario']['active_measures_baseline'][i]['space_heating']['geothermal'] = 1.4
        testPayloads[index + 10]['scenario']['active_measures_baseline'][i]['space_heating']['distributed_heat'] = 1.4
        testPayloads[index + 11]['scenario']['active_measures_baseline'][i]['space_heating']['advanced_electric_heating'] = 1.4
        testPayloads[index + 12]['scenario']['active_measures_baseline'][i]['space_heating']['conventional_electric_heating'] = 1.4
        testPayloads[index + 13]['scenario']['active_measures_baseline'][i]['space_heating']['bio_oil'] = 1.4
        testPayloads[index + 14]['scenario']['active_measures_baseline'][i]['space_heating']['bio_gas'] = 1.4
        testPayloads[index + 15]['scenario']['active_measures_baseline'][i]['space_heating']['hydrogen'] = 1.4
        testPayloads[index + 16]['scenario']['active_measures_baseline'][i]['space_heating']['electricity_in_circulation'] = 1.4
        testPayloads[index + 17]['scenario']['active_measures_baseline'][i]['space_cooling']['pct_build_equipped'] = 1.4
        testPayloads[index + 18]['scenario']['active_measures_baseline'][i]['space_cooling']['gas_heat_pumps'] = 1.4
        testPayloads[index + 19]['scenario']['active_measures_baseline'][i]['space_cooling']['electric_space_cooling'] = 1.4
        testPayloads[index + 20]['scenario']['active_measures_baseline'][i]['water_heating']['pct_build_equipped'] = 1.4
        testPayloads[index + 21]['scenario']['active_measures_baseline'][i]['water_heating']['solids'] = 1.4
        testPayloads[index + 22]['scenario']['active_measures_baseline'][i]['water_heating']['lpg'] = 1.4
        testPayloads[index + 23]['scenario']['active_measures_baseline'][i]['water_heating']['diesel_oil'] = 1.4
        testPayloads[index + 24]['scenario']['active_measures_baseline'][i]['water_heating']['natural_gas'] = 1.4
        testPayloads[index + 25]['scenario']['active_measures_baseline'][i]['water_heating']['biomass']
        testPayloads[index + 26]['scenario']['active_measures_baseline'][i]['water_heating']['geothermal'] = 1.4
        testPayloads[index + 27]['scenario']['active_measures_baseline'][i]['water_heating']['distributed_heat'] = 1.4
        testPayloads[index + 28]['scenario']['active_measures_baseline'][i]['water_heating']['advanced_electric_heating'] = 1.4
        testPayloads[index + 29]['scenario']['active_measures_baseline'][i]['water_heating']['bio_oil'] = 1.4
        testPayloads[index + 30]['scenario']['active_measures_baseline'][i]['water_heating']['bio_gas'] = 1.4
        testPayloads[index + 31]['scenario']['active_measures_baseline'][i]['water_heating']['hydrogen'] = 1.4
        testPayloads[index + 32]['scenario']['active_measures_baseline'][i]['water_heating']['solar'] = 1.4
        testPayloads[index + 33]['scenario']['active_measures_baseline'][i]['water_heating']['electricity'] = 1.4
        testPayloads[index + 34]['scenario']['active_measures_baseline'][i]['cooking']['pct_build_equipped'] = 1.4
        testPayloads[index + 35]['scenario']['active_measures_baseline'][i]['cooking']['solids'] = 1.4
        testPayloads[index + 36]['scenario']['active_measures_baseline'][i]['cooking']['lpg'] = 1.4
        testPayloads[index + 37]['scenario']['active_measures_baseline'][i]['cooking']['natural_gas'] = 1.4
        testPayloads[index + 39]['scenario']['active_measures_baseline'][i]['cooking']['biomass'] = 1.4
        testPayloads[index + 40]['scenario']['active_measures_baseline'][i]['cooking']['electricity'] = 1.4
        testPayloads[index + 41]['scenario']['active_measures_baseline'][i]['lighting']['pct_build_equipped'] = 1.4
        testPayloads[index + 42]['scenario']['active_measures_baseline'][i]['lighting']['electricity'] = 1.4
        testPayloads[index + 43]['scenario']['active_measures_baseline'][i]['appliances']['pct_build_equipped'] = 1.4
        testPayloads[index + 44]['scenario']['active_measures_baseline'][i]['appliances']['electricity'] = 1.4
        testPayloads[index + 45]['scenario']['active_measures_baseline'][i]['space_heating'] = 1.4
        testPayloads[index + 46]['scenario']['active_measures_baseline'][i]['space_cooling'] = 1.4
        testPayloads[index + 47]['scenario']['active_measures_baseline'][i]['water_heating'] = 1.4
        testPayloads[index + 48]['scenario']['active_measures_baseline'][i]['cooking'] = 1.4
        testPayloads[index + 49]['scenario']['active_measures_baseline'][i]['lighting'] = 1.4
        testPayloads[index + 50]['scenario']['active_measures_baseline'][i]['appliances'] = 1.4
        index += 50
    # index = 546 + (9 * 50) = 996

    # Call the API function (POST) to execute the process
    for payload in testPayloads:
        response = client.post('/api/qgis/building-energy-simulation-process', 
                                data = json.dumps(payload),
                                content_type = 'application/json',
                                headers = headers)

        # Check the status code: 400
        assert response.status_code == 400

        # Check the 'value' property
        assert 'value' in response.get_json() and\
            not response.get_json()['value'] is None and\
            response.get_json()['value'] == False


# Test 04 (c) -> Process successful
def testProcessSuccessful(client, caplog):
    '''
    Test 04 (c) -> Process successful.
    Input parameters:
        client: object -> The PyTest client object.
        caplog: object -> The PyTest object to capture the logs.
    '''

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
    with open('api/tests/payloads/bes_payload.json', 'r') as payloadFile:
        processPayload = json.load(payloadFile)

    # Call the API function (POST) to execute the process
    response = client.post('/api/qgis/building-energy-simulation-process', 
                           data = json.dumps(processPayload),
                           content_type = 'application/json',
                           headers = headers)

    # Check the status code: 200
    assert response.status_code == 200

    # Check the 'value' property
    assert 'value' in response.get_json() and response.get_json()['value']
