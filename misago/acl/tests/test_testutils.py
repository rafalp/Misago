from misago.acl.models import Role
from misago.acl.testutils import fake_post_data


def test_fake_post_data_for_role():
    """fake data was created for Role"""
    test_data = fake_post_data(Role(), {'can_fly': 1})
    assert "can_fly" in test_data
