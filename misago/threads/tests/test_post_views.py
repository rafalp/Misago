from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.models import Thread, Post
from misago.threads.testutils import post_thread, reply_thread


class PostViewTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(PostViewTestCase, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.forum.labels = []

        self.thread = post_thread(self.forum)

    def override_acl(self, new_acl, forum=None):
        new_acl.update({
            'can_see': True,
            'can_browse': True,
            'can_see_all_threads': True,
            'can_see_own_threads': False
        })

        forum = forum or self.forum

        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(forum.pk)
        forums_acl['forums'][forum.pk] = new_acl
        override_acl(self.user, forums_acl)


class UnhidePostViewTests(PostViewTestCase):
    def test_unhide_first_post(self):
        """attempt to reveal first post in thread fails"""
        post_link = reverse('misago:unhide_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_unhide_post_no_permission(self):
        """view fails due to lack of permissions"""
        post = reply_thread(self.thread, is_hidden=True)
        post_link = reverse('misago:unhide_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 0, 'can_hide_own_posts': 0})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_unhide_post(self):
        """view reveals post"""
        post = reply_thread(self.thread, is_hidden=True)
        post_link = reverse('misago:unhide_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 302)

        post = Post.objects.get(id=post.id)
        self.assertFalse(post.is_hidden)


class HidePostViewTests(PostViewTestCase):
    def test_hide_first_post(self):
        """attempt to hide first post in thread fails"""
        post_link = reverse('misago:hide_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_hide_post_no_permission(self):
        """view fails due to lack of permissions"""
        post = reply_thread(self.thread)
        post_link = reverse('misago:hide_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 0, 'can_hide_own_posts': 0})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_hide_post(self):
        """view hides post"""
        post = reply_thread(self.thread)
        post_link = reverse('misago:hide_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 302)

        post = Post.objects.get(id=post.id)
        self.assertTrue(post.is_hidden)


class DeletePostViewTests(PostViewTestCase):
    def test_delete_first_post(self):
        """attempt to delete first post in thread fails"""
        post_link = reverse('misago:delete_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_delete_post_no_permission(self):
        """view fails due to lack of permissions"""
        post = reply_thread(self.thread)
        post_link = reverse('misago:delete_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 0, 'can_hide_own_posts': 0})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_delete_post(self):
        """view deletes post"""
        post = reply_thread(self.thread)
        post_link = reverse('misago:delete_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 302)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(thread.first_post_id, thread.last_post_id)
        self.assertEqual(thread.replies, 0)

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)
