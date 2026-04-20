from ..tasks import synchronize_threads


def test_synchronize_threads_task_synchronizes_threads(thread, user_thread):
    thread.replies = 100
    thread.save()

    user_thread.replies = 200
    user_thread.save()

    synchronize_threads([thread.id, user_thread.id])

    thread.refresh_from_db()
    assert thread.replies == 0

    user_thread.refresh_from_db()
    assert user_thread.replies == 0
