from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import testutils
from misago.threads.models import Thread, Label
from misago.threads.moderation import ModerationError
from misago.threads.views.generic.forum import (ForumActions, ForumFiltering,
                                                ForumThreads)


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

        self.forum.acl = {}
        add_acl(self.user, self.forum)


class MockRequest(object):
    def __init__(self, user, method='GET', POST=None):
        self.POST = POST or {}
        self.user = user
        self.session = {}
        self.path = '/forum/fake-forum-1/'


class ActionsTests(ForumViewHelperTestCase):
    def setUp(self):
        super(ActionsTests, self).setUp()

        self.user._misago_real_ip = '127.0.0.1'
        Label.objects.clear_cache()

    def tearDown(self):
        super(ActionsTests, self).tearDown()
        Label.objects.clear_cache()

    def test_label_actions(self):
        """ForumActions initializes list with label actions"""
        self.override_acl({
            'can_change_threads_labels': 0,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [])

        self.override_acl({
            'can_change_threads_labels': 1,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [])

        self.override_acl({
            'can_change_threads_labels': 2,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [])

        label = Label.objects.create(name="Mock Label", slug="mock-label")
        self.forum.labels = [label]

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [
            {
                'action': 'label:%s' % label.slug,
                'icon': 'tag',
                'name': _('Label as "%(label)s"') % {'label': label.name}
            },
            {
                'action': 'unlabel',
                'icon': 'times-circle',
                'name': _("Remove labels")
            },
        ])

    def test_pin_unpin_actions(self):
        """ForumActions initializes list with pin and unpin actions"""
        self.override_acl({
            'can_pin_threads': 0,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [])

        self.override_acl({
            'can_pin_threads': 1,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [
            {
                'action': 'pin',
                'icon': 'star',
                'name': _("Pin threads")
            },
            {
                'action': 'unpin',
                'icon': 'circle',
                'name': _("Unpin threads")
            },
        ])

    def test_approve_action(self):
        """ForumActions initializes list with approve threads action"""
        self.override_acl({
            'can_review_moderated_content': 0,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [])

        self.override_acl({
            'can_review_moderated_content': 1,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [
            {
                'action': 'approve',
                'icon': 'check',
                'name': _("Approve threads")
            },
        ])

    def test_move_action(self):
        """ForumActions initializes list with move threads action"""
        self.override_acl({
            'can_move_threads': 0,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [])

        self.override_acl({
            'can_move_threads': 1,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [
            {
                'action': 'move',
                'icon': 'arrow-right',
                'name': _("Move threads")
            },
        ])

    def test_merge_action(self):
        """ForumActions initializes list with merge threads action"""
        self.override_acl({
            'can_merge_threads': 0,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [])

        self.override_acl({
            'can_merge_threads': 1,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [
            {
                'action': 'merge',
                'icon': 'reply-all',
                'name': _("Merge threads")
            },
        ])

    def test_close_open_actions(self):
        """ForumActions initializes list with close and open actions"""
        self.override_acl({
            'can_close_threads': 0,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [])

        self.override_acl({
            'can_close_threads': 1,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [
            {
                'action': 'open',
                'icon': 'unlock-alt',
                'name': _("Open threads")
            },
            {
                'action': 'close',
                'icon': 'lock',
                'name': _("Close threads")
            },
        ])

    def test_hide_delete_actions(self):
        """ForumActions initializes list with hide/delete actions"""
        self.override_acl({
            'can_hide_threads': 0,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [])

        self.override_acl({
            'can_hide_threads': 1,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [
            {
                'action': 'unhide',
                'icon': 'eye',
                'name': _("Unhide threads")
            },
            {
                'action': 'hide',
                'icon': 'eye-slash',
                'name': _("Hide threads")
            },
        ])

        self.override_acl({
            'can_hide_threads': 2,
        })

        actions = ForumActions(user=self.user, forum=self.forum)
        self.assertEqual(actions.available_actions, [
            {
                'action': 'unhide',
                'icon': 'eye',
                'name': _("Unhide threads")
            },
            {
                'action': 'hide',
                'icon': 'eye-slash',
                'name': _("Hide threads")
            },
            {
                'action': 'delete',
                'icon': 'times',
                'name': _("Delete threads"),
                'confirmation': _("Are you sure you want to delete selected "
                                  "threads? This action can't be undone.")
            },
        ])


class ForumFilteringTests(ForumViewHelperTestCase):
    def setUp(self):
        super(ForumFilteringTests, self).setUp()
        Label.objects.clear_cache()

    def tearDown(self):
        super(ForumFilteringTests, self).tearDown()
        Label.objects.clear_cache()

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


class ForumThreadsViewTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ForumThreadsViewTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.link = self.forum.get_absolute_url()
        self.forum.delete_content()

        Label.objects.clear_cache()

    def tearDown(self):
        super(ForumThreadsViewTests, self).tearDown()
        Label.objects.clear_cache()

    def override_acl(self, new_acl, forum=None):
        forum = forum or self.forum

        forums_acl = self.user.acl
        if new_acl['can_see']:
            forums_acl['visible_forums'].append(forum.pk)
        else:
            forums_acl['visible_forums'].remove(forum.pk)
        forums_acl['forums'][forum.pk] = new_acl
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

    def test_anonymous_request(self):
        """view renders to anonymous users"""
        anon_title = "Hello Anon!"
        testutils.post_thread(forum=self.forum, title=anon_title)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(anon_title, response.content)

    def test_change_threads_labels(self):
        """moderation allows for changing threads labels"""
        threads = [testutils.post_thread(self.forum) for t in xrange(10)]

        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_change_threads_labels': 2
        }

        labels = [
            Label(name='Label A', slug='label-a'),
            Label(name='Label B', slug='label-b'),
        ]
        for label in labels:
            label.save()
            label.forums.add(self.forum)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Remove labels", response.content)

        # label threads with invalid label
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'label:mehssiah', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Requested action is invalid.", response.content)

        # label threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'label:%s' % labels[0].slug,
            'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("10 threads were labeled", response.content)

        # label labeled threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'label:%s' % labels[0].slug,
            'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads were labeled.", response.content)

        # relabel labeled threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'label:%s' % labels[1].slug,
            'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("10 threads were labeled", response.content)

        # remove labels from threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'unlabel', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("10 threads labels were removed", response.content)

        # remove labels from unlabeled threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'unlabel', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads were unlabeled.", response.content)

    def test_pin_unpin_threads(self):
        """moderation allows for pinning and unpinning threads"""
        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_pin_threads': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Pin threads", response.content)

        pinned = testutils.post_thread(self.forum, is_pinned=True)
        thread = testutils.post_thread(self.forum, is_pinned=False)

        # pin nothing
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={'action': 'pin'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("You have to select at least one thread.",
                      response.content)

        # pin pinned
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'pin', 'thread': [pinned.pk]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads were pinned.",
                      response.content)

        # pin unpinned
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'pin', 'thread': [pinned.pk, thread.pk]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("1 thread was pinned.",
                      response.content)

        pinned = Thread.objects.get(pk=pinned.pk)
        thread = Thread.objects.get(pk=thread.pk)

        self.assertTrue(pinned.is_pinned)
        self.assertTrue(thread.is_pinned)

        # unpin thread
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'unpin', 'thread': [thread.pk]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("1 thread was unpinned.", response.content)

        pinned = Thread.objects.get(pk=pinned.pk)
        thread = Thread.objects.get(pk=thread.pk)

        self.assertTrue(pinned.is_pinned)
        self.assertFalse(thread.is_pinned)

    def test_approve_moderated_threads(self):
        """moderation allows for aproving moderated threads"""
        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_review_moderated_content': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Approve threads", response.content)

        thread = testutils.post_thread(self.forum, is_moderated=False)
        moderated_thread = testutils.post_thread(self.forum, is_moderated=True)

        # approve approved thread
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'approve', 'thread': [thread.pk]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads were approved.", response.content)

        # approve moderated thread
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'approve', 'thread': [moderated_thread.pk]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("1 thread was approved.", response.content)

    def test_move_threads(self):
        """moderation allows for moving threads"""
        new_forum = Forum(name="New Forum",
                          slug="new-forum",
                          role="forum")
        new_forum.insert_at(self.forum, save=True)

        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_move_threads': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Move threads", response.content)

        threads = [testutils.post_thread(self.forum) for t in xrange(10)]

        # see move threads form
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'move', 'thread': [t.pk for t in threads[:5]]
        })
        self.assertEqual(response.status_code, 200)

        for thread in threads[:5]:
            self.assertIn(thread.title, response.content)

        # submit form with non-existing forum
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'move',
            'thread': [t.pk for t in threads[:5]],
            'submit': '',
            'new_forum': new_forum.pk + 1234
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Select valid forum.", response.content)

        # attempt move to category
        self.override_acl(test_acl)

        category = Forum.objects.all_forums().filter(role="category")[:1][0]
        response = self.client.post(self.link, data={
            'action': 'move',
            'thread': [t.pk for t in threads[:5]],
            'submit': '',
            'new_forum': category.pk
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("You can&#39;t move threads to category.",
                      response.content)

        # attempt move to redirect
        self.override_acl(test_acl)

        redirect = Forum.objects.all_forums().filter(role="redirect")[:1][0]
        response = self.client.post(self.link, data={
            'action': 'move',
            'thread': [t.pk for t in threads[:5]],
            'submit': '',
            'new_forum': redirect.pk
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("You can&#39;t move threads to redirect.",
                      response.content)

        # move to new_forum
        self.override_acl(test_acl)
        self.override_acl(test_acl, new_forum)
        response = self.client.post(self.link, data={
            'action': 'move',
            'thread': [t.pk for t in threads[:5]],
            'submit': '',
            'new_forum': new_forum.pk
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("5 threads were moved to &quot;New Forum&quot;.",
                      response.content)

        for thread in new_forum.thread_set.all():
            self.assertIn(thread, threads[:5])
        for thread in self.forum.thread_set.all():
            self.assertIn(thread, threads[5:])

    def test_merge_threads(self):
        """moderation allows for merging threads"""
        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_merge_threads': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Merge threads", response.content)

        threads = [testutils.post_thread(self.forum) for t in xrange(10)]

        # see merge threads form
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'merge', 'thread': [t.pk for t in threads[:5]]
        })
        self.assertEqual(response.status_code, 200)

        # submit form with empty title
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'merge',
            'thread': [t.pk for t in threads[:5]],
            'submit': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("You have to enter merged thread title.",
                      response.content)

        # submit form with one thread selected
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'merge',
            'thread': [threads[0].pk],
            'submit': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("You have to select at least two threads to merge.",
                      response.content)

        # submit form with valid title
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'merge',
            'thread': [t.pk for t in threads[:5]],
            'merged_thread_title': 'Merged thread',
            'submit': ''
        })
        self.assertEqual(response.status_code, 302)

        # see if merged thread is there
        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Merged thread", response.content)

        # assert that merged threads are gone
        for thread in threads[:5]:
            self.assertNotIn(thread.get_absolute_url(), response.content)

        # assert that non-merged threads were untouched
        for thread in threads[5:]:
            self.assertIn(thread.get_absolute_url(), response.content)

    def test_close_open_threads(self):
        """moderation allows for closing and opening threads"""
        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_close_threads': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Close threads", response.content)
        self.assertIn("Open threads", response.content)

        threads = [testutils.post_thread(self.forum) for t in xrange(10)]

        # close threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'close', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("10 threads were closed.", response.content)

        # close closed threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'close', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads were closed.", response.content)

        # open closed threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'open', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("10 threads were opened.", response.content)

        # open opened threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'open', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads were opened.", response.content)

    def test_hide_unhide_threads(self):
        """moderation allows for hiding and unhiding threads"""
        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_hide_threads': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Unhide threads", response.content)
        self.assertIn("Hide threads", response.content)

        threads = [testutils.post_thread(self.forum) for t in xrange(10)]

        # hide threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'hide', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("10 threads were hidden.", response.content)

        # hide hidden threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'hide', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads were hidden.", response.content)

        # unhide hidden threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'unhide', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("10 threads were made visible.", response.content)

        # unhide visible threads
        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'unhide', 'thread': [t.pk for t in threads]
        })
        self.assertEqual(response.status_code, 302)

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads were made visible.", response.content)

    def test_delete_threads(self):
        """moderation allows for deleting threads"""
        threads = [testutils.post_thread(self.forum) for t in xrange(10)]

        self.forum.synchronize()
        self.assertEqual(self.forum.threads, 10)

        test_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_hide_threads': 2
        }

        self.override_acl(test_acl)
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Delete threads", response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.link, data={
            'action': 'delete', 'thread': [t.pk for t in threads]
        })

        forum = Forum.objects.get(pk=self.forum.pk)
        self.assertEqual(forum.threads, 0)
