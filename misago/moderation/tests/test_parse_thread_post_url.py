import pytest
from django.forms import ValidationError
from django.urls import reverse

from ..forms import parse_thread_post_url


def test_parse_thread_post_url_returns_post_id_from_valid_thread_post_link(rf):
    post_id = parse_thread_post_url(
        "http://example.com"
        + reverse(
            "misago:thread-post",
            kwargs={"thread_id": 123, "slug": "thread-slug", "post_id": 321},
        ),
        rf.get("/", HTTP_HOST="example.com"),
        ("misago:post", "misago:thread-post"),
        123,
    )

    assert post_id == 321


def test_parse_thread_post_url_returns_post_id_from_valid_post_link(rf):
    post_id = parse_thread_post_url(
        "http://example.com" + reverse("misago:post", kwargs={"post_id": 321}),
        rf.get("/", HTTP_HOST="example.com"),
        ("misago:post", "misago:thread-post"),
        123,
    )

    assert post_id == 321


def test_parse_thread_post_url_raises_validation_error_on_missing_hostname(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_post_url(
            reverse("misago:post", kwargs={"post_id": 321}),
            rf.get("/", HTTP_HOST="example.com"),
            ("misago:post", "misago:thread-post"),
            123,
        )

    assert exc_info.value.message == "Enter a valid link."


def test_parse_thread_post_url_raises_validation_error_on_missing_path(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_post_url(
            "http://example.com/",
            rf.get("/", HTTP_HOST="example.com"),
            ("misago:post", "misago:thread-post"),
            123,
        )

    assert exc_info.value.message == "Enter a valid link."


def test_parse_thread_post_url_raises_validation_error_on_invalid_hostname(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_post_url(
            "http://misago-project.org/"
            + reverse("misago:post", kwargs={"post_id": 321}),
            rf.get("/", HTTP_HOST="example.com"),
            ("misago:post", "misago:thread-post"),
            123,
        )

    assert exc_info.value.message == "Enter a link to this site."


def test_parse_thread_post_url_raises_validation_error_on_invalid_path(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_post_url(
            "http://example.com/invalid/",
            rf.get("/", HTTP_HOST="example.com"),
            ("misago:post", "misago:thread-post"),
            123,
        )

    assert exc_info.value.message == "Enter a valid post link."


def test_parse_thread_post_url_raises_validation_error_on_path_being_invalid_url(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_post_url(
            "http://example.com" + reverse("misago:account-settings"),
            rf.get("/", HTTP_HOST="example.com"),
            ("misago:post", "misago:thread-post"),
            123,
        )

    assert exc_info.value.message == "Enter a valid post link."


def test_parse_thread_url_raises_validation_error_on_path_being_invalid_thread(rf):
    with pytest.raises(ValidationError) as exc_info:
        parse_thread_post_url(
            "http://example.com"
            + reverse(
                "misago:thread-post",
                kwargs={"thread_id": 123, "slug": "thread-slug", "post_id": 321},
            ),
            rf.get("/", HTTP_HOST="example.com"),
            ("misago:post", "misago:thread-post"),
            2222,
        )

    assert exc_info.value.message == "Enter a link to the current thread."
