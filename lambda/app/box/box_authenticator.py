import json
import tempfile
from boxsdk import JWTAuth, Client
from config import BoxConfig

class BoxAuthenticator:
    def __init__(self, config: BoxConfig):
        self.config = config

    def save_to_temp_file(self) -> str:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        json.dump(self.config.jwt_config, open(temp_file.name, 'w'))
        return temp_file.name

    def authenticate(self) -> Client:
        temp_config_path = self.save_to_temp_file()
        auth = JWTAuth.from_settings_file(temp_config_path)
        client = Client(auth)
        return client
