from django.urls import reverse

from .. import test
from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase
from ..models import Thread
from ..test import patch_category_acl


class ReplyThreadTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category=self.category)

        self.api_link = reverse(
            "misago:api:thread-post-list", kwargs={"thread_pk": self.thread.pk}
        )

    def test_cant_reply_thread_as_guest(self):
        """user has to be authenticated to be able to post reply"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_thread_visibility(self):
        """thread's visibility is validated"""
        with patch_category_acl({"can_see": 0}):
            response = self.client.post(self.api_link)
            self.assertEqual(response.status_code, 404)

        with patch_category_acl({"can_browse": 0}):
            response = self.client.post(self.api_link)
            self.assertEqual(response.status_code, 404)

        with patch_category_acl({"can_see_all_threads": 0}):
            response = self.client.post(self.api_link)
            self.assertEqual(response.status_code, 404)

    @patch_category_acl({"can_reply_threads": False})
    def test_cant_reply_thread(self):
        """permission to reply thread is validated"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't reply to threads in this category."}
        )

    @patch_category_acl({"can_reply_threads": True, "can_close_threads": False})
    def test_closed_category_no_permission(self):
        """permssion to reply in closed category is validated"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't reply to threads in it."},
        )

    @patch_category_acl({"can_reply_threads": True, "can_close_threads": True})
    def test_closed_category(self):
        """permssion to reply in closed category is validated"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    @patch_category_acl({"can_reply_threads": True, "can_close_threads": False})
    def test_closed_thread_no_permission(self):
        """permssion to reply in closed thread is validated"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't reply to closed threads in this category."},
        )

    @patch_category_acl({"can_reply_threads": True, "can_close_threads": True})
    def test_closed_thread(self):
        """permssion to reply in closed thread is validated"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    @patch_category_acl({"can_reply_threads": True})
    def test_empty_data(self):
        """no data sent handling has no showstoppers"""
        response = self.client.post(self.api_link, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"post": ["You have to enter a message."]})

    @patch_category_acl({"can_reply_threads": True})
    def test_invalid_data(self):
        """api errors for invalid request data"""
        response = self.client.post(
            self.api_link, "false", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Invalid data. Expected a dictionary, but got bool."
                ]
            },
        )

    @patch_category_acl({"can_reply_threads": True})
    def test_post_is_validated(self):
        """post is validated"""
        response = self.client.post(self.api_link, data={"post": "a"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "post": [
                    "Posted message should be at least 5 characters long (it has 1)."
                ]
            },
        )

    @patch_category_acl({"can_reply_threads": True})
    def test_can_reply_thread(self):
        """endpoint creates new reply"""
        response = self.client.post(
            self.api_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, "<p>This is test response!</p>")

        # api increased user's posts counts
        self.reload_user()
        self.assertEqual(self.user.threads, 0)
        self.assertEqual(self.user.posts, 1)

        self.assertEqual(self.user.audittrail_set.count(), 1)

        post = self.user.post_set.all()[:1][0]
        self.assertEqual(post.category_id, self.category.pk)
        self.assertEqual(post.original, "This is test response!")
        self.assertEqual(post.poster_id, self.user.id)
        self.assertEqual(post.poster_name, self.user.username)

        self.assertEqual(thread.last_post_id, post.id)
        self.assertEqual(thread.last_poster_id, self.user.id)
        self.assertEqual(thread.last_poster_name, self.user.username)
        self.assertEqual(thread.last_poster_slug, self.user.slug)

        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(category.last_thread_id, thread.id)
        self.assertEqual(category.last_thread_title, thread.title)
        self.assertEqual(category.last_thread_slug, thread.slug)

        self.assertEqual(category.last_poster_id, self.user.id)
        self.assertEqual(category.last_poster_name, self.user.username)
        self.assertEqual(category.last_poster_slug, self.user.slug)

    @patch_category_acl({"can_reply_threads": True})
    def test_post_unicode(self):
        """unicode characters can be posted"""
        response = self.client.post(
            self.api_link, data={"post": "Chrzążczyżewoszyce, powiat Łękółody."}
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_reply_threads": True})
    def test_category_moderation_queue(self):
        """reply thread in category that requires approval"""
        self.category.require_replies_approval = True
        self.category.save()

        response = self.client.post(
            self.api_link, data={"post": "Lorem ipsum dolor met!"}
        )
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.is_unapproved)
        self.assertTrue(thread.has_unapproved_posts)
        self.assertEqual(thread.replies, self.thread.replies)

        post = self.user.post_set.all()[:1][0]
        self.assertTrue(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads)
        self.assertEqual(category.posts, self.category.posts)

    @patch_category_acl({"can_reply_threads": True})
    @patch_user_acl({"can_approve_content": True})
    def test_category_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        self.category.require_replies_approval = True
        self.category.save()

        response = self.client.post(
            self.api_link, data={"post": "Lorem ipsum dolor met!"}
        )
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)
        self.assertEqual(thread.replies, self.thread.replies + 1)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads)
        self.assertEqual(category.posts, self.category.posts + 1)

    @patch_category_acl({"can_reply_threads": True, "require_replies_approval": True})
    def test_user_moderation_queue(self):
        """reply thread by user that requires approval"""
        response = self.client.post(
            self.api_link, data={"post": "Lorem ipsum dolor met!"}
        )
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.is_unapproved)
        self.assertTrue(thread.has_unapproved_posts)
        self.assertEqual(thread.replies, self.thread.replies)

        post = self.user.post_set.all()[:1][0]
        self.assertTrue(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads)
        self.assertEqual(category.posts, self.category.posts)

    @patch_category_acl({"can_reply_threads": True, "require_replies_approval": True})
    @patch_user_acl({"can_approve_content": True})
    def test_user_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        response = self.client.post(
            self.api_link, data={"post": "Lorem ipsum dolor met!"}
        )
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)
        self.assertEqual(thread.replies, self.thread.replies + 1)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads)
        self.assertEqual(category.posts, self.category.posts + 1)

    @patch_category_acl(
        {
            "can_reply_threads": True,
            "require_threads_approval": True,
            "require_edits_approval": True,
        }
    )
    def test_omit_other_moderation_queues(self):
        """other queues are omitted"""
        self.category.require_threads_approval = True
        self.category.require_edits_approval = True
        self.category.save()

        response = self.client.post(
            self.api_link, data={"post": "Lorem ipsum dolor met!"}
        )
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)
        self.assertEqual(thread.replies, self.thread.replies + 1)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads)
        self.assertEqual(category.posts, self.category.posts + 1)
