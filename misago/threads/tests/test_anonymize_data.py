from django.test import RequestFactory
from django.urls import reverse

from .. import test
from ...cache.versions import get_cache_versions
from ...categories.models import Category
from ...conf.dynamicsettings import DynamicSettings
from ...users.test import AuthenticatedUserTestCase, create_test_user
from ..api.postendpoints.patch_post import patch_is_liked
from ..models import Post
from ..participants import (
    add_participant,
    change_owner,
    make_participants_aware,
    remove_participant,
    set_owner,
)


class AnonymizeEventsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

        category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category)

    def get_request(self, user=None):
        request = self.factory.get("/customer/details")
        request.user = user or self.user
        request.user_ip = "127.0.0.1"
        request.cache_versions = get_cache_versions()
        request.settings = DynamicSettings(request.cache_versions)
        request.include_frontend_context = False
        request.frontend_context = {}

        return request

    def test_anonymize_changed_owner_event(self):
        """changed owner event is anonymized by user.anonymize_data"""
        user = create_test_user("OtherUser", "otheruser@example.com")
        request = self.get_request()

        set_owner(self.thread, self.user)
        make_participants_aware(self.user, self.thread)
        change_owner(request, self.thread, user)

        user.anonymize_data(anonymous_username="Deleted")

        event = Post.objects.get(event_type="changed_owner")
        self.assertEqual(
            event.event_context,
            {
                "user": {
                    "id": None,
                    "username": user.username,
                    "url": reverse("misago:index"),
                }
            },
        )

    def test_anonymize_added_participant_event(self):
        """added participant event is anonymized by user.anonymize_data"""
        user = create_test_user("OtherUser", "otheruser@example.com")
        request = self.get_request()

        set_owner(self.thread, self.user)
        make_participants_aware(self.user, self.thread)
        add_participant(request, self.thread, user)

        user.anonymize_data(anonymous_username="Deleted")

        event = Post.objects.get(event_type="added_participant")
        self.assertEqual(
            event.event_context,
            {
                "user": {
                    "id": None,
                    "username": user.username,
                    "url": reverse("misago:index"),
                }
            },
        )

    def test_anonymize_owner_left_event(self):
        """owner left event is anonymized by user.anonymize_data"""
        user = create_test_user("OtherUser", "otheruser@example.com")
        request = self.get_request(user)

        set_owner(self.thread, user)
        make_participants_aware(user, self.thread)
        add_participant(request, self.thread, self.user)

        make_participants_aware(user, self.thread)
        remove_participant(request, self.thread, user)

        user.anonymize_data(anonymous_username="Deleted")

        event = Post.objects.get(event_type="owner_left")
        self.assertEqual(
            event.event_context,
            {
                "user": {
                    "id": None,
                    "username": user.username,
                    "url": reverse("misago:index"),
                }
            },
        )

    def test_anonymize_removed_owner_event(self):
        """removed owner event is anonymized by user.anonymize_data"""
        user = create_test_user("OtherUser", "otheruser@example.com")
        request = self.get_request()

        set_owner(self.thread, user)
        make_participants_aware(user, self.thread)
        add_participant(request, self.thread, self.user)

        make_participants_aware(user, self.thread)
        remove_participant(request, self.thread, user)

        user.anonymize_data(anonymous_username="Deleted")

        event = Post.objects.get(event_type="removed_owner")
        self.assertEqual(
            event.event_context,
            {
                "user": {
                    "id": None,
                    "username": user.username,
                    "url": reverse("misago:index"),
                }
            },
        )

    def test_anonymize_participant_left_event(self):
        """participant left event is anonymized by user.anonymize_data"""
        user = create_test_user("OtherUser", "otheruser@example.com")
        request = self.get_request(user)

        set_owner(self.thread, self.user)
        make_participants_aware(user, self.thread)
        add_participant(request, self.thread, user)

        make_participants_aware(user, self.thread)
        remove_participant(request, self.thread, user)

        user.anonymize_data(anonymous_username="Deleted")

        event = Post.objects.get(event_type="participant_left")
        self.assertEqual(
            event.event_context,
            {
                "user": {
                    "id": None,
                    "username": user.username,
                    "url": reverse("misago:index"),
                }
            },
        )

    def test_anonymize_removed_participant_event(self):
        """removed participant event is anonymized by user.anonymize_data"""
        user = create_test_user("OtherUser", "otheruser@example.com")
        request = self.get_request()

        set_owner(self.thread, self.user)
        make_participants_aware(self.user, self.thread)
        add_participant(request, self.thread, user)

        make_participants_aware(self.user, self.thread)
        remove_participant(request, self.thread, user)

        user.anonymize_data(anonymous_username="Deleted")

        event = Post.objects.get(event_type="removed_participant")
        self.assertEqual(
            event.event_context,
            {
                "user": {
                    "id": None,
                    "username": user.username,
                    "url": reverse("misago:index"),
                }
            },
        )


class AnonymizeLikesTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def get_request(self, user=None):
        request = self.factory.get("/customer/details")
        request.user = user or self.user
        request.user_ip = "127.0.0.1"

        return request

    def test_anonymize_user_likes(self):
        """post's last like is anonymized by user.anonymize_data"""
        category = Category.objects.get(slug="first-category")
        thread = test.post_thread(category)
        post = test.reply_thread(thread)
        post.acl = {"can_like": True}

        user = create_test_user("OtherUser", "otheruser@example.com")

        patch_is_liked(self.get_request(self.user), post, 1)
        patch_is_liked(self.get_request(user), post, 1)

        user.anonymize_data(anonymous_username="Deleted")

        last_likes = Post.objects.get(pk=post.pk).last_likes
        self.assertEqual(
            last_likes,
            [
                {"id": None, "username": user.username},
                {"id": self.user.id, "username": self.user.username},
            ],
        )


class AnonymizePostsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def get_request(self, user=None):
        request = self.factory.get("/customer/details")
        request.user = user or self.user
        request.user_ip = "127.0.0.1"

        return request

    def test_anonymize_user_posts(self):
        """post is anonymized by user.anonymize_data"""
        category = Category.objects.get(slug="first-category")
        thread = test.post_thread(category)

        user = create_test_user("OtherUser", "otheruser@example.com")
        post = test.reply_thread(thread, poster=user)
        user.anonymize_data(anonymous_username="Deleted")

        anonymized_post = Post.objects.get(pk=post.pk)
        self.assertTrue(anonymized_post.is_valid)
