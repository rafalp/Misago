from django.test import TestCase
from django.http import Http404 as DjHttp404
from django.core import exceptions as django_exceptions
from misago.views import exceptions as misago_exceptions
from misago.views.exceptions import handler


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


class MisagoExceptionHandlerTests(TestCase):
    def test_misago_exception_list_valid(self):
        """MISAGO_EXCEPTIONS list is valid"""
        self.assertEqual(len(misago_exceptions.MISAGO_EXCEPTIONS),
                         len(misago_exceptions.__all__))

        for exception in misago_exceptions.MISAGO_EXCEPTIONS:
            if exception.__name__ not in  misago_exceptions.__all__:
                self.fail("%s is registered in "
                          "misago.exceptions.MISAGO_EXCEPTIONS but not in "
                          "misago.exceptions.__all__" % exception.__name__)

    def test_misago_exceptions_detection(self):
        """Misago exception handler recognizes Misago exceptions"""
        for exception in misago_exceptions.MISAGO_EXCEPTIONS:
            try:
                raise exception()
            except exception as e:
                self.assertTrue(handler.is_misago_exception(e))

    def test_django_exceptions_detection(self):
        """Misago exception handler fails to recognize Django exceptions"""
        for exception in DJANGO_EXCEPTIONS:
            try:
                raise exception()
            except exception as e:
                self.assertFalse(handler.is_misago_exception(e))

    def test_python_exceptions_detection(self):
        """Misago exception handler fails to recognize Python exceptions"""
        for exception in PYTHON_EXCEPTIONS:
            try:
                raise exception()
            except exception as e:
                self.assertFalse(handler.is_misago_exception(e))

    def test_exception_handlers_list(self):
        """EXCEPTION_HANDLERS length matches that of MISAGO_EXCEPTIONS"""
        self.assertEqual(len(misago_exceptions.MISAGO_EXCEPTIONS),
                         len(handler.EXCEPTION_HANDLERS))

    def test_get_exception_handler(self):
        """Exception handler has handler for every Misago exception"""
        for exception in misago_exceptions.MISAGO_EXCEPTIONS:
            try:
                handler.get_exception_handler(exception())
            except ValueError:
                self.fail(
                    "%s has no exception handler defined " % exception.__name__)

    def test_handle_http404_exception(self):
        """Exception handler corrently turns Http404 exception into response"""
        self.fail("misago.views.exceptions.handler.handle_http404_exception "
                  "has not been implmented.")

    def test_handle_outdated_url_exception(self):
        """Exception handler corrently turns Misago exceptions into responses"""
        self.fail("misago.views.exceptionshandler.handle_outdated_url_exception "
                  "has not been implmented.")

    def test_handle_permission_denied_exception(self):
        """Exception handler corrently turns Misago exceptions into responses"""
        self.fail("misago.views.exceptions.handler.handle_"
                  "permission_denied_exception has not been implmented.")

    def test_handle_misago_exception(self):
        """Exception handler corrently turns Misago exceptions into responses"""
        self.fail("misago.views.exceptions.handler.handle_misago_exception has "
                  "not been implmented.")
