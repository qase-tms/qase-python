import os
import json
from .logger import Logger


class ConfigManager:

    def __init__(self, config_file='./qase.config.json', env_vars_prefix='QASE_'):
        self.logger = Logger()
        self.config = {}
        self.parseBool = lambda d: d in ("y", "yes", "true", "1", 1, True)

        try:
            if os.path.exists(config_file):
                with open(config_file, "r") as file:
                    def transform_keys(obj):
                        return {k.lower(): v for k, v in obj.items()}
                    self.config = json.load(file, object_hook=transform_keys)
        except Exception as e:
            self.logger.log("Failed to load config from file", "error")

        # Load from env vars
        try:
            for key, value in os.environ.items():
                if key.startswith(env_vars_prefix):
                    self._set_config(key[len(env_vars_prefix):].lower().replace('_', '.'), value)
        except Exception as e:
            self.logger.log("Failed to load config from env vars {e}", "error")

    def get(self, key, default=None, value_type=None):
        # Use _get_config method to get the value. If None, return default.
        value = self._get_config(key)
        if value_type and value_type == bool:
            return self.parseBool(value)
        return value or default

    def validate_config(self):
        if self.validator:
            self.validator.validate(self.config)

    def set(self, key, value):
        self._set_config(key, value)

    def _get_keys(self, config, prefix=""):
        for key, value in config.items():
            if isinstance(value, dict):
                yield from self._get_keys(value, f"{prefix}{key}.")
            else:
                yield f"{prefix}{key}"

    def _set_config(self, key, value, delimiter="."):
        keys = key.split(delimiter)
        config = self.config
        for key in keys[:-1]:
            config = config.setdefault(key, {})
        config[keys[-1]] = value

    def _get_config(self, key):
        keys = key.split(".")
        config = self.config
        for key in keys[:-1]:
            config = config.get(key, {})
        return config.get(keys[-1], None)

    def __str__(self):
        return json.dumps(self.config, indent=4, sort_keys=True)
