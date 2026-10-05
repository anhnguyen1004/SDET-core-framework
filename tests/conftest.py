import pytest
from src.api.base_client import BaseAPIClient
from src.models.db_client import PostgresDBClient
from src.config.settings import settings

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

@pytest.fixture(scope="function")
def cleanup_user_test(db_client):
    user_ids = []
    yield user_ids
    if user_ids:
        ids_str = ",".join(map(str, user_ids))
        db_client.execute_query(f"DELETE FROM nguoi_dung where id in ({ids_str})")

@pytest.fixture(scope="session")
def api_client():
    api_client = BaseAPIClient(base_url="https://jsonplaceholder.typicode.com")
    return api_client

