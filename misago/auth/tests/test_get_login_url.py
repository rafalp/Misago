from django.urls import reverse
from django.test import override_settings

from ..loginurl import get_login_url


@override_settings(LOGIN_URL="misago:login")
def test_get_login_url_returns_reversed_url():
    assert get_login_url() == reverse("misago:login")


@override_settings(LOGIN_URL="/other/login/")
def test_get_login_url_returns_absolute_url():
    assert get_login_url() == "/other/login/"
