import configparser
import os


class Config:

    def __init__(self):
        self.config_parser = configparser.SafeConfigParser()
        self.config_parser.read('config/config.ini')

    def get(self, section, key):
        env = section.upper() + "_" + key.upper().replace(".", "_")
        if os.environ.get(env) is not None:
            return os.environ.get(env)
        return self.config_parser.get(section, key)