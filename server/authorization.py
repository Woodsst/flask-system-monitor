import base64
import json
import logging
from db import Psql
from config import Settings

config = Settings()
db = Psql(password=config.db_password,
          host=config.db_host,
          port=config.db_port,
          db_name=config.db_name,
          username=config.db_username)


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
