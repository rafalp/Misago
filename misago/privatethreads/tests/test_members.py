from ...threadevents.enums import ThreadUpdateActionName
from ..members import (
    add_private_thread_member,
    get_private_thread_members,
    prefetch_private_thread_member_ids,
    private_thread_has_members,
    remove_private_thread_member,
    set_private_thread_owner,
)
from ..models import PrivateThreadMember


def test_private_thread_has_members_returns_true_if_thread_has_members(
    user_private_thread,
):
    assert private_thread_has_members(user_private_thread)


def test_private_thread_has_members_returns_false_if_thread_has_no_members(
    private_thread,
):
    assert not private_thread_has_members(private_thread)


def test_prefetch_private_thread_member_ids_sets_thread_owner_id_property(
    thread, user_thread, user, other_user, django_assert_num_queries
):
    PrivateThreadMember.objects.create(thread=thread, user=user, is_owner=False)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)
    PrivateThreadMember.objects.create(thread=user_thread, user=user, is_owner=True)
    PrivateThreadMember.objects.create(
        thread=user_thread, user=other_user, is_owner=False
    )

    with django_assert_num_queries(1):
        prefetch_private_thread_member_ids([thread, user_thread])

        assert thread.private_thread_owner_id == other_user.id
        assert user_thread.private_thread_owner_id == user.id


def test_prefetch_private_thread_member_ids_sets_thread_member_ids_property(
    thread, user_thread, user, other_user, django_assert_num_queries
):
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)
    PrivateThreadMember.objects.create(thread=thread, user=user, is_owner=False)
    PrivateThreadMember.objects.create(thread=user_thread, user=user, is_owner=True)
    PrivateThreadMember.objects.create(
        thread=user_thread, user=other_user, is_owner=False
    )

    with django_assert_num_queries(1):
        prefetch_private_thread_member_ids([thread, user_thread])

        assert thread.private_thread_member_ids == [other_user.id, user.id]
        assert user_thread.private_thread_member_ids == [user.id, other_user.id]


def test_get_private_thread_members_returns_thread_owner_and_members_list(
    thread, user, other_user, django_assert_num_queries
):
    PrivateThreadMember.objects.create(thread=thread, user=user, is_owner=False)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    with django_assert_num_queries(1):
        owner, members = get_private_thread_members(thread)

    assert owner == other_user
    assert members == [user, other_user]


def test_get_private_thread_members_sets_thread_owner_and_member_ids_properties(
    thread, user, other_user, django_assert_num_queries
):
    PrivateThreadMember.objects.create(thread=thread, user=user, is_owner=False)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    with django_assert_num_queries(1):
        get_private_thread_members(thread)
        assert thread.private_thread_owner_id == other_user.id
        assert thread.private_thread_member_ids == [user.id, other_user.id]


def test_add_private_thread_member_adds_new_member_to_private_thread(
    user, private_thread
):
    assert add_private_thread_member(private_thread, user)

    private_thread.private_thread_members == [user]
    private_thread.private_thread_member_ids == [user.id]

    owner, members = get_private_thread_members(private_thread)
    assert owner is None
    assert members == [user]


def test_add_private_thread_member_returns_false_if_user_is_already_private_thread_member_using_db(
    django_assert_num_queries, user, other_user, moderator, user_private_thread
):
    with django_assert_num_queries(1):
        assert not add_private_thread_member(user_private_thread, user)

    user_private_thread.private_thread_members == [user, other_user, moderator]
    user_private_thread.private_thread_member_ids == [
        user.id,
        other_user.id,
        moderator.id,
    ]

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, other_user, moderator]


def test_add_private_thread_member_returns_false_if_user_is_already_private_thread_member_using_thread_cache(
    django_assert_num_queries, user, other_user, moderator, user_private_thread
):
    get_private_thread_members(user_private_thread)

    with django_assert_num_queries(0):
        assert not add_private_thread_member(user_private_thread, user)

    user_private_thread.private_thread_members == [user, other_user, moderator]
    user_private_thread.private_thread_member_ids == [
        user.id,
        other_user.id,
        moderator.id,
    ]

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, other_user, moderator]


def test_set_private_thread_owner_sets_member_as_private_thread_owner(
    user, other_user, moderator, user_private_thread
):
    assert set_private_thread_owner(user_private_thread, other_user)

    user_private_thread.private_thread_owner == other_user
    user_private_thread.private_thread_owner_id == other_user.id

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == other_user
    assert members == [user, other_user, moderator]


def test_set_private_thread_owner_returns_true_if_existing_owner_was_used(
    user, other_user, moderator, user_private_thread
):
    assert set_private_thread_owner(user_private_thread, user)

    user_private_thread.private_thread_owner == other_user
    user_private_thread.private_thread_owner_id == other_user.id

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, other_user, moderator]


def test_set_private_thread_owner_returns_false_if_new_owner_is_not_set(
    user, other_user, moderator, user_private_thread
):
    PrivateThreadMember.objects.filter(
        thread=user_private_thread, user=other_user
    ).delete()

    assert not set_private_thread_owner(user_private_thread, other_user)

    user_private_thread.private_thread_owner == user
    user_private_thread.private_thread_owner_id == user.id

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, moderator]


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


def test_remove_private_thread_member_updates_private_thread_member_cache(
    user, other_user, moderator, user_private_thread
):
    get_private_thread_members(user_private_thread)

    remove_private_thread_member(user, user_private_thread, user)

    user_private_thread.private_thread_members == [other_user, moderator]
    user_private_thread.private_thread_member_ids == [other_user.id, moderator.id]
