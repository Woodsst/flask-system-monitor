import base64
import json
import logging


def authorization(username: str, password: str) -> bool or int:
    with open('clients.csv', 'r', encoding='utf-8') as file:
        for string in file.readlines():
            strip = string.strip()
            _, client_id = strip.split(';')
            uniq_id = base64.b64encode(f'{username}:{password}'.encode())
            uniq_id = uniq_id.decode()
            if client_id == uniq_id:
                return client_id
    return False


def add_client(username: str, password: str) -> int:
    uniq_id = base64.b64encode(f'{username}:{password}'.encode())
    uniq_id = uniq_id.decode()
    with open('clients.csv', 'a', encoding='utf-8') as file:
        file.write(f'{username};{uniq_id}\n')
    with open(f'{username}_system_load.csv', 'w', encoding='utf-8') as file:
        file.write('time;cpu;memory;storage\n')
    return uniq_id


def user_verification(user_name: str) -> bool:
    try:
        with open('clients.csv', 'r', encoding='utf-8') as file:
            for string in file.readlines():
                strip = string.strip()
                username, _ = strip.split(';')
                if user_name == username:
                    return True
            return False
    except FileNotFoundError:
        return False


def error_authorization(request) -> dict:
    logging.info('%s - incorrect username or pass', request.get_json())
    return {
        'Error': 'incorrect username or pass'
    }


def id_verification(client_id: str) -> str or bool:
    with open('clients.csv', 'r', encoding='utf-8') as file:
        for string in file.readlines():
            strip = string.strip()
            username, client_id_in_file = strip.split(';')
            if client_id == client_id_in_file:
                return username
    return False


def to_json_for_client_data(data: dict):
    for key, _ in data.items():
        if key == 'cpu_load':
            data[key] = float(data[key])
            continue
        data[key] = int(data[key])
    return json.dumps(data)
