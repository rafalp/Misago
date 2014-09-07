from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from misago.readtracker.dates import cutoff_date, is_date_tracked


class ReadTrackerDatesTests(TestCase):
    def test_cutoff_date(self):
        """cutoff_date returns cut off date"""
        cutoff = cutoff_date()
        self.assertTrue(cutoff < timezone.now())

    def test_is_date_tracked(self):
        """is_date_tracked validates dates"""
        self.assertFalse(is_date_tracked(None))
        self.assertFalse(is_date_tracked(cutoff_date() - timedelta(seconds=1)))
        self.assertTrue(is_date_tracked(cutoff_date() + timedelta(minutes=1)))
