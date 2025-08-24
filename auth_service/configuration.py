import os
import json
import logging

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
        config_json = f'{os.getenv("CONFIG_PATH")}/config.json'
        LOGGER.info("Loading config file %s", config_json)
        with open(config_json, encoding="utf-8") as f:
            self._config = json.load(f)

    def get_user_json_record_path(self) -> str:
        return self._config.get("userJsonRecord", "No path found")


settings = Settings()
