from client_data import header, client_id, password, user, data_3, data_2


def test_client_log_time_work(api_client):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    api_client.post(f'/client/{client_id}', data=data_2, headers=header)
    api_client.post(f'/client/{client_id}', data=data_3, headers=header)
    response = api_client.get(f'/client/{client_id}/time')
    response_js = response.json()
    assert response_js['start'] == 1646650624
    assert response_js['end'] == 1646650626
