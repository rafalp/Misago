from django.utils import timezone

from ...threads.models import Thread
from ..models import ReadCategory
from ..tracker import threads_annotate_user_readcategory_time


def test_threads_annotate_user_readcategory_time_is_noop_for_anonymous_user(
    anonymous_user, thread
):
    queryset = threads_annotate_user_readcategory_time(
        Thread.objects.all(), anonymous_user
    )

    thread = queryset.get(id=thread.id)
    assert not hasattr(thread, "user_readcategory_time")


def test_threads_annotate_user_readcategory_time_sets_none_user_readcategory_time_for_user_without_one(
    user, thread
):
    queryset = threads_annotate_user_readcategory_time(Thread.objects.all(), user)

    thread = queryset.get(id=thread.id)
    assert not thread.user_readcategory_time


def test_threads_annotate_user_readcategory_time_sets_user_readcategory_time_for_user_with_one(
    user, thread
):
    read_time = timezone.now().replace(year=2012)

    ReadCategory.objects.create(
        user=user,
        category=thread.category,
        read_time=read_time,
    )

    queryset = threads_annotate_user_readcategory_time(Thread.objects.all(), user)

    thread = queryset.get(id=thread.id)
    assert thread.user_readcategory_time == read_time
