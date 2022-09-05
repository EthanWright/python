import configparser
import os

from paths import PYTHON_DIR


class Credentials(object):
    """
    Load API Credentials
    """
    credentials_file_path = os.path.join(PYTHON_DIR, 'youtube_api', 'input', 'credentials.txt')

    def __init__(self, api):
        self.api = api

        self.parser = configparser.ConfigParser()
        self.parser.read(self.credentials_file_path)

    def get(self, field):
        return self.parser.get(self.api, field).replace('"', '').strip()
