import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from app.main import app
from app.core.database import get_database


@pytest.fixture
def test_client():
    """
    Provides a TestClient wired to a fresh in-memory mock MongoDB for each test.
    Each test gets its own isolated database — no leftover data between tests.
    """
    mock_client = AsyncMongoMockClient()
    mock_db = mock_client["bleach_codex_test"]

    app.dependency_overrides[get_database] = lambda: mock_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
