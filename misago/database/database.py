from databases import Database, DatabaseURL

from ..conf import settings

database_url = DatabaseURL(settings.database_url)
if settings.test and settings.test_database_name:
    database_url = database_url.replace(database=settings.test_database_name)

database = Database(database_url, force_rollback=settings.test)
