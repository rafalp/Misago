from ..members import get_private_thread_members
from ..models import PrivateThreadMember


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
