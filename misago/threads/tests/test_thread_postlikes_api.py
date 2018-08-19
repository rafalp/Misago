from django.urls import reverse

from misago.threads import testutils
from misago.threads.serializers import PostLikeSerializer

from .test_threads_api import ThreadsApiTestCase


class ThreadPostLikesApiTestCase(ThreadsApiTestCase):
    def setUp(self):
        super(ThreadPostLikesApiTestCase, self).setUp()

        self.post = testutils.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            'misago:api:thread-post-likes',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.post.pk,
            }
        )

    def test_no_permission(self):
        """api errors if user has no permission to see likes"""
        self.override_acl({'can_see_posts_likes': 0})

        response = self.client.get(self.api_link)
        self.assertContains(response, "You can't see who liked this post.", status_code=403)

    def test_no_permission_to_list(self):
        """api errors if user has no permission to see likes, but can see likes count"""
        self.override_acl({'can_see_posts_likes': 1})

        response = self.client.get(self.api_link)
        self.assertContains(response, "You can't see who liked this post.", status_code=403)

    def test_no_likes(self):
        """api returns empty list if post has no likes"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_likes(self):
        """api returns list of likes"""
        like = testutils.like_post(self.post, self.user)
        other_like = testutils.like_post(self.post, self.user)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), [
                PostLikeSerializer({
                    'id': other_like.id,
                    'liked_on': other_like.liked_on,
                    'liker_id': other_like.liker_id,
                    'liker_name': other_like.liker_name,
                    'liker_slug': other_like.liker_slug,
                    'liker__avatars': self.user.avatars,
                }).data,
                PostLikeSerializer({
                    'id': like.id,
                    'liked_on': like.liked_on,
                    'liker_id': like.liker_id,
                    'liker_name': like.liker_name,
                    'liker_slug': like.liker_slug,
                    'liker__avatars': self.user.avatars,
                }).data,
            ]
        )

        # api has no showstoppers for likes by deleted users
        like.liker = None
        like.save()

        other_like.liker = None
        other_like.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), [
                PostLikeSerializer({
                    'id': other_like.id,
                    'liked_on': other_like.liked_on,
                    'liker_id': other_like.liker_id,
                    'liker_name': other_like.liker_name,
                    'liker_slug': other_like.liker_slug,
                    'liker__avatars': None,
                }).data,
                PostLikeSerializer({
                    'id': like.id,
                    'liked_on': like.liked_on,
                    'liker_id': like.liker_id,
                    'liker_name': like.liker_name,
                    'liker_slug': like.liker_slug,
                    'liker__avatars': None,
                }).data,
            ]
        )
