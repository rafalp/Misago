from django.urls import reverse

from .. import test
from ..serializers import PostLikeSerializer
from ..test import patch_category_acl
from .test_threads_api import ThreadsApiTestCase


class ThreadPostLikesApiTestCase(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.post = test.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            "misago:api:thread-post-likes",
            kwargs={"thread_pk": self.thread.pk, "pk": self.post.pk},
        )

    @patch_category_acl({"can_see_posts_likes": 0})
    def test_no_permission(self):
        """api errors if user has no permission to see likes"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't see who liked this post."}
        )

    @patch_category_acl({"can_see_posts_likes": 1})
    def test_no_permission_to_list(self):
        """api errors if user has no permission to see likes, but can see likes count"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't see who liked this post."}
        )

    @patch_category_acl({"can_see_posts_likes": 2})
    def test_no_likes(self):
        """api returns empty list if post has no likes"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch_category_acl({"can_see_posts_likes": 2})
    def test_likes(self):
        """api returns list of likes"""
        like = test.like_post(self.post, self.user)
        other_like = test.like_post(self.post, self.user)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                PostLikeSerializer(
                    {
                        "id": other_like.id,
                        "liked_on": other_like.liked_on,
                        "liker_id": other_like.liker_id,
                        "liker_name": other_like.liker_name,
                        "liker_slug": other_like.liker_slug,
                        "liker__avatars": self.user.avatars,
                    }
                ).data,
                PostLikeSerializer(
                    {
                        "id": like.id,
                        "liked_on": like.liked_on,
                        "liker_id": like.liker_id,
                        "liker_name": like.liker_name,
                        "liker_slug": like.liker_slug,
                        "liker__avatars": self.user.avatars,
                    }
                ).data,
            ],
        )

        # api has no showstoppers for likes by deleted users
        like.liker = None
        like.save()

        other_like.liker = None
        other_like.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                PostLikeSerializer(
                    {
                        "id": other_like.id,
                        "liked_on": other_like.liked_on,
                        "liker_id": other_like.liker_id,
                        "liker_name": other_like.liker_name,
                        "liker_slug": other_like.liker_slug,
                        "liker__avatars": None,
                    }
                ).data,
                PostLikeSerializer(
                    {
                        "id": like.id,
                        "liked_on": like.liked_on,
                        "liker_id": like.liker_id,
                        "liker_name": like.liker_name,
                        "liker_slug": like.liker_slug,
                        "liker__avatars": None,
                    }
                ).data,
            ],
        )
