from unittest.mock import patch

import pytest
from django.urls import reverse

from ...notifications.models import Notification
from .. import test
from ...categories.models import Category
from ..models import Poll, PollVote, Thread
from ..test import patch_category_acl, patch_other_category_acl
from .test_threads_api import ThreadsApiTestCase


class ThreadMergeApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        Category(name="Other Category", slug="other-category").insert_at(
            self.category, position="last-child", save=True
        )
        self.other_category = Category.objects.get(slug="other-category")

        self.api_link = reverse(
            "misago:api:thread-merge", kwargs={"pk": self.thread.pk}
        )

    @patch_category_acl({"can_merge_threads": False})
    def test_merge_no_permission(self):
        """api validates if thread can be merged with other one"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't merge threads in this category."}
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_no_url(self):
        """api validates if thread url was given"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Enter link to new thread."})

    @patch_category_acl({"can_merge_threads": True})
    def test_invalid_url(self):
        """api validates thread url"""
        response = self.client.post(
            self.api_link, {"other_thread": self.user.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "This is not a valid thread link."}
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_current_other_thread(self):
        """api validates if thread url given is to current thread"""
        response = self.client.post(
            self.api_link, {"other_thread": self.thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "You can't merge thread with itself."}
        )

    @patch_other_category_acl()
    @patch_category_acl({"can_merge_threads": True})
    def test_other_thread_exists(self):
        """api validates if other thread exists"""
        other_thread = test.post_thread(self.other_category)
        other_other_thread = other_thread.get_absolute_url()
        other_thread.delete()

        response = self.client.post(self.api_link, {"other_thread": other_other_thread})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "The thread you have entered link to doesn't exist "
                    "or you don't have permission to see it."
                )
            },
        )

    @patch_other_category_acl({"can_see": False})
    @patch_category_acl({"can_merge_threads": True})
    def test_other_thread_is_invisible(self):
        """api validates if other thread is visible"""
        other_thread = test.post_thread(self.other_category)

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "The thread you have entered link to doesn't exist "
                    "or you don't have permission to see it."
                )
            },
        )

    @patch_other_category_acl({"can_merge_threads": False})
    @patch_category_acl({"can_merge_threads": True})
    def test_other_thread_is_not_mergeable(self):
        """api validates if other thread can be merged"""
        other_thread = test.post_thread(self.other_category)

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "Other thread can't be merged with."}
        )

    @patch_other_category_acl({"can_merge_threads": True, "can_close_threads": False})
    @patch_category_acl({"can_merge_threads": True})
    def test_thread_category_is_closed(self):
        """api validates if thread's category is open"""
        other_thread = test.post_thread(self.other_category)

        self.category.is_closed = True
        self.category.save()

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't merge it's threads."},
        )

    @patch_other_category_acl({"can_merge_threads": True, "can_close_threads": False})
    @patch_category_acl({"can_merge_threads": True})
    def test_thread_is_closed(self):
        """api validates if thread is open"""
        other_thread = test.post_thread(self.other_category)

        self.thread.is_closed = True
        self.thread.save()

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't merge it with other threads."},
        )

    @patch_other_category_acl({"can_merge_threads": True, "can_close_threads": False})
    @patch_category_acl({"can_merge_threads": True})
    def test_other_thread_category_is_closed(self):
        """api validates if other thread's category is open"""
        other_thread = test.post_thread(self.other_category)

        self.other_category.is_closed = True
        self.other_category.save()

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Other thread's category is closed. You can't merge with it."},
        )

    @patch_other_category_acl({"can_merge_threads": True, "can_close_threads": False})
    @patch_category_acl({"can_merge_threads": True})
    def test_other_thread_is_closed(self):
        """api validates if other thread is open"""
        other_thread = test.post_thread(self.other_category)

        other_thread.is_closed = True
        other_thread.save()

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Other thread is closed and can't be merged with."},
        )

    @patch_other_category_acl({"can_merge_threads": True, "can_reply_threads": False})
    @patch_category_acl({"can_merge_threads": True})
    def test_other_thread_isnt_replyable(self):
        """api validates if other thread can be replied, which is condition for merge"""
        other_thread = test.post_thread(self.other_category)

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You can't merge this thread into thread you can't reply."},
        )

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    @patch("misago.threads.moderation.threads.delete_duplicate_watched_threads")
    def test_merge_threads(self, delete_duplicate_watched_threads_mock):
        """api merges two threads successfully"""
        other_thread = test.post_thread(self.other_category)

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": other_thread.id,
                "title": other_thread.title,
                "url": other_thread.get_absolute_url(),
            },
        )

        # other thread has two posts
        self.assertEqual(other_thread.post_set.count(), 2)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    @patch("misago.threads.moderation.threads.delete_duplicate_watched_threads")
    def test_merge_threads_kept_best_answer(
        self, delete_duplicate_watched_threads_mock
    ):
        """api merges two threads successfully, keeping best answer from old thread"""
        other_thread = test.post_thread(self.other_category)
        best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": other_thread.id,
                "title": other_thread.title,
                "url": other_thread.get_absolute_url(),
            },
        )

        # other thread has three posts
        self.assertEqual(other_thread.post_set.count(), 3)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # best answer is kept in other thread
        other_thread = Thread.objects.get(pk=other_thread.pk)
        self.assertEqual(other_thread.best_answer, best_answer)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    @patch("misago.threads.moderation.threads.delete_duplicate_watched_threads")
    def test_merge_threads_moved_best_answer(
        self, delete_duplicate_watched_threads_mock
    ):
        """api merges two threads successfully, moving best answer to old thread"""
        other_thread = test.post_thread(self.other_category)

        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": other_thread.id,
                "title": other_thread.title,
                "url": other_thread.get_absolute_url(),
            },
        )

        # other thread has three posts
        self.assertEqual(other_thread.post_set.count(), 3)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # best answer is kept in other thread
        other_thread = Thread.objects.get(pk=other_thread.pk)
        self.assertEqual(other_thread.best_answer, best_answer)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_merge_conflict_best_answer(self):
        """api errors on merge conflict, returning list of available best answers"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.other_category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "best_answers": [
                    ["0", "Unmark all best answers"],
                    [str(self.thread.id), self.thread.title],
                    [str(other_thread.id), other_thread.title],
                ]
            },
        )

        # best answers were untouched
        self.assertEqual(self.thread.post_set.count(), 2)
        self.assertEqual(other_thread.post_set.count(), 2)
        self.assertEqual(
            Thread.objects.get(pk=self.thread.pk).best_answer_id, best_answer.id
        )
        self.assertEqual(
            Thread.objects.get(pk=other_thread.pk).best_answer_id, other_best_answer.id
        )

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_best_answer_invalid_resolution(self):
        """api errors on invalid merge conflict resolution"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.other_category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link,
            {
                "other_thread": other_thread.get_absolute_url(),
                "best_answer": other_thread.id + 10,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid choice."})

        # best answers were untouched
        self.assertEqual(self.thread.post_set.count(), 2)
        self.assertEqual(other_thread.post_set.count(), 2)
        self.assertEqual(
            Thread.objects.get(pk=self.thread.pk).best_answer_id, best_answer.id
        )
        self.assertEqual(
            Thread.objects.get(pk=other_thread.pk).best_answer_id, other_best_answer.id
        )

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    @patch("misago.threads.moderation.threads.delete_duplicate_watched_threads")
    def test_threads_merge_conflict_unmark_all_best_answers(
        self, delete_duplicate_watched_threads_mock
    ):
        """api unmarks all best answers when unmark all choice is selected"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.other_category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link,
            {"other_thread": other_thread.get_absolute_url(), "best_answer": 0},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": other_thread.id,
                "title": other_thread.title,
                "url": other_thread.get_absolute_url(),
            },
        )

        # other thread has four posts
        self.assertEqual(other_thread.post_set.count(), 4)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # final thread has no marked best answer
        self.assertIsNone(Thread.objects.get(pk=other_thread.pk).best_answer_id)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    @patch("misago.threads.moderation.threads.delete_duplicate_watched_threads")
    def test_threads_merge_conflict_keep_first_best_answer(
        self, delete_duplicate_watched_threads_mock
    ):
        """api unmarks other best answer on merge"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.other_category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link,
            {
                "other_thread": other_thread.get_absolute_url(),
                "best_answer": self.thread.pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": other_thread.id,
                "title": other_thread.title,
                "url": other_thread.get_absolute_url(),
            },
        )

        # other thread has four posts
        self.assertEqual(other_thread.post_set.count(), 4)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # other thread's best answer was unchanged
        self.assertEqual(
            Thread.objects.get(pk=other_thread.pk).best_answer_id, best_answer.id
        )

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    @patch("misago.threads.moderation.threads.delete_duplicate_watched_threads")
    def test_threads_merge_conflict_keep_other_best_answer(
        self, delete_duplicate_watched_threads_mock
    ):
        """api unmarks first best answer on merge"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.other_category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link,
            {
                "other_thread": other_thread.get_absolute_url(),
                "best_answer": other_thread.pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": other_thread.id,
                "title": other_thread.title,
                "url": other_thread.get_absolute_url(),
            },
        )

        # other thread has four posts
        self.assertEqual(other_thread.post_set.count(), 4)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # other thread's best answer was changed to merged in thread's answer
        self.assertEqual(
            Thread.objects.get(pk=other_thread.pk).best_answer_id, other_best_answer.id
        )


@pytest.fixture
def delete_duplicate_watched_threads_mock(mocker):
    return mocker.patch(
        "misago.threads.moderation.threads.delete_duplicate_watched_threads"
    )


@patch_category_acl({"can_merge_threads": True})
def test_thread_merge_api_merges_notifications(
    delete_duplicate_watched_threads_mock,
    user,
    user_client,
    thread,
    other_thread,
):
    notification = Notification.objects.create(
        user=user,
        verb="TEST",
        category=other_thread.category,
        thread=other_thread,
        thread_title=other_thread.title,
        post=other_thread.first_post,
    )

    response = user_client.post(
        reverse("misago:api:thread-merge", kwargs={"pk": thread.pk}),
        json={
            "other_thread": other_thread.get_absolute_url(),
        },
    )

    assert response.status_code == 200

    notification.refresh_from_db()

    assert notification.category_id == other_thread.category_id
    assert notification.thread_id == other_thread.id
    assert notification.thread_title == other_thread.title


@patch_category_acl({"can_merge_threads": True})
def test_thread_merge_api_merges_watched_threads(
    delete_duplicate_watched_threads_mock,
    user,
    user_client,
    thread,
    other_thread,
    watched_thread_factory,
):
    watched_thread = watched_thread_factory(user, thread, send_emails=True)

    response = user_client.post(
        reverse("misago:api:thread-merge", kwargs={"pk": thread.pk}),
        json={
            "other_thread": other_thread.get_absolute_url(),
        },
    )

    assert response.status_code == 200

    watched_thread.refresh_from_db()

    assert watched_thread.category_id == other_thread.category_id
    assert watched_thread.thread_id == other_thread.id

    delete_duplicate_watched_threads_mock.delay.assert_called_once_with(other_thread.id)
