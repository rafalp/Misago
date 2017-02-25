# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.markup.mentions import MENTIONS_LIMIT
from misago.threads import testutils
from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class PostMentionsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(PostMentionsTests, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)
        self.override_acl()

        self.post_link = reverse(
            'misago:api:thread-post-list', kwargs={
                'thread_pk': self.thread.pk,
            }
        )

    def override_acl(self):
        new_acl = self.user.acl_cache
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 1,
            'can_reply_threads': 1,
            'can_edit_posts': 1,
        })

        override_acl(self.user, new_acl)

    def put(
            self,
            url,
            data=None,
    ):
        content = encode_multipart(BOUNDARY, data or {})
        return self.client.put(url, content, content_type=MULTIPART_CONTENT)

    def test_mention_noone(self):
        """endpoint handles no mentions in post"""
        response = self.client.post(
            self.post_link, data={
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by('id').last()
        self.assertEqual(post.mentions.count(), 0)

    def test_mention_nonexistant(self):
        """endpoint handles nonexistant mention"""
        response = self.client.post(
            self.post_link, data={
                'post': "This is test response, @InvalidUser!",
            }
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by('id').last()
        self.assertEqual(post.mentions.count(), 0)

    def test_mention_self(self):
        """endpoint mentions author"""
        response = self.client.post(
            self.post_link, data={
                'post': "This is test response, @{}!".format(self.user),
            }
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by('id').last()

        self.assertEqual(post.mentions.count(), 1)
        self.assertEqual(post.mentions.all()[0], self.user)

    def test_mention_limit(self):
        """endpoint mentions limits mentions to 24 users"""
        users = []

        for i in range(MENTIONS_LIMIT + 5):
            users.append(
                UserModel.objects.
                create_user('Mention{}'.format(i), 'mention{}@bob.com'.format(i), 'pass123')
            )

        mentions = ['@{}'.format(u) for u in users]
        response = self.client.post(
            self.post_link,
            data={
                'post': "This is test response, {}!".format(', '.join(mentions)),
            }
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by('id').last()

        self.assertEqual(post.mentions.count(), 24)
        self.assertEqual(list(post.mentions.order_by('id')), users[:24])

    def test_mention_update(self):
        """edit post endpoint updates mentions"""
        user_a = UserModel.objects.create_user('Mention', 'mention@test.com', 'pass123')
        user_b = UserModel.objects.create_user('MentionB', 'mentionb@test.com', 'pass123')

        response = self.client.post(
            self.post_link, data={
                'post': "This is test response, @{}!".format(user_a),
            }
        )
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.order_by('id').last()

        self.assertEqual(post.mentions.count(), 1)
        self.assertEqual(post.mentions.order_by('id')[0], user_a)

        # add mention to post
        edit_link = reverse(
            'misago:api:thread-post-detail', kwargs={
                'thread_pk': self.thread.pk,
                'pk': post.pk,
            }
        )

        self.override_acl()
        response = self.put(
            edit_link,
            data={
                'post': "This is test response, @{} and @{}!".format(user_a, user_b),
            }
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(post.mentions.count(), 2)
        self.assertEqual(list(post.mentions.order_by('id')), [user_a, user_b])

        # remove first mention from post - should preserve mentions
        self.override_acl()
        response = self.put(
            edit_link, data={
                'post': "This is test response, @{}!".format(user_b),
            }
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(post.mentions.count(), 2)
        self.assertEqual(list(post.mentions.order_by('id')), [user_a, user_b])

        # remove mentions from post - should preserve mentions
        self.override_acl()
        response = self.put(
            edit_link, data={
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(post.mentions.count(), 2)
        self.assertEqual(list(post.mentions.order_by('id')), [user_a, user_b])

    def test_mentions_merge(self):
        """posts merge sums mentions"""
        user_a = UserModel.objects.create_user('Mention', 'mention@test.com', 'pass123')
        user_b = UserModel.objects.create_user('MentionB', 'mentionb@test.com', 'pass123')

        response = self.client.post(
            self.post_link, data={
                'post': "This is test response, @{}!".format(user_a),
            }
        )
        self.assertEqual(response.status_code, 200)

        post_a = self.user.post_set.order_by('id').last()

        self.assertEqual(post_a.mentions.count(), 1)
        self.assertEqual(list(post_a.mentions.all()), [user_a])

        # post second reply
        self.user.last_post_on = None
        self.user.save()

        response = self.client.post(
            self.post_link,
            data={
                'post': "This is test response, @{} and @{}!".format(user_a, user_b),
            }
        )
        self.assertEqual(response.status_code, 200)

        post_b = self.user.post_set.order_by('id').last()

        # merge posts and validate that post A has all mentions
        post_b.merge(post_a)

        self.assertEqual(post_a.mentions.count(), 2)
        self.assertEqual(list(post_a.mentions.order_by('id')), [user_a, user_b])
