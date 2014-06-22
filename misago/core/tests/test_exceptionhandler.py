from django.core import exceptions as django_exceptions
from django.test import TestCase
from misago.core import exceptionhandler


INVALID_EXCEPTIONS = (
    django_exceptions.ObjectDoesNotExist,
    django_exceptions.ViewDoesNotExist,
    TypeError,
    ValueError,
    KeyError,
)


class IsMisagoExceptionTests(TestCase):
    def test_is_misago_exception_true_for_handled_exceptions(self):
        """
        exceptionhandler.is_misago_exception recognizes handled exceptions
        """
        for exception in exceptionhandler.HANDLED_EXCEPTIONS:
            try:
                raise exception()
            except exception as e:
                self.assertTrue(exceptionhandler.is_misago_exception(e))

    def test_is_misago_exception_false_for_not_handled_exceptions(self):
        """
        exceptionhandler.is_misago_exception fails to recognize other
        exceptions
        """
        for exception in INVALID_EXCEPTIONS:
            try:
                raise exception()
            except exception as e:
                self.assertFalse(exceptionhandler.is_misago_exception(e))


class GetExceptionHandlerTests(TestCase):
    def test_exception_handlers_list(self):
        """HANDLED_EXCEPTIONS length matches that of EXCEPTION_HANDLERS"""
        self.assertEqual(len(exceptionhandler.HANDLED_EXCEPTIONS),
                         len(exceptionhandler.EXCEPTION_HANDLERS))

    def test_get_exception_handler_for_handled_exceptions(self):
        """Exception handler has correct handler for every Misago exception"""
        for exception in exceptionhandler.HANDLED_EXCEPTIONS:
            exceptionhandler.get_exception_handler(exception())

    def test_get_exception_handler_for_non_handled_exceptio(self):
        """Exception handler has no handler for non-supported exception"""
        for exception in INVALID_EXCEPTIONS:
            with self.assertRaises(ValueError):
                exceptionhandler.get_exception_handler(exception())
