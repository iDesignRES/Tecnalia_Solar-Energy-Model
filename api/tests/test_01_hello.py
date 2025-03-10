import requests


BASE_URL = 'http://localhost:5010'
HELLO_URL = '/api/qgis/hello'


# Test 01 -> The API is online and healthy
def testHello():
    ''' Test 01 -> The API is online and healthy. '''

    # Call the API function (GET)
    response = requests.get(BASE_URL + HELLO_URL)
    
    # Check the status code: 200
    assert response.status_code == 200
