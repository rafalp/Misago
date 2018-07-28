from django.test import TestCase, override_settings
from django.urls import reverse

from misago.admin.testutils import AdminTestCase
from misago.admin.views.index import check_misago_address


class AdminIndexViewTests(AdminTestCase):
    def test_view_returns_200(self):
        """admin index view returns 200"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertContains(response, self.user.username)

    def test_view_contains_address_check(self):
        """admin index view contains address check"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertContains(response, "MISAGO_ADDRESS")


class RequestMock(object):
    absolute_uri = 'https://misago-project.org/somewhere/'

    def build_absolute_uri(self, location):
        assert location == '/'
        return self.absolute_uri


request = RequestMock()
incorrect_address = 'http://somewhere.com'
correct_address = request.absolute_uri


class AdminIndexAddressCheckTests(TestCase):
    @override_settings(MISAGO_ADDRESS=None)
    def test_address_not_set(self):
        """check handles address not set"""
        result = check_misago_address(request)

        self.assertEqual(result, {
            'is_correct': False,
            'set_address': None,
            'correct_address': request.absolute_uri,
        })

    @override_settings(MISAGO_ADDRESS=incorrect_address)
    def test_address_set_invalid(self):
        """check handles incorrect address"""
        result = check_misago_address(request)

        self.assertEqual(result, {
            'is_correct': False,
            'set_address': incorrect_address,
            'correct_address': request.absolute_uri,
        })

    @override_settings(MISAGO_ADDRESS=correct_address)
    def test_address_set_valid(self):
        """check handles correct address"""
        result = check_misago_address(request)

        self.assertEqual(result, {
            'is_correct': True,
            'set_address': correct_address,
            'correct_address': request.absolute_uri,
        })
