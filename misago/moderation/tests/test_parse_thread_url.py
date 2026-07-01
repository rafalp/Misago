import pytest
from django.forms import ValidationError
from django.urls import reverse

from ..forms import THREAD_URLS, parse_thread_url


def test_parse_thread_url_returns_thread_id_from_valid_thread_link(rf):
    thread_id = parse_thread_url(
        "http://example.com"
        + reverse("misago:thread", kwargs={"thread_id": 123, "slug": "thread-slug"}),
        rf.get("/", HTTP_HOST="example.com"),
        THREAD_URLS,
    )

    assert thread_id == 123


def test_parse_thread_url_raises_validation_error_on_missing_hostname(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_url(
            reverse("misago:thread", kwargs={"thread_id": 123, "slug": "thread-slug"}),
            rf.get("/", HTTP_HOST="example.com"),
            THREAD_URLS,
        )

    assert exc_info.value.message == "Enter a valid link."


def test_parse_thread_url_raises_validation_error_on_missing_path(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_url(
            "http://example.com/",
            rf.get("/", HTTP_HOST="example.com"),
            THREAD_URLS,
        )

    assert exc_info.value.message == "Enter a valid link."


def test_parse_thread_url_raises_validation_error_on_invalid_hostname(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_url(
            "http://misago-project.org/"
            + reverse(
                "misago:thread", kwargs={"thread_id": 123, "slug": "thread-slug"}
            ),
            rf.get("/", HTTP_HOST="example.com"),
            THREAD_URLS,
        )

    assert exc_info.value.message == "Enter a link to this site."


def test_parse_thread_url_raises_validation_error_on_invalid_path(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_url(
            "http://example.com/invalid/",
            rf.get("/", HTTP_HOST="example.com"),
            THREAD_URLS,
        )

    assert exc_info.value.message == "Enter a valid thread link."


def test_parse_thread_url_raises_validation_error_on_path_being_invalid_url(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_url(
            "http://example.com" + reverse("misago:account-settings"),
            rf.get("/", HTTP_HOST="example.com"),
            THREAD_URLS,
        )

    assert exc_info.value.message == "Enter a valid thread link."
