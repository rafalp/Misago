from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from misago.core import threadstore
from misago.core.middleware.threadstore import ThreadStoreMiddleware


class ThreadStoreTests(TestCase):
    def setUp(self):
        threadstore.clear()

    def test_set_get_value(self):
        """It's possible to set and get value from threadstore"""
        self.assertEqual(threadstore.get('knights_say'), None)

        returned_value = threadstore.set('knights_say', 'Ni!')
        self.assertEqual(returned_value, 'Ni!')
        self.assertEqual(threadstore.get('knights_say'), 'Ni!')

    def test_clear_store(self):
        """clear cleared threadstore"""
        self.assertEqual(threadstore.get('the_fish'), None)
        threadstore.set('the_fish', 'Eric')
        self.assertEqual(threadstore.get('the_fish'), 'Eric')
        threadstore.clear()
        self.assertEqual(threadstore.get('the_fish'), None)


class ThreadStoreMiddlewareTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('misago:index'))

    def test_middleware_clears_store_on_response_exception(self):
        """Middleware cleared store on response"""

        threadstore.set('any_chesse', 'Nope')
        middleware = ThreadStoreMiddleware()
        response = middleware.process_response(self.request, 'FakeResponse')
        self.assertEqual(response, 'FakeResponse')
        self.assertEqual(threadstore.get('any_chesse'), None)
