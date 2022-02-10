import pytest
from datatype import DataType


def test_storage_info_200(api_client):
    response = api_client.get('/monitor/storage/info')
    assert response.status_code == 200, f'{response.status_code}'
    for units in DataType:
        response_for_units = api_client.get(f'/monitor/storage/info?{units.value}')
        response_for_units_json = response_for_units.json()
        assert len(response_for_units_json) == 5
        for value in response_for_units_json.values():
            assert isinstance(value, (str, float, int))


def test_storage_info_405(api_client):
    response = api_client.post('/monitor/storage/info')
    assert response.status_code == 405, f'{response.status_code}'
    for units in DataType:
        response_for_units = api_client.post(f'/monitor/storage/info?{units.value}')
        assert response_for_units.status_code == 405


def test_storage_total_200(api_client):
    response = api_client.get('/monitor/storage/total')
    assert response.status_code == 200, f'{response.status_code}'
    for units in DataType:
        response_for_units = api_client.get(f'/monitor/storage/total?{units.value}')
        response_for_units_json = response_for_units.json()
        assert len(response_for_units_json) == 3
        assert isinstance(response_for_units_json['units'], str)
        assert isinstance(response_for_units_json['total'], int)
        assert isinstance(response_for_units_json['used'], int)


def test_storage_total_405(api_client):
    response = api_client.post('/monitor/storage/total')
    assert response.status_code == 405, f'{response.status_code}'
    for units in DataType:
        response_for_units = api_client.post(f'/monitor/storage/total?{units.value}')
        assert response_for_units.status_code == 405

