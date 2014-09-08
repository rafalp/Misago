from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.admin.testutils import AdminTestCase
from misago.forums.models import Forum

from misago.threads import testutils


class ForumThreadsAuthenticatedTests(AdminTestCase):
    def setUp(self):
        super(ForumThreadsAuthenticatedTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.link = self.forum.get_absolute_url()
        self.forum.delete_content()

    def override_acl(self, new_acl):
        forums_acl = self.test_admin.acl
        if new_acl['can_see']:
            forums_acl['visible_forums'].append(self.forum.pk)
        else:
            forums_acl['visible_forums'].remove(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = new_acl
        override_acl(self.test_admin, forums_acl)

    def test_cant_see(self):
        """has no permission to see forum"""
        self.override_acl({
            'can_see': 0,
            'can_browse': 0,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 404)

    def test_cant_browse(self):
        """has no permission to browse forum"""
        self.override_acl({
            'can_see': 1,
            'can_browse': 0,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)

    def test_can_browse_empty(self):
        """has permission to browse forum, sees empty list"""
        self.override_acl({
            'can_see': 1,
            'can_browse': 1,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads", response.content)

    def test_owned_threads_visibility(self):
        """
        can_see_all_threads=0 displays only owned threads to authenticated user
        """
        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 0,
            'can_review_moderated_content': 0,
        }

        other_moderated_title = "Test other user moderated thread"
        testutils.post_thread(
            forum=self.forum, title=other_moderated_title, is_moderated=True)

        other_title = "Test other user thread"
        testutils.post_thread(forum=self.forum, title=other_title)

        owned_title = "Test authenticated user thread"
        testutils.post_thread(
            forum=self.forum,
            title=owned_title,
            poster=self.test_admin)

        owned_moderated_title = "Test authenticated user moderated thread"
        testutils.post_thread(
            forum=self.forum,
            title=owned_moderated_title,
            poster=self.test_admin,
            is_moderated=True)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(other_title, response.content)
        self.assertNotIn(other_moderated_title, response.content)
        self.assertIn(owned_title, response.content)
        self.assertIn(owned_moderated_title, response.content)
        self.assertNotIn('show-my-threads', response.content)

    def test_moderated_threads_visibility(self):
        """moderated threads are not rendered to non-moderator, except owned"""
        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_review_moderated_content': 0,
        }

        test_title = "Test moderated thread"
        thread = testutils.post_thread(
            forum=self.forum, title=test_title, is_moderated=True)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_title, response.content)

        test_title = "Test owned moderated thread"
        thread = testutils.post_thread(
            forum=self.forum,
            title=test_title,
            is_moderated=True,
            poster=self.test_admin)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_title, response.content)

    def test_owned_threads_filter(self):
        """owned threads filter is available to authenticated user"""
        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_review_moderated_content': 0,
        }

        other_moderated_title = "Test other user moderated thread"
        testutils.post_thread(
            forum=self.forum, title=other_moderated_title, is_moderated=True)

        other_title = "Test other user thread"
        testutils.post_thread(forum=self.forum, title=other_title)

        owned_title = "Test authenticated user thread"
        testutils.post_thread(
            forum=self.forum,
            title=owned_title,
            poster=self.test_admin)

        owned_moderated_title = "Test authenticated user moderated thread"
        testutils.post_thread(
            forum=self.forum,
            title=owned_moderated_title,
            poster=self.test_admin,
            is_moderated=True)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(other_title, response.content)
        self.assertNotIn(other_moderated_title, response.content)
        self.assertIn(owned_title, response.content)
        self.assertIn(owned_moderated_title, response.content)
        self.assertIn('show-my-threads', response.content)

        self.override_acl(test_acl)
        response = self.client.get(reverse('misago:forum', kwargs={
                'forum_id': self.forum.id,
                'forum_slug': self.forum.slug,
                'show': 'my-threads',
            }))

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(other_title, response.content)
        self.assertNotIn(other_moderated_title, response.content)
        self.assertIn(owned_title, response.content)
        self.assertIn(owned_moderated_title, response.content)

    def test_moderated_threads_filter(self):
        """moderated threads filter is available to moderator"""
        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_review_moderated_content': 0,
        }

        not_moderated_title = "Not moderated thread"
        testutils.post_thread(forum=self.forum, title=not_moderated_title)

        hidden_title = "Test moderated thread"
        testutils.post_thread(
            forum=self.forum, title=hidden_title, is_moderated=True)

        visible_title = "Test owned moderated thread"
        testutils.post_thread(
            forum=self.forum,
            title=visible_title,
            is_moderated=True,
            poster=self.test_admin)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(not_moderated_title, response.content)
        self.assertNotIn(hidden_title, response.content)
        self.assertIn(visible_title, response.content)
        self.assertNotIn('show-moderated-threads', response.content)
        self.assertNotIn('show-moderated-posts', response.content)

        self.override_acl(test_acl)
        response = self.client.get(reverse('misago:forum', kwargs={
                'forum_id': self.forum.id,
                'forum_slug': self.forum.slug,
                'show': 'moderated-threads',
            }))
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(reverse('misago:forum', kwargs={
                'forum_id': self.forum.id,
                'forum_slug': self.forum.slug,
                'show': 'moderated-posts',
            }))
        self.assertEqual(response.status_code, 302)

        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_review_moderated_content': 1,
        }

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(not_moderated_title, response.content)
        self.assertIn(hidden_title, response.content)
        self.assertIn(visible_title, response.content)
        self.assertIn('show-moderated-threads', response.content)
        self.assertIn('show-moderated-posts', response.content)

        self.override_acl(test_acl)
        response = self.client.get(reverse('misago:forum', kwargs={
                'forum_id': self.forum.id,
                'forum_slug': self.forum.slug,
                'show': 'moderated-threads',
            }))

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(not_moderated_title, response.content)
        self.assertIn(hidden_title, response.content)
        self.assertIn(visible_title, response.content)
        self.assertIn('show-moderated-threads', response.content)
        self.assertIn('show-moderated-posts', response.content)
