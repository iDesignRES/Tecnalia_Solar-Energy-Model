import json
import building_energy_process
import pytest


# Test 01 -> The process works
def testProcess():
    '''
    Test 01 -> The process works.
    Input parameters:
        None.
    '''
    
    # Load the authorization payload
    with open('auth.json', 'r') as authPayloadFile:
        authPayload = json.load(authPayloadFile)
    assert authPayload is not None
    
    # Load the process payload
    with open('process.json', 'r') as processPayloadFile:
        processPayload = json.load(processPayloadFile)
    assert processPayload is not None
    
    # Declare the parameters
    startTime = '2019-01-01T13:00:00'
    endTime = '2019-01-02T13:00:00'
    buildingUse = 'Apartment Block'

    # Execute the process
    dictResult = building_energy_process.executeBuildingEnergySimulationProcess(authPayload, processPayload, startTime, endTime, buildingUse)
    
    # Check the result
    assert dictResult is not None
    assert isinstance(dictResult, dict)
    assert len(dictResult) > 0
    
