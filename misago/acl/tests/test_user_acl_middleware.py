from unittest.mock import Mock

from ..middleware import user_acl_middleware


def test_middleware_sets_attr_on_request(cache_versions, user):
    get_response = Mock()
    request = Mock(user=user, cache_versions=cache_versions)
    middleware = user_acl_middleware(get_response)
    middleware(request)
    assert request.user_acl


def test_middleware_calls_get_response(cache_versions, user):
    get_response = Mock()
    request = Mock(user=user, cache_versions=cache_versions)
    middleware = user_acl_middleware(get_response)
    middleware(request)
    get_response.assert_called_once()
