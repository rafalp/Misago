from io import StringIO

from django.core.management import call_command

from ...cache.test import assert_invalidates_cache
from ...users import BANS_CACHE
from ...users.models import Ban
from ..management.commands import createfakebans


def test_management_command_creates_fake_bans(db):
    call_command(createfakebans.Command(), stdout=StringIO())
    assert Ban.objects.exists()


def test_management_command_invalidates_bans_cache(db):
    with assert_invalidates_cache(BANS_CACHE):
        call_command(createfakebans.Command(), stdout=StringIO())
