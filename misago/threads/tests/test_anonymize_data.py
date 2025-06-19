from django.test import RequestFactory

from .. import test
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase, create_test_user
from ..api.postendpoints.patch_post import patch_is_liked
from ..models import Post


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

        user = create_test_user("Other_User", "otheruser@example.com")

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

        user = create_test_user("Other_User", "otheruser@example.com")
        post = test.reply_thread(thread, poster=user)
        user.anonymize_data(anonymous_username="Deleted")

        anonymized_post = Post.objects.get(pk=post.pk)
        self.assertTrue(anonymized_post.is_valid)
