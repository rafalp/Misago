from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from misago.conf import settings
from misago.readtracker.dates import get_cutoff_date, is_date_tracked


class MockUser(object):
    is_authenticated = True

    def __init__(self):
        self.joined_on = timezone.now()


class MockAnonymousUser(object):
    is_authenticated = False


class ReadTrackerDatesTests(TestCase):
    def test_get_cutoff_date_no_user(self):
        """get_cutoff_date utility works without user argument"""
        valid_cutoff_date = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        returned_cutoff_date = get_cutoff_date()

        self.assertTrue(returned_cutoff_date > valid_cutoff_date)

    def test_get_cutoff_date_user(self):
        """get_cutoff_date utility works with user argument"""
        user = MockUser()

        valid_cutoff_date = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        returned_cutoff_date = get_cutoff_date(user)

        self.assertTrue(returned_cutoff_date > valid_cutoff_date)
        self.assertEqual(returned_cutoff_date, user.joined_on)

    def test_get_cutoff_date_user(self):
        """passing anonymous user to get_cutoff_date has no effect"""
        user = MockAnonymousUser()

        valid_cutoff_date = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)
        returned_cutoff_date = get_cutoff_date(user)

        self.assertTrue(returned_cutoff_date > valid_cutoff_date)

    def test_is_date_tracked(self):
        """is_date_tracked validates dates"""
        self.assertFalse(is_date_tracked(None, MockUser()))

        past_date = timezone.now() - timedelta(minutes=10)
        self.assertFalse(is_date_tracked(past_date, MockUser()))

        future_date = timezone.now() + timedelta(minutes=10)
        self.assertTrue(is_date_tracked(future_date, MockUser()))
