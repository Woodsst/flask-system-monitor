import pytest


def test_api_200(api_client):
    response = api_client.get('/api')
    assert response.status_code == 200, f'{response.status_code}'
    response_json = response.json()
    assert response_json['name'] == 'system monitor'
    assert response_json['version'] == '0.0.1'


def test_api_405(api_client):
    response = api_client.post('/api')
    assert response.status_code == 405, f'{response.status_code}'
