from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission


def test_post_view_returns_404_for_not_existing_post_id(
    thread_reply_factory, client, thread
):
    reply = thread_reply_factory(thread)

    response = client.get(reverse("misago:post", kwargs={"post_id": reply.id + 10}))
    assert response.status_code == 404


def test_post_view_returns_error_404_if_user_cant_see_thread(
    thread_reply_factory, user_client, hidden_thread
):
    reply = thread_reply_factory(hidden_thread)

    response = user_client.get(reverse("misago:post", kwargs={"post_id": reply.id}))
    assert response.status_code == 404


def test_post_view_returns_error_404_if_user_cant_see_thread_post(
    thread_reply_factory, user_client, thread
):
    thread.category.delay_browse_check = True
    thread.category.save()

    CategoryGroupPermission.objects.filter(
        category=thread.category,
        permission=CategoryPermission.BROWSE,
    ).delete()

    reply = thread_reply_factory(thread)

    response = user_client.get(reverse("misago:post", kwargs={"post_id": reply.id}))
    assert response.status_code == 404


def test_post_view_returns_error_404_if_user_cant_use_private_threads(
    thread_reply_factory, user_client, members_group, user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    reply = thread_reply_factory(user_private_thread)

    response = user_client.get(reverse("misago:post", kwargs={"post_id": reply.id}))
    assert response.status_code == 404


def test_post_view_returns_error_404_if_user_cant_see_private_thread(
    thread_reply_factory, user_client, private_thread
):
    reply = thread_reply_factory(private_thread)

    response = user_client.get(reverse("misago:post", kwargs={"post_id": reply.id}))
    assert response.status_code == 404


def test_post_view_returns_redirect_to_thread_post(
    thread_reply_factory, client, thread
):
    reply = thread_reply_factory(thread)

    response = client.get(reverse("misago:post", kwargs={"post_id": reply.id}))

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{reply.id}"
    )


def test_post_view_returns_redirect_to_private_thread_post(
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = user_client.get(reverse("misago:post", kwargs={"post_id": reply.id}))

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
        + f"#post-{reply.id}"
    )


def test_post_view_returns_redirect_to_thread_post_for_post_request(
    thread_reply_factory, client, thread
):
    reply = thread_reply_factory(thread)

    response = client.post(reverse("misago:post", kwargs={"post_id": reply.id}))

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{reply.id}"
    )


def test_post_view_returns_redirect_to_private_thread_post_for_post_request(
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = user_client.post(reverse("misago:post", kwargs={"post_id": reply.id}))

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
        + f"#post-{reply.id}"
    )
