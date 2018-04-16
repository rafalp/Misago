from django.core import exceptions as django_exceptions
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import TestCase

from misago.api import exceptionhandler
from misago.core.exceptions import Banned
from misago.users.models import Ban


INVALID_EXCEPTIONS = [
    django_exceptions.ObjectDoesNotExist,
    django_exceptions.ViewDoesNotExist,
    TypeError,
    ValueError,
    KeyError,
]


class HandleAPIExceptionTests(TestCase):
    def test_banned(self):
        """banned exception is correctly handled"""
        ban = Ban(user_message="This is test ban!")

        response = exceptionhandler.handle_api_exception(Banned(ban), None)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail']['html'], "<p>This is test ban!</p>")
        self.assertIn('expires_on', response.data)

    def test_permission_denied(self):
        """permission denied exception is correctly handled"""
        response = exceptionhandler.handle_api_exception(PermissionDenied(), None)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': "Permission denied."})

    def test_permission_denied_message(self):
        """permission denied with message is correctly handled"""
        exception = PermissionDenied("You shall not pass!")
        response = exceptionhandler.handle_api_exception(exception, None)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': "You shall not pass!"})

    def test_not_found(self):
        """exception handler sets NOT FOUND as default message for 404"""
        response = exceptionhandler.handle_api_exception(Http404(), None)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'detail': 'NOT FOUND'})

    def test_not_found_message(self):
        """exception handler hides custom message behind 404 error"""
        response = exceptionhandler.handle_api_exception(Http404("Nada!"), None)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'detail': 'NOT FOUND'})

    def test_unhandled_exception(self):
        """our exception handler is not interrupting other exceptions"""
        for exception in INVALID_EXCEPTIONS:
            response = exceptionhandler.handle_api_exception(exception(), None)
            self.assertIsNone(response)
