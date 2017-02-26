from django.core.exceptions import ValidationError
from django.test import TestCase

from misago.core.validators import validate_sluggable


class ValidateSluggableTests(TestCase):
    def test_error_messages_set(self):
        """custom error messages are set and used"""
        error_short = "I'm short custom error!"
        error_long = "I'm long custom error!"

        validator = validate_sluggable(error_short, error_long)

        self.assertEqual(validator.error_short, error_short)
        self.assertEqual(validator.error_long, error_long)

    def test_faulty_input_validation(self):
        """invalid values raise errors"""
        validator = validate_sluggable()

        with self.assertRaises(ValidationError):
            validator('!#@! !@#@')
        with self.assertRaises(ValidationError):
            validator(
                '!#@! !@#@ 1234567890 1234567890 1234567890 1234567890'
                '1234567890 1234567890 1234567890 1234567890 1234567890'
                '1234567890 1234567890 1234567890 1234567890 1234567890'
                '1234567890 1234567890 1234567890 1234567890 1234567890'
                '1234567890 1234567890 1234567890 1234567890 1234567890'
            )

    def test_valid_input_validation(self):
        """valid values don't raise errors"""
        validator = validate_sluggable()

        validator('Bob')
        validator('Lorem ipsum123!')
