import pytest

from ..dynamicsettings import get_settings_from_db
from ..update import update_setting, update_settings


@pytest.mark.asyncio
async def test_single_setting_value_is_updated(db):
    await update_setting("forum_name", "Test Forum")
    settings = await get_settings_from_db()
    assert settings["forum_name"] == "Test Forum"


@pytest.mark.asyncio
async def test_multiple_settings_value_is_updated(db):
    await update_settings({"forum_name": "Test Forum"})
    settings = await get_settings_from_db()
    assert settings["forum_name"] == "Test Forum"
