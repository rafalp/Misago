from django.test import TestCase

from misago.core import threadstore
from misago.core.cache import cache


class MisagoTestCase(TestCase):
    """
    TestCase class that empties global state before and after each test
    """
    def clear_state(self):
        cache.clear()
        threadstore.clear()

    def setUp(self):
        super(MisagoTestCase, self).setUp()
        self.clear_state()

    def tearDown(self):
        self.clear_state()
        super(MisagoTestCase, self).tearDown()
