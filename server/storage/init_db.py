from typing import Optional

from config.settings import settings
from storage.db import Psql

db: Optional[Psql] = None


def init_postgres():
    global db
    db = Psql(
        password=settings.storage.password,
        host=settings.storage.host,
        port=settings.storage.port,
        db_name=settings.storage.name,
        username=settings.storage.username,
    )
