from contextlib import contextmanager
from unittest.mock import patch


async def _noop():
    pass


@contextmanager
def existing_database_connection():
    with patch("misago.database.database.connect", _noop):
        with patch("misago.database.database.disconnect", _noop):
            yield
