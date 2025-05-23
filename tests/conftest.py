import pytest
from app import create_app
from config import Config


class TestConfig(Config):
    DATABASE_URL = 'sqlite:///:memory:'
    LOAD_USERS_ON_STARTUP = False

    TESTING = True


@pytest.fixture()
def app():
    with create_app(TestConfig) as app:
        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
