from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse

from .. import test
from ...categories.models import Category
from ...markup.mentions import MENTIONS_LIMIT
from ...users.test import AuthenticatedUserTestCase, create_test_user


class PostMentionsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category=self.category)

        self.post_link = reverse(
            "misago:api:thread-post-list", kwargs={"thread_pk": self.thread.pk}
        )

    def put(self, url, data=None):
        content = encode_multipart(BOUNDARY, data or {})
        return self.client.put(url, content, content_type=MULTIPART_CONTENT)

    def test_mention_noone(self):
        """endpoint handles no mentions in post"""
        response = self.client.post(
            self.post_link, data={"post": "This is test response!"}
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by("id").last()
        self.assertEqual(post.mentions.count(), 0)

    def test_mention_nonexistant(self):
        """endpoint handles nonexistant mention"""
        response = self.client.post(
            self.post_link, data={"post": "This is test response, @InvalidUser!"}
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by("id").last()
        self.assertEqual(post.mentions.count(), 0)

    def test_mention_self(self):
        """endpoint mentions author"""
        response = self.client.post(
            self.post_link, data={"post": "This is test response, @%s!" % self.user}
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by("id").last()

        self.assertEqual(post.mentions.count(), 1)
        self.assertEqual(post.mentions.all()[0], self.user)

    def test_mention_limit(self):
        """endpoint mentions limits mentions to 24 users"""
        users = []

        for i in range(MENTIONS_LIMIT + 5):
            users.append(create_test_user("User%s" % i, "user%s@example.com" % i))

        mentions = ["@%s" % u for u in users]
        response = self.client.post(
            self.post_link,
            data={"post": "This is test response, %s!" % (", ".join(mentions))},
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by("id").last()

        self.assertEqual(post.mentions.count(), 24)
        self.assertEqual(list(post.mentions.order_by("id")), users[:24])

    def test_mention_update(self):
        """edit post endpoint updates mentions"""
        user = create_test_user("User", "user@example.com")
        other_user = create_test_user("OtherUser", "otheruser@example.com")

        response = self.client.post(
            self.post_link, data={"post": "This is test response, @%s!" % user}
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by("id").last()

        self.assertEqual(post.mentions.count(), 1)
        self.assertEqual(post.mentions.order_by("id")[0], user)

        # add mention to post
        edit_link = reverse(
            "misago:api:thread-post-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": post.pk},
        )

        response = self.put(
            edit_link,
            data={"post": "This is test response, @%s and @%s!" % (user, other_user)},
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(post.mentions.count(), 2)
        self.assertEqual(list(post.mentions.order_by("id")), [user, other_user])

        # remove first mention from post - should preserve mentions
        response = self.put(
            edit_link, data={"post": "This is test response, @%s!" % other_user}
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(post.mentions.count(), 2)
        self.assertEqual(list(post.mentions.order_by("id")), [user, other_user])

        # remove mentions from post - should preserve mentions
        response = self.put(edit_link, data={"post": "This is test response!"})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(post.mentions.count(), 2)
        self.assertEqual(list(post.mentions.order_by("id")), [user, other_user])

    def test_mentions_merge(self):
        """posts merge sums mentions"""
        user = create_test_user("User1", "user1@example.com")
        other_user = create_test_user("User2", "user2@example.com")

        response = self.client.post(
            self.post_link, data={"post": "This is test response, @%s!" % user}
        )
        self.assertEqual(response.status_code, 200)

        post_a = self.user.post_set.order_by("id").last()

        self.assertEqual(post_a.mentions.count(), 1)
        self.assertEqual(list(post_a.mentions.all()), [user])

        # post second reply
        self.user.last_post_on = None
        self.user.save()

        response = self.client.post(
            self.post_link,
            data={"post": "This is test response, @%s and @%s!" % (user, other_user)},
        )
        self.assertEqual(response.status_code, 200)

        post_b = self.user.post_set.order_by("id").last()

        # merge posts and validate that post A has all mentions
        post_b.merge(post_a)

        self.assertEqual(post_a.mentions.count(), 2)
        self.assertEqual(list(post_a.mentions.order_by("id")), [user, other_user])
