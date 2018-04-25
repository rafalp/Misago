from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.settings import api_settings

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.http import Http404
from django.utils import six
from django.utils.translation import gettext as _


ALLOWED_OPS = ('add', 'remove', 'replace')


class InvalidAction(Exception):
    pass


HANDLED_EXCEPTIONS = (
    serializers.ValidationError,
    ValidationError,
    InvalidAction,
    PermissionDenied,
    Http404,
)


class ApiPatch(object):
    def __init__(self):
        self._actions = []

    def add(self, path, handler):
        self._actions.append({
            'op': 'add',
            'path': path,
            'handler': handler,
        })

    def remove(self, path, handler):
        self._actions.append({
            'op': 'remove',
            'path': path,
            'handler': handler,
        })

    def replace(self, path, handler):
        self._actions.append({
            'op': 'replace',
            'path': path,
            'handler': handler,
        })

    def dispatch(self, request, target):
        response = {'id': target.pk}

        try:
            self.validate_actions(request.data)
        except HANDLED_EXCEPTIONS as exception:
            return self.handle_exception(exception)

        for action in request.data:
            try:
                self.dispatch_action(response, request, target, action)
            except HANDLED_EXCEPTIONS as exception:
                return self.handle_exception(exception)

        return Response(response)

    def dispatch_bulk(self, request, targets):
        try:
            self.validate_actions(request.data['ops'])
        except HANDLED_EXCEPTIONS as exception:
            return self.handle_exception(exception)

        result = []
        for target in targets:
            data = {'id': target.pk, 'status': 200, 'patch': {}}
            for action in request.data['ops']:
                try:
                    self.dispatch_action(data['patch'], request, target, action)
                except HANDLED_EXCEPTIONS as exception:
                    data, status = self.get_error_data_status(exception)
                    data.update({'id': target.pk, 'status': status, })
                    break
            result.append(data)

        # sort result items by id then cast id and status to string
        # so we are compliant with our bulk actions spec
        result.sort(key=lambda item: item['id'])
        for data in result:
            data['id'] = str(data['id'])
            data['status'] = str(data['status'])

        # always returning 200 on op error saves us logic duplication
        # in the frontend, were we need to do success handling in both
        # success and error handles
        return Response(result)

    def validate_actions(self, actions):
        if not isinstance(actions, list):
            raise InvalidAction(_("PATCH request should be a list of operations."))

        reduced_actions = []
        for action in actions:
            self.validate_action(action)

            reduced_action = self.reduce_action(action)
            if reduced_action in reduced_actions:
                raise InvalidAction(
                    _('"%(op)s" op for "%(path)s" path is repeated.') % reduced_action)
            reduced_actions.append(reduced_action)

    def validate_action(self, action):
        if not action.get('op'):
            raise InvalidAction(_('"op" parameter must be defined.'))

        if action.get('op') not in ALLOWED_OPS:
            raise InvalidAction(_('"%s" op is unsupported.') % action.get('op'))

        if not action.get('path'):
            raise InvalidAction(_('"%s" op has to specify path.') % action.get('op'))

        if 'value' not in action:
            raise InvalidAction(_('"%s" op has to specify value.') % action.get('op'))

    def reduce_action(self, action):
        return {'op': action['op'], 'path': action['path']}

    def dispatch_action(self, data, request, target, action):
        for handler in self._actions:
            if action['op'] == handler['op'] and action['path'] == handler['path']:
                with transaction.atomic():
                    data.update(handler['handler'](request, target, action['value']))

    def handle_exception(self, exception):
        data, status = self.get_error_data_status(exception)
        return Response(data, status=status)

    def get_error_data_status(self, exception):
        if isinstance(exception, InvalidAction):
            return {api_settings.NON_FIELD_ERRORS_KEY: [six.text_type(exception)]}, 400

        if isinstance(exception, serializers.ValidationError):
            return {'value': exception.detail}, 400

        if isinstance(exception, ValidationError):
            return {'value': exception.messages}, 400

        if isinstance(exception, PermissionDenied):
            return {'detail': six.text_type(exception)}, 403

        if isinstance(exception, Http404):
            return {'detail': 'NOT FOUND'}, 404
