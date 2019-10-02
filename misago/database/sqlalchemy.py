from databases import DatabaseURL
from sqlalchemy.engine.url import URL

from .database import database


def convert_database_url_to_sql_alchemy_format(url: DatabaseURL) -> str:
    new_url = URL(
        "postgresql",
        username=url.options.get("user"),
        password=url.options.get("password"),
        host=url.hostname,
        port=url.port,
        database=url.database,
    )
    return str(new_url)


database_url = convert_database_url_to_sql_alchemy_format(database.url)
