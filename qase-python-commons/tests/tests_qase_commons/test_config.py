import os
import json
import unittest
from unittest.mock import patch, mock_open
from qase.commons.config import ConfigManager


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.mock_config_data = json.dumps({
            "database": {
                "host": "localhost",
                "port": "5432"
            },
            "secretkey": "supersecret"
        })

    @patch("os.path.exists")
    def test_load_config_from_file(self, mock_exists):
        mock_exists.return_value = True
        with patch("builtins.open", new_callable=mock_open, read_data=self.mock_config_data):
            config = ConfigManager()

        self.assertEqual(config.get("database.host"), "localhost")
        self.assertEqual(config.get("database.port"), "5432")
        self.assertEqual(config.get("secretkey"), "supersecret")

    @patch.dict(os.environ,
                {"QASE_DATABASE_HOST": "localhost", "QASE_DATABASE_PORT": "5432", "QASE_SECRETKEY": "supersecret"})
    def test_load_config_from_env(self):
        config = ConfigManager()

        self.assertEqual(config.get("database.host"), "localhost")
        self.assertEqual(config.get("database.port"), "5432")
        self.assertEqual(config.get("secretkey"), "supersecret")

    def test_get_config_key_not_exist(self):
        config = ConfigManager()

        self.assertIsNone(config.get("non_existent_key"))

    @patch("os.path.exists")
    def test_set_config(self, mock_exists):
        mock_exists.return_value = True
        with patch("builtins.open", new_callable=mock_open, read_data=self.mock_config_data):
            config = ConfigManager()
        config._set_config("new_config_key", "newvalue")

        self.assertEqual(config.get("new_config_key"), "newvalue")

    @patch("os.path.exists")
    def test_empty_config(self, mock_exists):
        mock_exists.return_value = False
        config = ConfigManager()

        self.assertEqual(config.config, {})

    @patch("os.path.exists")
    def test_env_overrides_file(self, mock_exists):
        mock_exists.return_value = True
        with patch("builtins.open", new_callable=mock_open, read_data=self.mock_config_data):
            with patch.dict(os.environ, {"QASE_DATABASE_HOST": "override"}):
                config = ConfigManager()

        self.assertEqual(config.get("database.host"), "override")

    @patch("os.path.exists")
    def test_set_get_nested_config(self, mock_exists):
        mock_exists.return_value = True
        with patch("builtins.open", new_callable=mock_open, read_data=self.mock_config_data):
            config = ConfigManager()

        config._set_config("new_nested_key_1_2_3", "nestedvalue")
        self.assertEqual(config._get_config("new_nested_key_1_2_3"), "nestedvalue")


if __name__ == '__main__':
    unittest.main()
