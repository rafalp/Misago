from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from misago.readtracker.dates import is_date_tracked


class MockUser(object):
    def __init__(self):
        self.reads_cutoff = timezone.now()


class ReadTrackerDatesTests(TestCase):
    def test_is_date_tracked(self):
        """is_date_tracked validates dates"""
        self.assertFalse(is_date_tracked(MockUser(), None))

        past_date = timezone.now() - timedelta(minutes=10)
        self.assertFalse(is_date_tracked(MockUser(), past_date))

        future_date = timezone.now() + timedelta(minutes=10)
        self.assertTrue(is_date_tracked(MockUser(), future_date))
