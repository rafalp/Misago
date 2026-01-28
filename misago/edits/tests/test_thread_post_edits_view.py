from django.urls import reverse

from ...permissions.enums import CanHideOwnPostEdits, CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..create import create_post_edit
from ..hide import hide_post_edit


def test_thread_post_edits_view_shows_empty(user_client, thread, post):
    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_to_anonymous_user(client, thread, post):
    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_in_htmx(user_client, thread, post):
    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_to_anonymous_user_in_htmx(
    client, thread, post
):
    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_in_modal(user_client, thread, post):
    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_to_anonymous_user_in_modal(
    client, thread, post
):
    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_redirects_to_last_edit(user_client, thread, post):
    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread-post-edits",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "post_id": post.id,
            "page": 2,
        },
    )


def test_thread_post_edits_view_redirects_to_last_edit_in_htmx(
    user_client, thread, post
):
    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread-post-edits",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "post_id": post.id,
            "page": 2,
        },
    )


def test_thread_post_edits_view_redirects_to_last_edit_in_modal(
    user_client, thread, post
):
    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true"
    )


def test_thread_post_edits_view_redirects_to_last_edit_for_out_of_range_page(
    user_client, thread, post
):
    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 5,
            },
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread-post-edits",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "post_id": post.id,
            "page": 2,
        },
    )


def test_thread_post_edits_view_redirects_to_last_edit_for_out_of_range_page_in_htmx(
    user_client, thread, post
):
    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 5,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread-post-edits",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "post_id": post.id,
            "page": 2,
        },
    )


def test_thread_post_edits_view_redirects_to_last_edit_for_out_of_range_page_in_modal(
    user_client, thread, post
):
    create_post_edit(post=post, user="Moderator")
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
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
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true"
    )


def test_thread_post_edits_view_shows_only_edit(user_client, thread, post):
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        )
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_only_edit_in_htmx(user_client, thread, post):
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_only_edit_in_modal(user_client, thread, post):
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_first_edit(user_client, thread, post):
    create_post_edit(post=post, user="FirstEditor")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        )
    )

    assert_contains(response, "FirstEditor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_first_edit_in_htmx(user_client, thread, post):
    create_post_edit(post=post, user="FirstEditor")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "FirstEditor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_first_edit_in_modal(user_client, thread, post):
    create_post_edit(post=post, user="FirstEditor")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "FirstEditor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_middle_edit(user_client, thread, post):
    create_post_edit(post=post, user="Editor")
    create_post_edit(post=post, user="MiddleEditor")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
    )

    assert_contains(response, "MiddleEditor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_middle_edit_in_htmx(user_client, thread, post):
    create_post_edit(post=post, user="Editor")
    create_post_edit(post=post, user="MiddleEditor")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "MiddleEditor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_middle_edit_in_modal(user_client, thread, post):
    create_post_edit(post=post, user="Editor")
    create_post_edit(post=post, user="MiddleEditor")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "MiddleEditor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_last_edit(user_client, thread, post):
    create_post_edit(post=post, user="Editor")
    create_post_edit(post=post, user="LastEditor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
    )

    assert_contains(response, "LastEditor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_last_edit_in_htmx(user_client, thread, post):
    create_post_edit(post=post, user="Editor")
    create_post_edit(post=post, user="LastEditor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "LastEditor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_last_edit_in_modal(user_client, thread, post):
    create_post_edit(post=post, user="Editor")
    create_post_edit(post=post, user="LastEditor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "LastEditor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_empty_edit(user_client, thread, post):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_empty_edit_to_anonymous_user(
    client, thread, post
):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_empty_edit_in_htmx(user_client, thread, post):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_empty_edit_to_anonymous_user_in_htmx(
    client, thread, post
):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_empty_edit_in_modal(user_client, thread, post):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_empty_edit_to_anonymous_user_in_modal(
    client, thread, post
):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "No changes were made in this edit")


def test_thread_post_edits_view_shows_editor(user_client, moderator, thread, post):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user=moderator)

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, moderator.get_absolute_url())
    assert_contains(response, moderator.username)


def test_thread_post_edits_view_shows_editor_in_htmx(
    user_client, moderator, thread, post
):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user=moderator)

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, moderator.get_absolute_url())
    assert_contains(response, moderator.username)


def test_thread_post_edits_view_shows_editor_in_modal(
    user_client, moderator, thread, post
):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user=moderator)

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, moderator.get_absolute_url())
    assert_contains(response, moderator.username)


def test_thread_post_edits_view_shows_edit_reason(user_client, thread, post):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor", edit_reason="Lorem ipsum dolor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Lorem ipsum dolor")


def test_thread_post_edits_view_shows_edit_reason_in_htmx(user_client, thread, post):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor", edit_reason="Lorem ipsum dolor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Lorem ipsum dolor")


def test_thread_post_edits_view_shows_edit_reason_in_modal(user_client, thread, post):
    create_post_edit(post=post, user="User")
    create_post_edit(post=post, user="Editor", edit_reason="Lorem ipsum dolor")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Lorem ipsum dolor")


def test_thread_post_edits_view_shows_thread_title_diff(user_client, thread, post):
    create_post_edit(post=post, user="User")
    create_post_edit(
        post=post,
        user="Editor",
        old_title="Lorem ipsum",
        new_title="Dolor met",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Title changes")
    assert_contains(response, "Lorem ipsum")
    assert_contains(response, "Dolor met")


def test_thread_post_edits_view_shows_post_contents_diff(user_client, thread, post):
    create_post_edit(post=post, user="User")
    create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
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


def test_thread_post_edits_view_shows_post_contents_diff_with_collapsed_hunk_at_beginning(
    user_client, thread, post
):
    create_post_edit(post=post, user="User")
    create_post_edit(
        post=post,
        user="Editor",
        old_content="\n".join(
            [
                "Lorem ipsum",
                "Dolor met",
                "Sit amet",
                "Etiam rutrum",
                "Suspendisse dictum",
                "Pellentesque nec",
                "Integer nisl",
            ]
        ),
        new_content="\n".join(
            [
                "Lorem ipsum",
                "Dolor met",
                "Sit amet",
                "Etiam rutrum",
                "Suspendisse dictum",
                "Pellentesque nec",
            ]
        ),
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Content changes")
    assert_contains(response, "Lorem ipsum")
    assert_contains(response, "Dolor met")


def test_thread_post_edits_view_shows_post_contents_diff_with_collapsed_hunk_in_middle(
    user_client, thread, post
):
    create_post_edit(post=post, user="User")
    create_post_edit(
        post=post,
        user="Editor",
        old_content="\n".join(
            [
                "Lorem ipsum",
                "Dolor met",
                "Sit amet",
                "Etiam rutrum",
                "Suspendisse dictum",
                "Pellentesque nec",
                "Integer nisl",
                "Praesent ut",
                "Nam blandit",
                "Sed tempus",
                "Curabitur eget",
            ]
        ),
        new_content="\n".join(
            [
                "Dolor met",
                "Sit amet",
                "Etiam rutrum",
                "Suspendisse dictum",
                "Pellentesque nec",
                "Integer nisl",
                "Praesent ut",
                "Nam blandit",
                "Sed tempus",
            ]
        ),
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Content changes")
    assert_contains(response, "Lorem ipsum")
    assert_contains(response, "Dolor met")


def test_thread_post_edits_view_shows_post_contents_diff_with_collapsed_hunk_at_end(
    user_client, thread, post
):
    create_post_edit(post=post, user="User")
    create_post_edit(
        post=post,
        user="Editor",
        old_content="\n".join(
            [
                "Lorem ipsum",
                "Dolor met",
                "Sit amet",
                "Etiam rutrum",
                "Suspendisse dictum",
                "Pellentesque nec",
                "Integer nisl",
            ]
        ),
        new_content="\n".join(
            [
                "Dolor met",
                "Sit amet",
                "Etiam rutrum",
                "Suspendisse dictum",
                "Pellentesque nec",
                "Integer nisl",
            ]
        ),
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Content changes")
    assert_contains(response, "Lorem ipsum")
    assert_contains(response, "Dolor met")


def test_thread_post_edits_view_shows_attachments_diff(
    attachment_factory, text_file, user_client, thread, post
):
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
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
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


def test_thread_post_edits_view_shows_hidden_post_diff_to_moderator(
    moderator_client, thread, post
):
    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_contains(response, "Content changes")
    assert_contains(response, "Lorem ipsum")
    assert_contains(response, "Dolor met")
    assert_contains(response, "Another paragraph")


def test_thread_post_edits_view_shows_hidden_post_diff_to_moderator_in_htmx(
    moderator_client, thread, post
):
    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_contains(response, "Content changes")
    assert_contains(response, "Lorem ipsum")
    assert_contains(response, "Dolor met")
    assert_contains(response, "Another paragraph")


def test_thread_post_edits_view_shows_hidden_post_diff_to_moderator_in_modal(
    moderator_client, thread, post
):
    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_contains(response, "Content changes")
    assert_contains(response, "Lorem ipsum")
    assert_contains(response, "Dolor met")
    assert_contains(response, "Another paragraph")


def test_thread_post_edits_view_doesnt_show_hidden_post_diff_to_user(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_not_contains(response, "Content changes")
    assert_not_contains(response, "Lorem ipsum")
    assert_not_contains(response, "Dolor met")
    assert_not_contains(response, "Another paragraph")


def test_thread_post_edits_view_doesnt_show_hidden_post_diff_to_user_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_not_contains(response, "Content changes")
    assert_not_contains(response, "Lorem ipsum")
    assert_not_contains(response, "Dolor met")
    assert_not_contains(response, "Another paragraph")


def test_thread_post_edits_view_doesnt_show_hidden_post_diff_to_user_in_modal(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_not_contains(response, "Content changes")
    assert_not_contains(response, "Lorem ipsum")
    assert_not_contains(response, "Dolor met")
    assert_not_contains(response, "Another paragraph")


def test_thread_post_edits_view_doesnt_show_hidden_post_diff_to_anonymous_user(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_not_contains(response, "Content changes")
    assert_not_contains(response, "Lorem ipsum")
    assert_not_contains(response, "Dolor met")
    assert_not_contains(response, "Another paragraph")


def test_thread_post_edits_view_doesnt_show_hidden_post_diff_to_anonymous_user_in_htmx(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_not_contains(response, "Content changes")
    assert_not_contains(response, "Lorem ipsum")
    assert_not_contains(response, "Dolor met")
    assert_not_contains(response, "Another paragraph")


def test_thread_post_edits_view_doesnt_show_hidden_post_diff_to_anonymous_user_in_modal(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_not_contains(response, "Content changes")
    assert_not_contains(response, "Lorem ipsum")
    assert_not_contains(response, "Dolor met")
    assert_not_contains(response, "Another paragraph")


def test_thread_post_edits_view_shows_hidden_message_for_edit_hidden_by_registered_user(
    thread_reply_factory, client, user, moderator, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, moderator)

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_not_contains(response, "Content changes")
    assert_not_contains(response, "Lorem ipsum")
    assert_not_contains(response, "Dolor met")
    assert_not_contains(response, "Another paragraph")


def test_thread_post_edits_view_shows_hidden_message_for_edit_hidden_by_registered_user_in_htmx(
    thread_reply_factory, client, user, moderator, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, moderator)

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_not_contains(response, "Content changes")
    assert_not_contains(response, "Lorem ipsum")
    assert_not_contains(response, "Dolor met")
    assert_not_contains(response, "Another paragraph")


def test_thread_post_edits_view_shows_hidden_message_for_edit_hidden_by_registered_user_in_modal(
    thread_reply_factory, client, user, moderator, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, moderator)

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Editor")
    assert_contains(response, "Edit contents hidden")
    assert_not_contains(response, "Content changes")
    assert_not_contains(response, "Lorem ipsum")
    assert_not_contains(response, "Dolor met")
    assert_not_contains(response, "Another paragraph")


def test_thread_post_edits_view_doesnt_show_restore_edit_option_to_anonymous_user_post(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_edit_option_to_anonymous_user_post_in_htmx(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_edit_option_to_anonymous_user_post_in_modal(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="User")
    post_edit = create_post_edit(
        post=post,
        user="Editor",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_edit_option_to_other_user_post(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_edit_option_to_other_user_post_in_htmx(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_edit_option_to_other_user_post_in_modal(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_edit_option_to_user_non_editable_post(
    thread_reply_factory, user_client, user, thread
):
    thread.is_closed = True
    thread.save()

    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_edit_option_to_user_non_editable_post_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    thread.is_closed = True
    thread.save()

    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_edit_option_to_user_non_editable_post_in_modal(
    thread_reply_factory, user_client, user, thread
):
    thread.is_closed = True
    thread.save()

    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_restore_edit_option_to_user_editable_post(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_restore_edit_option_to_user_editable_post_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_restore_edit_option_to_user_editable_post_in_modal(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_restore_edit_option_to_moderator(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_restore_edit_option_to_moderator_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_restore_edit_option_to_moderator_in_modal(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_hidden_edit_option_to_user(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_hidden_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_restore_hidden_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_restore_hidden_edit_option_to_moderator(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, user)

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_restore_hidden_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, user)

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_restore_hidden_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, user)

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="DeletedUser")

    create_post_edit(post=post, user="DeletedUser")
    post_edit = create_post_edit(
        post=post,
        user="DeletedUser",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="DeletedUser")

    create_post_edit(post=post, user="DeletedUser")
    post_edit = create_post_edit(
        post=post,
        user="DeletedUser",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_other_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_other_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_other_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_edit_option_to_user(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="DeletedUser")

    create_post_edit(post=post, user="DeletedUser")
    post_edit = create_post_edit(
        post=post,
        user="DeletedUser",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="DeletedUser")

    create_post_edit(post=post, user="DeletedUser")
    post_edit = create_post_edit(
        post=post,
        user="DeletedUser",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="DeletedUser")

    create_post_edit(post=post, user="DeletedUser")
    post_edit = create_post_edit(
        post=post,
        user="DeletedUser",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_other_user_edit_option_to_user(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_other_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_other_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_edit_option_to_user_without_permission(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_edit_option_to_user_without_permission_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_edit_option_to_user_without_permission_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_hide_user_edit_option_to_user_with_permission(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_hide_user_edit_option_to_user_with_permission_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_hide_user_edit_option_to_user_with_permission_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_hide_deleted_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_hide_deleted_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_hide_deleted_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_hide_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_hide_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_hide_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_hidden_edit_option_to_anonymous_user(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_hidden_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_hidden_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_anonymous_user(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_hidden_edit_option_to_user(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_hidden_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_hidden_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_other_user_hidden_edit_option_to_user(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_other_user_hidden_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_other_user_hidden_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_user_without_permission(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_user_without_permission_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_user_without_permission_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_user_with_permission(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_user_with_permission_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_user_with_permission_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_hidden_edit_option_to_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Delete")

    create_post_edit(post=post, user="Delete")
    post_edit = create_post_edit(
        post=post,
        user="Delete",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_hidden_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Delete")

    create_post_edit(post=post, user="Delete")
    post_edit = create_post_edit(
        post=post,
        user="Delete",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_deleted_user_hidden_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Delete")

    create_post_edit(post=post, user="Delete")
    post_edit = create_post_edit(
        post=post,
        user="Delete",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_moderator(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_hide_user_hidden_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_deleted_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_deleted_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_deleted_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_deleted_user_edit_option_to_user(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_deleted_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_deleted_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_other_user_edit_option_to_user(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_other_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_other_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_user_edit_option_to_user(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_deleted_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_deleted_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_deleted_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_deleted_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_deleted_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_deleted_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_deleted_user_edit_option_to_user(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_deleted_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_deleted_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_other_user_edit_option_to_user(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_other_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_other_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_user_edit_option_to_user(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_unhide_hidden_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_unhide_hidden_deleted_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_unhide_hidden_deleted_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_unhide_hidden_deleted_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_unhide_hidden_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_unhide_hidden_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_unhide_hidden_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_deleted_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_deleted_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_deleted_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_deleted_user_edit_option_to_user(
    thread_reply_factory, user_client, members_group, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_deleted_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, members_group, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_deleted_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, members_group, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_other_user_edit_option_to_user(
    thread_reply_factory, user_client, members_group, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_other_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, members_group, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_other_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, members_group, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_user_edit_option_to_user_without_permission(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_user_edit_option_to_user_without_permission_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_user_edit_option_to_user_without_permission_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_user_edit_option_to_user_with_permission(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_user_edit_option_to_user_with_permission_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_user_edit_option_to_user_with_permission_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_deleted_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_deleted_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_deleted_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_deleted_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_deleted_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_deleted_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_user_edit_option_to_anonymous_user(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_user_edit_option_to_anonymous_user_in_htmx(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_user_edit_option_to_anonymous_user_in_modal(
    thread_reply_factory, client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_deleted_user_edit_option_to_user(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_deleted_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_deleted_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_other_user_edit_option_to_user(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_other_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_other_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    create_post_edit(post=post, user=other_user)
    post_edit = create_post_edit(
        post=post,
        user=other_user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_user_edit_option_to_user(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_user_edit_option_to_user_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_doesnt_show_delete_hidden_user_edit_option_to_user_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_not_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_hidden_deleted_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_hidden_deleted_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_hidden_deleted_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, poster="Deleted")

    create_post_edit(post=post, user="Deleted")
    post_edit = create_post_edit(
        post=post,
        user="Deleted",
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_hidden_user_edit_option_to_moderator(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_hidden_user_edit_option_to_moderator_in_htmx(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_shows_delete_hidden_user_edit_option_to_moderator_in_modal(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    create_post_edit(post=post, user=user)
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum\n\nAnother paragraph",
        new_content="Dolor met\n\nAnother paragraph",
    )

    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )

    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edits_view_returns_error_404_if_thread_doesnt_exist(user_client):
    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": 1,
                "slug": "doesnt-exist",
                "post_id": 1,
                "page": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edits_view_returns_error_404_if_user_cant_see_thread_category(
    thread_reply_factory, user_client, members_group, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.SEE,
    ).delete()

    post = thread_reply_factory(thread, poster=user)
    create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edits_view_returns_error_404_if_user_cant_browse_thread_category(
    thread_reply_factory, user_client, members_group, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    post = thread_reply_factory(thread, poster=user)
    create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edits_view_returns_error_404_if_user_cant_see_thread(
    thread_reply_factory, user_client, user, thread
):
    thread.is_hidden = True
    thread.save()

    post = thread_reply_factory(thread, poster=user)
    create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        ),
    )
    assert response.status_code == 404
