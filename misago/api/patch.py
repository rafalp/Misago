from __future__ import unicode_literals

from rest_framework.exceptions import ValidationError as ApiValidationError
from rest_framework.response import Response

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.http import Http404
from django.utils import six
from django.utils.translation import gettext as _


ALLOWED_OPS = ('add', 'remove', 'replace')


class InvalidAction(Exception):
    pass


HANDLED_EXCEPTIONS = (
    ApiValidationError,
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
        if not isinstance(request.data, list):
            return Response({
                'detail': _("PATCH request should be a list of operations."),
            }, status=400)

        response = {'id': target.pk}
        for action in request.data:
            try:
                self.validate_action(action)
                self.dispatch_action(response, request, target, action)
            except HANDLED_EXCEPTIONS as exception:
                detail, status = self.get_error_detail_code(exception)
                return Response({'detail': detail}, status=status)

        return Response(response)

    def dispatch_bulk(self, request, targets):
        result = []

        for action in request.data['ops']:
            try:
                self.validate_action(action)
            except InvalidAction as exception:
                detail, status = self.get_error_detail_code(exception)
                return Response({'detail': detail}, status=status)

        for target in targets:
            patch = {'id': target.pk, 'status': 200}
            for action in request.data['ops']:
                try:
                    self.dispatch_action(patch, request, target, action)
                except HANDLED_EXCEPTIONS as exception:
                    detail, status = self.get_error_detail_code(exception)
                    patch = {
                        'id': target.pk,
                        'detail': detail,
                        'status': status,
                    }
                    break
            result.append(patch)

        # always returning 200 on op error saves us logic duplication
        # in the frontend, were we need to do success handling in both
        # success and error handles
        return Response(result)

    def validate_action(self, action):
        if not action.get('op'):
            raise InvalidAction(_('"op" parameter must be defined.'))

        if action.get('op') not in ALLOWED_OPS:
            raise InvalidAction(_('"%s" op is unsupported.') % action.get('op'))

        if not action.get('path'):
            raise InvalidAction(_('"%s" op has to specify path.') % action.get('op'))

        if 'value' not in action:
            raise InvalidAction(_('"%s" op has to specify value.') % action.get('op'))

    def dispatch_action(self, patch, request, target, action):
        for handler in self._actions:
            if action['op'] == handler['op'] and action['path'] == handler['path']:
                with transaction.atomic():
                    patch.update(handler['handler'](request, target, action['value']))

    def get_error_detail_code(self, exception):
        if isinstance(exception, InvalidAction):
            return six.text_type(exception), 400

        if isinstance(exception, ApiValidationError):
            return exception.detail, 400

        if isinstance(exception, ValidationError):
            return exception.messages, 400

        if isinstance(exception, PermissionDenied):
            return six.text_type(exception), 403

        if isinstance(exception, Http404):
            return six.text_type(exception) or "NOT FOUND", 404
