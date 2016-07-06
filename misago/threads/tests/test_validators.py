from django.core.exceptions import ValidationError
from django.test import TestCase

from misago.conf import settings
from misago.threads.validators import validate_title


class ValidateTitleTests(TestCase):
    def test_valid_titles(self):
        """validate_title is ok with valid titles"""
        VALID_TITLES = (
            'Lorem ipsum dolor met',
            '123 456 789 112'
            'Ugabugagagagagaga',
        )

        for title in VALID_TITLES:
            validate_title(title)

    def test_too_short_title(self):
        """too short title is unblocked"""
        with self.assertRaises(ValidationError):
            title = 'a' * settings.thread_title_length_min
            validate_title(title[1:])

    def test_too_long_title(self):
        """too long title is unblocked"""
        with self.assertRaises(ValidationError):
            title = 'a' * settings.thread_title_length_max
            validate_title(title * 2)

    def test_unsluggable_title(self):
        """unsluggable title is blocked"""
        with self.assertRaises(ValidationError):
            title = '--' * settings.thread_title_length_min
            validate_title(title)
