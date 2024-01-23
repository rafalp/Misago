from unittest.mock import Mock

import pytest
from django.test import override_settings

from ..forumaddress import ForumAddress


@pytest.mark.parametrize(
    "link",
    (
        "https://misago-project.org/",
        "http://misago-project.org/",
        "http://misago-project.org",
        "misago-project.org",
        "misago-project.org/some-path/",
    ),
)
def test_forum_address_is_inbound_link_returns_true_for_inbound_link(link):
    forum_address = ForumAddress(Mock(forum_address="https://misago-project.org"))
    assert forum_address.is_inbound_link(link)


@pytest.mark.parametrize(
    "link",
    (
        "https://example.org/",
        "http://example.org/",
        "http://example.org",
        "example.org",
        "example.org/some-path/",
    ),
)
@override_settings(MISAGO_FORUM_ADDRESS_HISTORY=["http://example.org"])
def test_forum_address_is_inbound_link_returns_true_for_historic_inbound_link(link):
    forum_address = ForumAddress(Mock(forum_address="https://misago-project.org"))
    assert forum_address.is_inbound_link(link)


@pytest.mark.parametrize(
    "link",
    (
        "https://google.com",
        "http://google.org/",
        "http://google.org",
        "google.org",
        "google.org/some-path/",
    ),
)
@override_settings(MISAGO_FORUM_ADDRESS_HISTORY=["http://example.org"])
def test_forum_address_is_inbound_link_returns_false_for_outbound_link(link):
    forum_address = ForumAddress(Mock(forum_address="https://misago-project.org"))
    assert not forum_address.is_inbound_link(link)


@pytest.mark.parametrize(
    "link",
    (
        "https://google.com",
        "http://google.org/",
        "http://google.org",
        "google.org",
        "google.org/some-path/",
    ),
)
def test_forum_address_is_inbound_link_returns_false_if_address_is_not_configured(link):
    forum_address = ForumAddress(Mock(forum_address=None))
    assert not forum_address.is_inbound_link(link)
