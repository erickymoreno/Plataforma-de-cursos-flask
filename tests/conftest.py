from src import app
import pytest

@pytest.fixture
def client():
    return app