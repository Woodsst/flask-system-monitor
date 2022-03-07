import pytest


def test_work_time_request_200(api_client):
    response = api_client.get('/start_time')
    assert response.status_code == 200, f'{response.status_code}'
    response_json = response.json()
    assert response_json['type'] == 'WORK_TIME'
    assert isinstance(response_json['payload'], dict)
    assert len(response_json['payload']) == 2
    assert isinstance(response_json['payload']['start_work'], str)
    assert isinstance(response_json['payload']['actual_time'], str)
    assert len(response_json['payload']['actual_time']) == 20
    assert len(response_json['payload']['start_work']) == 25


def test_work_time_request_405(api_client):
    response = api_client.post('/start_time')
    assert response.status_code == 405, f'{response.status_code}'
    response = api_client.put('/start_time')
    assert response.status_code == 405, f'{response.status_code}'
    response = api_client.patch('/start_time')
    assert response.status_code == 405, f'{response.status_code}'
    response = api_client.delete('/start_time')
    assert response.status_code == 405, f'{response.status_code}'
