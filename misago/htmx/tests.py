from .request import is_request_htmx


def test_is_request_htmx_returns_true_for_htmx_request(rf):
    request = rf.get("/", headers={"hx-request": "true"})
    assert is_request_htmx(request)


def test_is_request_htmx_returns_false_for_non_htmx_request(rf):
    request = rf.get("/", headers={})
    assert not is_request_htmx(request)
