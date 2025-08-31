from ..members import prefetch_private_thread_member_ids
from ..models import PrivateThreadMember


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
