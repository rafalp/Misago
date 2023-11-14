import responses

from ..tasks import update_remote_css_size


@responses.activate
def test_task_uses_response_body_to_set_css_size(css_link):
    content = "html {}"
    content_bytes = content.encode()

    responses.add(
        responses.GET,
        css_link.url,
        headers={
            "Content-Type": "text/css;charset=utf-8",
            "Content-Length": str(len(content_bytes)),
        },
        body=content_bytes,
    )

    update_remote_css_size(css_link.pk)

    css_link.refresh_from_db()
    assert css_link.size == len(content)


@responses.activate
def test_task_doesnt_change_css_size_if_http_request_failed(css_link):
    responses.add(responses.GET, css_link.url, status=404)
    update_remote_css_size(css_link.pk)


def test_task_handles_css_without_url(css):
    update_remote_css_size(css.pk)


def test_task_handles_nonexisting_css(db):
    update_remote_css_size(1)
