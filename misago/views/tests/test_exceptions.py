from django.http import Http404
from django.core import exceptions as django_exceptions
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.test.client import RequestFactory
from misago.views.exceptions import OutdatedSlug
from misago.views import exceptionhandler


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

    def test_get_exception_handler(self):
        """Exception handler has correct handler for every Misago exception"""
        for exception in exceptionhandler.HANDLED_EXCEPTIONS:
            try:
                exceptionhandler.get_exception_handler(exception())
            except ValueError:
                self.fail(
                    "%s has no exception handler defined" % exception.__name__)


class HandleHttp404ExceptionTests(TestCase):
    def setUp(self):
        self.exception = Http404()
        self.request = RequestFactory().get('/')

    def test_get_handle_http404_exception(self):
        """get_exception_handler returns correct Http404 exception handler"""
        found_handler = exceptionhandler.get_exception_handler(self.exception)
        self.assertEqual(
            found_handler, exceptionhandler.handle_http404_exception)

        response = found_handler(self.request, self.exception)
        self.assertEqual(response.status_code, 404)

    def test_handle_http404_exception(self):
        """handle_misago_exception handles Http404 exception correctly"""
        response = exceptionhandler.handle_misago_exception(
            self.request, self.exception)
        self.assertEqual(response.status_code, 404)


class HandleOutdatedSlugExceptionTests(TestCase):
    def setUp(self):
        self.exception = OutdatedSlug()
        self.request = RequestFactory().get('/')

    def test_get_handle_outdated_slug_exception(self):
        """
        get_exception_handler returns correct OutdatedSlug exception handler
        """
        found_handler = exceptionhandler.get_exception_handler(self.exception)
        self.assertEqual(
            found_handler, exceptionhandler.handle_outdated_slug_exception)

        response = found_handler(self.request, self.exception)
        self.assertEqual(response.status_code, 301)

    def test_handle_outdated_slug_exception(self):
        """
        handle_misago_exception handles OutdatedSlug exception correctly
        """
        response = exceptionhandler.handle_misago_exception(
            self.request, self.exception)
        self.assertEqual(response.status_code, 301)


class HandlePermissionDeniedExceptionTests(TestCase):
    def setUp(self):
        self.exception_message = "Page access not allowed"
        self.exception = PermissionDenied(self.exception_message)
        self.request = RequestFactory().get('/')

    def test_get_handle_permission_denied_exception(self):
        """
        get_exception_handler returns correct PermissionDenied exception
        handler
        """
        found_handler = exceptionhandler.get_exception_handler(self.exception)
        self.assertEqual(
            found_handler, exceptionhandler.handle_permission_denied_exception)

        response = found_handler(self.request, self.exception)
        self.assertIn(self.exception_message, response.content)
        self.assertEqual(response.status_code, 403)

    def test_handle_permission_denied_exception(self):
        """
        handle_misago_exception handles PermissionDenied exception correctly
        """
        response = exceptionhandler.handle_misago_exception(
            self.request, self.exception)
        self.assertIn(self.exception_message, response.content)
        self.assertEqual(response.status_code, 403)
