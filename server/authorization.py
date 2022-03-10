import base64
import json
import logging


def authorization(username: str, password: str) -> (bool, int):
    with open('clients.csv', 'r') as file:
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
    with open('clients.csv', 'a') as file:
        file.write(f'{username};{uniq_id}\n')
    with open(f'{username}_system_load.csv', 'w') as file:
        file.write(f'time;cpu;memory;storage\n')
    return uniq_id


def user_verification(user_name: str) -> bool:
    try:
        with open('clients.csv', 'r') as file:
            for string in file.readlines():
                strip = string.strip()
                username, client_id = strip.split(';')
                if user_name == username:
                    return True
    except FileNotFoundError:
        return False


def error_authorization(request):
    logging.info(f'{request.get_json()}, incorrect username or pass')
    return {
        'Error': 'incorrect username or pass'
    }


def id_verification(client_id: str) -> str or bool:
    with open('clients.csv', 'r') as file:
        for string in file.readlines():
            strip = string.strip()
            username, client_id_in_file = strip.split(';')
            if client_id == client_id_in_file:
                return username
    return False


def to_json_for_client_data(data: dict):
    for key, value in data.items():
        if key == 'cpu_load':
            data[key] = float(data[key])
            continue
        data[key] = int(data[key])
    return json.dumps(data)
