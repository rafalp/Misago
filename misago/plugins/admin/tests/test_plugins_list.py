from django.urls import reverse

from ....test import assert_contains


def test_plugins_list_contains_plugins(admin_client):
    response = admin_client.get(reverse("misago:admin:plugins:index"))

    assert_contains(response, "Example plugin")
    assert_contains(response, "empty_manifest_plugin")
    assert_contains(response, "invalid_manifest_plugin")
    assert_contains(response, "minimal_plugin")


def test_plugins_list_contains_plugins_directories_and_packages(admin_client):
    response = admin_client.get(reverse("misago:admin:plugins:index"))

    assert_contains(response, "empty-manifest-plugin")
    assert_contains(response, "empty_manifest_plugin")
    assert_contains(response, "full-manifest-plugin")
    assert_contains(response, "full_manifest_plugin")
    assert_contains(response, "invalid-manifest-plugin")
    assert_contains(response, "invalid_manifest_plugin")
    assert_contains(response, "minimal-plugin")
    assert_contains(response, "minimal_plugin")


def test_plugins_list_contains_plugins_metadata(admin_client):
    response = admin_client.get(reverse("misago:admin:plugins:index"))

    assert_contains(response, "Rafał Pitoń")
    assert_contains(response, "0.1DEV")
    assert_contains(response, "GNU GPL v2")
