from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from ...notifications.models import Notification
from .. import test
from .test_threads_api import ThreadsApiTestCase


class PostReadApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.post = test.reply_thread(
            self.thread, poster=self.user, posted_on=timezone.now()
        )

        self.api_link = reverse(
            "misago:api:thread-post-read",
            kwargs={"thread_pk": self.thread.pk, "pk": self.post.pk},
        )

    def test_read_anonymous(self):
        """api validates if reading user is authenticated"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    def test_read_post(self):
        """api marks post as read"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.postread_set.count(), 1)
        self.user.postread_set.get(post=self.post)

        # one post read, first post is still unread
        self.assertFalse(response.json()["thread_is_read"])

        # read second post
        response = self.client.post(
            reverse(
                "misago:api:thread-post-read",
                kwargs={"thread_pk": self.thread.pk, "pk": self.thread.first_post.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.postread_set.count(), 2)
        self.user.postread_set.get(post=self.thread.first_post)

        # both posts are read
        self.assertTrue(response.json()["thread_is_read"])


def test_read_watched_thread_post_updates_watching_read_at_if_its_older_than_post(
    user, user_client, thread, reply, watched_thread_factory
):
    watched_thread = watched_thread_factory(user, thread, send_emails=True)
    watched_thread.read_at = timezone.now() - timedelta(seconds=1)
    watched_thread.save()

    response = user_client.post(
        reverse(
            "misago:api:thread-post-read",
            kwargs={"thread_pk": thread.pk, "pk": reply.pk},
        )
    )
    assert response.status_code == 200

    watched_thread.refresh_from_db()
    assert watched_thread.read_at == reply.posted_on


def test_read_watched_thread_post_skips_watching_read_at_if_its_newer_than_post(
    user, user_client, thread, reply, watched_thread_factory
):
    watched_thread = watched_thread_factory(user, thread, send_emails=True)
    watched_thread.read_at = timezone.now() + timedelta(seconds=5)
    watched_thread.save()

    response = user_client.post(
        reverse(
            "misago:api:thread-post-read",
            kwargs={"thread_pk": thread.pk, "pk": reply.pk},
        )
    )
    assert response.status_code == 200

    watched_thread.refresh_from_db()
    assert watched_thread.read_at > reply.posted_on


def test_read_thread_post_reads_its_unread_notifications(
    user, user_client, thread, reply
):
    notification = Notification.objects.create(
        user=user,
        verb="TEST",
        post=reply,
        is_read=False,
    )

    response = user_client.post(
        reverse(
            "misago:api:thread-post-read",
            kwargs={"thread_pk": thread.pk, "pk": reply.pk},
        )
    )
    assert response.status_code == 200

    notification.refresh_from_db()
    assert notification.is_read

    user.refresh_from_db()
    assert user.unread_notifications == 0


def test_read_thread_post_updates_unread_notifications_count(
    user, user_client, thread, reply
):
    user.unread_notifications = 5
    user.save()

    notification = Notification.objects.create(
        user=user,
        verb="TEST",
        post=reply,
        is_read=False,
    )
    other_notification = Notification.objects.create(
        user=user,
        verb="TEST",
        post=reply,
        is_read=False,
    )

    response = user_client.post(
        reverse(
            "misago:api:thread-post-read",
            kwargs={"thread_pk": thread.pk, "pk": reply.pk},
        )
    )
    assert response.status_code == 200

    notification.refresh_from_db()
    assert notification.is_read

    other_notification.refresh_from_db()
    assert other_notification.is_read

    user.refresh_from_db()
    assert user.unread_notifications == 3


def test_read_thread_post_excludes_other_users_notifications(
    user, user_client, other_user, thread, reply
):
    user.unread_notifications = 5
    user.save()

    notification = Notification.objects.create(
        user=user,
        verb="TEST",
        post=reply,
        is_read=False,
    )
    other_user_notification = Notification.objects.create(
        user=other_user,
        verb="TEST",
        post=reply,
        is_read=False,
    )

    response = user_client.post(
        reverse(
            "misago:api:thread-post-read",
            kwargs={"thread_pk": thread.pk, "pk": reply.pk},
        )
    )
    assert response.status_code == 200

    notification.refresh_from_db()
    assert notification.is_read

    other_user_notification.refresh_from_db()
    assert not other_user_notification.is_read

    user.refresh_from_db()
    assert user.unread_notifications == 4
