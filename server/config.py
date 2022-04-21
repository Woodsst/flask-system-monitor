import os

import yaml

raw_path = os.path.dirname(__file__)
raw_path = raw_path.split('/')
raw_path.pop(-1)
raw_path.append('config_for_github.yml')
path = '/'.join(raw_path)


class Settings:
    def __init__(self):
        with open(path, 'r') as conf:
            yaml_file = yaml.safe_load(conf)
            self.db_name = yaml_file["db_name"]
            self.db_username = yaml_file["db_username"]
            self.db_host = yaml_file["db_host"]
            self.db_port = yaml_file["db_port"]
            self.db_password = yaml_file["db_password"]
