from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404

from rest_framework.response import Response


ALLOWED_OPS = ('add', 'remove', 'replace')


class InvalidAction(Exception):
    pass


class ApiPatchRouter(object):
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
        try:
            return Response(self.run_actions(request, target))
        except Http404:
            pass
        except PermissionDenied as e:
            pass
        except InvalidAction as e:
            pass
        return Response({})

    def run_actions(self, request, target):
        if not isinstance(request.data, list):
            raise InvalidAction("PATCH request should be list of operations")

        for action in request.data:
            self.validate_action(action)
            return self.dispatch_action(request, target, action)

    def validate_action(self, action):
        if action.get('op') not in ALLOWED_OPS:
            if action.get('op'):
                raise InvalidAction(
                    u"\"%s\" op is unsupported" % action.get('op'))
            else:
                raise InvalidAction(u"server didn't receive valid op")

        if not action.get('path'):
            raise InvalidAction(
                u"\"%s\" op has to define path" % action.get('op'))

        if 'value' not in action:
            raise InvalidAction(
                u"\"%s\" op has to define value" % action.get('op'))

    def dispatch_action(self, request, target, action):
        patch = {'id': target.pk}
        for handler in self._actions:
            if (action['op'] == handler['op'] and
                    action['path'] == handler['path']):
                with transaction.atomic():
                    patch.update(
                        handler['handler'](request, target, action['value'])
                    )
        return patch