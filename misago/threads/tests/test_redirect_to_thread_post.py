from django.urls import reverse

from ..redirect import redirect_to_thread_post


def test_redirect_to_thread_post_returns_redirect_to_post(
    rf, dynamic_settings, user_permissions, thread, post
):
    request = rf.post("/threads/")
    request.settings = dynamic_settings
    request.user_permissions = user_permissions

    response = redirect_to_thread_post(request, thread, post)

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{post.id}"
    )
