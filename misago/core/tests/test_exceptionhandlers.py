from django.core import exceptions as django_exceptions
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import TestCase

from misago.core import exceptionhandler
from misago.core.exceptions import Banned
from misago.users.models import Ban


INVALID_EXCEPTIONS = [
    django_exceptions.ObjectDoesNotExist,
    django_exceptions.ViewDoesNotExist,
    TypeError,
    ValueError,
    KeyError,
]


class IsMisagoExceptionTests(TestCase):
    def test_is_misago_exception_true_for_handled_exceptions(self):
        """exceptionhandler.is_misago_exception recognizes handled exceptions"""
        for exception in exceptionhandler.HANDLED_EXCEPTIONS:
            self.assertTrue(exceptionhandler.is_misago_exception(exception()))

    def test_is_misago_exception_false_for_not_handled_exceptions(self):
        """exceptionhandler.is_misago_exception fails to recognize other exceptions"""
        for exception in INVALID_EXCEPTIONS:
            self.assertFalse(exceptionhandler.is_misago_exception(exception()))


class GetExceptionHandlerTests(TestCase):
    def test_exception_handlers_list(self):
        """HANDLED_EXCEPTIONS length matches that of EXCEPTION_HANDLERS"""
        self.assertEqual(
            len(exceptionhandler.HANDLED_EXCEPTIONS), len(exceptionhandler.EXCEPTION_HANDLERS)
        )

    def test_get_exception_handler_for_handled_exceptions(self):
        """Exception handler has correct handler for every Misago exception"""
        for exception in exceptionhandler.HANDLED_EXCEPTIONS:
            exceptionhandler.get_exception_handler(exception())

    def test_get_exception_handler_for_non_handled_exceptio(self):
        """Exception handler has no handler for non-supported exception"""
        for exception in INVALID_EXCEPTIONS:
            with self.assertRaises(ValueError):
                exceptionhandler.get_exception_handler(exception())


class HandleAPIExceptionTests(TestCase):
    def test_banned(self):
        """banned exception is correctly handled"""
        ban = Ban(user_message="This is test ban!")

        response = exceptionhandler.handle_api_exception(Banned(ban), None)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['ban']['message']['html'], "<p>This is test ban!</p>")

    def test_permission_denied(self):
        """permission denied exception is correctly handled"""
        response = exceptionhandler.handle_api_exception(PermissionDenied(), None)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], "Permission denied.")

    def test_permission_message_denied(self):
        """permission denied with message is correctly handled"""
        exception = PermissionDenied("You shall not pass!")
        response = exceptionhandler.handle_api_exception(exception, None)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], "You shall not pass!")

    def test_unhandled_exception(self):
        """our exception handler is not interrupting other exceptions"""
        for exception in INVALID_EXCEPTIONS:
            response = exceptionhandler.handle_api_exception(exception(), None)
            self.assertIsNone(response)

        response = exceptionhandler.handle_api_exception(Http404(), None)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], "Not found.")
