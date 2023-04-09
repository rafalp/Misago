import pytest
from django.core.exceptions import PermissionDenied

from ..permissions import allow_use_notifications


def test_allow_use_notifications_permission_check_passes_authenticated(user):
    allow_use_notifications(user)


def test_allow_use_notifications_permission_check_blocks_anonymous_users(
    anonymous_user,
):
    with pytest.raises(PermissionDenied) as excinfo:
        allow_use_notifications(anonymous_user)

    assert "You must be signed in" in str(excinfo)
