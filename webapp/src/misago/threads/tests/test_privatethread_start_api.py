from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from django.utils.encoding import smart_str

from ...acl.test import patch_user_acl
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...users.test import AuthenticatedUserTestCase, create_test_user
from ..models import ThreadParticipant
from ..test import other_user_cant_use_private_threads

User = get_user_model()


class StartPrivateThreadTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.private_threads()
        self.api_link = reverse("misago:api:private-thread-list")

        self.other_user = create_test_user("OtherUser", "otheruser@example.com")

    def test_cant_start_thread_as_guest(self):
        """user has to be authenticated to be able to post private thread"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)

    @patch_user_acl({"can_use_private_threads": False})
    def test_cant_use_private_threads(self):
        """has no permission to use private threads"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't use private threads."})

    @patch_user_acl({"can_start_private_threads": False})
    def test_cant_start_private_thread(self):
        """permission to start private thread is validated"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't start private threads."}
        )

    def test_empty_data(self):
        """no data sent handling has no showstoppers"""
        response = self.client.post(self.api_link, data={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "to": ["This field is required."],
                "title": ["You have to enter thread title."],
                "post": ["You have to enter a message."],
            },
        )

    def test_title_is_validated(self):
        """title is validated"""
        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
                "title": "------",
                "post": "Lorem ipsum dolor met, sit amet elit!",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"title": ["Thread title should contain alpha-numeric characters."]},
        )

    def test_post_is_validated(self):
        """post is validated"""
        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
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

    def test_cant_invite_self(self):
        """api validates that you cant invite yourself to private thread"""
        response = self.client.post(
            self.api_link,
            data={
                "to": [self.user.username],
                "title": "Lorem ipsum dolor met",
                "post": "Lorem ipsum dolor.",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "to": [
                    "You can't include yourself on the list "
                    "of users to invite to new thread."
                ]
            },
        )

    def test_cant_invite_nonexisting(self):
        """api validates that you cant invite nonexisting user to thread"""
        response = self.client.post(
            self.api_link,
            data={
                "to": ["Ab", "Cd"],
                "title": "Lorem ipsum dolor met",
                "post": "Lorem ipsum dolor.",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"to": ["One or more users could not be found: ab, cd"]}
        )

    def test_cant_invite_too_many(self):
        """api validates that you cant invite too many users to thread"""
        response = self.client.post(
            self.api_link,
            data={
                "to": ["Username%s" % i for i in range(50)],
                "title": "Lorem ipsum dolor met",
                "post": "Lorem ipsum dolor.",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "to": [
                    "You can't add more than 3 users to private thread "
                    "(you've added 50)."
                ]
            },
        )

    @patch_user_acl(other_user_cant_use_private_threads)
    def test_cant_invite_no_permission(self):
        """api validates invited user permission to private thread"""
        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
                "title": "Lorem ipsum dolor met",
                "post": "Lorem ipsum dolor.",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"to": ["OtherUser can't participate in private threads."]}
        )

    def test_cant_invite_blocking(self):
        """api validates that you cant invite blocking user to thread"""
        self.other_user.blocks.add(self.user)

        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
                "title": "Lorem ipsum dolor met",
                "post": "Lorem ipsum dolor.",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"to": ["OtherUser is blocking you."]})

    @patch_user_acl({"can_add_everyone_to_private_threads": 1})
    def test_cant_invite_blocking_override(self):
        """api validates that you cant invite blocking user to thread"""
        self.other_user.blocks.add(self.user)

        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
                "title": "-----",
                "post": "Lorem ipsum dolor.",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"title": ["Thread title should contain alpha-numeric characters."]},
        )

    def test_cant_invite_followers_only(self):
        """api validates that you cant invite followers-only user to thread"""
        user_constant = User.LIMIT_INVITES_TO_FOLLOWED
        self.other_user.limits_private_thread_invites_to = user_constant
        self.other_user.save()

        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
                "title": "Lorem ipsum dolor met",
                "post": "Lorem ipsum dolor.",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "to": [
                    "OtherUser limits invitations to private threads to followed users."
                ]
            },
        )

        # allow us to bypass following check
        with patch_user_acl({"can_add_everyone_to_private_threads": 1}):
            response = self.client.post(
                self.api_link,
                data={
                    "to": [self.other_user.username],
                    "title": "-----",
                    "post": "Lorem ipsum dolor.",
                },
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(),
                {"title": ["Thread title should contain alpha-numeric characters."]},
            )

        # make user follow us
        self.other_user.follows.add(self.user)

        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
                "title": "-----",
                "post": "Lorem ipsum dolor.",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"title": ["Thread title should contain alpha-numeric characters."]},
        )

    def test_cant_invite_anyone(self):
        """api validates that you cant invite nobody user to thread"""
        user_constant = User.LIMIT_INVITES_TO_NOBODY
        self.other_user.limits_private_thread_invites_to = user_constant
        self.other_user.save()

        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
                "title": "Lorem ipsum dolor met",
                "post": "Lorem ipsum dolor.",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"to": ["OtherUser is not allowing invitations to private threads."]},
        )

        # allow us to bypass user preference check
        with patch_user_acl({"can_add_everyone_to_private_threads": 1}):
            response = self.client.post(
                self.api_link,
                data={
                    "to": [self.other_user.username],
                    "title": "-----",
                    "post": "Lorem ipsum dolor.",
                },
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json(),
                {"title": ["Thread title should contain alpha-numeric characters."]},
            )

    @override_dynamic_settings(forum_address="http://test.com/")
    def test_can_start_thread(self):
        """endpoint creates new thread"""
        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
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

        # don't count private threads
        self.reload_user()
        self.assertEqual(self.user.threads, 0)
        self.assertEqual(self.user.posts, 0)

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

        self.assertEqual(self.user.audittrail_set.count(), 1)

        # thread has two participants
        self.assertEqual(thread.participants.count(), 2)

        # we are thread owner
        ThreadParticipant.objects.get(thread=thread, user=self.user, is_owner=True)

        # other user was added to thread
        ThreadParticipant.objects.get(
            thread=thread, user=self.other_user, is_owner=False
        )

        # other user has sync_unread_private_threads flag
        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        # notification about new private thread was sent to other user
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[-1]

        self.assertIn(self.user.username, email.subject)
        self.assertIn(thread.title, email.subject)

        email_body = smart_str(email.body)

        self.assertIn(self.user.username, email_body)
        self.assertIn(thread.title, email_body)
        self.assertIn(thread.get_absolute_url(), email_body)

    def test_post_unicode(self):
        """unicode characters can be posted"""
        response = self.client.post(
            self.api_link,
            data={
                "to": [self.other_user.username],
                "title": "Brzęczyżczykiewicz",
                "post": "Chrzążczyżewoszyce, powiat Łękółody.",
            },
        )
        self.assertEqual(response.status_code, 200)
