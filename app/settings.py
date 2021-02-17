import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_URL = '/templates/'
TEMPLATES_ROOT = f'{BASE_DIR}{TEMPLATES_URL}'

DB_USER = os.environ.get("USER_DATABASE") or 'test'
DB_PASS = os.environ.get("PASSWORD_DATABASE") or 'test123test'
DB_NAME = os.environ.get("NAME_DATABASE") or 'test'
DB_HOST = os.environ.get("HOST") or 'localhost'
DB_PORT = os.environ.get("PORT") or 5432
SECRET_KEY = os.environ.get(
    "SECRET_KEY") or "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = os.environ.get("ALGORITHM")

DEBUG = os.environ.get("DEBUG") or True

if DEBUG:
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
        "DEBUG_ACCESS_TOKEN_EXPIRE_MINUTES") or 3000
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
        "PROD_ACCESS_TOKEN_EXPIRE_MINUTES") or 30
