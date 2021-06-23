import os
import cx_Oracle
import json

from dataclasses import dataclass
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

secret_file = os.path.join(base_dir, 'app/common/secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise KeyError(f'Set the {setting} environment variable')


@dataclass
class Config:
    BASE_DIR = base_dir

    DB_POOL_RECYCLE: int = 900
    # DB_ECHO: bool = True
    DB_ECHO: bool = environ.get("LOGGING",
                                "False").lower() in ('true', '1', 't')

    DB_URL: str = environ.get(
        "DB_URL", "oracle://{user}:{password}@{sid}".format(
            user=get_secret('DB_USER'),
            password=get_secret('DB_PASSWORD'),
            sid=cx_Oracle.makedsn(get_secret('DB_HOST'),
                                  get_secret('DB_PORT'),
                                  sid=get_secret('DB_SID'))))


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))
