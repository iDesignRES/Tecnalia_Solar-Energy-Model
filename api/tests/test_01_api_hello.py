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


# Test 01 -> The API is online and healthy
def testHello(client, caplog):
    '''
    Test 01 -> The API is online and healthy.
    Input parameters:
        client: object -> The PyTest client object.
        caplog: object -> The PyTest object to capture the logs.
    '''

    # Call the API function using 'test_client'
    with app.app_context():  # Application context
        with app.test_request_context('/api/qgis/hello'):  # Request context
            with caplog.at_level(logging.INFO):
                response = client.get('/api/qgis/hello')
    
    # Check the status code: 200
    assert response.status_code == 200
