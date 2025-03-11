import json
import requests

from api.api import app


TEST_URL_AUTH = 'http://localhost:5010/api/qgis/authenticate'
TEST_URL_PROCESS = 'http://localhost:5010/api/qgis/building-energy-simulation-process'


# Test 04 (a) -> Missing input parameters
def testMissingInputParameters():
    ''' Test 04 (a) -> Missing input parameters. '''

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
        response = requests.post(TEST_URL_PROCESS, json = payload, headers = headers)

        # Check the status code: 400
        assert response.status_code == 400

        # Check the 'value' property
        assert 'value' in response.json() and\
            not response.json()['value'] is None and\
            response.json()['value'] == False


# Test 03 (b) -> Wrong values in input parameters
# def testWrongValuesInInputParameters():
#     ''' Test 03 (b) -> Wrong values in input parameters. '''

#     # Load the authentication payload
#     with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
#         authPayload = json.load(payloadFile)
    
#     # Call the API function (POST) to authenticate
#     response = requests.post(TEST_URL_AUTH, json = authPayload)

#     # Check the authentication status code: 200
#     assert response.status_code == 200

#     # Check the 'value' property, and define the headers for the process
#     assert 'value' in response.json() and response.json()['value']
#     headers = {'Authorization': 'Bearer ' + response.json()['value'],
#                'Content-Type': 'application/json' }
    
#     # Load the process payload
#     with open('api/tests/payloads/pv_payload.json', 'r') as payloadFile:
#         processPayload = json.load(payloadFile)

#     # Define the test payloads
#     testPayloads = [processPayload, processPayload]
#     testPayloads[0]['nutsid'] = 'ES70'
#     testPayloads[1]['slope_angle'] = 370

#     # Call the API function (POST) to execute the process
#     for payload in testPayloads:
#         response = requests.post(TEST_URL_PROCESS, json = payload, headers = headers)

#         # Check the status code: 400
#         assert response.status_code == 400

#         # Check the 'value' property
#         assert 'value' in response.json() and\
#             not response.json()['value'] is None and\
#             response.json()['value'] == False


# Test 03 (c) -> Process successful
# def testProcessSuccessful():
#     ''' Test 03 (c) -> Process successful. '''

#     # Load the authentication payload
#     with open('api/tests/payloads/auth_payload.json', 'r') as payloadFile:
#         authPayload = json.load(payloadFile)
    
#     # Call the API function (POST) to authenticate
#     response = requests.post(TEST_URL_AUTH, json = authPayload)

#     # Check the authentication status code: 200
#     assert response.status_code == 200

#     # Check the 'value' property, and define the headers for the process
#     assert 'value' in response.json() and response.json()['value']
#     headers = {'Authorization': 'Bearer ' + response.json()['value'],
#                'Content-Type': 'application/json' }
    
#     # Load the process payload
#     with open('api/tests/payloads/bes_payload.json', 'r') as payloadFile:
#         processPayload = json.load(payloadFile)

#     # Call the API function (POST) to execute the process
#     response = requests.post(TEST_URL_PROCESS, json = processPayload, headers = headers)

#     # Check the status code: 200
#     assert response.status_code == 200

#     # Check the 'value' property
#     assert 'value' in response.json() and response.json()['value']
