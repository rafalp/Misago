from django.urls import reverse

from ..members import get_private_thread_members


def test_private_thread_owner_change_view_changes_thread_owner(
    user_client, user, other_user, moderator, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == other_user
    assert members == [user, other_user, moderator]
