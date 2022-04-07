import base64
import json
import logging
from db import Psql
import os

db = Psql(username='wood', db_name='clients', password='123', host="database", port=5432)


def authorization(username: str, password: str) -> bool or int:
    uniq_id = base64.b64encode(f'{username}:{password}'.encode())
    uniq_id = uniq_id.decode()
    client_id = db.authorization_by_uniq_id(uniq_id)
    if client_id:
        db.commit()
        return client_id
    return False


def add_client(username: str, password: str) -> int:
    uniq_id = base64.b64encode(f'{username}:{password}'.encode())
    uniq_id = uniq_id.decode()
    db.add_client(uniq_id, username=username)
    path = os.path.dirname(__file__)
    with open(f'{path}/{username}_system_load.csv', 'w', encoding='utf-8') as file:
        file.write('time;cpu;memory;storage\n')
    return uniq_id


def user_verification(user_name: str) -> bool:
    return db.verification_user(user_name)


def error_authorization(request) -> dict:
    logging.info('%s - incorrect username or pass', request.get_json())
    return {
        'Error': 'incorrect username or pass'
    }


def id_verification(client_id: str) -> str or bool:
    return db.id_verification(client_id)


def to_json_for_client_data(data: dict):
    for key, _ in data.items():
        if key == 'cpu_load':
            data[key] = float(data[key])
            continue
        data[key] = int(data[key])
    return json.dumps(data)
