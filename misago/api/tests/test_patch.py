from __future__ import unicode_literals

from django.test import TestCase

from misago.api.patch import ApiPatch, InvalidAction


class MockObject(object):
    def __init__(self, pk):
        self.id = pk
        self.pk = pk


class ApiPatchTests(TestCase):
    def test_add(self):
        """add method adds function to patch object"""
        patch = ApiPatch()

        def mock_function():
            pass

        patch.add('test-add', mock_function)

        self.assertEqual(len(patch._actions), 1)
        self.assertEqual(patch._actions[0]['op'], 'add')
        self.assertEqual(patch._actions[0]['path'], 'test-add')
        self.assertEqual(patch._actions[0]['handler'], mock_function)

    def test_remove(self):
        """remove method adds function to patch object"""
        patch = ApiPatch()

        def mock_function():
            pass

        patch.remove('test-remove', mock_function)

        self.assertEqual(len(patch._actions), 1)
        self.assertEqual(patch._actions[0]['op'], 'remove')
        self.assertEqual(patch._actions[0]['path'], 'test-remove')
        self.assertEqual(patch._actions[0]['handler'], mock_function)

    def test_replace(self):
        """replace method adds function to patch object"""
        patch = ApiPatch()

        def mock_function():
            pass

        patch.replace('test-replace', mock_function)

        self.assertEqual(len(patch._actions), 1)
        self.assertEqual(patch._actions[0]['op'], 'replace')
        self.assertEqual(patch._actions[0]['path'], 'test-replace')
        self.assertEqual(patch._actions[0]['handler'], mock_function)

    def test_validate_action(self):
        """validate_action method validates action dict"""
        patch = ApiPatch()

        VALID_ACTIONS = [
            {
                'op': 'add',
                'path': 'test',
                'value': 42
            },
            {
                'op': 'remove',
                'path': 'other-test',
                'value': 'Lorem'
            },
            {
                'op': 'replace',
                'path': 'false-test',
                'value': None
            },
        ]

        for action in VALID_ACTIONS:
            patch.validate_action(action)

        # undefined op
        UNSUPPORTED_ACTIONS = ({}, {'op': ''}, {'no': 'op'}, )

        for action in UNSUPPORTED_ACTIONS:
            try:
                patch.validate_action(action)
            except InvalidAction as e:
                self.assertEqual(e.args[0], '"op" parameter must be defined.')

        # unsupported op
        try:
            patch.validate_action({'op': 'nope'})
        except InvalidAction as e:
            self.assertEqual(e.args[0], u'"nope" op is unsupported.')

        # op lacking patch
        try:
            patch.validate_action({'op': 'add'})
        except InvalidAction as e:
            self.assertEqual(e.args[0], u'"add" op has to specify path.')

        # op lacking value
        try:
            patch.validate_action({
                'op': 'add',
                'path': 'yolo',
            })
        except InvalidAction as e:
            self.assertEqual(e.args[0], u'"add" op has to specify value.')

        # empty value is allowed
        try:
            patch.validate_action({
                'op': 'add',
                'path': 'yolo',
                'value': '',
            })
        except InvalidAction as e:
            self.assertEqual(e.args[0], u'"add" op has to specify value.')

    def test_dispatch_action(self):
        """dispatch_action calls specified actions"""
        patch = ApiPatch()

        mock_target = MockObject(13)

        def action_a(request, target, value):
            self.assertEqual(request, 'request')
            self.assertEqual(target, mock_target)
            return {'a': value * 2, 'b': 111}

        patch.replace('abc', action_a)

        def action_b(request, target, value):
            self.assertEqual(request, 'request')
            self.assertEqual(target, mock_target)
            return {'b': value * 10}

        patch.replace('abc', action_b)

        def action_fail(request, target, value):
            self.fail("unrequired action was called")

        patch.add('c', action_fail)
        patch.remove('c', action_fail)
        patch.replace('c', action_fail)

        patch_dict = {'id': 123}

        patch.dispatch_action(
            patch_dict, 'request', mock_target, {
                'op': 'replace',
                'path': 'abc',
                'value': 5,
            }
        )

        self.assertEqual(len(patch_dict), 3)
        self.assertEqual(patch_dict['id'], 123)
        self.assertEqual(patch_dict['a'], 10)
        self.assertEqual(patch_dict['b'], 50)
