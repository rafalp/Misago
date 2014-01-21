from django.test import TestCase
from django.http import Http404 as DjHttp404
from django.core import exceptions as django_exceptions
from misago.core import exceptionhandler, exceptions as misago_exceptions


DJANGO_EXCEPTIONS = (
    django_exceptions.PermissionDenied,
    django_exceptions.ViewDoesNotExist,
    DjHttp404,
)


PYTHON_EXCEPTIONS = (
    TypeError,
    ValueError,
    KeyError,
)


class ExceptionHandlerIsMisagoExceptionTestCase(TestCase):
    def test_misago_exception_list_valid(self):
        """Misago exception handler MISAGO_EXCEPTIONS list is valid"""
        self.assertEqual(len(exceptionhandler.MISAGO_EXCEPTIONS),
                         len(misago_exceptions.__all__))

    def test_misago_exceptions_detection(self):
        """Misago exception handler correctly identifies Misago exceptions"""
        for exception in exceptionhandler.MISAGO_EXCEPTIONS:
            try:
                raise exception()
            except exception as e:
                self.assertTrue(exceptionhandler.is_misago_exception(e))

    def test_django_exceptions_detection(self):
        """Misago exception handler correctly identifies Django exceptions"""
        for exception in DJANGO_EXCEPTIONS:
            try:
                raise exception()
            except exception as e:
                self.assertFalse(exceptionhandler.is_misago_exception(e))

    def test_python_exceptions_detection(self):
        """Misago exception handler correctly identifies Python exceptions"""
        for exception in PYTHON_EXCEPTIONS:
            try:
                raise exception()
            except exception as e:
                self.assertFalse(exceptionhandler.is_misago_exception(e))
