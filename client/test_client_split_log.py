import base64

import pytest

import os

user = 'user'
password = 'password'
raw_directory = os.getcwd().split('/')
raw_directory.pop(-1)
server_directory = '/'.join(raw_directory) + '/server'
try:
    os.remove(f'{server_directory}/clients.csv')
    os.remove(f'{server_directory}/user_system_load.csv')
except FileNotFoundError:
    pass
client_id = base64.b64encode(f'{user}:{password}'.encode()).decode()
data = {"cpu_load": 25.9, "mem": 6172, "storage": 95888, "time": 1646650624}
data_2 = {"cpu_load": 20.9, "mem": 6272, "storage": 95838, "time": 1646650625}
data_3 = {"cpu_load": 20.9, "mem": 6272, "storage": 95838, "time": 1646650626}
header = {'Authorization': f'Basic {client_id}'}


def test_split_log(api_client):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    api_client.post(f'/client/{client_id}', data=data, headers=header)
    api_client.post(f'/client/{client_id}', data=data_2, headers=header)
    api_client.post(f'/client/{client_id}', data=data_3, headers=header)
    response = api_client.get(path=f'/client/{client_id}/time/report?start={1646650624}&end={1646650626}')
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json['payload'], list)
    assert len(response_json) == 1
    assert len(response_json['payload']) == 2
    os.remove(f'{server_directory}/clients.csv')
    os.remove(f'{server_directory}/user_system_load.csv')
