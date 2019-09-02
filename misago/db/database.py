from databases import Database

from ..conf import settings


if settings.test:
    database_url = settings.test_database_url
else:
    database_url = settings.database_url


database = Database(database_url, force_rollback=settings.test)
