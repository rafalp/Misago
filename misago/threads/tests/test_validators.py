from rest_framework import serializers

from django.core.exceptions import ValidationError
from django.test import TestCase

from misago.conf import settings
from misago.core.testproject.validators import test_post_validator
from misago.threads.validators import (
    load_post_validators, validate_post, validate_post_length, validate_title)


class LoadPostValidatorsTests(TestCase):
    def test_empty_list(self):
        """empty validator list returns no validators"""
        self.assertEqual(load_post_validators([]), [])

    def test_load_validator(self):
        """function loads validator from list"""
        validators = load_post_validators([
            'misago.core.testproject.validators.test_post_validator',
        ])

        self.assertEqual(validators, [test_post_validator])

    def test_load_nonexistant_validator(self):
        """nonexistant validator raises"""
        with self.assertRaises(ImportError):
            validators = load_post_validators([
                'misago.core.yaddayadda.yaddayadda',
            ])

        with self.assertRaises(AttributeError):
            validators = load_post_validators([
                'misago.core.yaddayadda',
            ])


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
