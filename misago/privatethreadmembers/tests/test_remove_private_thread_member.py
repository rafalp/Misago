from ...threadupdates.enums import ThreadUpdateActionName
from ..members import get_private_thread_members, remove_private_thread_member


def test_remove_private_thread_member_actor_leaves_thread(
    user, other_user, moderator, user_private_thread
):
    thread_update = remove_private_thread_member(user, user_private_thread, user)

    _, members = get_private_thread_members(user_private_thread)
    assert members == [other_user, moderator]

    assert thread_update.action == ThreadUpdateActionName.LEFT


def test_remove_private_thread_member_removes_other_member(
    user, other_user, moderator, user_private_thread
):
    thread_update = remove_private_thread_member(user, user_private_thread, other_user)

    _, members = get_private_thread_members(user_private_thread)
    assert members == [user, moderator]

    assert thread_update.action == ThreadUpdateActionName.REMOVED_MEMBER
