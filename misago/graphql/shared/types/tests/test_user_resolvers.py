from .....conf import settings
from ..user import resolve_avatar, resolve_avatars


def test_user_avatars_list_is_resolved(user):
    assert list(resolve_avatars(user, None))


def test_user_avatar_is_resolved_to_largest_avatar_by_default(user):
    assert resolve_avatar(user, None)["size"] == max(settings.avatar_sizes)


def test_user_avatar_is_resolved_to_specified_size(user):
    assert resolve_avatar(user, None, size=100)["size"] == 100
