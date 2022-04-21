import os

import yaml


class Settings:
    def __init__(self):
        self.path = self.config_path()
        with open(self.path, 'r') as conf:
            yaml_file = yaml.safe_load(conf)
            self.db_name = yaml_file["db_name"]
            self.db_username = yaml_file["db_username"]
            self.db_host = yaml_file["db_host"]
            self.db_port = yaml_file["db_port"]
            self.db_password = yaml_file["db_password"]
        self.default = self.default_config()

    def default_config(self):
        default = {
            "db_name": self.db_name,
            "db_username": self.db_username,
            "db_host": self.db_host,
            "db_port": self.db_port,
            "db_password": self.db_password
        }
        return default

    @staticmethod
    def config_path():
        raw_path = os.path.dirname(__file__)
        raw_path = raw_path.split('/')
        raw_path.pop(-1)
        raw_path.append('config_for_github.yml')
        path = '/'.join(raw_path)
        return path

    def config_for_tests(self):
        with open(self.path, 'w') as file:
            yaml.dump({
                "db_name": "test_clients",
                "db_username": "test",
                "db_password": "123",
                "db_port": 5432,
                "db_host": "database"
            }, file)
        self.db_name = "test_clients"
        self.db_username = "test"
        self.db_password = "123"
        self.db_port = 5432
        self.db_host = "database"

    def reset_default_config(self):
        with open(self.path, 'w') as file:
            yaml.dump(self.default, file)
            file.flush()
