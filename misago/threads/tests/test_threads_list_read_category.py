from datetime import timedelta

from ...readtracker.models import ReadCategory, ReadThread


def test_unread_category_without_unread_threads_is_marked_read(
    thread_factory, default_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    threads = (
        thread_factory(
            default_category,
            started_on=-900,
        ),
        thread_factory(
            default_category,
            started_on=-600,
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
    thread_factory, default_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    thread = thread_factory(
        default_category,
        started_on=-2400,
    )

    read_category = ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=thread.last_post_on,
    )

    read_thread = thread_factory(
        default_category,
        started_on=-1200,
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
    thread_factory, default_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    read_thread = thread_factory(
        default_category,
        started_on=-900,
    )

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=read_thread,
        read_time=read_thread.last_post_on,
    )

    thread_factory(
        default_category,
        started_on=-600,
    )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert ReadThread.objects.exists()
    assert not ReadCategory.objects.exists()
