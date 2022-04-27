from client_data import WSRequstsForClientSystemMonitoring as client_request
from client import WebSocketResponse as server_response


def test_get_client_data(ws_api):
    ws_api.get(client_request.CLIENT_DATA)
    response = ws_api.recv()
    assert len(response) > 0
    assert isinstance(response, str)
    assert response == server_response.DATA_RETURN_FOR_DATA_1


def test_error_get_client_data(ws_api):
    ws_api.get(client_request.EMPTY_CLIENT_DATA)
    response = ws_api.recv()
    assert isinstance(response, str)
    assert response == server_response.ERROR_DATA_SIZE
