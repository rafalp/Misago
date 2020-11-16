from unittest.mock import Mock

import pytest

from .. import THEME_CACHE
from ..context_processors import theme as context_processor


@pytest.fixture
def mock_request(cache_versions):
    return Mock(cache_versions=cache_versions)


def test_theme_data_is_included_in_template_context(db, mock_request):
    assert context_processor(mock_request)["theme"]


def test_theme_is_loaded_from_database_if_cache_is_not_available(
    db, mocker, mock_request, django_assert_num_queries
):
    mocker.patch("django.core.cache.cache.get", return_value=None)
    with django_assert_num_queries(3):
        context_processor(mock_request)


def test_theme_is_loaded_from_cache_if_it_is_set(
    db, mocker, mock_request, django_assert_num_queries
):
    cache_get = mocker.patch("django.core.cache.cache.get", return_value={})
    with django_assert_num_queries(0):
        context_processor(mock_request)
    cache_get.assert_called_once()


def test_theme_cache_is_set_if_none_exists(db, mocker, mock_request):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=None)

    context_processor(mock_request)
    cache_set.assert_called_once()


def test_theme_cache_is_not_set_if_it_already_exists(
    db, mocker, mock_request, django_assert_num_queries
):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value={})
    with django_assert_num_queries(0):
        context_processor(mock_request)
    cache_set.assert_not_called()


def test_theme_cache_key_includes_cache_name_and_version(
    db, mocker, mock_request, cache_versions
):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=None)
    context_processor(mock_request)
    cache_key = cache_set.call_args[0][0]
    assert THEME_CACHE in cache_key
    assert cache_versions[THEME_CACHE] in cache_key
