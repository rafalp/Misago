from django.utils import timezone

from ...threads.models import Thread
from ..models import ReadCategory, ReadThread
from ..tracker import thread_select_related_user_readthread


def test_thread_select_related_user_readthread_is_noop_for_anonymous_user(
    anonymous_user, thread
):
    queryset = thread_select_related_user_readthread(
        Thread.objects.all(), anonymous_user
    )

    thread = queryset.get(id=thread.id)
    assert not hasattr(thread, "user_readthread")
    assert not hasattr(thread, "user_readcategory_time")


def test_thread_select_related_user_readthread_doesnt_set_user_readthread_for_user_without_one(
    user, thread
):
    queryset = thread_select_related_user_readthread(Thread.objects.all(), user)

    thread = queryset.get(id=thread.id)
    assert not hasattr(thread, "user_readthread")


def test_thread_select_related_user_readthread_sets_threadread_for_user_with_one(
    user, thread
):
    read_time = timezone.now().replace(year=2012)

    threadread = ReadThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=read_time,
    )

    queryset = thread_select_related_user_readthread(Thread.objects.all(), user)

    thread = queryset.get(id=thread.id)
    assert thread.user_readthread == threadread


def test_thread_select_related_user_readthread_doesnt_set_user_readcategory_time_for_user_without_one(
    user, thread
):
    queryset = thread_select_related_user_readthread(Thread.objects.all(), user)

    thread = queryset.get(id=thread.id)
    assert not thread.user_readcategory_time


def test_thread_select_related_user_readthread_sets_user_readcategory_time_for_user_with_one(
    user, thread
):
    read_time = timezone.now().replace(year=2012)

    ReadCategory.objects.create(
        user=user,
        category=thread.category,
        read_time=read_time,
    )

    queryset = thread_select_related_user_readthread(Thread.objects.all(), user)

    thread = queryset.get(id=thread.id)
    assert thread.user_readcategory_time == read_time
