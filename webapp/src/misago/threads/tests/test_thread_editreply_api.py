from datetime import timedelta

from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from django.utils import timezone

from .. import test
from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase
from ..models import Post, Thread
from ..test import patch_category_acl


class EditReplyTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category=self.category)
        self.post = test.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            "misago:api:thread-post-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": self.post.pk},
        )

    def put(self, url, data=None):
        content = encode_multipart(BOUNDARY, data or {})
        return self.client.put(url, content, content_type=MULTIPART_CONTENT)

    def test_cant_edit_reply_as_guest(self):
        """user has to be authenticated to be able to edit reply"""
        self.logout_user()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_thread_visibility(self):
        """thread's visibility is validated"""
        with patch_category_acl({"can_see": False}):
            response = self.put(self.api_link)
            self.assertEqual(response.status_code, 404)

        with patch_category_acl({"can_browse": False}):
            response = self.put(self.api_link)
            self.assertEqual(response.status_code, 404)

        with patch_category_acl({"can_see_all_threads": False}):
            response = self.put(self.api_link)
            self.assertEqual(response.status_code, 404)

    @patch_category_acl({"can_edit_posts": 0})
    def test_cant_edit_reply(self):
        """permission to edit reply is validated"""
        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't edit posts in this category."}
        )

    @patch_category_acl({"can_edit_posts": 1})
    def test_cant_edit_other_user_reply(self):
        """permission to edit reply by other users is validated"""
        self.post.poster = None
        self.post.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't edit other users posts in this category."},
        )

    @patch_category_acl({"can_edit_posts": 1, "post_edit_time": 1})
    def test_edit_too_old(self):
        """permission to edit reply within timelimit is validated"""
        self.post.posted_on = timezone.now() - timedelta(minutes=5)
        self.post.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't edit posts that are older than 1 minute."},
        )

    @patch_category_acl({"can_edit_posts": 1, "can_close_threads": False})
    def test_closed_category_no_permission(self):
        """permssion to edit reply in closed category is validated"""
        self.category.is_closed = True
        self.category.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't edit posts in it."},
        )

    @patch_category_acl({"can_edit_posts": 1, "can_close_threads": True})
    def test_closed_category(self):
        """permssion to edit reply in closed category is validated"""
        self.category.is_closed = True
        self.category.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 400)

    @patch_category_acl({"can_edit_posts": 1, "can_close_threads": False})
    def test_closed_thread_no_permission(self):
        """permssion to edit reply in closed thread is validated"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't edit posts in it."},
        )

    @patch_category_acl({"can_edit_posts": 1, "can_close_threads": True})
    def test_closed_thread(self):
        """permssion to edit reply in closed thread is validated"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 400)

    @patch_category_acl({"can_edit_posts": 1, "can_protect_posts": False})
    def test_protected_post_no_permission(self):
        """permssion to edit protected post is validated"""
        self.post.is_protected = True
        self.post.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This post is protected. You can't edit it."}
        )

    @patch_category_acl({"can_edit_posts": 1, "can_protect_posts": True})
    def test_protected_post_no(self):
        """permssion to edit protected post is validated"""
        self.post.is_protected = True
        self.post.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 400)

    @patch_category_acl({"can_edit_posts": 1})
    def test_empty_data(self):
        """no data sent handling has no showstoppers"""
        response = self.put(self.api_link, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"post": ["You have to enter a message."]})

    @patch_category_acl({"can_edit_posts": 1})
    def test_invalid_data(self):
        """api errors for invalid request data"""
        response = self.client.put(
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

    @patch_category_acl({"can_edit_posts": 1})
    def test_edit_event(self):
        """events can't be edited"""
        self.post.is_event = True
        self.post.save()

        response = self.put(self.api_link, data={})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "Events can't be edited."})

    @patch_category_acl({"can_edit_posts": 1})
    def test_post_is_validated(self):
        """post is validated"""
        response = self.put(self.api_link, data={"post": "a"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "post": [
                    "Posted message should be at least 5 characters long (it has 1)."
                ]
            },
        )

    @patch_category_acl({"can_edit_posts": 1})
    def test_edit_reply_no_change(self):
        """endpoint isn't bumping edits count if no change was made to post's body"""
        self.assertEqual(self.post.edits_record.count(), 0)

        response = self.put(self.api_link, data={"post": self.post.original})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.post.parsed)

        post = self.thread.post_set.order_by("id").last()
        self.assertEqual(post.edits, 0)
        self.assertEqual(post.original, self.post.original)
        self.assertIsNone(post.last_editor_id, self.user.id)
        self.assertIsNone(post.last_editor_name, self.user.username)
        self.assertIsNone(post.last_editor_slug, self.user.slug)

        self.assertEqual(self.post.edits_record.count(), 0)

    @patch_category_acl({"can_edit_posts": 1})
    def test_edit_reply(self):
        """endpoint updates reply"""
        self.assertEqual(self.post.edits_record.count(), 0)

        response = self.put(self.api_link, data={"post": "This is test edit!"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, "<p>This is test edit!</p>")

        self.assertEqual(self.user.audittrail_set.count(), 1)

        post = self.thread.post_set.order_by("id").last()
        self.assertEqual(post.edits, 1)
        self.assertEqual(post.original, "This is test edit!")
        self.assertEqual(post.last_editor_id, self.user.id)
        self.assertEqual(post.last_editor_name, self.user.username)
        self.assertEqual(post.last_editor_slug, self.user.slug)

        self.assertEqual(self.post.edits_record.count(), 1)

        post_edit = post.edits_record.last()
        self.assertEqual(post_edit.edited_from, self.post.original)
        self.assertEqual(post_edit.edited_to, post.original)

        self.assertEqual(post_edit.editor_id, self.user.id)
        self.assertEqual(post_edit.editor_name, self.user.username)
        self.assertEqual(post_edit.editor_slug, self.user.slug)

    @patch_category_acl({"can_edit_posts": 2, "can_hide_threads": 1})
    def test_edit_first_post_hidden(self):
        """endpoint updates hidden thread's first post"""
        self.thread.is_hidden = True
        self.thread.save()
        self.thread.first_post.is_hidden = True
        self.thread.first_post.save()

        api_link = reverse(
            "misago:api:thread-post-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": self.thread.first_post.pk},
        )

        response = self.put(api_link, data={"post": "This is test edit!"})
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_edit_posts": 1, "can_protect_posts": True})
    def test_protect_post(self):
        """can protect post"""
        response = self.put(
            self.api_link, data={"post": "Lorem ipsum dolor met!", "protect": 1}
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by("id").last()
        self.assertTrue(post.is_protected)

    @patch_category_acl({"can_edit_posts": 1, "can_protect_posts": False})
    def test_protect_post_no_permission(self):
        """cant protect post without permission"""
        response = self.put(
            self.api_link, data={"post": "Lorem ipsum dolor met!", "protect": 1}
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by("id").last()
        self.assertFalse(post.is_protected)

    @patch_category_acl({"can_edit_posts": 1})
    def test_post_unicode(self):
        """unicode characters can be posted"""
        response = self.put(
            self.api_link, data={"post": "Chrzążczyżewoszyce, powiat Łękółody."}
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_edit_posts": 1})
    def test_reply_category_moderation_queue(self):
        """edit sends reply to queue due to category setup"""
        self.category.require_edits_approval = True
        self.category.save()

        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.all()[:1][0]
        self.assertTrue(post.is_unapproved)

    @patch_category_acl({"can_edit_posts": 1})
    @patch_user_acl({"can_approve_content": True})
    def test_reply_category_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        self.category.require_edits_approval = True
        self.category.save()

        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

    @patch_category_acl({"can_edit_posts": 1, "require_edits_approval": True})
    def test_reply_user_moderation_queue(self):
        """edit sends reply to queue due to user acl"""
        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.all()[:1][0]
        self.assertTrue(post.is_unapproved)

    @patch_category_acl({"can_edit_posts": 1, "require_edits_approval": True})
    @patch_user_acl({"can_approve_content": True})
    def test_reply_user_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

    @patch_category_acl(
        {
            "can_edit_posts": 1,
            "require_threads_approval": True,
            "require_replies_approval": True,
        }
    )
    def test_reply_omit_other_moderation_queues(self):
        """other queues are omitted"""
        self.category.require_threads_approval = True
        self.category.require_replies_approval = True
        self.category.save()

        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

    def setUpFirstReplyTest(self):
        self.post = self.thread.first_post

        self.post.poster = self.user
        self.post.save()

        self.api_link = reverse(
            "misago:api:thread-post-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": self.post.pk},
        )

    @patch_category_acl({"can_edit_posts": 1})
    def test_first_reply_category_moderation_queue(self):
        """edit sends thread to queue due to category setup"""
        self.setUpFirstReplyTest()

        self.category.require_edits_approval = True
        self.category.save()

        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertTrue(thread.is_unapproved)
        self.assertTrue(thread.has_unapproved_posts)

        post = Post.objects.get(pk=self.post.pk)
        self.assertTrue(post.is_unapproved)

    @patch_category_acl({"can_edit_posts": 1})
    @patch_user_acl({"can_approve_content": True})
    def test_first_reply_category_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        self.setUpFirstReplyTest()

        self.category.require_edits_approval = True
        self.category.save()

        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

        post = Post.objects.get(pk=self.post.pk)
        self.assertFalse(post.is_unapproved)

    @patch_category_acl({"can_edit_posts": 1, "require_edits_approval": True})
    def test_first_reply_user_moderation_queue(self):
        """edit sends thread to queue due to user acl"""
        self.setUpFirstReplyTest()

        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertTrue(thread.is_unapproved)
        self.assertTrue(thread.has_unapproved_posts)

        post = Post.objects.get(pk=self.post.pk)
        self.assertTrue(post.is_unapproved)

    @patch_category_acl({"can_edit_posts": 1, "require_edits_approval": True})
    @patch_user_acl({"can_approve_content": True})
    def test_first_reply_user_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        self.setUpFirstReplyTest()

        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

        post = Post.objects.get(pk=self.post.pk)
        self.assertFalse(post.is_unapproved)

    @patch_category_acl(
        {
            "can_edit_posts": 1,
            "require_threads_approval": True,
            "require_replies_approval": True,
        }
    )
    def test_first_reply_omit_other_moderation_queues(self):
        """other queues are omitted"""
        self.setUpFirstReplyTest()

        self.category.require_threads_approval = True
        self.category.require_replies_approval = True
        self.category.save()

        response = self.put(self.api_link, data={"post": "Lorem ipsum dolor met!"})
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

        post = Post.objects.get(pk=self.post.pk)
        self.assertFalse(post.is_unapproved)
