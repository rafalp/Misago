from django.core.exceptions import ValidationError
from django.test import TestCase

from misago.conf import settings
from misago.threads.validators import validate_post_length, validate_title


class ValidatePostLengthTests(TestCase):
    def test_valid_post(self):
        """valid post passes validation"""
        validate_post_length("Lorem ipsum dolor met sit amet elit.")

    def test_empty_post(self):
        """empty post is rejected"""
        with self.assertRaises(ValidationError):
            validate_post_length("")

    def test_too_short_post(self):
        """too short post is rejected"""
        with self.assertRaises(ValidationError):
            post = 'a' * settings.post_length_min
            validate_post_length(post[1:])

    def test_too_long_post(self):
        """too long post is rejected"""
        with self.assertRaises(ValidationError):
            post = 'a' * settings.post_length_max
            validate_post_length(post * 2)


class ValidateTitleTests(TestCase):
    def test_valid_titles(self):
        """validate_title is ok with valid titles"""
        VALID_TITLES = [
            'Lorem ipsum dolor met',
            '123 456 789 112'
            'Ugabugagagagagaga',
        ]

        for title in VALID_TITLES:
            validate_title(title)

    def test_empty_title(self):
        """empty title is rejected"""
        with self.assertRaises(ValidationError):
            validate_title("")

    def test_too_short_title(self):
        """too short title is rejected"""
        with self.assertRaises(ValidationError):
            title = 'a' * settings.thread_title_length_min
            validate_title(title[1:])

    def test_too_long_title(self):
        """too long title is rejected"""
        with self.assertRaises(ValidationError):
            title = 'a' * settings.thread_title_length_max
            validate_title(title * 2)

    def test_unsluggable_title(self):
        """unsluggable title is rejected"""
        with self.assertRaises(ValidationError):
            title = '--' * settings.thread_title_length_min
            validate_title(title)
