from ..actions import ModerationResult
from ..views import get_moderation_result_response


def test_get_moderation_result_response_returns_refresh_response(rf):
    request = rf.post("/path/")
    request.is_htmx = False

    result = ModerationResult(refresh=True)

    response = get_moderation_result_response(request, result)
    assert response.status_code == 302
    assert response["location"] == "/path/"


def test_get_moderation_result_response_returns_refresh_response_in_htmx(rf):
    request = rf.post("/path/")
    request.is_htmx = True

    result = ModerationResult(refresh=True)

    response = get_moderation_result_response(request, result)
    assert response.status_code == 201
    assert response["hx-refresh"] == "true"


def test_get_moderation_result_response_returns_refresh_response_with_event_in_htmx(rf):
    request = rf.post("/path/")
    request.is_htmx = True

    result = ModerationResult(refresh=True)

    response = get_moderation_result_response(request, result, "misago:event")
    assert response.status_code == 201
    assert response["hx-refresh"] == "true"
    assert response["hx-trigger-after-settle"] == "misago:event"


def test_get_moderation_result_response_returns_refresh_response_with_event_and_context_in_htmx(
    rf,
):
    request = rf.post("/path/")
    request.is_htmx = True

    result = ModerationResult(refresh=True)

    response = get_moderation_result_response(
        request, result, "misago:event", {"updated": [1, 2, 3]}
    )
    assert response.status_code == 201
    assert response["hx-refresh"] == "true"
    assert (
        response["hx-trigger-after-settle"]
        == '{"misago:event": {"updated": [1, 2, 3]}}'
    )


def test_get_moderation_result_response_returns_redirect_response(rf):
    request = rf.post("/path/")
    request.is_htmx = False

    result = ModerationResult(redirect_to="/new-path/")

    response = get_moderation_result_response(request, result)
    assert response.status_code == 302
    assert response["location"] == "/new-path/"


def test_get_moderation_result_response_returns_redirect_response_in_htmx(rf):
    request = rf.post("/path/")
    request.is_htmx = True

    result = ModerationResult(redirect_to="/new-path/")

    response = get_moderation_result_response(request, result)
    assert response.status_code == 201
    assert response["hx-redirect"] == "/new-path/"


def test_get_moderation_result_response_returns_redirect_response_with_event_in_htmx(
    rf,
):
    request = rf.post("/path/")
    request.is_htmx = True

    result = ModerationResult(redirect_to="/new-path/")

    response = get_moderation_result_response(request, result, "misago:event")
    assert response.status_code == 201
    assert response["hx-redirect"] == "/new-path/"
    assert response["hx-trigger-after-settle"] == "misago:event"


def test_get_moderation_result_response_returns_redirect_response_with_event_and_context_in_htmx(
    rf,
):
    request = rf.post("/path/")
    request.is_htmx = True

    result = ModerationResult(redirect_to="/new-path/")

    response = get_moderation_result_response(
        request, result, "misago:event", {"updated": [1, 2, 3]}
    )
    assert response.status_code == 201
    assert response["hx-redirect"] == "/new-path/"
    assert (
        response["hx-trigger-after-settle"]
        == '{"misago:event": {"updated": [1, 2, 3]}}'
    )


def test_get_moderation_result_response_prioritizes_refresh_before_redirect(rf):
    request = rf.post("/path/")
    request.is_htmx = False

    result = ModerationResult(refresh=True, redirect_to="/new-path/")

    response = get_moderation_result_response(request, result)
    assert response.status_code == 302
    assert response["location"] == "/path/"
