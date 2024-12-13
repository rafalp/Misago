from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from ..models import Thread


def test_start_thread_view_displays_login_page_to_guests(client, default_category):
    response = client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, "Sign in to start new thread")


def test_start_thread_view_displays_error_page_to_users_without_see_category_permission(
    user_client, user, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert response.status_code == 404


def test_start_thread_view_displays_error_page_to_users_without_browse_category_permission(
    user_client, user, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t browse the contents of this category.",
        status_code=403,
    )


def test_start_thread_view_displays_error_page_to_users_without_start_threads_permission(
    user_client, user, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t start new threads in this category.",
        status_code=403,
    )


def test_start_thread_view_displays_error_page_to_users_without_post_in_closed_category_permission(
    user_client, default_category
):
    default_category.is_closed = True
    default_category.save()

    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        "This category is closed.",
        status_code=403,
    )


def test_start_thread_view_displays_form_page_to_users(user_client, default_category):
    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, "Start new thread")


def test_start_thread_view_displays_form_page_to_users_with_permission_to_post_in_closed_category(
    user, user_client, default_category, members_group, moderators_group
):
    default_category.is_closed = True
    default_category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, "Start new thread")


def test_start_thread_view_posts_new_thread(user_client, default_category):
    response = user_client.post(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
        {
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:thread", kwargs={"id": thread.pk, "slug": thread.slug}
    )


def test_start_thread_view_previews_message(user_client, default_category):
    response = user_client.post(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
        {
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
            "preview": "true",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, "Message preview")


def test_start_thread_view_validates_thread_title(user_client, default_category):
    response = user_client.post(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
        {
            "posting-title-title": "???",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, "Thread title must include alphanumeric characters.")


def test_start_private_thread_view_validates_post(user_client, default_category):
    response = user_client.post(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
        {
            "posting-title-title": "Hello world",
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )
