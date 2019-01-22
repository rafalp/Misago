from ..user import get_fake_username


def test_fake_username_can_be_created(fake):
    assert get_fake_username(fake)


def test_different_fake_username_is_created_every_time(fake):
    fake_usernames = [get_fake_username(fake) for i in range(5)]
    assert len(fake_usernames) == len(set(fake_usernames))
