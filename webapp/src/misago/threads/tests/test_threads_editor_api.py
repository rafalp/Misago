import os

from django.urls import reverse

from .. import test
from ...acl import useracl
from ...acl.objectacl import add_acl_to_obj
from ...categories.models import Category
from ...conftest import get_cache_versions
from ...users.test import AuthenticatedUserTestCase
from ..models import Attachment
from ..serializers import AttachmentSerializer
from ..test import patch_category_acl

TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
TEST_DOCUMENT_PATH = os.path.join(TESTFILES_DIR, "document.pdf")

cache_versions = get_cache_versions()


class EditorApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")


class ThreadPostEditorApiTests(EditorApiTestCase):
    def setUp(self):
        super().setUp()

        self.api_link = reverse("misago:api:thread-editor")

    def test_anonymous_user_request(self):
        """endpoint validates if user is authenticated"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You need to be signed in to start threads."}
        )

    @patch_category_acl({"can_browse": False})
    def test_category_visibility_validation(self):
        """endpoint omits non-browseable categories"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "No categories that allow new threads are available "
                    "to you at the moment."
                )
            },
        )

    @patch_category_acl({"can_start_threads": False})
    def test_category_disallowing_new_threads(self):
        """endpoint omits category disallowing starting threads"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "No categories that allow new threads are available "
                    "to you at the moment."
                )
            },
        )

    @patch_category_acl({"can_close_threads": False, "can_start_threads": True})
    def test_category_closed_disallowing_new_threads(self):
        """endpoint omits closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "No categories that allow new threads are available "
                    "to you at the moment."
                )
            },
        )

    @patch_category_acl({"can_close_threads": True, "can_start_threads": True})
    def test_category_closed_allowing_new_threads(self):
        """endpoint adds closed category that allows new threads"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0],
            {
                "id": self.category.pk,
                "name": self.category.name,
                "level": 0,
                "post": {"close": True, "hide": False, "pin": 0},
            },
        )

    @patch_category_acl({"can_start_threads": True})
    def test_category_allowing_new_threads(self):
        """endpoint adds category that allows new threads"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0],
            {
                "id": self.category.pk,
                "name": self.category.name,
                "level": 0,
                "post": {"close": False, "hide": False, "pin": 0},
            },
        )

    @patch_category_acl({"can_close_threads": True, "can_start_threads": True})
    def test_category_allowing_closing_threads(self):
        """endpoint adds category that allows new closed threads"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0],
            {
                "id": self.category.pk,
                "name": self.category.name,
                "level": 0,
                "post": {"close": True, "hide": False, "pin": 0},
            },
        )

    @patch_category_acl({"can_start_threads": True, "can_pin_threads": 1})
    def test_category_allowing_locally_pinned_threads(self):
        """endpoint adds category that allows locally pinned threads"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0],
            {
                "id": self.category.pk,
                "name": self.category.name,
                "level": 0,
                "post": {"close": False, "hide": False, "pin": 1},
            },
        )

    @patch_category_acl({"can_start_threads": True, "can_pin_threads": 2})
    def test_category_allowing_globally_pinned_threads(self):
        """endpoint adds category that allows globally pinned threads"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0],
            {
                "id": self.category.pk,
                "name": self.category.name,
                "level": 0,
                "post": {"close": False, "hide": False, "pin": 2},
            },
        )

    @patch_category_acl({"can_start_threads": True, "can_hide_threads": 1})
    def test_category_allowing_hidding_threads(self):
        """endpoint adds category that allows hiding threads"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0],
            {
                "id": self.category.pk,
                "name": self.category.name,
                "level": 0,
                "post": {"close": 0, "hide": 1, "pin": 0},
            },
        )

    @patch_category_acl({"can_start_threads": True, "can_hide_threads": 2})
    def test_category_allowing_hidding_and_deleting_threads(self):
        """endpoint adds category that allows hiding and deleting threads"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0],
            {
                "id": self.category.pk,
                "name": self.category.name,
                "level": 0,
                "post": {"close": False, "hide": 1, "pin": 0},
            },
        )


class ThreadReplyEditorApiTests(EditorApiTestCase):
    def setUp(self):
        super().setUp()

        self.thread = test.post_thread(category=self.category)
        self.api_link = reverse(
            "misago:api:thread-post-editor", kwargs={"thread_pk": self.thread.pk}
        )

    def test_anonymous_user_request(self):
        """endpoint validates if user is authenticated"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You have to sign in to reply threads."}
        )

    def test_thread_visibility(self):
        """thread's visibility is validated"""
        with patch_category_acl({"can_see": False}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 404)

        with patch_category_acl({"can_browse": False}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 404)

        with patch_category_acl({"can_see_all_threads": False}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 404)

    @patch_category_acl({"can_reply_threads": False})
    def test_no_reply_permission(self):
        """permssion to reply is validated"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't reply to threads in this category."}
        )

    def test_closed_category(self):
        """permssion to reply in closed category is validated"""
        self.category.is_closed = True
        self.category.save()

        with patch_category_acl(
            {"can_reply_threads": True, "can_close_threads": False}
        ):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json(),
                {
                    "detail": (
                        "This category is closed. You can't reply to threads in it."
                    )
                },
            )

        # allow to post in closed category
        with patch_category_acl({"can_reply_threads": True, "can_close_threads": True}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 200)

    def test_closed_thread(self):
        """permssion to reply in closed thread is validated"""
        self.thread.is_closed = True
        self.thread.save()

        with patch_category_acl(
            {"can_reply_threads": True, "can_close_threads": False}
        ):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json(),
                {"detail": "You can't reply to closed threads in this category."},
            )

        # allow to post in closed thread
        with patch_category_acl({"can_reply_threads": True, "can_close_threads": True}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_reply_threads": True})
    def test_allow_reply_thread(self):
        """api returns 200 code if thread reply is allowed"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_reply_to_visibility(self):
        """api validates replied post visibility"""

        # unapproved reply can't be replied to
        unapproved_reply = test.reply_thread(self.thread, is_unapproved=True)

        with patch_category_acl({"can_reply_threads": True}):
            response = self.client.get(
                "%s?reply=%s" % (self.api_link, unapproved_reply.pk)
            )
            self.assertEqual(response.status_code, 404)

        # hidden reply can't be replied to
        hidden_reply = test.reply_thread(self.thread, is_hidden=True)

        with patch_category_acl({"can_reply_threads": True}):
            response = self.client.get("%s?reply=%s" % (self.api_link, hidden_reply.pk))
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json(), {"detail": "You can't reply to hidden posts."}
            )

    def test_reply_to_other_thread_post(self):
        """api validates is replied post belongs to same thread"""
        other_thread = test.post_thread(category=self.category)
        reply_to = test.reply_thread(other_thread)

        response = self.client.get("%s?reply=%s" % (self.api_link, reply_to.pk))
        self.assertEqual(response.status_code, 404)

    @patch_category_acl({"can_reply_threads": True})
    def test_reply_to_event(self):
        """events can't be replied to"""
        reply_to = test.reply_thread(self.thread, is_event=True)

        response = self.client.get("%s?reply=%s" % (self.api_link, reply_to.pk))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't reply to events."})

    @patch_category_acl({"can_reply_threads": True})
    def test_reply_to(self):
        """api includes replied to post details in response"""
        reply_to = test.reply_thread(self.thread)

        response = self.client.get("%s?reply=%s" % (self.api_link, reply_to.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": reply_to.pk,
                "post": reply_to.original,
                "poster": reply_to.poster_name,
            },
        )


class EditReplyEditorApiTests(EditorApiTestCase):
    def setUp(self):
        super().setUp()

        self.thread = test.post_thread(category=self.category)
        self.post = test.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            "misago:api:thread-post-editor",
            kwargs={"thread_pk": self.thread.pk, "pk": self.post.pk},
        )

    def test_anonymous_user_request(self):
        """endpoint validates if user is authenticated"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You have to sign in to edit posts."}
        )

    def test_thread_visibility(self):
        """thread's visibility is validated"""
        with patch_category_acl({"can_see": False}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 404)

        with patch_category_acl({"can_browse": False}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 404)

        with patch_category_acl({"can_see_all_threads": False}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 404)

    @patch_category_acl({"can_edit_posts": 0})
    def test_no_edit_permission(self):
        """permssion to edit is validated"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't edit posts in this category."}
        )

    def test_closed_category(self):
        """permssion to edit in closed category is validated"""
        self.category.is_closed = True
        self.category.save()

        with patch_category_acl({"can_edit_posts": 1, "can_close_threads": False}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json(),
                {"detail": "This category is closed. You can't edit posts in it."},
            )

        # allow to edit in closed category
        with patch_category_acl({"can_edit_posts": 1, "can_close_threads": True}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 200)

    def test_closed_thread(self):
        """permssion to edit in closed thread is validated"""
        self.thread.is_closed = True
        self.thread.save()

        with patch_category_acl({"can_edit_posts": 1, "can_close_threads": False}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json(),
                {"detail": "This thread is closed. You can't edit posts in it."},
            )

        # allow to edit in closed thread
        with patch_category_acl({"can_edit_posts": 1, "can_close_threads": True}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 200)

    def test_protected_post(self):
        """permssion to edit protected post is validated"""
        self.post.is_protected = True
        self.post.save()

        with patch_category_acl({"can_edit_posts": 1, "can_protect_posts": False}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json(),
                {"detail": "This post is protected. You can't edit it."},
            )

        # allow to post in closed thread
        with patch_category_acl({"can_edit_posts": 1, "can_protect_posts": True}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 200)

    def test_post_visibility(self):
        """edited posts visibility is validated"""
        self.post.is_hidden = True
        self.post.save()

        with patch_category_acl({"can_edit_posts": 1}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json(), {"detail": "This post is hidden, you can't edit it."}
            )

        # allow hidden edition
        with patch_category_acl({"can_edit_posts": 1, "can_hide_posts": 1}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 200)

        # test unapproved post
        self.post.is_unapproved = True
        self.post.is_hidden = False
        self.post.poster = None
        self.post.save()

        with patch_category_acl({"can_edit_posts": 2, "can_approve_content": 0}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 404)

        # allow unapproved edition
        with patch_category_acl({"can_edit_posts": 2, "can_approve_content": 1}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_edit_posts": 2})
    def test_post_is_event(self):
        """events can't be edited"""
        self.post.is_event = True
        self.post.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "Events can't be edited."})

    def test_other_user_post(self):
        """api validates if other user's post can be edited"""
        self.post.poster = None
        self.post.save()

        with patch_category_acl({"can_edit_posts": 1}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json(),
                {"detail": "You can't edit other users posts in this category."},
            )

        # allow other users post edition
        with patch_category_acl({"can_edit_posts": 2}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_hide_threads": 1, "can_edit_posts": 2})
    def test_edit_first_post_hidden(self):
        """
        endpoint returns valid configuration for editor of hidden thread's first post
        """
        self.thread.is_hidden = True
        self.thread.save()
        self.thread.first_post.is_hidden = True
        self.thread.first_post.save()

        api_link = reverse(
            "misago:api:thread-post-editor",
            kwargs={"thread_pk": self.thread.pk, "pk": self.thread.first_post.pk},
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_edit_posts": 1})
    def test_edit(self):
        """endpoint returns valid configuration for editor"""
        with patch_category_acl({"max_attachment_size": 1000}):
            for _ in range(3):
                with open(TEST_DOCUMENT_PATH, "rb") as upload:
                    response = self.client.post(
                        reverse("misago:api:attachment-list"), data={"upload": upload}
                    )
                self.assertEqual(response.status_code, 200)

        attachments = list(Attachment.objects.order_by("id"))

        attachments[0].uploader = None
        attachments[0].save()

        for attachment in attachments[:2]:
            attachment.post = self.post
            attachment.save()

        response = self.client.get(self.api_link)
        user_acl = useracl.get_user_acl(self.user, cache_versions)
        for attachment in attachments:
            add_acl_to_obj(user_acl, attachment)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": self.post.pk,
                "api": self.post.get_api_url(),
                "post": self.post.original,
                "can_protect": False,
                "is_protected": self.post.is_protected,
                "poster": self.post.poster_name,
                "attachments": [
                    AttachmentSerializer(
                        attachments[1], context={"user": self.user}
                    ).data,
                    AttachmentSerializer(
                        attachments[0], context={"user": self.user}
                    ).data,
                ],
            },
        )
