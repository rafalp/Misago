from django.urls import reverse

from ...test import assert_contains, assert_not_contains
from ..test import reply_thread


def test_edit_private_thread_post_view_displays_login_page_to_guests(
    client, user_private_thread
):
    response = client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        )
    )
    assert_contains(response, "Sign in to edit posts")


def test_edit_private_thread_post_view_displays_error_page_to_users_without_private_threads_permission(
    user, user_client, user_private_thread
):
    user.group.can_use_private_threads = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        )
    )
    assert_contains(
        response,
        "You can&#x27;t use private threads.",
        status_code=403,
    )


def test_edit_private_thread_post_view_displays_error_page_to_user_who_cant_see_private_thread(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": private_thread.id,
                "slug": private_thread.slug,
                "post": private_thread.first_post_id,
            },
        )
    )
    assert response.status_code == 404


def test_edit_private_thread_post_view_displays_error_page_to_user_who_cant_edit_own_posts(
    user, user_client, user_private_thread
):
    user.group.can_edit_own_posts = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit posts.",
        status_code=403,
    )


def test_edit_private_thread_post_view_displays_error_page_to_user_trying_to_edit_other_user_post(
    user_client, user_private_thread, other_user
):
    post = reply_thread(user_private_thread, poster=other_user)

    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": post.id,
            },
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit other users posts.",
        status_code=403,
    )


def test_edit_private_thread_post_view_displays_edit_post_form(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        )
    )
    assert_contains(response, "Edit post")
    assert_contains(response, user_private_thread.first_post.original)


def test_edit_private_thread_post_view_displays_inline_edit_post_form_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        )
        + "?inline=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.first_post.original)
    assert_contains(response, "?inline=true")


def test_edit_private_thread_post_view_displays_edit_post_form_for_other_user_post_to_moderator(
    user, user_client, user_private_thread, other_user, members_group, moderators_group
):
    post = reply_thread(user_private_thread, poster=other_user)

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": post.id,
            },
        )
    )

    assert_contains(response, "Edit post")
    assert_contains(response, post.original)


def test_edit_private_thread_post_view_updates_thread_post(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        ),
        {
            "posting-post-post": "Edited",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.pk, "slug": user_private_thread.slug},
        )
        + f"#post-{user_private_thread.first_post_id}"
    )

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited"
    assert post.edits == 1


def test_edit_private_thread_post_view_updates_thread_post_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        ),
        {
            "posting-post-post": "Edited",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    user_private_thread.refresh_from_db()
    assert (
        response["hx-redirect"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.pk, "slug": user_private_thread.slug},
        )
        + f"#post-{user_private_thread.first_post_id}"
    )

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited"
    assert post.edits == 1


def test_edit_private_thread_post_view_updates_thread_post_inline_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        )
        + "?inline=true",
        {
            "posting-post-post": "Edited",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "<p>Edited</p>")

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited"
    assert post.edits == 1


def test_edit_private_thread_post_view_cancels_thread_post_edits_inline_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        )
        + "?inline=true",
        {"posting-post-post": "Edited", "cancel": "true"},
        headers={"hx-request": "true"},
    )

    post_original = user_private_thread.first_post.original
    assert_contains(response, post_original)

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == post_original
    assert post.edits == 0


def test_edit_private_thread_post_view_previews_message(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        ),
        {"posting-post-post": "How's going?", "preview": "true"},
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "Message preview")


def test_edit_private_thread_post_view_previews_message_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        ),
        {"posting-post-post": "How's going?", "preview": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "Message preview")


def test_edit_private_thread_post_view_previews_message_inline_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        )
        + "?inline=true",
        {"posting-post-post": "How's going?", "preview": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Message preview")
    assert_contains(response, "?inline=true")


def test_edit_private_thread_post_view_validates_post(user_client, user_private_thread):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        ),
        {"posting-post-post": "?"},
    )
    assert_contains(response, "Edit post")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_edit_private_thread_post_view_validates_posted_contents(
    user_client, user_private_thread, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        ),
        {
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "Your message contains spam!")


def test_edit_private_thread_post_view_shows_error_if_thread_post_is_accessed(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={"id": thread.id, "slug": thread.slug, "post": thread.first_post_id},
        ),
    )

    assert_not_contains(response, "Edit post", status_code=404)
    assert_not_contains(response, thread.title, status_code=404)
