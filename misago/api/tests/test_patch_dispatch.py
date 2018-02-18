from __future__ import unicode_literals

from rest_framework.exceptions import ValidationError as ApiValidationError

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.test import TestCase

from misago.api.patch import ApiPatch


class MockRequest(object):
    def __init__(self, data=None):
        self.data = data


class MockObject(object):
    def __init__(self, pk):
        self.id = pk
        self.pk = pk


class ApiPatchDispatchTests(TestCase):
    def test_dispatch(self):
        """dispatch calls actions and returns response"""
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

        # dispatch requires list as an argument
        response = patch.dispatch(MockRequest({}), {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], "PATCH request should be a list of operations.")

        # valid dispatch
        response = patch.dispatch(
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
            ]), MockObject(13)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'value': 14, 'id': 13})

        # invalid action in dispatch
        response = patch.dispatch(
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
            ]), MockObject(13)
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], '"replace" op has to specify path.')

        # op raised validation error
        response = patch.dispatch(
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
            ]), MockObject(13)
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], ["invalid data here!"])

        # op raised api validation error
        response = patch.dispatch(
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
            ]), MockObject(13)
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], ["invalid api data here!"])

        # action in dispatch raised perm denied
        response = patch.dispatch(
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
            ]), MockObject(13)
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], "yo ain't doing that!")

        # action in dispatch raised 404
        response = patch.dispatch(
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
            ]), MockObject(13)
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], "NOT FOUND")

        # action in dispatch raised 404 with message
        response = patch.dispatch(
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
            ]), MockObject(13)
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], "something was removed")
