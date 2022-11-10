import datetime
import time
from typing import List

import psycopg
from psycopg import sql
from config.logger_config import logger


class Psql:
    def __init__(
        self, username: str, password: str, db_name: str, host: str, port: str
    ):
        self.conn = self.__connect(db_name, username, password, host, port)
        self.cursor = self.conn.cursor()

    @staticmethod
    def __connect(db_name, username, password, host, port):
        timeout = 0.1
        connect = False
        while not connect:
            time.sleep(timeout)
            try:
                conn = psycopg.connect(
                    dbname=db_name,
                    user=username,
                    password=password,
                    host=host,
                    port=port,
                )
            except psycopg.OperationalError:
                timeout += 0.1
                logger.warning("trying connection with database")
                if timeout > 0.5:
                    raise psycopg.OperationalError(
                        "connection with database failed"
                    )
                continue
            connect = True
        return conn

    def commit(self):
        self.conn.commit()

    def authorization_by_uniq_id(self, uniq_id) -> str:
        self.cursor.execute(
            "SELECT uniq_id FROM clients WHERE uniq_id = %s", (uniq_id,)
        )
        fetch = self.cursor.fetchone()
        if fetch is not None:
            client_id = fetch[0]
            self.conn.commit()
            return client_id
        return False

    def add_client(self, uniq_id: str, username: str):
        self.cursor.execute(
            """
            INSERT INTO clients (username, uniq_id, registration_date)
            VALUES (%s, %s, %s)
        """,
            (username, uniq_id, datetime.datetime.now()),
        )
        self.cursor.execute(
            sql.SQL(
                """
            CREATE TABLE {} (cpu real, memory real, storage real, time int)
        """
            ).format(sql.Identifier(username))
        )
        self.commit()

    def verification_user(self, user_name: str) -> bool:
        self.cursor.execute(
            "SELECT uniq_id FROM clients WHERE username = %s", (user_name,)
        )
        client_id = self.cursor.fetchone()
        if client_id is not None:
            self.commit()
            return client_id[0]
        self.commit()
        return False

    def id_verification(self, client_id: str) -> str or bool:
        self.cursor.execute(
            "SELECT uniq_id, username FROM clients WHERE uniq_id = %s",
            (client_id,),
        )
        fetch = self.cursor.fetchone()
        if fetch is None:
            return
        client_id_in_base, username = fetch
        if client_id is not None and client_id == client_id_in_base:
            self.commit()
            return username
        self.commit()
        return False

    def client_log(self, cpu, mem, storage, time, username):
        self.cursor.execute(
            sql.SQL(
                """
            INSERT INTO {} (cpu, memory, storage, time)
            VALUES (%(cpu)s, %(mem)s, %(storage)s, %(time)s)
        """
            ).format(sql.Identifier(username)),
            {"cpu": cpu, "mem": mem, "storage": storage, "time": time},
        )
        self.commit()

    def client_log_request(self, username, start, end) -> dict:
        self.cursor.execute(
            sql.SQL(
                """
            SELECT cpu, memory, storage, time
            FROM {}
            WHERE time <= %(end)s and time >= %(start)s
        """
            ).format(sql.Identifier(username)),
            {"end": end, "start": start},
        )
        fetch = self.cursor.fetchall()
        self.commit()
        return fetch

    def client_full_log(self, username) -> List[tuple]:
        self.cursor.execute(
            sql.SQL(
                """
            SELECT cpu, memory, storage, time FROM {}
        """
            ).format(sql.Identifier(username))
        )
        fetch = self.cursor.fetchall()
        self.commit()
        return fetch

    def log_write_time(self, username: str) -> List[tuple]:
        self.cursor.execute(
            sql.SQL(
                """
            SELECT MIN(time), MAX(time) FROM {}
        """
            ).format(sql.Identifier(username))
        )
        fetch = self.cursor.fetchone()
        self.commit()
        return fetch
