from .request import is_request_htmx
from .response import htmx_redirect


def test_is_request_htmx_returns_true_for_htmx_request(rf):
    request = rf.get("/", headers={"hx-request": "true"})
    assert is_request_htmx(request)


def test_is_request_htmx_returns_false_for_non_htmx_request(rf):
    request = rf.get("/", headers={})
    assert not is_request_htmx(request)


def test_htmx_redirect_returns_204_response_with_hx_redirect():
    response = htmx_redirect("/test/")

    assert response.status_code == 204
    assert response.headers["hx-redirect"] == "/test/"
    assert not response.content
