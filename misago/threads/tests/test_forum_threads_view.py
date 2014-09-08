from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import testutils
from misago.threads.models import Label
from misago.threads.views.generic.forum import ForumFiltering, ForumThreads


class ForumViewHelperTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ForumViewHelperTestCase, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.forum.labels = []

    def override_acl(self, new_acl):
        new_acl.update({'can_browse': True})

        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = new_acl
        override_acl(self.user, forums_acl)
        add_acl(self.user, self.forum)


class ForumFilteringTests(ForumViewHelperTestCase):
    def test_get_available_filters(self):
        """get_available_filters returns filters varying on forum acl"""
        default_acl = {
            'can_see_all_threads': False,
            'can_see_reports': False,
            'can_review_moderated_content': False,
        }

        cases = (
            ('can_see_all_threads', 'my-threads'),
            ('can_see_reports', 'reported'),
            ('can_review_moderated_content', 'moderated-threads'),
        )

        for permission, filter_type in cases:
            self.override_acl(default_acl)
            filtering = ForumFiltering(self.forum, 'misago:forum', {
                'forum_id': self.forum.id,
                'forum_slug': self.forum.slug,
            })

            available_filters = filtering.get_available_filters()
            available_filters = [f['type'] for f in available_filters]
            self.assertNotIn(filter_type, available_filters)

            acl = default_acl.copy()
            acl[permission] = True
            self.override_acl(acl)

            filtering = ForumFiltering(self.forum, 'misago:forum', {
                'forum_id': self.forum.id,
                'forum_slug': self.forum.slug,
            })

            available_filters = filtering.get_available_filters()
            available_filters = [f['type'] for f in available_filters]
            self.assertIn(filter_type, available_filters)

        self.forum.labels = [
            Label(name='Label A', slug='label-a'),
            Label(name='Label B', slug='label-b'),
            Label(name='Label C', slug='label-c'),
            Label(name='Label D', slug='label-d'),
        ]

        self.override_acl(default_acl)
        ForumFiltering(self.forum, 'misago:forum', {
                'forum_id': self.forum.id,
                'forum_slug': self.forum.slug,
            })

        available_filters = filtering.get_available_filters()
        available_filters = [f['type'] for f in available_filters]

        self.assertEqual(len(available_filters), len(self.forum.labels))
        for label in self.forum.labels:
            self.assertIn(label.slug, available_filters)

    def test_clean_kwargs(self):
        """clean_kwargs cleans kwargs"""
        self.override_acl({
            'can_see_all_threads': True,
            'can_see_reports': True,
            'can_review_moderated_content': True,
        })

        filtering = ForumFiltering(self.forum, 'misago:forum', {
            'forum_id': self.forum.id,
            'forum_slug': self.forum.slug,
        })

        available_filters = filtering.get_available_filters()
        available_filters = [f['type'] for f in available_filters]

        clean_kwargs = filtering.clean_kwargs({'test': 'kwarg'})
        self.assertEqual(clean_kwargs, {'test': 'kwarg'})

        clean_kwargs = filtering.clean_kwargs({
            'test': 'kwarg',
            'show': 'everything-hue-hue',
        })
        self.assertEqual(clean_kwargs, {'test': 'kwarg'})
        self.assertFalse(filtering.is_active)
        self.assertIsNone(filtering.show)

        for filter_type in available_filters:
            clean_kwargs = filtering.clean_kwargs({
                'test': 'kwarg',
                'show': filter_type,
            })

            self.assertEqual(clean_kwargs, {
                'test': 'kwarg',
                'show': filter_type,
            })
            self.assertTrue(filtering.is_active)
            self.assertEqual(filtering.show, filter_type)

    def test_current(self):
        """current returns dict with current filter"""
        self.override_acl({
            'can_see_all_threads': True,
            'can_see_reports': True,
            'can_review_moderated_content': True,
        })

        test_cases = (
            ('my-threads', _("My threads")),
            ('reported', _("With reported posts")),
            ('moderated-threads', _("Moderated threads")),
            ('moderated-posts', _("With moderated posts")),
        )

        for filter_type, name in test_cases:
            filtering = ForumFiltering(self.forum, 'misago:forum', {
                'forum_id': self.forum.id,
                'forum_slug': self.forum.slug,
            })
            filtering.clean_kwargs({'show': filter_type})
            self.assertEqual(filtering.current['name'], name)

    def test_choices(self):
        """choices returns list of dicts with available filters"""
        self.override_acl({
            'can_see_all_threads': True,
            'can_see_reports': True,
            'can_review_moderated_content': True,
        })

        test_cases = (
            'my-threads',
            'reported',
            'moderated-threads',
            'moderated-posts',
        )

        for filter_type in test_cases:
            filtering = ForumFiltering(self.forum, 'misago:forum', {
                'forum_id': self.forum.id,
                'forum_slug': self.forum.slug,
            })
            filtering.clean_kwargs({'show': filter_type})

            choices = [choice['type'] for choice in filtering.choices()]
            self.assertNotIn(filter_type, choices)


class ForumThreadsTests(ForumViewHelperTestCase):
    def test_empty_list(self):
        """list returns empty list of items"""
        self.override_acl({
            'can_see_all_threads': True,
            'can_review_moderated_content': False
        })

        threads = ForumThreads(self.user, self.forum)
        threads_list = threads.list()

        self.assertEqual(threads_list, [])

    def test_list_exception(self):
        """
        uninitialized list raises exceptions when
        page and paginator attributes are accessed
        """
        self.override_acl({
            'can_see_all_threads': False,
            'can_review_moderated_content': False
        })

        threads = ForumThreads(self.user, self.forum)

        with self.assertRaises(AttributeError):
            threads.page

        with self.assertRaises(AttributeError):
            threads.paginator

    def test_list_with_threads(self):
        """list returns list of visible threads"""
        test_threads = [
            testutils.post_thread(
                forum=self.forum,
                title="Hello, I am thread",
                is_moderated=False,
                poster=self.user),
            testutils.post_thread(
                forum=self.forum,
                title="Hello, I am moderated thread",
                is_moderated=True,
                poster=self.user),
            testutils.post_thread(
                forum=self.forum,
                title="Hello, I am other user thread",
                is_moderated=False,
                poster="Bob"),
            testutils.post_thread(
                forum=self.forum,
                title="Hello, I am other user moderated thread",
                is_moderated=True,
                poster="Bob"),
        ]

        self.override_acl({
            'can_see_all_threads': False,
            'can_review_moderated_content': False
        })

        threads = ForumThreads(self.user, self.forum)
        self.assertEqual(threads.list(), [test_threads[1], test_threads[0]])

        self.override_acl({
            'can_see_all_threads': True,
            'can_review_moderated_content': False
        })

        threads = ForumThreads(self.user, self.forum)
        self.assertEqual(threads.list(),
                         [test_threads[2], test_threads[1], test_threads[0]])

        self.override_acl({
            'can_see_all_threads': True,
            'can_review_moderated_content': True
        })

        threads = ForumThreads(self.user, self.forum)
        test_threads.reverse()
        self.assertEqual(threads.list(), test_threads)

        self.assertTrue(threads.page)
        self.assertTrue(threads.paginator)


class ForumThreadsAuthenticatedTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ForumThreadsAuthenticatedTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.link = self.forum.get_absolute_url()
        self.forum.delete_content()

    def override_acl(self, new_acl):
        forums_acl = self.user.acl
        if new_acl['can_see']:
            forums_acl['visible_forums'].append(self.forum.pk)
        else:
            forums_acl['visible_forums'].remove(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = new_acl
        override_acl(self.user, forums_acl)

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
            poster=self.user)

        owned_moderated_title = "Test authenticated user moderated thread"
        testutils.post_thread(
            forum=self.forum,
            title=owned_moderated_title,
            poster=self.user,
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
            poster=self.user)

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
            poster=self.user)

        owned_moderated_title = "Test authenticated user moderated thread"
        testutils.post_thread(
            forum=self.forum,
            title=owned_moderated_title,
            poster=self.user,
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
            poster=self.user)

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
