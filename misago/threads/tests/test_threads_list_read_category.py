from datetime import timedelta

from django.utils import timezone

from ...readtracker.models import ReadCategory, ReadThread
from ..test import post_thread


def test_unread_category_without_unread_threads_is_marked_read(
    default_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    threads = (
        post_thread(
            default_category,
            started_on=timezone.now() - timedelta(minutes=40),
        ),
        post_thread(
            default_category,
            started_on=timezone.now() - timedelta(minutes=20),
        ),
    )

    for thread in threads:
        ReadThread.objects.create(
            user=user,
            category=default_category,
            thread=thread,
            read_time=thread.last_post_on,
        )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    ReadCategory.objects.get(user=user, category=default_category)


def test_unread_category_read_entry_without_unread_threads_is_marked_read(
    default_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    post_thread(
        default_category,
        started_on=timezone.now() - timedelta(minutes=40),
    )

    read_category = ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now() - timedelta(minutes=30),
    )

    read_thread = post_thread(
        default_category,
        started_on=timezone.now() - timedelta(minutes=20),
    )

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=read_thread,
        read_time=read_thread.last_post_on,
    )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    new_read_category = ReadCategory.objects.get(user=user, category=default_category)
    assert new_read_category.id == read_category.id
    assert new_read_category.read_time > read_category.read_time


def test_unread_category_with_unread_thread_is_not_marked_read(
    default_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    read_thread = post_thread(
        default_category,
        started_on=timezone.now() - timedelta(minutes=40),
    )

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=read_thread,
        read_time=read_thread.last_post_on,
    )

    post_thread(
        default_category,
        started_on=timezone.now() - timedelta(minutes=20),
    )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert ReadThread.objects.exists()
    assert not ReadCategory.objects.exists()
