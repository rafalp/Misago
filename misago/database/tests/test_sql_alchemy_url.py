from databases import DatabaseURL

from ..sqlalchemy import convert_database_url_to_sql_alchemy_format


def test_database_url_is_converted_to_sql_alchemy_format():
    databases_url = DatabaseURL(
        "postgresql://dbhost/dbname?user=dbuser&password=dbpass"
    )
    sqlalchemy_url = convert_database_url_to_sql_alchemy_format(databases_url)
    assert sqlalchemy_url == "postgresql://dbuser:dbpass@dbhost/dbname"
