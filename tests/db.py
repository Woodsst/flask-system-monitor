import psycopg
from psycopg import sql
from config import Settings

config = Settings()


class PostgresClient:
    def __init__(
        self, dbname: str, user: str, password: str, host: str, port: int
    ):
        self.conn = psycopg.connect(
            dbname=dbname, user=user, port=port, password=password, host=host
        )
        self.cursor = self.conn.cursor()

    def delete_username(self, test_user):
        self.cursor.execute(
            "DELETE FROM clients WHERE username = %s ", params=(test_user,)
        )
        self.conn.commit()

    def drop_table(self, test_user):
        self.cursor.execute(
            sql.SQL("DROP TABLE {}").format(sql.Identifier(test_user))
        )
        self.conn.commit()

    def select_username_uniq_id(self, test_user):
        self.cursor.execute(
            "SELECT username, uniq_id FROM clients WHERE username = %s",
            params=(test_user,),
        )
        return self.cursor.fetchone()

    def select_raw_data_for_time(self, test_user, time):
        self.cursor.execute(
            sql.SQL("""SELECT * FROM {} WHERE time=1646650624""").format(
                sql.Identifier(test_user)
            )
        )
        return self.cursor.fetchone()
