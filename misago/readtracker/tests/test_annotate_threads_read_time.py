from django.utils import timezone

from ...threads.models import Thread
from ..models import ReadCategory, ReadThread
from ..tracker import annotate_threads_read_time


def test_annotate_threads_read_time_is_noop_for_anonymous_user(anonymous_user, thread):
    queryset = annotate_threads_read_time(anonymous_user, Thread.objects.all())

    thread = queryset.get(id=thread.id)
    assert not hasattr(thread, "read_time")
    assert not hasattr(thread, "category_read_time")


def test_annotate_threads_read_time_sets_none_read_time_for_user_without_one(
    user, thread
):
    queryset = annotate_threads_read_time(user, Thread.objects.all())

    thread = queryset.get(id=thread.id)
    assert thread.read_time is None


def test_annotate_threads_read_time_sets_read_time_for_user_with_one(user, thread):
    read_time = timezone.now().replace(year=2012)

    ReadThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=read_time,
    )

    queryset = annotate_threads_read_time(user, Thread.objects.all())

    thread = queryset.get(id=thread.id)
    assert thread.read_time == read_time


def test_annotate_threads_read_time_sets_none_category_read_time_for_user_without_one(
    user, thread
):
    queryset = annotate_threads_read_time(user, Thread.objects.all())

    thread = queryset.get(id=thread.id)
    assert thread.category_read_time is None


def test_annotate_threads_read_time_sets_category_read_time_for_user_with_one(
    user, thread
):
    read_time = timezone.now().replace(year=2012)

    ReadCategory.objects.create(
        user=user,
        category=thread.category,
        read_time=read_time,
    )

    queryset = annotate_threads_read_time(user, Thread.objects.all())

    thread = queryset.get(id=thread.id)
    assert thread.category_read_time == read_time
