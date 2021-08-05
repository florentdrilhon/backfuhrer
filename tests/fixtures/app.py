import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    yield client

    ctx.pop()