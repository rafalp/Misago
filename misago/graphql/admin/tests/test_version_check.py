from unittest.mock import ANY, Mock

import pytest
from ariadne import gql
from requests.exceptions import RequestException

from .... import __version__
from ..versioncheck import CACHE_KEY, CACHE_LENGTH, resolve_version

test_query = gql("{ version { status message description } }")


def mock_requests_get(mocker, mock):
    return mocker.patch("requests.get", return_value=Mock(json=mock))


def test_version_check_query_returns_error_if_misago_version_is_unreleased(
    admin_graphql_client, mocker
):
    mocker.patch("misago.graphql.admin.versioncheck.__released__", False)
    mock_requests_get(mocker, Mock(return_value={"info": {"version": "outdated"}}))
    result = admin_graphql_client.query(test_query)
    assert result["version"]["status"] == "ERROR"


def test_version_check_query_returns_success_if_site_is_updated(
    admin_graphql_client, mocker
):
    mocker.patch("misago.graphql.admin.versioncheck.__released__", True)
    mock_requests_get(mocker, Mock(return_value={"info": {"version": __version__}}))
    result = admin_graphql_client.query(test_query)
    assert result["version"]["status"] == "SUCCESS"


def test_version_check_query_returns_error_if_site_is_outdated(
    admin_graphql_client, mocker
):
    mocker.patch("misago.graphql.admin.versioncheck.__released__", True)
    mock_requests_get(mocker, Mock(return_value={"info": {"version": "outdated"}}))
    result = admin_graphql_client.query(test_query)
    assert result["version"]["status"] == "ERROR"


def test_version_check_query_returns_warning_if_version_check_failed(
    admin_graphql_client, mocker
):
    mocker.patch("misago.graphql.admin.versioncheck.__released__", True)
    mock_requests_get(mocker, Mock(side_effect=RequestException()))
    result = admin_graphql_client.query(test_query)
    assert result["version"]["status"] == "WARNING"


def test_version_check_result_is_cached(mocker):
    mocker.patch("misago.graphql.admin.versioncheck.__released__", True)
    set_cache = mocker.patch("django.core.cache.cache.set")
    mock_requests_get(mocker, Mock(return_value={"info": {"version": "outdated"}}))
    resolve_version()
    set_cache.assert_called_with(CACHE_KEY, ANY, CACHE_LENGTH)


def test_failed_version_check_result_is_not_cached(admin_graphql_client, mocker):
    mocker.patch("misago.graphql.admin.versioncheck.__released__", True)
    set_cache = mocker.patch("django.core.cache.cache.set")
    mock_requests_get(mocker, Mock(side_effect=RequestException()))
    resolve_version()
    set_cache.assert_not_called()


def test_remote_api_is_not_called_if_version_check_cache_is_available(mocker):
    mocker.patch("misago.graphql.admin.versioncheck.__released__", True)
    mocker.patch("django.core.cache.cache.get", return_value={"status": "TEST"})
    api_mock = mock_requests_get(mocker, Mock())
    resolve_version()
    api_mock.assert_not_called()


def test_version_check_cache_is_returned_when_set(mocker):
    mocker.patch("misago.graphql.admin.versioncheck.__released__", True)
    mocker.patch("django.core.cache.cache.get", return_value={"status": "TEST"})
    api_mock = mock_requests_get(mocker, Mock())
    assert resolve_version() == {"status": "TEST"}
