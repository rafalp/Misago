from django.urls import reverse

from .. import test
from ..test import patch_category_acl
from .test_threads_api import ThreadsApiTestCase


class ThreadPostEditsApiTestCase(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.post = test.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            "misago:api:thread-post-edits",
            kwargs={"thread_pk": self.thread.pk, "pk": self.post.pk},
        )

    def mock_edit_record(self):
        edits_record = [
            self.post.edits_record.create(
                category=self.category,
                thread=self.thread,
                editor=self.user,
                editor_name=self.user.username,
                editor_slug=self.user.slug,
                edited_from="Original body",
                edited_to="First Edit",
            ),
            self.post.edits_record.create(
                category=self.category,
                thread=self.thread,
                editor_name="Deleted",
                editor_slug="deleted",
                edited_from="First Edit",
                edited_to="Second Edit",
            ),
            self.post.edits_record.create(
                category=self.category,
                thread=self.thread,
                editor=self.user,
                editor_name=self.user.username,
                editor_slug=self.user.slug,
                edited_from="Second Edit",
                edited_to="Last Edit",
            ),
        ]

        self.post.original = "Last Edit"
        self.post.parsed = "<p>Last Edit</p>"
        self.post.save()

        return edits_record


class ThreadPostGetEditTests(ThreadPostEditsApiTestCase):
    def test_no_edits(self):
        """api returns 403 if post has no edits record"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "Edits record is unavailable for this post."}
        )

        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "Edits record is unavailable for this post."}
        )

    def test_empty_edit_id(self):
        """api handles empty edit in querystring"""
        response = self.client.get("%s?edit=" % self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_invalid_edit_id(self):
        """api handles invalid edit in querystring"""
        response = self.client.get("%s?edit=dsa67d8sa68" % self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_edit_id(self):
        """api handles nonexistant edit in querystring"""
        response = self.client.get("%s?edit=1321" % self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_get_last_edit(self):
        """api returns last edit record"""
        edits = self.mock_edit_record()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertEqual(response_json["id"], edits[-1].id)
        self.assertIsNone(response_json["next"])
        self.assertEqual(response_json["previous"], edits[1].id)

    def test_get_middle_edit(self):
        """api returns middle edit record"""
        edits = self.mock_edit_record()

        response = self.client.get("%s?edit=%s" % (self.api_link, edits[1].id))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertEqual(response_json["id"], edits[1].id)
        self.assertEqual(response_json["next"], edits[-1].id)
        self.assertEqual(response_json["previous"], edits[0].id)

    def test_get_first_edit(self):
        """api returns middle edit record"""
        edits = self.mock_edit_record()

        response = self.client.get("%s?edit=%s" % (self.api_link, edits[0].id))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertEqual(response_json["id"], edits[0].id)
        self.assertEqual(response_json["next"], edits[1].id)
        self.assertIsNone(response_json["previous"])


class ThreadPostPostEditTests(ThreadPostEditsApiTestCase):
    def setUp(self):
        super().setUp()
        self.edits = self.mock_edit_record()

    @patch_category_acl({"can_edit_posts": 2})
    def test_empty_edit_id(self):
        """api handles empty edit in querystring"""
        response = self.client.post("%s?edit=" % self.api_link)
        self.assertEqual(response.status_code, 404)

    @patch_category_acl({"can_edit_posts": 2})
    def test_invalid_edit_id(self):
        """api handles invalid edit in querystring"""
        response = self.client.post("%s?edit=dsa67d8sa68" % self.api_link)
        self.assertEqual(response.status_code, 404)

    @patch_category_acl({"can_edit_posts": 2})
    def test_nonexistant_edit_id(self):
        """api handles nonexistant edit in querystring"""
        response = self.client.post("%s?edit=1321" % self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_anonymous(self):
        """only signed in users can rever ports"""
        self.logout_user()

        response = self.client.post("%s?edit=%s" % (self.api_link, self.edits[0].id))
        self.assertEqual(response.status_code, 403)

    @patch_category_acl({"can_edit_posts": 0})
    def test_no_permission(self):
        """api validates permission to revert post"""
        response = self.client.post("%s?edit=1321" % self.api_link)
        self.assertEqual(response.status_code, 403)

    @patch_category_acl({"can_edit_posts": 2})
    def test_revert_post(self):
        """api reverts post to version from before specified edit"""
        response = self.client.post("%s?edit=%s" % (self.api_link, self.edits[0].id))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["edits"], 1)
        self.assertEqual(response_json["content"], "<p>Original body</p>")

        self.assertEqual(self.post.edits_record.count(), 4)

        edit = self.post.edits_record.first()
        self.assertEqual(edit.edited_from, self.post.original)
        self.assertEqual(edit.edited_to, "Original body")
