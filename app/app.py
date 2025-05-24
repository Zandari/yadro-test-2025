from flask import Flask
from flask_bootstrap import Bootstrap5
from peewee import PostgresqlDatabase
from playhouse.db_url import connect
from contextlib import contextmanager
from app.utils.load_service import load_users
from app.routes import user_registry_bp
from app import models
import typing
import peewee


@contextmanager
def create_app(config_class: typing.Type) -> typing.Generator[None, None, Flask]:
    database = connect(config_class.DATABASE_URL)
    _initialize_database(database)
    if getattr(config_class, 'LOAD_USERS_ON_STARTUP', False):
        load_users(1000)

    app = Flask(__name__)
    app.config.from_object(config_class)

    Bootstrap5(app)

    app.register_blueprint(user_registry_bp)

    yield app

    database.close()


def _initialize_database(database: peewee.Database) -> None:
    models.db_proxy.initialize(database)
    database.drop_tables(models.all_models)
    database.create_tables(models.all_models)
