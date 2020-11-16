import json

from ..useracl import get_user_acl, serialize_user_acl


def test_user_acl_is_serializeable(cache_versions, user):
    acl = get_user_acl(user, cache_versions)
    assert serialize_user_acl(acl)


def test_user_acl_is_json_serializeable(cache_versions, user):
    acl = get_user_acl(user, cache_versions)
    serialized_acl = serialize_user_acl(acl)
    assert json.dumps(serialized_acl)
