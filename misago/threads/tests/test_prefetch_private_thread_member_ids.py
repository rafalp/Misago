from ..models import ThreadParticipant
from ..privatethreads import prefetch_private_thread_member_ids


def test_prefetch_private_thread_member_ids_sets_thread_member_ids_property(
    thread, user_thread, user, other_user, django_assert_num_queries
):
    ThreadParticipant.objects.create(thread=thread, user=user, is_owner=False)
    ThreadParticipant.objects.create(thread=thread, user=other_user, is_owner=True)
    ThreadParticipant.objects.create(thread=user_thread, user=user, is_owner=True)
    ThreadParticipant.objects.create(
        thread=user_thread, user=other_user, is_owner=False
    )

    with django_assert_num_queries(1):
        prefetch_private_thread_member_ids([thread, user_thread])

        assert thread.private_thread_member_ids == [other_user.id, user.id]
        assert user_thread.private_thread_member_ids == [user.id, other_user.id]
