from ..models import Notification
from ..users import notify_user


def test_notify_user_creates_notification_for_user(user):
    notification = notify_user(user, "TEST")
    assert notification
    assert notification.user == user
    assert notification.verb == "TEST"
    assert notification.actor is None
    assert notification.actor_name is None
    assert notification.category is None
    assert notification.thread is None
    assert notification.thread_title is None
    assert notification.post is None

    db_notification = Notification.objects.get(id=notification.id)
    assert db_notification.user == user
    assert db_notification.verb == "TEST"
    assert db_notification.actor is None
    assert db_notification.actor_name is None
    assert db_notification.category is None
    assert db_notification.thread is None
    assert db_notification.thread_title is None
    assert db_notification.post is None


def test_notify_user_increases_user_unread_notifications_counter(user):
    assert user.unread_notifications == 0
    assert notify_user(user, "TEST")

    user.refresh_from_db()
    assert user.unread_notifications == 1


def test_notify_user_sets_actor_on_notification(user, other_user):
    notification = notify_user(user, "TEST", actor=other_user)
    assert notification
    assert notification.user == user
    assert notification.verb == "TEST"
    assert notification.actor == other_user
    assert notification.actor_name == other_user.username
    assert notification.category is None
    assert notification.thread is None
    assert notification.thread_title is None
    assert notification.post is None

    db_notification = Notification.objects.get(id=notification.id)
    assert db_notification.user == user
    assert db_notification.verb == "TEST"
    assert db_notification.actor == other_user
    assert db_notification.actor_name == other_user.username
    assert db_notification.category is None
    assert db_notification.thread is None
    assert db_notification.thread_title is None
    assert db_notification.post is None


def test_notify_user_sets_category_on_notification(user, default_category):
    notification = notify_user(user, "TEST", category=default_category)
    assert notification
    assert notification.user == user
    assert notification.verb == "TEST"
    assert notification.actor is None
    assert notification.actor_name is None
    assert notification.category == default_category
    assert notification.thread is None
    assert notification.thread_title is None
    assert notification.post is None

    db_notification = Notification.objects.get(id=notification.id)
    assert db_notification.user == user
    assert db_notification.verb == "TEST"
    assert db_notification.actor is None
    assert db_notification.actor_name is None
    assert db_notification.category == default_category
    assert db_notification.thread is None
    assert db_notification.thread_title is None
    assert db_notification.post is None


def test_notify_user_sets_thread_on_notification(user, thread):
    notification = notify_user(user, "TEST", thread=thread)
    assert notification
    assert notification.user == user
    assert notification.verb == "TEST"
    assert notification.actor is None
    assert notification.actor_name is None
    assert notification.category is None
    assert notification.thread == thread
    assert notification.thread_title == thread.title
    assert notification.post is None

    db_notification = Notification.objects.get(id=notification.id)
    assert db_notification.user == user
    assert db_notification.verb == "TEST"
    assert db_notification.actor is None
    assert db_notification.actor_name is None
    assert db_notification.category is None
    assert db_notification.thread == thread
    assert db_notification.thread_title == thread.title
    assert db_notification.post is None


def test_notify_user_sets_post_on_notification(user, post):
    notification = notify_user(user, "TEST", post=post)
    assert notification
    assert notification.user == user
    assert notification.verb == "TEST"
    assert notification.actor is None
    assert notification.actor_name is None
    assert notification.category is None
    assert notification.thread is None
    assert notification.thread_title is None
    assert notification.post == post

    db_notification = Notification.objects.get(id=notification.id)
    assert db_notification.user == user
    assert db_notification.verb == "TEST"
    assert db_notification.actor is None
    assert db_notification.actor_name is None
    assert db_notification.category is None
    assert db_notification.thread is None
    assert db_notification.thread_title is None
    assert db_notification.post == post
