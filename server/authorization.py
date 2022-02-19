import uuid
import base64

clients = {
    'uniq_id': {'login': 'pass'},
}


def authorization(user: str, password: str) -> (bool, int):
    for client_id, client in clients.items():
        if user in client.keys() and password in client.values():
            return client_id


def add_client(login: str, password: str) -> int:
    uniq_id = str(uuid.uuid4())
    clients.update({uniq_id: {login: password}})
    with open(f'client_{uniq_id}_cpu_load.csv', 'w') as file:
        file.write(f'{uniq_id};cpu\n')
        return uniq_id


def user_exist(user_name: str) -> bool:
    for _, client in clients.items():
        if user_name in client:
            return True
    return False


def hash_authorization(client_id: int, client_hash: str) -> bool:
    client = clients[client_id]
    client_login = list(client.keys())[0]
    client_password = list(client.values())[0]
    hash_authorize_client = base64.b64encode(f'{client_login}:{client_password}'.encode())
    if client_hash == hash_authorize_client.decode():
        return True
    return False