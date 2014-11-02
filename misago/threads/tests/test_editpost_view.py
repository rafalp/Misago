import json

from django.conf import settings
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.models import Label, Thread, Post
from misago.threads.testutils import post_thread


class EditPostTests(AuthenticatedUserTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def setUp(self):
        super(EditPostTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.thread = post_thread(self.forum, poster=self.user)
        self.link = reverse('misago:edit_post', kwargs={
            'forum_id': self.forum.id,
            'thread_id': self.thread.id,
            'post_id': self.thread.first_post_id,
        })

        Label.objects.clear_cache()

    def tearDown(self):
        Label.objects.clear_cache()

    def override_forum_acl(self, extra_acl=None):
        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
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

    def test_cant_edit_own_post_in_locked_forum(self):
        """can't edit own post in closed forum"""
        self.forum.is_closed = True
        self.forum.save()

        self.override_forum_acl({'can_edit_threads': 1})

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_cant_edit_other_user_post_in_locked_forum(self):
        """can't edit other user post in closed forum"""
        self.forum.is_closed = True
        self.forum.save()

        self.thread.first_post.poster = None
        self.thread.first_post.save()
        self.thread.synchronize()
        self.thread.save()

        self.override_forum_acl({'can_edit_threads': 2})

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_cant_edit_own_post_in_locked_thread(self):
        """can't edit own post in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        self.override_forum_acl({'can_edit_threads': 1})

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_cant_edit_other_user_post_in_locked_thread(self):
        """can't edit other user post in closed thread"""
        self.override_forum_acl({'can_edit_threads': 2})

        self.thread.first_post.poster = None
        self.thread.first_post.save()
        self.thread.is_closed = True
        self.thread.synchronize()
        self.thread.save()

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_cant_edit_own_post(self):
        """can't edit own post"""
        self.override_forum_acl({'can_edit_posts': 0})

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_cant_edit_other_user_post(self):
        """can't edit other user post"""
        self.override_forum_acl({'can_edit_posts': 1})

        self.thread.first_post.poster = None
        self.thread.first_post.save()
        self.thread.synchronize()
        self.thread.save()

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_cant_edit_protected_post(self):
        """can't edit post that was protected by moderator"""
        self.override_forum_acl({'can_edit_posts': 1, 'can_protect_posts': 0})

        self.thread.first_post.is_protected = True
        self.thread.first_post.save()

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_can_edit_own_post(self):
        """can edit own post"""
        self.override_forum_acl({'can_edit_posts': 1, 'can_edit_threads': 0})

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('thread-title', response.content)

        self.override_forum_acl({'can_edit_posts': 1, 'can_edit_threads': 0})
        response = self.client.post(self.link, data={
            'post': 'Edited reply!',
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        post = Post.objects.get(id=self.thread.first_post_id)
        self.assertEqual(post.original, 'Edited reply!')
        self.assertEqual(post.edits, 1)

    def test_can_edit_other_user_post(self):
        """can edit other user post"""
        self.override_forum_acl({'can_edit_posts': 2, 'can_edit_threads': 0})

        self.thread.first_post.poster = None
        self.thread.first_post.save()
        self.thread.synchronize()
        self.thread.save()

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('thread-title', response.content)

        self.override_forum_acl({'can_edit_posts': 2, 'can_edit_threads': 0})
        response = self.client.post(self.link, data={
            'post': 'Edited reply!',
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        post = Post.objects.get(id=self.thread.first_post_id)
        self.assertEqual(post.original, 'Edited reply!')
        self.assertEqual(post.edits, 1)

    def test_can_edit_own_thread(self):
        """can edit own thread"""
        self.override_forum_acl({'can_edit_posts': 1, 'can_edit_threads': 1})

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('thread-title', response.content)

        self.override_forum_acl({'can_edit_posts': 1, 'can_edit_threads': 1})
        response = self.client.post(self.link, data={
            'title': 'Edited title!',
            'post': self.thread.first_post.original,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(thread.title, 'Edited title!')

        post = Post.objects.get(id=self.thread.first_post_id)
        self.assertEqual(post.original, self.thread.first_post.original)
        self.assertEqual(post.edits, 1)

    def test_can_edit_other_user_thread(self):
        """can edit other user thread"""
        self.override_forum_acl({'can_edit_posts': 2, 'can_edit_threads': 2})

        self.thread.first_post.poster = None
        self.thread.first_post.save()
        self.thread.synchronize()
        self.thread.save()

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('thread-title', response.content)

        self.override_forum_acl({'can_edit_posts': 2, 'can_edit_threads': 2})
        response = self.client.post(self.link, data={
            'title': 'Edited title!',
            'post': self.thread.first_post.original,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(thread.title, 'Edited title!')

        post = Post.objects.get(id=self.thread.first_post_id)
        self.assertEqual(post.original, self.thread.first_post.original)
        self.assertEqual(post.edits, 1)

    def test_no_change_edit(self):
        """user edited post but submited no changes"""
        self.override_forum_acl({'can_edit_posts': 1, 'can_edit_threads': 1})

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn('thread-title', response.content)

        self.override_forum_acl({'can_edit_posts': 1, 'can_edit_threads': 1})
        response = self.client.post(self.link, data={
            'title': self.thread.title,
            'post': self.thread.first_post.original,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        post = Post.objects.get(id=self.thread.first_post_id)
        self.assertEqual(post.original, self.thread.first_post.original)
        self.assertEqual(post.edits, 0)

    def test_close_and_open_edit(self):
        """user edited post to close and open thread"""
        prefix = 'misago.threads.posting.threadclose.ThreadCloseFormMiddleware'
        field_name = '%s-is_closed' % prefix
        self.override_forum_acl({'can_edit_posts': 1, 'can_close_threads': 1})

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn(field_name, response.content)

        self.override_forum_acl({'can_edit_posts': 1, 'can_close_threads': 1})
        response = self.client.post(self.link, data={
            'post': self.thread.first_post.original,
            field_name: 1,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertTrue(thread.is_closed)

        self.user.last_posted_on = None
        self.user.save()

        self.override_forum_acl({'can_edit_posts': 1, 'can_close_threads': 1})
        response = self.client.post(self.link, data={
            'post': self.thread.first_post.original,
            field_name: 0,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertFalse(thread.is_closed)

    def test_pin_and_unpin_edit(self):
        """user edited post to pin and unpin thread"""
        prefix = 'misago.threads.posting.threadpin.ThreadPinFormMiddleware'
        field_name = '%s-is_pinned' % prefix
        self.override_forum_acl({'can_edit_posts': 1, 'can_pin_threads': 1})

        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn(field_name, response.content)

        self.override_forum_acl({'can_edit_posts': 1, 'can_pin_threads': 1})
        response = self.client.post(self.link, data={
            'post': self.thread.first_post.original,
            field_name: 1,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertTrue(thread.is_pinned)

        self.user.last_posted_on = None
        self.user.save()

        self.override_forum_acl({'can_edit_posts': 1, 'can_pin_threads': 1})
        response = self.client.post(self.link, data={
            'post': self.thread.first_post.original,
            field_name: 0,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content)
        self.assertIn('post_url', response_dict)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertFalse(thread.is_pinned)

    def test_label_and_unlabel_edit(self):
        """user edited thread to label and unlabel it"""
        prefix = 'misago.threads.posting.threadlabel.ThreadLabelFormMiddleware'
        field_name = '%s-label' % prefix

        label = Label.objects.create(name="Label", slug="label")
        label.forums.add(self.forum)

        acls = {
            'can_edit_posts': 1,
            'can_edit_threads': 1,
            'can_change_threads_labels': 1
        }
        self.override_forum_acl(acls)
        response = self.client.get(self.link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn(field_name, response.content)

        self.override_forum_acl(acls)
        response = self.client.post(self.link, data={
            field_name: label.pk,
            'title': self.thread.title,
            'post': self.thread.first_post.original,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(thread.label_id, label.id)

        self.user.last_posted_on = None
        self.user.save()

        self.override_forum_acl(acls)
        response = self.client.post(self.link, data={
            field_name: 0,
            'title': self.thread.title,
            'post': self.thread.first_post.original,
            'submit': True,
        },
        **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertIsNone(thread.label_id)
