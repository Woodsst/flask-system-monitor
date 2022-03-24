import base64
import datetime
import json
import logging

import psycopg

conn = psycopg.connect(dbname='clients', user='wood', password='123')

cur = conn.cursor()


def authorization(username: str, password: str) -> bool or int:
    uniq_id = base64.b64encode(f'{username}:{password}'.encode())
    uniq_id = uniq_id.decode()
    cur.execute('SELECT uniq_id FROM clients WHERE uniq_id = %s', (uniq_id,))
    client_id = cur.fetchone()[0]
    if client_id is not None and client_id == uniq_id:
        conn.commit()
        return client_id
    conn.commit()
    return False


def add_client(username: str, password: str) -> int:
    uniq_id = base64.b64encode(f'{username}:{password}'.encode())
    uniq_id = uniq_id.decode()
    cur.execute('INSERT INTO clients (username, uniq_id, registration_date) VALUES (%s, %s, %s)',
                (username, uniq_id, datetime.datetime.now()))
    with open(f'{username}_system_load.csv', 'w', encoding='utf-8') as file:
        file.write('time;cpu;memory;storage\n')
    conn.commit()
    return uniq_id


def user_verification(user_name: str) -> bool:
    cur.execute("SELECT username FROM clients WHERE username = %s ", (user_name,))
    if cur.fetchone() is not None:
        conn.commit()
        return True
    conn.commit()
    return False


def error_authorization(request) -> dict:
    logging.info('%s - incorrect username or pass', request.get_json())
    return {
        'Error': 'incorrect username or pass'
    }


def id_verification(client_id: str) -> str or bool:
    cur.execute('SELECT uniq_id, username FROM clients WHERE uniq_id = %s', (client_id,))
    client_id_in_base, username = cur.fetchone()
    if client_id is not None and client_id == client_id_in_base:
        conn.commit()
        return username
    conn.commit()
    return False


def to_json_for_client_data(data: dict):
    for key, _ in data.items():
        if key == 'cpu_load':
            data[key] = float(data[key])
            continue
        data[key] = int(data[key])
    return json.dumps(data)
