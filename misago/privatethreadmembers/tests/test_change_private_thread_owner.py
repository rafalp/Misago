from ...threadupdates.enums import ThreadUpdateActionName
from ..members import change_private_thread_owner, get_private_thread_members


def test_change_private_thread_owner_changes_private_thread_owner_to_other_member(
    user, other_user, moderator, user_private_thread
):
    thread_update = change_private_thread_owner(user, user_private_thread, other_user)

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == other_user
    assert members == [user, other_user, moderator]

    assert thread_update.action == ThreadUpdateActionName.CHANGED_OWNER


def test_change_private_thread_owner_moderator_takes_ownership(
    user, other_user, moderator, user_private_thread
):
    thread_update = change_private_thread_owner(
        moderator, user_private_thread, moderator
    )

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == moderator
    assert members == [user, other_user, moderator]

    assert thread_update.action == ThreadUpdateActionName.TOOK_OWNERSHIP
