from django.urls import reverse

from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase
from ..test import patch_category_acl


class StartThreadTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.api_link = reverse("misago:api:thread-list")

    def test_cant_start_thread_as_guest(self):
        """user has to be authenticated to be able to post thread"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)

    @patch_category_acl({"can_see": False})
    def test_cant_see(self):
        """has no permission to see selected category"""
        response = self.client.post(self.api_link, {"category": self.category.pk})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "category": ["Selected category is invalid."],
                "post": ["You have to enter a message."],
                "title": ["You have to enter thread title."],
            },
        )

    @patch_category_acl({"can_browse": False})
    def test_cant_browse(self):
        """has no permission to browse selected category"""
        response = self.client.post(self.api_link, {"category": self.category.pk})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "category": ["Selected category is invalid."],
                "post": ["You have to enter a message."],
                "title": ["You have to enter thread title."],
            },
        )

    @patch_category_acl({"can_start_threads": False})
    def test_cant_start_thread(self):
        """permission to start thread in category is validated"""
        response = self.client.post(self.api_link, {"category": self.category.pk})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "category": [
                    "You don't have permission to start new threads in this category."
                ],
                "post": ["You have to enter a message."],
                "title": ["You have to enter thread title."],
            },
        )

    @patch_category_acl({"can_start_threads": True, "can_close_threads": False})
    def test_cant_start_thread_in_locked_category(self):
        """can't post in closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.post(self.api_link, {"category": self.category.pk})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "category": [
                    "This category is closed. You can't start new threads in it."
                ],
                "post": ["You have to enter a message."],
                "title": ["You have to enter thread title."],
            },
        )

    def test_cant_start_thread_in_invalid_category(self):
        """can't post in invalid category"""
        response = self.client.post(
            self.api_link, {"category": self.category.pk * 100000}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "category": [
                    "Selected category doesn't exist or "
                    "you don't have permission to browse it."
                ],
                "post": ["You have to enter a message."],
                "title": ["You have to enter thread title."],
            },
        )

    @patch_category_acl({"can_start_threads": True})
    def test_empty_data(self):
        """no data sent handling has no showstoppers"""
        response = self.client.post(self.api_link, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "category": ["You have to select category to post thread in."],
                "title": ["You have to enter thread title."],
                "post": ["You have to enter a message."],
            },
        )

    @patch_category_acl({"can_start_threads": True})
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

    @patch_category_acl({"can_start_threads": True})
    def test_title_is_validated(self):
        """title is validated"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "------",
                "post": "Lorem ipsum dolor met, sit amet elit!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"title": ["Thread title should contain alpha-numeric characters."]},
        )

    @patch_category_acl({"can_start_threads": True})
    def test_post_is_validated(self):
        """post is validated"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Lorem ipsum dolor met",
                "post": "a",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "post": [
                    "Posted message should be at least 5 characters long (it has 1)."
                ]
            },
        )

    @patch_category_acl({"can_start_threads": True})
    def test_can_start_thread(self):
        """endpoint creates new thread"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]

        response_json = response.json()
        self.assertEqual(response_json["url"], thread.get_absolute_url())

        response = self.client.get(thread.get_absolute_url())
        self.assertContains(response, self.category.name)
        self.assertContains(response, thread.title)
        self.assertContains(response, "<p>Lorem ipsum dolor met!</p>")

        # api increased user's threads and posts counts
        self.reload_user()
        self.assertEqual(self.user.threads, 1)
        self.assertEqual(self.user.posts, 1)

        self.assertEqual(self.user.audittrail_set.count(), 1)

        self.assertEqual(thread.category_id, self.category.pk)
        self.assertEqual(thread.title, "Hello, I am test thread!")
        self.assertEqual(thread.starter_id, self.user.id)
        self.assertEqual(thread.starter_name, self.user.username)
        self.assertEqual(thread.starter_slug, self.user.slug)
        self.assertEqual(thread.last_poster_id, self.user.id)
        self.assertEqual(thread.last_poster_name, self.user.username)
        self.assertEqual(thread.last_poster_slug, self.user.slug)

        post = self.user.post_set.all()[:1][0]
        self.assertEqual(post.category_id, self.category.pk)
        self.assertEqual(post.original, "Lorem ipsum dolor met!")
        self.assertEqual(post.poster_id, self.user.id)
        self.assertEqual(post.poster_name, self.user.username)

        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(category.threads, 1)
        self.assertEqual(category.posts, 1)
        self.assertEqual(category.last_thread_id, thread.id)
        self.assertEqual(category.last_thread_title, thread.title)
        self.assertEqual(category.last_thread_slug, thread.slug)

        self.assertEqual(category.last_poster_id, self.user.id)
        self.assertEqual(category.last_poster_name, self.user.username)
        self.assertEqual(category.last_poster_slug, self.user.slug)

    @patch_category_acl({"can_start_threads": True, "can_close_threads": False})
    def test_start_closed_thread_no_permission(self):
        """permission is checked before thread is closed"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
                "close": True,
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_closed)

    @patch_category_acl({"can_start_threads": True, "can_close_threads": True})
    def test_start_closed_thread(self):
        """can post closed thread"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
                "close": True,
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertTrue(thread.is_closed)

    @patch_category_acl({"can_start_threads": True, "can_pin_threads": 1})
    def test_start_unpinned_thread(self):
        """can post unpinned thread"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
                "pin": 0,
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 0)

    @patch_category_acl({"can_start_threads": True, "can_pin_threads": 1})
    def test_start_locally_pinned_thread(self):
        """can post locally pinned thread"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
                "pin": 1,
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 1)

    @patch_category_acl({"can_start_threads": True, "can_pin_threads": 2})
    def test_start_globally_pinned_thread(self):
        """can post globally pinned thread"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
                "pin": 2,
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 2)

    @patch_category_acl({"can_start_threads": True, "can_pin_threads": 1})
    def test_start_globally_pinned_thread_no_permission(self):
        """cant post globally pinned thread without permission"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
                "pin": 2,
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 0)

    @patch_category_acl({"can_start_threads": True, "can_pin_threads": 0})
    def test_start_locally_pinned_thread_no_permission(self):
        """cant post locally pinned thread without permission"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
                "pin": 1,
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 0)

    @patch_category_acl({"can_start_threads": True, "can_hide_threads": 1})
    def test_start_hidden_thread(self):
        """can post hidden thread"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
                "hide": 1,
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertTrue(thread.is_hidden)

        category = Category.objects.get(pk=self.category.pk)
        self.assertNotEqual(category.last_thread_id, thread.id)

    @patch_category_acl({"can_start_threads": True, "can_hide_threads": 0})
    def test_start_hidden_thread_no_permission(self):
        """cant post hidden thread without permission"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
                "hide": 1,
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_hidden)

    @patch_category_acl({"can_start_threads": True})
    def test_post_unicode(self):
        """unicode characters can be posted"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Brzęczyżczykiewicz",
                "post": "Chrzążczyżewoszyce, powiat Łękółody.",
            },
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_start_threads": True})
    def test_category_moderation_queue(self):
        """start unapproved thread in category that requires approval"""
        self.category.require_threads_approval = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertTrue(thread.is_unapproved)
        self.assertTrue(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertTrue(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads)
        self.assertEqual(category.posts, self.category.posts)
        self.assertFalse(category.last_thread_id == thread.id)

    @patch_category_acl({"can_start_threads": True})
    @patch_user_acl({"can_approve_content": True})
    def test_category_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        self.category.require_threads_approval = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads + 1)
        self.assertEqual(category.posts, self.category.posts + 1)
        self.assertEqual(category.last_thread_id, thread.id)

    @patch_category_acl({"can_start_threads": True, "require_threads_approval": True})
    def test_user_moderation_queue(self):
        """start unapproved thread in category that requires approval"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertTrue(thread.is_unapproved)
        self.assertTrue(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertTrue(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads)
        self.assertEqual(category.posts, self.category.posts)
        self.assertFalse(category.last_thread_id == thread.id)

    @patch_category_acl({"can_start_threads": True, "require_threads_approval": True})
    @patch_user_acl({"can_approve_content": True})
    def test_user_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads + 1)
        self.assertEqual(category.posts, self.category.posts + 1)
        self.assertEqual(category.last_thread_id, thread.id)

    @patch_category_acl(
        {
            "can_start_threads": True,
            "require_replies_approval": True,
            "require_edits_approval": True,
        }
    )
    def test_omit_other_moderation_queues(self):
        """other queues are omitted"""
        self.category.require_replies_approval = True
        self.category.require_edits_approval = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Hello, I am test thread!",
                "post": "Lorem ipsum dolor met!",
            },
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.threads, self.category.threads + 1)
        self.assertEqual(category.posts, self.category.posts + 1)
        self.assertEqual(category.last_thread_id, thread.id)
