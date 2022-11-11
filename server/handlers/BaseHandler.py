from storage.db import Psql
from storage.init_db import db


class BaseHandler:
    """Base class for all Handlers"""

    def __init__(self, database: Psql = db):
        self.db = database
