from client_data import user, password, header


def test_split_log(api_client):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.post(path=f'/client/{user}/time/report?start={1646650624}&end={1646650626}', headers=header)
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json['payload'], list)
    assert len(response_json) == 1
    assert len(response_json['payload']) == 3


def test_split_log_empty_start_end(api_client):
    response = api_client.post(path=f'/client/{user}/time/report?start=&end=', headers=header)
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json['payload'], list)
    assert len(response_json) == 1
    assert len(response_json['payload']) == 3


def test_split_log_for_errors(api_client):
    response = api_client.post(path=f'/client/{user}/time/report?start=badargument&end=badargumenttwo', headers=header)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json == {'error': 'value error'}
    response = api_client.post(f'/client/other_client/time/report?start=&end=', headers={"Authorization": 'bad client id'})
    assert response.status_code == 401
    assert response.json() == {'error': 'authorization error'}
