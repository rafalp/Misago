from unittest.mock import Mock

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Ban
from ..test import create_test_user
from ..validators import (
    validate_email,
    validate_email_available,
    validate_email_banned,
    validate_gmail_email,
    validate_username,
    validate_username_available,
    validate_username_banned,
    validate_username_content,
    validate_username_length,
)


class ValidateEmailAvailableTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")

    def test_valid_email(self):
        """validate_email_available allows available emails"""
        validate_email_available("other@example.com")
        validate_email_available(self.user.email, exclude=self.user)

    def test_invalid_email(self):
        """validate_email_available disallows unvailable emails"""
        with self.assertRaises(ValidationError):
            validate_email_available(self.user.email)


class ValidateEmailBannedTests(TestCase):
    def setUp(self):
        Ban.objects.create(check_type=Ban.EMAIL, banned_value="ban@test.com")

    def test_unbanned_name(self):
        """unbanned email passes validation"""
        validate_email_banned("noban@test.com")

    def test_banned_name(self):
        """banned email fails validation"""
        with self.assertRaises(ValidationError):
            validate_email_banned("ban@test.com")


class ValidateEmailTests(TestCase):
    def test_validate_email(self):
        """validate_email has no crashes"""
        validate_email("user@example.com")
        with self.assertRaises(ValidationError):
            validate_email("*")


class ValidateUsernameTests(TestCase):
    def test_validate_username(self):
        """validate_username has no crashes"""
        settings = Mock(username_length_min=1, username_length_max=5)
        validate_username(settings, "LeBob")
        with self.assertRaises(ValidationError):
            validate_username(settings, "*")


class ValidateUsernameAvailableTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")

    def test_valid_name(self):
        """validate_username_available allows available names"""
        validate_username_available("OtherUser")
        validate_username_available(self.user.username, exclude=self.user)

    def test_invalid_name(self):
        """validate_username_available disallows unvailable names"""
        with self.assertRaises(ValidationError):
            validate_username_available(self.user.username)


class ValidateUsernameBannedTests(TestCase):
    def setUp(self):
        Ban.objects.create(check_type=Ban.USERNAME, banned_value="Ban")

    def test_unbanned_name(self):
        """unbanned name passes validation"""
        validate_username_banned("User")

    def test_banned_name(self):
        """banned name fails validation"""
        with self.assertRaises(ValidationError):
            validate_username_banned("Ban")


class ValidateUsernameContentTests(TestCase):
    def test_valid_name(self):
        """validate_username_content allows valid names"""
        validate_username_content("123")
        validate_username_content("User")
        validate_username_content("User123")

    def test_invalid_name(self):
        """validate_username_content disallows invalid names"""
        with self.assertRaises(ValidationError):
            validate_username_content("!")
        with self.assertRaises(ValidationError):
            validate_username_content("User!")
        with self.assertRaises(ValidationError):
            validate_username_content("John Doe")
        with self.assertRaises(ValidationError):
            validate_username_content("Rafał")
        with self.assertRaises(ValidationError):
            validate_username_content("初音 ミク")


class ValidateUsernameLengthTests(TestCase):
    def test_valid_name(self):
        """validate_username_length allows valid names"""
        settings = Mock(username_length_min=1, username_length_max=5)
        validate_username_length(settings, "a" * settings.username_length_min)
        validate_username_length(settings, "a" * settings.username_length_max)

    def test_invalid_name(self):
        """validate_username_length disallows invalid names"""
        settings = Mock(username_length_min=1, username_length_max=5)
        with self.assertRaises(ValidationError):
            validate_username_length(settings, "a" * (settings.username_length_min - 1))
        with self.assertRaises(ValidationError):
            validate_username_length(settings, "a" * (settings.username_length_max + 1))


class ValidateGmailEmailTests(TestCase):
    def test_validate_gmail_email(self):
        """validate_gmail_email spots spammy gmail address"""
        added_errors = {}

        def add_errors(field_name, errors):
            added_errors[field_name] = errors

        validate_gmail_email(None, {}, add_errors)
        validate_gmail_email(None, {"email": "invalid-email"}, add_errors)
        validate_gmail_email(None, {"email": "the.valid.email@gmail.com"}, add_errors)
        validate_gmail_email(None, {"email": "the.valid.email@hotmail.com"}, add_errors)

        self.assertFalse(added_errors)

        validate_gmail_email(
            None, {"email": "the.s.p.a.m.my.e.ma.il@gmail.com"}, add_errors
        )
        self.assertTrue(added_errors)
