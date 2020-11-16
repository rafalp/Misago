from unittest.mock import Mock

from ..context_processors import preload_socialauth_json


def test_context_processor_sets_socialauth_entry_in_frontend_context():
    request = Mock(frontend_context={}, socialauth={})
    preload_socialauth_json(request)
    assert "SOCIAL_AUTH" in request.frontend_context
