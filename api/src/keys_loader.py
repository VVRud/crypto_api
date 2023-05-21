import inspect
import json
import logging
import os

logger = logging.getLogger(__name__)


class KeysLoader:

    def __init__(self, config_path: str):
        with open(config_path, "r") as file:
            config = json.load(file)
        funcs = {name[1:]: inst for name, inst in inspect.getmembers(self)}
        self.key_parts = []
        for conf in config:
            try:
                self.key_parts.extend(funcs[conf["method"]](**conf["params"]))
            except Exception as e:
                logger.warning(f"Key was not loaded with error: {str(e)}")

    @staticmethod
    def _load_from_aws(bucket, file_paths) -> list[tuple[int, str]]:
        raise Exception("Failed loading")

    @staticmethod
    def _load_from_gcp(bucket, file_paths) -> list[tuple[int, str]]:
        raise Exception("Failed loading")

    @staticmethod
    def _load_from_files(file_paths: list[str]) -> list[tuple[int, str]]:
        """Load keys from files."""
        key_parts = []
        for file_path in file_paths:
            with open(file_path, "r") as file:
                idx, key_share = file.read().split("\n")
                key_parts.append((int(idx), key_share))
        return key_parts

    @staticmethod
    def _load_from_env_variables(**kwargs) -> list[tuple[int, str]]:
        """Load keys from environment variables."""
        key_name = "SECURE_KEY_"
        key_parts = []
        for env_name in filter(lambda x: x.startswith(key_name), os.environ.keys()):
            key_parts.append((int(env_name.replace(key_name, '')), os.environ[env_name]))
        return key_parts
