import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(scope="module")
def client():
    """Тестовый клиент FastAPI."""
    return TestClient(app)
