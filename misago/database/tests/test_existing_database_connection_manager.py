import pytest

from ..database import database
from ..testing import existing_database_connection


@pytest.mark.asyncio
async def test_context_manager_prevents_already_connected_error_in_nested_context():
    async with database:
        with existing_database_connection():
            async with database:
                pass
