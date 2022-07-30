import pytest

from ...tables import settings
from ..fetchall import fetch_all_assoc


@pytest.mark.asyncio
async def test_fetch_all_assoc_returns_dicts_of_db_rows(db):
    for row in await fetch_all_assoc(settings.select(None)):
        assert "name" in row
        assert "value" in row
