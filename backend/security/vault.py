import json

class KeyVault:
    def __init__(self, file="config/api_keys.json"):
        self.file = file

    def load_keys(self):
        with open(self.file, "r") as f:
            return json.load(f)

    def get_key(self, service):
        return self.load_keys().get(service)