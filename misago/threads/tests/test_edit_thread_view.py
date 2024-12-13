from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


def test_edit_thread_view_displays_login_page_to_guests(client, user_thread):
    response = client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert_contains(response, "Sign in to edit posts")


def test_edit_thread_view_displays_error_page_to_user_who_cant_see_thread_category(
    user, user_client, user_thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert response.status_code == 404


def test_edit_thread_view_displays_error_page_to_user_who_cant_browse_thread_category(
    user, user_client, user_thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert response.status_code == 404


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_in_closed_category(
    user_client, user_thread
):
    user_thread.category.is_closed = True
    user_thread.category.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "This category is closed.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_in_closed_thread(
    user_client, user_thread
):
    user_thread.is_closed = True
    user_thread.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "This thread is closed.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_protected_post(
    user_client, user_thread
):
    post = user_thread.first_post
    post.is_protected = True
    post.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit protected posts.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_own_threads(
    user, user_client, user_thread
):
    user.group.can_edit_own_threads = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit threads.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_own_posts(
    user, user_client, user_thread
):
    user.group.can_edit_own_posts = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit posts.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_trying_to_edit_other_user_thread(
    user_client, other_user_thread, other_user
):

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": other_user_thread.id, "slug": other_user_thread.slug},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit other users threads.",
        status_code=403,
    )


def test_edit_thread_view_displays_edit_form(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_view_displays_inline_edit_form_in_htmx(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
        + "?inline=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_thread.first_post.original)
    assert_contains(response, "?inline=true")


def test_edit_thread_view_displays_edit_form_in_closed_category_to_moderator(
    user, user_client, user_thread, members_group, moderators_group
):
    user_thread.category.is_closed = True
    user_thread.category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(response, "Edit thread")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_view_displays_edit_form_in_closed_thread_to_moderator(
    user, user_client, user_thread, members_group, moderators_group
):
    user_thread.is_closed = True
    user_thread.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(response, "Edit thread")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_view_displays_edit_form_for_protected_post_to_moderator(
    user, user_client, user_thread, members_group, moderators_group
):
    post = user_thread.first_post
    post.is_protected = True
    post.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(response, "Edit thread")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_view_displays_edit_form_for_other_user_thread_to_moderator(
    user, user_client, other_user_thread, members_group, moderators_group
):
    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": other_user_thread.id, "slug": other_user_thread.slug},
        )
    )

    assert_contains(response, "Edit thread")
    assert_contains(response, other_user_thread.first_post.original)


def test_edit_thread_view_updates_thread_and_post(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert user_thread.title == "Edited title"

    assert response["location"] == reverse(
        "misago:thread",
        kwargs={"id": user_thread.pk, "slug": user_thread.slug},
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited post"
    assert post.edits == 1


def test_edit_thread_view_updates_thread_and_post_in_htmx(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    user_thread.refresh_from_db()
    assert user_thread.title == "Edited title"

    assert response["hx-redirect"] == reverse(
        "misago:thread",
        kwargs={"id": user_thread.pk, "slug": user_thread.slug},
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited post"
    assert post.edits == 1


def test_edit_thread_view_updates_thread_and_post_inline_in_htmx(
    user_client, user_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
        + "?inline=true",
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    user_thread.refresh_from_db()
    assert user_thread.title == "Edited title"

    assert response["hx-redirect"] == reverse(
        "misago:thread",
        kwargs={"id": user_thread.pk, "slug": user_thread.slug},
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited post"
    assert post.edits == 1


def test_edit_thread_view_cancels_thread_and_post_edits_inline_in_htmx(
    user_client, user_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
        + "?inline=true",
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
            "cancel": "true",
        },
        headers={"hx-request": "true"},
    )

    post_original = user_thread.first_post.original
    assert_contains(response, post_original)

    user_thread.refresh_from_db()
    assert user_thread.title == "Test thread"

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == post_original
    assert post.edits == 0


def test_edit_thread_view_previews_message(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {"posting-post-post": "How's going?", "preview": "true"},
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Message preview")


def test_edit_thread_view_previews_message_in_htmx(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {"posting-post-post": "How's going?", "preview": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Message preview")


def test_edit_thread_view_previews_message_inline_in_htmx(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
        + "?inline=true",
        {"posting-post-post": "How's going?", "preview": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Message preview")
    assert_contains(response, "?inline=true")


def test_edit_thread_view_validates_thread_title(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-title-title": "???",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Thread title must include alphanumeric characters.")


def test_edit_thread_view_validates_post(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_edit_thread_view_shows_error_if_private_thread_post_is_accessed(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )

    assert_not_contains(response, "Edit thread", status_code=404)
    assert_not_contains(response, user_private_thread.title, status_code=404)
