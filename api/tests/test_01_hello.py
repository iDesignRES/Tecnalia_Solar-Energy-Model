import requests
from api.api import app


TEST_URL = 'http://localhost:5010/api/qgis/hello'


# Test 01 -> The API is online and healthy
def testHello():
    ''' Test 01 -> The API is online and healthy. '''

    # Call the API function (GET)
    response = requests.get(TEST_URL)
    
    # Check the status code: 200
    assert response.status_code == 200
