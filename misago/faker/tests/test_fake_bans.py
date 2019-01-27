from ...users.models import Ban
from ..bans import get_fake_email_ban, get_fake_ip_ban, get_fake_username_ban


def test_fake_username_ban_can_be_created(db, fake):
    assert get_fake_username_ban(fake)
    Ban.objects.get(check_type=Ban.USERNAME)


def test_fake_email_ban_can_be_created(db, fake):
    assert get_fake_email_ban(fake)
    Ban.objects.get(check_type=Ban.EMAIL)


def test_fake_ip_ban_can_be_created(db, fake):
    assert get_fake_ip_ban(fake)
    Ban.objects.get(check_type=Ban.IP)
