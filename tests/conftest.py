import pytest
from app import create_app
from app import models
from tests.utils.random_user import create_random_user
from config import Config


class TestConfig(Config):
    DATABASE_URL = 'sqlite:///:memory:'
    LOAD_USERS_ON_STARTUP = False

    TESTING = True


@pytest.fixture()
def app():
    with create_app(TestConfig) as app:
        yield app
        models.db_proxy.drop_tables(models.all_models)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def persisted_user() -> models.User:
    return create_random_user()
