from django.test import TestCase

from misago.threads.moderation import ModerationError
from misago.threads.views.generic.threads import Actions, Sorting

from misago.users.testutils import AuthenticatedUserTestCase


class MockRequest(object):
    def __init__(self, user, method='GET', POST=None):
        self.POST = POST or {}
        self.user = user
        self.session = {}
        self.path = '/cool-threads/'


class MockActions(Actions):
    def get_available_actions(self, kwargs):
        return []

    def action_test(self):
        pass


class ActionsTests(AuthenticatedUserTestCase):
    def test_resolve_valid_action(self):
        """resolve_action returns valid action"""
        actions = MockActions(user=self.user)

        actions.available_actions = [{
            'action': 'test',
            'name': "Test action"
        }]

        resolution = actions.resolve_action(MockRequest(
            user=self.user,
            POST={'action': 'test'},
        ))

        self.assertEqual(resolution[0], actions.action_test)
        self.assertIsNone(resolution[1])

    def test_resolve_arg_action(self):
        """resolve_action returns valid action and argument"""
        actions = MockActions(user=self.user)

        actions.available_actions = [{
            'action': 'test:1234',
            'name': "Test action"
        }]

        resolution = actions.resolve_action(MockRequest(
            user=self.user,
            POST={'action': 'test:1234'},
        ))

        self.assertEqual(resolution[0], actions.action_test)
        self.assertEqual(resolution[1], '1234')

    def test_resolve_invalid_action(self):
        """resolve_action handles invalid actions gracefully"""
        actions = MockActions(user=self.user)

        actions.available_actions = [{
            'action': 'test',
            'name': "Test action"
        }]

        with self.assertRaises(ModerationError):
            resolution = actions.resolve_action(MockRequest(
                user=self.user,
                POST={'action': 'test:1234'},
            ))

        with self.assertRaises(ModerationError):
            resolution = actions.resolve_action(MockRequest(
                user=self.user,
                POST={'action': 'test:1234'},
            ))

        actions.available_actions = [{
            'action': 'test:123',
            'name': "Test action"
        }]

        with self.assertRaises(ModerationError):
            resolution = actions.resolve_action(MockRequest(
                user=self.user,
                POST={'action': 'test'},
            ))

        with self.assertRaises(ModerationError):
            resolution = actions.resolve_action(MockRequest(
                user=self.user,
                POST={'action': 'test:'},
            ))

        with self.assertRaises(ModerationError):
            resolution = actions.resolve_action(MockRequest(
                user=self.user,
                POST={'action': 'test:321'},
            ))

    def test_clean_selection(self):
        """clean_selection clears valid input"""
        actions = MockActions(user=self.user)
        self.assertEqual(actions.clean_selection(['1', '-', '9']), [1, 9])

    def test_clean_invalid_selection(self):
        """clean_selection raises exception for invalid/empty input"""
        actions = MockActions(user=self.user)
        with self.assertRaises(ModerationError):
            actions.clean_selection([])

        with self.assertRaises(ModerationError):
            actions.clean_selection(['abc'])

    def get_list(self):
        """get_list returns list of available actions"""
        actions = MockActions(user=self.user)
        actions.available_actions = [{
            'action': 'test:123',
            'name': "Test action"
        }]
        self.assertEqual(actions.get_list(), actions.available_actions)

    def get_selected_ids(self):
        """get_selected_ids returns list of selected items"""
        actions = MockActions(user=self.user)
        actions.selected_ids = [1, 2, 4, 5, 6]
        self.assertEqual(actions.get_selected_ids(), actions.selected_ids)


class SortingTests(TestCase):
    def setUp(self):
        self.sorting = Sorting('misago:category', {
            'category_slug': "test-category",
            'category_id': 42,
        })

    def test_clean_kwargs_removes_default_sorting(self):
        """clean_kwargs removes default sorting"""
        default_sorting = self.sorting.sortings[0]['method']

        cleaned_kwargs = self.sorting.clean_kwargs({'sort': default_sorting})
        cleaned_kwargs['pie'] = 'yum-yum'
        self.assertEqual(cleaned_kwargs, {'pie': 'yum-yum'})

    def test_clean_kwargs_removes_invalid_sorting(self):
        """clean_kwargs removes invalid sorting"""
        default_sorting = self.sorting.sortings[0]['method']

        cleaned_kwargs = self.sorting.clean_kwargs({'sort': 'bad-sort'})
        cleaned_kwargs['pie'] = 'yum-yum'
        self.assertEqual(cleaned_kwargs, {'pie': 'yum-yum'})

    def test_clean_kwargs_preserves_valid_sorting(self):
        """clean_kwargs preserves valid sorting"""
        default_sorting = self.sorting.sortings[0]['method']

        cleaned_kwargs = self.sorting.clean_kwargs({'sort': 'oldest'})
        cleaned_kwargs['pie'] = 'yum-yum'
        self.assertEqual(cleaned_kwargs, {'sort': 'oldest', 'pie': 'yum-yum'})

    def test_set_sorting_sets_valid_method(self):
        """set_sorting sets valid sorting"""
        for sorting in self.sorting.sortings:
            self.sorting.set_sorting(sorting['method'])
            self.assertEqual(sorting, self.sorting.sorting)
            self.assertEqual(sorting['name'], self.sorting.name)

    def test_choices(self):
        """choices returns set of valid choices"""
        for sorting in self.sorting.sortings:
            self.sorting.set_sorting(sorting['method'])
            choices = [choice['name'] for choice in self.sorting.choices()]
            self.assertNotIn(sorting['name'], choices)

            for other_sorting in self.sorting.sortings:
                if other_sorting != sorting:
                    self.assertIn(other_sorting['name'], choices)
