import pytest

from .. import SETTINGS_CACHE
from ..dynamicsettings import DynamicSettings


def test_settings_are_loaded_from_database_if_cache_is_not_available(
    db, mocker, cache_versions, django_assert_num_queries
):
    mocker.patch("django.core.cache.cache.get", return_value=None)
    with django_assert_num_queries(1):
        DynamicSettings(cache_versions)


def test_settings_are_loaded_from_cache_if_it_is_set(
    db, mocker, cache_versions, django_assert_num_queries
):
    cache_get = mocker.patch("django.core.cache.cache.get", return_value={})
    with django_assert_num_queries(0):
        DynamicSettings(cache_versions)
    cache_get.assert_called_once()


def test_settings_cache_is_set_if_none_exists(db, mocker, cache_versions):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=None)

    DynamicSettings(cache_versions)
    cache_set.assert_called_once()


def test_settings_cache_is_not_set_if_it_already_exists(
    db, mocker, cache_versions, django_assert_num_queries
):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value={})
    with django_assert_num_queries(0):
        DynamicSettings(cache_versions)
    cache_set.assert_not_called()


def test_settings_cache_key_includes_cache_name_and_version(db, mocker, cache_versions):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=None)
    DynamicSettings(cache_versions)
    cache_key = cache_set.call_args[0][0]
    assert SETTINGS_CACHE in cache_key
    assert cache_versions[SETTINGS_CACHE] in cache_key


def test_accessing_attr_returns_setting_value(db, cache_versions):
    settings = DynamicSettings(cache_versions)
    assert settings.forum_name == "Misago"


def test_accessing_attr_for_undefined_setting_raises_attribute_error(
    db, cache_versions
):
    settings = DynamicSettings(cache_versions)
    with pytest.raises(AttributeError):
        settings.not_existing  # pylint: disable=pointless-statement


def test_accessing_attr_for_lazy_setting_with_value_returns_true(
    cache_versions, lazy_setting
):
    settings = DynamicSettings(cache_versions)
    assert settings.lazy_setting is True


def test_lazy_setting_getter_for_lazy_setting_with_value_returns_real_value(
    cache_versions, lazy_setting
):
    settings = DynamicSettings(cache_versions)
    assert settings.get_lazy_setting_value("lazy_setting") == lazy_setting.value


def test_lazy_setting_getter_for_lazy_setting_makes_db_query(
    cache_versions, lazy_setting, django_assert_num_queries
):
    settings = DynamicSettings(cache_versions)
    with django_assert_num_queries(1):
        settings.get_lazy_setting_value("lazy_setting")


def test_accessing_attr_for_lazy_setting_without_value_returns_none(
    cache_versions, lazy_setting_without_value
):
    settings = DynamicSettings(cache_versions)
    assert settings.lazy_setting is None


def test_lazy_setting_getter_for_lazy_setting_is_reusing_query_result(
    cache_versions, lazy_setting, django_assert_num_queries
):
    settings = DynamicSettings(cache_versions)
    settings.get_lazy_setting_value("lazy_setting")
    with django_assert_num_queries(0):
        settings.get_lazy_setting_value("lazy_setting")


def test_lazy_setting_getter_for_undefined_setting_raises_attribute_error(
    db, cache_versions
):
    settings = DynamicSettings(cache_versions)
    with pytest.raises(AttributeError):
        settings.get_lazy_setting_value("undefined")


def test_lazy_setting_getter_for_not_lazy_setting_raises_value_error(
    db, cache_versions
):
    settings = DynamicSettings(cache_versions)
    with pytest.raises(ValueError):
        settings.get_lazy_setting_value("forum_name")


def test_public_settings_getter_returns_dict_with_public_settings(
    cache_versions, public_setting
):
    settings = DynamicSettings(cache_versions)
    public_settings = settings.get_public_settings()
    assert public_settings["public_setting"] == "Hello"


def test_public_settings_getter_excludes_private_settings_from_dict(
    cache_versions, private_setting
):
    settings = DynamicSettings(cache_versions)
    public_settings = settings.get_public_settings()
    assert "private_setting" not in public_settings


def test_getter_returns_setting_dict(cache_versions, public_setting):
    settings = DynamicSettings(cache_versions)
    assert settings.get(public_setting.setting) == {
        "value": public_setting.value,
        "is_lazy": public_setting.is_lazy,
        "is_public": public_setting.is_public,
        "width": public_setting.image_width,
        "height": public_setting.image_height,
    }
