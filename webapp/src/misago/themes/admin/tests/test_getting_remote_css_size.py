import responses

from ..tasks import update_remote_css_size


def mock_http_head_response(css_link, content_length=None):
    headers = {}
    if content_length is not None:
        headers["content-length"] = str(content_length)

    responses.add(responses.HEAD, css_link.url, headers=headers)


@responses.activate
def test_task_uses_content_length_header_to_set_css_size(css_link):
    content_length = 343
    mock_http_head_response(css_link, content_length)

    update_remote_css_size(css_link.pk)

    css_link.refresh_from_db()
    assert css_link.size == content_length


@responses.activate
def test_task_doesnt_change_css_size_if_content_length_header_is_incorrect(css_link):
    mock_http_head_response(css_link, "incorrect")
    update_remote_css_size(css_link.pk)

    css_link.refresh_from_db()
    assert css_link.size == 0


@responses.activate
def test_task_doesnt_change_css_size_if_content_length_header_is_empty(css_link):
    mock_http_head_response(css_link, "")
    update_remote_css_size(css_link.pk)

    css_link.refresh_from_db()
    assert css_link.size == 0


@responses.activate
def test_task_doesnt_change_css_size_if_content_length_header_is_not_set(css_link):
    mock_http_head_response(css_link)
    update_remote_css_size(css_link.pk)

    css_link.refresh_from_db()
    assert css_link.size == 0


@responses.activate
def test_task_doesnt_change_css_size_if_http_request_failed(css_link):
    responses.add(responses.HEAD, css_link.url, status=404)
    update_remote_css_size(css_link.pk)


def test_task_handles_css_without_url(css):
    update_remote_css_size(css.pk)


def test_task_handles_nonexisting_css(db):
    update_remote_css_size(1)
