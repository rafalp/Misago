from django.urls import reverse

from ...test import assert_contains
from ..create import create_post_edit


def test_private_thread_post_edits_view_shows_empty(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "This post has no edit history.")


def test_private_thread_post_edits_view_shows_empty_in_htmx(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_private_thread_post_edits_view_shows_empty_in_modal(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_private_thread_post_edits_view_redirects_to_last_edit(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread-post-edits",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
            "post_id": post.id,
            "page": 2,
        },
    )


def test_private_thread_post_edits_view_redirects_to_last_edit_in_htmx(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread-post-edits",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
            "post_id": post.id,
            "page": 2,
        },
    )


def test_private_thread_post_edits_view_redirects_to_last_edit_in_modal(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true"
    )


def test_private_thread_post_edits_view_redirects_to_last_edit_for_out_of_range_page(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread-post-edits",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
            "post_id": post.id,
            "page": 5,
            "page": 2,
        },
    )


def test_private_thread_post_edits_view_redirects_to_last_edit_for_out_of_range_page_in_htmx(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 5,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread-post-edits",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
            "post_id": post.id,
            "page": 2,
        },
    )


def test_private_thread_post_edits_view_redirects_to_last_edit_for_out_of_range_page_in_modal(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 5,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true"
    )


def test_private_thread_post_edits_view_shows_empty_edit(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_private_thread_post_edits_view_shows_empty_edit_in_htmx(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_private_thread_post_edits_view_shows_empty_edit_in_modal(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_private_thread_post_edits_view_shows_edit_user(
    user_client, moderator, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user=moderator)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, moderator.get_absolute_url())
    assert_contains(response, moderator.username)


def test_private_thread_post_edits_view_shows_edit_user_in_htmx(
    user_client, moderator, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user=moderator)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, moderator.get_absolute_url())
    assert_contains(response, moderator.username)


def test_private_thread_post_edits_view_shows_edit_user_in_modal(
    user_client, moderator, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user=moderator)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, moderator.get_absolute_url())
    assert_contains(response, moderator.username)


def test_private_thread_post_edits_view_shows_edit_reason(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor", edit_reason="Lorem ipsum dolor")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Lorem ipsum dolor")


def test_private_thread_post_edits_view_shows_edit_reason_in_htmx(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor", edit_reason="Lorem ipsum dolor")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Lorem ipsum dolor")


def test_private_thread_post_edits_view_shows_edit_reason_in_modal(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor", edit_reason="Lorem ipsum dolor")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Lorem ipsum dolor")


def test_private_thread_post_edits_view_shows_thread_title_diff(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(
        post=post,
        user="Editor",
        old_title="Lorem ipsum",
        new_title="Dolor met",
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Title changes")
    assert_contains(response, "Lorem ipsum")
    assert_contains(response, "Dolor met")


def test_private_thread_post_edits_view_shows_post_contents_diff(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    create_post_edit(post=post, user="User")
    create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Content changes")
    assert_contains(response, "Lorem ipsum")
    assert_contains(response, "Dolor met")
    assert_contains(response, "Another paragraph")


def test_private_thread_post_edits_view_shows_attachments_diff(
    attachment_factory, text_file, user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    kept_attachment = attachment_factory(
        text_file,
        name="kept-attachment.txt",
        post=post,
    )
    new_attachment = attachment_factory(
        text_file,
        name="new-attachment.txt",
    )
    deleted_attachment = attachment_factory(
        text_file,
        name="deleted-attachment.txt",
        post=post,
    )

    create_post_edit(post=post, user="User")
    create_post_edit(
        post=post,
        user="Editor",
        attachments=[kept_attachment, new_attachment],
        deleted_attachments=[deleted_attachment],
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Attachment changes")
    assert_contains(response, "kept-attachment.txt")
    assert_contains(response, "new-attachment.txt")
    assert_contains(response, "deleted-attachment.txt")
