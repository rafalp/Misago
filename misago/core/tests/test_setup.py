import os

from django.test import TestCase
from django.utils.encoding import smart_str

from misago.core import setup


class MockParser(object):
    def error(self, message):
        raise ValueError(message)


class SetupTests(TestCase):
    def test_validate_project_name(self):
        """validate_project_name identifies incorrect names correctly"""
        mock_parser = MockParser()

        with self.assertRaises(ValueError):
            setup.validate_project_name(mock_parser, '-lorem')

        with self.assertRaises(ValueError):
            setup.validate_project_name(mock_parser, 'django')

        with self.assertRaises(ValueError):
            setup.validate_project_name(mock_parser, 'dja-ngo')

        with self.assertRaises(ValueError):
            setup.validate_project_name(mock_parser, '123')

        self.assertTrue(setup.validate_project_name(mock_parser, 'myforum'))
        self.assertTrue(setup.validate_project_name(mock_parser, 'myforum123'))

    def test_get_misago_project_template(self):
        """get_misago_project_template returns correct path to template"""
        misago_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        test_project_path = os.path.join(misago_path, 'project_template')

        self.assertEqual(
            smart_str(setup.get_misago_project_template()), smart_str(test_project_path)
        )
