import base64

from client_data import header, password, user, data_3, data_2


def test_client_log_time_work(api_client):
    api_client.post(path='/client', json={'username': user, 'pass': password}, headers=header)
    api_client.post(f'/client/{user}', data=data_2, headers=header)
    api_client.post(f'/client/{user}', data=data_3, headers=header)
    response = api_client.post(f'/client/{user}/time', headers=header)
    response_js = response.json()
    assert response_js['start'] == 1646650624
    assert response_js['end'] == 1646650626


def test_client_log_time_work_error(api_client):
    api_client.post(path='/client', json={'username': 'other_client', 'pass': password})
    client_id = base64.b64encode(f'other_client:{password}'.encode()).decode()
    response = api_client.post(f'/client/other_client/time', headers={"Authorization": client_id})
    assert response.status_code == 406
    assert response.json() == {"error": "log is empty"}
