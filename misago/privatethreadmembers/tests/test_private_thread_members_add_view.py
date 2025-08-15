from django.urls import reverse

from ...test import assert_contains


def test_private_thread_members_add_view_renders_form(user_client, user_private_thread):
    response = user_client.get(
        reverse(
            "misago:private-thread-members-add",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, "Add members")
