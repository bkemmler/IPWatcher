# config.py
# This file contains the configuration settings for the IP Watcher application.

import yaml
from .schemas import Config

class Settings:
    """
    The Settings class loads the application configuration from a YAML file.
    """
    def __init__(self, config_file="/config/config.yaml"):
        """
        Initialize the Settings object.

        Args:
            config_file: The path to the configuration file.
        """
        self.config_file = config_file
        self.reload()

    def reload(self):
        """
        Reload the configuration from the YAML file.
        """
        with open(self.config_file, "r") as f:
            self._config = Config(**yaml.safe_load(f))

    def __getattr__(self, name):
        """
        Get a configuration setting by name.
        """
        return getattr(self._config, name)

# Create a single instance of the Settings class.
settings = Settings()
