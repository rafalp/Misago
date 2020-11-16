from ...models import Role
from ..test import mock_role_form_data


def test_factory_for_change_role_permissions_form_data():
    test_data = mock_role_form_data(Role(), {"can_fly": 1})
    assert "can_fly" in test_data
