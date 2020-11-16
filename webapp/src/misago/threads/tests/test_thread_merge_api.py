from django.urls import reverse

from .. import test
from ...categories.models import Category
from ...readtracker import poststracker
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
    def test_other_thread_isnt_mergeable(self):
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
    def test_merge_threads(self):
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

        # other thread has two posts and an event now
        self.assertEqual(other_thread.post_set.count(), 3)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_kept_reads(self):
        """api keeps both threads readtrackers after merge"""
        other_thread = test.post_thread(self.other_category)

        poststracker.save_read(self.user, self.thread.first_post)
        poststracker.save_read(self.user, other_thread.first_post)

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

        # posts reads are kept
        postreads = self.user.postread_set.filter(post__is_event=False).order_by("id")

        self.assertEqual(
            list(postreads.values_list("post_id", flat=True)),
            [self.thread.first_post_id, other_thread.first_post_id],
        )
        self.assertEqual(postreads.filter(thread=other_thread).count(), 2)
        self.assertEqual(postreads.filter(category=self.other_category).count(), 2)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_kept_subs(self):
        """api keeps other thread's subscription after merge"""
        other_thread = test.post_thread(self.other_category)

        self.user.subscription_set.create(
            thread=self.thread,
            category=self.thread.category,
            last_read_on=self.thread.last_post_on,
            send_email=False,
        )

        self.assertEqual(self.user.subscription_set.count(), 1)
        self.user.subscription_set.get(thread=self.thread)
        self.user.subscription_set.get(category=self.category)

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

        # subscriptions are kept
        self.assertEqual(self.user.subscription_set.count(), 1)
        self.user.subscription_set.get(thread=other_thread)
        self.user.subscription_set.get(category=self.other_category)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_moved_subs(self):
        """api keeps other thread's subscription after merge"""
        other_thread = test.post_thread(self.other_category)

        self.user.subscription_set.create(
            thread=other_thread,
            category=other_thread.category,
            last_read_on=other_thread.last_post_on,
            send_email=False,
        )

        self.assertEqual(self.user.subscription_set.count(), 1)
        self.user.subscription_set.get(thread=other_thread)
        self.user.subscription_set.get(category=self.other_category)

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

        # subscriptions are kept
        self.assertEqual(self.user.subscription_set.count(), 1)
        self.user.subscription_set.get(thread=other_thread)
        self.user.subscription_set.get(category=self.other_category)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_handle_subs_colision(self):
        """api resolves conflicting thread subscriptions after merge"""
        self.user.subscription_set.create(
            thread=self.thread,
            category=self.thread.category,
            last_read_on=self.thread.last_post_on,
            send_email=False,
        )

        other_thread = test.post_thread(self.other_category)

        self.user.subscription_set.create(
            thread=other_thread,
            category=other_thread.category,
            last_read_on=other_thread.last_post_on,
            send_email=False,
        )

        self.assertEqual(self.user.subscription_set.count(), 2)
        self.user.subscription_set.get(thread=self.thread)
        self.user.subscription_set.get(category=self.category)
        self.user.subscription_set.get(thread=other_thread)
        self.user.subscription_set.get(category=self.other_category)

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

        # subscriptions are kept
        self.assertEqual(self.user.subscription_set.count(), 1)
        self.user.subscription_set.get(thread=other_thread)
        self.user.subscription_set.get(category=self.other_category)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_kept_best_answer(self):
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

        # other thread has three posts and an event now
        self.assertEqual(other_thread.post_set.count(), 4)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # best answer is kept in other thread
        other_thread = Thread.objects.get(pk=other_thread.pk)
        self.assertEqual(other_thread.best_answer, best_answer)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_moved_best_answer(self):
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

        # other thread has three posts and an event now
        self.assertEqual(other_thread.post_set.count(), 4)

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
    def test_threads_merge_conflict_unmark_all_best_answers(self):
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

        # other thread has four posts and an event now
        self.assertEqual(other_thread.post_set.count(), 5)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # final thread has no marked best answer
        self.assertIsNone(Thread.objects.get(pk=other_thread.pk).best_answer_id)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_keep_first_best_answer(self):
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

        # other thread has four posts and an event now
        self.assertEqual(other_thread.post_set.count(), 5)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # other thread's best answer was unchanged
        self.assertEqual(
            Thread.objects.get(pk=other_thread.pk).best_answer_id, best_answer.id
        )

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_keep_other_best_answer(self):
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

        # other thread has four posts and an event now
        self.assertEqual(other_thread.post_set.count(), 5)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # other thread's best answer was changed to merged in thread's answer
        self.assertEqual(
            Thread.objects.get(pk=other_thread.pk).best_answer_id, other_best_answer.id
        )

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_kept_poll(self):
        """api merges two threads successfully, keeping poll from other thread"""
        other_thread = test.post_thread(self.other_category)
        poll = test.post_poll(other_thread, self.user)

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

        # other thread has two posts and an event now
        self.assertEqual(other_thread.post_set.count(), 3)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # poll and its votes were kept
        self.assertEqual(
            Poll.objects.filter(pk=poll.pk, thread=other_thread).count(), 1
        )
        self.assertEqual(
            PollVote.objects.filter(poll=poll, thread=other_thread).count(), 4
        )

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_moved_poll(self):
        """api merges two threads successfully, moving poll from old thread"""
        other_thread = test.post_thread(self.other_category)
        poll = test.post_poll(self.thread, self.user)

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

        # other thread has two posts and an event now
        self.assertEqual(other_thread.post_set.count(), 3)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # poll and its votes were moved
        self.assertEqual(
            Poll.objects.filter(pk=poll.pk, thread=other_thread).count(), 1
        )
        self.assertEqual(
            PollVote.objects.filter(poll=poll, thread=other_thread).count(), 4
        )

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_polls(self):
        """api errors on merge conflict, returning list of available polls"""
        other_thread = test.post_thread(self.other_category)
        poll = test.post_poll(self.thread, self.user)
        other_poll = test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "polls": [
                    ["0", "Delete all polls"],
                    [str(poll.pk), "%s (%s)" % (poll.question, poll.thread.title)],
                    [
                        str(other_poll.pk),
                        "%s (%s)" % (other_poll.question, other_poll.thread.title),
                    ],
                ]
            },
        )

        # polls and votes were untouched
        self.assertEqual(Poll.objects.count(), 2)
        self.assertEqual(PollVote.objects.count(), 8)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_poll_invalid_resolution(self):
        """api errors on invalid merge conflict resolution"""
        other_thread = test.post_thread(self.other_category)

        test.post_poll(self.thread, self.user)
        test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            {
                "other_thread": other_thread.get_absolute_url(),
                "poll": Poll.objects.all()[0].pk + 10,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid choice."})

        # polls and votes were untouched
        self.assertEqual(Poll.objects.count(), 2)
        self.assertEqual(PollVote.objects.count(), 8)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_delete_all_polls(self):
        """api deletes all polls when delete all choice is selected"""
        other_thread = test.post_thread(self.other_category)
        test.post_poll(self.thread, self.user)
        test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link, {"other_thread": other_thread.get_absolute_url(), "poll": 0}
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

        # other thread has two posts and an event now
        self.assertEqual(other_thread.post_set.count(), 3)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # polls and votes are gone
        self.assertEqual(Poll.objects.count(), 0)
        self.assertEqual(PollVote.objects.count(), 0)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_keep_first_poll(self):
        """api deletes other poll on merge"""
        other_thread = test.post_thread(self.other_category)
        poll = test.post_poll(self.thread, self.user)
        other_poll = test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            {"other_thread": other_thread.get_absolute_url(), "poll": poll.pk},
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

        # other thread has two posts and an event now
        self.assertEqual(other_thread.post_set.count(), 3)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # other poll and its votes are gone
        self.assertEqual(Poll.objects.filter(thread=self.thread).count(), 0)
        self.assertEqual(PollVote.objects.filter(thread=self.thread).count(), 0)

        self.assertEqual(Poll.objects.filter(thread=other_thread).count(), 1)
        self.assertEqual(PollVote.objects.filter(thread=other_thread).count(), 4)

        Poll.objects.get(pk=poll.pk)
        with self.assertRaises(Poll.DoesNotExist):
            Poll.objects.get(pk=other_poll.pk)

    @patch_other_category_acl({"can_merge_threads": True})
    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_keep_other_poll(self):
        """api deletes first poll on merge"""
        other_thread = test.post_thread(self.other_category)
        poll = test.post_poll(self.thread, self.user)
        other_poll = test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            {"other_thread": other_thread.get_absolute_url(), "poll": other_poll.pk},
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

        # other thread has two posts and an event now
        self.assertEqual(other_thread.post_set.count(), 3)

        # first thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # other poll and its votes are gone
        self.assertEqual(Poll.objects.filter(thread=self.thread).count(), 0)
        self.assertEqual(PollVote.objects.filter(thread=self.thread).count(), 0)

        self.assertEqual(Poll.objects.filter(thread=other_thread).count(), 1)
        self.assertEqual(PollVote.objects.filter(thread=other_thread).count(), 4)

        Poll.objects.get(pk=other_poll.pk)
        with self.assertRaises(Poll.DoesNotExist):
            Poll.objects.get(pk=poll.pk)
