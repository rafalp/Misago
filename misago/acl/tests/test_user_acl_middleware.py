from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.acl.middleware import user_acl_middleware

User = get_user_model()

cache_versions = {"acl": "abcdefgh"}


class MiddlewareTests(TestCase):
    def test_middleware_sets_attr_on_request(self):
        user = User.objects.create_user("User", "user@example.com")

        get_response = Mock()
        request = Mock(user=user, cache_versions=cache_versions)
        middleware = user_acl_middleware(get_response)
        middleware(request)
        assert request.user_acl

    def test_middleware_calls_get_response(self):
        user = User.objects.create_user("User", "user@example.com")
        get_response = Mock()
        request = Mock(user=user, cache_versions=cache_versions)
        middleware = user_acl_middleware(get_response)
        middleware(request)
        get_response.assert_called_once()
