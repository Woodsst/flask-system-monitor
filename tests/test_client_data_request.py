import base64
import json
import os

import pytest

user = 'user'
password = 'password'
client_id = base64.b64encode(f'{user}:{password}'.encode()).decode()
raw_directory = os.getcwd().split('/')
raw_directory.pop(-1)
server_directory = '/'.join(raw_directory) + '/server'
data = {"cpu_load": 25.9, "mem": 6172, "storage": 95888, "time": 1646650624}
header = {'Authorization': f'Basic {client_id}'}


def test_client_data_request_202(api_client):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.post(f'/client/{client_id}', data=data,
                                 headers=header)
    assert response.status_code == 202
    response_json = response.json()
    assert isinstance(response_json, dict)
    assert len(response_json) == 4
    for value in response_json.values():
        assert isinstance(value, (int, float))
    with open(f'{server_directory}/user_system_load.csv', 'r') as file_data:
        lines_in_file = file_data.readlines()
        assert lines_in_file[0].strip() == 'time;cpu;memory;storage'
        assert lines_in_file[-1].strip() == '1646650624;25.9;6172;95888'
    os.remove(f'{server_directory}/user_system_load.csv')
    os.remove(f'{server_directory}/clients.csv')


def test_client_data_request_405(api_client):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.get(f'/client/{client_id}')
    assert response.status_code == 405
    response = api_client.put(f'/client/{client_id}')
    assert response.status_code == 405
    response = api_client.patch(f'/client/{client_id}')
    assert response.status_code == 405
    response = api_client.delete(f'/client/{client_id}')
    assert response.status_code == 405


def test_client_data_request_401(api_client):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.post(f'/client/{client_id}', data='',
                                 headers=header)
    assert response.status_code == 401
    response = api_client.post(f'/client/{client_id}', data=data,
                               headers={'Authorization': f'Basic afgjn123'})
    assert response.status_code == 401
    response = api_client.post(f'/client/{client_id}', data=data,
                               headers='')
    assert response.status_code == 401

