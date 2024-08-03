from urllib.parse import quote_plus

from django.urls import reverse

from ..nextpage import clean_next_page_url, get_next_page_url


def test_get_next_page_url_returns_clean_url_from_post(rf):
    request = rf.get(
        reverse("misago:login"),
        {"next": reverse("misago:account-preferences")},
    )

    assert get_next_page_url(request) == reverse("misago:account-preferences")


def test_get_next_page_url_returns_clean_url_from_get(rf):
    request = rf.get(
        reverse("misago:login")
        + "?next="
        + quote_plus(reverse("misago:account-preferences")),
    )

    assert get_next_page_url(request) == reverse("misago:account-preferences")


def test_get_next_page_url_returns_clean_url_from_post_before_get(rf):
    request = rf.get(
        reverse("misago:login") + "?next=" + quote_plus(reverse("misago:index")),
        {"next": reverse("misago:account-preferences")},
    )

    assert get_next_page_url(request) == reverse("misago:account-preferences")


def test_clean_next_page_url_returns_valid_relative_misago_url(rf):
    request = rf.get(reverse("misago:login"))
    next_page_url = clean_next_page_url(request, reverse("misago:account-preferences"))
    assert next_page_url == reverse("misago:account-preferences")


def test_clean_next_page_url_returns_none_if_relative_url_has_no_match(rf):
    request = rf.get(reverse("misago:login"))
    next_page_url = clean_next_page_url(request, "/wp-admin.php")
    assert next_page_url is None


def test_clean_next_page_url_returns_valid_absolute_url(rf):
    request = rf.get(reverse("misago:login"))
    next_page_url = clean_next_page_url(request, "http://testserver/account/")
    assert next_page_url == "/account/"


def test_clean_next_page_url_returns_valid_absolute_url_with_querystring(rf):
    request = rf.get(reverse("misago:login"))
    next_page_url = clean_next_page_url(request, "http://testserver/account/?query=1")
    assert next_page_url == "/account/?query=1"


def test_clean_next_page_url_returns_none_for_absolute_url_with_invalid_host(rf):
    request = rf.get(reverse("misago:login"))
    next_page_url = clean_next_page_url(request, "http://example.com/account/?query=1")
    assert next_page_url is None


def test_clean_next_page_url_returns_none_for_absolute_url_with_invalid_path(rf):
    request = rf.get(reverse("misago:login"))
    next_page_url = clean_next_page_url(request, "http://testserver/wp-admin.php")
    assert next_page_url is None
