def test_cpu_load_200(api_client):
    response = api_client.get('/monitor/cpu/load')
    assert response.status_code == 200, f'{response.status_code}'
    response_json = response.json()
    assert 'load' in response_json
    assert isinstance(response_json['load'], float)
    assert 0.0 < response_json['load']
    assert 100.0 >= response_json['load']
    assert len(response_json) == 1


def test_cpu_load_405(api_client):
    response = api_client.post('/monitor/cpu/load')
    assert response.status_code == 405, f'{response.status_code}'


def test_cpu_core_info_200(api_client):
    response = api_client.get('/monitor/cpu/info')
    assert response.status_code == 200, f'{response.status_code}'
    response_json = response.json()
    assert 'cores frequency' in response_json
    assert 'physical cores count' in response_json
    assert len(response_json) >= 2
    assert len(response_json) <= 3
    assert len(response_json['cores frequency']) == 3
    assert isinstance(response_json['logical cores count'], int)
    assert isinstance(response_json['physical cores count'], int)


def test_cpu_core_info_405(api_client):
    response = api_client.post('/monitor/cpu/info')
    assert response.status_code == 405, f'{response.status_code}'
