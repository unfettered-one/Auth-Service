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
        self._config["userJsonRecord"] = os.getenv("USER_JSON_RECORD", "data/user_records.json")
        self._config["userDynamoTable"] = os.getenv("USER_DYNAMO_TABLE", None)
        self._config["environment"] = os.getenv("ENVIRONMENT", "development")
        self._jwt_secret_key = os.getenv("JWT_SECRET_KEY", None)

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

    def get_user_dynamo_table_name(self) -> str | None:
        """
        DynamoDB table name for user records
        """
        return self._config.get("userDynamoTable")

    def get_environment(self) -> str:
        """
        Environment in which application is running
        """
        return self._config.get("environment", "development")

    def get_jwt_secret(self) -> str | None:
        """
        Secret key for JWT token encoding/decoding
        """
        return self._jwt_secret_key

    def get_aws_region(self) -> str:
        """
        AWS region for DynamoDB operations
        """
        return self._config.get("AWS_REGION", "ap-south-1")


settings = Settings()
