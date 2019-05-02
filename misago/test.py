from django.contrib.messages.api import get_messages
from django.contrib.messages.constants import ERROR, INFO, SUCCESS


def assert_contains(response, string, status_code=200):
    assert response.status_code == status_code
    fail_message = f'"{string}" not found in response.content'
    assert string in response.content.decode("utf-8"), fail_message


def assert_not_contains(response, string, status_code=200):
    assert response.status_code == status_code
    fail_message = f'"{string}" was unexpectedly found in response.content'
    assert string not in response.content.decode("utf-8"), fail_message


def assert_has_error_message(response):
    messages = get_messages(response.wsgi_request)
    levels = [i.level for i in messages]

    assert levels, "No messages were set during the request"
    assert ERROR in levels, "No error messages were set during the request"


def assert_has_info_message(response):
    messages = get_messages(response.wsgi_request)
    levels = [i.level for i in messages]

    assert levels, "No messages were set during the request"
    assert INFO in levels, "No info messages were set during the request"


def assert_has_success_message(response):
    messages = get_messages(response.wsgi_request)
    levels = [i.level for i in messages]

    assert levels, "No messages were set during the request"
    assert SUCCESS in levels, "No success messages were set during the request"


def assert_has_message(response, message, level=None):
    messages = get_messages(response.wsgi_request)
    found = False
    for msg in messages:
        if message in str(msg):
            if level and level != msg.level:
                error = (
                    'Message containing "%s" was set '
                    "but didn't have level %s (it had %s)"
                )
                raise AssertionError(error % (message, level, message.level))
            found = True

    if not found:
        raise AssertionError(
            'Message containing "%s" was not set during the request' % message
        )
