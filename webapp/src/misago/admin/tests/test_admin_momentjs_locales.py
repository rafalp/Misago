from django.urls import reverse
from django.utils import translation

from ...test import assert_contains, assert_not_contains
from ..momentjs import MISAGO_ADMIN_MOMENT_LOCALES, get_admin_locales


def test_admin_loads_locales_list():
    assert get_admin_locales()


def test_admin_locales_list_include_some_valid_locales():
    assert "pl" in MISAGO_ADMIN_MOMENT_LOCALES
    assert "en-gb" in MISAGO_ADMIN_MOMENT_LOCALES


def test_moment_locale_is_not_included_for_english(admin_client):
    with translation.override("en"):
        response = admin_client.get(reverse("misago:admin:index"))
        assert_not_contains(response, "misago/admin/momentjs/")


def test_moment_locale_is_included_for_british_english(admin_client):
    with translation.override("en_GB"):
        response = admin_client.get(reverse("misago:admin:index"))
        assert_contains(response, "misago/admin/momentjs/en-gb.js")
