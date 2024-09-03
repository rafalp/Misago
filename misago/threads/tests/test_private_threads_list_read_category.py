from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from ...readtracker.models import ReadCategory, ReadThread
from ..models import Thread, ThreadParticipant
from ..test import post_thread


def make_user_participant(user):
    for thread in Thread.objects.all():
        ThreadParticipant.objects.create(user=user, thread=thread)


def test_private_threads_list_without_unread_threads_is_marked_read(
    private_threads_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    threads = (
        post_thread(
            private_threads_category,
            started_on=timezone.now() - timedelta(minutes=40),
        ),
        post_thread(
            private_threads_category,
            started_on=timezone.now() - timedelta(minutes=20),
        ),
    )

    for thread in threads:
        ReadThread.objects.create(
            user=user,
            category=private_threads_category,
            thread=thread,
            read_time=thread.last_post_on,
        )

    private_threads_category.synchronize()
    private_threads_category.save()

    make_user_participant(user)

    response = user_client.get(reverse("misago:private-threads"))
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    ReadCategory.objects.get(user=user, category=private_threads_category)


def test_private_threads_list_without_unread_threads_clears_user_unread_threads_count(
    private_threads_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.unread_private_threads = 50
    user.save()

    threads = (
        post_thread(
            private_threads_category,
            started_on=timezone.now() - timedelta(minutes=40),
        ),
        post_thread(
            private_threads_category,
            started_on=timezone.now() - timedelta(minutes=20),
        ),
    )

    for thread in threads:
        ReadThread.objects.create(
            user=user,
            category=private_threads_category,
            thread=thread,
            read_time=thread.last_post_on,
        )

    private_threads_category.synchronize()
    private_threads_category.save()

    make_user_participant(user)

    response = user_client.get(reverse("misago:private-threads"))
    assert response.status_code == 200

    user.refresh_from_db()
    assert user.unread_private_threads == 0


def test_private_threads_list_read_entry_without_unread_threads_is_marked_read(
    private_threads_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    post_thread(
        private_threads_category,
        started_on=timezone.now() - timedelta(minutes=40),
    )

    read_category = ReadCategory.objects.create(
        user=user,
        category=private_threads_category,
        read_time=timezone.now() - timedelta(minutes=30),
    )

    read_thread = post_thread(
        private_threads_category,
        started_on=timezone.now() - timedelta(minutes=20),
    )

    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=read_thread,
        read_time=read_thread.last_post_on,
    )

    private_threads_category.synchronize()
    private_threads_category.save()

    make_user_participant(user)

    response = user_client.get(reverse("misago:private-threads"))
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    new_read_category = ReadCategory.objects.get(
        user=user, category=private_threads_category
    )
    assert new_read_category.id == read_category.id
    assert new_read_category.read_time > read_category.read_time


def test_private_threads_list_with_unread_thread_is_not_marked_read(
    private_threads_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    read_thread = post_thread(
        private_threads_category,
        started_on=timezone.now() - timedelta(minutes=40),
    )

    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=read_thread,
        read_time=read_thread.last_post_on,
    )

    post_thread(
        private_threads_category,
        started_on=timezone.now() - timedelta(minutes=20),
    )

    private_threads_category.synchronize()
    private_threads_category.save()

    make_user_participant(user)

    response = user_client.get(reverse("misago:private-threads"))
    assert response.status_code == 200

    assert ReadThread.objects.exists()
    assert not ReadCategory.objects.exists()
