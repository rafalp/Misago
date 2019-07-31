from unittest.mock import Mock

import pytest

from .. import SOCIALAUTH_CACHE
from ..enabledproviders import get_enabled_providers, get_provider_settings
from ..models import SocialAuthProvider


@pytest.fixture
def provider(db):
    return SocialAuthProvider.objects.create(
        provider="facebook", is_active=True, order=0
    )


def test_enabled_providers_are_read_from_db_if_cache_is_not_available(
    db, mocker, cache_versions, django_assert_num_queries
):
    mocker.patch("django.core.cache.cache.get", return_value=None)
    with django_assert_num_queries(1):
        get_enabled_providers(cache_versions)


def test_enabled_providers_are_loaded_from_cache_if_it_is_set(
    db, mocker, cache_versions, django_assert_num_queries
):
    cache_get = mocker.patch("django.core.cache.cache.get", return_value={})
    with django_assert_num_queries(0):
        get_enabled_providers(cache_versions)
    cache_get.assert_called_once()


def test_enabled_providers_cache_is_set_if_none_exists(db, mocker, cache_versions):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=None)

    get_enabled_providers(cache_versions)
    cache_set.assert_called_once()


def test_enabled_providers_cache_is_not_set_if_it_already_exists(
    db, mocker, cache_versions, django_assert_num_queries
):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value={})
    with django_assert_num_queries(0):
        get_enabled_providers(cache_versions)
    cache_set.assert_not_called()


def test_enabled_providers_cache_key_includes_cache_name_and_version(
    db, mocker, cache_versions
):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=None)
    get_enabled_providers(cache_versions)
    cache_key = cache_set.call_args[0][0]
    assert SOCIALAUTH_CACHE in cache_key
    assert cache_versions[SOCIALAUTH_CACHE] in cache_key


def test_enabled_providers_are_returned_as_dict(provider, mocker, cache_versions):
    mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=None)
    providers = get_enabled_providers(cache_versions)
    assert provider.pk in providers


def test_enabled_providers_dict_includes_settings(provider, mocker, cache_versions):
    mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=None)
    providers = get_enabled_providers(cache_versions)
    assert providers[provider.pk]["settings"]


def test_enabled_providers_dict_includes_auth_backend(provider, mocker, cache_versions):
    mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=None)
    providers = get_enabled_providers(cache_versions)
    assert providers[provider.pk]["auth_backend"]


def test_provider_settings_keys_are_capitalized():
    provider = Mock(pk="google", settings={"key": "text-key"})
    settings = get_provider_settings(provider)
    assert settings == {"KEY": "text-key"}


def test_provider_settings_are_merged_from_model_and_defaults():
    provider = Mock(pk="facebook", settings={"key": "text-key"})
    settings = get_provider_settings(provider)
    assert settings == {"SCOPE": ["email"], "KEY": "text-key"}
