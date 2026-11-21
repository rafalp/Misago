import csv
import io
from unittest.mock import ANY

import pytest
from django.http import StreamingHttpResponse
from django.urls import reverse

from ...search.logging import log_search
from ...test import assert_contains

search_logs_link = reverse("misago:admin:searchlogs:index")


def test_search_logs_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, search_logs_link)


def test_search_logs_list_renders_empty(admin_client):
    response = admin_client.get(search_logs_link + "?redirected=1")
    assert_contains(response, "No search logs exist")


def test_search_logs_list_renders_public_user_search(admin_client, other_user):
    search_log = log_search(other_user, "127.0.0.1", "test search", is_public=True)

    response = admin_client.get(search_logs_link + "?redirected=1")
    assert_contains(response, search_log.search_query)
    assert_contains(response, search_log.user.username)
    assert_contains(response, search_log.ip_address)


def test_search_logs_list_renders_public_deleted_user_search(admin_client):
    search_log = log_search(None, "127.0.0.1", "test search", is_public=True)

    response = admin_client.get(search_logs_link + "?redirected=1")
    assert_contains(response, search_log.search_query)
    assert_contains(response, "Guest")
    assert_contains(response, search_log.ip_address)


def test_search_logs_list_excludes_private_user_search(admin_client, other_user):
    log_search(other_user, "127.0.0.1", "test search")

    response = admin_client.get(search_logs_link + "?redirected=1")
    assert_contains(response, "No search logs exist")


def test_search_logs_list_excludes_private_deleted_user_search(admin_client):
    log_search(None, "127.0.0.1", "test search")

    response = admin_client.get(search_logs_link + "?redirected=1")
    assert_contains(response, "No search logs exis")


def test_search_logs_list_search_renders_empty(admin_client):
    log_search(None, "127.0.0.1", "test search", is_public=False)

    response = admin_client.get(search_logs_link + "?redirected=1&search_query=lorem")
    assert_contains(response, "No search logs found")


def test_search_logs_list_search_query_renders_public_log(admin_client):
    search_log = log_search(None, "127.0.0.1", "test search", is_public=True)

    response = admin_client.get(search_logs_link + "?redirected=1&search_query=test")
    assert_contains(response, search_log.search_query)
    assert_contains(response, "Guest")
    assert_contains(response, search_log.ip_address)


def test_search_logs_list_search_query_excludes_private_log(admin_client):
    log_search(None, "127.0.0.1", "test search")

    response = admin_client.get(search_logs_link + "?redirected=1&search_query=test")
    assert_contains(response, "No search logs found")


def test_search_logs_list_search_ip_address_renders_public_log(admin_client):
    search_log = log_search(None, "127.0.0.1", "test search", is_public=True)

    response = admin_client.get(search_logs_link + "?redirected=1&ip_address=127.*")
    assert_contains(response, search_log.search_query)
    assert_contains(response, "Guest")
    assert_contains(response, search_log.ip_address)


def test_search_logs_list_search_ip_address_excludes_private_log(admin_client):
    log_search(None, "127.0.0.1", "test search")

    response = admin_client.get(search_logs_link + "?redirected=1&ip_address=127.*")
    assert_contains(response, "No search logs found")


def read_streaming_response(response: StreamingHttpResponse) -> list[dict]:
    csv_string = (b"".join(response.streaming_content)).decode()
    return list(csv.DictReader(io.StringIO(csv_string)))


def test_search_logs_download_returns_empty_csv(admin_client):
    response = admin_client.post(reverse("misago:admin:searchlogs:download"))

    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv"

    csv_data = read_streaming_response(response)
    assert csv_data == []


def test_search_logs_download_returns_csv_with_rows(admin_client, user):
    log_search(user, "127.0.0.1", "lorem", is_public=True)
    log_search(None, "125.0.0.1", "ipsum")
    log_search(None, "120.0.0.1", "dolor", is_public=True)

    response = admin_client.post(reverse("misago:admin:searchlogs:download"))

    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv"

    csv_data = read_streaming_response(response)
    assert csv_data == [
        {
            "Search": "dolor",
            "Searched": ANY,
            "User": "",
            "IP address": "120.0.0.1",
        },
        {
            "Search": "lorem",
            "Searched": ANY,
            "User": user.username,
            "IP address": "127.0.0.1",
        },
    ]


def test_search_logs_download_raises_error_for_get_request(admin_client):
    response = admin_client.get(reverse("misago:admin:searchlogs:download"))
    return response.status_code == 401
