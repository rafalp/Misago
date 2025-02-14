import re

from django.contrib.messages.api import get_messages
from django.contrib.messages.constants import ERROR, INFO, SUCCESS, WARNING


def assert_status_code(response, status_code):
    assert (
        response.status_code == status_code
    ), f"unexpected status code: {response.status_code} (expected: {status_code})"


def assert_contains(response, string, status_code=200):
    assert_status_code(response, status_code)

    fail_message = f'"{string}" not found in response.content'
    assert string in response.content.decode("utf-8"), fail_message


def assert_not_contains(response, string, status_code=200):
    assert_status_code(response, status_code)

    fail_message = f'"{string}" was unexpectedly found in response.content'
    assert string not in response.content.decode("utf-8"), fail_message


def assert_contains_element(response, element, status_code=200, **attrs):
    assert_status_code(response, status_code)

    fail_message = f'"{element}" element not found in response.content'

    document = response.content.decode("utf-8")
    assert f"<{element}" in document, fail_message
    assert _find_html_element(document, element, attrs), fail_message


def assert_not_contains_element(response, element, status_code=200, **attrs):
    assert_status_code(response, status_code)

    fail_message = f'"{element}" was unexpectedly found in response.content'

    document = response.content.decode("utf-8")
    if f"<{element}" in document:
        assert not _find_html_element(document, element, attrs), fail_message


_HTML_RE = re.compile(r"\<.+?\>", re.DOTALL)


def _find_html_element(document, element, attrs) -> bool:
    for match in _HTML_RE.findall(document):
        if element not in match:
            continue

        if _match_html_element(match, element, attrs):
            return True

    return False


def _match_html_element(match, element, attrs) -> bool:
    tag_name, html_attrs = _parse_element_html(match)

    if tag_name != element:
        return False

    if attrs:
        for attr, value in attrs.items():
            if attr not in html_attrs:
                return False

            if isinstance(value, int):
                value = str(value)

            if html_attrs[attr] != value:
                return False

    return True


def _parse_element_html(html) -> tuple[str, dict]:
    parts = _split_element_html(html.strip(" <>/").replace("\r\n", "\n"))
    tag_name: str = parts[0].lower()

    attrs: dict[str, str | bool] = {}
    for part in parts[1:]:
        try:
            equals = part.index("=")
            attr_name = part[:equals]
            attr_value = part[equals + 1 :].strip('"')
            attrs[attr_name] = attr_value
        except ValueError:
            attrs[part] = True

    return tag_name, attrs


_HTML_SEPARATOR = (" ", "\n")


def _split_element_html(html) -> list[str]:
    parts: list[str] = []

    part = ""
    quoted = False

    for c in html:
        if c in _HTML_SEPARATOR and not quoted:
            if part:
                parts.append(part)
                part = ""
        else:
            if c == '"':
                quoted = not quoted

            part += c

    if part:
        parts.append(part)

    return parts


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
