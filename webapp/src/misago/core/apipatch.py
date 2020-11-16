from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from rest_framework.response import Response

ALLOWED_OPS = ("add", "remove", "replace")


class InvalidAction(Exception):
    pass


class ApiPatch:
    def __init__(self):
        self._actions = []

    def add(self, path, handler):
        self._actions.append({"op": "add", "path": path, "handler": handler})

    def remove(self, path, handler):
        self._actions.append({"op": "remove", "path": path, "handler": handler})

    def replace(self, path, handler):
        self._actions.append({"op": "replace", "path": path, "handler": handler})

    def dispatch(self, request, target):
        if not isinstance(request.data, list):
            return Response(
                {"detail": "PATCH request should be list of operations"}, status=400
            )

        detail = []
        is_errored = False

        patch = {"id": target.pk}
        for action in request.data:
            try:
                self.validate_action(action)
                self.dispatch_action(patch, request, target, action)
                detail.append("ok")
            except Http404:
                is_errored = True
                detail.append("NOT FOUND")
                break
            except (InvalidAction, PermissionDenied) as e:
                is_errored = True
                detail.append(e.args[0])
                break

        patch["detail"] = detail
        if is_errored:
            return Response(patch, status=400)
        return Response(patch)

    def dispatch_bulk(self, request, targets):
        is_errored = False
        result = []

        for target in targets:
            detail = []

            patch = {"id": target.pk}
            for action in request.data["ops"]:
                try:
                    self.validate_action(action)
                    self.dispatch_action(patch, request, target, action)
                except Http404:
                    is_errored = True
                    detail.append("NOT FOUND")
                    break
                except (InvalidAction, PermissionDenied) as e:
                    is_errored = True
                    detail.append(e.args[0])
                    break
            if detail:
                patch["detail"] = detail
            result.append(patch)

        if is_errored:
            return Response(result, status=400)
        return Response(result)

    def validate_action(self, action):
        if not action.get("op"):
            raise InvalidAction("undefined op")

        if action.get("op") not in ALLOWED_OPS:
            raise InvalidAction('"%s" op is unsupported' % action.get("op"))

        if not action.get("path"):
            raise InvalidAction('"%s" op has to specify path' % action.get("op"))

        if "value" not in action:
            raise InvalidAction('"%s" op has to specify value' % action.get("op"))

    def dispatch_action(self, patch, request, target, action):
        for handler in self._actions:
            if action["op"] == handler["op"] and action["path"] == handler["path"]:
                with transaction.atomic():
                    patch.update(handler["handler"](request, target, action["value"]))
