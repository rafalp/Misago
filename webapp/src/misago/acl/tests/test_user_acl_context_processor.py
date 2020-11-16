from unittest.mock import Mock

from ..context_processors import user_acl


def test_context_processor_adds_request_user_acl_to_context():
    test_acl = {"test": True}
    context = user_acl(Mock(user_acl=test_acl))
    assert context == {"user_acl": test_acl}
