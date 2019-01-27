from io import StringIO

from django.core.management import call_command

from ..management.commands import createfakefollowers
from ..users import get_fake_user


def test_management_command_creates_fake_followers_for_two_users(user, other_user):
    call_command(createfakefollowers.Command(), stdout=StringIO())


def test_management_command_creates_fake_followers_for_multiple_users(db, fake):
    [get_fake_user(fake) for i in range(10)]
    call_command(createfakefollowers.Command(), stdout=StringIO())


def test_management_command_displays_error_if_no_users_exist(db):
    stderr = StringIO()
    call_command(createfakefollowers.Command(), stderr=stderr)
    stderr.seek(0)
    assert stderr.read()


def test_management_command_displays_error_if_only_one_user_exist(user):
    stderr = StringIO()
    call_command(createfakefollowers.Command(), stderr=stderr)
    stderr.seek(0)
    assert stderr.read()
