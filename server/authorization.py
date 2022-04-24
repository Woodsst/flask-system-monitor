import base64
import logging

from db import Psql


class Authorization:
    def __init__(self, database: Psql) -> None:
        self.db = database

    def authorization(self, username: str, password: str) -> bool or int:
        uniq_id = self.uniq_id(username, password)
        client_id = self.db.authorization_by_uniq_id(uniq_id)
        if client_id:
            self.db.commit()
            return client_id
        return False

    def uniq_id(self, username: str, password: str) -> str:
        uniq_id = base64.b64encode(f'{username}:{password}'.encode())
        uniq_id = uniq_id.decode()
        return uniq_id

    def add_client(self, username: str, password: str) -> int:
        uniq_id = self.uniq_id(username, password)
        self.db.add_client(uniq_id, username=username)
        return uniq_id

    def user_verification(self, user_name: str) -> bool:
        return self.db.verification_user(user_name)

    @staticmethod
    def error_authorization(request) -> dict:
        logging.info('%s - incorrect username or pass', request.get_json())
        return {
            'Error': 'incorrect username or pass'
        }

    def id_verification(self, client_id: str) -> str or bool:
        return self.db.id_verification(client_id)
