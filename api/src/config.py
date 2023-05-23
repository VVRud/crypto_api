import os

from sqlalchemy import URL

VERSION = "0.0.1"
DEBUG = os.getenv("DEBUG", "true") == "true"

# Authentication related
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE = int(os.getenv("JWT_EXPIRE", "60"))
PWD_ALGORITHM = os.getenv("PWD_ALGORITHM", "bcrypt")

# Database
DATABASE_CONNECTION_STRING = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("POSTGRESQL_USERNAME", "tester"),
    password=os.getenv("POSTGRESQL_PASSWORD", "test"),
    host=os.getenv("POSTGRESQL_HOST", "localhost"),
    port=int(os.getenv("POSTGRESQL_PORT", "5432")),
    database=os.getenv("POSTGRESQL_DATABASE", "zeply"),
)

# Secret Keys
KEYS_CONFIG_FILE = os.getenv("KEYS_CONFIG_FILE", "keys_config.dev.json")

# Wallet
WALLET_LANGUAGE = os.getenv("WALLET_LANGUAGE", "english")
WALLET_STRENGTH = int(os.getenv("WALLET_STRENGTH", "256"))
PASSPHRASE_LENGTH = int(os.getenv("PASSPHRASE_LENGTH", "64"))
