from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import TestCase

from ..apipatch import ApiPatch, InvalidAction


class MockRequest:
    def __init__(self, data=None):
        self.data = data


class MockObject:
    def __init__(self, pk):
        self.id = pk
        self.pk = pk


class ApiPatchTests(TestCase):
    def test_add(self):
        """add method adds function to patch object"""
        patch = ApiPatch()

        def mock_function():
            pass

        patch.add("test-add", mock_function)

        self.assertEqual(len(patch._actions), 1)
        self.assertEqual(patch._actions[0]["op"], "add")
        self.assertEqual(patch._actions[0]["path"], "test-add")
        self.assertEqual(patch._actions[0]["handler"], mock_function)

    def test_remove(self):
        """remove method adds function to patch object"""
        patch = ApiPatch()

        def mock_function():
            pass

        patch.remove("test-remove", mock_function)

        self.assertEqual(len(patch._actions), 1)
        self.assertEqual(patch._actions[0]["op"], "remove")
        self.assertEqual(patch._actions[0]["path"], "test-remove")
        self.assertEqual(patch._actions[0]["handler"], mock_function)

    def test_replace(self):
        """replace method adds function to patch object"""
        patch = ApiPatch()

        def mock_function():
            pass

        patch.replace("test-replace", mock_function)

        self.assertEqual(len(patch._actions), 1)
        self.assertEqual(patch._actions[0]["op"], "replace")
        self.assertEqual(patch._actions[0]["path"], "test-replace")
        self.assertEqual(patch._actions[0]["handler"], mock_function)

    def test_validate_action(self):
        """validate_action method validates action dict"""
        patch = ApiPatch()

        VALID_ACTIONS = [
            {"op": "add", "path": "test", "value": 42},
            {"op": "remove", "path": "other-test", "value": "Lorem"},
            {"op": "replace", "path": "false-test", "value": None},
        ]

        for action in VALID_ACTIONS:
            patch.validate_action(action)

        # undefined op
        UNSUPPORTED_ACTIONS = ({}, {"op": ""}, {"no": "op"})

        for action in UNSUPPORTED_ACTIONS:
            try:
                patch.validate_action(action)
            except InvalidAction as e:
                self.assertEqual(e.args[0], "undefined op")

        # unsupported op
        try:
            patch.validate_action({"op": "nope"})
        except InvalidAction as e:
            self.assertEqual(e.args[0], '"nope" op is unsupported')

        # op lacking patch
        try:
            patch.validate_action({"op": "add"})
        except InvalidAction as e:
            self.assertEqual(e.args[0], '"add" op has to specify path')

        # op lacking value
        try:
            patch.validate_action({"op": "add", "path": "yolo"})
        except InvalidAction as e:
            self.assertEqual(e.args[0], '"add" op has to specify value')

        # empty value is allowed
        try:
            patch.validate_action({"op": "add", "path": "yolo", "value": ""})
        except InvalidAction as e:
            self.assertEqual(e.args[0], '"add" op has to specify value')

    def test_dispatch_action(self):
        """dispatch_action calls specified actions"""
        patch = ApiPatch()

        mock_target = MockObject(13)

        def action_a(request, target, value):
            self.assertEqual(request, "request")
            self.assertEqual(target, mock_target)
            return {"a": value * 2, "b": 111}

        patch.replace("abc", action_a)

        def action_b(request, target, value):
            self.assertEqual(request, "request")
            self.assertEqual(target, mock_target)
            return {"b": value * 10}

        patch.replace("abc", action_b)

        def action_fail(request, target, value):
            self.fail("unrequired action was called")

        patch.add("c", action_fail)
        patch.remove("c", action_fail)
        patch.replace("c", action_fail)

        patch_dict = {"id": 123}

        patch.dispatch_action(
            patch_dict,
            "request",
            mock_target,
            {"op": "replace", "path": "abc", "value": 5},
        )

        self.assertEqual(len(patch_dict), 3)
        self.assertEqual(patch_dict["id"], 123)
        self.assertEqual(patch_dict["a"], 10)
        self.assertEqual(patch_dict["b"], 50)

    def test_dispatch(self):
        """dispatch calls actions and returns response"""
        patch = ApiPatch()

        def action_error(request, target, value):
            if value == "404":
                raise Http404()
            if value == "perm":
                raise PermissionDenied("yo ain't doing that!")

        patch.replace("error", action_error)

        def action_mutate(request, target, value):
            return {"value": value * 2}

        patch.replace("mutate", action_mutate)

        # dispatch requires list as an argument
        response = patch.dispatch(MockRequest({}), {})
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.data["detail"], "PATCH request should be list of operations"
        )

        # valid dispatch
        response = patch.dispatch(
            MockRequest(
                [
                    {"op": "replace", "path": "mutate", "value": 2},
                    {"op": "replace", "path": "mutate", "value": 6},
                    {"op": "replace", "path": "mutate", "value": 7},
                ]
            ),
            MockObject(13),
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data["detail"]), 3)
        self.assertEqual(response.data["detail"][0], "ok")
        self.assertEqual(response.data["detail"][1], "ok")
        self.assertEqual(response.data["detail"][2], "ok")
        self.assertEqual(response.data["id"], 13)
        self.assertEqual(response.data["value"], 14)

        # invalid action in dispatch
        response = patch.dispatch(
            MockRequest(
                [
                    {"op": "replace", "path": "mutate", "value": 2},
                    {"op": "replace", "path": "mutate", "value": 6},
                    {"op": "replace"},
                    {"op": "replace", "path": "mutate", "value": 7},
                ]
            ),
            MockObject(13),
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(len(response.data["detail"]), 3)
        self.assertEqual(response.data["detail"][0], "ok")
        self.assertEqual(response.data["detail"][1], "ok")
        self.assertEqual(response.data["detail"][2], '"replace" op has to specify path')
        self.assertEqual(response.data["id"], 13)
        self.assertEqual(response.data["value"], 12)

        # action in dispatch raised 404
        response = patch.dispatch(
            MockRequest(
                [
                    {"op": "replace", "path": "mutate", "value": 2},
                    {"op": "replace", "path": "error", "value": "404"},
                    {"op": "replace", "path": "mutate", "value": 6},
                    {"op": "replace", "path": "mutate", "value": 7},
                ]
            ),
            MockObject(13),
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(len(response.data["detail"]), 2)
        self.assertEqual(response.data["detail"][0], "ok")
        self.assertEqual(response.data["detail"][1], "NOT FOUND")
        self.assertEqual(response.data["id"], 13)
        self.assertEqual(response.data["value"], 4)

        # action in dispatch raised perm denied
        response = patch.dispatch(
            MockRequest(
                [
                    {"op": "replace", "path": "mutate", "value": 2},
                    {"op": "replace", "path": "mutate", "value": 6},
                    {"op": "replace", "path": "mutate", "value": 9},
                    {"op": "replace", "path": "error", "value": "perm"},
                ]
            ),
            MockObject(13),
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(len(response.data["detail"]), 4)
        self.assertEqual(response.data["detail"][0], "ok")
        self.assertEqual(response.data["detail"][1], "ok")
        self.assertEqual(response.data["detail"][2], "ok")
        self.assertEqual(response.data["detail"][3], "yo ain't doing that!")
        self.assertEqual(response.data["id"], 13)
        self.assertEqual(response.data["value"], 18)
