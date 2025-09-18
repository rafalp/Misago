from django.urls import reverse

from ..redirect import redirect_to_private_thread_post


def test_redirect_to_private_thread_post_returns_redirect_to_post(
    rf, dynamic_settings, user_permissions, private_thread, private_thread_post
):
    request = rf.post("/threads/")
    request.settings = dynamic_settings
    request.user_permissions = user_permissions

    response = redirect_to_private_thread_post(
        request, private_thread, private_thread_post
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"thread_id": private_thread.id, "slug": private_thread.slug},
        )
        + f"#post-{private_thread_post.id}"
    )
