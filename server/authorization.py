import base64
import logging


def authorization(username: str, password: str) -> (bool, int):
    with open('Clients.csv', 'r') as file:
        for string in file.readlines():
            strip = string.strip()
            name, client_id = strip.split(';')
            uniq_id = base64.b64encode(f'{username}:{password}'.encode())
            uniq_id = uniq_id.decode()
            if client_id == uniq_id:
                return client_id
    return False


def add_client(username: str, password: str) -> int:
    uniq_id = base64.b64encode(f'{username}:{password}'.encode())
    uniq_id = uniq_id.decode()
    with open('Clients.csv', 'a') as file:
        file.write(f'{username};{uniq_id}\n')
    with open(f'{username}_system_load.csv', 'w') as file:
        file.write(f'time;cpu;memory;storage\n')
    return uniq_id


def user_exist(user_name: str) -> bool:
    with open('Clients.csv', 'r') as file:
        for string in file.readlines():
            strip = string.strip()
            username, client_id = strip.split(';')
            if user_name == username:
                return True
    return False


def hash_authorization(client_hash: str) -> bool:
    with open('Clients.csv', 'r') as file:
        for string in file.readlines():
            strip = string.strip()
            username, client_id_in_file = strip.split(';')
            if client_hash == client_id_in_file:
                return True
    return False


def error_authorization(request):
    logging.info(f'{request.get_json()}, incorrect username or pass')
    return {
        'Error': 'incorrect username or pass'
    }


def id_verification(client_id):
    with open('Clients.csv', 'r') as file:
        for string in file.readlines():
            strip = string.strip()
            username, client_id_in_file = strip.split(';')
            if client_id == client_id_in_file:
                return username
    return False
