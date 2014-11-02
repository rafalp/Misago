import json

from django.conf import settings
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.models import Thread
from misago.threads.testutils import post_thread


class ReplyThreadTests(AuthenticatedUserTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def setUp(self):
        super(ReplyThreadTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.thread = post_thread(self.forum)
        self.link = reverse('misago:reply_thread', kwargs={
            'forum_id': self.forum.id,
            'thread_id': self.thread.id,
        })

    def allow_reply_thread(self, extra_acl=None):
        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_reply_threads': 2,
        }
        if extra_acl:
            forums_acl['forums'][self.forum.pk].update(extra_acl)
        override_acl(self.user, forums_acl)

    def test_cant_see(self):
        """has no permission to see forum"""
        forums_acl = self.user.acl
        forums_acl['visible_forums'].remove(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = {
            'can_see': 0,
            'can_browse': 0,
            'can_see_all_threads': 1,
            'can_reply_threads': 1,
        }
        override_acl(self.user, forums_acl)

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 404)

    def test_cant_browse(self):
        """has no permission to browse forum"""
        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = {
            'can_see': 1,
            'can_browse': 0,
            'can_see_all_threads': 1,
            'can_reply_threads': 1,
        }
        override_acl(self.user, forums_acl)

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_cant_reply_thread_in_locked_forum(self):
        """can't post in closed forum"""
        self.forum.is_closed = True
        self.forum.save()

        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_reply_threads': 1,
        }
        override_acl(self.user, forums_acl)

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_cant_reply_closed_thread(self):
        """can't post in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        self.allow_reply_thread()
        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

        # now let us reply to closed threads
        self.allow_reply_thread({'can_close_threads': 1})
        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

    def test_cant_reply_thread_as_guest(self):
        """guests can't reply threads"""
        self.client.post(reverse(settings.LOGOUT_URL))

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_can_reply_thread(self):
        """can reply to thread"""
        self.allow_reply_thread()
        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        self.allow_reply_thread()
        response = self.client.post(self.link, data={
            'post': 'Hello, I am test reply!',
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        self.allow_reply_thread()
        response = self.client.get(response_dict['post_url'])
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, I am test reply!', response.content)

        updated_user = self.user.lock()
        self.assertEqual(updated_user.threads, 0)
        self.assertEqual(updated_user.posts, 1)

        self.thread = Thread.objects.get(id=self.thread.id)

        self.assertEqual(self.thread.replies, 1)
        self.assertEqual(self.thread.forum_id, self.forum.pk)
        self.assertEqual(self.thread.last_poster_id, updated_user.id)
        self.assertEqual(self.thread.last_poster_name, updated_user.username)
        self.assertEqual(self.thread.last_poster_slug, updated_user.slug)

        last_post = self.user.post_set.all()[:1][0]
        self.assertEqual(last_post.forum_id, self.forum.pk)
        self.assertEqual(last_post.original, 'Hello, I am test reply!')
        self.assertEqual(last_post.poster_id, updated_user.id)
        self.assertEqual(last_post.poster_name, updated_user.username)

        updated_forum = Forum.objects.get(id=self.forum.id)
        self.assertEqual(updated_forum.threads, 1)
        self.assertEqual(updated_forum.posts, 2)
        self.assertEqual(updated_forum.last_thread_id, self.thread.id)
        self.assertEqual(updated_forum.last_thread_title, self.thread.title)
        self.assertEqual(updated_forum.last_thread_slug, self.thread.slug)

        self.assertEqual(updated_forum.last_poster_id, updated_user.id)
        self.assertEqual(updated_forum.last_poster_name,
                         updated_user.username)
        self.assertEqual(updated_forum.last_poster_slug, updated_user.slug)

    def test_can_close_replied_thread(self):
        """can close/open thread while replying to it"""
        prefix = 'misago.threads.posting.threadclose.ThreadCloseFormMiddleware'
        field_name = '%s-is_closed' % prefix

        self.allow_reply_thread({'can_close_threads': 1})
        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn(field_name, response.content)

        self.allow_reply_thread({'can_close_threads': 1})
        response = self.client.post(self.link, data={
            'post': 'Lorem ipsum dolor met!',
            field_name: 1,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Thread.objects.get(id=self.thread.id).is_closed)

        self.user.last_posted_on = None
        self.user.save()

        self.allow_reply_thread({'can_close_threads': 1})
        response = self.client.post(self.link, data={
            'post': 'Lorem ipsum dolor met!',
            field_name: 0,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Thread.objects.get(id=self.thread.id).is_closed)

    def test_can_pin_replied_thread(self):
        """can pin/unpin thread while replying to it"""
        prefix = 'misago.threads.posting.threadpin.ThreadPinFormMiddleware'
        field_name = '%s-is_pinned' % prefix

        self.allow_reply_thread({'can_pin_threads': 1})
        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn(field_name, response.content)

        self.allow_reply_thread({'can_pin_threads': 1})
        response = self.client.post(self.link, data={
            'post': 'Lorem ipsum dolor met!',
            field_name: 1,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Thread.objects.get(id=self.thread.id).is_pinned)

        self.user.last_posted_on = None
        self.user.save()

        self.allow_reply_thread({'can_pin_threads': 1})
        response = self.client.post(self.link, data={
            'post': 'Lorem ipsum dolor met!',
            field_name: 0,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Thread.objects.get(id=self.thread.id).is_pinned)
