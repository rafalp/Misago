import pytest

from ..database import database
from ..testing import existing_database_connection


@pytest.mark.asyncio
async def test_database_raises_already_connected_error_when_contexts_are_nested():
    with pytest.raises(AssertionError):
        async with database:
            async with database:
                pass


@pytest.mark.asyncio
async def test_context_manager_prevents_already_connected_error_in_nested_context():
    async with database:
        with existing_database_connection():
            async with database:
                pass
