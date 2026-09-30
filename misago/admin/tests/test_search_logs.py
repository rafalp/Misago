import pytest
from django.urls import reverse

from ...search.logging import log_search
from ...test import assert_contains


@pytest.fixture
def search_logs_link(admin_client):
    response = admin_client.get(reverse("misago:admin:searchlogs:index"))
    return response["location"]


def test_search_logs_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, reverse("misago:admin:searchlogs:index"))


def test_search_logs_list_renders_empty(admin_client, search_logs_link):
    response = admin_client.get(search_logs_link)
    assert_contains(response, "No search logs exist")


def test_search_logs_list_renders_public_user_search(
    admin_client, search_logs_link, other_user
):
    search_log = log_search(other_user, "127.0.0.1", "test search", is_public=True)

    response = admin_client.get(search_logs_link)
    assert_contains(response, search_log.search_query)
    assert_contains(response, search_log.user.username)
    assert_contains(response, search_log.ip_address)


def test_search_logs_list_renders_public_deleted_user_search(
    admin_client, search_logs_link
):
    search_log = log_search(None, "127.0.0.1", "test search", is_public=True)

    response = admin_client.get(search_logs_link)
    assert_contains(response, search_log.search_query)
    assert_contains(response, "Guest")
    assert_contains(response, search_log.ip_address)


def test_search_logs_list_excludes_private_user_search(
    admin_client, search_logs_link, other_user
):
    log_search(other_user, "127.0.0.1", "test search")

    response = admin_client.get(search_logs_link)
    assert_contains(response, "No search logs exist")


def test_search_logs_list_excludes_private_deleted_user_search(
    admin_client, search_logs_link
):
    log_search(None, "127.0.0.1", "test search")

    response = admin_client.get(search_logs_link)
    assert_contains(response, "No search logs exis")


def test_search_logs_list_search_renders_empty(admin_client, search_logs_link):
    log_search(None, "127.0.0.1", "test search", is_public=False)

    response = admin_client.get(search_logs_link + "&search_query=lorem")
    assert_contains(response, "No search logs found")


def test_search_logs_list_search_query_renders_public_log(
    admin_client, search_logs_link
):
    search_log = log_search(None, "127.0.0.1", "test search", is_public=True)

    response = admin_client.get(search_logs_link + "&search_query=test")
    assert_contains(response, search_log.search_query)
    assert_contains(response, "Guest")
    assert_contains(response, search_log.ip_address)


def test_search_logs_list_search_query_excludes_private_log(
    admin_client, search_logs_link
):
    log_search(None, "127.0.0.1", "test search")

    response = admin_client.get(search_logs_link + "&search_query=test")
    assert_contains(response, "No search logs found")


def test_search_logs_list_search_ip_address_renders_public_log(
    admin_client, search_logs_link
):
    search_log = log_search(None, "127.0.0.1", "test search", is_public=True)

    response = admin_client.get(search_logs_link + "&ip_address=127.*")
    assert_contains(response, search_log.search_query)
    assert_contains(response, "Guest")
    assert_contains(response, search_log.ip_address)


def test_search_logs_list_search_ip_address_excludes_private_log(
    admin_client, search_logs_link
):
    log_search(None, "127.0.0.1", "test search")

    response = admin_client.get(search_logs_link + "&ip_address=127.*")
    assert_contains(response, "No search logs found")
