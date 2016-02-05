from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.conf import settings
from misago.core import threadstore
from misago.core.cache import cache
from misago.forums.models import Forum
from misago.threads.testutils import post_thread

from misago.users.models import Online, Rank
from misago.users.testutils import AuthenticatedUserTestCase


class ActivePostersListTests(AuthenticatedUserTestCase):
    """
    tests for active posters list (GET /users/?list=active)
    """
    def setUp(self):
        super(ActivePostersListTests, self).setUp()
        self.link = '/api/users/?list=active'

        cache.clear()
        threadstore.clear()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.forum.labels = []

    def test_empty_list(self):
        """empty list is served"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user.username, response.content)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user.username, response.content)

    def test_filled_list(self):
        """filled list is served"""
        post_thread(self.forum, poster=self.user)
        self.user.posts = 1
        self.user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username, response.content)
        self.assertIn('"is_online":true', response.content)
        self.assertIn('"is_offline":false', response.content)

        self.logout_user()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username, response.content)
        self.assertIn('"is_online":false', response.content)
        self.assertIn('"is_offline":true', response.content)


class RankListTests(AuthenticatedUserTestCase):
    """
    tests for rank list (GET /users/?list=rank&rank=slug)
    """
    def setUp(self):
        super(RankListTests, self).setUp()
        self.link = '/api/users/?list=rank&rank='

    def test_nonexistent_rank(self):
        """list for non-existing rank returns 404"""
        response = self.client.get(self.link + 'this-rank-is-non-existing')
        self.assertEqual(response.status_code, 404)

    def test_empty_list(self):
        """tab rank without members returns 200"""
        rank_slug = self.user.rank.slug

        self.user.rank = Rank.objects.filter(is_tab=False)[:1][0]
        self.user.rank.save()

        response = self.client.get(self.link + rank_slug)
        self.assertEqual(response.status_code, 404)

    def test_disabled_list(self):
        """non-tab rank with members returns 404"""
        self.user.rank.is_tab = False
        self.user.rank.save()

        response = self.client.get(self.link + self.user.rank.slug)
        self.assertEqual(response.status_code, 404)

    def test_filled_list(self):
        """tab rank with members return 200"""
        self.user.rank.is_tab = True
        self.user.rank.save()

        response = self.client.get(self.link + self.user.rank.slug)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username, response.content)


class UserForumOptionsTests(AuthenticatedUserTestCase):
    """
    tests for user forum options RPC (POST to /api/users/1/forum-options/)
    """
    def setUp(self):
        super(UserForumOptionsTests, self).setUp()
        self.link = '/api/users/%s/forum-options/' % self.user.pk

    def test_empty_request(self):
        """empty request is handled"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 400)

        fields = (
            'limits_private_thread_invites_to',
            'subscribe_to_started_threads',
            'subscribe_to_replied_threads'
        )

        for field in fields:
            self.assertIn('"%s"' % field, response.content)

    def test_change_forum_options(self):
        """forum options are changed"""
        response = self.client.post(self.link, data={
            'limits_private_thread_invites_to': 1,
            'subscribe_to_started_threads': 2,
            'subscribe_to_replied_threads': 1
        })
        self.assertEqual(response.status_code, 200)

        self.reload_user();

        self.assertFalse(self.user.is_hiding_presence)
        self.assertEqual(self.user.limits_private_thread_invites_to, 1)
        self.assertEqual(self.user.subscribe_to_started_threads, 2)
        self.assertEqual(self.user.subscribe_to_replied_threads, 1)
