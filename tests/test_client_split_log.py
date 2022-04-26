from client_data import user, password, client_id


def test_split_log(api_client):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.get(path=f'/client/{client_id}/time/report?start={1646650624}&end={1646650626}')
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json['payload'], list)
    assert len(response_json) == 1
    assert len(response_json['payload']) == 3
