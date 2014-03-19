#-*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.test import TestCase
from misago.users.validators import (validate_username_available,
                                     validate_username_content,
                                     validate_username_length,
                                     validate_username)


class ValidateContentTests(TestCase):
    def test_valid_names(self):
        """validate_username_content allows valid names"""
        validate_username_content('123')
        validate_username_content('Bob')
        validate_username_content('Bob123')

    def test_invalid_names(self):
        """validate_username_content disallows invalid names"""
        with self.assertRaises(ValidationError):
            validate_username_content('!')
        with self.assertRaises(ValidationError):
            validate_username_content('Bob!')
        with self.assertRaises(ValidationError):
            validate_username_content('Bob Boberson')
        with self.assertRaises(ValidationError):
            validate_username_content(u'Rafał')
        with self.assertRaises(ValidationError):
            validate_username_content(u'初音 ミク')
