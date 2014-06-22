#-*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TransactionTestCase
from misago.conf import settings
from misago.users.validators import (validate_email, validate_email_available,
                                     validate_password,
                                     validate_username,
                                     validate_username_available,
                                     validate_username_content,
                                     validate_username_length)


class ValidateUsernameLengthTests(TransactionTestCase):
    serialized_rollback = True

    def test_valid_name(self):
        """validate_username_length allows valid names"""
        validate_username_length('a' * settings.username_length_min)
        validate_username_length('a' * settings.username_length_max)

    def test_invalid_name(self):
        """validate_username_length disallows invalid names"""
        with self.assertRaises(ValidationError):
            validate_username_length('a' * (settings.username_length_min - 1))
        with self.assertRaises(ValidationError):
            validate_username_length('a' * (settings.username_length_max + 1))
