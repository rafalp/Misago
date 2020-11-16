from unittest.mock import Mock

import pytest

from ..templatetags.misago_absoluteurl import absoluteurl


@pytest.fixture
def context():
    return {"settings": Mock(forum_address="http://test.com/")}


def test_path_is_prefixed_with_forum_address(context):
    assert absoluteurl(context, "/path/") == "http://test.com/path/"


def test_link_is_reversed_and_prefixed_with_forum_address(context):
    assert absoluteurl(context, "misago:index") == "http://test.com/"


def test_absolute_url_is_not_changed(context):
    url = "https://github.com/rafalp/Misago/issues/1067"
    assert absoluteurl(context, url) == url
