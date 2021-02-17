import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_URL = '/templates/'
TEMPLATES_ROOT = f'{BASE_DIR}{TEMPLATES_URL}'

DB_USER = os.environ.get("USER_DATABASE")
DB_PASS = os.environ.get("PASSWORD_DATABASE")
DB_NAME = os.environ.get("NAME_DATABASE")
DB_HOST = os.environ.get("HOST")
DB_PORT = os.environ.get("PORT")
SECRET_KEY = os.environ.get("SECRET_KEY") 
ALGORITHM = os.environ.get("ALGORITHM")

DEBUG = bool(int(os.environ.get("DEBUG")))

if DEBUG:
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
        "DEBUG_ACCESS_TOKEN_EXPIRE_MINUTES")
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
        "PROD_ACCESS_TOKEN_EXPIRE_MINUTES")
