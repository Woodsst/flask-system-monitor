import datetime

import psycopg


class Psql:
    def __init__(self, username: str, password: str, db_name: str):
        self.conn = psycopg.connect(dbname=db_name, user=username, password=password)
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def authorization_by_uniq_id(self, uniq_id) -> str:
        self.cursor.execute('SELECT uniq_id FROM clients WHERE uniq_id = %s', (uniq_id,))
        fetch = self.cursor.fetchone()
        if fetch is not None:
            client_id = fetch[0]
            self.conn.commit()
            return client_id
        return False

    def add_client(self, uniq_id: str, username: str):
        self.cursor.execute('INSERT INTO clients (username, uniq_id, registration_date) VALUES (%s, %s, %s)',
                            (username, uniq_id, datetime.datetime.now()))
        self.commit()

    def verification_user(self, user_name: str) -> bool:
        self.cursor.execute("SELECT username FROM clients WHERE username = %s ", (user_name,))
        if self.cursor.fetchone() is not None:
            self.commit()
            return user_name
        self.commit()
        return False

    def id_verification(self, client_id: str) -> str or bool:
        self.cursor.execute('SELECT uniq_id, username FROM clients WHERE uniq_id = %s', (client_id,))
        client_id_in_base, username = self.cursor.fetchone()
        if client_id is not None and client_id == client_id_in_base:
            self.commit()
            return username
        self.commit()
        return False

