#-*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from misago.conf import settings
from misago.users.validators import (validate_email, validate_email_available,
                                     validate_password,
                                     validate_username,
                                     validate_username_available,
                                     validate_username_content,
                                     validate_username_length)


class ValidateEmailAvailableTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.test_user = User.objects.create_user('EricTheFish',
                                                  'eric@test.com',
                                                  'pass123')

    def test_valid_email(self):
        """validate_email_available allows available emails"""
        validate_email_available('bob@boberson.com')

    def test_invalid_email(self):
        """validate_email_available disallows unvailable emails"""
        with self.assertRaises(ValidationError):
            validate_email_available(self.test_user.email)


class ValidateEmailTests(TestCase):
    def test_validate_email(self):
        """validate_email has no crashes"""
        validate_email('bob@boberson.com')
        with self.assertRaises(ValidationError):
            validate_email('*')


class ValidatePasswordTests(TestCase):
    def test_valid_password(self):
        """validate_password allows valid password"""
        validate_password('A' * (settings.password_length_min + 1))

    def test_invalid_name(self):
        """validate_password disallows invalid password"""
        with self.assertRaises(ValidationError):
            validate_password('A' * (settings.password_length_min - 1))


class ValidateUsernameTests(TestCase):
    def test_validate_username(self):
        """validate_username has no crashes"""
        validate_username('LeBob')
        with self.assertRaises(ValidationError):
            validate_username('*')


class ValidateUsernameAvailableTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.test_user = User.objects.create_user('EricTheFish',
                                                  'eric@test.com',
                                                  'pass123')

    def test_valid_name(self):
        """validate_username_available allows available names"""
        validate_username_available('BobBoberson')

    def test_invalid_name(self):
        """validate_username_available disallows unvailable names"""
        with self.assertRaises(ValidationError):
            validate_username_available(self.test_user.username)


class ValidateUsernameContentTests(TestCase):
    def test_valid_name(self):
        """validate_username_content allows valid names"""
        validate_username_content('123')
        validate_username_content('Bob')
        validate_username_content('Bob123')

    def test_invalid_name(self):
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


class ValidateUsernameLengthTests(TestCase):
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
