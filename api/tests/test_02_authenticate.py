import requests


BASE_URL = 'http://localhost:5010'
AUTH_URL = '/api/qgis/authenticate'


# Test 02 (a) -> 'Admin' user logs in successfully
def testAdminLoginSuccess():
    ''' Test 02 (a) -> 'Admin' user logs in successfully. '''
    
    # Define the payload
    payload = {'username': 'admin', 'password': 'PWDadmin#2024'}
    
    # Call the API function (POST)
    response = requests.post(BASE_URL + AUTH_URL, json = payload)

    # Check the status code: 200
    assert response.status_code == 200

    # Check the 'value' property
    response_json = response.json()
    assert 'value' in response_json and response_json['value']


# Test 02 (b) -> 'Operator' user logs in successfully
def testOperatorLoginSuccess():
    ''' Test 02 (b) -> 'Operator' user logs in successfully. '''
    
    # Define the payload
    payload = {'username': 'operator', 'password': 'PWDoperator#2024'}
    
    # Call the API function (POST)
    response = requests.post(BASE_URL + AUTH_URL, json = payload)

    # Check the status code: 200
    assert response.status_code == 200

    # Check the 'value' property
    response_json = response.json()
    assert 'value' in response_json and response_json['value']


# Test 02 (c) -> 'Admin' authentication fails
def testAdminLoginFailure():
    ''' Test 02 (c) -> 'Admin' authentication fails. '''

    # Define the payload
    payload = {'username': 'admin', 'password': 'wrongpassword'}

    # Call the API function (POST)
    response = requests.post(BASE_URL + AUTH_URL, json = payload)

    # Check the status code: 401
    assert response.status_code == 401

    # Check the 'value' property
    response_json = response.json()
    assert 'value' in response_json and\
        not response_json['value'] is None and\
        response_json['value'] == False


# Test 02 (d) -> 'Operator' authentication fails
def testOperatorLoginFailure():
    ''' Test 02 (d) -> 'Operator' authentication fails. '''

    # Define the payload
    payload = {'username': 'operator', 'password': 'wrongpassword'}

    # Call the API function (POST)
    response = requests.post(BASE_URL + AUTH_URL, json = payload)

    # Check the status code: 401
    assert response.status_code == 401

    # Check the 'value' property
    response_json = response.json()
    assert 'value' in response_json and\
        not response_json['value'] is None and\
        response_json['value'] == False


# Test 02 (e) -> Missing fields
def testMissingFields():
    ''' Test 02 (e) -> Missing fields. '''
    
    # Define the payload
    payload = {'username': 'operator'}

    # Call the API function (POST)
    response = requests.post(BASE_URL + AUTH_URL, json = payload)

    # Check the status code: 400
    assert response.status_code == 400

    # Check the 'value' property
    response_json = response.json()
    assert 'value' in response_json and\
        not response_json['value'] is None and\
        response_json['value'] == False

