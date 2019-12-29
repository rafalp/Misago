from ..user import resolve_avatars


def test_user_avatars_list_is_resolved(user):
    assert list(resolve_avatars(user, None))
