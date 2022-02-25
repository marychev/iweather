import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent


def get_config() -> dict:
    return {
        'postgres': {
            'database': os.environ.get('POSTGRES_DB', 'iweather'),
            'user': os.environ.get('POSTGRES_USER', 'postgres'),
            'password': os.environ.get('POSTGRES_PASSWORD', 'password'),
            'host': os.environ.get('POSTGRES_HOST', 'db'),
            'port': os.environ.get('POSTGRES_PORT', 5432),
            'minsize': os.environ.get('POSTGRES_MINSIZE', 1),
            'maxsize': os.environ.get('POSTGRES_MAXSIZE', 5)
        }
    }


config = get_config()
