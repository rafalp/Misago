from django.test import TestCase

from ..models import Role
from ..testutils import fake_post_data


class FakeTestDataTests(TestCase):
    def test_fake_post_data_for_role(self):
        """fake data was created for Role"""
        test_data = fake_post_data(Role(), {'can_fly': 1})

        self.assertIn('can_fly', test_data)
