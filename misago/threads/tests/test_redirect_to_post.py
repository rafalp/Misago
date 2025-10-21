import pytest
from django.http import Http404
from django.urls import reverse

# Import views to register them in 'redirect_to_post'
from ...privatethreads.views.post import PrivateThreadPostView
from ..views.post import ThreadPostView
from ..redirect import redirect_to_post


def test_redirect_to_post_returns_redirect_to_thread_post(
    rf, dynamic_settings, user_permissions, thread, post
):
    request = rf.get("/something/else/")
    request.settings = dynamic_settings
    request.user_permissions = user_permissions

    response = redirect_to_post(request, post)
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{post.id}"
    )


def test_redirect_to_post_checks_thread_post_permission(
    rf, dynamic_settings, user_permissions, hidden_thread
):
    request = rf.get("/something/else/")
    request.settings = dynamic_settings
    request.user_permissions = user_permissions

    with pytest.raises(Http404):
        redirect_to_post(request, hidden_thread.first_post)


def test_redirect_to_post_returns_redirect_to_private_thread_post(
    rf, dynamic_settings, user_permissions, user_private_thread
):
    request = rf.get("/something/else/")
    request.settings = dynamic_settings
    request.user_permissions = user_permissions

    response = redirect_to_post(request, user_private_thread.first_post)
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{user_private_thread.first_post.id}"
    )


def test_redirect_to_post_checks_private_thread_post_permission(
    rf, dynamic_settings, user_permissions, private_thread
):
    request = rf.get("/something/else/")
    request.settings = dynamic_settings
    request.user_permissions = user_permissions

    with pytest.raises(Http404):
        redirect_to_post(request, private_thread.first_post)
