import pytest
from datatype import DataType


def test_memory_info_200(api_client):
    response = api_client.get('/monitor/memory/info')
    assert response.status_code == 200, f'{response.status_code}'
    for units in DataType:
        response_for_units = api_client.get(f'/monitor/memory/info?{units.value}')
        response_for_units_json = response_for_units.json()
        assert len(response_for_units_json) == 11
        for value in response_for_units_json.values():
            assert value >= 0


def test_memory_info_405(api_client):
    response = api_client.post('/monitor/memory/info')
    assert response.status_code == 405, f'{response.status_code}'
    for units in DataType:
        response_for_units = api_client.post(f'/monitor/memory/info?{units.value}')
        assert response_for_units.status_code == 405


def test_memory_total_200(api_client):
    response = api_client.get('/monitor/memory/total')
    assert response.status_code == 200, f'{response.status_code}'
    for units in DataType:
        response_for_units = api_client.get(f'/monitor/memory/total?{units.value}')
        response_for_units_json = response_for_units.json()
        assert len(response_for_units_json) == 2
        assert isinstance(response_for_units_json['total'], int)
        assert isinstance(response_for_units_json['units'], str)


def test_memory_total_405(api_client):
    response = api_client.post('/monitor/memory/total')
    assert response.status_code == 405, f'{response.status_code}'
    for units in DataType:
        response_for_units = api_client.post(f'/monitor/memory/total?{units.value}')
        assert response_for_units.status_code == 405
