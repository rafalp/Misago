from django.contrib.messages.api import get_messages
from django.contrib.messages.constants import ERROR, INFO, SUCCESS, WARNING
from django.test import Client


def assert_contains(response, string, status_code=200):
    assert response.status_code == status_code
    fail_message = f'"{string}" not found in response.content'
    assert string in response.content.decode("utf-8"), fail_message


def assert_not_contains(response, string, status_code=200):
    assert response.status_code == status_code
    fail_message = f'"{string}" was unexpectedly found in response.content'
    assert string not in response.content.decode("utf-8"), fail_message


def assert_has_warning_message(response, message: str | None = None):
    messages = get_messages(response.wsgi_request)
    levels = [i.level for i in messages]

    assert levels, "No messages were set during the request"
    assert WARNING in levels, "No warning messages were set during the request"

    if message:
        _assert_message_exists(messages, WARNING, message)


def assert_has_error_message(response, message: str | None = None):
    messages = get_messages(response.wsgi_request)
    levels = [i.level for i in messages]

    assert levels, "No messages were set during the request"
    assert ERROR in levels, "No error messages were set during the request"

    if message:
        _assert_message_exists(messages, ERROR, message)


def assert_has_info_message(response, message: str | None = None):
    messages = get_messages(response.wsgi_request)
    levels = [i.level for i in messages]

    assert levels, "No messages were set during the request"
    assert INFO in levels, "No info messages were set during the request"

    if message:
        _assert_message_exists(messages, INFO, message)


def assert_has_success_message(response, message: str | None = None):
    messages = get_messages(response.wsgi_request)
    levels = [i.level for i in messages]

    assert levels, "No messages were set during the request"
    assert SUCCESS in levels, "No success messages were set during the request"

    if message:
        _assert_message_exists(messages, SUCCESS, message)


def _assert_message_exists(messages, level, message: str) -> bool:
    for m in messages:
        if m.level == level and message == str(m.message):
            return

    messages = "\n".join([m.message for m in messages])

    raise AssertionError(
        f"Expected message was not set during the request: {message}\n"
        f"Found messages:\n\n{messages}"
    )


class MisagoClient(Client):
    def post(self, *args, **kwargs):
        if "json" in kwargs:
            return super().post(
                *args,
                data=kwargs.pop("json"),
                content_type="application/json",
                **kwargs,
            )

        return super().post(*args, **kwargs)

    def put(self, *args, **kwargs):
        if "json" in kwargs:
            return super().put(
                *args,
                data=kwargs.pop("json"),
                content_type="application/json",
                **kwargs,
            )

        return super().put(*args, **kwargs)
