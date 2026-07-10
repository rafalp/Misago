from django.http import HttpResponse

from ..views import set_moderation_response_headers


def test_set_moderation_response_headers_sets_no_headers(rf):
    request = rf.post("/view/")
    response = HttpResponse()

    set_moderation_response_headers(request, response)

    assert len(response.headers) == 1
    assert response["content-type"]


def test_set_moderation_response_headers_sets_hx_retarget_header(rf):
    request = rf.post("/view/", {"success-hx-target": "#misago-root"})
    response = HttpResponse()

    set_moderation_response_headers(request, response)

    assert len(response.headers) == 2
    assert response["content-type"]
    assert response["hx-retarget"] == "#misago-root"


def test_set_moderation_response_headers_sets_hx_reswap_header(rf):
    request = rf.post("/view/", {"success-hx-swap": "none"})
    response = HttpResponse()

    set_moderation_response_headers(request, response)

    assert len(response.headers) == 2
    assert response["content-type"]
    assert response["hx-reswap"] == "none"


def test_set_moderation_response_headers_sets_hx_trigger_header(rf):
    request = rf.post("/view/")
    response = HttpResponse()

    set_moderation_response_headers(request, response, "misago:event")

    assert len(response.headers) == 2
    assert response["content-type"]
    assert response["hx-trigger-after-settle"] == "misago:event"


def test_set_moderation_response_headers_sets_hx_trigger_with_context_header(rf):
    request = rf.post("/view/")
    response = HttpResponse()

    set_moderation_response_headers(
        request, response, "misago:event", {"updated": [1, 2, 3]}
    )

    assert len(response.headers) == 2
    assert response["content-type"]
    assert (
        response["hx-trigger-after-settle"]
        == '{"misago:event": {"updated": [1, 2, 3]}}'
    )
