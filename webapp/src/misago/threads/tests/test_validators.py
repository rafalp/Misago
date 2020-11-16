from unittest.mock import Mock

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..validators import validate_post_length, validate_thread_title


class ValidatePostLengthTests(TestCase):
    def test_valid_post_length_passes_validation(self):
        """valid post passes validation"""
        settings = Mock(post_length_min=1, post_length_max=50)
        validate_post_length(settings, "Lorem ipsum dolor met sit amet elit.")

    def test_for_empty_post_validation_error_is_raised(self):
        """empty post is rejected"""
        settings = Mock(post_length_min=3)
        with self.assertRaises(ValidationError):
            validate_post_length(settings, "")

    def test_for_too_short_post_validation_error_is_raised(self):
        """too short post is rejected"""
        settings = Mock(post_length_min=3)
        with self.assertRaises(ValidationError):
            validate_post_length(settings, "a")

    def test_for_too_long_post_validation_error_is_raised(self):
        """too long post is rejected"""
        settings = Mock(post_length_min=1, post_length_max=2)
        with self.assertRaises(ValidationError):
            validate_post_length(settings, "abc")


class ValidateThreadTitleTests(TestCase):
    def test_valid_thread_titles_pass_validation(self):
        """validate_thread_title is ok with valid titles"""
        settings = Mock(thread_title_length_min=1, thread_title_length_max=50)

        VALID_TITLES = ["Lorem ipsum dolor met", "123 456 789 112", "Ugabugagagagagaga"]

        for title in VALID_TITLES:
            validate_thread_title(settings, title)

    def test_for_empty_thread_title_validation_error_is_raised(self):
        """empty title is rejected"""
        settings = Mock(thread_title_length_min=3)
        with self.assertRaises(ValidationError):
            validate_thread_title(settings, "")

    def test_for_too_short_thread_title_validation_error_is_raised(self):
        """too short title is rejected"""
        settings = Mock(thread_title_length_min=3)
        with self.assertRaises(ValidationError):
            validate_thread_title(settings, "a")

    def test_for_too_long_thread_title_validation_error_is_raised(self):
        """too long title is rejected"""
        settings = Mock(thread_title_length_min=1, thread_title_length_max=2)
        with self.assertRaises(ValidationError):
            validate_thread_title(settings, "abc")

    def test_for_unsluggable_thread_title_valdiation_error_is_raised(self):
        """unsluggable title is rejected"""
        settings = Mock(thread_title_length_min=1, thread_title_length_max=9)
        with self.assertRaises(ValidationError):
            validate_thread_title(settings, "-#%^&-")
