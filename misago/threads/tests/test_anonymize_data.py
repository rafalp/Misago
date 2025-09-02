from django.test import RequestFactory

from .. import test
from ...categories.models import Category
from ...posts.models import Post
from ...users.test import AuthenticatedUserTestCase, create_test_user
from ..models import Post


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
