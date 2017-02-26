from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from misago.readtracker.dates import is_date_tracked


class MockUser(object):
    def __init__(self):
        self.joined_on = timezone.now()


class ReadTrackerDatesTests(TestCase):
    def test_is_date_tracked(self):
        """is_date_tracked validates dates"""
        self.assertFalse(is_date_tracked(None, MockUser()))

        past_date = timezone.now() - timedelta(minutes=10)
        self.assertFalse(is_date_tracked(past_date, MockUser()))

        future_date = timezone.now() + timedelta(minutes=10)
        self.assertTrue(is_date_tracked(future_date, MockUser()))

    def test_is_date_tracked_with_category_cutoff(self):
        """is_date_tracked validates dates using category cutoff"""
        self.assertFalse(is_date_tracked(None, MockUser()))
        past_date = timezone.now() + timedelta(minutes=10)

        category_cutoff = timezone.now() + timedelta(minutes=20)
        self.assertFalse(is_date_tracked(past_date, MockUser(), category_cutoff))

        category_cutoff = timezone.now() - timedelta(minutes=20)
        self.assertTrue(is_date_tracked(past_date, MockUser(), category_cutoff))
