import pytest

from ..templatetags.misago_avatars import avatar


@pytest.fixture
def avatars(user):
    return {i["size"]: i["url"] for i in user.avatars}


def test_filter_returns_url_to_200_size_image(user, avatars):
    assert avatar(user) == avatars[200]


def test_filter_returns_url_to_next_largest_image_for_given_size(user, avatars):
    assert avatar(user, 250) == avatars[400]
    assert avatar(user, 150) == avatars[200]
    assert avatar(user, 50) == avatars[100]


def test_filter_returns_url_largest_image_if_requested_size_is_not_available(
    user, avatars
):
    assert avatar(user, 500) == avatars[400]
