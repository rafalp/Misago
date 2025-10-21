import pytest

from ...privatethreads.models import PrivateThreadMember
from ...threads.models import Thread


def test_delete_user_deletes_private_thread_if_it_has_no_other_members(
    user, user_private_thread
):
    PrivateThreadMember.objects.exclude(user=user).delete()

    user.delete(anonymous_username="Anon")

    with pytest.raises(Thread.DoesNotExist):
        user_private_thread.refresh_from_db()


def test_delete_user_leaves_private_thread_if_it_has_other_members(
    user, user_private_thread
):
    user.delete(anonymous_username="Anon")
    user_private_thread.refresh_from_db()
