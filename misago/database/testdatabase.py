from functools import lru_cache

from databases import DatabaseURL
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL

from ..conf import settings
from .database import database_url
from .migrations import run_migrations


@lru_cache
def create_test_database():
    with get_database_connection(database_url) as connection:
        # if test_database_url is set, we will create test db from scratch
        if settings.test_database_name:
            database_name = database_url.database
            connection.execute(f"DROP DATABASE IF EXISTS {database_name}")
            connection.execute(f"CREATE DATABASE {database_name}")

    run_migrations()


def teardown_test_database():
    if settings.test_database_name:
        with get_database_connection(database_url) as connection:
            database_name = database_url.database
            connection.execute(f"DROP DATABASE IF EXISTS {database_name}")


def get_database_connection(url: DatabaseURL) -> Engine:
    server_url = get_database_server_url(url)
    return create_engine(server_url, isolation_level="AUTOCOMMIT").connect()


def get_database_server_url(url: DatabaseURL) -> URL:
    return URL(
        "postgresql",
        username=url.options.get("user"),
        password=url.options.get("password"),
        host=url.hostname,
        port=url.port,
    )
