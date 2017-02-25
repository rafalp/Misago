from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404


ALLOWED_OPS = ('add', 'remove', 'replace')


class InvalidAction(Exception):
    pass


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
                'detail': "PATCH request should be list of operations",
            }, status=400)

        detail = []
        is_errored = False

        patch = {'id': target.pk}
        for action in request.data:
            try:
                self.validate_action(action)
                self.dispatch_action(patch, request, target, action)
                detail.append('ok')
            except Http404:
                is_errored = True
                detail.append('NOT FOUND')
                break
            except (InvalidAction, PermissionDenied) as e:
                is_errored = True
                detail.append(e.args[0])
                break

        patch['detail'] = detail
        if is_errored:
            return Response(patch, status=400)
        else:
            return Response(patch)

    def validate_action(self, action):
        if not action.get('op'):
            raise InvalidAction(u"undefined op")

        if action.get('op') not in ALLOWED_OPS:
            raise InvalidAction(u'"%s" op is unsupported' % action.get('op'))

        if not action.get('path'):
            raise InvalidAction(u'"%s" op has to specify path' % action.get('op'))

        if 'value' not in action:
            raise InvalidAction(u'"%s" op has to specify value' % action.get('op'))

    def dispatch_action(self, patch, request, target, action):
        for handler in self._actions:
            if action['op'] == handler['op'] and action['path'] == handler['path']:
                with transaction.atomic():
                    patch.update(handler['handler'](request, target, action['value']))
