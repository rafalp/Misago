from django.test import override_settings
from django.urls import reverse

from ...test import assert_contains
from ..views.index import check_misago_address

admin_link = reverse("misago:admin:index")


def test_view_has_no_showstoppers(admin_client):
    response = admin_client.get(admin_link)
    assert response.status_code == 200


def test_view_has_misago_address_check(admin_client):
    response = admin_client.get(admin_link)
    assert_contains(response, "MISAGO_ADDRESS")


class RequestMock:
    absolute_uri = "https://misago-project.org/somewhere/"

    def build_absolute_uri(self, location):
        assert location == "/"
        return self.absolute_uri


request = RequestMock()
incorrect_address = "http://somewhere.com"
correct_address = request.absolute_uri


@override_settings(MISAGO_ADDRESS=None)
def test_misago_address_check_handles_setting_not_configured():
    result = check_misago_address(request)
    assert result == {
        "is_correct": False,
        "set_address": None,
        "correct_address": request.absolute_uri,
    }


@override_settings(MISAGO_ADDRESS=incorrect_address)
def test_misago_address_check_detects_invalid_address_configuration():
    result = check_misago_address(request)
    assert result == {
        "is_correct": False,
        "set_address": incorrect_address,
        "correct_address": request.absolute_uri,
    }


@override_settings(MISAGO_ADDRESS=correct_address)
def test_misago_address_check_detects_valid_address_configuration():
    result = check_misago_address(request)
    assert result == {
        "is_correct": True,
        "set_address": correct_address,
        "correct_address": request.absolute_uri,
    }
