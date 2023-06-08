import os
import json

class ConfigManager:

    def __init__(self, config_file = './qase.config.json', env_vars_prefix = 'QASE_'):
        self.config_file = config_file
        self.env_vars_prefix = env_vars_prefix
        self.config = {}

    def load_config(self):
        # Load from file
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as file:
                    self.config = json.load(file)
        except Exception as e:
            print(f"⚠️  Failed to load config from file {self.config_file}: {e}")

        # Load from env vars
        try:
            for key, value in os.environ.items():
                if key.startswith(self.env_vars_prefix):
                    self._set_config(key[len(self.env_vars_prefix):].lower(), value)
        except Exception as e:
            print(f"⚠️  Failed to load config from env vars: {e}")

    def get(self, key):
        return self._get_config(key)

    def _get_keys(self, config, prefix=""):
        for key, value in config.items():
            if isinstance(value, dict):
                yield from self._get_keys(value, f"{prefix}{key}_")
            else:
                yield f"{prefix}{key}"

    def _set_config(self, key, value):
        keys = key.split("_")
        config = self.config
        for key in keys[:-1]:
            config = config.setdefault(key, {})
        config[keys[-1]] = value

    def _get_config(self, key):
        keys = key.split("_")
        config = self.config
        for key in keys[:-1]:
            config = config.get(key, {})
        return config.get(keys[-1], None)