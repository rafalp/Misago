from __future__ import unicode_literals

from rest_framework.exceptions import ValidationError as ApiValidationError

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.test import TestCase

from misago.api.patch import ApiPatch, InvalidAction


class MockRequest(object):
    def __init__(self, ops):
        self.data = {'ops': ops}


class MockObject(object):
    def __init__(self, pk):
        self.id = pk
        self.pk = pk


class ApiPatchDispatchBulkTests(TestCase):
    def test_dispatch_bulk(self):
        """dispatch_bulk calls actions and returns response"""
        patch = ApiPatch()

        def action_error(request, target, value):
            if value == '404':
                raise Http404()
            if value == '404_reason':
                raise Http404("something was removed")
            if value == 'perm':
                raise PermissionDenied("yo ain't doing that!")
            if value == 'invalid':
                raise ValidationError("invalid data here!")
            if value == 'api_invalid':
                raise ApiValidationError("invalid api data here!")

        patch.replace('error', action_error)

        def action_mutate(request, target, value):
            return {'value': value * 2}

        patch.replace('mutate', action_mutate)

        # valid bulk dispatch
        response = patch.dispatch_bulk(
            MockRequest([
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 2,
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 6,
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 7,
                },
            ]),
            [MockObject(5), MockObject(7)],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {'id': 5, 'value': 14, 'status': 200},
            {'id': 7, 'value': 14, 'status': 200},
        ])

        # invalid action in bulk dispatch
        response = patch.dispatch_bulk(
            MockRequest([
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 2,
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 6,
                },
                {
                    'op': 'replace',
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 7,
                },
            ]),
            [MockObject(5), MockObject(7)],
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], '"replace" op has to specify path.')

        # op raised validation error
        response = patch.dispatch_bulk(
            MockRequest([
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 2,
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 6,
                },
                {
                    'op': 'replace',
                    'path': 'error',
                    'value': 'invalid',
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 7,
                },
            ]),
            [MockObject(5), MockObject(7)],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {'id': 5, 'detail': ["invalid data here!"], 'status': 400},
            {'id': 7, 'detail': ["invalid data here!"], 'status': 400},
        ])

        # op raised api validation error
        response = patch.dispatch_bulk(
            MockRequest([
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 2,
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 6,
                },
                {
                    'op': 'replace',
                    'path': 'error',
                    'value': 'api_invalid',
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 7,
                },
            ]),
            [MockObject(5), MockObject(7)],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {'id': 5, 'detail': ["invalid api data here!"], 'status': 400},
            {'id': 7, 'detail': ["invalid api data here!"], 'status': 400},
        ])

        # action in bulk dispatch raised perm denied
        response = patch.dispatch_bulk(
            MockRequest([
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 2,
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 6,
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 9,
                },
                {
                    'op': 'replace',
                    'path': 'error',
                    'value': 'perm',
                },
            ]),
            [MockObject(5), MockObject(7)],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {'id': 5, 'detail': "yo ain't doing that!", 'status': 403},
            {'id': 7, 'detail': "yo ain't doing that!", 'status': 403},
        ])

        # action in bulk dispatch raised 404
        response = patch.dispatch_bulk(
            MockRequest([
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 2,
                },
                {
                    'op': 'replace',
                    'path': 'error',
                    'value': '404',
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 6,
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 7,
                },
            ]),
            [MockObject(5), MockObject(7)],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {'id': 5, 'detail': "NOT FOUND", 'status': 404},
            {'id': 7, 'detail': "NOT FOUND", 'status': 404},
        ])

        # action in bulk dispatch raised 404 with message
        response = patch.dispatch_bulk(
            MockRequest([
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 2,
                },
                {
                    'op': 'replace',
                    'path': 'error',
                    'value': '404_reason',
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 6,
                },
                {
                    'op': 'replace',
                    'path': 'mutate',
                    'value': 7,
                },
            ]),
            [MockObject(5), MockObject(7)],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {'id': 5, 'detail': "something was removed", 'status': 404},
            {'id': 7, 'detail': "something was removed", 'status': 404},
        ])
