import pytest
from starlette.testclient import TestClient
from databases import Database
from alembic import command
from alembic.config import Config

from app.main import app
from app.settings import DB_HOST, DB_USER, DB_PORT, DB_PASS, BASE_DIR
from app.models import Base, engine

DB_NAME_ASYNC = "async-test"
DB_NAME_SYNC = "sync-test"

DB_URL_TEST_ASYNC = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME_ASYNC}"
DB_URL_TEST_SYNC = DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME_SYNC}"



@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def test_db_async():
    pass