from django.test import TestCase
from misago.views.utils import is_request_to_misago

class MisagoExceptionHandlerTests(TestCase):
    def test_is_request_to_misago(self):
        """is_request_to_misago correctly detects requests directed at Misago"""
        self.fail("Not yet implemented")
