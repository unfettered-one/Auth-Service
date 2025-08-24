"""
Module for managing application configuration settings.
"""

import os
import json
import logging
from errorhub.models import EnvironmentEnum

from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger(__name__)


class Settings:
    """
    Configuration settings for the application.
    """

    def __init__(self) -> None:
        self._config = {}
        self.load_env_variable()

    def load_env_variable(self):
        """
        load config json file and env variables
        """
        config_json = f'{os.getenv("CONFIG_PATH")}/config.json'
        LOGGER.info("Loading config file %s", config_json)
        with open(config_json, encoding="utf-8") as f:
            self._config = json.load(f)
        temp_env = os.getenv("ENVIRONMENT")
        if temp_env is not None:
            if temp_env == "production":
                self._config["environment"] = EnvironmentEnum.PRODUCTION
            elif temp_env == "staging":
                self._config["environment"] = EnvironmentEnum.STAGING
            else:
                self._config["environment"] = EnvironmentEnum.DEVELOPMENT
        else:
            self._config["environment"] = EnvironmentEnum.DEVELOPMENT

    def get_user_json_record_path(self) -> str:
        """
        Path to json file acting as a temp database
        """
        return self._config.get("userJsonRecord", "No path found")

    def get_environment(self) -> str:
        """
        Environment in which application is running
        """
        return self._config.get("environment", "development")


settings = Settings()
