from databases import DatabaseURL

from ..testdatabase import get_database_server_url


def test_database_url_is_converted_to_sql_alchemy_server_url_format():
    databases_url = DatabaseURL(
        "postgresql://dbuser:dbpass@dbhost/dbname"
    )
    sqlalchemy_server_url = get_database_server_url(databases_url)
    assert str(sqlalchemy_server_url) == "postgresql://dbuser:dbpass@dbhost"
