import pytest

from ..dynamicsettings import get_dynamic_settings


@pytest.mark.asyncio
async def test_settings_are_loaded_from_database_if_cache_is_not_available(
    db, mocker, cache_versions
):
    mocker.patch("misago.cache.cache.get", return_value=None)
    db_get = mocker.patch(
        "misago.conf.dynamicsettings.get_settings_from_db", return_value={}
    )
    await get_dynamic_settings(cache_versions)
    db_get.assert_called_once()


@pytest.mark.asyncio
async def test_settings_are_loaded_from_cache_if_it_is_set(db, mocker, cache_versions):
    cache_get = mocker.patch("misago.cache.cache.get", return_value={})
    db_get = mocker.patch("misago.conf.dynamicsettings.get_settings_from_db")
    await get_dynamic_settings(cache_versions)
    cache_get.assert_called_once()
    db_get.assert_not_called()


@pytest.mark.asyncio
async def test_settings_cache_is_set_if_none_exists(db, mocker, cache_versions):
    cache_set = mocker.patch("misago.cache.cache.set")
    mocker.patch("misago.cache.cache.get", return_value=None)
    await get_dynamic_settings(cache_versions)
    cache_set.assert_called_once()


@pytest.mark.asyncio
async def test_settings_cache_is_not_set_if_it_already_exists(
    db, mocker, cache_versions
):
    cache_set = mocker.patch("misago.cache.cache.set")
    mocker.patch("misago.cache.cache.get", return_value={})
    await get_dynamic_settings(cache_versions)
    cache_set.assert_not_called()


@pytest.mark.asyncio
async def test_accessing_item_returns_setting_value(db, cache_versions):
    settings = await get_dynamic_settings(cache_versions)
    assert settings["forum_name"] == "Misago"


@pytest.mark.asyncio
async def test_accessing_item_for_undefined_setting_raises_key_error(
    db, cache_versions
):
    settings = await get_dynamic_settings(cache_versions)
    with pytest.raises(KeyError):
        settings["not_existing"]  # pylint: disable=pointless-statement
