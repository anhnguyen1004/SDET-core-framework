import pytest
from api.base_client import BaseAPIClient
from models.db_client import PostgresDBClient
from config.settings import settings

@pytest.fixture(scope="session")
def db_client():
    client = PostgresDBClient(
        host = settings.DB_HOST,
        db_name = settings.DB_NAME,
        user = settings.DB_USER,
        password = settings.DB_PASSWORD,
        port = 5432
    )

    client.connect()
    yield client

    client.disconnect()

@pytest.fixture(scope="session")
def api_client():
    api_client = BaseAPIClient(base_url="https://jsonplaceholder.typicode.com")
    return api_client

