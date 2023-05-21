import inspect
import json
import logging
import os

from singleton import SingletonMeta

logger = logging.getLogger(__name__)


class KeysLoader(metaclass=SingletonMeta):
    """Class specifically used for keys management."""

    def __init__(self, config_path: str):
        with open(config_path, "r") as file:
            self.config = json.load(file)
        self.funcs = {name[1:]: inst for name, inst in inspect.getmembers(self)}

    def load_aes_keys(self) -> list[tuple[int, str]]:
        """Load AES Shamir key parts."""
        key_parts = []
        for conf in self.config["AES_KEYS"]:
            try:
                key_parts.extend(self.funcs[conf["method"]](**conf["params"]))
            except Exception as e:
                logger.warning(f"Key was not loaded with error: {str(e)}")
        return key_parts

    def load_jwt_secret_token(self) -> str:
        """Loads JWT secret key."""
        conf = self.config["JWT_KEY"]
        return self.funcs[conf["method"]](**conf["params"])

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
    def _load_from_env_variables(**kwargs) -> list[tuple[int, str]] | str:
        """Load keys from environment variables."""
        if "env_name" in kwargs:
            return os.environ[kwargs["env_name"]]
        elif "env_starts" in kwargs:
            key_name = kwargs["env_starts"]
            key_parts = []
            for env_name in filter(lambda x: x.startswith(key_name), os.environ.keys()):
                key_parts.append(
                    (int(env_name.replace(key_name, "")), os.environ[env_name])
                )
            return key_parts
        else:
            raise NotImplementedError()
