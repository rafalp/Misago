import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.acl.useracl import get_user_acl, serialize_user_acl

User = get_user_model()

cache_versions = {"acl": "abcdefgh"}


class SerializingUserACLTests(TestCase):
    def test_user_acl_is_serializeable(self):
        user = User.objects.create_user('Bob', 'bob@bob.com')
        acl = get_user_acl(user, cache_versions)
        assert serialize_user_acl(acl)

    def test_user_acl_is_json_serializeable(self):
        user = User.objects.create_user('Bob', 'bob@bob.com')
        acl = get_user_acl(user, cache_versions)
        serialized_acl = serialize_user_acl(acl)
        assert json.dumps(serialized_acl)
